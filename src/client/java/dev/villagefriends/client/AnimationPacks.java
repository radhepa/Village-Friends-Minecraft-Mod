package dev.villagefriends.client;

import dev.villagefriends.VillageFriends;
import dev.villagefriends.animation.AnimationLibrary;
import dev.villagefriends.animation.AnimationPack;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import net.fabricmc.fabric.api.resource.v1.ResourceLoader;
import net.minecraft.resources.Identifier;
import net.minecraft.server.packs.PackType;
import net.minecraft.server.packs.resources.ResourceManager;
import net.minecraft.server.packs.resources.SimplePreparableReloadListener;
import net.minecraft.util.profiling.ProfilerFiller;

/**
 * Loads every {@code assets/<namespace>/resident_animations/*.json} pack. A resource pack can replace
 * the bundled Village Life file or add new packs beside it; a broken pack is skipped with a log line.
 */
public final class AnimationPacks {
    public static final String FOLDER = "resident_animations";

    public static void register() {
        ResourceLoader.get(PackType.CLIENT_RESOURCES).registerReloadListener(
                Identifier.fromNamespaceAndPath("villagefriends", "resident_animations"),
                new SimplePreparableReloadListener<AnimationLibrary>() {
                    @Override protected AnimationLibrary prepare(ResourceManager resources, ProfilerFiller profiler) { return load(resources); }
                    @Override protected void apply(AnimationLibrary library, ResourceManager resources, ProfilerFiller profiler) {
                        AnimationLibrary.install(library);
                        VillageFriends.LOGGER.info("Resident animations: {} clips from {} pack(s)", library.clips().size(), library.packs().size());
                    }
                });
    }

    static AnimationLibrary load(ResourceManager resources) {
        var found = resources.listResources(FOLDER, id -> id.getPath().endsWith(".json"));
        var ids = new ArrayList<>(found.keySet());
        // The bundled pack loads first so other packs can replace or disable its clips.
        ids.sort(Comparator.comparing((Identifier id) -> !isBuiltin(id)).thenComparing(Identifier::toString));
        var packs = new ArrayList<AnimationPack>();
        for (var id : ids) {
            String file = id.getPath().substring(FOLDER.length() + 1, id.getPath().length() - 5);
            String packId = id.getNamespace().equals("villagefriends") ? file : id.getNamespace() + "." + file;
            try (var reader = found.get(id).open()) {
                packs.add(AnimationPack.parse(packId, new String(reader.readAllBytes(), StandardCharsets.UTF_8)));
            } catch (Exception e) {
                VillageFriends.LOGGER.error("Skipping resident animation pack {}: {}", id, e.getMessage());
            }
        }
        if (packs.isEmpty()) return AnimationLibrary.builtin();
        return new AnimationLibrary(List.copyOf(packs));
    }
    private static boolean isBuiltin(Identifier id) {
        return id.getNamespace().equals("villagefriends") && id.getPath().equals(FOLDER + "/" + AnimationLibrary.BUILTIN + ".json");
    }
    private AnimationPacks() {}
}
