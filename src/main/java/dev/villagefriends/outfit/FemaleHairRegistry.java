package dev.villagefriends.outfit;

import java.util.List;

public final class FemaleHairRegistry {
    public enum Geometry { NOBLE_BRAIDS, RELAXED_WAVY, ELEGANT_SIDE_BRAID, CROWN_BUN, MESSY_BOB,
        TWIN_BRAID, LONG_SWEEPING_LOCKS, BRAIDED_CROWN, FISHTAIL_BRAID, CURLY_CASCADE }
    public record Entry(String id, String name, Geometry geometry, int voxelVolume, int strandLayerDepth,
                        int backLength, int variant, HairModel model) {
        public boolean hoodCompatible() {
            return voxelVolume<=2 && (geometry==Geometry.MESSY_BOB || geometry==Geometry.ELEGANT_SIDE_BRAID
                || geometry==Geometry.FISHTAIL_BRAID);
        }
    }
    public static final List<Entry> ALL = RegistrySource.FEMALE.rows("FemaleHairRegistry","f_hair_",7).stream().map(row -> {
        String id=RegistrySource.string(row,0), name=RegistrySource.string(row,1);
        var shape=Geometry.valueOf(RegistrySource.string(row,2));
        int volume=RegistrySource.integer(row,3), depth=RegistrySource.integer(row,4), length=RegistrySource.integer(row,5),
            variant=RegistrySource.integer(row,6);
        return new Entry(id,name,shape,volume,depth,length,variant,FemaleGeometry.hair(id,shape,volume,depth,length,variant));
    }).toList();
    public static final List<HairModel> MODELS = ALL.stream().map(Entry::model).toList();
    private FemaleHairRegistry() {}
}
