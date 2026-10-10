package dev.villagefriends.stable.ride;

import static dev.villagefriends.VillageFriends.profession;
import static dev.villagefriends.VillageFriends.target;

import dev.villagefriends.GuardPatrols;
import dev.villagefriends.ResidentRoutines;
import dev.villagefriends.VillageBlocks;
import dev.villagefriends.VillageRecord;
import dev.villagefriends.VillageSettlements;
import dev.villagefriends.routine.Routine;
import dev.villagefriends.stable.api.Stables;
import dev.villagefriends.stable.data.StableData;
import dev.villagefriends.stable.data.StallHome;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import net.minecraft.core.BlockPos;
import net.minecraft.core.GlobalPos;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.memory.MemoryModuleType;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.entity.animal.equine.Donkey;
import net.minecraft.world.entity.animal.equine.Horse;
import net.minecraft.world.entity.animal.equine.Mule;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;
import org.jspecify.annotations.Nullable;

/**
 * Residents on horseback, called from Village Friends' core (routines, patrols, guards and companions). A
 * villager riding a tame horse steers it: its navigation is the horse's, so a walk target or a
 * {@code getNavigation().moveTo(...)} moves the horse at the horse's own speed times the modifier, and vanilla
 * switches the horse's own move, jump and look goals off while a mob rides it (it won't panic, wander or buck).
 *
 * <ul>
 * <li><b>Night watch.</b> A knight on the night watch whose village has a stable anywhere in it (village stables
 * stand on the outer streets, often 80 blocks or more from the bell) walks to a free stable horse, mounts it
 * ("patrol") and rides the patrol. When the watch ends they ride back to its stall and get off, or get off where
 * they are once the ride has taken too long (the horse then drifts home by {@link HorseDeeds}, from any distance,
 * since no player took it). Never for a raid: that is no moment to walk to the stable.</li>
 * <li><b>Companions.</b> When the player they follow gets on a horse, a companion looks once for a spare horse the
 * player owns within 8 blocks and mounts it at once ("companion"); they get off when the player does.</li>
 * <li><b>Caravans.</b> Another mod seats a guard with {@code PackAnimals.mountGuard} ("caravan"): their routine and
 * villager brain stay off ({@link #caravan}) and only the caller steers them.</li>
 * </ul>
 * Owned by the riders package; the foundation's signatures are frozen.
 */
public final class Mounts {
    public static final String PATROL = "patrol", COMPANION = "companion", CARAVAN = "caravan";
    /**
     * A knight looks for horses stalled in their village: the village record around the bell (as far out as its outer
     * lots), at most this far from its centre. With no record there, horses stalled this far from the bell.
     */
    static final int VILLAGE_REACH = 192, STABLE_REACH = 64;
    /** Close enough to swing up into the saddle. */
    static final double MOUNT_REACH = 2.5;
    /** Close enough to the stall to get off after the watch. */
    static final double HOME_REACH = 3;
    /** A companion only takes a spare horse this close (no walking off to fetch one). */
    static final double SPARE_REACH = 8;
    /**
     * Ticks to reach a horse before giving up and to ride home before getting off in place (both at least, and more
     * for a far one: {@link MountedPace#errandTicks}), and to wait before looking again.
     */
    static final int FETCH_TICKS = 600, RIDE_HOME_TICKS = 1200, LOOK_AGAIN = 200, GIVE_UP_REST = 1200;
    /**
     * A rider steers through the horse's navigation, which plans paths only as far as the horse's follow range (16
     * blocks, against a villager's 48), so a patrol leg or the ride home would go in short hops. While a resident
     * rides, the horse plans as far as a villager does. Transient (never saved): taken off on dismount, and put back
     * when a mounted resident and their horse load again ({@link #loaded}).
     */
    private static final Identifier RIDER_REACH = VillageBlocks.id("rider_reach");
    static final double RIDER_REACH_BONUS = 32;

    /** Knights on their way to a stable horse: which horse (no one else takes it meanwhile) and until when they try. */
    private record Fetch(UUID horse, long until) {}
    private static final Map<UUID, Fetch> fetching = new HashMap<>();
    /** Mounted knights whose watch ended: until when they ride home before getting off where they are. */
    private static final Map<UUID, Long> rideHomeUntil = new HashMap<>();
    /** When a knight may look for a horse again after finding none or giving up. */
    private static final Map<UUID, Long> nextLook = new HashMap<>();
    /** Companions already checked for a spare horse during the player's current ride (cleared when they dismount). */
    private static final Set<UUID> checked = new HashSet<>();

