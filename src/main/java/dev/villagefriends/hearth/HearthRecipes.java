package dev.villagefriends.hearth;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.FileToIdConverter;
import net.minecraft.resources.Identifier;
import net.minecraft.server.packs.resources.ResourceManager;
import net.minecraft.server.packs.resources.SimpleJsonResourceReloadListener;
import net.minecraft.util.profiling.ProfilerFiller;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Loads station recipes from data packs: {@code data/<namespace>/hearth_recipe/<name>.json}. Recipes that need
 * another mod carry {@code fabric:load_conditions} and are skipped without it.
 *
 * <pre>{"station": "pot", "ingredients": ["villagefriends:onion", "#villagefriends:cooking/fish"],
 *  "vessel": "minecraft:bowl", "result": {"id": "villagefriends:fishermans_stew", "count": 1}, "time": 240, "secret": false}</pre>
 */
public final class HearthRecipes extends SimpleJsonResourceReloadListener<HearthRecipes.Json> {
    private static final Logger LOGGER = LoggerFactory.getLogger("Hearth & Harvest");

    record Result(String id, int count) {
        static final Codec<Result> CODEC = RecordCodecBuilder.create(i -> i.group(
                Codec.STRING.fieldOf("id").forGetter(Result::id), Codec.INT.optionalFieldOf("count", 1).forGetter(Result::count)).apply(i, Result::new));
    }
    record Json(String station, List<String> ingredients, Optional<String> vessel, Result result, int time, boolean secret) {
        static final Codec<Json> CODEC = RecordCodecBuilder.create(i -> i.group(
                Codec.STRING.fieldOf("station").forGetter(Json::station),
                Codec.STRING.listOf().fieldOf("ingredients").forGetter(Json::ingredients),
                Codec.STRING.optionalFieldOf("vessel").forGetter(Json::vessel),
                Result.CODEC.fieldOf("result").forGetter(Json::result),
                Codec.INT.optionalFieldOf("time", 200).forGetter(Json::time),
                Codec.BOOL.optionalFieldOf("secret", false).forGetter(Json::secret)).apply(i, Json::new));
    }

    HearthRecipes() { super(Json.CODEC, FileToIdConverter.json("hearth_recipe")); }

    @Override protected void apply(Map<Identifier, Json> found, ResourceManager manager, ProfilerFiller profiler) {
        var recipes = new ArrayList<CookingRecipe>();
        for (var entry : found.entrySet()) {
            var j = entry.getValue();
            try {
                if (!BuiltInRegistries.ITEM.containsKey(Identifier.parse(j.result().id()))) { LOGGER.warn("Recipe {} makes unknown item {}", entry.getKey(), j.result().id()); continue; }
                recipes.add(new CookingRecipe(entry.getKey().toString(), Station.byId(j.station()), j.ingredients(), j.vessel().orElse(null),
                        j.result().id(), j.result().count(), j.time(), j.secret()));
            } catch (IllegalArgumentException e) {
                LOGGER.warn("Skipping recipe {}: {}", entry.getKey(), e.getMessage());
            }
        }
        Cookbook.load(recipes);
        LOGGER.info("Hearth & Harvest: {} station recipes", recipes.size());
    }
}
