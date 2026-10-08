package dev.villagefriends;

import static dev.villagefriends.VillageFriends.*;

import dev.villagefriends.routine.Routine;
import dev.villagefriends.tavern.Seat;
import dev.villagefriends.tavern.Taverns;
import java.util.List;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.minecraft.client.gui.screens.worldselection.WorldCreationUiState;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.entity.ai.village.poi.PoiManager;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.level.levelgen.presets.WorldPresets;
import net.minecraft.world.phys.AABB;
import dev.villagefriends.tavern.TavernSurvey;
import net.minecraft.core.HolderSet;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.level.levelgen.structure.PoolElementStructurePiece;
import net.minecraft.world.level.levelgen.structure.StructureStart;
import net.minecraft.world.level.levelgen.structure.pools.SinglePoolElement;

/**
 * A whole generated village on a Market Day evening and at lunch: its residents walk from their homes and
 * workshops to the tavern and sit down, inside a building found through its village structure piece.
 * Screenshots are named {@code tavern-village-*}.
 */
@SuppressWarnings("UnstableApiUsage")
public final class TavernVillageGameTest implements FabricClientGameTest {
    private static final int GROUND = -61, X = 2000, Z = 2000;
    private static void check(boolean ok, String why) { if (!ok) throw new AssertionError(why); }

    private static int seatedAt(TestSingleplayerContext w, AABB area) {
        return w.getServer().computeOnServer(s -> w.getConnection().getServerLevel().getEntitiesOfClass(Villager.class, area, Seat::seated).size());
    }
    private static void view(ClientGameTestContext c, TestSingleplayerContext w, double x, double y, double z, float yaw, float pitch, String name) {
        w.getServer().runCommand(String.format(java.util.Locale.ROOT, "tp @a %.2f %.2f %.2f %.1f %.1f", x, y, z, yaw, pitch));
        c.waitTicks(60);
        c.runOnClient(client -> client.gui.toastManager().clear());
        c.takeScreenshot("tavern-village-" + name);
    }

