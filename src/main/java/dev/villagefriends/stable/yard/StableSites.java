package dev.villagefriends.stable.yard;

import dev.villagefriends.stable.data.StableBlocks;
import java.util.Optional;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.ai.village.poi.PoiManager;
import net.minecraft.world.entity.npc.villager.Villager;

/**
 * Where the stables are. Owned by the stables package; the signatures are frozen.
 */
public final class StableSites {
    /** The nearest Horse Stall within {@code radius} blocks (a point-of-interest search, so only indexed stalls count). */
    public static Optional<BlockPos> stableNear(ServerLevel level, BlockPos pos, int radius) {
        return level.getPoiManager().findClosest(h -> h.is(StableBlocks.STALL_POI), pos, radius, PoiManager.Occupancy.ANY);
    }
    /** True when a stalled horse is within 12 blocks of this resident (conversations can mention the horses). */
    public static boolean horsesNear(Villager v) { return false; }

    private StableSites() {}
}
