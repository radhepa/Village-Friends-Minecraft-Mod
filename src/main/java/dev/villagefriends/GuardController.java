package dev.villagefriends;

import static dev.villagefriends.VillageFriends.*;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.Registries;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.Identifier;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.tags.ItemTags;
import net.minecraft.tags.TagKey;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.animal.golem.IronGolem;
import net.minecraft.world.entity.monster.Creeper;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.projectile.Projectile;
import net.minecraft.world.entity.projectile.arrow.AbstractArrow;
import net.minecraft.world.entity.projectile.arrow.Arrow;
import net.minecraft.world.item.BowItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;

/** Loaded guards only: native navigation, equipment and damage; no terrain edits or chunk loads. */
public final class GuardController {
    public static final TagKey<EntityType<?>> PREDATORS = TagKey.create(Registries.ENTITY_TYPE,
            Identifier.fromNamespaceAndPath("villagefriends", "villager_predators"));
    private static final EquipmentSlot[] ARMOR = {EquipmentSlot.HEAD, EquipmentSlot.CHEST, EquipmentSlot.LEGS, EquipmentSlot.FEET};
    private static final Item[] IRON = {Items.IRON_HELMET, Items.IRON_CHESTPLATE, Items.IRON_LEGGINGS, Items.IRON_BOOTS};
    private static final Item[] CHAIN = {Items.CHAINMAIL_HELMET, Items.CHAINMAIL_CHESTPLATE, Items.CHAINMAIL_LEGGINGS, Items.CHAINMAIL_BOOTS};
    private static final Map<UUID, Combat> fights = new HashMap<>();
    private static final Map<UUID, RecentAttack> recent = new HashMap<>();
    private static final Map<UUID, Incident> pending = new HashMap<>();
    private record RecentAttack(ServerLevel level, long until) {}
    private record Incident(DamageSource source, boolean forgiven) {}
    private static final class Combat {
        final Map<UUID, Long> anger = new HashMap<>();
        Vec3 origin, lastPosition;
        LivingEntity foe;
        long nextAttack, returnUntil, lastProgress, retryAfter;
        boolean returning, engaged;
        Combat(Villager v, long now) { origin = lastPosition = v.position(); lastProgress = now; }
    }

    public static boolean isGuard(Villager v) {
        return !v.isBaby() && v.getVillagerData().profession().unwrapKey()
                .map(k -> k.equals(VillageProfessions.key("knight")) || k.equals(VillageProfessions.key("archer"))).orElse(false);
    }
    private static boolean archer(Villager v) {
        return v.getVillagerData().profession().unwrapKey().map(k -> k.equals(VillageProfessions.key("archer"))).orElse(false);
    }
    private static boolean eligible(Villager v) {
        return isGuard(v) && v.isAlive() && !v.isNoAi() && !CompanionController.state(v).downed()
                && !CompanionController.hasActivity(v);
    }
    public static void initializeEquipment(Villager v) {
        if (!isGuard(v) || target(v).getAttachedOrElse(GUARD_EQUIPPED, false)) return;
        var iron = GuardPolicy.ironSlots(v.getUUID());
        for (int i = 0; i < ARMOR.length; i++) fill(v, ARMOR[i], iron.contains(i) ? IRON[i] : CHAIN[i]);
        fill(v, EquipmentSlot.MAINHAND, archer(v) ? Items.BOW : Items.IRON_SWORD);
        target(v).setAttached(GUARD_EQUIPPED, true);
    }
    private static void fill(Villager v, EquipmentSlot slot, Item item) {
        if (v.getItemBySlot(slot).isEmpty()) { v.setItemSlot(slot, new ItemStack(item)); v.setDropChance(slot, 1); }
    }
    public static void unload(Villager v) { fights.remove(v.getUUID()); recent.remove(v.getUUID()); pending.remove(v.getUUID()); }
    public static void clear() { fights.clear(); recent.clear(); pending.clear(); }
    public static void tick(MinecraftServer server) {
        pending.clear();
        if (server.getTickCount() % 20 == 0) {
            recent.entrySet().removeIf(e -> e.getValue().level().getGameTime() >= e.getValue().until()
                    || e.getValue().level().getEntity(e.getKey()) == null);
        }
    }
    public static boolean fighting(Villager v) {
        var c = fights.get(v.getUUID()); return c != null && (c.foe != null || c.returning);
    }
    public static LivingEntity combatTarget(Villager v) { var c = fights.get(v.getUUID()); return c == null ? null : c.foe; }
    public static boolean angryAt(Villager v, ServerPlayer p) {
        var c = fights.get(v.getUUID());
        return c != null && GuardPolicy.angerActive(v.level().getGameTime(), c.anger.getOrDefault(p.getUUID(), 0L));
    }