    @Override public void runTest(ClientGameTestContext c) {
        c.getInput().resizeWindow(1280, 800);
        try (var w = c.worldBuilder().adjustSettings(ui -> {
            var flat = ui.getSettings().worldgenLoadContext().lookupOrThrow(Registries.WORLD_PRESET).getOrThrow(WorldPresets.FLAT);
            ui.setWorldType(new WorldCreationUiState.WorldTypeEntry(flat));
            ui.setGenerateStructures(false);
            ui.setSeed("23");
        }).create()) {
            for (int attempt = 0; attempt < 3; attempt++) { try { w.getConnection().waitForChunksRender(); break; } catch (AssertionError slow) { c.waitTicks(100); } }
            for (var cmd : List.of("gamerule advance_time false", "gamerule advance_weather false", "gamerule spawn_mobs false", "weather clear", "gamemode spectator @a", "difficulty peaceful"))
                w.getServer().runCommand(cmd);
            w.getServer().runCommand("time set " + (6 * 24000 + Routine.at(17, 0)));
            w.getServer().runOnServer(s -> {
                var level = w.getConnection().getServerLevel();
                for (int cx = (X - 112) >> 4; cx <= (X + 112) >> 4; cx++) for (int cz = (Z - 112) >> 4; cz <= (Z + 112) >> 4; cz++) level.getChunk(cx, cz);
            });
            w.getServer().runCommand("place structure villagefriends:village " + X + " " + (GROUND + 1) + " " + Z);
            w.getServer().runCommand("tp @a " + X + " " + (GROUND + 30) + " " + Z);
            c.waitTicks(100);
            BlockPos station = w.getServer().computeOnServer(s -> {
                var level = w.getConnection().getServerLevel();
                var poi = VillageProfessions.poiKey("tavern_keeper");
                return level.getPoiManager().findClosest(h -> h.is(poi), new BlockPos(X, GROUND, Z), 128, PoiManager.Occupancy.ANY).orElse(null);
            });
            check(station != null, "The village has a tavern");
            int residents = w.getServer().computeOnServer(s -> w.getConnection().getServerLevel()
                    .getEntitiesOfClass(Villager.class, new AABB(X - 128, GROUND - 10, Z - 128, X + 128, GROUND + 40, Z + 128)).size());
            LOGGER.info("TAVERN VILLAGE: {} residents, tavern station at {}", residents, station);
            // Market Day evening.
            w.getServer().runCommand("time set " + (6 * 24000 + Routine.at(18, 40)));
            AABB[] area = new AABB[1]; int best = 0;
            for (int i = 0; i < 120; i++) {
                c.waitTicks(20);
                if (area[0] == null) w.getServer().runOnServer(s -> {
                    var tavern = Taverns.tavernAt(w.getConnection().getServerLevel(), station);
                    if (tavern != null) { var b = tavern.box(); area[0] = new AABB(b.minX(), b.minY(), b.minZ(), b.maxX() + 1, b.maxY() + 1, b.maxZ() + 1).inflate(1); }
                });
                if (area[0] == null) continue;
                int n = seatedAt(w, area[0]);
                best = Math.max(best, n);
                if (n >= 8) break;
            }
            check(area[0] != null, "Residents found their way to the tavern");
            var box = area[0];
            boolean structural = box.getXsize() <= 19 && box.getZsize() <= 33;
            LOGGER.info("TAVERN VILLAGE EVENING: {} seated at most; tavern box {} (from the village piece: {})", best, box, structural);
            check(best >= 4, "A village's residents fill the tavern on Market Day evening: " + best);
            c.runOnClient(client -> { if (!client.gui.hud.isHidden()) client.gui.hud.toggle(); });
            // Aim at the seated crowd from a little way off, above their heads.
            double[] crowd = w.getServer().computeOnServer(s -> {
                double x = 0, z = 0, y = 0; int n = 0;
                for (var v : w.getConnection().getServerLevel().getEntitiesOfClass(Villager.class, box, Seat::seated)) { x += v.getX(); y += v.getY(); z += v.getZ(); n++; }
                return n == 0 ? new double[]{box.getCenter().x, station.getY(), box.getCenter().z} : new double[]{x / n, y / n, z / n};
            });
            for (int i = 0; i < 3; i++) {
                double angle = Math.toRadians(45 + i * 120), ex = crowd[0] + Math.sin(angle) * 3.2, ez = crowd[2] + Math.cos(angle) * 3.2;
                float look = (float) Math.toDegrees(Math.atan2(-(crowd[0] - ex), crowd[2] - ez));
                view(c, w, ex, crowd[1] + 2.4, ez, look, 30, "evening-" + i);
            }
            view(c, w, box.getCenter().x, station.getY() + 30, box.getCenter().z - 24, 0, 50, "evening-outside");
            c.runOnClient(client -> { if (client.gui.hud.isHidden()) client.gui.hud.toggle(); });
            LOGGER.info("TAVERN VILLAGE EVENING PASSED: {} residents seated at the tavern of a placed village on Market Day evening.", best);
        }
        // A naturally generated village (placed villages record no structure start): its tavern is read from its own structure piece.
        try (var w = c.worldBuilder().adjustSettings(ui -> {
            var normal = ui.getSettings().worldgenLoadContext().lookupOrThrow(Registries.WORLD_PRESET).getOrThrow(WorldPresets.NORMAL);
            ui.setWorldType(new WorldCreationUiState.WorldTypeEntry(normal));
            ui.setGenerateStructures(true);
            ui.setSeed("1");
        }).create()) {
            w.getConnection().waitForChunksDownload();
            w.getServer().runCommand("gamemode spectator @a");
            BlockPos hearthStation = w.getServer().computeOnServer(server -> {
                var level = w.getConnection().getServerLevel();
                var holder = level.registryAccess().lookupOrThrow(Registries.STRUCTURE).getOrThrow(ResourceKey.create(Registries.STRUCTURE, VillageBlocks.id("village")));
                var located = level.getChunkSource().getGenerator().findNearestMapStructure(level, HolderSet.direct(holder), BlockPos.ZERO, 80, false);
                check(located != null, "A normal world has a village");
                var entrance = located.getFirst(); level.getChunkAt(entrance);
                StructureStart start = StructureStart.INVALID_START;
                for (int y = 32; y < 256 && !start.isValid(); y += 4) start = level.structureManager().getStructureAt(new BlockPos(entrance.getX(), y, entrance.getZ()), holder.value());
                check(start.isValid(), "The village has a structure start");
                PoolElementStructurePiece hearth = null;
                for (var piece : start.getPieces())
                    if (piece instanceof PoolElementStructurePiece pool && pool.getElement() instanceof SinglePoolElement single && single.getTemplateLocation().getPath().contains("tavern")) hearth = pool;
                check(hearth != null, "The village has a tavern piece");
                var box = hearth.getBoundingBox();
                for (int x = box.minX() >> 4; x <= box.maxX() >> 4; x++) for (int z = box.minZ() >> 4; z <= box.maxZ() >> 4; z++) level.getChunk(x, z);
                BlockPos station = null;
                for (var pos : BlockPos.betweenClosed(box.minX(), box.minY(), box.minZ(), box.maxX(), box.maxY(), box.maxZ()))
                    if (level.getBlockState(pos).is(VillageBlocks.get("tap_stand"))) { station = pos.immutable(); break; }
                check(station != null, "The Hearth has its tap stand");
                var tavern = TavernSurvey.survey(level, station);
                check(tavern.box().equals(box), "The survey reads the tavern's own structure piece: " + tavern.box() + " vs " + box);
                return station;
            });
            // Freshly generated chunks register their points of interest over the next few ticks; look again, as the tavern does every minute.
            c.waitTicks(100);
            String found = w.getServer().computeOnServer(server -> {
                var level = w.getConnection().getServerLevel();
                var tavern = TavernSurvey.survey(level, hearthStation);
                check(tavern.seats().size() >= 30 && tavern.stations().size() >= 2 && tavern.stage() != null && !tavern.stoves().isEmpty(),
                        "and finds its seats, stations, stage and stove: " + tavern.seats().size() + " seats, " + tavern.stations().size() + " stations");
                return tavern.seats().size() + " seats (" + tavern.seats().stream().filter(x -> x.hearth()).count() + " by the hearth, "
                        + tavern.seats().stream().filter(x -> x.outdoor()).count() + " outdoors), " + tavern.standing().size() + " standing, " + tavern.stations().size() + " stations, box " + tavern.box();
            });
            LOGGER.info("TAVERN VILLAGE PASSED: natural village tavern {}", found);
        }
    }
}
