package dev.villagefriends.outfit;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.*;

/**
 * The compiled wardrobe ({@code tools/wardrobe/wardrobe.py} output): hairstyles, tops, bottoms,
 * outfit templates per profession, master palettes, hair colors and the key-color table.
 * Loaded once from the mod's own resources so client and server agree on every choice.
 */
public final class Wardrobe {
    public static final String ROLE_LETTERS = "PSALMKH";
    public static final int HAIR_ROLE = 6, SHADES = 5, TRANSPARENT = -1, SHADOW_LIGHT = 40, SHADOW_DEEP = 41;
    private static final String ROOT = "/assets/villagefriends/wardrobe/";

    public record OutfitTemplate(String id, String name, Garment top, Garment bottom) {}

    public static final List<Garment> HAIR, TOPS, BOTTOMS, ALL;
    public static final List<OutfitTemplate> OUTFITS;
    public static final List<HairColor> HAIR_COLORS;
    static final Map<PaletteID, ColorPalette> PALETTES;
    private static final Map<String, Garment> BY_ID;
    private static final Map<Profession, List<OutfitTemplate>> BY_PROFESSION;
    private static final Map<Integer, Integer> KEY_CODES;
    private static final int[] SHADOW_ALPHA = new int[2];

    static {
        try {
            var catalog = read("catalog.json");
            if (catalog.get("schemaVersion").getAsInt() != 1) throw new IllegalArgumentException("Unsupported wardrobe schema");
            var keys = new HashMap<Integer, Integer>();
            for (var entry : catalog.getAsJsonObject("keys").entrySet()) {
                String key = entry.getKey();
                int role = ROLE_LETTERS.indexOf(key.charAt(0)), shade = key.charAt(1) - '0';
                if (key.length() != 2 || role < 0 || shade < 0 || shade >= SHADES) throw new IllegalArgumentException("Invalid key " + key);
                if (keys.put(0xFF000000 | rgb(entry.getValue().getAsString()), role * SHADES + shade) != null)
                    throw new IllegalArgumentException("Duplicate key color " + key);
            }
            if (keys.size() != ROLE_LETTERS.length() * SHADES) throw new IllegalArgumentException("Incomplete key table");
            var shadows = catalog.getAsJsonObject("shadowKeys");
            SHADOW_ALPHA[0] = shadows.get("X1").getAsInt(); SHADOW_ALPHA[1] = shadows.get("X2").getAsInt();
            keys.put(SHADOW_ALPHA[0] << 24, SHADOW_LIGHT); keys.put(SHADOW_ALPHA[1] << 24, SHADOW_DEEP);
            KEY_CODES = Map.copyOf(keys);

            var byId = new LinkedHashMap<String, Garment>();
            HAIR = load(catalog.getAsJsonArray("hair"), "hair", Garment.Kind.HAIR, byId);
            TOPS = load(catalog.getAsJsonArray("tops"), "tops", Garment.Kind.TOP, byId);
            BOTTOMS = load(catalog.getAsJsonArray("bottoms"), "bottoms", Garment.Kind.BOTTOM, byId);
            if (HAIR.isEmpty() || TOPS.isEmpty() || BOTTOMS.isEmpty()) throw new IllegalArgumentException("Empty wardrobe");
            BY_ID = Collections.unmodifiableMap(byId);
            ALL = List.copyOf(byId.values());

            var outfits = new ArrayList<OutfitTemplate>(); var templateIds = new HashMap<String, OutfitTemplate>();
            for (var element : catalog.getAsJsonArray("outfits")) {
                var o = element.getAsJsonObject();
                var template = new OutfitTemplate(o.get("id").getAsString(), o.get("name").getAsString(),
                    require(o.get("top").getAsString(), Garment.Kind.TOP), require(o.get("bottom").getAsString(), Garment.Kind.BOTTOM));
                if (!compatible(template.top(), template.bottom())) throw new IllegalArgumentException("Incompatible template " + template.id());
                if (templateIds.put(template.id(), template) != null) throw new IllegalArgumentException("Duplicate outfit " + template.id());
                outfits.add(template);
            }
            OUTFITS = List.copyOf(outfits);
            var jobs = new EnumMap<Profession, List<OutfitTemplate>>(Profession.class);
            for (var entry : catalog.getAsJsonObject("professions").entrySet()) {
                var list = new ArrayList<OutfitTemplate>();
                for (var id : entry.getValue().getAsJsonArray()) {
                    var template = templateIds.get(id.getAsString());
                    if (template == null) throw new IllegalArgumentException("Unknown outfit " + id + " for " + entry.getKey());
                    list.add(template);
                }
                if (list.isEmpty()) throw new IllegalArgumentException("Profession without outfits: " + entry.getKey());
                jobs.put(Profession.valueOf(entry.getKey()), List.copyOf(list));
            }
            if (!jobs.containsKey(Profession.NONE)) throw new IllegalArgumentException("NONE needs outfits");
            BY_PROFESSION = Collections.unmodifiableMap(jobs);

            var palettes = new EnumMap<PaletteID, ColorPalette>(PaletteID.class);
            for (var entry : read("palettes.json").getAsJsonObject("palettes").entrySet()) {
                var p = entry.getValue().getAsJsonObject(); var ramps = new int[ColorPalette.ROLES][];
                for (int role = 0; role < ColorPalette.ROLES; role++)
                    ramps[role] = ramp(p.getAsJsonObject("ramps").getAsJsonArray(String.valueOf(ROLE_LETTERS.charAt(role))));
                var id = PaletteID.valueOf(entry.getKey());
                palettes.put(id, new ColorPalette(id, p.get("name").getAsString(), ramps));
            }
            if (palettes.size() != PaletteID.values().length) throw new IllegalArgumentException("Missing master palette");
            PALETTES = Collections.unmodifiableMap(palettes);

            var colors = new ArrayList<HairColor>();
            for (var entry : read("hair_colors.json").getAsJsonObject("colors").entrySet()) {
                var c = entry.getValue().getAsJsonObject();
                colors.add(new HairColor(entry.getKey(), c.get("name").getAsString(), ramp(c.getAsJsonArray("ramp"))));
            }
            if (colors.isEmpty()) throw new IllegalArgumentException("No hair colors");
            HAIR_COLORS = List.copyOf(colors);
        } catch (Exception e) { throw new ExceptionInInitializerError(e); }
    }

