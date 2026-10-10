package dev.villagefriends;

import static dev.villagefriends.VillageFriends.*;

import dev.villagefriends.deed.DeedKind;
import dev.villagefriends.deed.Deeds;
import dev.villagefriends.stable.api.PackAnimals;
import dev.villagefriends.stable.api.Riders;
import dev.villagefriends.stable.api.Stables;
import dev.villagefriends.stable.data.StableBlocks;
import dev.villagefriends.stable.data.StallHome;
import dev.villagefriends.stable.ride.Mounts;
import dev.villagefriends.stable.ride.Spook;
import dev.villagefriends.stable.ride.SpookRule;
import java.util.UUID;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.minecraft.core.BlockPos;
import net.minecraft.core.GlobalPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.ai.memory.MemoryModuleType;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.phys.Vec3;

/**
 * {@link StablehandGameTest}'s riders scene: knights on the night watch, companions' horses, caravan guards, horse
 * theft and spooking. Each part starts from a clean pad and reports its own failure, so one broken part never hides
 * the others. Not-So-Vanilla Mobs is not in the test run, so spooking is checked with an ordinary monster only.
 */
@SuppressWarnings("UnstableApiUsage")
final class StableRiderScenes {
    static void run(ClientGameTestContext c, TestSingleplayerContext w, StableTestKit kit) {
        part(kit, "night watch", () -> nightWatch(c, w, kit));
        kit.pad(w);
        part(kit, "companion", () -> companion(c, w, kit));
        kit.pad(w);
        part(kit, "caravan", () -> caravan(c, w, kit));
        kit.pad(w);
        part(kit, "theft", () -> theft(c, w, kit));
        kit.pad(w);
        part(kit, "spook", () -> spook(c, w, kit));
        w.getServer().runCommand("time set 6000");
    }

    /** Runs one part; a failure is recorded (soft) and the next part still runs. */
    private static void part(StableTestKit kit, String name, StableTestKit.Body body) {
        try { body.run(); }
        catch (Throwable t) { kit.expect(false, name + ": " + (t.getMessage() == null ? t.toString() : t.getMessage())); }
    }

    // -- helpers -------------------------------------------------------------------------------------------

    private static Villager villager(ServerLevel level, Vec3 at, String job) {
        var v = new Villager(EntityTypes.VILLAGER, level);
        v.setPos(at.x, at.y, at.z);
        if (job != null) {
            v.setVillagerData(v.getVillagerData().withProfession(level.registryAccess(), VillageProfessions.key(job)));
            v.setVillagerXp(1);
        }
        level.addFreshEntity(v);
        return v;
    }
    private static Vec3 at(BlockPos pos) { return Vec3.atBottomCenterOf(pos); }
    private static Villager resident(TestSingleplayerContext w, StableTestKit kit, UUID id) { return (Villager) kit.entity(w, id); }
    private static AbstractHorse horse(TestSingleplayerContext w, StableTestKit kit, UUID id) { return (AbstractHorse) kit.entity(w, id); }
    private static boolean rides(TestSingleplayerContext w, StableTestKit kit, UUID villager) {
        return kit.onServer(w, () -> kit.entity(w, villager) instanceof Villager v && v.getVehicle() instanceof AbstractHorse);
    }
    private static StallHome stall(TestSingleplayerContext w, StableTestKit kit, UUID horse) {
        return w.getServer().computeOnServer(s -> Stables.stallOf(horse(w, kit, horse)).orElse(null));
    }
    /** A stable horse: tame, no owner, kept by the village at {@code stall}. */
    private static UUID stableHorse(StableTestKit kit, ServerLevel level, BlockPos stall, Vec3 at, String village) {
        var h = kit.horse(level, at, "destrier", null);
        Stables.stall(h, stall, village, "village");
        return h.getUUID();
    }

    // -- knights fetch a stable horse for the night watch and ride it home after ---------------------------

