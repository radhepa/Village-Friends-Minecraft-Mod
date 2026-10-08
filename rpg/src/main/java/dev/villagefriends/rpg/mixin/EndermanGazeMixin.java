package dev.villagefriends.rpg.mixin;

import dev.villagefriends.rpg.Rpg;
import net.minecraft.world.entity.monster.Enderman;
import net.minecraft.world.entity.player.Player;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Steady Gaze (Legend of the Endermen): looking at an enderman no longer angers it. */
@Mixin(Enderman.class)
public abstract class EndermanGazeMixin {
    @Inject(method = "isBeingStaredBy", at = @At("HEAD"), cancellable = true)
    private void villagefriendsRpg$steadyGaze(Player player, CallbackInfoReturnable<Boolean> cir) {
        if (Rpg.sheet(player).special("steady_gaze")) cir.setReturnValue(false);
    }
}
