package dev.villagefriends;

import com.google.gson.GsonBuilder;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.minecraft.client.gui.screens.worldselection.WorldCreationUiState;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.StructureTags;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.level.block.DoorBlock;
import net.minecraft.world.level.block.LeavesBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.chunk.status.ChunkStatus;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.presets.WorldPresets;
import net.minecraft.world.level.levelgen.structure.BoundingBox;
import net.minecraft.world.level.levelgen.structure.PoolElementStructurePiece;
import net.minecraft.world.level.levelgen.structure.Structure;
import net.minecraft.world.level.levelgen.structure.StructureStart;
import net.minecraft.world.level.levelgen.structure.placement.RandomSpreadStructurePlacement;
import net.minecraft.world.level.levelgen.structure.pools.SinglePoolElement;
import net.minecraft.world.level.levelgen.structure.pools.StructureTemplatePool;
import net.minecraft.world.level.material.Fluids;
import net.minecraft.world.phys.AABB;

/**
 * Development survey of naturally generated villages; not part of the regression suite.
 *
 * <p>Run {@code gradlew runClientGameTest -Ptests=VillageSurveyGameTest} with optional
 * {@code -PsurveySeed=1 -PsurveyCount=4 -PsurveyTypes=village,village_desert -PsurveyShots=false}.
 * It creates a normal world, finds villages through the real structure placement, generates
 * them, measures terrain problems (floating or buried buildings, roads over gaps or on
 * buildings, wild trees inside lots, blocked doors) and writes
 * {@code build/run/clientGameTest/survey/<seed>.json} plus aerial screenshots.
 */
@SuppressWarnings("UnstableApiUsage")
public final class VillageSurveyGameTest implements FabricClientGameTest {
    private static final Set<String> ROAD = Set.of("dirt_path", "gravel", "cobblestone", "mossy_cobblestone", "andesite",
        "coarse_dirt", "spruce_planks", "oak_planks", "acacia_planks", "dark_oak_planks", "smooth_sandstone", "sandstone",
        "cut_sandstone", "packed_ice", "snow_block", "packed_mud", "mud_bricks", "red_sand", "terracotta", "stone_bricks",
        "polished_andesite", "podzol", "rooted_dirt", "smooth_red_sandstone", "red_sandstone", "orange_terracotta",
        "brown_terracotta", "white_terracotta", "polished_granite", "granite", "tuff", "calcite", "cobbled_deepslate");

    private record Found(String type, StructureStart start) {}

    private static String path(BlockState s) { return BuiltInRegistries.BLOCK.getKey(s.getBlock()).getPath(); }

    private static boolean passable(ServerLevel level, BlockPos p) {
        var s = level.getBlockState(p);
        return !(s.getBlock() instanceof DoorBlock) && (s.isAir() || s.getCollisionShape(level, p).isEmpty());
    }

    private static boolean hollow(BlockState s) { return s.isAir() || !s.getFluidState().isEmpty() && s.getFluidState().is(Fluids.WATER); }

    private static boolean inside2d(BoundingBox b, int x, int z) {
        return x >= b.minX() && x <= b.maxX() && z >= b.minZ() && z <= b.maxZ();
    }

