package dev.villagefriends.stable.mixin;

import dev.villagefriends.stable.gear.PackHooks;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * Pack slots from tack: the column count (donkeys and mules count theirs in {@code ChestedHorsePackMixin}), saving
 * and loading a pack vanilla would not save, and a last resize before the horse menu is built, so the menu never
 * has more slots than the container.
 */
@Mixin(AbstractHorse.class)
abstract class HorsePackMixin {
    @Inject(method = "getInventoryColumns()I", at = @At("RETURN"), cancellable = true)
    private void villagefriends$packColumns(CallbackInfoReturnable<Integer> cir) {
        cir.setReturnValue(PackHooks.columns((AbstractHorse)(Object)this, cir.getReturnValueI()));
    }
    @Inject(method = "addAdditionalSaveData(Lnet/minecraft/world/level/storage/ValueOutput;)V", at = @At("TAIL"))
    private void villagefriends$savePack(ValueOutput out, CallbackInfo ci) {
        PackHooks.save((AbstractHorse)(Object)this, out);
    }
    @Inject(method = "readAdditionalSaveData(Lnet/minecraft/world/level/storage/ValueInput;)V", at = @At("TAIL"))
    private void villagefriends$loadPack(ValueInput in, CallbackInfo ci) {
        PackHooks.load((AbstractHorse)(Object)this, in);
    }
    @Inject(method = "openCustomInventoryScreen(Lnet/minecraft/world/entity/player/Player;)V", at = @At("HEAD"))
    private void villagefriends$sizePack(Player player, CallbackInfo ci) {
        PackHooks.refresh((AbstractHorse)(Object)this);
    }
}
