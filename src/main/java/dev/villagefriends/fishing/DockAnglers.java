package dev.villagefriends.fishing;

import dev.villagefriends.ResidentRoutines;
import dev.villagefriends.VillageFriends;
import dev.villagefriends.VillageRecord;
import dev.villagefriends.VillageSettlements;
import dev.villagefriends.routine.Routine;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;
import java.util.UUID;
import net.fabricmc.fabric.api.attachment.v1.AttachmentRegistry;
import net.fabricmc.fabric.api.attachment.v1.AttachmentSyncPredicate;
import net.fabricmc.fabric.api.attachment.v1.AttachmentTarget;
import net.fabricmc.fabric.api.attachment.v1.AttachmentType;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.FluidTags;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.ai.memory.MemoryModuleType;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.level.levelgen.Heightmap;

/**
 * Residents who fish. A village's fisherman spends his mornings (and all of contest day) fishing off the village
 * dock, and residents whose hobby is fishing do too in their free time, or from the bank where they are when
 * there's no dock. At their place they cast, wait, feel the bite, reel in and hold up what they caught (or shrug
 * when it gets away), round and round. The phase is shared with clients as {@link #STATE}
 * ("phase|x|y|z|item": where the bobber is and the catch in hand) for the {@code angling} clips, the rod in their
 * hand and the line. Driven once a second from {@code ResidentRoutines}; their catches enter the contest.
 */
public final class DockAnglers {
    /** On a resident, shared with clients while they fish: "cast|x|y|z|", "wait|...", "bite", "reel", "catch|x|y|z|item", "lost". */
    public static final AttachmentType<String> STATE = AttachmentRegistry.create(Fishing.id("angling"),
            b -> b.syncWith(ByteBufCodecs.STRING_UTF8, AttachmentSyncPredicate.all()));

    private record Session(BlockPos stand, BlockPos cast, long spot, String phase, long until) {
        Session next(String phase, long until) { return new Session(stand, cast, spot, phase, until); }
    }
    private record Landed(Fish fish, long at) {}
    private static final Map<UUID, Session> SESSIONS = new HashMap<>();
    private static final Map<Long, UUID> TAKEN = new HashMap<>();
    private static final Map<UUID, Landed> LANDED = new HashMap<>();
    private static final Map<String, BlockPos> VILLAGE_WATER = new HashMap<>();
    private static final Random RANDOM = new Random();

    static void register() { ServerTickEvents.END_SERVER_TICK.register(DockAnglers::tick); }
    public static void clear() { SESSIONS.clear(); TAKEN.clear(); LANDED.clear(); VILLAGE_WATER.clear(); }

    /** Whether this resident is at their place with a line in the water. */
    public static boolean angling(Villager v) {
        var s = SESSIONS.get(v.getUUID());
        return s != null && s.phase() != null;
    }
    /** What they landed in the last two minutes, for "look at this {catch}!". */
    public static Fish lastCatch(Villager v) {
        var l = LANDED.get(v.getUUID());
        return l == null || v.level().getGameTime() - l.at() > 2400 ? null : l.fish();
    }
    /** The status line: "Fishing off the dock". */
    public static String doing(Villager v, String otherwise) {
        var s = SESSIONS.get(v.getUUID());
        if (s == null) return otherwise;
        return s.phase() == null ? "Off to fish" : s.spot() != 0 ? "Fishing off the dock" : "Fishing";
    }

    /** While they fish, their vanilla work at the barrel is set aside (it would walk them off the dock). */
    public static net.minecraft.world.entity.schedule.Activity activity(Villager v, net.minecraft.world.entity.schedule.Activity planned) {
        return SESSIONS.containsKey(v.getUUID()) ? net.minecraft.world.entity.schedule.Activity.IDLE : planned;
    }

