package dev.villagefriends.outfit;

import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;

public final class MasterPalettes {
    public static final List<ColorPalette> ALL = List.of(
        new ColorPalette(PaletteID.WASHED_INDIGO_AND_CREAM, "Washed Indigo & Cream", 0x647593, 0xE6DCC5, 0xB88663, 0xAA9873),
        new ColorPalette(PaletteID.FOREST_AND_HEARTH, "Forest & Hearth", 0x465D49, 0xD8C9AC, 0xB86D50, 0xA99467),
        new ColorPalette(PaletteID.SCHOLARLY_PLUM, "Scholarly Plum", 0x65506B, 0xD9D0BD, 0xA88955, 0xB7AD94),
        new ColorPalette(PaletteID.DESERT_SUN, "Desert Sun", 0xC29A55, 0xEEE0BD, 0xB96C42, 0x9D8353),
        new ColorPalette(PaletteID.ROYAL_VELVET, "Royal Velvet", 0x494866, 0xC9C7BE, 0x91465A, 0xBDA46A),
        new ColorPalette(PaletteID.RUSTIC_TWEED, "Rustic Tweed", 0x796E55, 0xDDD1B7, 0xA86F50, 0x94846A),
        new ColorPalette(PaletteID.TANNER_AMBER, "Tanner Amber", 0xA57643, 0xE1D1B0, 0x665044, 0xB7A077),
        new ColorPalette(PaletteID.WINTER_TUNDRA, "Winter Tundra", 0x879DA4, 0xE7E8DF, 0x596977, 0xBDC4C3),
        new ColorPalette(PaletteID.SAGE_AND_TERRACOTTA, "Sage & Terracotta", 0x8A9B7A, 0xE3D8BE, 0xB9775C, 0xB09A72),
        new ColorPalette(PaletteID.ASH_AND_TEAL, "Ash & Teal", 0x62676B, 0xD6D3C6, 0x518C89, 0xAAB1AD)
    );
    private static final Map<PaletteID, ColorPalette> BY_ID;
    static {
        var palettes = new EnumMap<PaletteID, ColorPalette>(PaletteID.class);
        for (var palette : ALL) {
            if (palettes.put(palette.id(), palette) != null) throw new IllegalStateException("Duplicate palette");
        }
        if (palettes.size() != PaletteID.values().length) throw new IllegalStateException("Missing master palette");
        BY_ID = Map.copyOf(palettes);
    }
    public static ColorPalette get(PaletteID id) { return BY_ID.get(Objects.requireNonNull(id, "palette")); }
    private MasterPalettes() {}
}
