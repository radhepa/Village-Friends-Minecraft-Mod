package dev.villagefriends.stable;

import dev.villagefriends.stable.breed.BreedFeature;
import dev.villagefriends.stable.data.StableBlocks;
import dev.villagefriends.stable.data.StableComponents;
import dev.villagefriends.stable.data.StableData;
import dev.villagefriends.stable.data.StableItems;
import dev.villagefriends.stable.data.StableTable;
import dev.villagefriends.stable.gear.GearFeature;
import dev.villagefriends.stable.ride.RideFeature;
import dev.villagefriends.stable.yard.YardFeature;

/**
 * Stablehand: horses worth caring about, and villages with stables. Breeds are saved data on vanilla horses
 * (no new horse entity), bulk content comes from the tables in {@code tools/stablehand}, and four features hang
 * off this one call in {@code VillageFriends.onInitialize}: breeds and bond ({@code breed}, {@code bond}), gear
 * and mounted combat ({@code gear}), stables and the stablehand ({@code yard}), and residents on horseback,
 * horse deeds and spooking ({@code ride}). Add-ons use {@code api}: {@code Horses}, {@code PackAnimals},
 * {@code Stables}, {@code Riders} and {@code StablehandEvents}. Works with and without the RPG add-on and
 * Not-So-Vanilla Mobs.
 */
public final class Stablehand {
    public static void register() {
        // Attachments first: synced types must exist before any player joins.
        StableData.register();
        StableTable.load();
        StableComponents.register();
        StableBlocks.register();
        StableItems.register();
        BreedFeature.register();
        GearFeature.register();
        YardFeature.register();
        RideFeature.register();
    }

    private Stablehand() {}
}
