package dev.villagefriends.outfit;

import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

public final class FemaleBottomRegistry {
    public enum Family { HIGH_WAIST_SKIRT, LAYERED_LONG_DRESS, FITTED_TROUSERS, PLEATED_SKIRT, WRAP_ROBE_BOTTOM }
    public record Entry(String id, String name, Family family, Set<OutfitStyle> styles, int length,
                        int variant, String maskId, MaterialMask materials, BottomGarment model) {}
    public static final List<Entry> ALL = RegistrySource.FEMALE.rows("FemaleBottomRegistry","f_bottom_",7).stream().map(row -> {
        String id=RegistrySource.string(row,0), name=RegistrySource.string(row,1);
        var family=Family.valueOf(RegistrySource.string(row,2));
        var styles=row.get(3).getAsJsonArray().asList().stream().map(s->OutfitStyle.valueOf(s.getAsString())).collect(Collectors.toUnmodifiableSet());
        int length=RegistrySource.integer(row,4), variant=RegistrySource.integer(row,5);
        String maskId=RegistrySource.string(row,6); var mask=RegistrySource.FEMALE.material(maskId);
        return new Entry(id,name,family,styles,length,variant,maskId,mask,FemaleGeometry.bottom(id,family,styles,length,variant,mask));
    }).toList();
    public static final List<BottomGarment> MODELS = ALL.stream().map(Entry::model).toList();
    private FemaleBottomRegistry() {}
}
