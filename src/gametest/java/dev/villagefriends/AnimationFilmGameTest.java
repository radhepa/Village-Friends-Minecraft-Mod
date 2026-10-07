package dev.villagefriends;

import static dev.villagefriends.VillageFriends.*;
import dev.villagefriends.animation.AnimationClip;
import dev.villagefriends.animation.AnimationLibrary;
import dev.villagefriends.client.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.*;
import net.fabricmc.fabric.api.client.gametest.v1.screenshot.TestScreenshotOptions;
import net.fabricmc.loader.api.FabricLoader;
import net.minecraft.client.gui.screens.worldselection.WorldCreationUiState;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.Mirror;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.levelgen.presets.WorldPresets;
import net.minecraft.world.level.levelgen.structure.templatesystem.JigsawReplacementProcessor;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructurePlaceSettings;
import net.minecraft.world.phys.EntityHitResult;
import net.minecraft.world.phys.Vec3;

/**
 * Development film of the Village Life animation pack; not part of the regression suite.
 * {@code gradlew runClientGameTest -PanimationVideo [-PfilmScenes=gallery,village]} writes numbered
 * 30 fps frames to {@code build/run/clientGameTest/film/}; {@code python tools/animations/film.py}
 * adds titles and encodes the MP4. Gallery frames sample clips at exact times; village frames step a
 * frozen world one tick at a time and render between ticks, so the motion is smooth and repeatable.
 */
@SuppressWarnings("UnstableApiUsage")
public final class AnimationFilmGameTest implements FabricClientGameTest {
    private static final int GROUND = -61, FPS = 30;
    private ClientGameTestContext c;
    private Path frames;
    private int frame, stepped;
    private String scene = "";

    private void shot(float delta) {
        c.takeScreenshot(TestScreenshotOptions.of(String.format(Locale.ROOT, "%s_%05d", scene, frame++)).disableCounterPrefix()
                .withDeltaTicks(delta).withDestinationDir(frames));
    }

    @Override public void runTest(ClientGameTestContext context) {
        c = context;
        frames = FabricLoader.getInstance().getGameDir().resolve("film");
        try { Files.createDirectories(frames); } catch (java.io.IOException e) { throw new RuntimeException(e); }
        var wanted = new HashSet<>(Arrays.asList(System.getProperty("villagefriends.filmScenes", "").split(",")));
        wanted.remove("");
        boolean all = wanted.isEmpty();
        c.getInput().resizeWindow(1280, 720);
        c.runOnClient(client -> { client.options.guiScale().set(2); client.resizeGui(); });
        try (var w = c.worldBuilder().adjustSettings(ui -> {
            var flat = ui.getSettings().worldgenLoadContext().lookupOrThrow(Registries.WORLD_PRESET).getOrThrow(WorldPresets.FLAT);
            ui.setWorldType(new WorldCreationUiState.WorldTypeEntry(flat));
            ui.setGenerateStructures(false);
            ui.setSeed("26");
        }).create()) {
            settle(w);
            w.getServer().runCommand("gamerule advance_time false");
            w.getServer().runCommand("gamerule advance_weather false");
            w.getServer().runCommand("gamerule spawn_mobs false");
            w.getServer().runCommand("weather clear");
            w.getServer().runCommand("time set 1500");
            if (all || wanted.contains("gallery")) gallery(w);
            if (all || wanted.contains("scout")) scout(w);
            if (all || wanted.contains("village")) village(w);
        }
        LOGGER.info("ANIMATION FILM CAPTURED: {} frames in {}", frame, frames);
    }

    private void settle(TestSingleplayerContext w) {
        for (int attempt = 0; attempt < 3; attempt++) {
            try { w.getConnection().waitForChunksRender(); return; } catch (AssertionError slow) { c.waitTicks(100); }
        }
    }

    // -- gallery: labeled pages of residents, each looping one clip -------------------------------

