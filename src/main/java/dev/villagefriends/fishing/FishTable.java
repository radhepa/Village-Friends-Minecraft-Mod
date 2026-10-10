package dev.villagefriends.fishing;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Collection;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * The fish table: every fish by id and by item, the biome regions that tell a desert river from a taiga one, and
 * the words residents use for them in tall tales. Read once at start-up from {@code villagefriends/fishing/fish.json}
 * (compiled by {@code tools/fishing/fishing.py}); other features add fish with {@link FishingApi#registerFish}.
 * Pure, so the catches, tales and contests that read it can be unit-tested.
 */
public final class FishTable {
    private static final Map<String, Fish> BY_ID = new LinkedHashMap<>(), BY_ITEM = new LinkedHashMap<>();
    private static final Map<String, String> REGION_OF_BIOME = new LinkedHashMap<>(), REGION_WORDS = new LinkedHashMap<>();

    public static Collection<Fish> all() { return List.copyOf(BY_ID.values()); }
    public static Fish get(String id) { return BY_ID.get(id); }
    /** The fish an item is ("minecraft:cod", "villagefriends:pike"), or null. */
    public static Fish byItem(String item) { return BY_ITEM.get(item); }
    /** The region a biome belongs to ("minecraft:taiga" is "taiga"), or null for rivers, oceans and the rest. */
    public static String region(String biome) { return REGION_OF_BIOME.get(biome); }
    public static Set<String> regions() { return new LinkedHashSet<>(REGION_WORDS.keySet()); }
    /** "the plains", "the snowy north". */
    public static String regionWords(String region) { return REGION_WORDS.getOrDefault(region, "the wilds"); }

    public static synchronized void put(Fish fish) {
        BY_ID.put(fish.id(), fish);
        BY_ITEM.put(fish.item(), fish);
    }

    public static void load() {
        try (var in = FishTable.class.getResourceAsStream("/villagefriends/fishing/fish.json")) {
            if (in == null) throw new IllegalStateException("villagefriends/fishing/fish.json is missing");
            parse(new InputStreamReader(in, StandardCharsets.UTF_8));
        } catch (IOException e) {
            throw new IllegalStateException("Could not read the Tall Tales Fishing fish table", e);
        }
    }

    public static void parse(Reader reader) {
        JsonObject root = JsonParser.parseReader(reader).getAsJsonObject();
        for (var e : root.getAsJsonObject("regions").entrySet())
            for (var biome : e.getValue().getAsJsonArray()) REGION_OF_BIOME.put(biome.getAsString(), e.getKey());
        for (var e : root.getAsJsonObject("region_words").entrySet()) REGION_WORDS.put(e.getKey(), e.getValue().getAsString());
        for (var e : root.getAsJsonArray("fish")) {
            var o = e.getAsJsonObject();
            var size = o.getAsJsonArray("size");
            put(new Fish(o.get("id").getAsString(), o.get("item").getAsString(), o.get("name").getAsString(),
                    Fish.Rarity.byId(o.get("rarity").getAsString()), set(o.getAsJsonArray("water")), set(o.getAsJsonArray("region")),
                    set(o.getAsJsonArray("time")), o.get("weather").getAsString(), set(o.getAsJsonArray("season")),
                    size.get(0).getAsInt(), size.get(1).getAsInt(), Fish.Behavior.byId(o.get("behavior").getAsString()),
                    o.get("difficulty").getAsInt(), o.get("food").getAsInt(), o.get("saturation").getAsFloat(),
                    set(o.getAsJsonArray("flags")), o.get("text").getAsString()));
        }
    }
    private static Set<String> set(JsonArray a) {
        var out = new LinkedHashSet<String>();
        if (a != null) for (var e : a) out.add(e.getAsString());
        return Set.copyOf(out);
    }
    /** For tests: fish that bite here, in table order. */
    public static List<Fish> biting(Spot spot) {
        var out = new ArrayList<Fish>();
        for (var f : BY_ID.values()) if (f.bites(spot)) out.add(f);
        return out;
    }

    private FishTable() {}
}