    /** Capture forgiveness before the existing relationship damage callback changes trust. */
    public static boolean allowDamage(LivingEntity entity, DamageSource source, float amount) {
        if (source.getDirectEntity() instanceof AbstractArrow arrow && protectedFromArrow(arrow, entity)) return false;
        if (entity instanceof Villager v && !CompanionController.state(v).downed()) {
            Entity attacker = attacker(source);
            boolean forgiven = attacker instanceof ServerPlayer p && GuardPolicy.forgives(bond(v, p), state(v, p));
            pending.put(v.getUUID(), new Incident(source, forgiven));
        }
        return CompanionController.allowDamage(entity, source, amount);
    }
    public static void afterDamage(LivingEntity entity, DamageSource source, float original, float taken, boolean blocked) {
        if (taken > 0 && !blocked) observeDamage(entity, source);
        else if (entity instanceof Villager v) pending.remove(v.getUUID());
    }
    public static boolean allowDeath(LivingEntity entity, DamageSource source, float amount) {
        observeDamage(entity, source);
        return CompanionController.allowDeath(entity, source, amount);
    }
    private static Entity attacker(DamageSource source) {
        if (source.getEntity() != null) return source.getEntity();
        return source.getDirectEntity() instanceof Projectile p ? p.getOwner() : source.getDirectEntity();
    }
    private static void observeDamage(LivingEntity entity, DamageSource source) {
        if (!(entity instanceof Villager victim) || !(victim.level() instanceof ServerLevel level)) return;
        Incident incident = pending.remove(victim.getUUID());
        if (incident == null || incident.source() != source) return;
        Entity attacker = attacker(source);
        long now = level.getGameTime();
        if (attacker instanceof ServerPlayer p) {
            if (incident.forgiven() || p.isCreative() || p.isSpectator()) return;
            for (Villager guard : level.getEntitiesOfClass(Villager.class, victim.getBoundingBox().inflate(16),
                    v -> eligible(v) && v.distanceToSqr(victim) <= 256)) {
                initializeEquipment(guard);
                var c = fights.computeIfAbsent(guard.getUUID(), id -> new Combat(guard, now));
                if (c.foe == null && !c.returning) c.origin = guard.position();
                c.anger.put(p.getUUID(), now + GuardPolicy.ANGER_TICKS);
                c.retryAfter = 0;
            }
        } else if (attacker instanceof Mob m && !(m instanceof Villager) && !(m instanceof IronGolem)) {
            recent.put(m.getUUID(), new RecentAttack(level, now + GuardPolicy.RECENT_ATTACK_TICKS));
        }
    }
    private static boolean threat(Mob m, ServerLevel level) {
        var attack = recent.get(m.getUUID());
        return m.isAlive() && !(m instanceof Villager) && !(m instanceof IronGolem) && GuardPolicy.threat(
                m instanceof Creeper, BuiltInRegistries.ENTITY_TYPE.wrapAsHolder(m.getType()).is(PREDATORS), m.getTarget() instanceof Villager,
                attack != null && attack.level() == level && level.getGameTime() < attack.until());
    }
    private static boolean playerValid(ServerPlayer p, Villager v) {
        return p.isAlive() && !p.isRemoved() && !p.isCreative() && !p.isSpectator() && p.level() == v.level()
                && ((ServerLevel)v.level()).getServer().getPlayerList().getPlayer(p.getUUID()) == p;
    }
    private static boolean valid(Villager v, Combat c, LivingEntity foe, ServerLevel level) {
        if (!foe.isAlive() || foe.isRemoved() || foe.level() != level || foe.position().distanceToSqr(c.origin) > 1024) return false;
        if (foe instanceof ServerPlayer p) return playerValid(p, v) && angryAt(v, p);
        return foe instanceof Mob m && threat(m, level);
    }
    private static int priority(LivingEntity foe) {
        if (foe instanceof ServerPlayer) return 0;
        var attack = recent.get(foe.getUUID());
        return foe instanceof Mob m && (m.getTarget() instanceof Villager
                || attack != null && attack.level() == foe.level() && foe.level().getGameTime() < attack.until()) ? 1 : 2;
    }
    private static LivingEntity select(Villager v, Combat c, ServerLevel level) {
        LivingEntity best = c.foe != null && valid(v, c, c.foe, level) ? c.foe : null;
        for (UUID id : c.anger.keySet()) {
            var p = level.getServer().getPlayerList().getPlayer(id);
            if (p != null && v.distanceToSqr(p) <= 256 && valid(v, c, p, level)
                    && (best == null || priority(best) > 0 || v.distanceToSqr(p) < v.distanceToSqr(best))) best = p;
        }
        if (best != null && priority(best) == 0) return best;
        for (Mob m : level.getEntitiesOfClass(Mob.class, v.getBoundingBox().inflate(16),
                m -> v.distanceToSqr(m) <= 256 && threat(m, level) && v.hasLineOfSight(m))) {
            if (valid(v, c, m, level) && (best == null || priority(m) < priority(best)
                    || priority(m) == priority(best) && best != c.foe && v.distanceToSqr(m) < v.distanceToSqr(best))) best = m;
        }
        return best;
    }

