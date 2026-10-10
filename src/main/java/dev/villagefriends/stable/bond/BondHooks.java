package dev.villagefriends.stable.bond;

import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;

/**
 * Called by the foundation's {@code HorseEatingMixin}. Owned by the breeds package (bond); the signature is frozen.
 */
public final class BondHooks {
    /**
     * A player fed a horse: runs when {@code AbstractHorse.handleEating} returns, before vanilla shrinks the
     * stack, so {@code food} is still the item that was eaten. {@code ate} is that method's result.
     * Only food the horse really ate counts (vanilla refuses wheat from a full, grown horse), and only from its owner;
     * golden food is worth three times as much.
     */
    public static void ate(AbstractHorse horse, Player player, ItemStack food, boolean ate) {
        if (!ate || !(player instanceof ServerPlayer sp) || horse.level().isClientSide()) return;
        boolean golden = food.is(Items.GOLDEN_CARROT) || food.is(Items.GOLDEN_APPLE) || food.is(Items.ENCHANTED_GOLDEN_APPLE);
        Bonds.gain(horse, sp, golden ? BondMath.Source.FEED_GOLDEN : BondMath.Source.FEED, 0, null);
    }

    private BondHooks() {}
}
