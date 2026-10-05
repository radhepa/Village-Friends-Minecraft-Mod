package dev.villagefriends.outfit;

import java.util.List;
import java.util.Set;

/** Natural hair color is independent; ribbons and pins still use the outfit's four roles. */
public record HairModel(String id, Set<Gender> genders, List<VoxelBox> voxels, List<ClothingLayer> ornaments) {
    public HairModel {
        ModelChecks.id(id); genders = ModelChecks.nonempty(genders, "hair genders");
        voxels = ModelChecks.nonempty(voxels, "hair voxels"); ornaments = List.copyOf(ornaments);
        ModelChecks.unique(voxels.stream().map(VoxelBox::id).toList());
        ModelChecks.unique(ornaments.stream().map(ClothingLayer::id).toList());
        if (voxels.stream().anyMatch(v -> v.bone() != BodyPart.HEAD))
            throw new IllegalArgumentException("Hair must attach to the head");
        if (voxels.stream().noneMatch(v -> v.depthLayer() > 0 && v.outsideHead()))
            throw new IllegalArgumentException("Hair requires outer-layer volume beyond the head");
        if (ornaments.stream().anyMatch(l -> l.slot() != LayerSlot.HAIR_ORNAMENT
            || l.voxels().stream().anyMatch(v -> v.geometry().bone() != BodyPart.HEAD)))
            throw new IllegalArgumentException("Hair ornaments must be head-mounted ornament layers");
    }
}