    public static void clear() { fetching.clear(); rideHomeUntil.clear(); nextLook.clear(); checked.clear(); }
    /**
     * A mounted resident or their horse loaded back in (a chunk or the world reloading): the follow-range bonus
     * was never saved, so it goes back on. Passengers load with their vehicle; whichever of the two loads second
     * sees the other.
     */
    public static void loaded(Entity e) {
        if (e instanceof Villager v && v.getVehicle() instanceof AbstractHorse h && !order(v).isEmpty()) reach(h, true);
        else if (e instanceof AbstractHorse h && h.getFirstPassenger() instanceof Villager v && !order(v).isEmpty()) reach(h, true);
    }
    /** A villager or horse left the world: forget their errands. */
    public static void unload(Entity e) {
        if (e instanceof Villager v) { var id = v.getUUID(); fetching.remove(id); rideHomeUntil.remove(id); nextLook.remove(id); checked.remove(id); }
        else if (e instanceof AbstractHorse h) fetching.values().removeIf(f -> f.horse().equals(h.getUUID()));
    }

    // -- the seams Village Friends calls ------------------------------------------------------------

    /** Riding a horse (so the routine keeps steering them instead of handing a passenger back to vanilla). */
    public static boolean mounted(Villager v) { return v.getVehicle() instanceof AbstractHorse; }
    /**
     * Seated by {@code PackAnimals.mountGuard} for a caravan (order "caravan") and still on the horse: their routine
     * and their villager brain stay off, so only the caller steers them. A guard still fights first.
     */
    public static boolean caravan(Villager v) { return v.getVehicle() instanceof AbstractHorse && CARAVAN.equals(target(v).getAttached(StableData.MOUNT_ORDER)); }
    /** Why a resident is riding ("patrol", "companion" or "caravan"), or "" with no order. */
    public static String order(Villager v) { return target(v).getAttachedOrElse(StableData.MOUNT_ORDER, ""); }

    /** Mounting for the night watch and riding back to the stable afterwards; true while it is steering them this update. */
    public static boolean update(Villager v, ServerLevel level, Routine.Plan plan) {
        String order = order(v);
        if (v.getVehicle() instanceof AbstractHorse horse) {
            if (!order.equals(PATROL)) return false;
            if (plan.block() == Routine.Block.NIGHT_WATCH || plan.block() == Routine.Block.DEFEND) { rideHomeUntil.remove(v.getUUID()); return false; }
            return rideHome(v, level, horse);
        }
        // Their horse is gone (it died, or a knockout or the alarm pulled them off): forget the order.
        if (!order.isEmpty()) dismount(v);
        if (plan.block() != Routine.Block.NIGHT_WATCH || v.isBaby() || !profession(v).equals("knight")) { fetching.remove(v.getUUID()); return false; }
        return fetch(v, level);
    }
    /** What to multiply a walking speed modifier by: 1 on foot; on horseback it keeps a mixed squad together. */
    public static double pace(Villager v) {
        if (!(v.getVehicle() instanceof AbstractHorse horse)) return 1.0;
        return MountedPace.modifier(1, MountedPace.RIDER_BASE, horse.getAttributeValue(Attributes.MOVEMENT_SPEED), squadMounted(v));
    }
    /** How much wider patrol followers keep their distance (horses are wider than people). */
    public static double spacing(Villager v) { return MountedPace.spacing(mounted(v)); }
    /** A companion following a mounted player rides a spare horse; true while it is steering them this tick. */
    public static boolean companion(Villager v, ServerPlayer p, ServerLevel level, String mode) {
        String order = v.getVehicle() instanceof AbstractHorse ? order(v) : null;
        if (!mode.equals("follow") || !(p.getVehicle() instanceof AbstractHorse)) {
            checked.remove(v.getUUID());
            if (order != null && !order.equals(CARAVAN)) dismount(v);
            return false;
        }
        if (order == null) {
            // Looked for once, the moment the player is seen in the saddle; no horse close by means they walk.
            if (!checked.add(v.getUUID())) return false;
            var horse = spare(v, p, level);
            if (horse == null || !mount(v, horse, COMPANION)) return false;
            order = COMPANION;
        }
        if (order.equals(CARAVAN)) return false;
        v.getLookControl().setLookAt(p, 30, 30);
        // Modifier 1 at the horse's own speed is how fast a horse under a player goes.
        if (v.tickCount % 10 == 0) { if (v.distanceToSqr(p) > 5 * 5) v.getNavigation().moveTo(p, 1.0); else v.getNavigation().stop(); }
        return true;
    }
    /** Takes a resident off a horse and clears their order (teleporting a passenger would snap them back to it). */
    public static void dismount(Villager v) {
        if (v.getVehicle() instanceof AbstractHorse horse) { v.stopRiding(); reach(horse, false); }
        if (target(v).hasAttached(StableData.MOUNT_ORDER)) target(v).removeAttached(StableData.MOUNT_ORDER);
        // Released or sent home: if they are taken along again, they look for a spare horse afresh.
        fetching.remove(v.getUUID()); rideHomeUntil.remove(v.getUUID()); checked.remove(v.getUUID());
    }

