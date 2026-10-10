package dev.villagefriends.stable.api;

import dev.villagefriends.stable.ride.Mounts;
import java.util.Optional;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.entity.npc.villager.Villager;

/**
 * Residents on horseback, for the rest of Stablehand and for add-ons (server side). {@code order} says why they
 * ride: "patrol" (night watch), "companion" (following a player) or "caravan" (seated by another mod). A rider
 * steers the horse: {@code v.getNavigation()} is the horse's while they ride, so {@code moveTo(...)} moves the horse
 * at its own speed times the modifier. A "caravan" rider's routine and villager brain stay off until
 * {@link #dismount}, so only the caller steers them; residents riding for the other two orders are steered by
 * Village Friends (the night watch, or following their player).
 * Owned by the riders package; the signatures are frozen.
 */
public final class Riders {
    /**
     * Seats a resident on a horse with an order; false if they can't ride it: a baby, an empty order, or a horse that
     * is not a tame, living adult with no rider in the same world.
     */
    public static boolean mount(Villager v, AbstractHorse horse, String order) { return Mounts.mount(v, horse, order); }
    /** Takes a resident off their horse and clears their order. */
    public static void dismount(Villager v) { Mounts.dismount(v); }
    /** The horse a resident is riding, if any. */
    public static Optional<AbstractHorse> riding(Villager v) { return v.getVehicle() instanceof AbstractHorse h ? Optional.of(h) : Optional.empty(); }
    /** Why a resident rides: "patrol", "companion" or "caravan"; "" when they have no order. */
    public static String order(Villager v) { return Mounts.order(v); }

    private Riders() {}
}
