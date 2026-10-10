package dev.villagefriends.client.mixin;

import dev.villagefriends.client.FishingClient;
import net.minecraft.client.Minecraft;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** While the fishing minigame is up, the use button lifts the catch bar instead of reeling the rod in. */
@Mixin(Minecraft.class)
public abstract class FishingUseItemMixin {
    @Inject(method = "startUseItem", at = @At("HEAD"), cancellable = true)
    private void villagefriends$reel(CallbackInfo ci) {
        if (FishingClient.active()) ci.cancel();
    }
}
