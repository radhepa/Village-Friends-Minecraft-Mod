package dev.villagefriends.outfit;

import java.util.HashSet;
import java.util.List;
import java.util.Objects;
import java.util.Set;

/**
 * A hairstyle, top or bottom compiled from {@code tools/wardrobe/}. The texture is pixel art in
 * key colors (role + shade); geometry is the player mesh plus {@link #pieces()}. Garments hold no
 * RGB of their own: an {@link Outfit}'s single palette resolves every key.
 */
public record Garment(String id, Kind kind, String name, String texture, int extrasHeight,
                      Set<String> tags, Set<String> requires, Set<String> rejects,
                      boolean tucked, boolean coversWaist, List<Piece> pieces) {
    public enum Kind { HAIR, TOP, BOTTOM }

    public Garment {
        if (id == null || !id.matches("[a-z0-9_]+")) throw new IllegalArgumentException("Invalid garment id " + id);
        Objects.requireNonNull(kind, "kind");
        if (name == null || name.isBlank()) throw new IllegalArgumentException("Missing garment name: " + id);
        if (texture == null || !texture.matches("[a-z0-9_/]+\\.png")) throw new IllegalArgumentException("Invalid texture: " + id);
        if (extrasHeight < 0 || extrasHeight % 16 != 0) throw new IllegalArgumentException("Extras height must be a multiple of 16: " + id);
        tags = Set.copyOf(tags); requires = Set.copyOf(requires); rejects = Set.copyOf(rejects); pieces = List.copyOf(pieces);
        var ids = new HashSet<String>();
        for (var piece : pieces) {
            if (!ids.add(piece.id())) throw new IllegalArgumentException("Duplicate piece " + piece.id() + " in " + id);
            if (piece.u() + piece.netWidth() > 64 || piece.v() + piece.netHeight() > extrasHeight)
                throw new IllegalArgumentException("Piece UV outside extras region: " + id + ":" + piece.id());
            boolean head = piece.bone() == BodyPart.HEAD;
            boolean legs = piece.bone() == BodyPart.LEFT_LEG || piece.bone() == BodyPart.RIGHT_LEG;
            boolean arms = piece.bone() == BodyPart.LEFT_ARM || piece.bone() == BodyPart.RIGHT_ARM;
            if (kind == Kind.HAIR ? !head : head || (kind == Kind.TOP && legs) || (kind == Kind.BOTTOM && arms))
                throw new IllegalArgumentException("Piece on a bone this garment cannot dress: " + id + ":" + piece.id());
        }
        if (kind != Kind.TOP && (tucked || coversWaist)) throw new IllegalArgumentException("Only tops tuck or cover the waist: " + id);
    }
}
