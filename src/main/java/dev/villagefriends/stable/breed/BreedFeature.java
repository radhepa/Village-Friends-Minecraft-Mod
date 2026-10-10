package dev.villagefriends.stable.breed;

import dev.villagefriends.stable.bond.Bonds;
import dev.villagefriends.stable.bond.Grooming;
import dev.villagefriends.stable.bond.Whistle;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerChunkEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerEntityEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.fabricmc.fabric.api.event.player.UseEntityCallback;
import net.fabricmc.fabric.api.event.player.UseItemCallback;
import net.fabricmc.fabric.api.networking.v1.ServerPlayConnectionEvents;

/**
 * Breeds, bond, brush and whistle (the breeds package): registers that package's listeners. Called once from
 * {@code Stablehand.register()}.
 */
public final class BreedFeature {
    public static void register() {
        Breeds.spawns();
        // A horse without a breed gets its biome's; any bonded horse gets its tier's bonuses back (they aren't saved).
        ServerEntityEvents.ENTITY_LOAD.register((entity, level) -> { Breeds.loaded(entity, level); Bonds.loaded(entity); });
        ServerChunkEvents.CHUNK_GENERATE.register(Breeds::generated);
        ServerTickEvents.END_SERVER_TICK.register(server -> { Breeds.tick(server); Bonds.tick(server); Whistle.tick(server); });
        UseEntityCallback.EVENT.register((player, level, hand, entity, hit) -> Grooming.use(player, level, hand, entity));
        UseItemCallback.EVENT.register(Whistle::use);
        ServerPlayConnectionEvents.DISCONNECT.register((handler, server) -> Bonds.left(handler.getPlayer(), server));
        ServerLifecycleEvents.SERVER_STOPPED.register(server -> { Breeds.clear(); Bonds.clear(); Whistle.clear(); });
    }

    private BreedFeature() {}
}