    private static final String[][] PAGES = {
        {"Everyday life", "look_around", "stretch_up", "yawn", "scratch_head", "arms_crossed", "hum_a_tune",
                "kick_pebble", "sneeze", "side_stretch", "dust_off", "rock_on_heels", "pat_pockets"},
        {"A hobby for every personality", "knead_dough", "read_a_book", "conduct_a_tune", "scout_the_horizon", "inspect_a_trinket",
                "tend_the_soil", "cast_a_line", "frame_the_view", "whittle", "stargaze", "sand_a_plank", "smell_a_flower"},
        {"Work for every profession", "hammer_and_anvil", "hoe_the_rows", "write_notes", "pray", "chop_vegetables", "stir_the_pot",
                "pour_a_drink", "stitch_cloth", "sight_an_arrow", "stand_guard", "sword_drill", "practice_the_draw"},
        {"Greetings, conversation and feelings", "wave_hello", "bow_politely", "salute", "talk_both_hands", "talk_think", "belly_laugh",
                "cheer", "hug_the_gift", "bashful_thanks", "shake_head", "huff", "flinch"},
        {"Children at play, rain and cold", "hop_in_place", "twirl", "play_airplane", "peekaboo", "watch_a_bug", "wave_excitedly",
                "hunch_in_the_rain", "catch_raindrops", "shake_off_rain", "shiver", "chase_tag", "silly_dance"},
    };
    private static final float PAGE_SECONDS = 8.5F;

    private void gallery(TestSingleplayerContext w) {
        scene = "gallery"; frame = 0;
        var random = new Random(77);
        var casts = new ArrayList<List<UUID>>();
        w.getServer().runOnServer(s -> {
            var p = w.getConnection().getServerPlayer();
            for (int page = 0; page < PAGES.length; page++) {
                var ids = new ArrayList<UUID>();
                for (int i = 1; i < PAGES[page].length; i++) {
                    var clip = AnimationLibrary.current().clip("village_life:" + PAGES[page][i]);
                    if (clip == null) throw new AssertionError("Missing clip " + PAGES[page][i]);
                    var role = AnimationCast.role(clip, page * 12 + i);
                    var id = AnimationCast.identity(random, role.personality());
                    ids.add(id);
                    AnimationCast.spawn(s.overworld(), id, role, p.getX() - 10 + i * 1.6, p.getY(), p.getZ() - 12 - page * 2, 0, false);
                }
                casts.add(ids);
            }
        });
        w.getConnection().waitForClientboundEntityUpdates(EntityTypes.VILLAGER);
        c.waitTicks(10);
        for (int page = 0; page < PAGES.length; page++) {
            var ids = casts.get(page);
            var entities = w.getServer().computeOnServer(s -> ids.stream().map(id -> s.overworld().getEntity(id).getId()).toList());
            String[] spec = PAGES[page];
            c.runOnClient(client -> {
                var cells = new ArrayList<AnimationShowcaseScreen.Cell>();
                for (int i = 1; i < spec.length; i++) {
                    var clip = AnimationLibrary.current().clip("village_life:" + spec[i]);
                    var v = (Villager) client.level.getEntity(entities.get(i - 1));
                    cells.add(new AnimationShowcaseScreen.Cell(v, clip, false, caption(clip, v)));
                }
                client.gui.setScreen(new AnimationShowcaseScreen("VILLAGE LIFE  -  ANIMATION PACK 1", spec[0], cells, 6));
            });
            c.waitForScreen(AnimationShowcaseScreen.class);
            c.waitTicks(3);
            for (int f = 0; f < PAGE_SECONDS * FPS; f++) {
                float seconds = f / (float) FPS;
                c.runOnClient(client -> ((AnimationShowcaseScreen) client.gui.screen()).seconds = seconds);
                shot(1);
            }
        }
        c.runOnClient(client -> client.gui.setScreen(null));
    }
    private static String caption(AnimationClip clip, Villager v) {
        if (v.isBaby()) return "Child";
        for (var group : clip.require()) for (String tag : new TreeSet<>(group)) {
            if (tag.startsWith("personality:")) return VillageProfessions.label(tag.substring(12));
        }
        String job = VillageFriends.profession(v);
        return job.equals("none") ? "Neighbor" : VillageProfessions.label(job);
    }

