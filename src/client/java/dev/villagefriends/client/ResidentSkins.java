package dev.villagefriends.client;

import com.mojang.blaze3d.platform.NativeImage;
import dev.villagefriends.outfit.*;
import java.util.*;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.resource.v1.ResourceLoader;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.texture.DynamicTexture;
import net.minecraft.resources.Identifier;
import net.minecraft.server.packs.PackType;
import net.minecraft.server.packs.resources.*;
import net.minecraft.util.profiling.ProfilerFiller;

/**
 * Bakes one texture per (complexion, outfit): the complexion body, then each garment's key-color
 * pixel art resolved through the outfit's single palette (hair keys through the natural hair
 * color), then the garments' 3D-piece nets into their atlas blocks. Baking happens once per
 * outfit on a cache miss; animation never allocates textures.
 */
public final class ResidentSkins {
    private record Entry(Identifier texture, long tick) {}
    private record Loaded(List<int[]> bodies, Map<String, int[]> art) {}
    private static final LinkedHashMap<String, Entry> textures = new LinkedHashMap<>(64, .75F, true);
    private static final LinkedHashMap<String, Outfit> outfits = new LinkedHashMap<>(256, .75F, true);
    private static List<int[]> bodies = List.of();
    private static Map<String, int[]> art = Map.of();
    private static Identifier id(String path) { return Identifier.fromNamespaceAndPath("villagefriends", path); }
    private static long tick() { return Minecraft.getInstance().level == null ? 0 : Minecraft.getInstance().level.getGameTime(); }
    public static int cachedCount() { return textures.size(); }
    public static void clear() {
        var manager = Minecraft.getInstance().getTextureManager();
        for (var entry : textures.values()) manager.release(entry.texture());
        textures.clear(); outfits.clear();
    }
    private static ResidentLook look(String recipe) {
        var look = ResidentLook.parse(recipe);
        return look == null ? ResidentLook.generate(new UUID(0, 0)) : look;
    }
    public static Outfit outfit(String recipe, String profession) {
        var look = look(recipe); var job = Profession.fromId(profession);
        String key = look.recipe() + ":" + job;
        var outfit = outfits.computeIfAbsent(key, ignored -> look.outfit(job));
        if (outfits.size() > 256) outfits.pollFirstEntry();
        return outfit;
    }
    public static Identifier texture(String recipe) { return texture(recipe, "none"); }
    public static Identifier texture(String recipe, String profession) {
        return texture(outfit(recipe, profession), look(recipe).complexion());
    }
    /** Explicit outfits (previews, portraits, tests) share the same cache and baking path. */
    public static Identifier texture(Outfit outfit, int complexion) {
        String key = complexion + "_" + outfit.key();
        var previous = textures.get(key);
        if (previous != null) {
            textures.put(key, new Entry(previous.texture(), tick()));
            return previous.texture();
        }
        if (bodies.size() != 6) return id("textures/body/0.png");
        var image = new NativeImage(OutfitAtlas.WIDTH, OutfitAtlas.HEIGHT, true);
        var body = bodies.get(complexion);
        int[] skin = body.clone();
        for (var garment : outfit.layers()) {
            int[] codes = codes(garment);
            for (int i = 0; i < 64 * 64; i++) {
                int code = codes[i];
                if (code == Wardrobe.TRANSPARENT) continue;
                if (Wardrobe.shadow(code)) {
                    if ((skin[i] >>> 24) != 0) skin[i] = darken(skin[i], Wardrobe.shadowAlpha(code));
                } else skin[i] = 0xFF000000 | resolve(code, outfit);
            }
        }
        for (int y = 0; y < 64; y++) for (int x = 0; x < 64; x++) image.setPixel(x, y, skin[y * 64 + x]);
        for (var garment : outfit.garments()) {
            var block = OutfitAtlas.block(garment);
            if (block == null) continue;
            int[] codes = codes(garment);
            for (int y = 0; y < garment.extrasHeight(); y++) for (int x = 0; x < 64; x++) {
                int code = codes[(64 + y) * 64 + x];
                int argb = code == Wardrobe.TRANSPARENT ? 0
                    : Wardrobe.shadow(code) ? Wardrobe.shadowAlpha(code) << 24 : 0xFF000000 | resolve(code, outfit);
                image.setPixel(block.x() + x, block.y() + y, argb);
            }
        }
        int hair = outfit.hairColor().base();
        image.setPixel(FaceDetails.BROW_U, FaceDetails.V, FaceDetails.brow(hair));
        image.setPixel(FaceDetails.LASH_U, FaceDetails.V, FaceDetails.lash(hair));
        image.setPixel(FaceDetails.SOCKET_U, FaceDetails.V, FaceDetails.shadow(body[12 * 64 + 12]));
        image.setPixel(FaceDetails.CHIN_U, FaceDetails.V, FaceDetails.shadow(body[15 * 64 + 12]));
        Identifier texture = id("generated/" + key.toLowerCase(Locale.ROOT));
        Minecraft.getInstance().getTextureManager().register(texture, new DynamicTexture(() -> "Outfit " + key, image));
        textures.put(key, new Entry(texture, tick()));
        return texture;
    }
    private static int[] codes(Garment garment) {
        var codes = art.get(garment.id());
        if (codes == null) throw new IllegalStateException("Wardrobe art not loaded: " + garment.id());
        return codes;
    }
    static int resolve(int code, Outfit outfit) {
        int role = code / Wardrobe.SHADES, shade = code % Wardrobe.SHADES;
        return role == Wardrobe.HAIR_ROLE ? outfit.hairColor().shade(shade) : outfit.palette().rgb(role, shade);
    }
    private static int darken(int argb, int alpha) {
        float keep = 1 - alpha / 255F;
        int result = argb & 0xFF000000;
        for (int shift = 16; shift >= 0; shift -= 8) result |= Math.round(((argb >>> shift) & 255) * keep) << shift;
        return result;
    }
    private static void prune() {
        if (textures.size() <= 64) return;
        long now = tick(); var manager = Minecraft.getInstance().getTextureManager();
        for (var iterator = textures.values().iterator(); iterator.hasNext() && textures.size() > 64;) {
            var entry = iterator.next();
            if (entry.tick() < now - 2) { manager.release(entry.texture()); iterator.remove(); }
        }
    }
    private static int[] read(ResourceManager resources, Identifier location, int width, int height) {
        try (var stream = resources.getResourceOrThrow(location).open(); var image = NativeImage.read(stream)) {
            if (image.getWidth() != width || image.getHeight() != height)
                throw new IllegalArgumentException(location + " must be " + width + "x" + height);
            return image.getPixels();
        } catch (Exception e) { throw new IllegalStateException("Unreadable resident texture " + location, e); }
    }
    public static void register() {
        ResourceLoader.get(PackType.CLIENT_RESOURCES).registerReloadListener(id("outfit_bodies"), new SimplePreparableReloadListener<Loaded>() {
            @Override protected Loaded prepare(ResourceManager resources, ProfilerFiller profiler) {
                var loadedBodies = new ArrayList<int[]>();
                for (int skin = 0; skin < 6; skin++) loadedBodies.add(read(resources, id("textures/body/" + skin + ".png"), 64, 64));
                var loadedArt = new HashMap<String, int[]>();
                for (var garment : Wardrobe.ALL) {
                    int[] pixels = read(resources, id("wardrobe/" + garment.texture()), 64, 64 + garment.extrasHeight());
                    int[] codes = new int[pixels.length];
                    for (int i = 0; i < pixels.length; i++) codes[i] = Wardrobe.code(pixels[i]);
                    loadedArt.put(garment.id(), codes);
                }
                return new Loaded(List.copyOf(loadedBodies), Map.copyOf(loadedArt));
            }
            @Override protected void apply(Loaded loaded, ResourceManager resources, ProfilerFiller profiler) {
                clear(); bodies = loaded.bodies(); art = loaded.art();
            }
        });
        ClientTickEvents.END_CLIENT_TICK.register(client -> prune());
        net.fabricmc.fabric.api.client.networking.v1.ClientPlayConnectionEvents.DISCONNECT.register((handler, client) -> client.execute(ResidentSkins::clear));
    }
    private ResidentSkins() {}
}
