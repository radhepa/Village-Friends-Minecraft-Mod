package dev.villagefriends.outfit;

import java.util.List;
import java.util.Objects;
import java.util.Set;

public record TopGarment(String id, Set<Gender> genders, OutfitStyle style, List<ClothingLayer> layers) {
    public TopGarment {
        ModelChecks.id(id); genders = ModelChecks.nonempty(genders, "top genders");
        Objects.requireNonNull(style, "style"); layers = ModelChecks.nonempty(layers, "top layers");
        ModelChecks.unique(layers.stream().map(ClothingLayer::id).toList());
        if (layers.stream().anyMatch(l -> l.slot() == LayerSlot.BOTTOM || l.slot() == LayerSlot.HAIR_ORNAMENT))
            throw new IllegalArgumentException("Invalid top layer slot");
    }
}
