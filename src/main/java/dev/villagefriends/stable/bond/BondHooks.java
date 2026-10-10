package dev.villagefriends.stable.bond;

import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;

/**
 * Called by the foundation's {@code HorseEatingMixin}. Owned by the breeds package (bond); the signature is frozen.
 */
public final class BondHooks {
    /**
     * A player fed a horse: runs when {@code AbstractHorse.handleEating} returns, before vanilla shrinks the
     * stack, so {@code food} is still the item that was eaten. {@code ate} is that method's result.
     */
    public static void ate(AbstractHorse horse, Player player, ItemStack food, boolean ate) {}

    private BondHooks() {}
}
