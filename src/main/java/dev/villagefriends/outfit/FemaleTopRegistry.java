package dev.villagefriends.outfit;

import java.util.List;

public final class FemaleTopRegistry {
    public enum Family { CORSET_VEST, EMPIRE_TOP, OFF_SHOULDER_BLOUSE, WRAP_TUNIC, HOODED_MANTLE, KNIT_SWEATER }
    public record Entry(String id, String name, Family family, OutfitStyle style, int length, int sleeveLength,
                        int variant, String maskId, MaterialMask materials, TopGarment model) {}
    public static final List<Entry> ALL = RegistrySource.FEMALE.rows("FemaleTopRegistry","f_top_",8).stream().map(row -> {
        String id=RegistrySource.string(row,0), name=RegistrySource.string(row,1);
        var family=Family.valueOf(RegistrySource.string(row,2)); var style=OutfitStyle.valueOf(RegistrySource.string(row,3));
        int length=RegistrySource.integer(row,4), sleeves=RegistrySource.integer(row,5), variant=RegistrySource.integer(row,6);
        String maskId=RegistrySource.string(row,7); var mask=RegistrySource.FEMALE.material(maskId);
        return new Entry(id,name,family,style,length,sleeves,variant,maskId,mask,FemaleGeometry.top(id,family,style,length,sleeves,variant,mask));
    }).toList();
    public static final List<TopGarment> MODELS = ALL.stream().map(Entry::model).toList();
    private FemaleTopRegistry() {}
}