    private static void nightWatch(ClientGameTestContext c, TestSingleplayerContext w, StableTestKit kit) {
        BlockPos bell = kit.origin.offset(0, 0, -6), stallA = kit.origin.offset(10, 0, 8), stallB = kit.origin.offset(13, 0, 8);
        UUID[] ids = w.getServer().computeOnServer(s -> {
            var level = kit.level();
            level.setBlock(bell, Blocks.BELL.defaultBlockState(), 3);
            level.setBlock(stallA, StableBlocks.HORSE_STALL.defaultBlockState(), 3);
            level.setBlock(stallB, StableBlocks.HORSE_STALL.defaultBlockState(), 3);
            String village = VillageSettlements.mark(level, bell, "Stablebrook").id();
            UUID a = stableHorse(kit, level, stallA, at(stallA.north(2)), village), b = stableHorse(kit, level, stallB, at(stallB.north(2)), village);
            var knights = new UUID[2];
            for (int i = 0; i < 2; i++) {
                var k = villager(level, at(bell.offset(i == 0 ? 2 : -2, 0, 2)), "knight");
                k.getBrain().setMemory(MemoryModuleType.MEETING_POINT, GlobalPos.of(level.dimension(), bell));
                knights[i] = k.getUUID();
            }
            return new UUID[]{a, b, knights[0], knights[1]};
        });
        UUID horseA = ids[0], horseB = ids[1], knightA = ids[2], knightB = ids[3];
        w.getServer().runCommand("time set 14000");
        kit.until(c, () -> rides(w, kit, knightA) || rides(w, kit, knightB), 1400, "a knight on night watch mounts a stable horse");
        UUID rider = rides(w, kit, knightA) ? knightA : knightB;
        Vec3 mountedAt = w.getServer().computeOnServer(s -> resident(w, kit, rider).position());
        kit.expect(w.getServer().computeOnServer(s -> Riders.order(resident(w, kit, rider)).equals(Mounts.PATROL)), "the knight rides with the patrol order");
        kit.until(c, () -> kit.onServer(w, () -> resident(w, kit, rider).position().distanceTo(mountedAt) >= 5), 900, "the mounted knight rides the patrol 5+ blocks");
        kit.expect(rides(w, kit, rider), "the knight is still in the saddle on patrol");
        Vec3 above = w.getServer().computeOnServer(s -> resident(w, kit, rider).position().add(0, 7, -8));
        kit.view(c, w, above, 0, 35, "riders-night-watch");
        // Morning: they ride back to the stalls and get off (or get off where they are after a minute).
        w.getServer().runCommand("time set 3000");
        kit.until(c, () -> !rides(w, kit, knightA) && !rides(w, kit, knightB), 1700, "both knights are off their horses after the watch");
        kit.expect(kit.onServer(w, () -> Riders.order(resident(w, kit, knightA)).isEmpty() && Riders.order(resident(w, kit, knightB)).isEmpty()), "the patrol orders are cleared");
        // With nobody near, any horse left out drifts back beside its stall.
        w.getServer().runOnServer(s -> kit.player().teleportTo(kit.origin.getX() - 45.5, kit.origin.getY(), kit.origin.getZ() + .5));
        kit.until(c, () -> kit.onServer(w, () -> near(horse(w, kit, horseA), stallA, 8) && near(horse(w, kit, horseB), stallB, 8)), 700,
                () -> "both stable horses end up within 8 blocks of their stalls");
        kit.expect(stall(w, kit, horseA).stolenBy().isEmpty() && stall(w, kit, horseA).awaySince() == 0, "a knight's ride flags nothing");
        w.getServer().runOnServer(s -> kit.player().teleportTo(kit.origin.getX() + .5, kit.origin.getY(), kit.origin.getZ() + .5));
        w.getServer().runCommand("time set 6000");
    }
    private static boolean near(AbstractHorse horse, BlockPos stall, double blocks) { return horse != null && horse.position().distanceTo(at(stall)) <= blocks; }

    // -- a companion takes a spare horse when the player rides ---------------------------------------------

    private static void companion(ClientGameTestContext c, TestSingleplayerContext w, StableTestKit kit) {
        UUID[] ids = w.getServer().computeOnServer(s -> {
            var level = kit.level(); var p = kit.player();
            var v = villager(level, at(kit.origin.offset(3, 0, 0)), null);
            target(v).setAttached(COMPANION, new CompanionState(p.getUUID().toString(), "follow", v.getX(), v.getY(), v.getZ(), 0, false, level.getGameTime()));
            target(p).setAttached(PARTY, profile(v).id());
            var spare = kit.horse(level, at(kit.origin.offset(6, 0, 4)), "palfrey", p);
            var own = kit.horse(level, at(kit.origin.offset(-2, 0, 0)), "courser", p);
            return new UUID[]{v.getUUID(), spare.getUUID(), own.getUUID()};
        });
        UUID friend = ids[0], spare = ids[1], own = ids[2];
        c.waitTicks(10);
        w.getServer().runOnServer(s -> kit.check(kit.player().startRiding(horse(w, kit, own), true, true), "the player gets on their horse"));
        kit.until(c, () -> rides(w, kit, friend), 60, "the companion mounts the spare horse at once");
        kit.expect(kit.onServer(w, () -> resident(w, kit, friend).getVehicle() == horse(w, kit, spare)), "it is the spare horse, not someone else's");
        kit.expect(kit.onServer(w, () -> Riders.order(resident(w, kit, friend)).equals(Mounts.COMPANION)), "the companion rides with the companion order");
        kit.view(c, w, at(kit.origin.offset(2, 4, -9)), 0, 20, "riders-companion");
        w.getServer().runOnServer(s -> kit.player().stopRiding());
        kit.until(c, () -> !rides(w, kit, friend), 60, "the companion gets off when the player does");
        w.getServer().runOnServer(s -> CompanionController.returnHome(resident(w, kit, friend), kit.player(), false));
    }

