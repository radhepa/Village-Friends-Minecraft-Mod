package dev.villagefriends.client;

import dev.villagefriends.outfit.Garment;
import dev.villagefriends.outfit.Wardrobe;

/**
 * Fixed layout of the per-resident 256x512 texture: the 64x64 player skin at the origin, the
 * face-detail swatches at (64..67, 0), then one 64-pixel-wide slot per garment kind holding the
 * box-UV nets of that garment's 3D pieces. An outfit wears exactly one hairstyle, top and
 * bottom, so every garment of a kind shares its kind's slot and the wardrobe can grow without
 * growing the texture. One baked model serves every outfit.
 */
final class OutfitAtlas {
    static final int WIDTH = 256, HEIGHT = 512;
    record Block(int x, int y) {}
    private static final Block HAIR = new Block(64, 8), TOP = new Block(128, 0), BOTTOM = new Block(192, 0);
    static {
        for (Garment garment : Wardrobe.ALL) {
            var block = slot(garment.kind());
            if (block.y() + garment.extrasHeight() > HEIGHT)
                throw new IllegalStateException("Wardrobe pieces exceed the " + garment.kind() + " slot: " + garment.id());
        }
    }
    private static Block slot(Garment.Kind kind) {
        return switch (kind) { case HAIR -> HAIR; case TOP -> TOP; case BOTTOM -> BOTTOM; };
    }
    static Block block(Garment garment) { return garment.extrasHeight() == 0 ? null : slot(garment.kind()); }
    private OutfitAtlas() {}
}