    /** True while this resident is fishing (or on their way to). */
    public static boolean update(Villager v, ServerLevel level, Routine.Plan plan) {
        var s = SESSIONS.get(v.getUUID());
        if (!wants(v, level, plan)) { if (s != null) stop(v); return false; }
        if (s == null) {
            s = start(v, level, plan);
            if (s == null) return false;
            SESSIONS.put(v.getUUID(), s);
        }
        if (s.phase() == null) {
            if (!s.stand().closerToCenterThan(v.position(), 1.2)) { ResidentRoutines.walk(v, s.stand(), .5F, 0); return true; }
            v.getNavigation().stop();
            v.getBrain().eraseMemory(MemoryModuleType.WALK_TARGET);
            s = s.next("cast", level.getGameTime() + 30);
            SESSIONS.put(v.getUUID(), s);
            show(v, s, "");
        }
        // Idle wandering doesn't take them off their place.
        if (!s.stand().closerToCenterThan(v.position(), 1.6)) ResidentRoutines.walk(v, s.stand(), .5F, 0);
        else { v.getNavigation().stop(); v.getBrain().eraseMemory(MemoryModuleType.WALK_TARGET); }
        advance(v, level, s);
        return true;
    }

    private static boolean wants(Villager v, ServerLevel level, Routine.Plan plan) {
        if (v.isBaby() || v.isSleeping() || v.isPassenger()) return false;
        boolean fisherman = VillageFriends.profession(v).equals("fisherman"), angler = "fishing".equals(VillageFriends.profile(v).hobby());
        if (!fisherman && !angler) return false;
        var village = VillageSettlements.home(v);
        boolean contest = village != null && Contests.phase(level, village.id()) == Contest.Phase.OPEN;
        var block = plan.block();
        if (contest && (block == Routine.Block.WORK || block == Routine.Block.HOBBY || block == Routine.Block.SOCIAL || block == Routine.Block.MARKET)) return true;
        int time = Math.floorMod(ResidentRoutines.timeOfDay(level), 24000);
        if (fisherman && block == Routine.Block.WORK) return time < 5000 && village != null && Docks.dock(level, village.id()) != null;
        return angler && block == Routine.Block.HOBBY;
    }

