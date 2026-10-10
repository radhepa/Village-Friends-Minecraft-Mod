package dev.villagefriends.stable.client;

import dev.villagefriends.stable.client.breed.BreedClient;
import dev.villagefriends.stable.client.gear.GearClient;
import dev.villagefriends.stable.client.ride.RideClient;
import dev.villagefriends.stable.client.yard.YardClient;
import net.fabricmc.api.ClientModInitializer;

/** Stablehand's client entrypoint: each feature package registers its own client side. */
public final class StablehandClient implements ClientModInitializer {
    @Override public void onInitializeClient() {
        BreedClient.register();
        GearClient.register();
        YardClient.register();
        RideClient.register();
    }
}
