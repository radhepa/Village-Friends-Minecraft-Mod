package dev.villagefriends.outfit;

import com.google.gson.*;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.*;

/** Compact JSON arrays are canonical; registry order and IDs are validated before model construction. */
final class RegistrySource {
    static final RegistrySource MALE = new RegistrySource("male-registry.json", Gender.MALE,5);
    static final RegistrySource FEMALE = new RegistrySource("female-registry.json", Gender.FEMALE,50);
    private final JsonObject root;
    private final Map<String, MaterialMask> masks;
    private final int itemCount;
    private RegistrySource(String resource, Gender gender,int itemCount) {
        this.itemCount=itemCount;
        try (var input = RegistrySource.class.getResourceAsStream("/assets/villagefriends/outfits/" + resource)) {
            if (input == null) throw new IllegalStateException(resource + " missing");
            root = JsonParser.parseReader(new InputStreamReader(input, StandardCharsets.UTF_8)).getAsJsonObject();
            if (root.get("schemaVersion").getAsBigDecimal().intValueExact() != 1
                || !root.get("gender").getAsString().equals(gender.name())) throw new IllegalArgumentException("Unsupported registry " + resource);
            var size = root.getAsJsonArray("maskSize"); var loaded = new HashMap<String, MaterialMask>();
            if (size.size() != 2) throw new IllegalArgumentException("Expected [width,height]");
            for (var named : root.getAsJsonObject("roleMasks").entrySet()) {
                var roles = new EnumMap<ColorRole, List<PixelBounds>>(ColorRole.class);
                for (var role : ColorRole.values()) {
                    var rects = new ArrayList<PixelBounds>();
                    for (var entry : named.getValue().getAsJsonObject().getAsJsonArray(role.name())) {
                        var b = entry.getAsJsonArray();
                        if (b.size() != 4) throw new IllegalArgumentException("Expected [x0,y0,x1,y1]");
                        rects.add(new PixelBounds(integer(b,0),integer(b,1),integer(b,2),integer(b,3)));
                    }
                    roles.put(role, rects);
                }
                loaded.put(named.getKey(), new MaterialMask(integer(size,0), integer(size,1), roles));
            }
            masks = Map.copyOf(loaded);
        } catch (Exception e) { throw new ExceptionInInitializerError(e); }
    }
    List<JsonArray> rows(String registry, String prefix, int columns) {
        var rows = root.getAsJsonArray(registry);
        if (rows == null || rows.size() != itemCount) throw new IllegalArgumentException("Expected " + itemCount + " " + registry + " items");
        var result = new ArrayList<JsonArray>();
        for (int i = 0; i < rows.size(); i++) {
            var row = rows.get(i).getAsJsonArray();
            if (row.size() != columns || !string(row,0).equals(prefix + String.format(Locale.ROOT,"%02d",i+1)))
                throw new IllegalArgumentException("Invalid registry row " + registry + ":" + i);
            if (string(row,1).isBlank()) throw new IllegalArgumentException("Missing asset name");
            result.add(row);
        }
        return List.copyOf(result);
    }
    static int integer(JsonArray row, int index) { return row.get(index).getAsBigDecimal().intValueExact(); }
    static String string(JsonArray row, int index) { return row.get(index).getAsString(); }
    MaterialMask material(String name) {
        var mask = masks.get(name);
        if (mask == null) throw new IllegalArgumentException("Unknown material mask " + name);
        return mask;
    }
}
