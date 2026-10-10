package dev.villagefriends;

import static dev.villagefriends.VillageFriends.*;
import dev.villagefriends.routine.Routine;
import java.util.*;
import net.minecraft.core.BlockPos;
import net.minecraft.core.GlobalPos;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.ai.memory.MemoryModuleType;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.raid.Raid;
import net.minecraft.world.entity.raid.Raider;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.phys.Vec3;

/**
 * Guard duty beyond the single fight. At night the village's guards walk a loop around the village in
 * squads of two or three: if fewer than two of a village's guards keep the night watch, the next guards on
 * the roster are called up for the night, and a village with a single guard keeps them standing watch at
 * the bell instead of walking alone. During a raid, guards don't hide: they wake, muster at the bell and
 * go after the raiders, leaving the fighting itself to {@link GuardController}.
 */
public final class GuardPatrols {
    /** Called up for tonight's watch because their village had fewer than two guards on it. */
    private static final Set<UUID> drafted = new HashSet<>();
    private static final Map<UUID, Squad> squads = new HashMap<>();
    /** Drafted guards are on watch from after supper until dawn. */
    private static final int DRAFT_FROM = Routine.at(19, 0), DRAFT_UNTIL = Routine.at(6, 0) + 24000;

    private static final class Squad {
        final List<UUID> members; final BlockPos anchor;
        List<BlockPos> route = List.of(); int leg; long legStarted;
        Squad(List<UUID> members, BlockPos anchor) { this.members = members; this.anchor = anchor; }
    }

    public static void clear() { drafted.clear(); squads.clear(); }
    public static void unload(Villager v) { squads.remove(v.getUUID()); }
    /** Everyone in this guard's patrol squad tonight, leader first; empty when they have none. */
    public static List<UUID> squad(UUID guard) { var s = squads.get(guard); return s == null ? List.of() : s.members; }

    // -- who is on duty ----------------------------------------------------------------------------

    private static boolean onDuty(Villager v) {
        return GuardController.isGuard(v) && v.isAlive() && !v.isNoAi() && !Knockouts.injured(v)
                && !CompanionController.state(v).active() && !CompanionController.hasActivity(v);
    }
    /** The raid a guard should be fighting: one at or near their village that isn't over yet. */
    public static Raid raid(Villager v) {
        if (!(v.level() instanceof ServerLevel level)) return null;
        var raid = level.getRaidAt(v.blockPosition());
        return raid != null && !raid.isOver() ? raid : null;
    }
    public static boolean defending(Villager v) { return onDuty(v) && raid(v) != null; }
    /** Called up for tonight's watch, and it's that time. */
    public static boolean drafted(Villager v, int timeOfDay) {
        int t = timeOfDay < DRAFT_FROM ? timeOfDay + 24000 : timeOfDay;
        return drafted.contains(v.getUUID()) && t >= DRAFT_FROM && t < DRAFT_UNTIL;
    }

    /** How a village's watch splits up: squads of two, the last one taking a third when the count is odd. */
    public static List<Integer> squadSizes(int onWatch) {
        var sizes = new ArrayList<Integer>();
        if (onWatch < 2) return sizes;
        for (int i = 0; i < onWatch / 2; i++) sizes.add(2);
        if (onWatch % 2 == 1) sizes.set(sizes.size() - 1, 3);
        return sizes;
    }
    /** How many of a village's guards must be called up so at least two keep the watch. */
    public static int draftsNeeded(int guards, int watchers) { return guards < 2 ? 0 : Math.max(0, 2 - watchers); }

