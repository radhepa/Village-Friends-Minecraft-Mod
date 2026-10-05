package dev.villagefriends.outfit;

import java.util.Objects;

/** The mask uses normalized face UVs on all six solid faces; no embedded garment RGB. */
public record MaskedVoxel(VoxelBox geometry, RoleMask mask) {
    public MaskedVoxel { Objects.requireNonNull(geometry, "geometry"); Objects.requireNonNull(mask, "mask"); }
}
