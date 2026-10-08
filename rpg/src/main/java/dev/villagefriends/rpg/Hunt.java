package dev.villagefriends.rpg;

import net.fabricmc.fabric.api.tag.convention.v2.ConventionalBlockTags;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.BlockTags;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.tags.ItemTags;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.damagesource.DamageTypes;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.animal.Animal;
import net.minecraft.world.entity.boss.enderdragon.EnderDragon;
import net.minecraft.world.entity.monster.Enemy;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.projectile.arrow.ThrownTrident;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.enchantment.EnchantmentHelper;
import net.minecraft.world.item.enchantment.Enchantments;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.CropBlock;
import net.minecraft.world.level.block.NetherWartBlock;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

/** Combat and gathering: damage scaling, kills, masteries, bonus drops, and skill experience from blocks. */
public final class Hunt {
    private Hunt() {}
    /** Recent kills per player and family, for kill fatigue; decayed by {@link Life#tick}. */
    static final Map<UUID, Map<String, Integer>> RECENT = new HashMap<>();
    private static final Set<String> FLYING = Set.of("ghast", "phantom", "blaze", "breeze", "vex", "bat", "bee", "allay");
    static void clear() { RECENT.clear(); }

    static String path(LivingEntity e) { return BuiltInRegistries.ENTITY_TYPE.getKey(e.getType()).getPath(); }
    static Bestiary.Family family(LivingEntity e) { return Bestiary.ofMob(path(e)); }

    // -- damage ------------------------------------------------------------------------------------
    /** Called at the start of every hurt: scales damage dealt by players and damage taken by them. */
    public static float adjust(LivingEntity target, DamageSource source, float amount) {
        if (amount <= 0 || !(target.level() instanceof ServerLevel level)) return amount;
        if (target instanceof ServerPlayer p) amount = incoming(p, source, amount);
        if (source.getEntity() instanceof ServerPlayer p && p != target) amount = outgoing(p, target, source, amount, level);
        return amount;
    }
    private static float incoming(ServerPlayer p, DamageSource src, float amount) {
        var s = Rpg.sheet(p); double r = 0;
        if (src.getEntity() instanceof LivingEntity attacker) { var f = family(attacker); if (f != null) r += Bestiary.TIER_RESIST * s.tier(f); }
        if (src.is(DamageTypeTags.IS_EXPLOSION)) r += s.perk("resist", "explosion");
        if (src.is(DamageTypeTags.IS_FIRE)) r += s.perk("resist", "fire");
        if (src.is(DamageTypes.MAGIC) || src.is(DamageTypes.INDIRECT_MAGIC)) r += s.perk("resist", "magic");
        if (src.is(DamageTypeTags.IS_FALL)) r += s.perk("resist", "fall");
        if (src.is(DamageTypes.SONIC_BOOM)) r += s.perk("resist", "sonic");
        if (src.is(DamageTypes.DRAGON_BREATH) || src.getEntity() instanceof EnderDragon) r += s.perk("resist", "dragon");
        return r <= 0 ? amount : Balance.incoming(amount, r);
    }
    private static float outgoing(ServerPlayer p, LivingEntity target, DamageSource src, float amount, ServerLevel level) {
        boolean projectile = src.is(DamageTypeTags.IS_PROJECTILE), melee = !projectile && src.is(DamageTypeTags.IS_PLAYER_ATTACK);
        if (!projectile && !melee) return amount;
        var s = Rpg.sheet(p); double m;
        if (melee) {
            var held = p.getMainHandItem();
            m = Balance.meleeBase(s.level()) + Balance.STR_MELEE * s.attr(Attr.STRENGTH);
            if (held.is(ItemTags.SWORDS)) m += Balance.SWORD_DAMAGE * s.skill(Skill.SWORDS);
            else if (held.is(ItemTags.AXES)) m += Balance.AXE_DAMAGE * s.skill(Skill.AXES);
            if (p.getRandom().nextDouble() < Balance.PRE_CRIT * s.attr(Attr.PRECISION)) {
                m += Balance.CRIT_BONUS;
                level.sendParticles(ParticleTypes.ENCHANTED_HIT, target.getX(), target.getY(.6), target.getZ(), 12, .3, .3, .3, .2);
                level.playSound(null, target.blockPosition(), SoundEvents.PLAYER_ATTACK_CRIT, SoundSource.PLAYERS, 1, 1.3F);
            }
        } else {
            m = 1 + Balance.PRE_PROJECTILE * s.attr(Attr.PRECISION) + Balance.ARCHERY_DAMAGE * s.skill(Skill.ARCHERY) + s.perk("damage", "projectile");
            if (src.getDirectEntity() instanceof ThrownTrident) m += s.perk("damage", "trident");
        }
        var f = family(target);
        boolean boss = f != null && f.boss();
        if (f != null) m += Bestiary.TIER_DAMAGE * s.tier(f);
        if (boss) m += s.perk("damage", "boss");
        if (level.dimension() == Level.NETHER) m += s.perk("damage", "nether");
        if (FLYING.contains(path(target))) m += s.perk("damage", "flying");
        if (level.isRaided(target.blockPosition())) m += s.perk("damage", "raid");
        return Balance.outgoing(amount, m, boss, target.getMaxHealth());
    }
    /** Pearl Thrift: ender pearls don't hurt at all. */
    static boolean allowDamage(LivingEntity entity, DamageSource source, float amount) {
        return !(entity instanceof ServerPlayer p && source.is(DamageTypes.ENDER_PEARL) && Rpg.sheet(p).perk("resist", "pearl") >= 1);
    }
    /** Skill experience from hits given and taken. */
    static void afterDamage(LivingEntity entity, DamageSource source, float base, float taken, boolean blocked) {
        if (entity instanceof ServerPlayer p) {
            if (blocked) Progress.skill(p, Skill.DEFENSE, base * 1.5);
            if (taken > 0 && source.is(DamageTypeTags.IS_FALL)) Progress.skill(p, Skill.ACROBATICS, taken * 5);
            else if (taken > 0 && wearsArmor(p)) Progress.skill(p, Skill.DEFENSE, Math.min(taken, 20) * 2);
        }
        if (taken > 0 && source.getEntity() instanceof ServerPlayer p && p != entity && (entity instanceof Enemy || entity instanceof Animal)) {
            var skill = weaponSkill(p, source);
            if (skill != null) Progress.skill(p, skill, Math.min(taken, 20));
        }
    }
    private static boolean wearsArmor(Player p) {
        for (var slot : new EquipmentSlot[]{EquipmentSlot.HEAD, EquipmentSlot.CHEST, EquipmentSlot.LEGS, EquipmentSlot.FEET}) if (!p.getItemBySlot(slot).isEmpty()) return true;
        return false;
    }
    private static Skill weaponSkill(ServerPlayer p, DamageSource source) {
        if (source.is(DamageTypeTags.IS_PROJECTILE)) return Skill.ARCHERY;
        if (!source.is(DamageTypeTags.IS_PLAYER_ATTACK)) return null;
        var held = p.getMainHandItem();
        return held.is(ItemTags.SWORDS) ? Skill.SWORDS : held.is(ItemTags.AXES) ? Skill.AXES : null;
    }

