package dev.villagefriends.client;

import dev.villagefriends.VillageFriends;
import dev.villagefriends.pet.PetTrick;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;
import net.fabricmc.fabric.api.resource.v1.ResourceLoader;
import net.minecraft.resources.Identifier;
import net.minecraft.server.packs.PackType;
import net.minecraft.server.packs.resources.ResourceManager;
import net.minecraft.server.packs.resources.SimplePreparableReloadListener;
import net.minecraft.util.profiling.ProfilerFiller;

/** Loads every {@code assets/<namespace>/pet_tricks/*.json}; later files replace tricks with the same species and id. */
public final class PetTricks {
    public static final String FOLDER = "pet_tricks";
    private static volatile Map<String, PetTrick> tricks = Map.of();

    public static PetTrick get(String species, String id) { return tricks.get(species + ":" + id); }
    public static Map<String, PetTrick> all() { return tricks; }

    public static void register() {
        ResourceLoader.get(PackType.CLIENT_RESOURCES).registerReloadListener(Identifier.fromNamespaceAndPath("villagefriends", FOLDER),
                new SimplePreparableReloadListener<Map<String, PetTrick>>() {
                    @Override protected Map<String, PetTrick> prepare(ResourceManager resources, ProfilerFiller profiler) { return load(resources); }
                    @Override protected void apply(Map<String, PetTrick> loaded, ResourceManager resources, ProfilerFiller profiler) {
                        tricks = loaded;
                        VillageFriends.LOGGER.info("Pet tricks: {}", loaded.size());
                    }
                });
    }
    static Map<String, PetTrick> load(ResourceManager resources) {
        var found = resources.listResources(FOLDER, id -> id.getPath().endsWith(".json"));
        var ids = new java.util.ArrayList<>(found.keySet());
        // The bundled file loads first so resource packs can replace its tricks.
        ids.sort(java.util.Comparator.comparing((Identifier id) -> !id.getNamespace().equals("villagefriends")).thenComparing(Identifier::toString));
        var all = new HashMap<String, PetTrick>();
        for (var id : ids) {
            try (var reader = found.get(id).open()) {
                all.putAll(PetTrick.parse(id.toString(), new String(reader.readAllBytes(), StandardCharsets.UTF_8)));
            } catch (Exception e) {
                VillageFriends.LOGGER.error("Skipping pet tricks {}: {}", id, e.getMessage());
            }
        }
        return Map.copyOf(all);
    }
    private PetTricks() {}
}
