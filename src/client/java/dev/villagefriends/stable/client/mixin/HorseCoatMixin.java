package dev.villagefriends.stable.client.mixin;

import dev.villagefriends.stable.client.breed.HorseCoats;
import net.minecraft.client.renderer.entity.HorseRenderer;
import net.minecraft.client.renderer.entity.state.HorseRenderState;
import net.minecraft.resources.Identifier;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** A bred horse wears its breed's painted coat; vanilla's markings layer still draws on top. */
@Mixin(HorseRenderer.class)
abstract class HorseCoatMixin {
    @Inject(method = "getTextureLocation(Lnet/minecraft/client/renderer/entity/state/HorseRenderState;)Lnet/minecraft/resources/Identifier;", at = @At("HEAD"), cancellable = true)
    private void villagefriends$coat(HorseRenderState state, CallbackInfoReturnable<Identifier> cir) {
        var texture = HorseCoats.texture(state);
        if (texture != null) cir.setReturnValue(texture);
    }
}
