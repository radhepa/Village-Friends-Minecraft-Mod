package dev.villagefriends.outfit;

import java.util.Objects;

/**
 * One master palette: five-shade ramps for primary (60%), secondary (30%), accent (10%),
 * and the materials leather, metal, ink and denim. Colors exist only here; garments carry
 * role/shade keys.
 */
public record ColorPalette(PaletteID id, String name, int[][] ramps) {
    public static final int PRIMARY = 0, SECONDARY = 1, ACCENT = 2, LEATHER = 3, METAL = 4, INK = 5, DENIM = 6, ROLES = 7;

    public ColorPalette {
        Objects.requireNonNull(id, "id");
        if (name == null || name.isBlank()) throw new IllegalArgumentException("Missing palette name");
        if (ramps == null || ramps.length != ROLES) throw new IllegalArgumentException("Palettes have seven role ramps");
        var copy = new int[ROLES][];
        for (int role = 0; role < ROLES; role++) {
            if (ramps[role] == null || ramps[role].length != 5) throw new IllegalArgumentException("Ramps have five shades");
            for (int rgb : ramps[role]) requireRgb(rgb);
            copy[role] = ramps[role].clone();
        }
        ramps = copy;
    }

    static void requireRgb(int rgb) {
        if ((rgb & 0xFF000000) != 0) throw new IllegalArgumentException("Expected 24-bit RGB");
    }

    public int rgb(int role, int shade) { return ramps[role][shade]; }
    public int primary() { return ramps[PRIMARY][2]; }
    public int secondary() { return ramps[SECONDARY][2]; }
    public int accent() { return ramps[ACCENT][2]; }

    @Override public int[][] ramps() {
        var copy = new int[ROLES][];
        for (int role = 0; role < ROLES; role++) copy[role] = ramps[role].clone();
        return copy;
    }
}
