package dev.villagefriends.client;

import dev.villagefriends.outfit.Garment;
import dev.villagefriends.outfit.Wardrobe;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Fixed layout of the per-resident 512x512 texture: the 64x64 player skin at the origin, the
 * face-detail swatches at (64..67, 0), then one 64-pixel-wide block per garment holding the
 * box-UV nets of its 3D pieces. Every resident texture shares this layout so one baked model
 * serves every outfit; only the selected garments' blocks are painted.
 */
final class OutfitAtlas {
    static final int WIDTH = 512, HEIGHT = 512, COLUMN = 64;
    record Block(int x, int y) {}
    private static final Map<String, Block> BLOCKS;
    static {
        var blocks = new LinkedHashMap<String, Block>();
        int[] next = new int[WIDTH / COLUMN];
        next[0] = 64; next[1] = 8;
        for (Garment garment : Wardrobe.ALL) {
            int h = garment.extrasHeight();
            if (h == 0) continue;
            int column = 0;
            while (column < next.length && next[column] + h > HEIGHT) column++;
            if (column == next.length) throw new IllegalStateException("Wardrobe atlas overflow at " + garment.id());
            blocks.put(garment.id(), new Block(column * COLUMN, next[column]));
            next[column] += h;
        }
        BLOCKS = Map.copyOf(blocks);
    }
    static Block block(Garment garment) {
        var block = BLOCKS.get(garment.id());
        if (block == null && garment.extrasHeight() > 0) throw new IllegalArgumentException("Garment not in atlas " + garment.id());
        return block;
    }
    private OutfitAtlas() {}
}
