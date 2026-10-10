package dev.villagefriends.stable.api;

import static dev.villagefriends.VillageFriends.target;

import dev.villagefriends.deed.Deeds;
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
 *
 * <p>A stalled horse carries a {@link StallHome}: its Horse Stall block, who keeps it ({@code "player:<uuid>"}, a
 * resident id, or {@code "village"} for a stable template's horses) and its village. Its vanilla home is the stall,
 * so it wanders no further than six blocks; stalled horses that are hurt or still foals eat from a Hay Trough
 * within six blocks of their stall, and the village's stablehand looks in on them.
 */
public final class Stables {
    /** The nearest Horse Stall within {@code radius} blocks. */
    public static Optional<BlockPos> stableNear(ServerLevel level, BlockPos pos, int radius) { return StableSites.stableNear(level, pos, radius); }
    /**
     * Gives a horse a stall: who keeps it ({@code keeper}: a resident id, "village" or "player:&lt;uuid&gt;") and its
     * village id ("" when not known yet). Its vanilla home becomes the stall, so it wanders no further than 6 blocks.
     * Theft flags start clear. This does not move another horse out of the stall (the Horse Stall block does that
     * when a player stables a horse there).
     */
    public static void stall(AbstractHorse horse, BlockPos stall, String village, String keeper) {
        target(horse).setAttached(StableData.STALL, new StallHome(stall.immutable(), horse.level().dimension().identifier().toString(), village, keeper, "", 0, 0));
        horse.setHomeTo(stall, 6);
    }
    /**
     * The horse's stall, if it has one. A stall placed before its village was discovered (a stable built with the
     * village, settled the moment its horses loaded) learns its village here, the first time anyone asks.
     */
    public static Optional<StallHome> stallOf(AbstractHorse horse) {
        StallHome home = target(horse).getAttached(StableData.STALL);
        if (home != null && home.village().isEmpty() && horse.level() instanceof ServerLevel level
                && home.dimension().equals(level.dimension().identifier().toString())) {
            var place = Deeds.place(level, home.stall());
            if (place != null) { home = home.withVillage(place.village()); target(horse).setAttached(StableData.STALL, home); }
        }
        return Optional.ofNullable(home);
    }
    /** Loaded horses whose stall is within {@code radius} blocks of {@code stable}. */
    public static List<AbstractHorse> stalledHorses(ServerLevel level, BlockPos stable, int radius) {
        String dimension = level.dimension().identifier().toString();
        return level.getEntitiesOfClass(AbstractHorse.class, new AABB(stable).inflate(radius + 8), h -> {
            StallHome home = target(h).getAttached(StableData.STALL);
            return h.isAlive() && home != null && home.dimension().equals(dimension) && home.stall().closerThan(stable, radius);
        });
    }

    private Stables() {}
}
