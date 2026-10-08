package dev.villagefriends;

import java.util.*;
import net.minecraft.core.BlockPos;
import net.minecraft.core.GlobalPos;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.ai.memory.MemoryModuleType;
import net.minecraft.world.entity.ai.util.DefaultRandomPos;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.phys.Vec3;
import dev.villagefriends.home.Homes;

/**
 * When a player knocks out (or kills) a resident, the neighbors who are about panic: they drop what they're
 * doing, run home and stay indoors for a minute. Guards don't run, they answer the alarm (see
 * {@link GuardController#call}).
 */
public final class VillageAlarm {
    /** Residents this close to the victim flee, and everyone in the same village out to {@value #VILLAGE_REACH}. */
    public static final int NEAR = 40, VILLAGE_REACH = 96;
    /** How long they stay indoors: a minute. */
    public static final int HIDE_TICKS = 20 * 60;
    /** Running speed: vanilla's panic speed (they stroll at .5). */
    static final double RUN = .75;
    private static final class Flight {
        final ServerLevel level; final Vec3 from; final long until;
        BlockPos home; long lastProgress; Vec3 lastPosition; boolean arrived;
        Flight(ServerLevel level, BlockPos home, Vec3 from, long until, Villager v) {
            this.level = level; this.home = home; this.from = from; this.until = until; lastProgress = level.getGameTime(); lastPosition = v.position();
        }
    }
    private record Alarm(ServerLevel level, BlockPos at, int radius, long until) {}
    private static final Map<UUID, Flight> fleeing = new HashMap<>();
    private static final List<Alarm> alarms = new ArrayList<>();

    public static void clear() { fleeing.clear(); alarms.clear(); }
    public static void unload(Villager v) { fleeing.remove(v.getUUID()); }
    public static void tick(MinecraftServer server) {
        if (server.getTickCount() % 20 != 0) return;
        alarms.removeIf(a -> a.level().getGameTime() >= a.until());
        fleeing.values().removeIf(f -> f.level.getGameTime() >= f.until);
    }
    /** Running home or hiding there after an alarm: the alarm moves them, not their brain or routine. */
    public static boolean fleeing(Villager v) { return fleeing.containsKey(v.getUUID()); }
    /** For tests and debugging: where they're running to. */
    public static String describe(Villager v) {
        var f = fleeing.get(v.getUUID());
        return f == null ? "calm" : "home=" + f.home + " arrived=" + f.arrived + " left=" + (f.until - f.level.getGameTime());
    }
    /** An alarm is still ringing around here (children don't start games, for one). */
    public static boolean raised(ServerLevel level, BlockPos pos) {
        for (var a : alarms) if (a.level() == level && a.at().closerThan(pos, a.radius())) return true;
        return false;
    }
    /** The village whose grounds this is, or null out in the wild. */
    public static VillageRecord villageAt(ServerLevel level, BlockPos pos) {
        VillageRecord best = null;
        for (var village : VillageSettlements.book(level).villages().values())
            if (village.contains(pos) && (best == null || village.radius() < best.radius())) best = village;
        return best;
    }

    /** A player has just knocked out (or killed) {@code victim}: everyone who saw it runs home, guards come running. */
    public static void raise(Villager victim, ServerLevel level, Entity culprit) {
        var village = villageAt(level, victim.blockPosition());
        int radius = village == null ? NEAR : Math.clamp(village.radius(), NEAR, VILLAGE_REACH);
        long now = level.getGameTime();
        alarms.add(new Alarm(level, victim.blockPosition(), radius, now + HIDE_TICKS));
        var from = culprit != null ? culprit.position() : victim.position();
        for (var v : level.getEntitiesOfClass(Villager.class, victim.getBoundingBox().inflate(radius, 24, radius),
                v -> v != victim && v.isAlive() && (village == null ? v.distanceToSqr(victim) <= NEAR * NEAR : village.contains(v.blockPosition())))) {
            if (GuardController.isGuard(v) || v.isNoAi() || v.isSleeping() || Knockouts.injured(v) || CompanionController.state(v).active()) continue;
            flee(v, level, from, now);
        }
    }
    private static void flee(Villager v, ServerLevel level, Vec3 from, long now) {
        dev.villagefriends.tavern.Taverns.leave(v);
        dev.villagefriends.play.Playground.excuse(v);
        if (v.isPassenger()) v.stopRiding();
        v.setTradingPlayer(null); v.stopUsingItem();
        var brain = v.getBrain();
        brain.eraseMemory(MemoryModuleType.WALK_TARGET); brain.eraseMemory(MemoryModuleType.LOOK_TARGET);
        var home = home(v, level);
        if (home == null) home = away(v, from);
        boolean first = !fleeing(v);
        fleeing.put(v.getUUID(), new Flight(level, home, from, now + HIDE_TICKS, v));
        if (first) VillageSocieties.emote(v, Emote.EXCLAIM, level.getRandom().nextInt(6));
        if (home != null) v.getNavigation().moveTo(home.getX() + .5, home.getY(), home.getZ() + .5, RUN);
    }
    /** Nowhere to hide: somewhere well away from them (straight away if no better spot turns up). */
    private static BlockPos away(Villager v, Vec3 from) {
        var away = DefaultRandomPos.getPosAway(v, 16, 7, from);
        if (away == null) {
            var direction = v.position().subtract(from).multiply(1, 0, 1);
            if (direction.lengthSqr() < 1e-4) direction = new Vec3(1, 0, 0);
            away = v.position().add(direction.normalize().scale(14));
        }
        return BlockPos.containing(away);
    }
    /** Inside their own house, else their vanilla home (bed) if it's in reach. */
    private static BlockPos home(Villager v, ServerLevel level) {
        var house = Homes.houseOf(v);
        var inside = house == null ? null : Homes.hearth(level, house);
        if (inside != null && inside.closerToCenterThan(v.position(), VILLAGE_REACH * 1.5)) return inside;
        return v.getBrain().getMemory(MemoryModuleType.HOME).filter(h -> h.dimension() == level.dimension()).map(GlobalPos::pos)
                .filter(h -> h.closerToCenterThan(v.position(), VILLAGE_REACH * 1.5)).orElse(null);
    }

    /** Runs instead of the brain while fleeing. Returns false once they're calm again. */
    public static boolean drive(Villager v, ServerLevel level) {
        var f = fleeing.get(v.getUUID());
        if (f == null) return false;
        long now = level.getGameTime();
        if (f.level != level || now >= f.until || Knockouts.injured(v) || CompanionController.state(v).active()) {
            fleeing.remove(v.getUUID()); v.getNavigation().stop(); return false;
        }
        if (v.isSleeping()) return true;
        if (f.home == null || f.arrived) { v.getNavigation().stop(); return true; }
        if (v.position().distanceToSqr(Vec3.atBottomCenterOf(f.home)) <= 1.5 * 1.5) {
            f.arrived = true; v.getNavigation().stop();
            VillageSocieties.emote(v, Emote.SWEAT, 0);
            return true;
        }
        if (v.position().distanceToSqr(f.lastPosition) > 1) { f.lastPosition = v.position(); f.lastProgress = now; }
        // Stuck (no path in): stay put where they are rather than run on the spot.
        if (now - f.lastProgress > 200) { f.arrived = true; v.getNavigation().stop(); return true; }
        if (now % 10 == 0)
            v.getNavigation().moveTo(f.home.getX() + .5, f.home.getY(), f.home.getZ() + .5, RUN);
        return true;
    }
    private VillageAlarm() {}
}
