package dev.villagefriends;

import dev.villagefriends.client.*;
import dev.villagefriends.outfit.*;
import java.util.*;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.minecraft.client.renderer.texture.DynamicTexture;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.npc.villager.VillagerProfession;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;

/** Renders the whole wardrobe through the real resident renderer and checks palette lock and armor hiding. */
@SuppressWarnings("UnstableApiUsage")
public final class OutfitGameTest implements FabricClientGameTest {
    private static final int PAGE = 10;
    private static final Set<String> VANILLA_JOBS = Set.of("none", "nitwit", "armorer", "butcher", "cartographer", "cleric", "farmer",
        "fisherman", "fletcher", "leatherworker", "librarian", "mason", "shepherd", "toolsmith", "weaponsmith");
    private static void check(boolean ok, String message) { if (!ok) throw new AssertionError(message); }
    private static ResourceKey<VillagerProfession> registryKey(Profession job) {
        String name = job.name().toLowerCase(Locale.ROOT);
        if (VillageProfessions.JOBS.contains(name)) return VillageProfessions.key(name);
        if (VANILLA_JOBS.contains(name)) return ResourceKey.create(Registries.VILLAGER_PROFESSION, Identifier.withDefaultNamespace(name));
        return null;
    }
    /** The resident gender a template dresses: its own set's (unisex templates show on men). */
    static Gender gender(Wardrobe.OutfitTemplate template) {
        return template.top().fit() == Garment.Fit.FEMALE ? Gender.FEMALE : Gender.MALE;
    }
    static String setName(Gender gender) { return gender == Gender.FEMALE ? "Women's wardrobe" : "Men's wardrobe"; }
    /** A real, registered profession that wears this template, preferring jobs where it comes first. */
    private static Profession sceneJob(Wardrobe.OutfitTemplate template) {
        Profession best = null; int bestRank = Integer.MAX_VALUE;
        for (var job : Profession.values()) {
            int rank = Wardrobe.templates(job, gender(template)).indexOf(template);
            if (registryKey(job) != null && rank >= 0 && rank < bestRank) { best = job; bestRank = rank; }
        }
        if (best == null) throw new AssertionError("No registered profession wears " + template.id());
        return best;
    }
    private static Profession jobFor(Wardrobe.OutfitTemplate template) {
        for (var job : Profession.values()) if (Wardrobe.templates(job, gender(template)).contains(template)) return job;
        return Profession.NONE;
    }
    private static void gallery(ClientGameTestContext c, int villager, List<OutfitPreviewScreen.Cell> cells, int columns,
                                OutfitPreviewScreen.View view, String title, String subtitle, String screenshot) {
        c.runOnClient(client -> client.gui.setScreen(new OutfitPreviewScreen((Villager)client.level.getEntity(villager), cells, columns, view, title, subtitle)));
        c.waitForScreen(OutfitPreviewScreen.class); c.waitTicks(4); c.takeScreenshot(screenshot);
        c.runOnClient(client -> client.gui.setScreen(null));
    }

    /** Spawns one resident per template in two staggered rows, each dressed by a real profession and recipe. */
    private static List<Integer> scene(TestSingleplayerContext world, List<Wardrobe.OutfitTemplate> templates, int offset, double[] origin) {
        var palettes = PaletteID.values();
        return world.getServer().computeOnServer(server -> {
            var list = new ArrayList<Integer>(); var level = world.getConnection().getServerLevel();
            for (int index = 0; index < templates.size(); index++) {
                var template = templates.get(index); int n = offset + index;
                var job = sceneJob(template); var palette = palettes[n % palettes.length]; var gender = gender(template);
                var hairs = Wardrobe.hair(gender); var wantHair = hairs.get(n % hairs.size());
                long seed = -1;
                for (long s = 0; s < 4_000_000 && seed < 0; s++) {
                    var o = new ResidentLook(n % 6, gender, palette, s).outfit(job);
                    if (o.top() == template.top() && o.bottom() == template.bottom() && o.hair() == wantHair) seed = s;
                }
                check(seed >= 0, "Scene seed for " + template.id());
                var resident = new Villager(EntityTypes.VILLAGER, level);
                resident.setNoAi(true); resident.setAge(0);
                // Two staggered rows so every resident is visible from the camera.
                int row = index % 2, column = index / 2;
                resident.setPos(origin[0] + (column - 2) * 1.5 - .4 + row * .8, origin[1], origin[2] + 4.4 + row * 1.9);
                resident.setYRot(180); resident.yBodyRot = resident.yHeadRot = 180;
                resident.setVillagerData(resident.getVillagerData().withProfession(server.registryAccess(), registryKey(job)));
                String recipe = new ResidentLook(n % 6, gender, palette, seed).recipe();
                VillageFriends.target(resident).setAttached(VillageFriends.PROFILE, ResidentProfile.generate(resident.getUUID(), recipe));
                level.addFreshEntity(resident);
                list.add(resident.getId());
            }
            return list;
        });
    }

