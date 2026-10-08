package dev.villagefriends.mixin;

import dev.villagefriends.routine.RoutineBrain;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.behavior.SleepInBed;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Being at home is not the same as going to bed: residents home for breakfast, supper or out of the rain stay up. */
@Mixin(SleepInBed.class)
public abstract class SleepInBedRoutineMixin {
    @Inject(method = "checkExtraStartConditions", at = @At("HEAD"), cancellable = true)
    private void villagefriends$stayUp(ServerLevel level, LivingEntity body, CallbackInfoReturnable<Boolean> cir) {
        if (body.getBrain() instanceof RoutineBrain routine && !routine.villagefriends$maySleep()) cir.setReturnValue(false);
    }
}