    // -- death -------------------------------------------------------------------------------------
    /** Grave Resolve: once every 20 minutes a killing blow leaves you at 4 health. */
    static boolean allowDeath(LivingEntity entity, DamageSource source, float amount) {
        if (!(entity instanceof ServerPlayer p) || source.is(DamageTypeTags.BYPASSES_INVULNERABILITY)) return true;
        var s = Rpg.sheet(p); long now = p.level().getGameTime();
        if (!s.special("cheat_death") || now - s.mark("cd:cheat_death") < 24000 && s.marks().containsKey("cd:cheat_death")) return true;
        Rpg.set(p, s.mark("cd:cheat_death", now));
        p.setHealth(4);
        p.addEffect(new MobEffectInstance(MobEffects.REGENERATION, 100, 1));
        p.level().playSound(null, p.blockPosition(), SoundEvents.TOTEM_USE, SoundSource.PLAYERS, .8F, 1.2F);
        p.sendSystemMessage(Component.literal("Grave Resolve: you refuse to fall. (Ready again in 20 minutes.)").withStyle(ChatFormatting.DARK_GREEN));
        return false;
    }
    /** A kill: experience, weapon skill, mastery, slay quests and bonus drops. */
    static void died(LivingEntity dead, DamageSource source) {
        // Credit the player who struck it, even if a fall or lava finished it off.
        var credit = source.getEntity() instanceof ServerPlayer sp ? sp : dead.getKillCredit();
        if (!(dead.level() instanceof ServerLevel level) || dead instanceof Player || !(credit instanceof ServerPlayer p)) return;
        var f = family(dead);
        boolean hostile = dead instanceof Enemy, animal = dead instanceof Animal;
        String key = f != null ? f.id() : path(dead);
        int recent = RECENT.computeIfAbsent(p.getUUID(), k -> new HashMap<>()).merge(key, 1, Integer::sum);
        int xp = (int) Math.round(Balance.killXp(dead.getMaxHealth(), hostile, f == null ? null : f.rarity()) * Balance.fatigue(recent - 1));
        if (hostile || animal) Progress.xp(p, Math.max(1, xp), "(" + dead.getName().getString() + ")");
        var weapon = weaponSkill(p, source);
        if (weapon != null && hostile) Progress.skill(p, weapon, xp / 2.0);
        var s = Rpg.sheet(p);
        if (animal) {
            Progress.skill(p, Skill.HUSBANDRY, 2);
            if (p.getRandom().nextDouble() < Balance.HUSBANDRY_EXTRA * s.skill(Skill.HUSBANDRY)) rollLoot(dead, level, source);
        }
        if (hostile && p.getRandom().nextDouble() < Balance.LUCK_LOOT * s.attr(Attr.LUCK)) rollLoot(dead, level, source);
        if (f == null) return;
        int before = s.tier(f);
        var next = s.kill(f.id(), 1);
        Rpg.set(p, next);
        Quests.advance(p, "slay", f.id(), 1);
        if (next.tier(f) > before) Progress.mastery(p, f, next.tier(f));
        for (var perk : f.perks()) {
            if (!perk.kind().equals("drop") || next.tier(f) < perk.tier() || p.getRandom().nextDouble() >= perk.amount()) continue;
            var item = BuiltInRegistries.ITEM.getValue(Identifier.parse(perk.key()));
            if (item != Items.AIR) dead.spawnAtLocation(level, new ItemStack(item, perk.count()));
        }
    }
    /** Rolls the mob's own loot table once more (Luck's bonus loot, Husbandry's extra meat). */
    private static void rollLoot(LivingEntity dead, ServerLevel level, DamageSource source) {
        dead.getLootTable().ifPresent(table -> dead.dropFromLootTable(level, source, true, table));
    }

