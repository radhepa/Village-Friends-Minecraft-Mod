package dev.villagefriends.hearth;

import net.fabricmc.fabric.api.event.Event;
import net.fabricmc.fabric.api.event.EventFactory;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.item.ItemStack;

/**
 * Hearth & Harvest's hooks for add-ons (the RPG add-on's Cooking skill listens to all three). Register
 * listeners during mod initialization; they run on the server thread.
 */
public final class HearthEvents {
    /** A station finished a batch. Listeners may change {@code result} (for example {@link HearthApi#makeFine}). */
    @FunctionalInterface public interface Cooked {
        /** @param cook the player who last opened the station, if they are online; null otherwise */
        void cooked(ServerLevel level, BlockPos pos, Station station, CookingRecipe recipe, ServerPlayer cook, ItemStack result);
    }
    /** A player took cooked food out of a station's output slot (not hoppers). */
    @FunctionalInterface public interface Taken {
        void taken(ServerPlayer player, Station station, ItemStack taken);
    }
    /** A player ate a dish. Return a factor for its Well Fed time (1 for no change); the factors multiply. */
    @FunctionalInterface public interface Eaten {
        double wellFedFactor(ServerPlayer player, Dish dish, ItemStack stack);
    }

    public static final Event<Cooked> COOKED = EventFactory.createArrayBacked(Cooked.class, listeners -> (level, pos, station, recipe, cook, result) -> {
        for (var l : listeners) l.cooked(level, pos, station, recipe, cook, result);
    });
    public static final Event<Taken> TAKEN = EventFactory.createArrayBacked(Taken.class, listeners -> (player, station, taken) -> {
        for (var l : listeners) l.taken(player, station, taken);
    });
    public static final Event<Eaten> EATEN = EventFactory.createArrayBacked(Eaten.class, listeners -> (player, dish, stack) -> {
        double factor = 1;
        for (var l : listeners) factor *= l.wellFedFactor(player, dish, stack);
        return factor;
    });

    private HearthEvents() {}
}
