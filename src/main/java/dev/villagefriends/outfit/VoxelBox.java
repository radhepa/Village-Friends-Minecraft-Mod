package dev.villagefriends.outfit;

import java.util.Objects;

/** Bone-local model pixels (16 per block). Head bounds: [-4,4] x [-8,0] x [-4,4]. */
public record VoxelBox(String id, BodyPart bone, int depthLayer,
                       float x, float y, float z, float width, float height, float depth, float inflation) {
    public VoxelBox {
        if (id == null || !id.matches("[a-z0-9_]+")) throw new IllegalArgumentException("Invalid voxel id");
        Objects.requireNonNull(bone, "bone");
        if (depthLayer < 0 || depthLayer > 15) throw new IllegalArgumentException("Invalid depth layer");
        for (float value : new float[]{x, y, z, width, height, depth, inflation})
            if (!Float.isFinite(value)) throw new IllegalArgumentException("Non-finite geometry");
        if (width <= 0 || height <= 0 || depth <= 0 || inflation < 0)
            throw new IllegalArgumentException("Voxels require volume and nonnegative inflation");
        if (!Float.isFinite(x + width + inflation) || !Float.isFinite(y + height + inflation)
            || !Float.isFinite(z + depth + inflation) || !Float.isFinite(x - inflation)
            || !Float.isFinite(y - inflation) || !Float.isFinite(z - inflation))
            throw new IllegalArgumentException("Geometry bounds overflow");
    }

    public boolean outsideHead() {
        return x - inflation < -4 || y - inflation < -8 || z - inflation < -4
            || x + width + inflation > 4 || y + height + inflation > 0 || z + depth + inflation > 4;
    }
}