    // -- a caravan guard is steered only by the caller ----------------------------------------------------

    private static void caravan(ClientGameTestContext c, TestSingleplayerContext w, StableTestKit kit) {
        w.getServer().runCommand("time set 6000");
        Vec3 goal = at(kit.origin.offset(20, 0, 2));
        UUID[] ids = w.getServer().computeOnServer(s -> {
            var level = kit.level();
            var k = villager(level, at(kit.origin.offset(0, 0, 2)), "knight");
            var h = kit.horse(level, at(kit.origin.offset(2, 0, 2)), "rouncey", null);
            return new UUID[]{k.getUUID(), h.getUUID()};
        });
        UUID guard = ids[0], mount = ids[1];
        c.waitTicks(10);
        w.getServer().runOnServer(s -> {
            var k = resident(w, kit, guard);
            kit.check(PackAnimals.mountGuard(k, horse(w, kit, mount)), "PackAnimals.mountGuard seats the knight");
            kit.check(Mounts.caravan(k) && Riders.order(k).equals(Mounts.CARAVAN), "the knight rides with the caravan order");
            k.getNavigation().moveTo(goal.x, goal.y, goal.z, 1.2);
        });
        kit.until(c, () -> kit.onServer(w, () -> horse(w, kit, mount).position().distanceTo(goal) <= 3), 500, "the caller's moveTo drives the horse 20 blocks");
        c.waitTicks(200);
        kit.expect(kit.onServer(w, () -> resident(w, kit, guard).getVehicle() == horse(w, kit, mount)), "the caravan guard is still mounted 200 ticks later");
        kit.expect(kit.onServer(w, () -> horse(w, kit, mount).position().distanceTo(goal) <= 6), "no routine walked the horse home");
        w.getServer().runOnServer(s -> PackAnimals.dismountGuard(resident(w, kit, guard)));
        kit.expect(!rides(w, kit, guard), "dismountGuard takes the guard off");
        kit.expect(kit.onServer(w, () -> Riders.order(resident(w, kit, guard)).isEmpty() && !Mounts.caravan(resident(w, kit, guard))), "and clears the caravan order");
    }

    // -- riding a village horse far away is theft; the thief bringing it back earns nothing -----------------

    private static void theft(ClientGameTestContext c, TestSingleplayerContext w, StableTestKit kit) {
        BlockPos stallPos = kit.origin.offset(6, 0, 6);
        UUID mare = w.getServer().computeOnServer(s -> {
            var level = kit.level();
            level.setBlock(stallPos, StableBlocks.HORSE_STALL.defaultBlockState(), 3);
            String village = VillageSettlements.mark(level, kit.origin, "Stablebrook").id();
            return stableHorse(kit, level, stallPos, at(stallPos.north(2)), village);
        });
        c.waitTicks(5);
        w.getServer().runOnServer(s -> kit.check(kit.player().startRiding(horse(w, kit, mare), true, true), "the player gets on a village horse"));
        // One check while still at home, so the ride counts as taking it from its stable.
        c.waitTicks(45);
        kit.stepTo(w, w.getServer().computeOnServer(s -> horse(w, kit, mare)), at(stallPos).add(60, 0, 0), 8);
        String me = w.getServer().computeOnServer(s -> kit.player().getUUID().toString());
        kit.until(c, () -> me.equals(stall(w, kit, mare).stolenBy()), 120, "riding a village horse 60 blocks out flags it stolen");
        kit.expect(deeds(w, kit, stallPos, DeedKind.STOLE_HORSE) == 1, "one Stole a Horse deed in the village's log");
        kit.stepTo(w, w.getServer().computeOnServer(s -> horse(w, kit, mare)), at(stallPos.north(2)), 8);
        kit.until(c, () -> stall(w, kit, mare).stolenBy().isEmpty(), 120, "riding it back clears the flag");
        kit.expect(deeds(w, kit, stallPos, DeedKind.RETURNED_HORSE) == 0, "the thief earns no Returned a Horse");
        w.getServer().runOnServer(s -> kit.player().stopRiding());
    }
    private static long deeds(TestSingleplayerContext w, StableTestKit kit, BlockPos stall, DeedKind kind) {
        return w.getServer().computeOnServer(s -> {
            var log = Deeds.log(Deeds.place(kit.level(), stall), kit.player().getUUID());
            return log == null ? 0L : log.deeds().stream().filter(d -> d.kind() == kind).count();
        });
    }

