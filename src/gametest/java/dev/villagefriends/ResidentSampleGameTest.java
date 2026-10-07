package dev.villagefriends;

import dev.villagefriends.client.*;
import dev.villagefriends.outfit.*;
import java.util.*;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.npc.villager.VillagerProfession;

/**
 * Development sample, not part of the regression suite: five random men and five random women,
 * dressed exactly as a new village would dress them (a fresh recipe and a real profession each).
 *
 * <p>Run {@code gradlew runClientGameTest -PresidentSample} (optionally {@code -PsampleSeed=123}
 * to repeat a draw). It saves an in-world shot and a labelled close-up per gender under
 * {@code build/run/clientGameTest/screenshots} and logs every resident's pieces.
 */
@SuppressWarnings("UnstableApiUsage")
public final class ResidentSampleGameTest implements FabricClientGameTest {
    private static final int COUNT = 5;
    private static final Set<String> VANILLA = Set.of("none", "nitwit", "armorer", "butcher", "cartographer", "cleric", "farmer",
        "fisherman", "fletcher", "leatherworker", "librarian", "mason", "shepherd", "toolsmith", "weaponsmith");
    /** Guards arrive in armor, which would hide the clothes this sample is meant to show. */
    private static final Set<Profession> ARMORED = EnumSet.of(Profession.KNIGHT, Profession.ARCHER, Profession.GUARD);

    private record Resident(Gender gender, Profession job, ResidentLook look, Outfit outfit) {}

    private static void check(boolean ok, String message) { if (!ok) throw new AssertionError(message); }
    private static ResourceKey<VillagerProfession> registryKey(Profession job) {
        String name = job.name().toLowerCase(Locale.ROOT);
        if (VillageProfessions.JOBS.contains(name)) return VillageProfessions.key(name);
        if (VANILLA.contains(name)) return ResourceKey.create(Registries.VILLAGER_PROFESSION, Identifier.withDefaultNamespace(name));
        return null;
    }
    private static String jobLabel(Profession job) {
        String id = job.name().toLowerCase(Locale.ROOT);
        return job == Profession.NONE ? "Neighbor" : job == Profession.NITWIT ? "Free Spirit" : VillageProfessions.label(id);
    }

    private static List<Resident> draw(SplittableRandom random, Gender gender) {
        var jobs = Arrays.stream(Profession.values()).filter(j -> registryKey(j) != null && !ARMORED.contains(j)).toList();
        var palettes = PaletteID.values();
        var list = new ArrayList<Resident>();
        for (int i = 0; i < COUNT; i++) {
            var look = new ResidentLook(random.nextInt(6), gender, palettes[random.nextInt(palettes.length)], random.nextLong());
            var job = jobs.get(random.nextInt(jobs.size()));
            list.add(new Resident(gender, job, look, look.outfit(job)));
        }
        return list;
    }

    /** Spawns the residents in a row on a small grass stage, facing the camera; returns entity ids. */
    private static List<Integer> spawn(TestSingleplayerContext world, List<Resident> residents, double[] origin) {
        return world.getServer().computeOnServer(server -> {
            var level = world.getConnection().getServerLevel(); var ids = new ArrayList<Integer>();
            for (int i = 0; i < residents.size(); i++) {
                var r = residents.get(i);
                var villager = new Villager(EntityTypes.VILLAGER, level);
                villager.setNoAi(true); villager.setAge(0);
                villager.setPos(origin[0] + (i - (residents.size() - 1) / 2.0) * 1.45, origin[1], origin[2] + 4.6 + (i % 2) * .35);
                villager.setYRot(180); villager.yBodyRot = villager.yHeadRot = 180;
                villager.setVillagerData(villager.getVillagerData().withProfession(server.registryAccess(), registryKey(r.job())));
                var target = VillageFriends.target(villager);
                target.setAttached(VillageFriends.PROFILE, ResidentProfile.generate(villager.getUUID(), r.look().recipe()));
                target.setAttached(VillageFriends.LOOK, r.look().recipe());
                level.addFreshEntity(villager);
                ids.add(villager.getId());
            }
            return ids;
        });
    }

    private static void gallery(ClientGameTestContext c, int model, List<OutfitPreviewScreen.Cell> cells, OutfitPreviewScreen.View view,
                                String title, String subtitle, String screenshot) {
        c.runOnClient(client -> client.gui.setScreen(new OutfitPreviewScreen((Villager)client.level.getEntity(model), cells, COUNT, view, title, subtitle)));
        c.waitForScreen(OutfitPreviewScreen.class); c.waitTicks(4); c.takeScreenshot(screenshot);
        c.runOnClient(client -> client.gui.setScreen(null));
    }

