package dev.villagefriends.rpg;

import net.minecraft.ChatFormatting;
import net.minecraft.core.Holder;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.stats.Stats;
import net.minecraft.tags.BlockTags;
import net.minecraft.tags.ItemTags;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.ai.attributes.Attribute;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.block.state.BlockState;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

/**
 * The character's body: attribute modifiers, hunger and tool speed, the once-a-second pulse
 * (immunities, passive abilities, Recovery healing, stat-based skills, quest tracking), joining,
 * respawning and the character sheet's buttons.
 */
public final class Life {
    private Life() {}
    private static final Map<UUID, Integer> RECOVERY = new HashMap<>();
    static void clear() { RECOVERY.clear(); }

    // -- attributes --------------------------------------------------------------------------------
    /** Puts the sheet's numbers on the player's attributes; cheap when nothing changed. */
    public static void apply(ServerPlayer p) {
        var s = Rpg.sheet(p);
        int vit = s.attr(Attr.VITALITY), dex = s.attr(Attr.DEXTERITY), agi = s.attr(Attr.AGILITY), end = s.attr(Attr.ENDURANCE),
                tou = s.attr(Attr.TOUGHNESS), luck = s.attr(Attr.LUCK);
        int ath = s.skill(Skill.ATHLETICS), acro = s.skill(Skill.ACROBATICS), swim = s.skill(Skill.SWIMMING), def = s.skill(Skill.DEFENSE),
                fish = s.skill(Skill.FISHING), swords = s.skill(Skill.SWORDS);
        var add = AttributeModifier.Operation.ADD_VALUE; var base = AttributeModifier.Operation.ADD_MULTIPLIED_BASE; var total = AttributeModifier.Operation.ADD_MULTIPLIED_TOTAL;
        set(p, Attributes.MAX_HEALTH, "health", add, Balance.baseHealth(s.level()) - 20 + Balance.VIT_HEALTH * vit + s.perk("attr", "max_health"));
        set(p, Attributes.ATTACK_SPEED, "attack_speed", total, Balance.DEX_SPEED * dex);
        set(p, Attributes.MOVEMENT_SPEED, "speed", total, Balance.AGI_SPEED * agi + Balance.ATHLETICS_SPEED * ath);
        set(p, Attributes.JUMP_STRENGTH, "jump", base, Balance.AGI_JUMP * agi);
        set(p, Attributes.SAFE_FALL_DISTANCE, "safe_fall", add, Balance.AGI_SAFE_FALL * agi + Balance.ACRO_SAFE_FALL * acro + s.perk("attr", "safe_fall_distance"));
        set(p, Attributes.FALL_DAMAGE_MULTIPLIER, "fall_damage", base, -Balance.ACRO_FALL_DAMAGE * acro);
        set(p, Attributes.OXYGEN_BONUS, "breath", add, Balance.END_BREATH * end + Balance.SWIM_BREATH * swim + s.perk("attr", "oxygen_bonus"));
        set(p, Attributes.WATER_MOVEMENT_EFFICIENCY, "water", add, Balance.SWIM_EFFICIENCY * swim + s.perk("attr", "water_movement_efficiency"));
        set(p, Attributes.ARMOR, "armor", add, Balance.TOU_ARMOR * tou);
        set(p, Attributes.ARMOR_TOUGHNESS, "toughness", add, Balance.TOU_TOUGHNESS * tou + Balance.DEFENSE_TOUGHNESS * def);
        set(p, Attributes.KNOCKBACK_RESISTANCE, "knockback", add, Balance.DEFENSE_KNOCKBACK * def + s.perk("attr", "knockback_resistance"));
        set(p, Attributes.LUCK, "luck", add, Balance.LUCK_LUCK * luck + Balance.FISH_LUCK * fish);
        set(p, Attributes.SWEEPING_DAMAGE_RATIO, "sweep", add, Balance.SWORD_SWEEP * swords);
        set(p, Attributes.BLOCK_BREAK_SPEED, "mining", base, Balance.mineBase(s.level()) - 1 + s.perk("mine", ""));
        if (p.getHealth() > p.getMaxHealth()) p.setHealth(p.getMaxHealth());
    }
    private static void set(ServerPlayer p, Holder<Attribute> attribute, String name, AttributeModifier.Operation op, double amount) {
        var inst = p.getAttribute(attribute);
        if (inst == null) return;
        Identifier id = Rpg.id(name); var old = inst.getModifier(id);
        if (Math.abs(amount) < 1e-6) { if (old != null) inst.removeModifier(id); return; }
        if (old != null && old.operation() == op && Math.abs(old.amount() - amount) < 1e-6) return;
        inst.addOrUpdateTransientModifier(new AttributeModifier(id, amount, op));
    }

