package dev.villagefriends.stable.yard;

import static dev.villagefriends.VillageFriends.target;

import dev.villagefriends.stable.data.StableBlocks;
import dev.villagefriends.stable.data.StableData;
import java.util.Optional;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.ai.village.poi.PoiManager;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.entity.npc.villager.Villager;

/**
 * Where the stables are. Owned by the stables package; the signatures are frozen.
 */
public final class StableSites {
    /** How close a stalled horse must be for a resident to bring the horses up in conversation. */
    public static final int TALK_REACH = 12;

    /**
     * The nearest Horse Stall within {@code radius} blocks (a point-of-interest search, so only indexed stalls count:
     * right for finding a village's stable, where the stalls have long been indexed; template horses settle by
     * reading blocks instead, see {@link StableHorses}).
     */
    public static Optional<BlockPos> stableNear(ServerLevel level, BlockPos pos, int radius) {
        return level.getPoiManager().findClosest(h -> h.is(StableBlocks.STALL_POI), pos, radius, PoiManager.Occupancy.ANY);
    }
    /** True when a stalled horse is within 12 blocks of this resident (conversations can mention the horses). */
    public static boolean horsesNear(Villager v) {
        return !v.level().getEntitiesOfClass(AbstractHorse.class, v.getBoundingBox().inflate(TALK_REACH),
                h -> h.isAlive() && target(h).hasAttached(StableData.STALL)).isEmpty();
    }

    private StableSites() {}
}