    // -- blocks ------------------------------------------------------------------------------------
    static void broke(Level world, Player player, BlockPos pos, BlockState state, BlockEntity be) {
        if (!(player instanceof ServerPlayer p) || !(world instanceof ServerLevel level) || p.isCreative() || p.isSpectator()) return;
        var held = p.getMainHandItem(); var s = Rpg.sheet(p);
        boolean silk = EnchantmentHelper.getItemEnchantmentLevel(level.registryAccess().lookupOrThrow(Registries.ENCHANTMENT).getOrThrow(Enchantments.SILK_TOUCH), held) > 0;
        String block = BuiltInRegistries.BLOCK.getKey(state.getBlock()).getPath();
        boolean ore = state.is(ConventionalBlockTags.ORES) || block.equals("ancient_debris");
        if (held.is(ItemTags.PICKAXES) && state.is(BlockTags.MINEABLE_WITH_PICKAXE)) {
            int oreXp = ore && !silk ? Balance.oreXp(block) : 0;
            Progress.skill(p, Skill.MINING, 1 + oreXp * 2);
            if (oreXp > 0) {
                Progress.xp(p, oreXp, null);
                if (p.getRandom().nextDouble() < Balance.MINING_DOUBLE * s.skill(Skill.MINING)) Block.dropResources(state, level, pos, be, p, held);
            }
            if (ore) Quests.advance(p, "mine", "ores", 1);
            else if (state.is(BlockTags.BASE_STONE_OVERWORLD) || state.is(BlockTags.BASE_STONE_NETHER) || block.contains("stone")) Quests.advance(p, "mine", "stone", 1);
        } else if (held.is(ItemTags.AXES) && state.is(BlockTags.LOGS)) {
            Progress.skill(p, Skill.WOODCUTTING, 2);
            if (p.getRandom().nextDouble() < Balance.WOOD_DOUBLE * s.skill(Skill.WOODCUTTING)) Block.dropResources(state, level, pos, be, p, held);
            Quests.advance(p, "mine", "logs", 1);
        } else if (held.is(ItemTags.AXES) && state.is(BlockTags.MINEABLE_WITH_AXE)) {
            Progress.skill(p, Skill.WOODCUTTING, 1);
        } else if (held.is(ItemTags.SHOVELS) && state.is(BlockTags.MINEABLE_WITH_SHOVEL)) {
            Progress.skill(p, Skill.EXCAVATION, 1);
            Quests.advance(p, "mine", "dirt", 1);
            if (p.getRandom().nextDouble() < Balance.DIG_FIND * s.skill(Skill.EXCAVATION)) {
                double r = p.getRandom().nextDouble();
                var find = r < .4 ? Items.FLINT : r < .65 ? Items.CLAY_BALL : r < .8 ? Items.BONE : r < .92 ? Items.GOLD_NUGGET : r < .97 ? Items.STRING : Items.EMERALD;
                Block.popResource(level, pos, new ItemStack(find));
            }
        }
        if (ripe(state)) {
            Progress.skill(p, Skill.FARMING, 3);
            Progress.xp(p, 1, null);
            Quests.advance(p, "harvest", "crops", 1);
            if (p.getRandom().nextDouble() < Balance.FARM_EXTRA * s.skill(Skill.FARMING)) Block.dropResources(state, level, pos, be, p, held);
        }
    }
    private static boolean ripe(BlockState state) {
        if (state.getBlock() instanceof CropBlock crop) return crop.isMaxAge(state);
        if (state.is(Blocks.NETHER_WART)) return state.getValue(NetherWartBlock.AGE) >= 3;
        return state.is(Blocks.MELON) || state.is(Blocks.PUMPKIN);
    }
}