    private static JsonObject measure(ServerLevel level, Found found) {
        var start = found.start();
        var pieces = start.getPieces().stream().filter(p -> p instanceof PoolElementStructurePiece).map(p -> (PoolElementStructurePiece) p).toList();
        var rigidBoxes = new ArrayList<BoundingBox>();
        for (var p : pieces) if (p.getElement().getProjection() == StructureTemplatePool.Projection.RIGID) rigidBoxes.add(p.getBoundingBox());
        var all = pieces.stream().map(PoolElementStructurePiece::getBoundingBox).toList();
        int floating = 0, maxGap = 0, walls = 0, cliffs = 0, worstEdge = 0, blockedDoors = 0, leaves = 0, water = 0;
        int roadCells = 0, roadGaps = 0, roadSteps = 0, roadOnBuildings = 0, lowY = Integer.MAX_VALUE, highY = Integer.MIN_VALUE;
        var issues = new JsonArray();
        for (var piece : pieces) {
            var box = piece.getBoundingBox();
            String template = piece.getElement() instanceof SinglePoolElement single ? single.getTemplateLocation().getPath().replace("village/", "") : piece.getElement().toString();
            int pieceLeaves = 0;
            for (var p : BlockPos.betweenClosed(box.minX(), box.minY(), box.minZ(), box.maxX(), box.maxY(), box.maxZ())) {
                var s = level.getBlockState(p);
                if (s.getBlock() instanceof LeavesBlock && s.hasProperty(LeavesBlock.PERSISTENT) && !s.getValue(LeavesBlock.PERSISTENT)) pieceLeaves++;
            }
            leaves += pieceLeaves;
            if (piece.getElement().getProjection() == StructureTemplatePool.Projection.RIGID) {
                int y0 = box.minY(); lowY = Math.min(lowY, y0); highY = Math.max(highY, y0);
                int pieceFloat = 0, pieceGap = 0, pieceWalls = 0, pieceCliffs = 0, pieceEdge = 0, pieceDoors = 0, pieceWater = 0;
                for (int x = box.minX(); x <= box.maxX(); x++) for (int z = box.minZ(); z <= box.maxZ(); z++) {
                    var ground = level.getBlockState(new BlockPos(x, y0, z));
                    if (ground.isAir() || !ground.getFluidState().isEmpty()) continue;
                    int gap = 0;
                    while (gap < 24 && hollow(level.getBlockState(new BlockPos(x, y0 - 1 - gap, z)))) gap++;
                    if (gap > 0) { pieceFloat++; pieceGap = Math.max(pieceGap, gap); }
                }
                for (var p : BlockPos.betweenClosed(box.minX(), y0 + 1, box.minZ(), box.maxX(), box.maxY(), box.maxZ())) {
                    var s = level.getBlockState(p);
                    if (s.getFluidState().is(Fluids.WATER) || s.getFluidState().is(Fluids.FLOWING_WATER)) pieceWater++;
                    if (s.getBlock() instanceof DoorBlock && s.getValue(DoorBlock.HALF) == net.minecraft.world.level.block.state.properties.DoubleBlockHalf.LOWER) {
                        var facing = s.getValue(DoorBlock.FACING);
                        boolean ok = true;
                        for (var side : List.of(facing, facing.getOpposite())) for (int h = 0; h < 2; h++) ok &= passable(level, p.relative(side).above(h));
                        if (!ok) pieceDoors++;
                    }
                }
                for (int x = box.minX() - 2; x <= box.maxX() + 2; x++) for (int z = box.minZ() - 2; z <= box.maxZ() + 2; z++) {
                    if (inside2d(box, x, z)) continue;
                    int fx = x, fz = z;
                    if (all.stream().anyMatch(b -> inside2d(b, fx, fz))) continue;
                    int top = level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, x, z) - 1;
                    int diff = top - y0;
                    if (diff >= 3) pieceWalls++;
                    if (diff <= -3) pieceCliffs++;
                    pieceEdge = Math.max(pieceEdge, Math.abs(diff));
                }
                floating += pieceFloat; maxGap = Math.max(maxGap, pieceGap); walls += pieceWalls; cliffs += pieceCliffs;
                worstEdge = Math.max(worstEdge, pieceEdge); blockedDoors += pieceDoors; water += pieceWater;
                if (pieceFloat > 2 || pieceWalls > 4 || pieceCliffs > 4 || pieceDoors > 0 || pieceLeaves > 0) {
                    var issue = new JsonObject();
                    issue.addProperty("template", template); issue.addProperty("pos", box.minX() + " " + y0 + " " + box.minZ());
                    issue.addProperty("float", pieceFloat); issue.addProperty("gap", pieceGap); issue.addProperty("walls", pieceWalls);
                    issue.addProperty("cliffs", pieceCliffs); issue.addProperty("edge", pieceEdge); issue.addProperty("doors", pieceDoors);
                    issue.addProperty("leaves", pieceLeaves); issue.addProperty("water", pieceWater);
                    issues.add(issue);
                }
            } else {
                var tops = new HashMap<Long, Integer>();
                int pieceGaps = 0, pieceSteps = 0, pieceOn = 0;
                for (int x = box.minX(); x <= box.maxX(); x++) for (int z = box.minZ(); z <= box.maxZ(); z++) {
                    int top = level.getHeight(Heightmap.Types.WORLD_SURFACE, x, z) - 1;
                    var s = level.getBlockState(new BlockPos(x, top, z));
                    if (!ROAD.contains(path(s))) continue;
                    roadCells++;
                    tops.put(BlockPos.asLong(x, 0, z), top);
                    if (level.getBlockState(new BlockPos(x, top - 1, z)).isAir()) pieceGaps++;
                    for (var r : rigidBoxes) if (inside2d(r, x, z) && top > r.minY() + 1) { pieceOn++; break; }
                }
                for (var e : tops.entrySet()) {
                    var p = BlockPos.of(e.getKey());
                    for (var d : List.of(Direction.EAST, Direction.SOUTH)) {
                        var n = tops.get(BlockPos.asLong(p.getX() + d.getStepX(), 0, p.getZ() + d.getStepZ()));
                        if (n != null && Math.abs(n - e.getValue()) >= 2) pieceSteps++;
                    }
                }
                roadGaps += pieceGaps; roadSteps += pieceSteps; roadOnBuildings += pieceOn;
                if (pieceGaps > 0 || pieceSteps > 1 || pieceOn > 0) {
                    var issue = new JsonObject();
                    issue.addProperty("template", template); issue.addProperty("pos", box.minX() + " " + box.minY() + " " + box.minZ());
                    issue.addProperty("roadGaps", pieceGaps); issue.addProperty("roadSteps", pieceSteps); issue.addProperty("roadOnBuildings", pieceOn);
                    issues.add(issue);
                }
            }
        }
        var bounds = start.getBoundingBox();
        var center = bounds.getCenter();
        var out = new JsonObject();
        out.addProperty("type", found.type());
        out.addProperty("center", center.getX() + " " + center.getY() + " " + center.getZ());
        out.addProperty("biome", level.getBiome(center).unwrapKey().map(k -> k.identifier().getPath()).orElse("?"));
        out.addProperty("pieces", pieces.size());
        out.addProperty("rigid", rigidBoxes.size());
        out.addProperty("span", bounds.getXSpan() + "x" + bounds.getZSpan());
        out.addProperty("groundRange", highY - lowY);
        out.addProperty("residents", level.getEntitiesOfClass(Villager.class, AABB.of(bounds).inflate(4)).size());
        out.addProperty("floatingColumns", floating); out.addProperty("maxGap", maxGap);
        out.addProperty("wallColumns", walls); out.addProperty("cliffColumns", cliffs); out.addProperty("worstEdge", worstEdge);
        out.addProperty("blockedDoors", blockedDoors); out.addProperty("wildLeaves", leaves); out.addProperty("waterInBuildings", water);
        out.addProperty("roadCells", roadCells); out.addProperty("roadGaps", roadGaps); out.addProperty("roadSteps", roadSteps);
        out.addProperty("roadOnBuildings", roadOnBuildings);
        out.add("issues", issues);
        return out;
    }

    private static void shot(ClientGameTestContext c, TestSingleplayerContext w, double x, double y, double z, float yaw, float pitch, String name) {
        w.getServer().runCommand(String.format(Locale.ROOT, "tp @a %.1f %.1f %.1f %.1f %.1f", x, y, z, yaw, pitch));
        c.waitTicks(Integer.getInteger("villagefriends.galleryWait", 160));
        c.runOnClient(client -> client.gui.toastManager().clear());
        c.takeScreenshot(name);
    }

    @Override
    public void runTest(ClientGameTestContext c) {
        String seed = System.getProperty("villagefriends.surveySeed", "1");
        int count = Integer.getInteger("villagefriends.surveyCount", 4);
        boolean shots = !"false".equals(System.getProperty("villagefriends.surveyShots", "true"));
        var wanted = new HashSet<String>();
        for (String t : System.getProperty("villagefriends.surveyTypes", "").split(",")) if (!t.isBlank()) wanted.add(t.trim());
        c.getInput().resizeWindow(1280, 800);
        c.runOnClient(client -> {
            client.options.guiScale().set(2);
            if (!client.gui.hud.isHidden()) client.gui.hud.toggle();
            client.resizeGui();
        });
        try (var w = c.worldBuilder().adjustSettings(ui -> {
            var normal = ui.getSettings().worldgenLoadContext().lookupOrThrow(Registries.WORLD_PRESET).getOrThrow(WorldPresets.NORMAL);
            ui.setWorldType(new WorldCreationUiState.WorldTypeEntry(normal));
            ui.setGenerateStructures(true);
            ui.setSeed(seed);
        }).create()) {
            w.getServer().runCommand("gamemode spectator @a");
            w.getServer().runCommand("time set 5000");
            w.getServer().runCommand("gamerule advance_time false");
            w.getServer().runCommand("weather clear");
            c.runOnClient(client -> { client.options.renderDistance().set(10); client.options.broadcastOptions(); });
            List<Found> found = w.getServer().computeOnServer(server -> {
                server.getPlayerList().setViewDistance(10);
                var level = server.overworld();
                var registry = level.registryAccess().lookupOrThrow(Registries.STRUCTURE);
                var ours = new HashMap<Structure, String>();
                for (var holder : registry.getOrThrow(StructureTags.VILLAGE)) {
                    var key = holder.unwrapKey().orElseThrow().identifier();
                    if (key.getNamespace().equals("villagefriends") && (wanted.isEmpty() || wanted.contains(key.getPath()))) ours.put(holder.value(), key.getPath());
                }
                var state = level.getChunkSource().getGeneratorState();
                var placements = new LinkedHashSet<RandomSpreadStructurePlacement>();
                for (var holder : registry.getOrThrow(StructureTags.VILLAGE))
                    if (ours.containsKey(holder.value()))
                        for (var p : state.getPlacementsForStructure(holder)) if (p instanceof RandomSpreadStructurePlacement r) placements.add(r);
                var counts = new HashMap<String, Integer>();
                var result = new ArrayList<Found>();
                for (var placement : placements) {
                    int spacing = placement.spacing();
                    var regions = new ArrayList<int[]>();
                    for (int rx = -9; rx <= 9; rx++) for (int rz = -9; rz <= 9; rz++) regions.add(new int[]{rx, rz});
                    regions.sort(Comparator.comparingInt(r -> r[0] * r[0] + r[1] * r[1]));
                    for (var r : regions) {
                        if (ours.values().stream().allMatch(t -> counts.getOrDefault(t, 0) >= count)) break;
                        var chunkPos = placement.getPotentialStructureChunk(state.getLevelSeed(), r[0] * spacing, r[1] * spacing);
                        var chunk = level.getChunk(chunkPos.x(), chunkPos.z(), ChunkStatus.STRUCTURE_STARTS, true);
                        for (var e : chunk.getAllStarts().entrySet()) {
                            String type = ours.get(e.getKey());
                            if (type == null || !e.getValue().isValid() || counts.getOrDefault(type, 0) >= count) continue;
                            counts.merge(type, 1, Integer::sum);
                            result.add(new Found(type, e.getValue()));
                        }
                    }
                }
                VillageFriends.LOGGER.info("SURVEY found {} villages: {}; site verdicts {}", result.size(), counts, new java.util.TreeMap<>(VillageStructure.VERDICTS));
                return result;
            });
            var report = new JsonArray();
            int index = 0;
            for (var f : found) {
                int i = index++;
                var bounds = f.start().getBoundingBox();
                JsonObject row = w.getServer().computeOnServer(server -> {
                    var level = server.overworld();
                    for (int cx = (bounds.minX() >> 4) - 1; cx <= (bounds.maxX() >> 4) + 1; cx++)
                        for (int cz = (bounds.minZ() >> 4) - 1; cz <= (bounds.maxZ() >> 4) + 1; cz++) level.getChunk(cx, cz);
                    return measure(level, f);
                });
                row.addProperty("index", i);
                report.add(row);
                VillageFriends.LOGGER.info("SURVEY {} #{} {}", f.type(), i, row);
                if (shots) {
                    var center = bounds.getCenter();
                    int top = bounds.maxY() + 34;
                    shot(c, w, center.getX() - 78, top, center.getZ() - 78, -45f, 33f, "survey-" + f.type() + "-" + i + "-nw");
                    shot(c, w, center.getX() + 78, top, center.getZ() + 78, 135f, 33f, "survey-" + f.type() + "-" + i + "-se");
                }
            }
            try {
                var dir = Path.of("survey");
                Files.createDirectories(dir);
                Files.writeString(dir.resolve(seed + ".json"), new GsonBuilder().setPrettyPrinting().create().toJson(report), StandardCharsets.UTF_8);
            } catch (IOException e) { throw new AssertionError(e); }
        }
        VillageFriends.LOGGER.info("VILLAGE SURVEY DONE for seed {}.", seed);
    }
}