    @Override public void runTest(ClientGameTestContext context) {
        long seed = Long.getLong("villagefriends.sampleSeed", System.nanoTime());
        var random = new SplittableRandom(seed);
        var groups = new LinkedHashMap<Gender, List<Resident>>();
        groups.put(Gender.MALE, draw(random, Gender.MALE));
        groups.put(Gender.FEMALE, draw(random, Gender.FEMALE));
        VillageFriends.LOGGER.info("RESIDENT SAMPLE seed {} (repeat with -PsampleSeed={})", seed, seed);

        context.getInput().resizeWindow(1920, 1080);
        context.runOnClient(client -> { client.options.pauseOnLostFocus = false; client.options.guiScale().set(2); client.resizeGui(); });
        try (var world = context.worldBuilder().create()) {
            world.getConnection().waitForChunksRender();
            world.getServer().runCommand("time set noon"); world.getServer().runCommand("weather clear");
            world.getServer().runCommand("gamerule advance_time false");
            double[] origin = world.getServer().computeOnServer(server -> {
                var p = world.getConnection().getServerPlayer(); return new double[]{Math.floor(p.getX()) + .5, Math.floor(p.getY()), Math.floor(p.getZ()) + .5};
            });
            // A flat grass stage with open air, so terrain never hides a resident's boots or skirt.
            int x = (int)Math.floor(origin[0]), y = (int)origin[1], z = (int)Math.floor(origin[2]);
            world.getServer().runCommand(String.format(Locale.ROOT, "fill %d %d %d %d %d %d grass_block", x - 7, y - 1, z - 2, x + 7, y - 1, z + 9));
            world.getServer().runCommand(String.format(Locale.ROOT, "fill %d %d %d %d %d %d air", x - 7, y, z - 2, x + 7, y + 4, z + 9));
            int model = -1;
            for (var entry : groups.entrySet()) {
                var gender = entry.getKey(); var residents = entry.getValue();
                String who = gender == Gender.MALE ? "men" : "women";
                var ids = spawn(world, residents, origin);
                world.getConnection().waitForClientboundEntityUpdates(EntityTypes.VILLAGER); context.waitTicks(30);
                var names = new ArrayList<String>();
                context.runOnClient(client -> {
                    for (int i = 0; i < ids.size(); i++) {
                        var villager = (Villager)client.level.getEntity(ids.get(i));
                        var renderer = (ResidentRenderer)client.getEntityRenderDispatcher().getRenderer(villager);
                        var state = renderer.createRenderState(villager, 1); var expected = residents.get(i).outfit();
                        check(state.outfit != null && state.outfit.key().equals(expected.key()), "Resident wears its recipe's outfit");
                        for (var garment : state.outfit.garments()) check(garment.fits(gender), gender + " resident wears " + garment.id());
                        names.add(Dialogue.name(villager.getUUID(), residents.get(i).look().recipe()));
                    }
                });
                for (int i = 0; i < residents.size(); i++) {
                    var r = residents.get(i); var o = r.outfit();
                    VillageFriends.LOGGER.info("RESIDENT SAMPLE {} {}: {} ({}), hair {} in {}, top {}, bottom {}{}, palette {}, complexion {}",
                        who, i + 1, names.get(i), jobLabel(r.job()), o.hair().name(), o.hairColor().name(), o.top().name(), o.bottom().name(),
                        o.top().locked() ? " (locked set)" : "", o.palette().name(), r.look().complexion());
                }
                context.runOnClient(client -> { if (!client.gui.hud.isHidden()) client.gui.hud.toggle(); });
                world.getServer().runCommand("gamemode spectator @p");
                world.getServer().runCommand(String.format(Locale.ROOT, "tp @p %.2f %.2f %.2f 0 18", origin[0], origin[1] + 1.75, origin[2] - 1.4));
                context.waitTicks(30);
                context.takeScreenshot("village-friends-random-" + who + "-in-world");
                context.runOnClient(client -> { if (client.gui.hud.isHidden()) client.gui.hud.toggle(); });
                world.getServer().runCommand("gamemode creative @p");

                var cells = new ArrayList<OutfitPreviewScreen.Cell>();
                for (int i = 0; i < residents.size(); i++) {
                    var r = residents.get(i);
                    cells.add(new OutfitPreviewScreen.Cell(r.outfit(), r.look().complexion(), names.get(i) + "  /  " + jobLabel(r.job()),
                        r.outfit().top().name(), r.outfit().bottom().name()));
                }
                int first = ids.getFirst();
                String title = "VILLAGE FRIENDS  /  FIVE RANDOM " + who.toUpperCase(Locale.ROOT);
                gallery(context, first, cells, OutfitPreviewScreen.View.FRONT, title,
                    "Fresh recipes and real professions, as a new village dresses them  /  seed " + seed, "village-friends-random-" + who);
                gallery(context, first, cells, OutfitPreviewScreen.View.BACK, title + "  (BACK)",
                    "Hair and garments are painted all the way around", "village-friends-random-" + who + "-back");
                if (gender == Gender.FEMALE) model = first;
                else world.getServer().runOnServer(server -> ids.forEach(id -> world.getConnection().getServerLevel().getEntity(id).discard()));
            }
            check(model >= 0, "Sample residents spawned");
            context.waitTicks(20);
        }
        VillageFriends.LOGGER.info("RESIDENT SAMPLE PASSED: {} men and {} women dressed from their own wardrobe sets.", COUNT, COUNT);
    }
}
