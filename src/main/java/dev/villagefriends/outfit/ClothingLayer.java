package dev.villagefriends.outfit;

import java.util.List;
import java.util.Objects;

/** Reusable color-free geometry. Equipped bindings, not definitions, hold the active palette. */
public record ClothingLayer(String id, LayerSlot slot, List<MaskedVoxel> voxels) {
    public ClothingLayer {
        ModelChecks.id(id); Objects.requireNonNull(slot, "slot");
        voxels = ModelChecks.nonempty(voxels, "clothing voxels");
        ModelChecks.unique(voxels.stream().map(v -> v.geometry().id()).toList());
    }
}