    /** Returns true only while combat/return movement owns the villager's brain. */
    public static boolean drive(Villager v, ServerLevel level, boolean stationary) {
        initializeEquipment(v);
        if (!eligible(v)) { unload(v); return false; }
        long now = level.getGameTime();
        var c = fights.get(v.getUUID());
        if (c == null) {
            if (v.tickCount % GuardPolicy.SCAN_INTERVAL != 0) return false;
            c = new Combat(v, now);
            var selected = select(v, c, level);
            if (selected == null) return false;
            c.foe = selected; fights.put(v.getUUID(), c);
        }
        c.anger.entrySet().removeIf(e -> {
            var p = level.getServer().getPlayerList().getPlayer(e.getKey());
            return !GuardPolicy.angerActive(now, e.getValue()) || p == null || !playerValid(p, v);
        });
        if (c.engaged && v.position().distanceToSqr(c.origin) > 1024) beginReturn(v, c, now);
        if (c.returning) {
            if (stationary || v.position().distanceToSqr(c.origin) <= 4 || now >= c.returnUntil) {
                c.returning = false; c.engaged = false; v.getNavigation().stop();
                if (c.anger.isEmpty() && now >= c.retryAfter) fights.remove(v.getUUID());
                return false;
            }
            if (now % 10 == 0 && level.hasChunkAt(net.minecraft.core.BlockPos.containing(c.origin)))
                v.getNavigation().moveTo(c.origin.x, c.origin.y, c.origin.z, .8);
            return true;
        }
        if (now < c.retryAfter) return false;
        if (v.tickCount % 10 == 0 || c.foe == null || !valid(v, c, c.foe, level)) {
            var previous = c.foe;
            c.foe = select(v, c, level);
            if (previous != c.foe) { v.stopUsingItem(); c.lastProgress = now; c.lastPosition = v.position(); }
        }
        if (c.foe == null) {
            if (c.engaged && v.position().distanceToSqr(c.origin) > 4 && !stationary) { beginReturn(v, c, now); return true; }
            if (c.engaged) { v.stopUsingItem(); v.getNavigation().stop(); }
            c.engaged = false;
            if (c.anger.isEmpty()) fights.remove(v.getUUID());
            return false;
        }
        if (!c.engaged) { c.origin = c.lastPosition = v.position(); c.lastProgress = now; c.engaged = true; }
        v.stopSleeping(); v.setTradingPlayer(null); v.getLookControl().setLookAt(c.foe, 30, 30);
        if (v.position().distanceToSqr(c.lastPosition) > 1) { c.lastPosition = v.position(); c.lastProgress = now; }
        if (now - c.lastProgress > 200 && (!v.hasLineOfSight(c.foe) || !archer(v) && !v.isWithinMeleeAttackRange(c.foe))) {
            c.retryAfter = now + 200; beginReturn(v, c, now); return true;
        }
        if (archer(v)) ranged(v, c, level, stationary);
        else {
            if (stationary) v.getNavigation().stop();
            else if (now % 10 == 0) v.getNavigation().moveTo(c.foe, .8);
            if (now >= c.nextAttack && v.hasLineOfSight(c.foe) && v.isWithinMeleeAttackRange(c.foe)) {
                v.swingForAttack(InteractionHand.MAIN_HAND); c.nextAttack = now + 20;
                if (v.doHurtTarget(level, c.foe)) {
                    v.getMainHandItem().postHurtEnemy(c.foe, v);
                    c.lastProgress = now; rememberDefense(v, c.foe);
                }
            }
        }
        return true;
    }
    private static void beginReturn(Villager v, Combat c, long now) {
        if (c.returning) return;
        c.foe = null; c.returning = true; c.returnUntil = now + 200;
        v.stopUsingItem(); v.getNavigation().stop();
    }
    private static void ranged(Villager v, Combat c, ServerLevel level, boolean stationary) {
        var bow = v.getMainHandItem();
        if (!(bow.getItem() instanceof BowItem)) { v.stopUsingItem(); v.getNavigation().stop(); return; }
        double distance = v.distanceToSqr(c.foe);
        if (stationary) v.getNavigation().stop();
        else if (distance < 16) {
            if (level.getGameTime() % 10 == 0) {
                var away = v.position().subtract(c.foe.position()).multiply(1, 0, 1).normalize().scale(4).add(v.position());
                if (level.hasChunkAt(net.minecraft.core.BlockPos.containing(away))) v.getNavigation().moveTo(away.x, away.y, away.z, .8);
            }
        } else if (distance > 144 || !v.hasLineOfSight(c.foe)) {
            if (level.getGameTime() % 10 == 0) v.getNavigation().moveTo(c.foe, .8);
        } else v.getNavigation().stop();
        if (distance > 256 || !v.hasLineOfSight(c.foe) || !safeShot(v, c.foe, level)) { v.stopUsingItem(); return; }
        if (level.getGameTime() < c.nextAttack) return;
        if (!v.isUsingItem()) { v.startUsingItem(InteractionHand.MAIN_HAND); return; }
        if (v.getTicksUsingItem() < 20) return;
        var arrow = new Arrow(level, v, new ItemStack(Items.ARROW), bow.copy());
        arrow.pickup = AbstractArrow.Pickup.DISALLOWED;
        target(arrow).setAttached(GUARD_ARROW_TARGET, c.foe.getUUID().toString());
        var aim = c.foe.getBoundingBox().getCenter().subtract(arrow.position());
        double horizontal = Math.sqrt(aim.x * aim.x + aim.z * aim.z);
        Projectile.spawnProjectileUsingShoot(arrow, level, bow, aim.x, aim.y + horizontal * .2, aim.z, 1.6F, 1F);
        bow.hurtAndBreak(1, v, EquipmentSlot.MAINHAND);
        v.playSound(net.minecraft.sounds.SoundEvents.SKELETON_SHOOT, 1F, 1F);
        v.stopUsingItem(); c.nextAttack = level.getGameTime() + 20; c.lastProgress = level.getGameTime();
    }
    public static boolean protectedFromArrow(AbstractArrow arrow, Entity hit) {
        String intended = target(arrow).getAttached(GUARD_ARROW_TARGET);
        return intended != null && (hit instanceof Villager || hit instanceof IronGolem || hit instanceof Creeper
                || hit instanceof net.minecraft.world.entity.player.Player && !hit.getUUID().toString().equals(intended));
    }
    private static boolean safeShot(Villager v, LivingEntity foe, ServerLevel level) {
        Vec3 start = v.getEyePosition(), end = foe.getBoundingBox().getCenter();
        if (level.clip(new ClipContext(start, end, ClipContext.Block.COLLIDER, ClipContext.Fluid.NONE, v)).getType() != HitResult.Type.MISS) return false;
        for (LivingEntity e : level.getEntitiesOfClass(LivingEntity.class, new AABB(start, end).inflate(1),
                e -> e != v && e != foe && (e instanceof Villager || e instanceof IronGolem || e instanceof net.minecraft.world.entity.player.Player))) {
            if (e.getBoundingBox().inflate(.4).clip(start, end).isPresent()) return false;
        }
        return true;
    }
    public static void rememberDefense(Villager v, Entity foe) {
        var s = CompanionController.state(v);
        if (!s.active()) return;
        var p = ((ServerLevel)v.level()).getServer().getPlayerList().getPlayer(UUID.fromString(s.owner()));
        if (p != null && !bond(v, p).has("outing:defense"))
            saveBond(v, p, bond(v, p).flag("outing:defense").flag("adventure_defense")
                    .remember(day(v.level()), "We defended each other against a " + foe.getName().getString().toLowerCase() + "."));
    }

