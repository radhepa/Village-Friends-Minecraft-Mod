package dev.villagefriends.outfit;

/** Half-open material-island bounds: [x0,y0,x1,y1]. */
public record PixelBounds(int x0, int y0, int x1, int y1) {
    public PixelBounds {
        if (x0 < 0 || y0 < 0 || x1 <= x0 || y1 <= y0) throw new IllegalArgumentException("Invalid pixel bounds");
    }
    public int area() { return Math.multiplyExact(x1 - x0, y1 - y0); }
}
