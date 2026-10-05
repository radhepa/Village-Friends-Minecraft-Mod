package dev.villagefriends;

import java.util.ArrayList;
import java.util.List;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.minecraft.client.gui.screens.worldselection.WorldCreationUiState;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.level.block.Mirror;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.levelgen.presets.WorldPresets;
import net.minecraft.world.level.levelgen.structure.templatesystem.JigsawReplacementProcessor;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructurePlaceSettings;

/**
 * Development gallery for village art direction; not part of the regression suite.
 *
 * <p>Run {@code gradlew runClientGameTest -PvillageGallery} (optionally
 * {@code -Pgallery=tavern,cottage_oak} and {@code -PgalleryVillages=3}). It places
 * templates on a superflat world and generates whole villages with
 * {@code /place structure}, then saves screenshots under
 * {@code build/run/clientGameTest/screenshots}.
 */
@SuppressWarnings("UnstableApiUsage")
public final class VillageGalleryGameTest implements FabricClientGameTest {
    private static final int GROUND = -61;

    private static void view(ClientGameTestContext c, net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext w,
                             double x, double y, double z, float yaw, float pitch, String name) {
        w.getServer().runCommand(String.format(java.util.Locale.ROOT, "tp @a %.1f %.1f %.1f %.1f %.1f", x, y, z, yaw, pitch));
        // Software rendering rarely satisfies the strict all-chunks predicate quickly; a fixed wait suffices.
        c.waitTicks(Integer.getInteger("villagefriends.galleryWait", 160));
        c.runOnClient(client -> client.gui.toastManager().clear());
        c.takeScreenshot("gallery-" + name);
    }

    private static void settle(ClientGameTestContext c, net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext w) {
        // Software rendering can be slower than the API's default wait; a late chunk only softens a screenshot.
        for (int attempt = 0; attempt < 3; attempt++) {
            try { w.getConnection().waitForChunksRender(); return; }
            catch (AssertionError slow) { c.waitTicks(100); }
        }
    }

    @Override
    public void runTest(ClientGameTestContext c) {
        String list = System.getProperty("villagefriends.gallery", "");
        int villages = Integer.getInteger("villagefriends.galleryVillages", 2);
        List<String> templates = new ArrayList<>();
        for (String name : list.split(",")) if (!name.isBlank()) templates.add(name.trim());
        c.getInput().resizeWindow(1280, 800);
        c.runOnClient(client -> {
            client.options.guiScale().set(2);
            if (!client.gui.hud.isHidden()) client.gui.hud.toggle();
            client.resizeGui();
        });
        try (var w = c.worldBuilder().adjustSettings(ui -> {
            var flat = ui.getSettings().worldgenLoadContext().lookupOrThrow(Registries.WORLD_PRESET).getOrThrow(WorldPresets.FLAT);
            ui.setWorldType(new WorldCreationUiState.WorldTypeEntry(flat));
            ui.setGenerateStructures(false);
            ui.setSeed("7");
        }).create()) {
            settle(c, w);
            c.runOnClient(client -> { client.options.renderDistance().set(9); client.options.broadcastOptions(); });
            w.getServer().runCommand("gamemode spectator @a");
            w.getServer().runCommand("weather clear");
            w.getServer().runCommand("time set 5000");
            w.getServer().runOnServer(server -> server.getPlayerList().setViewDistance(9));
            int x = 0;
            List<int[]> spots = new ArrayList<>();
            for (String name : templates) {
                int origin = x;
                w.getServer().runOnServer(server -> {
                    var level = server.overworld();
                    var id = VillageBlocks.id("village/" + name);
                    var template = level.getStructureTemplateManager().get(id).orElseThrow(() -> new AssertionError("Missing template " + id));
                    var pos = new BlockPos(origin, GROUND, 0);
                    for (int cx = (origin - 16) >> 4; cx <= (origin + 48) >> 4; cx++)
                        for (int cz = -2; cz <= 3; cz++) level.getChunk(cx, cz);
                    template.placeInWorld(level, pos, pos, new StructurePlaceSettings().setRotation(Rotation.NONE).setMirror(Mirror.NONE)
                            .setIgnoreEntities(true).setKnownShape(true).addProcessor(JigsawReplacementProcessor.INSTANCE), level.getRandom(), 18);
                });
                int[] size = w.getServer().computeOnServer(server -> {
                    var t = server.overworld().getStructureTemplateManager().get(VillageBlocks.id("village/" + name)).orElseThrow();
                    return new int[]{t.getSize().getX(), t.getSize().getY(), t.getSize().getZ()};
                });
                spots.add(new int[]{origin, size[0], size[1], size[2]});
                x += Math.max(size[0], size[2]) + 24;
            }
            for (int i = 0; i < templates.size(); i++) {
                int[] s = spots.get(i);
                double cx = s[0] + s[1] / 2.0, cz = s[3] / 2.0;
                double d = Math.max(s[1], s[3]) * 0.9 + 8;
                // Street view from the north-west (the template's front faces north).
                view(c, w, cx - d * 0.55, GROUND + 3 + s[2] * 0.45, cz - d * 0.85, -33f, 18f, templates.get(i) + "-front");
                view(c, w, cx + d * 0.7, GROUND + 4 + s[2] * 0.6, cz + d * 0.8, 139f, 24f, templates.get(i) + "-back");
            }
            for (int v = 0; v < villages; v++) {
                int vx = 2000 + v * 600, vz = 2000;
                w.getServer().runOnServer(server -> {
                    var level = server.overworld();
                    for (int cx = (vx - 128) >> 4; cx <= (vx + 128) >> 4; cx++)
                        for (int cz = (vz - 128) >> 4; cz <= (vz + 128) >> 4; cz++) level.getChunk(cx, cz);
                });
                w.getServer().runCommand("place structure villagefriends:village " + vx + " " + (GROUND + 1) + " " + vz);
                view(c, w, vx - 72, GROUND + 58, vz - 72, -45f, 32f, "village" + v + "-aerial");
                view(c, w, vx - 21, GROUND + 15, vz - 21, -45f, 22f, "village" + v + "-square");
                view(c, w, vx + 72, GROUND + 58, vz + 72, 135f, 32f, "village" + v + "-aerial2");
                view(c, w, vx + 0.5, GROUND + 170, vz + 0.5, 0f, 89.5f, "village" + v + "-map");
            }
        }
        VillageFriends.LOGGER.info("VILLAGE GALLERY CAPTURED: {} templates, {} villages.", templates.size(), villages);
    }
}
