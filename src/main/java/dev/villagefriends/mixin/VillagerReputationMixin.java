package dev.villagefriends.mixin;

import dev.villagefriends.deed.Deeds;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.player.Player;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * One price engine: vanilla's villager reputation, plus what this resident knows of the player's deeds in
 * their village (see DEEDS.md). Trade prices and iron golems both read this, so both agree with what
 * residents say. Nothing is written into vanilla's gossip.
 */
@Mixin(Villager.class)
public abstract class VillagerReputationMixin {
    @Inject(method = "getPlayerReputation", at = @At("RETURN"), cancellable = true)
    private void villagefriends$deeds(Player player, CallbackInfoReturnable<Integer> cir) {
        int deeds = Deeds.reputation((Villager) (Object) this, player);
        if (deeds != 0) cir.setReturnValue(cir.getReturnValueI() + deeds);
    }
}
