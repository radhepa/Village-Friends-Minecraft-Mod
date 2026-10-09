package dev.villagefriends.hearth;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Collection;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * The dish table: every dish and kitchen ingredient by item id. Read once at start-up from
 * {@code villagefriends/hearth/dishes.json} (compiled by {@code tools/hearth/hearth.py}); other mods and
 * later features add rows with {@link HearthApi#registerDish}. Pure, so the tastes and menus that read it
 * can be unit-tested.
 */
public final class Dishes {
    public static final String NS = "villagefriends";
    /** A crop row: the produce item, its seed, and how filling the produce is raw. */
    public record Crop(String id, String seed, int food, float saturation, List<String> biomes) {}
    /** An ingredient that drops from a mob ({@code source}, "mod:mob"), with what eating it raw does ({@code effect} may be null). */
    public record Ingredient(String id, int food, float saturation, String effect, int effectSeconds, String needs, String source, int min, int max) {}
    /** The whole table as compiled. */
    public record Table(List<Crop> crops, List<Ingredient> ingredients, List<Dish> dishes) {}

    private static final Map<String, Dish> BY_ID = new LinkedHashMap<>();
    private static Table table = new Table(List.of(), List.of(), List.of());

    public static Table table() { return table; }
    public static Collection<Dish> all() { return List.copyOf(BY_ID.values()); }
    /** Real dishes only (no flour or butter). */
    public static List<Dish> meals() { return BY_ID.values().stream().filter(Dish::dish).toList(); }
    public static Dish get(String id) { return BY_ID.get(id); }
    public static boolean has(String id) { return BY_ID.containsKey(id); }

    /** Adds (or replaces) a row. */
    public static synchronized void put(Dish dish) { BY_ID.put(dish.id(), dish); }

    public static Table load() {
        try (var in = Dishes.class.getResourceAsStream("/villagefriends/hearth/dishes.json")) {
            if (in == null) throw new IllegalStateException("villagefriends/hearth/dishes.json is missing");
            table = parse(new InputStreamReader(in, StandardCharsets.UTF_8));
        } catch (IOException e) {
            throw new IllegalStateException("Could not read the Hearth & Harvest dish table", e);
        }
        for (var d : table.dishes()) put(d);
        return table;
    }

    public static Table parse(Reader reader) {
        JsonObject root = JsonParser.parseReader(reader).getAsJsonObject();
        var crops = new ArrayList<Crop>();
        for (var e : root.getAsJsonArray("crops")) {
            var o = e.getAsJsonObject();
            crops.add(new Crop(o.get("id").getAsString(), o.get("seed").getAsString(), o.get("food").getAsInt(), o.get("saturation").getAsFloat(),
                    strings(o.getAsJsonArray("biomes"))));
        }
        var ingredients = new ArrayList<Ingredient>();
        for (var e : root.getAsJsonArray("ingredients")) {
            var o = e.getAsJsonObject();
            var raw = o.get("raw_effect");
            boolean hasEffect = raw != null && raw.isJsonObject();
            ingredients.add(new Ingredient(o.get("id").getAsString(), o.get("food").getAsInt(), o.get("saturation").getAsFloat(),
                    hasEffect ? raw.getAsJsonObject().get("effect").getAsString() : null, hasEffect ? raw.getAsJsonObject().get("seconds").getAsInt() : 0,
                    string(o.get("needs")), o.get("source").getAsString(), o.getAsJsonArray("drops").get(0).getAsInt(), o.getAsJsonArray("drops").get(1).getAsInt()));
        }
        var dishes = new ArrayList<Dish>();
        for (var e : root.getAsJsonArray("dishes")) {
            var o = e.getAsJsonObject();
            dishes.add(new Dish(NS + ":" + o.get("id").getAsString(), Station.byId(o.get("station").getAsString()),
                    o.get("existing").getAsBoolean(), o.get("ingredient").getAsBoolean(), o.get("secret").getAsBoolean(), string(o.get("needs")),
                    o.get("food").getAsInt(), o.get("saturation").getAsFloat(), o.get("tier").getAsInt(), o.get("buff").getAsInt(),
                    o.get("serve").getAsString(), o.get("vessel").getAsString(), strings(o.getAsJsonArray("meals")), strings(o.getAsJsonArray("likes"))));
        }
        return new Table(List.copyOf(crops), List.copyOf(ingredients), List.copyOf(dishes));
    }
    private static String string(JsonElement e) { return e == null || e.isJsonNull() ? null : e.getAsString(); }
    private static List<String> strings(JsonArray a) {
        var out = new ArrayList<String>();
        for (var e : a) out.add(e.getAsString());
        return out;
    }

    private Dishes() {}
}
