package dev.villagefriends.stable.data;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * The breed and gear tables, parsed from the JSON {@code tools/stablehand} writes
 * ({@code /data/villagefriends/villagefriends/stablehand/breeds.json} and {@code gear.json} on the classpath).
 * Pure: Gson only, no Minecraft classes, so unit tests read the same files the game does. Every row keeps its
 * {@code raw} JSON object, so a feature can read a key the schema does not name without a schema change.
 */
public final class StableTable {
    /** An inclusive stat range. */
    public record Range(double min, double max) {
        public double width() { return max - min; }
    }
    /** Where a breed is picked: a biome keyword ("plains", "any"...) and its weight. */
    public record Spawn(String biome, int weight) {}
    /** An extra natural spawn group in biomes vanilla gives no horses. */
    public record ExtraSpawn(String biome, int weight, int min, int max) {}
    public record Breed(String id, Range health, Range speed, Range jump, List<Spawn> spawns, List<ExtraSpawn> extraSpawns,
                        List<String> markings, int coats, List<String> village, JsonObject raw) {}
    /** One gear item: barding (BODY slot, armor numbers) or tack (SADDLE slot, pack columns, bond and calm). */
    public record Gear(String id, String kind, String slot, List<String> animals, int defense, float toughness, float knockback,
                       int enchantability, String repair, boolean dyeable, int undyed, int columns, double bondRide, int calm, JsonObject raw) {
        public boolean barding() { return kind.equals("barding"); }
        public boolean tack() { return kind.equals("tack"); }
    }
    /** The jousting lance: Item.Properties.spear arguments in order, then the six AttackRange numbers. */
    public record Lance(String id, String material, float attackDuration, float damageMultiplier, float delay, float dismountTime,
                        float dismountThreshold, float knockbackTime, float knockbackThreshold, float damageTime, float damageThreshold,
                        float[] reach) {}
    public record Tables(List<Breed> breeds, List<Gear> gear, Lance lance) {}

    private static final String ROOT = "/data/villagefriends/villagefriends/stablehand/";
    private static volatile Tables tables;

    /** Reads both tables from the classpath once (later calls return the same tables). */
    public static Tables load() {
        if (tables != null) return tables;
        try (InputStream breeds = open("breeds.json"); InputStream gear = open("gear.json")) {
            tables = parse(new InputStreamReader(breeds, StandardCharsets.UTF_8), new InputStreamReader(gear, StandardCharsets.UTF_8));
        } catch (IOException e) {
            throw new IllegalStateException("Could not read the Stablehand tables", e);
        }
        return tables;
    }
    private static InputStream open(String name) {
        var in = StableTable.class.getResourceAsStream(ROOT + name);
        if (in == null) throw new IllegalStateException(ROOT + name + " is missing (run tools/stablehand/stablehand.py)");
        return in;
    }

    /** Parses the two tables (pure; tests call it with any reader). */
    public static Tables parse(Reader breedsJson, Reader gearJson) {
        var breeds = new ArrayList<Breed>();
        for (var e : JsonParser.parseReader(breedsJson).getAsJsonObject().getAsJsonArray("breeds")) {
            var o = e.getAsJsonObject();
            var spawns = new ArrayList<Spawn>();
            for (var s : array(o, "spawns")) spawns.add(new Spawn(s.getAsJsonObject().get("biome").getAsString(), s.getAsJsonObject().get("weight").getAsInt()));
            var extra = new ArrayList<ExtraSpawn>();
            for (var s : array(o, "extra_spawns")) {
                var x = s.getAsJsonObject();
                extra.add(new ExtraSpawn(x.get("biome").getAsString(), x.get("weight").getAsInt(), x.get("min").getAsInt(), x.get("max").getAsInt()));
            }
            breeds.add(new Breed(o.get("id").getAsString(), range(o, "health"), range(o, "speed"), range(o, "jump"), List.copyOf(spawns),
                    List.copyOf(extra), strings(o, "markings"), o.has("coats") ? o.get("coats").getAsInt() : 1, strings(o, "village"), o));
        }
        var root = JsonParser.parseReader(gearJson).getAsJsonObject();
        var gear = new ArrayList<Gear>();
        for (var e : root.getAsJsonArray("gear")) {
            var o = e.getAsJsonObject();
            gear.add(new Gear(o.get("id").getAsString(), o.get("kind").getAsString(), o.get("slot").getAsString(), strings(o, "animals"),
                    integer(o, "defense"), (float) number(o, "toughness", 0), (float) number(o, "knockback", 0), integer(o, "enchantability"),
                    o.has("repair") ? o.get("repair").getAsString() : "", o.has("dyeable") && o.get("dyeable").getAsBoolean(), integer(o, "undyed"),
                    integer(o, "columns"), number(o, "bond_ride", 1), integer(o, "calm"), o));
        }
        var l = root.getAsJsonObject("lance");
        var reachArray = l.getAsJsonArray("reach");
        float[] reach = new float[reachArray.size()];
        for (int i = 0; i < reach.length; i++) reach[i] = reachArray.get(i).getAsFloat();
        var lance = new Lance(l.get("id").getAsString(), l.get("material").getAsString(), f(l, "attack_duration"), f(l, "damage_multiplier"),
                f(l, "delay"), f(l, "dismount_time"), f(l, "dismount_threshold"), f(l, "knockback_time"), f(l, "knockback_threshold"),
                f(l, "damage_time"), f(l, "damage_threshold"), reach);
        return new Tables(List.copyOf(breeds), List.copyOf(gear), lance);
    }

    public static List<Breed> breeds() { return load().breeds(); }
    public static Optional<Breed> breed(String id) { return breeds().stream().filter(b -> b.id().equals(id)).findFirst(); }
    public static List<Gear> gear() { return load().gear(); }
    public static Optional<Gear> gear(String id) { return gear().stream().filter(g -> g.id().equals(id)).findFirst(); }
    public static Lance lance() { return load().lance(); }
    /** Breeds by id, in table order. */
    public static Map<String, Breed> breedsById() {
        var map = new LinkedHashMap<String, Breed>();
        for (var b : breeds()) map.put(b.id(), b);
        return map;
    }

    private static JsonArray array(JsonObject o, String key) { return o.has(key) ? o.getAsJsonArray(key) : new JsonArray(); }
    private static List<String> strings(JsonObject o, String key) {
        var out = new ArrayList<String>();
        for (JsonElement e : array(o, key)) out.add(e.getAsString());
        return List.copyOf(out);
    }
    private static Range range(JsonObject o, String key) {
        var a = o.getAsJsonArray(key);
        return new Range(a.get(0).getAsDouble(), a.get(1).getAsDouble());
    }
    private static int integer(JsonObject o, String key) { return o.has(key) ? o.get(key).getAsInt() : 0; }
    private static double number(JsonObject o, String key, double fallback) { return o.has(key) ? o.get(key).getAsDouble() : fallback; }
    private static float f(JsonObject o, String key) { return o.get(key).getAsFloat(); }

    private StableTable() {}
}
