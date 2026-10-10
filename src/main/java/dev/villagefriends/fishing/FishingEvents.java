package dev.villagefriends.fishing;

import net.fabricmc.fabric.api.event.Event;
import net.fabricmc.fabric.api.event.EventFactory;
import net.minecraft.server.level.ServerPlayer;

/**
 * Hooks for add-ons (the RPG add-on's Fishing skill uses both). {@link #TUNE} adjusts a player's minigame before it
 * starts (a bigger catch zone, a faster reel); {@link #CAUGHT} fires for every fish a player lands, minigame or not.
 */
public final class FishingEvents {
    @FunctionalInterface public interface Tune { Minigame.Tuning tune(ServerPlayer player, Fish fish, Minigame.Tuning tuning); }
    @FunctionalInterface public interface Caught { void caught(ServerPlayer player, Fish fish, int sizeTenths, boolean perfect); }

    public static final Event<Tune> TUNE = EventFactory.createArrayBacked(Tune.class, listeners -> (player, fish, tuning) -> {
        var t = tuning;
        for (var l : listeners) t = l.tune(player, fish, t);
        return t;
    });
    public static final Event<Caught> CAUGHT = EventFactory.createArrayBacked(Caught.class, listeners -> (player, fish, size, perfect) -> {
        for (var l : listeners) l.caught(player, fish, size, perfect);
    });

    private FishingEvents() {}
}
