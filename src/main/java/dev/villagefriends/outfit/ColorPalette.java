package dev.villagefriends.outfit;

import java.util.Objects;

/** Immutable sRGB colors, encoded as 0xRRGGBB. Color exists only at palette resolution. */
public record ColorPalette(PaletteID id, String name, int primary, int secondary, int accent, int hardware) {
    public ColorPalette {
        Objects.requireNonNull(id, "id");
        if (name == null || name.isBlank()) throw new IllegalArgumentException("Missing palette name");
        requireRgb(primary); requireRgb(secondary); requireRgb(accent); requireRgb(hardware);
    }

    static void requireRgb(int rgb) {
        if ((rgb & 0xFF000000) != 0) throw new IllegalArgumentException("Expected 24-bit RGB");
    }

    public int rgb(ColorRole role) {
        return switch (Objects.requireNonNull(role, "role")) {
            case ROLE_PRIMARY -> primary;
            case ROLE_SECONDARY -> secondary;
            case ROLE_ACCENT -> accent;
            case ROLE_HARDWARE -> hardware;
        };
    }
}
