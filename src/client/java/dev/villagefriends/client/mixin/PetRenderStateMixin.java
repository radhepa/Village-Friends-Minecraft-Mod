package dev.villagefriends.client.mixin;

import dev.villagefriends.client.PetPoser;
import net.minecraft.client.renderer.entity.LivingEntityRenderer;
import net.minecraft.client.renderer.entity.state.LivingEntityRenderState;
import net.minecraft.world.entity.LivingEntity;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Cats and dogs carry the trick they're doing into their render state. */
@Mixin(LivingEntityRenderer.class)
abstract class PetRenderStateMixin {
    @Inject(method = "extractRenderState(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/client/renderer/entity/state/LivingEntityRenderState;F)V", at = @At("TAIL"))
    private void villagefriends$petTrick(LivingEntity entity, LivingEntityRenderState state, float partial, CallbackInfo ci) {
        PetPoser.extract(entity, state, partial);
    }
}
