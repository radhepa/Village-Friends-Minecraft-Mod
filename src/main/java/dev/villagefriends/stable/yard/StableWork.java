package dev.villagefriends.stable.yard;

import dev.villagefriends.routine.Routine;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.npc.villager.Villager;

/**
 * The stablehand's working day (filling troughs, visiting stalled horses). Called from the routine chain in
 * {@code ResidentRoutines.update}. Owned by the stables package; the signature is frozen.
 */
public final class StableWork {
    /** True while this resident is busy with stable work this update (the rest of the routine chain is skipped). */
    public static boolean update(Villager v, ServerLevel level, Routine.Plan plan) { return false; }

    private StableWork() {}
}