    // -- getting on ----------------------------------------------------------------------------------

    /**
     * Seats a resident on a horse with an order. False for a baby or a dead resident, an empty order, or a horse that
     * isn't a tame, living adult with no rider in the same world.
     */
    public static boolean mount(Villager v, AbstractHorse horse, String order) {
        if (v.level().isClientSide() || !v.isAlive() || v.isBaby() || order == null || order.isEmpty()) return false;
        if (horse.level() != v.level() || !horse.isAlive() || horse.isRemoved() || horse.isBaby() || !horse.isTamed() || horse.isVehicle()) return false;
        if (v.isSleeping()) v.stopSleeping();
        if (v.isPassenger()) { if (v.getVehicle() instanceof AbstractHorse old) reach(old, false); v.stopRiding(); }
        if (!v.startRiding(horse, true, true)) return false;
        reach(horse, true);
        target(v).setAttached(StableData.MOUNT_ORDER, order);
        fetching.remove(v.getUUID()); rideHomeUntil.remove(v.getUUID());
        // Whatever they were walking to on foot is not where the horse should go.
        v.getBrain().eraseMemory(MemoryModuleType.WALK_TARGET);
        v.getNavigation().stop();
        return true;
    }
    /** Lets the horse plan paths as far as a villager does while a resident rides it, or puts its own range back. */
    private static void reach(AbstractHorse horse, boolean ridden) {
        var range = horse.getAttribute(Attributes.FOLLOW_RANGE);
        if (range == null) return;
        if (!ridden) range.removeModifier(RIDER_REACH);
        else if (!range.hasModifier(RIDER_REACH)) range.addTransientModifier(new AttributeModifier(RIDER_REACH, RIDER_REACH_BONUS, AttributeModifier.Operation.ADD_VALUE));
    }

    // -- the night watch -----------------------------------------------------------------------------

