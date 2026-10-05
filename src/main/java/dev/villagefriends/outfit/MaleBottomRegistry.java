package dev.villagefriends.outfit;

import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

public final class MaleBottomRegistry {
    public enum Family { LINEN_TROUSERS, HEAVY_TROUSERS, CUFFED_DENIM, TRAVEL_BREECHES, TAILORED_TROUSERS }
    public record Entry(String id, String name, Family family, Set<OutfitStyle> styles, int length,
                        int variant, String maskId, MaterialMask materials, BottomGarment model) {}
    public static final List<Entry> ALL = RegistrySource.MALE.rows("MaleBottomRegistry", "m_bottom_", 7).stream().map(row -> {
        String id=RegistrySource.string(row,0), name=RegistrySource.string(row,1);
        var family=Family.valueOf(RegistrySource.string(row,2));
        var styles=row.get(3).getAsJsonArray().asList().stream().map(s -> OutfitStyle.valueOf(s.getAsString())).collect(Collectors.toUnmodifiableSet());
        int length=RegistrySource.integer(row,4), variant=RegistrySource.integer(row,5);
        String maskId=RegistrySource.string(row,6); var materials=RegistrySource.MALE.material(maskId);
        return new Entry(id,name,family,styles,length,variant,maskId,materials,
            MaleGeometry.bottom(id,family,styles,length,variant,materials));
    }).toList();
    public static final List<BottomGarment> MODELS = ALL.stream().map(Entry::model).toList();
    private MaleBottomRegistry() {}
}
