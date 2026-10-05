package dev.villagefriends.outfit;

import java.util.List;

public final class MaleHairRegistry {
    public enum Geometry { MESSY_PARTED, SPIKY_LAYERED, LOW_PONYTAIL, SHAGGY_CROP, UNDERCUT_SWEEP }
    public record Entry(String id, String name, Geometry geometry, int voxelVolume, int strandLayerDepth,
                        HairModel model) {}
    public static final List<Entry> ALL = RegistrySource.MALE.rows("MaleHairRegistry", "m_hair_", 5).stream().map(row -> {
        String id=RegistrySource.string(row,0), name=RegistrySource.string(row,1);
        var shape=Geometry.valueOf(RegistrySource.string(row,2));
        int volume=RegistrySource.integer(row,3), depth=RegistrySource.integer(row,4);
        var model=MaleHairModels.get(id);
        if (volume<1 || volume>3 || depth!=model.voxels().stream().mapToInt(VoxelBox::depthLayer).max().orElseThrow())
            throw new IllegalArgumentException("Handcrafted hair metadata mismatch");
        return new Entry(id,name,shape,volume,depth,model);
    }).toList();
    public static final List<HairModel> MODELS = ALL.stream().map(Entry::model).toList();
    private MaleHairRegistry() {}
}
