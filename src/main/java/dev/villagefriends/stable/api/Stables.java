package dev.villagefriends.stable.api;

import static dev.villagefriends.VillageFriends.target;

import dev.villagefriends.stable.data.StableData;
import dev.villagefriends.stable.data.StallHome;
import dev.villagefriends.stable.yard.StableSites;
import java.util.List;
import java.util.Optional;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.phys.AABB;

/**
 * Stalls and stables, for the rest of Stablehand and for add-ons (server side).
 * Owned by the stables package; the signatures are frozen.
 */
public final class Stables {
    /** The nearest Horse Stall within {@code radius} blocks. */
    public static Optional<BlockPos> stableNear(ServerLevel level, BlockPos pos, int radius) { return StableSites.stableNear(level, pos, radius); }
    /**
     * Gives a horse a stall: who keeps it ({@code keeper}: a resident id, "village" or "player:&lt;uuid&gt;") and its
     * village id ("" when not known yet). Its vanilla home becomes the stall, so it wanders no further than 6 blocks.
     */
    public static void stall(AbstractHorse horse, BlockPos stall, String village, String keeper) {
        target(horse).setAttached(StableData.STALL, new StallHome(stall.immutable(), horse.level().dimension().identifier().toString(), village, keeper, "", 0, 0));
        horse.setHomeTo(stall, 6);
    }
    /** The horse's stall, if it has one. */
    public static Optional<StallHome> stallOf(AbstractHorse horse) { return Optional.ofNullable(target(horse).getAttached(StableData.STALL)); }
    /** Loaded horses whose stall is within {@code radius} blocks of {@code stable}. */
    public static List<AbstractHorse> stalledHorses(ServerLevel level, BlockPos stable, int radius) {
        return level.getEntitiesOfClass(AbstractHorse.class, new AABB(stable).inflate(radius + 8),
                h -> stallOf(h).filter(s -> s.stall().closerThan(stable, radius)).isPresent());
    }

    private Stables() {}
}
