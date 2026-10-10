package dev.villagefriends.stable.client.mixin;

import dev.villagefriends.stable.client.breed.HorseCoats;
import net.minecraft.client.renderer.entity.AbstractHorseRenderer;
import net.minecraft.client.renderer.entity.state.EquineRenderState;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Carries a horse's breed into its render state. The erased descriptor is pinned: the class also has bridge methods
 * with the same name for its generic parents.
 */
@Mixin(AbstractHorseRenderer.class)
abstract class HorseRenderStateMixin {
    @Inject(method = "extractRenderState(Lnet/minecraft/world/entity/animal/equine/AbstractHorse;Lnet/minecraft/client/renderer/entity/state/EquineRenderState;F)V", at = @At("TAIL"))
    private void villagefriends$breed(AbstractHorse horse, EquineRenderState state, float partial, CallbackInfo ci) {
        HorseCoats.extract(horse, state);
    }
}
