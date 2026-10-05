package dev.villagefriends.mixin;

import dev.villagefriends.GuardController;
import net.minecraft.world.entity.projectile.arrow.AbstractArrow;
import net.minecraft.world.phys.EntityHitResult;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(AbstractArrow.class)
public abstract class GuardArrowMixin {
    @Inject(method = "onHitEntity", at = @At("HEAD"), cancellable = true)
    private void villagefriends$safeImpact(EntityHitResult hit, CallbackInfo ci) {
        var arrow = (AbstractArrow)(Object)this;
        if (GuardController.protectedFromArrow(arrow, hit.getEntity())) { arrow.discard(); ci.cancel(); }
        else if (arrow.getOwner() instanceof net.minecraft.world.entity.npc.villager.Villager v
                && dev.villagefriends.VillageFriends.target(arrow).hasAttached(dev.villagefriends.VillageFriends.GUARD_ARROW_TARGET))
            GuardController.rememberDefense(v, hit.getEntity());
    }
}
