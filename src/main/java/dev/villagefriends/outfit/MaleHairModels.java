package dev.villagefriends.outfit;

import com.google.gson.*;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.*;

/** Five handwritten coordinate tables; loading never calculates or randomizes their shapes. */
public final class MaleHairModels {
    private static final Map<String,HairModel> MODELS;
    static {
        try (var input=MaleHairModels.class.getResourceAsStream("/assets/villagefriends/outfits/male-hair-models.json")) {
            if (input==null) throw new IllegalStateException("Handcrafted male hair models missing");
            var root=JsonParser.parseReader(new InputStreamReader(input,StandardCharsets.UTF_8)).getAsJsonObject();
            if (root.get("schemaVersion").getAsBigDecimal().intValueExact()!=1) throw new IllegalArgumentException("Unsupported hair model schema");
            float inflation=root.get("inflation").getAsFloat();
            var definitions=root.getAsJsonObject("models"); var models=new LinkedHashMap<String,HairModel>();
            if (definitions.size()!=5) throw new IllegalArgumentException("Exactly five handcrafted hairstyles required");
            for (var definition:definitions.entrySet()) {
                var voxels=new ArrayList<VoxelBox>();
                for (var data:definition.getValue().getAsJsonArray()) {
                    var row=data.getAsJsonArray();
                    if (row.size()!=8) throw new IllegalArgumentException("Invalid hair coordinate row");
                    voxels.add(new VoxelBox(row.get(0).getAsString(),BodyPart.HEAD,row.get(1).getAsBigDecimal().intValueExact(),
                        row.get(2).getAsFloat(),row.get(3).getAsFloat(),row.get(4).getAsFloat(),row.get(5).getAsFloat(),
                        row.get(6).getAsFloat(),row.get(7).getAsFloat(),inflation));
                }
                models.put(definition.getKey(),new HairModel(definition.getKey(),Set.of(Gender.MALE),voxels,List.of()));
            }
            MODELS=Map.copyOf(models);
        } catch (Exception exception) { throw new ExceptionInInitializerError(exception); }
    }
    public static HairModel get(String id) {
        var model=MODELS.get(id);
        if (model==null) throw new IllegalArgumentException("Unknown handcrafted male hair: "+id);
        return model;
    }
    private MaleHairModels() {}
}