    /** Every five seconds: work out each village's watch roster and its patrol squads. */
    public static void tick(MinecraftServer server) {
        if (server.getTickCount() % 100 != 0) return;
        // A village is the guards who share a bell; a guard who knows no bell joins whichever village is near.
        var villages = new LinkedHashMap<BlockPos, List<Villager>>();
        var homeless = new ArrayList<Villager>();
        for (var v : CompanionController.loaded) {
            if (!onDuty(v) || !(v.level() instanceof ServerLevel)) continue;
            var bell = bell(v);
            if (bell != null) villages.computeIfAbsent(bell, k -> new ArrayList<>()).add(v); else homeless.add(v);
        }
        for (var v : homeless) {
            var near = villages.keySet().stream().filter(a -> a.distToCenterSqr(v.position()) < 48 * 48)
                    .min(Comparator.comparingDouble(a -> a.distToCenterSqr(v.position()))).orElse(null);
            villages.computeIfAbsent(near != null ? near : v.blockPosition(), k -> new ArrayList<>()).add(v);
        }
        drafted.clear();
        var next = new HashMap<UUID, Squad>();
        for (var e : villages.entrySet()) {
            var guards = e.getValue();
            guards.sort(Comparator.comparingInt(ResidentRoutines::seed));
            int watchers = (int) guards.stream().filter(g -> Routine.nightWatch(ResidentRoutines.seed(g), profession(g))).count();
            int needed = draftsNeeded(guards.size(), watchers);
            for (var g : guards) {
                if (needed == 0) break;
                if (!Routine.nightWatch(ResidentRoutines.seed(g), profession(g))) { drafted.add(g.getUUID()); needed--; }
            }
            var watch = guards.stream().filter(g -> Routine.Block.NIGHT_WATCH.id().equals(target(g).getAttached(ROUTINE)) && !GuardController.fighting(g)).toList();
            int from = 0;
            for (int size : squadSizes(watch.size())) {
                var members = watch.subList(from, from + size).stream().map(Villager::getUUID).toList();
                from += size;
                var old = squads.get(members.getFirst());
                var squad = old != null && old.members.equals(members) ? old : new Squad(members, e.getKey());
                for (var id : members) next.put(id, squad);
            }
        }
        squads.clear(); squads.putAll(next);
    }
    private static BlockPos bell(Villager v) {
        return v.getBrain().getMemory(MemoryModuleType.MEETING_POINT).filter(p -> p.dimension() == v.level().dimension()).map(GlobalPos::pos).orElse(null);
    }

    // -- night patrols -----------------------------------------------------------------------------

