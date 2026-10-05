package dev.villagefriends.outfit;

import java.util.Objects;

/**
 * Four weight channels packed as 0xPPSSAAHH (primary, secondary, accent, hardware).
 * Each covered texel sums to 255. All-zero weights mean empty space.
 * Opacity is separate: the fourth role channel is hardware, NOT image transparency.
 * Signed shade adds neutral lightness to all three resolved sRGB channels.
 */
public final class RoleMask {
    private final int width, height;
    private final int[] weights;
    private final byte[] opacity, shade;

    public RoleMask(int width, int height, int[] weights, byte[] opacity, byte[] shade) {
        if (width < 1 || height < 1) throw new IllegalArgumentException("Invalid mask dimensions");
        int count = Math.multiplyExact(width, height);
        Objects.requireNonNull(weights, "weights");
        Objects.requireNonNull(opacity, "opacity");
        Objects.requireNonNull(shade, "shade");
        if (weights.length != count || opacity.length != count || shade.length != count)
            throw new IllegalArgumentException("Mask arrays must match dimensions");
        this.width = width; this.height = height;
        this.weights = weights.clone(); this.opacity = opacity.clone(); this.shade = shade.clone();
        for (int i = 0; i < count; i++) {
            int w = this.weights[i], sum = (w >>> 24) + ((w >>> 16) & 255) + ((w >>> 8) & 255) + (w & 255);
            if (sum != 0 && sum != 255) throw new IllegalArgumentException("Role weights must sum to 255");
            if (sum == 0 && this.opacity[i] != 0) throw new IllegalArgumentException("Empty texel must be transparent");
        }
    }

    public static RoleMask solid(ColorRole role) {
        int weights = switch (Objects.requireNonNull(role, "role")) {
            case ROLE_PRIMARY -> 0xFF000000;
            case ROLE_SECONDARY -> 0x00FF0000;
            case ROLE_ACCENT -> 0x0000FF00;
            case ROLE_HARDWARE -> 0x000000FF;
        };
        return new RoleMask(1, 1, new int[]{weights}, new byte[]{(byte)255}, new byte[]{0});
    }

    public int width() { return width; }
    public int height() { return height; }
    public int[] weights() { return weights.clone(); }
    public byte[] opacity() { return opacity.clone(); }
    public byte[] shade() { return shade.clone(); }

    /** Resolve one texel to straight-alpha ARGB. Shade never selects a new palette hue. */
    public int argb(int x, int y, ColorPalette palette) {
        Objects.requireNonNull(palette, "palette");
        Objects.checkIndex(x, width); Objects.checkIndex(y, height);
        return resolve(y * width + x, palette);
    }

    public int[] resolve(ColorPalette palette) {
        Objects.requireNonNull(palette, "palette");
        int[] result = new int[weights.length];
        for (int i = 0; i < result.length; i++) result[i] = resolve(i, palette);
        return result;
    }

    private int resolve(int i, ColorPalette palette) {
        int alpha = Byte.toUnsignedInt(opacity[i]);
        if (alpha == 0) return 0;
        int w = weights[i], p = w >>> 24, s = (w >>> 16) & 255, a = (w >>> 8) & 255, h = w & 255;
        int rgb = 0;
        for (int shift = 16; shift >= 0; shift -= 8) {
            int channel = (p * ((palette.primary() >>> shift) & 255)
                + s * ((palette.secondary() >>> shift) & 255)
                + a * ((palette.accent() >>> shift) & 255)
                + h * ((palette.hardware() >>> shift) & 255) + 127) / 255;
            rgb |= Math.clamp(channel + shade[i], 0, 255) << shift;
        }
        return (alpha << 24) | rgb;
    }
}
