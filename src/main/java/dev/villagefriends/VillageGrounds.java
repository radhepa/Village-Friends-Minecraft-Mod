package dev.villagefriends;

import net.minecraft.core.BlockPos;
import net.minecraft.core.SectionPos;
import net.minecraft.world.level.StructureManager;

/**
 * Keeps wild trees, fallen logs, cacti, bamboo and boulders out of generated villages.
 *
 * <p>Vegetation is decorated after structures, so a forest at a village's edge would
 * otherwise grow trunks through yards and leaves into attics. While a chunk is being
 * decorated, {@code ChunkGeneratorDecorationMixin} lends this class the region's
 * structure manager, and {@code VillageVegetationMixin} asks before each large plant.
 */
public final class VillageGrounds {
    private static final ThreadLocal<StructureManager> DECORATING = new ThreadLocal<>();
    /** Canopies spread about two blocks from the trunk. */
    private static final int MARGIN = 2;

    private VillageGrounds() {}

    public static void begin(StructureManager manager) { DECORATING.set(manager); }

    public static void end() { DECORATING.remove(); }

    public static boolean occupied(BlockPos origin) {
        var manager = DECORATING.get();
        if (manager == null) return false;
        var starts = manager.startsForStructure(SectionPos.blockToSectionCoord(origin.getX()), SectionPos.blockToSectionCoord(origin.getZ()),
                structure -> structure instanceof VillageStructure);
        for (var start : starts)
            for (var piece : start.getPieces()) {
                var box = piece.getBoundingBox();
                if (origin.getX() >= box.minX() - MARGIN && origin.getX() <= box.maxX() + MARGIN && origin.getZ() >= box.minZ() - MARGIN
                        && origin.getZ() <= box.maxZ() + MARGIN && origin.getY() >= box.minY() - 2 && origin.getY() <= box.maxY()) return true;
            }
        return false;
    }
}
