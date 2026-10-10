package dev.villagefriends.stable.ride;

import net.fabricmc.fabric.api.event.lifecycle.v1.ServerEntityEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;

/**
 * Knights on horseback, companions' horses, horse deeds and spooking (the riders package): registers that
 * package's listeners. Called once from {@code Stablehand.register()}. The routine, patrol, guard and companion
 * hooks into {@link Mounts} are one-line calls in Village Friends' core and need no listener.
 */
public final class RideFeature {
    public static void register() {
        ServerEntityEvents.ENTITY_LOAD.register((entity, level) -> Spook.loaded(entity));
        ServerEntityEvents.ENTITY_UNLOAD.register((entity, level) -> { Mounts.unload(entity); HorseDeeds.unload(entity); Spook.unload(entity); });
        ServerTickEvents.END_SERVER_TICK.register(server -> { HorseDeeds.tick(server); Spook.tick(server); });
        ServerLifecycleEvents.SERVER_STOPPED.register(server -> { Mounts.clear(); HorseDeeds.clear(); Spook.clear(); });
    }

    private RideFeature() {}
}