    private static void checkDressed(ClientGameTestContext context, List<Integer> ids, List<Wardrobe.OutfitTemplate> templates) {
        context.runOnClient(client -> {
            for (int n = 0; n < ids.size(); n++) {
                var resident = (Villager)client.level.getEntity(ids.get(n));
                var renderer = (ResidentRenderer)client.getEntityRenderDispatcher().getRenderer(resident);
                var state = renderer.createRenderState(resident, 1);
                var template = templates.get(n);
                check(state.outfit != null && state.outfit.top() == template.top() && state.outfit.bottom() == template.bottom(),
                    "Profession dresses " + template.id());
                var image = ((DynamicTexture)client.getTextureManager().getTexture(state.texture)).getPixels();
                check(image.getWidth() == 256 && image.getHeight() == 512, "Resident atlas dimensions");
                // Palette lock: every texel outside the 64x64 skin is a palette or hair-ramp color.
                var allowed = new HashSet<Integer>();
                for (var ramp : state.outfit.palette().ramps()) for (int rgb : ramp) allowed.add(0xFF000000 | rgb);
                for (int rgb : state.outfit.hairColor().ramp()) allowed.add(0xFF000000 | rgb);
                for (int y = 0; y < image.getHeight(); y++) for (int x = 0; x < image.getWidth(); x++) {
                    if (x < 64 && y < 64 || y == 0 && x >= 64 && x < 68) continue;
                    int argb = image.getPixel(x, y);
                    if ((argb >>> 24) == 0) continue;
                    check(allowed.contains(argb) || (argb >>> 24) < 255, "Off-palette texel at " + x + "," + y + " in " + template.id());
                }
                // Guard professions now arrive armored; compare an explicit unarmored pose with an armored one.
                state.headEquipment = ItemStack.EMPTY; state.chestEquipment = ItemStack.EMPTY; state.legsEquipment = ItemStack.EMPTY;
                var model = new ResidentModel(false); model.setupAnim(state);
                var bare = WardrobeLayer.shown(state);
                int pieces = state.outfit.garments().stream().mapToInt(g -> g.pieces().size()).sum();
                check(bare.size() <= pieces && bare.stream().allMatch(s -> state.outfit.garments().contains(s.garment())),
                    "Only the worn garments' pieces are drawn");
                state.headEquipment = new ItemStack(Items.IRON_HELMET); state.chestEquipment = new ItemStack(Items.IRON_CHESTPLATE);
                state.legsEquipment = new ItemStack(Items.IRON_LEGGINGS); model.setupAnim(state);
                check(WardrobeLayer.shown(state).isEmpty(), "Full armor hides every wardrobe piece");
                check(!model.hat.visible, "Helmet hides the hair layer");
                state.headEquipment = ItemStack.EMPTY; state.chestEquipment = ItemStack.EMPTY; state.legsEquipment = ItemStack.EMPTY;
                model.setupAnim(state);
                check(WardrobeLayer.shown(state).equals(bare), "Pieces return without armor");
            }
        });
    }

