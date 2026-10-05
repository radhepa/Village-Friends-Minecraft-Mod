package dev.villagefriends;

import dev.villagefriends.client.*;
import dev.villagefriends.outfit.*;
import java.util.*;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.minecraft.client.renderer.texture.DynamicTexture;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.npc.villager.VillagerProfession;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;

/** Renders the whole wardrobe through the real resident renderer and checks palette lock and armor hiding. */
@SuppressWarnings("UnstableApiUsage")
public final class OutfitGameTest implements FabricClientGameTest {
    private static void check(boolean ok, String message) { if (!ok) throw new AssertionError(message); }
    private static String nice(String id) {
        var words = id.toLowerCase(Locale.ROOT).split("_");
        var out = new StringBuilder();
        for (var w : words) out.append(out.isEmpty() ? "" : " ").append(Character.toUpperCase(w.charAt(0))).append(w.substring(1));
        return out.toString();
    }
    /** Real professions whose preferred outfit is each template, for the in-world scene. */
    private static final Map<String, ResourceKey<VillagerProfession>> SCENE_JOBS = new LinkedHashMap<>();
    static {
        SCENE_JOBS.put("knight_errant", VillageProfessions.key("knight"));
        SCENE_JOBS.put("trailblazer", VillagerProfession.CARTOGRAPHER);
        SCENE_JOBS.put("arcanist", VillageProfessions.key("scholar"));
        SCENE_JOBS.put("farmhand", VillagerProfession.FARMER);
        SCENE_JOBS.put("merchant", VillageProfessions.key("tavern_keeper"));
        SCENE_JOBS.put("mariner", VillagerProfession.FISHERMAN);
        SCENE_JOBS.put("smith", VillagerProfession.TOOLSMITH);
        SCENE_JOBS.put("ranger", VillageProfessions.key("archer"));
        SCENE_JOBS.put("minstrel", VillageProfessions.key("bard"));
        SCENE_JOBS.put("pilgrim", VillagerProfession.CLERIC);
    }
    private static Profession jobFor(Wardrobe.OutfitTemplate template) {
        for (var job : Profession.values()) if (Wardrobe.templates(job).getFirst() == template) return job;
        return Profession.NONE;
    }
    private static void gallery(ClientGameTestContext c, int villager, List<OutfitPreviewScreen.Cell> cells, int columns,
                                OutfitPreviewScreen.View view, String title, String subtitle, String screenshot) {
        c.runOnClient(client -> client.gui.setScreen(new OutfitPreviewScreen((Villager)client.level.getEntity(villager), cells, columns, view, title, subtitle)));
        c.waitForScreen(OutfitPreviewScreen.class); c.waitTicks(4); c.takeScreenshot(screenshot);
        c.runOnClient(client -> client.gui.setScreen(null));
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
            // In-world scene: one resident per template, dressed by their real profession and recipe.
            var ids = world.getServer().computeOnServer(server -> {
                var list = new ArrayList<Integer>(); var player = world.getConnection().getServerPlayer();
                int index = 0;
                for (var template : templates) {
                    var key = SCENE_JOBS.getOrDefault(template.id(), VillagerProfession.NONE);
                    var job = Profession.fromId(key.identifier().getPath());
                    var palette = palettes[index % palettes.length];
                    var wantHair = Wardrobe.HAIR.get(index % Wardrobe.HAIR.size());
                    long seed = -1;
                    for (long s = 0; s < 400000 && seed < 0; s++) {
                        var o = new ResidentLook(index % 6, Gender.MALE, palette, s).outfit(job);
                        if (o.top() == template.top() && o.bottom() == template.bottom() && o.hair() == wantHair) seed = s;
                    }
                    check(seed >= 0, "Scene seed for " + template.id());
                    var resident = new Villager(EntityTypes.VILLAGER, player.level());
                    resident.setNoAi(true); resident.setAge(0);
                    // Two staggered rows so every resident is visible from the camera.
                    int row = index % 2, column = index / 2;
                    double x = player.getX() + (column - 2) * 1.5 - .4 + row * .8, z = player.getZ() + 4.4 + row * 1.9;
                    resident.setPos(x, player.getY(), z);
                    resident.setYRot(180); resident.yBodyRot = resident.yHeadRot = 180;
                    resident.setVillagerData(resident.getVillagerData().withProfession(server.registryAccess(), key));
                    String recipe = new ResidentLook(index % 6, Gender.MALE, palette, seed).recipe();
                    VillageFriends.target(resident).setAttached(VillageFriends.PROFILE, ResidentProfile.generate(resident.getUUID(), recipe));
                    world.getConnection().getServerLevel().addFreshEntity(resident);
                    list.add(resident.getId()); index++;
                }
                return list;
            });
            world.getConnection().waitForClientboundEntityUpdates(EntityTypes.VILLAGER); context.waitTicks(20);

            context.runOnClient(client -> {
                for (int n = 0; n < ids.size(); n++) {
                    var resident = (Villager)client.level.getEntity(ids.get(n));
                    var renderer = (ResidentRenderer)client.getEntityRenderDispatcher().getRenderer(resident);
                    var state = renderer.createRenderState(resident, 1);
                    var template = templates.get(n);
                    check(state.outfit != null && state.outfit.top() == template.top() && state.outfit.bottom() == template.bottom(),
                        "Profession dresses " + template.id());
                    var image = ((DynamicTexture)client.getTextureManager().getTexture(state.texture)).getPixels();
                    check(image.getWidth() == 512 && image.getHeight() == 512, "Resident atlas dimensions");
                    // Palette lock: every texel outside the 64x64 skin is a palette or hair-ramp color.
                    var allowed = new HashSet<Integer>();
                    for (var ramp : state.outfit.palette().ramps()) for (int rgb : ramp) allowed.add(0xFF000000 | rgb);
                    for (int rgb : state.outfit.hairColor().ramp()) allowed.add(0xFF000000 | rgb);
                    int painted = 0;
                    for (int y = 0; y < 512; y++) for (int x = 0; x < 512; x++) {
                        if (x < 64 && y < 64 || y == 0 && x >= 64 && x < 68) continue;
                        int argb = image.getPixel(x, y);
                        if ((argb >>> 24) == 0) continue;
                        painted++;
                        check(allowed.contains(argb) || (argb >>> 24) < 255, "Off-palette texel at " + x + "," + y + " in " + template.id());
                    }
                    check(painted > 0 || state.outfit.garments().stream().allMatch(g -> g.pieces().isEmpty()), "3D pieces painted");
                    var model = new ResidentModel(false); model.setupAnim(state);
                    long visible = model.root().getAllParts().stream().filter(p -> p.visible).count();
                    state.headEquipment = new ItemStack(Items.IRON_HELMET); state.chestEquipment = new ItemStack(Items.IRON_CHESTPLATE);
                    state.legsEquipment = new ItemStack(Items.IRON_LEGGINGS); model.setupAnim(state);
                    check(model.root().getAllParts().stream().filter(p -> p.visible).count() < visible, "Armor hides wardrobe pieces");
                    check(!model.hat.visible, "Helmet hides the hair layer");
                }
            });
            context.runOnClient(client -> { if (!client.gui.hud.isHidden()) client.gui.hud.toggle(); });
            world.getServer().runCommand("gamemode spectator @p");
            world.getServer().runCommand("tp @p ~ ~1.9 ~-.6 0 24");
            context.waitTicks(30);
            context.takeScreenshot("village-friends-wardrobe-in-world");
            context.runOnClient(client -> { if (client.gui.hud.isHidden()) client.gui.hud.toggle(); });
            world.getServer().runCommand("gamemode creative @p");

            int model = ids.getFirst();
            // 1. The ten outfits, each with its own hairstyle, hair color, palette and complexion.
            var outfitCells = new ArrayList<OutfitPreviewScreen.Cell>();
            for (int i = 0; i < templates.size(); i++) {
                var t = templates.get(i); var palette = MasterPalettes.get(palettes[i % palettes.length]);
                var outfit = new Outfit(Gender.MALE, jobFor(t), palette, Wardrobe.HAIR.get(i % Wardrobe.HAIR.size()),
                    Wardrobe.HAIR_COLORS.get((i * 3) % Wardrobe.HAIR_COLORS.size()), t.top(), t.bottom(), t);
                outfitCells.add(new OutfitPreviewScreen.Cell(outfit, i % 6, t.name(), palette.name()));
            }
            gallery(context, model, outfitCells, 5, OutfitPreviewScreen.View.FRONT, "VILLAGE FRIENDS  /  TEN OUTFITS",
                "Palette-locked pixel art  /  3D collars, flaps, pauldrons and pouches", "village-friends-ten-outfits");
            gallery(context, model, outfitCells, 5, OutfitPreviewScreen.View.BACK, "VILLAGE FRIENDS  /  TEN OUTFITS  (BACK)",
                "Every garment is painted all the way around", "village-friends-ten-outfits-back");
            gallery(context, model, outfitCells, 5, OutfitPreviewScreen.View.WALK, "VILLAGE FRIENDS  /  MID-STRIDE",
                "Coat and apron flaps follow the leading leg", "village-friends-ten-outfits-walking");

            // 2. The ten hairstyles in ten natural colors.
            var hairCells = new ArrayList<OutfitPreviewScreen.Cell>();
            var base = templates.get(3 % templates.size());
            for (int i = 0; i < Wardrobe.HAIR.size(); i++) {
                var hair = Wardrobe.HAIR.get(i); var color = Wardrobe.HAIR_COLORS.get(i % Wardrobe.HAIR_COLORS.size());
                var outfit = new Outfit(Gender.MALE, Profession.NONE, MasterPalettes.get(palettes[i % palettes.length]), hair, color,
                    base.top(), base.bottom(), base);
                hairCells.add(new OutfitPreviewScreen.Cell(outfit, (i + 2) % 6, nice(hair.id().substring(4)), color.name()));
            }
            gallery(context, model, hairCells, 5, OutfitPreviewScreen.View.HEAD, "VILLAGE FRIENDS  /  TEN HAIRSTYLES",
                "Volumetric hair  /  independent natural hair colors", "village-friends-ten-hairstyles");
            gallery(context, model, hairCells, 5, OutfitPreviewScreen.View.HEAD_BACK, "VILLAGE FRIENDS  /  TEN HAIRSTYLES  (BACK)",
                "Layered locks, tails, knots and buns", "village-friends-ten-hairstyles-back");

            // 3. Mix and match: any top with any compatible bottom, any palette, any hair.
            var random = new SplittableRandom(20261005L); var mixCells = new ArrayList<OutfitPreviewScreen.Cell>();
            for (int i = 0; i < 10; i++) {
                var top = Wardrobe.TOPS.get(random.nextInt(Wardrobe.TOPS.size()));
                var bottoms = Wardrobe.bottomsFor(top); var bottom = bottoms.get(random.nextInt(bottoms.size()));
                var palette = MasterPalettes.get(palettes[random.nextInt(palettes.length)]);
                var outfit = new Outfit(Gender.MALE, Profession.NONE, palette, Wardrobe.HAIR.get(random.nextInt(Wardrobe.HAIR.size())),
                    Wardrobe.HAIR_COLORS.get(random.nextInt(Wardrobe.HAIR_COLORS.size())), top, bottom, templates.getFirst());
                var topName = Wardrobe.OUTFITS.stream().filter(t -> t.top() == top).findFirst().map(Wardrobe.OutfitTemplate::name).orElse(top.id());
                var bottomName = Wardrobe.OUTFITS.stream().filter(t -> t.bottom() == bottom).findFirst().map(Wardrobe.OutfitTemplate::name).orElse(bottom.id());
                mixCells.add(new OutfitPreviewScreen.Cell(outfit, random.nextInt(6), topName + " top", bottomName + " bottom / " + palette.name()));
            }
            gallery(context, model, mixCells, 5, OutfitPreviewScreen.View.FRONT, "VILLAGE FRIENDS  /  MIX AND MATCH",
                "Tops and bottoms combine freely within one palette (armor and hose have rules)", "village-friends-mix-and-match");

            // 4. One outfit across all ten master palettes.
            var paletteCells = new ArrayList<OutfitPreviewScreen.Cell>();
            var showcase = templates.get(Math.min(2, templates.size() - 1));
            for (int i = 0; i < palettes.length; i++) {
                var palette = MasterPalettes.get(palettes[i]);
                var outfit = new Outfit(Gender.MALE, jobFor(showcase), palette, Wardrobe.HAIR.get((i + 4) % Wardrobe.HAIR.size()),
                    Wardrobe.HAIR_COLORS.get((i + 5) % Wardrobe.HAIR_COLORS.size()), showcase.top(), showcase.bottom(), showcase);
                paletteCells.add(new OutfitPreviewScreen.Cell(outfit, i % 6, palette.name(), ""));
            }
            gallery(context, model, paletteCells, 5, OutfitPreviewScreen.View.FRONT, "VILLAGE FRIENDS  /  TEN MASTER PALETTES",
                "One palette per outfit, no mixing: " + showcase.name(), "village-friends-ten-palettes");

            var reload = context.computeOnClient(client -> client.reloadResourcePacks());
            context.waitFor(client -> reload.isDone(), 600); reload.join();
            context.runOnClient(client -> {
                var resident = (Villager)client.level.getEntity(ids.getFirst());
                var renderer = (ResidentRenderer)client.getEntityRenderDispatcher().getRenderer(resident);
                check(renderer.createRenderState(resident, 1).texture.getPath().startsWith("generated/"), "Outfits survive resource reload");
                ResidentSkins.clear(); check(ResidentSkins.cachedCount() == 0, "Atlas cache released");
            });
            // Let the client/server test phases settle after reload before disconnecting the integrated server.
            context.waitTicks(40);
        }
        VillageFriends.LOGGER.info("WARDROBE PASSED: {} outfits, {} hairstyles, {} tops, {} bottoms, palette lock, armor and reload.",
            Wardrobe.OUTFITS.size(), Wardrobe.HAIR.size(), Wardrobe.TOPS.size(), Wardrobe.BOTTOMS.size());
    }
}