    /** Called once a second for a guard on night watch. */
    static void patrol(Villager v, ServerLevel level) {
        var squad = squads.get(v.getUUID());
        Villager leader = squad == null ? null : level.getEntity(squad.members.getFirst()) instanceof Villager l && l.isAlive() ? l : null;
        if (leader == null) { standWatch(v, level); return; }
        if (leader == v) lead(v, level, squad); else follow(v, leader, squad.members.indexOf(v.getUUID()));
    }
    private static void lead(Villager v, ServerLevel level, Squad squad) {
        long now = level.getGameTime();
        if (squad.route.isEmpty()) {
            squad.route = route(level, bell(v) != null ? bell(v) : v.blockPosition(), ResidentRoutines.seed(v));
            squad.leg = nearest(squad.route, v.blockPosition()); squad.legStarted = now;
        }
        var point = squad.route.get(squad.leg);
        boolean arrived = horizontal(v.position(), point) < 3.5 * 3.5;
        // Wait for anyone lagging behind; nobody walks the dark alone.
        Villager straggler = null;
        for (var id : squad.members) {
            if (level.getEntity(id) instanceof Villager m && m != v && m.isAlive() && !GuardController.fighting(m) && m.distanceToSqr(v) > 10 * 10) straggler = m;
        }
        if (straggler != null) {
            v.getBrain().eraseMemory(MemoryModuleType.WALK_TARGET); v.getNavigation().stop();
            v.getLookControl().setLookAt(straggler, 30, 30);
            return;
        }
        if (arrived || now - squad.legStarted > 600) {
            squad.leg = (squad.leg + 1) % squad.route.size(); squad.legStarted = now;
            point = squad.route.get(squad.leg);
        }
        ResidentRoutines.walk(v, point, .45F, 2);
    }
    /** Followers keep a pace behind the leader, side by side. */
    private static void follow(Villager v, Villager leader, int slot) {
        // Horses are wider than people: mounted followers keep wider gaps.
        double gap = dev.villagefriends.stable.ride.Mounts.spacing(v);
        if (v.distanceToSqr(leader) < 2.5 * gap * 2.5 * gap) return;
        var facing = Vec3.directionFromRotation(0, leader.getYRot());
        var side = new Vec3(-facing.z, 0, facing.x).scale(slot % 2 == 1 ? 1.3 * gap : -1.3 * gap);
        var spot = leader.position().subtract(facing.scale(1.8 * gap)).add(side);
        ResidentRoutines.walk(v, BlockPos.containing(spot), v.distanceToSqr(leader) > 12 * 12 ? .7F : .55F, 1);
    }
    /** A guard without a partner tonight keeps watch at the bell. */
    private static void standWatch(Villager v, ServerLevel level) {
        var bell = bell(v);
        if (bell == null) return;
        ResidentRoutines.walk(v, spot(level, bell, ResidentRoutines.seed(v), 4), .5F, 1);
    }
    /** A loop of up to eight checkpoints around the village, skipping roofs, water and drops. */
    public static List<BlockPos> route(ServerLevel level, BlockPos anchor, int seed) {
        var points = new ArrayList<BlockPos>();
        double start = Math.floorMod(seed, 360) * Math.PI / 180, turn = (seed & 1) == 0 ? 1 : -1;
        for (int i = 0; i < 8; i++) {
            double angle = start + turn * i * Math.PI / 4;
            for (int radius : new int[]{22, 16, 28, 11}) {
                int x = anchor.getX() + (int) Math.round(Math.cos(angle) * radius), z = anchor.getZ() + (int) Math.round(Math.sin(angle) * radius);
                if (!level.hasChunkAt(new BlockPos(x, anchor.getY(), z))) continue;
                var pos = new BlockPos(x, level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, x, z), z);
                if (Math.abs(pos.getY() - anchor.getY()) > 5 || !level.getFluidState(pos.below()).isEmpty() || !level.getFluidState(pos).isEmpty()) continue;
                points.add(pos); break;
            }
        }
        if (points.size() < 3) points.add(anchor);
        return points;
    }
    private static int nearest(List<BlockPos> route, BlockPos from) {
        int best = 0;
        for (int i = 1; i < route.size(); i++) if (route.get(i).distSqr(from) < route.get(best).distSqr(from)) best = i;
        return best;
    }
    private static double horizontal(Vec3 a, BlockPos b) {
        double dx = a.x - (b.getX() + .5), dz = a.z - (b.getZ() + .5);
        return dx * dx + dz * dz;
    }

    // -- raids -------------------------------------------------------------------------------------

    /** Called once a second for a guard during a raid: form up at the bell, then go after the raiders. */
    static void muster(Villager v, ServerLevel level) {
        var raid = raid(v);
        if (raid == null) return;
        var rally = bell(v) != null ? bell(v) : raid.getCenter();
        Raider nearest = null;
        if (raid.hasFirstWaveSpawned()) for (var r : raid.getAllRaiders()) {
            if (!r.isAlive() || r.level() != level || r.blockPosition().distSqr(rally) > 48 * 48) continue;
            if (nearest == null || r.distanceToSqr(v) < nearest.distanceToSqr(v)) nearest = r;
        }
        if (nearest != null) ResidentRoutines.walk(v, nearest.blockPosition(), .7F, 2);
        else ResidentRoutines.walk(v, spot(level, rally, ResidentRoutines.seed(v), 4), .7F, 1);
    }
    /** Each guard's own place in a ring around a point, so they don't all stand on one block. */
    private static BlockPos spot(ServerLevel level, BlockPos center, int seed, int radius) {
        double angle = Math.floorMod(seed * 47, 360) * Math.PI / 180;
        int x = center.getX() + (int) Math.round(Math.cos(angle) * radius), z = center.getZ() + (int) Math.round(Math.sin(angle) * radius);
        int y = level.hasChunkAt(new BlockPos(x, center.getY(), z)) ? level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, x, z) : center.getY();
        return Math.abs(y - center.getY()) > 4 ? center : new BlockPos(x, y, z);
    }
    private GuardPatrols() {}
}
