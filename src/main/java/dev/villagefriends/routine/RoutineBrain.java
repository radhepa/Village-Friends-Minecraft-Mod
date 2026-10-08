package dev.villagefriends.routine;

import net.minecraft.world.entity.schedule.Activity;

/** Added to every {@code Brain}: a resident's routine can stand in for vanilla's villager schedule. */
public interface RoutineBrain {
    /** The activity the resident's routine asks for, or null to follow vanilla's schedule; and whether bed is allowed. */
    void villagefriends$routine(Activity activity, boolean maySleep);
    Activity villagefriends$routine();
    boolean villagefriends$maySleep();
}