    // -- scouting: where the village set is and how it looks ----------------------------------------

    private void placeVillage(TestSingleplayerContext w) {
        w.getServer().runOnServer(server -> {
            var level = server.overworld();
            for (int cx = -128 >> 4; cx <= 128 >> 4; cx++) for (int cz = -128 >> 4; cz <= 128 >> 4; cz++) level.getChunk(cx, cz);
        });
        w.getServer().runCommand("place structure villagefriends:village 0 " + (GROUND + 1) + " 0");
        w.getServer().runCommand("kill @e[type=minecraft:villager]");
        w.getServer().runCommand("kill @e[type=minecraft:iron_golem]");
        w.getServer().runCommand("kill @e[type=minecraft:cat]");
    }
    private void mapDump(TestSingleplayerContext w) {
        var text = w.getServer().computeOnServer(server -> {
            var level = server.overworld();
            var out = new StringBuilder();
            for (int z = -40; z <= 40; z++) for (int x = -40; x <= 40; x++) {
                int top = level.getHeight(net.minecraft.world.level.levelgen.Heightmap.Types.MOTION_BLOCKING, x, z) - 1;
                var state = level.getBlockState(new BlockPos(x, top, z));
                out.append(x).append(',').append(z).append(',').append(top).append(',')
                   .append(BuiltInRegistries.BLOCK.getKey(state.getBlock()).getPath()).append('\n');
            }
            return out.toString();
        });
        try { Files.writeString(frames.resolve("plaza-map.csv"), text); } catch (java.io.IOException e) { throw new RuntimeException(e); }
    }
    private void view(TestSingleplayerContext w, double x, double y, double z, float yaw, float pitch, String name) {
        w.getServer().runCommand(String.format(Locale.ROOT, "tp @a %.2f %.2f %.2f %.1f %.1f", x, y, z, yaw, pitch));
        c.waitTicks(60);
        c.takeScreenshot(TestScreenshotOptions.of("scout-" + name).withDestinationDir(frames));
    }
    private void scout(TestSingleplayerContext w) {
        w.getServer().runCommand("gamemode spectator @a");
        c.runOnClient(client -> { if (!client.gui.hud.isHidden()) client.gui.hud.toggle(); });
        placeVillage(w);
        c.waitTicks(40);
        mapDump(w);
        view(w, -48, GROUND + 40, -48, -45, 35, "aerial-nw");
        view(w, 48, GROUND + 40, 48, 135, 35, "aerial-se");
        view(w, 0, GROUND + 60, 0, 0, 90, "top");
        view(w, 0, GROUND + 110, 0, 0, 90, "top-high");
        view(w, 0, GROUND + 30, 0, 0, 90, "top-low");
        view(w, -10, GROUND + 6, -10, -45, 20, "square");
    }

    // -- the living village ------------------------------------------------------------------------