    @Override public void runTest(ClientGameTestContext context) {
        context.getInput().resizeWindow(1920, 1080);
        context.runOnClient(client -> { client.options.pauseOnLostFocus = false; client.options.guiScale().set(2); client.resizeGui(); });
        var palettes = PaletteID.values();
        var templates = Wardrobe.OUTFITS;
        try (var world = context.worldBuilder().create()) {
            world.getConnection().waitForChunksRender();
            world.getServer().runCommand("time set noon"); world.getServer().runCommand("weather clear");
            world.getServer().runCommand("gamerule advance_time false");
            double[] origin = world.getServer().computeOnServer(server -> {
                var p = world.getConnection().getServerPlayer(); return new double[]{p.getX(), p.getY(), p.getZ()};
            });
            int model = -1;
            for (int page = 0; page * PAGE < templates.size(); page++) {
                var subset = templates.subList(page * PAGE, Math.min(templates.size(), (page + 1) * PAGE));
                var ids = scene(world, subset, page * PAGE, origin);
                world.getConnection().waitForClientboundEntityUpdates(EntityTypes.VILLAGER); context.waitTicks(20);
                checkDressed(context, ids, subset);
                context.runOnClient(client -> { if (!client.gui.hud.isHidden()) client.gui.hud.toggle(); });
                world.getServer().runCommand("gamemode spectator @p");
                world.getServer().runCommand(String.format(Locale.ROOT, "tp @p %.2f %.2f %.2f 0 24", origin[0], origin[1] + 1.9, origin[2] - .6));
                context.waitTicks(30);
                context.takeScreenshot("village-friends-wardrobe-in-world-" + (page + 1));
                context.runOnClient(client -> { if (client.gui.hud.isHidden()) client.gui.hud.toggle(); });
                world.getServer().runCommand("gamemode creative @p");
                boolean last = (page + 1) * PAGE >= templates.size();
                if (last) model = ids.getFirst();
                else world.getServer().runOnServer(server -> ids.forEach(id -> world.getConnection().getServerLevel().getEntity(id).discard()));
            }

            // 1. Every outfit, a page of ten at a time, each with its own hairstyle, hair color, palette and complexion.
            for (int page = 0; page * PAGE < templates.size(); page++) {
                var cells = new ArrayList<OutfitPreviewScreen.Cell>();
                for (int i = page * PAGE; i < Math.min(templates.size(), (page + 1) * PAGE); i++) {
                    var t = templates.get(i); var palette = MasterPalettes.get(palettes[i % palettes.length]);
                    var hairs = Wardrobe.hair(gender(t));
                    var outfit = new Outfit(gender(t), jobFor(t), palette, hairs.get(i % hairs.size()),
                        Wardrobe.HAIR_COLORS.get((i * 3) % Wardrobe.HAIR_COLORS.size()), t.top(), t.bottom(), t);
                    cells.add(new OutfitPreviewScreen.Cell(outfit, i % 6, t.name(), palette.name() + (t.locked() ? "  /  set" : "")));
                }
                String n = String.valueOf(page + 1);
                var sets = cells.stream().map(c -> setName(c.outfit().gender())).distinct().toList();
                gallery(context, model, cells, 5, OutfitPreviewScreen.View.FRONT, "VILLAGE FRIENDS  /  OUTFITS " + (page * PAGE + 1) + "-" + (page * PAGE + cells.size()),
                    String.join(" + ", sets) + "  /  palette-locked pixel art and 3D pieces",
                    "village-friends-outfits-" + n);
                gallery(context, model, cells, 5, OutfitPreviewScreen.View.BACK, "VILLAGE FRIENDS  /  OUTFITS " + (page * PAGE + 1) + "-" + (page * PAGE + cells.size()) + "  (BACK)",
                    "Every garment is painted all the way around", "village-friends-outfits-" + n + "-back");
                gallery(context, model, cells, 5, OutfitPreviewScreen.View.WALK, "VILLAGE FRIENDS  /  OUTFITS " + (page * PAGE + 1) + "-" + (page * PAGE + cells.size()) + "  (MID-STRIDE)",
                    "Skirts, aprons and cloaks follow the leading leg", "village-friends-outfits-" + n + "-walking");
            }

            // 2. Every hairstyle, ten per page, in natural colors, over its own set's everyday outfit.
            for (int page = 0; page * PAGE < Wardrobe.HAIR.size(); page++) {
                var cells = new ArrayList<OutfitPreviewScreen.Cell>();
                for (int i = page * PAGE; i < Math.min(Wardrobe.HAIR.size(), (page + 1) * PAGE); i++) {
                    var hair = Wardrobe.HAIR.get(i); var color = Wardrobe.HAIR_COLORS.get(i % Wardrobe.HAIR_COLORS.size());
                    var gender = hair.fit() == Garment.Fit.FEMALE ? Gender.FEMALE : Gender.MALE;
                    var base = Wardrobe.templates(Profession.NONE, gender).getFirst();
                    var outfit = new Outfit(gender, Profession.NONE, MasterPalettes.get(palettes[i % palettes.length]), hair, color,
                        base.top(), base.bottom(), base);
                    cells.add(new OutfitPreviewScreen.Cell(outfit, (i + 2) % 6, hair.name(), color.name()));
                }
                String n = String.valueOf(page + 1);
                var sets = cells.stream().map(c -> setName(c.outfit().gender())).distinct().toList();
                gallery(context, model, cells, 5, OutfitPreviewScreen.View.HEAD, "VILLAGE FRIENDS  /  HAIRSTYLES " + (page * PAGE + 1) + "-" + (page * PAGE + cells.size()),
                    String.join(" + ", sets) + "  /  anime-inspired, independent natural hair colors",
                    "village-friends-hairstyles-" + n);
                gallery(context, model, cells, 5, OutfitPreviewScreen.View.HEAD_BACK, "VILLAGE FRIENDS  /  HAIRSTYLES " + (page * PAGE + 1) + "-" + (page * PAGE + cells.size()) + "  (BACK)",
                    "Layered locks, tails, braids, knots and buns", "village-friends-hairstyles-" + n + "-back");
            }

            // 3. Mix and match within each set: any free top with any compatible bottom, any palette, any hair.
            var random = new SplittableRandom(20261005L);
            int mixPage = 0;
            for (var gender : List.of(Gender.MALE, Gender.FEMALE)) for (int page = 1; page <= 2; page++) {
                var tops = Wardrobe.tops(gender).stream().filter(t -> !t.locked()).toList(); var hairs = Wardrobe.hair(gender);
                if (tops.isEmpty()) continue;
                var mixCells = new ArrayList<OutfitPreviewScreen.Cell>();
                for (int i = 0; i < 10; i++) {
                    var top = tops.get(random.nextInt(tops.size()));
                    var bottoms = Wardrobe.bottomsFor(top, gender); var bottom = bottoms.get(random.nextInt(bottoms.size()));
                    var palette = MasterPalettes.get(palettes[random.nextInt(palettes.length)]);
                    var outfit = new Outfit(gender, Profession.NONE, palette, hairs.get(random.nextInt(hairs.size())),
                        Wardrobe.HAIR_COLORS.get(random.nextInt(Wardrobe.HAIR_COLORS.size())), top, bottom, templates.getFirst());
                    mixCells.add(new OutfitPreviewScreen.Cell(outfit, random.nextInt(6), top.name(), bottom.name(), palette.name()));
                }
                gallery(context, model, mixCells, 5, OutfitPreviewScreen.View.FRONT, "VILLAGE FRIENDS  /  MIX AND MATCH  /  " + setName(gender).toUpperCase(Locale.ROOT),
                    "Tops and bottoms combine freely within one palette (armor, hose and locked sets have rules)", "village-friends-mix-and-match-" + ++mixPage);
            }

            // 4. One outfit across all ten master palettes.
            var paletteCells = new ArrayList<OutfitPreviewScreen.Cell>();
            var showcase = templates.get(Math.min(16, templates.size() - 1));
            for (int i = 0; i < palettes.length; i++) {
                var palette = MasterPalettes.get(palettes[i]);
                var hairs = Wardrobe.hair(gender(showcase));
                var outfit = new Outfit(gender(showcase), jobFor(showcase), palette, hairs.get((i + 12) % hairs.size()),
                    Wardrobe.HAIR_COLORS.get((i + 5) % Wardrobe.HAIR_COLORS.size()), showcase.top(), showcase.bottom(), showcase);
                paletteCells.add(new OutfitPreviewScreen.Cell(outfit, i % 6, palette.name(), ""));
            }
            gallery(context, model, paletteCells, 5, OutfitPreviewScreen.View.FRONT, "VILLAGE FRIENDS  /  TEN MASTER PALETTES",
                "One palette per outfit, no mixing: " + showcase.name(), "village-friends-ten-palettes");

            int first = model;
            var reload = context.computeOnClient(client -> client.reloadResourcePacks());
            context.waitFor(client -> reload.isDone(), 600); reload.join();
            context.runOnClient(client -> {
                var resident = (Villager)client.level.getEntity(first);
                var renderer = (ResidentRenderer)client.getEntityRenderDispatcher().getRenderer(resident);
                check(renderer.createRenderState(resident, 1).texture.getPath().startsWith("generated/"), "Outfits survive resource reload");
                ResidentSkins.clear(); check(ResidentSkins.cachedCount() == 0, "Atlas cache released");
                // Measure what posing one resident costs per frame: the body model plus its worn garments' pieces.
                var state = renderer.createRenderState(resident, 1); var timed = new ResidentModel(false);
                var stack = new com.mojang.blaze3d.vertex.PoseStack(); int[] drawn = {0};
                for (int i = 0; i < 500; i++) { state.ageInTicks = i; timed.setupAnim(state); WardrobeLayer.pose(timed, state, stack, (part, posed) -> drawn[0]++); }
                drawn[0] = 0;
                long start = System.nanoTime();
                for (int i = 0; i < 4000; i++) {
                    state.ageInTicks = i * .5F; state.walkAnimationPos = i * .1F; state.walkAnimationSpeed = .6F;
                    timed.setupAnim(state); WardrobeLayer.pose(timed, state, stack, (part, posed) -> drawn[0]++);
                }
                VillageFriends.LOGGER.info("WARDROBE MODEL: {} body parts, {} pieces worn, pose {} us per resident", timed.allParts().size(),
                    drawn[0] / 4000, String.format(Locale.ROOT, "%.1f", (System.nanoTime() - start) / 4000 / 1000.0));
            });
            // Let the client/server test phases settle after reload before disconnecting the integrated server.
            context.waitTicks(40);
        }
        VillageFriends.LOGGER.info("WARDROBE PASSED: {} outfits, {} hairstyles, {} tops, {} bottoms, palette lock, armor and reload.",
            Wardrobe.OUTFITS.size(), Wardrobe.HAIR.size(), Wardrobe.TOPS.size(), Wardrobe.BOTTOMS.size());
    }
}
