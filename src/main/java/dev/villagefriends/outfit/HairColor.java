package dev.villagefriends.outfit;

/** Natural hair pigment: a five-step ramp (deep, shadow, base, light, sheen), independent of the outfit palette. */
public record HairColor(String id, String name, int[] ramp) {
    public HairColor {
        if (id == null || !id.matches("[A-Z_]+")) throw new IllegalArgumentException("Invalid hair color id " + id);
        if (name == null || name.isBlank()) throw new IllegalArgumentException("Missing hair color name");
        if (ramp == null || ramp.length != 5) throw new IllegalArgumentException("Hair ramps have five shades");
        ramp = ramp.clone();
        for (int rgb : ramp) ColorPalette.requireRgb(rgb);
    }
    public int shade(int shade) { return ramp[shade]; }
    public int base() { return ramp[2]; }
    @Override public int[] ramp() { return ramp.clone(); }
}
