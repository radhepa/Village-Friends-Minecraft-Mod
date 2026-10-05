package dev.villagefriends.outfit;

import java.util.Objects;

/**
 * One textured 3D cuboid of a garment, attached to a body bone. Coordinates are bone-local
 * model pixels (y down, +x is the wearer's left); {@code origin} is the box corner relative to
 * {@code pivot}, rotations are degrees, and (u, v) is the box-UV origin inside the garment's
 * extras texture.
 */
public record Piece(String id, BodyPart bone, Vec3 pivot, Vec3 rotation, Vec3 origin,
                    int width, int height, int depth, int u, int v, float inflate, Motion motion, Vec3 scale) {
    /** Flaps follow the forward- or backward-most leg so long hems never clip through a stride. */
    public enum Motion { NONE, FLAP_FRONT, FLAP_BACK, SWAY }

    public record Vec3(float x, float y, float z) {
        public static final Vec3 ZERO = new Vec3(0, 0, 0), ONE = new Vec3(1, 1, 1);
        public Vec3 {
            if (!Float.isFinite(x) || !Float.isFinite(y) || !Float.isFinite(z)) throw new IllegalArgumentException("Non-finite vector");
        }
    }

    public Piece {
        if (id == null || !id.matches("[a-z0-9_]+")) throw new IllegalArgumentException("Invalid piece id " + id);
        Objects.requireNonNull(bone, "bone"); Objects.requireNonNull(pivot, "pivot"); Objects.requireNonNull(rotation, "rotation");
        Objects.requireNonNull(origin, "origin"); Objects.requireNonNull(motion, "motion"); Objects.requireNonNull(scale, "scale");
        if (width < 1 || height < 1 || depth < 1) throw new IllegalArgumentException("Pieces need volume: " + id);
        if (u < 0 || v < 0 || inflate < 0 || !Float.isFinite(inflate)) throw new IllegalArgumentException("Invalid piece UV/inflation: " + id);
        if (scale.x() <= 0 || scale.y() <= 0 || scale.z() <= 0) throw new IllegalArgumentException("Invalid piece scale: " + id);
    }

    /** Unfolded box-UV net size. */
    public int netWidth() { return 2 * (width + depth); }
    public int netHeight() { return depth + height; }
}