    /** job, personality (or "-"), child?, x, z, facing yaw, ai? */
    private static final Object[][] CAST = {
        {"librarian", "thoughtful", false, -2.2, -8.5, -90F, false},    // two neighbors chatting, north
        {"farmer", "warmhearted", false, 0.2, -8.5, 90F, false},
        {"knight", "protective", false, -6.0, -9.0, -33F, false},
        {"painter", "imaginative", false, 6.5, -7.5, 41F, false},
        {"tailor", "playful", false, 8.5, 0.5, -90F, false},              // greets the camera from the east, then talks
        {"toolsmith", "pragmatic", false, -2.5, 8.5, 0F, false},          // workers, south, facing the camera
        {"cook", "warmhearted", false, 1.5, 8.5, 0F, false},
        {"bard", "playful", false, 4.5, 9.5, 20F, false},
        {"none", "playful", true, -9.0, -3.5, 85F, false},                // children, west, spaced apart to play
        {"none", "adventurous", true, -9.5, 0.0, 95F, false},
        {"none", "curious", true, -8.5, 3.5, 90F, false},
        {"fisherman", "reserved", false, -4.5, 4.5, -135F, false},        // fishing the fountain
        {"cleric", "gentle", false, 9.0, -3.5, 90F, false},
        {"none", "-", false, 12.0, -12.0, 0F, true},                      // free to wander
        {"nitwit", "-", false, -12.0, 12.0, 0F, true},
    };
    private static final int HOST = 4;
    /** Camera keys: seconds, x, eye height above the plaza, z, yaw, pitch. Eased between keys; close keys cut. */
    private static final double[][] CAMERA = {
        {0, 0.5, 9.0, -22.0, 0, 26}, {7.5, -0.6, 1.75, -13.6, -2, 8}, {12.6, -0.4, 1.62, -12.9, 4, 7},
        {13.0, -14.2, 1.3, 1.6, -100, 7}, {18.4, -13.2, 1.25, 2.2, -94, 8},
        {18.8, -1.4, 2.0, 13.4, 176, 10}, {24.2, 1.0, 1.9, 12.8, 186, 9},
        {24.6, 21.0, 1.62, 0.5, 90, 3}, {29.0, 11.6, 1.62, 0.5, 90, 3},
        {40.0, 11.6, 1.62, 0.5, 90, 3}, {48.5, 16.5, 5.0, 0.5, 90, 15},
    };
    private Runnable stepWorld = () -> {};

    private double surface(TestSingleplayerContext w, double x, double z) {
        return w.getServer().computeOnServer(s -> (double) s.overworld().getHeight(net.minecraft.world.level.levelgen.Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
                (int) Math.floor(x), (int) Math.floor(z)));
    }
    private static double ease(double t) { t = Math.max(0, Math.min(1, t)); return t * t * (3 - 2 * t); }
    /** Cuts happen where two keys sit half a second apart; everything else glides. */
    private static double[] camera(double seconds) {
        int i = 0;
        while (i < CAMERA.length - 2 && seconds > CAMERA[i + 1][0]) i++;
        var a = CAMERA[i]; var b = CAMERA[i + 1];
        double t = ease((seconds - a[0]) / (b[0] - a[0]));
        if (b[0] - a[0] <= .5) t = seconds >= b[0] ? 1 : 0;
        var out = new double[5];
        for (int k = 0; k < 5; k++) out[k] = a[k + 1] + (b[k + 1] - a[k + 1]) * t;
        return out;
    }
    private void place(double plaza, double[] cam) {
        double x = cam[0], y = plaza + cam[1] - 1.62, z = cam[2];
        float yaw = (float) cam[3], pitch = (float) cam[4];
        c.runOnClient(client -> {
            var p = client.player;
            p.setPos(x, y, z); p.xo = p.xOld = x; p.yo = p.yOld = y; p.zo = p.zOld = z;
            p.setYRot(yaw); p.yRotO = yaw; p.setXRot(pitch); p.xRotO = pitch;
            p.setYHeadRot(yaw); p.yHeadRotO = yaw; p.setDeltaMovement(Vec3.ZERO);
        });
    }
    /** One frozen-world tick forward; waits until the client has applied it. */
    private void step(int reference) {
        int before = c.computeOnClient(client -> client.level.getEntity(reference).tickCount);
        stepWorld.run();
        for (int i = 0; i < 20; i++) {
            c.waitTick();
            if (c.computeOnClient(client -> client.level.getEntity(reference).tickCount) > before) { stepped++; return; }
        }
        throw new AssertionError("Frozen world did not step");
    }