    /** On foot at the start of the watch: pick a stable horse, walk to it, swing up. True while walking to it. */
    private static boolean fetch(Villager v, ServerLevel level) {
        long now = level.getGameTime();
        var errand = fetching.get(v.getUUID());
        AbstractHorse horse = null;
        if (errand != null) {
            horse = level.getEntity(errand.horse()) instanceof AbstractHorse h ? h : null;
            if (horse == null || !free(horse, v, now) || now > errand.until()) {
                fetching.remove(v.getUUID()); nextLook.put(v.getUUID(), now + GIVE_UP_REST);
                return false;
            }
        } else {
            if (now < nextLook.getOrDefault(v.getUUID(), Long.MIN_VALUE)) return false;
            horse = pick(v, level, now);
            if (horse == null) { nextLook.put(v.getUUID(), now + LOOK_AGAIN); return false; }
            // A stable on the outer streets is a long walk from the bell: the allowance grows with the distance.
            fetching.put(v.getUUID(), new Fetch(horse.getUUID(), now + MountedPace.errandTicks(v.distanceTo(horse), FETCH_TICKS)));
        }
        if (v.distanceToSqr(horse) <= MOUNT_REACH * MOUNT_REACH) {
            if (!mount(v, horse, PATROL)) { fetching.remove(v.getUUID()); nextLook.put(v.getUUID(), now + LOOK_AGAIN); }
            // In the saddle the patrol steers them (and the horse) from here.
            return false;
        }
        ResidentRoutines.walk(v, horse.blockPosition(), .6F, 1);
        return true;
    }
    /** The nearest free horse stalled in the knight's village (the one around their bell), or null. */
    private static @Nullable AbstractHorse pick(Villager v, ServerLevel level, long now) {
        BlockPos bell = v.getBrain().getMemory(MemoryModuleType.MEETING_POINT).filter(p -> p.dimension() == level.dimension()).map(GlobalPos::pos).orElse(null);
        if (bell == null) return null;
        return villageHorses(level, bell).stream().filter(h -> free(h, v, now)).min(Comparator.comparingDouble(v::distanceToSqr)).orElse(null);
    }
    /**
     * Loaded horses stalled in the village around {@code bell}. The village's own stable usually stands on its outer
     * streets, well past any fixed reach from the bell, so this takes the village record's whole box (up to
     * {@link #VILLAGE_REACH} from its centre, plus the six blocks a stalled horse may stray) and keeps the horses
     * whose stall is in that village. Only with no village record around the bell does it fall back to
     * {@link #STABLE_REACH} blocks from the bell. One entity-section lookup per try, at most every
     * {@link #LOOK_AGAIN} ticks per knight on the watch.
     */
    private static List<AbstractHorse> villageHorses(ServerLevel level, BlockPos bell) {
        VillageRecord village = VillageSettlements.book(level).at(bell);
        if (village == null) return Stables.stalledHorses(level, bell, STABLE_REACH);
        int r = Math.min(village.radius(), VILLAGE_REACH) + 8;
        var box = new AABB(village.x() - r, village.y() - 80, village.z() - r, village.x() + r + 1, village.y() + 81, village.z() + r + 1);
        String here = level.dimension().identifier().toString();
        return level.getEntitiesOfClass(AbstractHorse.class, box, h -> h.isAlive()
                && Stables.stallOf(h).filter(s -> s.dimension().equals(here) && s.village().equals(village.id())).isPresent());
    }
    /**
     * A stable horse a knight may take: a tame, healthy adult horse kept by a resident or the village (never a player's),
     * home and not stolen, with no rider or lead, and not already being fetched by someone else.
     */
    private static boolean free(AbstractHorse h, Villager by, long now) {
        if (!(h instanceof Horse) || !h.isAlive() || h.isRemoved() || !h.isTamed() || h.isBaby() || h.isVehicle() || h.isLeashed() || h.isNoAi()) return false;
        StallHome stall = Stables.stallOf(h).orElse(null);
        if (stall == null || !stall.residentOwned() || !stall.stolenBy().isEmpty() || stall.awaySince() != 0) return false;
        for (var e : fetching.entrySet())
            if (!e.getKey().equals(by.getUUID()) && e.getValue().horse().equals(h.getUUID()) && now <= e.getValue().until()) return false;
        return true;
    }
    /**
     * After the watch: back to the horse's stall and off, or off where they are once the ride home has taken too long
     * (a minute, or longer when the watch ended far from the stable).
     */
    private static boolean rideHome(Villager v, ServerLevel level, AbstractHorse horse) {
        long now = level.getGameTime();
        String here = level.dimension().identifier().toString();
        BlockPos stall = Stables.stallOf(horse).filter(s -> s.dimension().equals(here)).map(StallHome::stall).orElse(null);
        double away = stall == null ? 0 : Math.sqrt(horse.distanceToSqr(Vec3.atBottomCenterOf(stall)));
        long until = rideHomeUntil.computeIfAbsent(v.getUUID(), k -> now + MountedPace.errandTicks(away, RIDE_HOME_TICKS));
        if (stall == null || now > until || away <= HOME_REACH) {
            dismount(v);
            return false;
        }
        ResidentRoutines.walk(v, stall, .5F, 1);
        return true;
    }

    // -- companions ----------------------------------------------------------------------------------

    /** The nearest spare horse, donkey or mule the player owns within {@link #SPARE_REACH} blocks of the companion. */
    private static @Nullable AbstractHorse spare(Villager v, ServerPlayer p, ServerLevel level) {
        var ridden = p.getVehicle();
        return level.getEntitiesOfClass(AbstractHorse.class, v.getBoundingBox().inflate(SPARE_REACH), h -> h != ridden && rideable(h) && h.isAlive()
                        && h.isTamed() && !h.isBaby() && !h.isVehicle() && !h.isLeashed() && !h.isNoAi() && owned(h, p) && v.distanceToSqr(h) <= SPARE_REACH * SPARE_REACH)
                .stream().min(Comparator.comparingDouble(v::distanceToSqr)).orElse(null);
    }
    /** Horses, donkeys and mules: what residents ride (not llamas, camels or undead horses). */
    public static boolean rideable(AbstractHorse h) { return h instanceof Horse || h instanceof Donkey || h instanceof Mule; }
    private static boolean owned(AbstractHorse h, ServerPlayer p) {
        var owner = h.getOwnerReference();
        return owner != null && owner.getUUID().equals(p.getUUID());
    }

    // -- pace ------------------------------------------------------------------------------------------

    /** Everyone in this rider's patrol squad is on horseback too (a lone rider counts as a mounted squad). */
    private static boolean squadMounted(Villager v) {
        if (!(v.level() instanceof ServerLevel level)) return true;
        for (var id : GuardPatrols.squad(v.getUUID())) if (!(level.getEntity(id) instanceof Villager m) || !mounted(m)) return false;
        return true;
    }

    private Mounts() {}
}
