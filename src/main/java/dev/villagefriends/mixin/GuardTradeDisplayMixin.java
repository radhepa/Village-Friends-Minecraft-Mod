package dev.villagefriends.mixin;

import dev.villagefriends.GuardController;
import net.minecraft.world.entity.ai.behavior.ShowTradesToPlayer;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.item.ItemStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Trade previews normally overwrite and clear MAINHAND. Guards keep their physical weapon. */
@Mixin(ShowTradesToPlayer.class)
public abstract class GuardTradeDisplayMixin {
    @Inject(method = "displayAsHeldItem", at = @At("HEAD"), cancellable = true)
    private static void villagefriends$keepWeapon(Villager villager, ItemStack display, CallbackInfo ci) {
        if (GuardController.isGuard(villager)) ci.cancel();
    }
    @Inject(method = "clearHeldItem", at = @At("HEAD"), cancellable = true)
    private static void villagefriends$keepWeaponOnClear(Villager villager, CallbackInfo ci) {
        if (GuardController.isGuard(villager)) ci.cancel();
    }
}