    private static JsonObject read(String path) throws Exception {
        try (var input = Wardrobe.class.getResourceAsStream(ROOT + path)) {
            if (input == null) throw new IllegalStateException("Wardrobe resource missing: " + path);
            return JsonParser.parseReader(new InputStreamReader(input, StandardCharsets.UTF_8)).getAsJsonObject();
        }
    }
    private static int rgb(String hex) {
        if (!hex.matches("#[0-9a-fA-F]{6}")) throw new IllegalArgumentException("Expected #rrggbb: " + hex);
        return Integer.parseInt(hex.substring(1), 16);
    }
    private static int[] ramp(JsonArray array) {
        if (array.size() != SHADES) throw new IllegalArgumentException("Ramps have five shades");
        int[] ramp = new int[SHADES];
        for (int i = 0; i < SHADES; i++) ramp[i] = rgb(array.get(i).getAsString());
        return ramp;
    }
    private static Set<String> strings(JsonObject o, String field) {
        var set = new HashSet<String>();
        for (var e : o.getAsJsonArray(field)) set.add(e.getAsString());
        return set;
    }
    private static Piece.Vec3 vec(JsonObject o, String field, Piece.Vec3 fallback) {
        var a = o.getAsJsonArray(field);
        if (a == null) return fallback;
        if (a.size() != 3) throw new IllegalArgumentException("Expected [x,y,z] for " + field);
        return new Piece.Vec3(a.get(0).getAsFloat(), a.get(1).getAsFloat(), a.get(2).getAsFloat());
    }
    private static List<Garment> load(JsonArray ids, String dir, Garment.Kind kind, Map<String, Garment> byId) throws Exception {
        var list = new ArrayList<Garment>();
        for (var element : ids) {
            String id = element.getAsString();
            var o = read(dir + "/" + id + ".json");
            if (!o.get("id").getAsString().equals(id) || !o.get("kind").getAsString().equals(kind.name().toLowerCase(Locale.ROOT)))
                throw new IllegalArgumentException("Garment definition mismatch: " + id);
            var pieces = new ArrayList<Piece>();
            for (var p : o.getAsJsonArray("pieces")) {
                var po = p.getAsJsonObject(); var size = po.getAsJsonArray("size"); var uv = po.getAsJsonArray("uv");
                pieces.add(new Piece(po.get("id").getAsString(), BodyPart.valueOf(po.get("bone").getAsString()),
                    vec(po, "pivot", Piece.Vec3.ZERO), vec(po, "rotation", Piece.Vec3.ZERO), vec(po, "origin", Piece.Vec3.ZERO),
                    size.get(0).getAsInt(), size.get(1).getAsInt(), size.get(2).getAsInt(), uv.get(0).getAsInt(), uv.get(1).getAsInt(),
                    po.has("inflate") ? po.get("inflate").getAsFloat() : 0,
                    po.has("motion") ? Piece.Motion.valueOf(po.get("motion").getAsString().toUpperCase(Locale.ROOT)) : Piece.Motion.NONE,
                    vec(po, "scale", Piece.Vec3.ONE)));
            }
            var garment = new Garment(id, kind, o.get("name").getAsString(), o.get("texture").getAsString(), o.get("extrasHeight").getAsInt(),
                strings(o, "tags"), strings(o, "requires"), strings(o, "rejects"),
                o.has("tucked") && o.get("tucked").getAsBoolean(), o.has("coversWaist") && o.get("coversWaist").getAsBoolean(), pieces);
            if (byId.put(id, garment) != null) throw new IllegalArgumentException("Duplicate garment " + id);
            list.add(garment);
        }
        return List.copyOf(list);
    }
    private static Garment require(String id, Garment.Kind kind) {
        var garment = BY_ID.get(id);
        if (garment == null || garment.kind() != kind) throw new IllegalArgumentException("Unknown " + kind + " " + id);
        return garment;
    }

