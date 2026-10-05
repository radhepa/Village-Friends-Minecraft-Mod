package dev.villagefriends.outfit;

import java.util.Arrays;
import java.util.List;
import java.util.Objects;

/** The ten master palettes (tools/wardrobe/palettes.json). One palette per outfit, no mixing. */
public final class MasterPalettes {
    public static final List<ColorPalette> ALL = Arrays.stream(PaletteID.values()).map(Wardrobe.PALETTES::get).toList();
    public static ColorPalette get(PaletteID id) { return Wardrobe.PALETTES.get(Objects.requireNonNull(id, "palette")); }
    private MasterPalettes() {}
}