    // -- a cared-for horse with no bond rears at a monster; a village horse doesn't -------------------------

    private static void spook(ClientGameTestContext c, TestSingleplayerContext w, StableTestKit kit) {
        UUID[] ids = w.getServer().computeOnServer(s -> {
            var level = kit.level(); var p = kit.player();
            BlockPos mine = kit.origin.offset(-5, 0, -2), theirs = kit.origin.offset(6, 0, -2);
            level.setBlock(mine, StableBlocks.HORSE_STALL.defaultBlockState(), 3);
            level.setBlock(theirs, StableBlocks.HORSE_STALL.defaultBlockState(), 3);
            var cared = kit.horse(level, at(kit.origin.offset(-3, 0, 0)), "rouncey", p);
            Stables.stall(cared, mine, "", "player:" + p.getUUID());
            var village = kit.horse(level, at(kit.origin.offset(3, 0, 0)), "rouncey", null);
            Stables.stall(village, theirs, "", "village");
            var husk = EntityTypes.HUSK.create(level, EntitySpawnReason.COMMAND);
            kit.check(husk != null, "a husk could be created");
            husk.snapTo(kit.origin.getX() + .5, kit.origin.getY(), kit.origin.getZ() + 2.5, 0, 0);
            husk.setNoAi(true);
            level.addFreshEntity(husk);
            return new UUID[]{cared.getUUID(), village.getUUID()};
        });
        UUID cared = ids[0], village = ids[1];
        c.waitTicks(5);
        w.getServer().runOnServer(s -> kit.check(kit.player().startRiding(horse(w, kit, cared), true, true), "the player gets on their own horse"));
        kit.until(c, () -> kit.onServer(w, () -> Spook.last(horse(w, kit, cared)) >= 0), 60, "the player's unbonded horse rears at the husk");
        kit.expect(kit.onServer(w, () -> kit.player().getVehicle() == horse(w, kit, cared)), "rearing at an ordinary monster never throws the rider");
        c.waitTicks(40);
        kit.expect(kit.onServer(w, () -> Spook.last(horse(w, kit, village)) < 0), "the village's horse beside the same husk is not spooked");
        // Riderless after the cooldown, the same horse bolts from the husk instead. (A stalled horse only runs within
        // its 6-block home; freeing it here makes the run easy to see. It still counts as cared for: its stall stays.)
        w.getServer().runOnServer(s -> { kit.player().stopRiding(); horse(w, kit, cared).clearHome(); });
        long reared = w.getServer().computeOnServer(s -> Spook.last(horse(w, kit, cared)));
        // Left alone through the cooldown it may well stroll off past the 4 blocks a monster frightens it from, so it is
        // put back beside the husk (closer than it started, with room to drift a step) once the cooldown is over.
        kit.until(c, () -> kit.onServer(w, () -> kit.level().getGameTime() - reared >= SpookRule.COOLDOWN), (int) SpookRule.COOLDOWN + 40, "the spook cooldown runs out");
        Vec3 start = at(kit.origin.offset(-2, 0, 1));
        w.getServer().runOnServer(s -> { var h = horse(w, kit, cared); h.getNavigation().stop(); h.teleportTo(start.x, start.y, start.z); });
        kit.until(c, () -> kit.onServer(w, () -> Spook.last(horse(w, kit, cared)) > reared), 120, "riderless, the cared-for horse bolts after the cooldown");
        kit.until(c, () -> kit.onServer(w, () -> horse(w, kit, cared).position().distanceTo(start) > 2), 100, "the bolting horse runs off");
        kit.expect(kit.onServer(w, () -> Spook.last(horse(w, kit, village)) < 0), "the village's horse never spooked");
    }

    private StableRiderScenes() {}
}