    public static Garment get(String id) {
        var garment = BY_ID.get(id);
        if (garment == null) throw new IllegalArgumentException("Unknown garment " + id);
        return garment;
    }
    public static OutfitTemplate template(String id) {
        return OUTFITS.stream().filter(t -> t.id().equals(id)).findFirst().orElseThrow(() -> new IllegalArgumentException("Unknown outfit " + id));
    }
    public static HairColor hairColor(String id) {
        return HAIR_COLORS.stream().filter(c -> c.id().equals(id)).findFirst().orElseThrow(() -> new IllegalArgumentException("Unknown hair color " + id));
    }
    /** Outfit templates for a profession, preferred first; unknown jobs dress like the unemployed. */
    public static List<OutfitTemplate> templates(Profession job) {
        return BY_PROFESSION.getOrDefault(Objects.requireNonNull(job, "profession"), BY_PROFESSION.get(Profession.NONE));
    }
    /** Sims-style mixing: any pair works unless a tag rule (armor, fancy hose...) forbids it. */
    public static boolean compatible(Garment top, Garment bottom) {
        if (top.kind() != Garment.Kind.TOP || bottom.kind() != Garment.Kind.BOTTOM) return false;
        if (!Collections.disjoint(top.rejects(), bottom.tags()) || !Collections.disjoint(bottom.rejects(), top.tags())) return false;
        if (!top.requires().isEmpty() && Collections.disjoint(top.requires(), bottom.tags())) return false;
        return bottom.requires().isEmpty() || !Collections.disjoint(bottom.requires(), top.tags());
    }
    public static List<Garment> bottomsFor(Garment top) { return BOTTOMS.stream().filter(b -> compatible(top, b)).toList(); }

    /** Key code for one texel: role * 5 + shade, a shadow code, or {@link #TRANSPARENT}. */
    public static int code(int argb) {
        if ((argb >>> 24) == 0) return TRANSPARENT;
        var code = KEY_CODES.get(argb);
        if (code == null) throw new IllegalArgumentException("Not a wardrobe key color: #" + Integer.toHexString(argb));
        return code;
    }
    public static int shadowAlpha(int code) { return SHADOW_ALPHA[code - SHADOW_LIGHT]; }
    public static boolean shadow(int code) { return code == SHADOW_LIGHT || code == SHADOW_DEEP; }

    private Wardrobe() {}
}
