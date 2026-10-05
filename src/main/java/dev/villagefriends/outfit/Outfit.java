package dev.villagefriends.outfit;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Objects;

/** One immutable palette owner. Every equipped layer is bound here, including hair ornaments. */
public final class Outfit {
    public final class EquippedLayer {
        private final ClothingLayer model;
        private EquippedLayer(ClothingLayer model) { this.model = model; }
        public ClothingLayer model() { return model; }
        public ColorPalette palette() { return Outfit.this.palette; }
        public int[] resolve(MaskedVoxel voxel) {
            if (!model.voxels().contains(voxel)) throw new IllegalArgumentException("Voxel is not in this layer");
            return voxel.mask().resolve(palette());
        }
    }

    private final Gender gender;
    private final Profession profession;
    private final ColorPalette palette;
    private final HairModel hair;
    private final int hairRgb;
    private final TopGarment top;
    private final BottomGarment bottom;
    private final List<EquippedLayer> layers;

    public Outfit(Gender gender, Profession profession, ColorPalette palette, HairModel hair,
                  int hairRgb, TopGarment top, BottomGarment bottom) {
        this.gender = Objects.requireNonNull(gender, "gender");
        this.profession = Objects.requireNonNull(profession, "profession");
        this.palette = Objects.requireNonNull(palette, "palette");
        this.hair = Objects.requireNonNull(hair, "hair");
        ColorPalette.requireRgb(hairRgb); this.hairRgb = hairRgb;
        this.top = Objects.requireNonNull(top, "top"); this.bottom = Objects.requireNonNull(bottom, "bottom");
        if (!hair.genders().contains(gender) || !top.genders().contains(gender) || !bottom.genders().contains(gender)
            || !bottom.compatibleStyles().contains(top.style())) throw new IllegalArgumentException("Incompatible outfit");
        var definitions = new ArrayList<ClothingLayer>();
        definitions.addAll(top.layers()); definitions.addAll(bottom.layers()); definitions.addAll(hair.ornaments());
        ModelChecks.unique(definitions.stream().map(ClothingLayer::id).toList());
        definitions.sort(Comparator.comparing(ClothingLayer::slot));
        layers = definitions.stream().map(EquippedLayer::new).toList();
    }

    public Gender gender() { return gender; }
    public Profession profession() { return profession; }
    public ColorPalette palette() { return palette; }
    public HairModel hair() { return hair; }
    public int hairRgb() { return hairRgb; }
    public TopGarment top() { return top; }
    public BottomGarment bottom() { return bottom; }
    public List<EquippedLayer> layers() { return layers; }
    public Outfit recolor(PaletteID id) {
        return new Outfit(gender, profession, MasterPalettes.get(id), hair, hairRgb, top, bottom);
    }
}