    // -- hooks shared by client and server (the sheet is synced to its owner) ---------------------------
    /** Hunger drain: the level curve, Endurance, and Athletics while sprinting. */
    public static float hunger(Player p, float amount) {
        if (amount <= 0) return amount;
        var s = Rpg.sheet(p);
        double m = Balance.hungerRate(s.level()) * (1 - Balance.END_HUNGER * s.attr(Attr.ENDURANCE));
        if (p.isSprinting()) m *= 1 - Balance.ATHLETICS_HUNGER * s.skill(Skill.ATHLETICS);
        return (float) (amount * Math.max(Balance.MIN_HUNGER, m));
    }
    /** Tool skills: pickaxe on stone, axe on wood, shovel on earth. */
    public static float toolSpeed(Player p, BlockState state) {
        var held = p.getMainHandItem(); var s = Rpg.sheet(p);
        Skill skill = held.is(ItemTags.PICKAXES) && state.is(BlockTags.MINEABLE_WITH_PICKAXE) ? Skill.MINING
                : held.is(ItemTags.AXES) && state.is(BlockTags.MINEABLE_WITH_AXE) ? Skill.WOODCUTTING
                : held.is(ItemTags.SHOVELS) && state.is(BlockTags.MINEABLE_WITH_SHOVEL) ? Skill.EXCAVATION : null;
        return skill == null ? 1 : (float) (1 + Balance.TOOL_SPEED * s.skill(skill));
    }
    /** Arcana: more vanilla experience, and gathering experience trains Arcana. */
    public static int vanillaXp(Player player, int amount) {
        if (amount <= 0 || !(player instanceof ServerPlayer p)) return amount;
        Progress.skill(p, Skill.ARCANA, amount / 2.0);
        return (int) Progress.roll(p, amount * (1 + Balance.ARCANA_XP * Rpg.sheet(p).skill(Skill.ARCANA)));
    }

    // -- the pulse ---------------------------------------------------------------------------------
    static void tick(MinecraftServer server) {
        for (var p : server.getPlayerList().getPlayers()) if ((p.tickCount + p.getId()) % 20 == 0 && p.isAlive()) pulse(p);
    }
    private static final List<String> IMMUNITIES = List.of("hunger", "poison", "weakness", "slowness", "levitation", "mining_fatigue", "wither", "darkness");
    /** Stats turned into skill experience: key, stat, skill, skill xp per unit, character xp per unit, divisor, quest kind. */
    private record Tracked(String key, Identifier stat, Skill skill, double skillXp, double xp, int per, String quest) {}
    private static final List<Tracked> TRACKED = List.of(
            new Tracked("fish", Stats.FISH_CAUGHT, Skill.FISHING, 15, 4, 1, "fish"),
            new Tracked("bred", Stats.ANIMALS_BRED, Skill.HUSBANDRY, 10, 3, 1, "breed"),
            new Tracked("enchant", Stats.ENCHANT_ITEM, Skill.ARCANA, 40, 10, 1, "enchant"),
            new Tracked("trade", Stats.TRADED_WITH_VILLAGER, Skill.BARTERING, 12, 2, 1, "trade"),
            new Tracked("anvil", Stats.INTERACT_WITH_ANVIL, Skill.ARCANA, 5, 0, 1, ""),
            new Tracked("brew", Stats.INTERACT_WITH_BREWINGSTAND, Skill.ARCANA, 3, 0, 1, ""),
            new Tracked("sprint", Stats.SPRINT_ONE_CM, Skill.ATHLETICS, 1, 0, 400, ""),
            new Tracked("swim", Stats.SWIM_ONE_CM, Skill.SWIMMING, 1, 0, 300, ""),
            new Tracked("ride", Stats.HORSE_ONE_CM, Skill.RIDING, 1, 0, 500, ""));