    private static Session start(Villager v, ServerLevel level, Routine.Plan plan) {
        var village = VillageSettlements.home(v);
        var dock = village == null ? null : Docks.dock(level, village.id());
        if (dock != null) {
            for (int i = 0; i < dock.spots().size(); i++) {
                long spot = dock.spots().get(i);
                var holder = TAKEN.get(spot);
                if (holder != null && !holder.equals(v.getUUID()) && SESSIONS.containsKey(holder)) continue;
                TAKEN.put(spot, v.getUUID());
                return new Session(BlockPos.of(spot), BlockPos.of(dock.casts().get(i)), spot, null, 0);
            }
        }
        // No dock (or it's full): fish from the bank, if they're beside the water.
        var here = v.blockPosition();
        for (int r = 2; r <= 5; r++) for (var dir : net.minecraft.core.Direction.Plane.HORIZONTAL) {
            var p = here.relative(dir, r);
            int y = level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, p.getX(), p.getZ()) - 1;
            var w = new BlockPos(p.getX(), y, p.getZ());
            if (level.getFluidState(w).is(FluidTags.WATER) && Math.abs(y - here.getY()) <= 3) return new Session(here, w, 0, null, 0);
        }
        return null;
    }

    private static void advance(Villager v, ServerLevel level, Session s) {
        long now = level.getGameTime();
        if (now < s.until()) return;
        var c = s.cast();
        Session next;
        switch (s.phase()) {
            case "cast" -> next = s.next("wait", now + 200 + RANDOM.nextInt(600));
            case "wait" -> {
                next = s.next("bite", now + 20);
                level.sendParticles(ParticleTypes.SPLASH, c.getX() + .5, c.getY() + 1, c.getZ() + .5, 8, .2, 0, .2, .1);
                level.playSound(null, c, SoundEvents.FISHING_BOBBER_SPLASH, SoundSource.NEUTRAL, .4F, 1);
            }
            case "bite" -> next = s.next("reel", now + 60);
            case "reel" -> {
                var fish = RANDOM.nextInt(4) > 0 ? Catches.pick(FishTable.all(), Angling.spot(level, c, true), new Catches.Odds(1, null, null, Gear.Rod.PLAIN), RANDOM) : null;
                if (fish != null && fish.legendary()) fish = null;
                level.playSound(null, v.blockPosition(), SoundEvents.FISHING_BOBBER_RETRIEVE, SoundSource.NEUTRAL, .6F, 1);
                if (fish == null) { next = s.next("lost", now + 40); show(v, next, ""); SESSIONS.put(v.getUUID(), next); return; }
                LANDED.put(v.getUUID(), new Landed(fish, now));
                Contests.residentCaught(level, v, fish, Catches.size(fish, RANDOM, 1, false));
                level.sendParticles(ParticleTypes.SPLASH, c.getX() + .5, c.getY() + 1, c.getZ() + .5, 12, .3, .1, .3, .2);
                next = s.next("catch", now + 50);
                show(v, next, fish.item());
                SESSIONS.put(v.getUUID(), next);
                return;
            }
            default -> next = s.next("cast", now + 30 + RANDOM.nextInt(40));
        }
        SESSIONS.put(v.getUUID(), next);
        show(v, next, "");
    }
    private static void show(Villager v, Session s, String item) {
        var c = s.cast();
        ((AttachmentTarget) v).setAttached(STATE, s.phase() + "|" + c.getX() + "|" + c.getY() + "|" + c.getZ() + "|" + item);
    }
    private static void stop(Villager v) {
        var s = SESSIONS.remove(v.getUUID());
        if (s != null && s.spot() != 0) TAKEN.remove(s.spot(), v.getUUID());
        ((AttachmentTarget) v).removeAttached(STATE);
    }

    /** Keeps everyone at their place facing out over the water. */
    private static void tick(MinecraftServer server) {
        if (SESSIONS.isEmpty()) return;
        var it = SESSIONS.entrySet().iterator();
        while (it.hasNext()) {
            var e = it.next(); var s = e.getValue();
            if (s.phase() == null) continue;
            Villager v = null;
            for (var level : server.getAllLevels()) if (level.getEntity(e.getKey()) instanceof Villager found) { v = found; break; }
            if (v == null || !v.isAlive()) { it.remove(); if (s.spot() != 0) TAKEN.remove(s.spot(), e.getKey()); continue; }
            double dx = s.cast().getX() + .5 - v.getX(), dz = s.cast().getZ() + .5 - v.getZ();
            float yaw = (float) (Mth.atan2(dz, dx) * Mth.RAD_TO_DEG) - 90;
            v.setYRot(yaw); v.setYBodyRot(yaw); v.setYHeadRot(yaw);
            v.getLookControl().setLookAt(s.cast().getX() + .5, s.cast().getY() + .8, s.cast().getZ() + .5);
        }
    }

    /** The village's water as the fish table sees it: off the end of its dock, or the nearest water to its centre. */
    public static Spot villageSpot(ServerLevel level, VillageRecord village) {
        var dock = Docks.dock(level, village.id());
        if (dock != null) return Angling.spot(level, BlockPos.of(dock.casts().get(1)), true);
        var cached = VILLAGE_WATER.get(village.id());
        if (cached != null) return Angling.spot(level, cached, true);
        for (int r = 8; r <= Math.min(village.radius(), 96); r += 8) {
            for (int a = 0; a < 16; a++) {
                int x = village.x() + (int) Math.round(Math.cos(a * Math.PI / 8) * r), z = village.z() + (int) Math.round(Math.sin(a * Math.PI / 8) * r);
                if (!level.hasChunk(x >> 4, z >> 4)) continue;
                int y = level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, x, z) - 1;
                var p = new BlockPos(x, y, z);
                if (!level.getFluidState(p).is(FluidTags.WATER)) continue;
                VILLAGE_WATER.put(village.id(), p);
                return Angling.spot(level, p, true);
            }
        }
        return null;
    }

    private DockAnglers() {}
}
