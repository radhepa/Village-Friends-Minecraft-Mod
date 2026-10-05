package dev.villagefriends.outfit;

import java.util.List;
import java.util.Set;

public record BottomGarment(String id, Set<Gender> genders, Set<OutfitStyle> compatibleStyles,
                             List<ClothingLayer> layers) {
    public BottomGarment {
        ModelChecks.id(id); genders = ModelChecks.nonempty(genders, "bottom genders");
        compatibleStyles = ModelChecks.nonempty(compatibleStyles, "compatible styles");
        layers = ModelChecks.nonempty(layers, "bottom layers");
        ModelChecks.unique(layers.stream().map(ClothingLayer::id).toList());
        if (layers.stream().anyMatch(l -> l.slot() != LayerSlot.BOTTOM && l.slot() != LayerSlot.TRIM
            && l.slot() != LayerSlot.HARDWARE)) throw new IllegalArgumentException("Invalid bottom layer slot");
    }
}
