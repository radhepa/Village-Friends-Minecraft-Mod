package dev.villagefriends.outfit;

import java.util.*;

/** Validated four-channel material atlas; islands are sampled by colored voxel components. */
public final class MaterialMask {
    private final int width, height;
    private final Map<ColorRole, List<PixelBounds>> bounds;
    private final Map<ColorRole, RoleMask> cells;
    private final RoleMask mask;

    public MaterialMask(int width, int height, Map<ColorRole, List<PixelBounds>> input) {
        if (width < 1 || height < 1 || width > 1024 || height > 1024) throw new IllegalArgumentException("Invalid material atlas size");
        this.width = width; this.height = height;
        int[] weights = new int[Math.multiplyExact(width, height)]; byte[] opacity = new byte[weights.length];
        var regions = new EnumMap<ColorRole, List<PixelBounds>>(ColorRole.class);
        var samples = new EnumMap<ColorRole, RoleMask>(ColorRole.class);
        if (!input.keySet().equals(Set.of(ColorRole.values()))) throw new IllegalArgumentException("Exactly four material roles required");
        for (var role : ColorRole.values()) {
            var rects = ModelChecks.nonempty(input.get(role), "role bounds");
            regions.put(role, rects);
            int packed = RoleMask.solid(role).weights()[0];
            for (var rect : rects) {
                if (rect.x1() > width || rect.y1() > height) throw new IllegalArgumentException("Bounds exceed material atlas");
                for (int y = rect.y0(); y < rect.y1(); y++) for (int x = rect.x0(); x < rect.x1(); x++) {
                    int pixel = y * width + x;
                    if (opacity[pixel] != 0) throw new IllegalArgumentException("Overlapping role bounds");
                    weights[pixel] = packed; opacity[pixel] = (byte)255;
                }
            }
            // One-pixel component swatch taken from this role's declared atlas island.
            var first = rects.getFirst(); int pixel = first.y0() * width + first.x0();
            samples.put(role, new RoleMask(1, 1, new int[]{weights[pixel]}, new byte[]{opacity[pixel]}, new byte[]{0}));
        }
        bounds = Map.copyOf(regions); cells = Map.copyOf(samples);
        mask = new RoleMask(width, height, weights, opacity, new byte[weights.length]);
        int textile = pixels(ColorRole.ROLE_PRIMARY) + pixels(ColorRole.ROLE_SECONDARY) + pixels(ColorRole.ROLE_ACCENT);
        for (var role : List.of(ColorRole.ROLE_PRIMARY, ColorRole.ROLE_SECONDARY, ColorRole.ROLE_ACCENT))
            if ((long)pixels(role) * 100 != (long)textile * role.textilePercent())
                throw new IllegalArgumentException("Textile pixel coverage must be 60/30/10");
    }
    public int width() { return width; }
    public int height() { return height; }
    public Map<ColorRole, List<PixelBounds>> bounds() { return bounds; }
    public int pixels(ColorRole role) { return bounds.get(Objects.requireNonNull(role)).stream().mapToInt(PixelBounds::area).sum(); }
    public RoleMask mask() { return mask; }
    public RoleMask cell(ColorRole role) { return cells.get(Objects.requireNonNull(role)); }
}
