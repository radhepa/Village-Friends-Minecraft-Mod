package dev.villagefriends.stable.ride;

import dev.villagefriends.routine.Routine;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.entity.npc.villager.Villager;

/**
 * Residents on horseback, called from Village Friends' core (routines, patrols, guards and companions). A
 * villager riding a tame horse steers it: its navigation is the horse's, so a walk target or a
 * {@code getNavigation().moveTo(...)} moves the horse at the horse's own speed times the modifier.
 * Owned by the riders package; the signatures are frozen.
 */
public final class Mounts {
    /** Riding a horse (so the routine keeps steering them instead of handing a passenger back to vanilla). */
    public static boolean mounted(Villager v) { return false; }
    /**
     * Seated by {@code PackAnimals.mountGuard} for a caravan (order "caravan") and still on the horse: their routine
     * and their villager brain stay off, so only the caller steers them. A guard still fights first.
     */
    public static boolean caravan(Villager v) { return false; }
    /** Mounting for the night watch and riding back to the stable afterwards; true while it is steering them this update. */
    public static boolean update(Villager v, ServerLevel level, Routine.Plan plan) { return false; }
    /** What to multiply a walking speed modifier by: 1 on foot; on horseback it keeps a mixed squad together. */
    public static double pace(Villager v) { return 1.0; }
    /** How much wider patrol followers keep their distance (horses are wider than people). */
    public static double spacing(Villager v) { return 1.0; }
    /** A companion following a mounted player rides a spare horse; true while it is steering them this tick. */
    public static boolean companion(Villager v, ServerPlayer p, ServerLevel level, String mode) { return false; }
    /** Takes a resident off a horse (teleporting a passenger would snap them back to it). */
    public static void dismount(Villager v) { if (v.getVehicle() instanceof AbstractHorse) v.stopRiding(); }

    private Mounts() {}
}
