package dev.villagefriends;

import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.Level;

/** Read it inside a village to see everyone who lives there, their families and how they all get along. */
public final class VillageLedgerItem extends Item {
    public VillageLedgerItem(Properties properties) { super(properties); }
    @Override public InteractionResult use(Level level, Player player, InteractionHand hand) {
        if (player instanceof ServerPlayer sp) VillageLedger.openHere(sp);
        return InteractionResult.SUCCESS;
    }
}
