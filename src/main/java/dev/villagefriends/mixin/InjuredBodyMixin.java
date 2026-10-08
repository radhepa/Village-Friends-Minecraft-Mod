package dev.villagefriends.mixin;

import dev.villagefriends.Knockouts;
import net.minecraft.world.entity.EntityDimensions;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Pose;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** A resident lying hurt on the ground has a low, body-sized hitbox (not a sleeper's speck) and isn't anyone's target. */
@Mixin(LivingEntity.class)
public abstract class InjuredBodyMixin {
    @Unique private static final EntityDimensions LYING = EntityDimensions.scalable(1F, .5F).withEyeHeight(.3F);
    @Unique private static final EntityDimensions LYING_CHILD = EntityDimensions.scalable(.6F, .3F).withEyeHeight(.2F);

    @Inject(method = "getDimensions", at = @At("RETURN"), cancellable = true)
    private void villagefriends$lying(Pose pose, CallbackInfoReturnable<EntityDimensions> cir) {
        var self = (LivingEntity) (Object) this;
        if (pose == Pose.SLEEPING && Knockouts.injured(self)) cir.setReturnValue(self.isBaby() ? LYING_CHILD : LYING);
    }
    @Inject(method = "canBeSeenAsEnemy", at = @At("HEAD"), cancellable = true)
    private void villagefriends$notATarget(CallbackInfoReturnable<Boolean> cir) {
        if (Knockouts.injured((LivingEntity) (Object) this)) cir.setReturnValue(false);
    }
}
