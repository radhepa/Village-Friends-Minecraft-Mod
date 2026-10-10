package dev.villagefriends.stable.mixin;

import dev.villagefriends.stable.bond.BondHooks;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Feeding grows the bond: the end of {@code handleEating}, before its caller ({@code fedFood}) shrinks the stack. */
@Mixin(AbstractHorse.class)
abstract class HorseEatingMixin {
    @Inject(method = "handleEating(Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/item/ItemStack;)Z", at = @At("RETURN"))
    private void villagefriends$ate(Player player, ItemStack food, CallbackInfoReturnable<Boolean> cir) {
        BondHooks.ate((AbstractHorse)(Object)this, player, food, cir.getReturnValueZ());
    }
}
