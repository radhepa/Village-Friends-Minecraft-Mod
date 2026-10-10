package dev.villagefriends.stable.api;

import dev.villagefriends.stable.ride.Mounts;
import java.util.Optional;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.entity.npc.villager.Villager;

/**
 * Residents on horseback, for the rest of Stablehand and for add-ons (server side). {@code order} says why they
 * ride: "patrol" (night watch), "companion" (following a player) or "caravan" (seated by another mod).
 * Owned by the riders package; the signatures are frozen.
 */
public final class Riders {
    /** Seats a resident on a horse with an order; false if they can't ride it. */
    public static boolean mount(Villager v, AbstractHorse horse, String order) { return false; }
    /** Takes a resident off their horse and clears their order. */
    public static void dismount(Villager v) { Mounts.dismount(v); }
    /** The horse a resident is riding, if any. */
    public static Optional<AbstractHorse> riding(Villager v) { return v.getVehicle() instanceof AbstractHorse h ? Optional.of(h) : Optional.empty(); }

    private Riders() {}
}
