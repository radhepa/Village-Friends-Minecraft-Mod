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

/** Bakes per-face grain, clothing overlap occlusion and hair-fringe shadows to palette-locked textures. */
public final class ResidentSkins {
    private record Entry(Identifier texture, long tick) {}
    private static final LinkedHashMap<String, Entry> textures = new LinkedHashMap<>(64, .75F, true);
    private static final LinkedHashMap<String, Outfit> outfits = new LinkedHashMap<>(256, .75F, true);
    private static List<int[]> bodies = List.of();
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
        var look = look(recipe); var outfit = outfit(recipe, profession);
        String key = look.complexion() + "_" + look.palette() + "_" + Integer.toHexString(outfit.hairRgb())
            + "_"+outfit.hair().id()+"_"+outfit.top().id()+"_"+outfit.bottom().id();
        var previous = textures.get(key);
        if (previous != null) {
            textures.put(key, new Entry(previous.texture(), tick()));
            return previous.texture();
        }
        if (bodies.size() != 6) return id("textures/body/0.png");
        var image = new NativeImage(OutfitAtlas.WIDTH, OutfitAtlas.HEIGHT, true);
        var body = bodies.get(look.complexion());
        for (int y = 0; y < 64; y++) for (int x = 0; x < 64; x++) image.setPixel(x, y, body[y * 64 + x]);
        var selected=OutfitAtlas.ENTRIES.stream().filter(e->e.selected(outfit)).toList();
        var occluders=selected.stream().map(OutfitAtlas.Entry::box).toList();
        for (var entry:selected) bake(image,entry,outfit,occluders);
        var face=new VoxelBox("face_shadow",BodyPart.HEAD,0,-4,-8,-4,8,8,8,0);
        for (int y=8;y<13;y++) for (int x=8;x<16;x++) {
            if (FaceDetails.protectedUv(x,y)) continue;
            float shadow=SurfaceTexture.occlusion(face,SurfaceTexture.Face.FRONT,(x-8+.5F)/8,(y-8+.5F)/8,outfit.hair().voxels());
            if (shadow>0) image.setPixel(x,y,SurfaceTexture.hsv(image.getPixel(x,y),1,1,1-shadow));
        }
        image.setPixel(FaceDetails.BROW_U,FaceDetails.V,FaceDetails.brow(outfit.hairRgb()));
        image.setPixel(FaceDetails.LASH_U,FaceDetails.V,FaceDetails.lash(outfit.hairRgb()));
        image.setPixel(FaceDetails.SOCKET_U,FaceDetails.V,FaceDetails.shadow(body[12*64+12]));
        image.setPixel(FaceDetails.CHIN_U,FaceDetails.V,FaceDetails.shadow(body[15*64+12]));
        Identifier texture = id("generated/" + key.toLowerCase(Locale.ROOT));
        Minecraft.getInstance().getTextureManager().register(texture, new DynamicTexture(() -> "Outfit " + key, image));
        textures.put(key, new Entry(texture, tick()));
        return texture;
    }
    private static void prune() {
        if (textures.size() <= 64) return;
        long now = tick(); var manager = Minecraft.getInstance().getTextureManager();
        for (var iterator = textures.values().iterator(); iterator.hasNext() && textures.size() > 64;) {
            var entry = iterator.next();
            if (entry.tick() < now - 2) { manager.release(entry.texture()); iterator.remove(); }
        }
    }
    private static void bake(NativeImage image,OutfitAtlas.Entry e,Outfit outfit,List<VoxelBox> occluders) {
        int w=e.tw(),h=e.th(),d=e.td();
        paint(image,e,outfit,occluders,SurfaceTexture.Face.TOP,d,0,w,d);
        paint(image,e,outfit,occluders,SurfaceTexture.Face.BOTTOM,d+w,0,w,d);
        paint(image,e,outfit,occluders,SurfaceTexture.Face.LEFT,0,d,d,h);
        paint(image,e,outfit,occluders,SurfaceTexture.Face.FRONT,d,d,w,h);
        paint(image,e,outfit,occluders,SurfaceTexture.Face.RIGHT,d+w,d,d,h);
        paint(image,e,outfit,occluders,SurfaceTexture.Face.BACK,d+w+d,d,w,h);
    }
    private static void paint(NativeImage image,OutfitAtlas.Entry e,Outfit outfit,List<VoxelBox> occluders,
                               SurfaceTexture.Face face,int offsetX,int offsetY,int width,int height) {
        var material=SurfaceTexture.material(e.box().id(),e.mask()==null);
        int seed=(e.modelId()+":"+e.box().id()).hashCode();
        for (int y=0;y<height;y++) for (int x=0;x<width;x++) {
            float u=(x+.5F)/width,v=(y+.5F)/height;
            int base=e.mask()==null?0xFF000000|outfit.hairRgb():e.mask().argb(Math.min(e.mask().width()-1,(int)(u*e.mask().width())),
                Math.min(e.mask().height()-1,(int)(v*e.mask().height())),outfit.palette());
            if (e.box().id().contains("boot")) base=SurfaceTexture.hsv(base,1,1,.72F);
            float shadow=SurfaceTexture.occlusion(e.box(),face,u,v,occluders);
            image.setPixel(e.u()+offsetX+x,e.v()+offsetY+y,SurfaceTexture.pixel(base,material,x,y,seed,shadow,face));
        }
    }
    public static void register() {
        ResourceLoader.get(PackType.CLIENT_RESOURCES).registerReloadListener(id("outfit_bodies"), new SimplePreparableReloadListener<List<int[]>>() {
            @Override protected List<int[]> prepare(ResourceManager resources, ProfilerFiller profiler) {
                var result = new ArrayList<int[]>();
                for (int skin = 0; skin < 6; skin++) {
                    try (var stream = resources.getResourceOrThrow(id("textures/body/" + skin + ".png")).open();
                         var image = NativeImage.read(stream)) {
                        if (image.getWidth() != 64 || image.getHeight() != 64) throw new IllegalArgumentException("Expected 64x64 body");
                        result.add(image.getPixels());
                    } catch (Exception e) { throw new IllegalStateException("Missing resident body " + skin, e); }
                }
                return List.copyOf(result);
            }
            @Override protected void apply(List<int[]> loaded, ResourceManager resources, ProfilerFiller profiler) { clear(); bodies = loaded; }
        });
        ClientTickEvents.END_CLIENT_TICK.register(client -> prune());
        net.fabricmc.fabric.api.client.networking.v1.ClientPlayConnectionEvents.DISCONNECT.register((handler, client) -> client.execute(ResidentSkins::clear));
    }
    private ResidentSkins() {}
}