    private static void pulse(ServerPlayer p) {
        apply(p);
        var s = Rpg.sheet(p);
        for (var id : IMMUNITIES) if (s.immune(id)) { var e = effect(id); if (e != null && p.hasEffect(e)) p.removeEffect(e); }
        if (s.special("night_eyes") && p.getY() < 63 && !p.level().canSeeSky(p.blockPosition())) keep(p, MobEffects.NIGHT_VISION);
        if (s.special("village_hero")) keep(p, MobEffects.HERO_OF_THE_VILLAGE);
        if (s.special("no_phantoms")) p.resetStat(Stats.CUSTOM.get(Stats.TIME_SINCE_REST));
        int interval = Balance.recoveryInterval(s.attr(Attr.RECOVERY));
        if (interval > 0 && p.getHealth() < p.getMaxHealth() && p.getFoodData().getFoodLevel() >= 10) {
            int acc = RECOVERY.merge(p.getUUID(), 20, Integer::sum);
            if (acc >= interval) { RECOVERY.put(p.getUUID(), 0); p.heal(.5F); p.causeFoodExhaustion(1.5F); }
        }
        // Stats: remember the last value, award the difference.
        var stats = p.getStats(); var seen = s; var gains = new long[TRACKED.size()];
        for (int i = 0; i < TRACKED.size(); i++) {
            var t = TRACKED.get(i); String key = "seen:" + t.key();
            long now = stats.getValue(Stats.CUSTOM.get(t.stat())) / t.per();
            if (!s.marks().containsKey(key)) { seen = seen.mark(key, now); continue; }
            long before = s.mark(key);
            if (now != before) { seen = seen.mark(key, now); gains[i] = Math.max(0, now - before); }
        }
        if (seen != s) Rpg.set(p, seen);
        for (int i = 0; i < TRACKED.size(); i++) {
            if (gains[i] <= 0) continue;
            var t = TRACKED.get(i);
            Progress.skill(p, t.skill(), gains[i] * t.skillXp());
            if (t.xp() > 0) Progress.xp(p, gains[i] * t.xp(), null);
            if (!t.quest().isEmpty()) Quests.advance(p, t.quest(), "", (int) gains[i]);
        }
        Quests.track(p);
    }
    private static Holder<MobEffect> effect(String id) {
        return switch (id) {
            case "hunger" -> MobEffects.HUNGER; case "poison" -> MobEffects.POISON; case "weakness" -> MobEffects.WEAKNESS;
            case "slowness" -> MobEffects.SLOWNESS; case "levitation" -> MobEffects.LEVITATION; case "mining_fatigue" -> MobEffects.MINING_FATIGUE;
            case "wither" -> MobEffects.WITHER; case "darkness" -> MobEffects.DARKNESS; default -> null;
        };
    }
    /** Keeps a quiet effect topped up so it never blinks out. */
    private static void keep(ServerPlayer p, Holder<MobEffect> effect) {
        var now = p.getEffect(effect);
        if (now == null || now.getDuration() < 240) p.addEffect(new MobEffectInstance(effect, 320, 0, true, false, true));
    }

    // -- joining, respawning, buttons ------------------------------------------------------------------
    static void joined(ServerPlayer p) {
        if (!((net.fabricmc.fabric.api.attachment.v1.AttachmentTarget) p).hasAttached(Rpg.SHEET)) {
            Rpg.set(p, Sheet.NEW);
            p.sendSystemMessage(Component.literal("Village Friends RPG: you start out weak. Level up by fighting, gathering and taking jobs from villagers. Press K for your character sheet.").withStyle(ChatFormatting.GOLD));
        }
        apply(p);
    }
    static void respawned(ServerPlayer old, ServerPlayer p, boolean alive) {
        if (!alive && Balance.deathPenalty > 0) {
            var s = Rpg.sheet(p); var next = s.penalized(Balance.deathPenalty);
            if (next.xp() < s.xp()) {
                Rpg.set(p, next);
                p.sendSystemMessage(Component.literal("You lost " + (s.xp() - next.xp()) + " experience toward level " + (s.level() + 1) + ".").withStyle(ChatFormatting.RED));
            }
        }
        apply(p);
        p.setHealth(p.getMaxHealth());
    }
    static void action(ServerPlayer p, RpgActionPayload a) {
        var s = Rpg.sheet(p);
        switch (a.action()) {
            case "spend" -> { var attr = Attr.byId(a.arg()); if (attr != null) { Rpg.set(p, s.spend(attr, 1)); apply(p); } }
            case "respec" -> {
                int cost = respecCost(s.level());
                if (s.spentPoints() == 0) return;
                if (count(p, Items.EMERALD) < cost) { p.sendSystemMessage(Component.literal("Unlearning your training costs " + cost + " emeralds.").withStyle(ChatFormatting.RED), true); return; }
                take(p, Items.EMERALD, cost); Rpg.set(p, s.respec()); apply(p);
                p.sendSystemMessage(Component.literal("Your attribute points are free to spend again.").withStyle(ChatFormatting.GOLD), true);
            }
            case "abandon" -> Quests.abandon(p, a.arg());
            case "ability" -> Abilities.use(p, a.arg());
            default -> {}
        }
    }
    public static int respecCost(int level) { return 5 + level / 2; }

    public static int count(ServerPlayer p, Item item) {
        int n = 0; var inv = p.getInventory();
        for (int i = 0; i < inv.getContainerSize(); i++) if (inv.getItem(i).is(item)) n += inv.getItem(i).getCount();
        return n;
    }
    public static void take(ServerPlayer p, Item item, int n) {
        var inv = p.getInventory();
        for (int i = 0; i < inv.getContainerSize() && n > 0; i++) {
            var stack = inv.getItem(i);
            if (!stack.is(item)) continue;
            int t = Math.min(n, stack.getCount()); stack.shrink(t); n -= t;
        }
        inv.setChanged();
    }
    public static Item item(String id) { return BuiltInRegistries.ITEM.getValue(Identifier.parse(id)); }
}