    public static boolean canExchange(Villager v, ServerPlayer p) {
        var s = CompanionController.state(v);
        return isGuard(v) && validTarget(p, v) && !s.downed() && !fighting(v) && !angryAt(v, p)
                && !CompanionController.hasActivity(v) && (!s.active() || s.owner().equals(p.getUUID().toString()));
    }
    public static boolean exchange(ServerPlayer p, Villager v) {
        if (!canExchange(v, p)) return false;
        initializeEquipment(v);
        var held = p.getMainHandItem();
        EquipmentSlot slot = null;
        var equippable = held.get(DataComponents.EQUIPPABLE);
        if (equippable != null && held.is(ItemTags.ARMOR_ENCHANTABLE))
            for (var armor : ARMOR) if (equippable.slot() == armor) slot = armor;
        if (!held.isEmpty() && (archer(v) ? held.getItem() instanceof BowItem : held.is(ItemTags.SWORDS))) slot = EquipmentSlot.MAINHAND;
        if (slot == null) {
            show(p, v, "companion", archer(v) ? "Hold a bow or armor piece to exchange." : "Hold a sword or armor piece to exchange.", "Your item was kept.", false);
            return true;
        }
        var previous = v.getItemBySlot(slot).copy();
        var replacement = held.copyWithCount(1); held.shrink(1);
        v.setItemSlot(slot, replacement); v.setDropChance(slot, 1);
        if (!previous.isEmpty()) {
            // Native Inventory.add discards overflow in Creative. Physical exchanges must return it instead.
            boolean room = p.getInventory().getFreeSlot() >= 0 || p.getInventory().getSlotWithRemainingSpace(previous) >= 0;
            if (!room || !p.getInventory().add(previous)) drop(p, previous);
        }
        show(p, v, "companion", "Thank you. I've returned my previous equipment.", "Equipped " + replacement.getHoverName().getString() + ".", false);
        return true;
    }
    private GuardController() {}
}
