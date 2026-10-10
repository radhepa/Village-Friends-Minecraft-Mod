package dev.villagefriends.stable.mixin;

import dev.villagefriends.stable.gear.PackHooks;
import net.minecraft.world.entity.animal.equine.AbstractChestedHorse;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Donkeys and mules count their own columns (5 with a chest) without asking the horse's method, so the pack hook goes here too. */
@Mixin(AbstractChestedHorse.class)
abstract class ChestedHorsePackMixin {
    @Inject(method = "getInventoryColumns()I", at = @At("RETURN"), cancellable = true)
    private void villagefriends$packColumns(CallbackInfoReturnable<Integer> cir) {
        cir.setReturnValue(PackHooks.columns((AbstractChestedHorse)(Object)this, cir.getReturnValueI()));
    }
}