    private void village(TestSingleplayerContext w) {
        scene = "village"; frame = 0; stepped = 0;
        int stride = Integer.getInteger("villagefriends.filmStride", 1);
        w.getServer().runCommand("gamemode creative @a");
        w.getServer().runCommand("time set 3000");
        c.runOnClient(client -> { if (!client.gui.hud.isHidden()) client.gui.hud.toggle(); client.player.getAbilities().flying = true; });
        placeVillage(w);
        double plaza = surface(w, -6, -9);
        w.getServer().runCommand(String.format(Locale.ROOT, "setblock -3 %d 9 minecraft:anvil[facing=east]", (int) surface(w, -3, 9)));
        w.getServer().runCommand(String.format(Locale.ROOT, "setblock 1 %d 9 minecraft:water_cauldron[level=3]", (int) surface(w, 1, 9)));
        var random = new Random(2026);
        var ids = new ArrayList<UUID>();
        for (var role : CAST) {
            String personality = role[1].equals("-") ? null : (String) role[1];
            var id = AnimationCast.identity(random, personality);
            ids.add(id);
            double x = (double) role[3], z = (double) role[4], y = surface(w, x, z);
            w.getServer().runOnServer(s -> {
                var v = AnimationCast.spawn(s.overworld(), id, new AnimationCast.Role((String) role[0], personality, (boolean) role[2]),
                        x, y, z, (float) role[5], (boolean) role[6]);
                v.setCustomNameVisible(false);
            });
        }
        w.getConnection().waitForClientboundEntityUpdates(EntityTypes.VILLAGER);
        place(plaza, camera(0));
        c.waitTicks(80);
        settle(w);
        var entities = w.getServer().computeOnServer(s -> ids.stream().map(id -> s.overworld().getEntity(id).getId()).toList());
        int reference = entities.getFirst(), host = entities.get(HOST);
        String gift = w.getServer().computeOnServer(s -> target(s.overworld().getEntity(ids.get(HOST))).getAttached(PROFILE).love());
        // Let the village settle into its rhythm before rolling.
        c.waitTicks(160);
        w.getServer().runCommand("tick freeze");
        c.waitTicks(5);
        stepWorld = () -> w.getServer().runCommand("tick step 1");
        boolean talking = false, joked = false, gifted = false, closed = false, rain = false;
        double end = CAMERA[CAMERA.length - 1][0];
        for (int f = 0; f <= end * FPS; f++) {
            double seconds = f / (double) FPS, ticks = seconds * 20;
            int target = (int) Math.floor(ticks);
            while (stepped < target) step(reference);
            if (!talking && seconds >= 29.6) {
                talking = true;
                w.getServer().runOnServer(s -> w.getConnection().getServerPlayer().setItemInHand(InteractionHand.MAIN_HAND,
                        new ItemStack(BuiltInRegistries.ITEM.getValue(Identifier.parse(gift)))));
                c.runOnClient(client -> { var v = client.level.getEntity(host); client.gameMode.interact(client.player, v, new EntityHitResult(v), InteractionHand.MAIN_HAND); });
                c.waitForScreen(FriendshipScreen.class);
            }
            if (talking && !joked && seconds >= 32.0) { joked = true; c.clickScreenButton("Share a joke"); }
            if (joked && !rain && seconds >= 32.6) { rain = true; w.getServer().runCommand("weather rain"); }
            if (joked && !gifted && seconds >= 35.6) { gifted = true; c.clickScreenButton("Give gift"); }
            if (gifted && !closed && seconds >= 40.0) { closed = true; c.runOnClient(client -> client.gui.setScreen(null)); }
            if (f % stride != 0) continue;
            place(plaza, camera(seconds));
            shot((float) (ticks - target));
        }
        w.getServer().runCommand("tick unfreeze");
    }
}
