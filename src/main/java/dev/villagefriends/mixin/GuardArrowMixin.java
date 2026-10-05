package dev.villagefriends.mixin;

import dev.villagefriends.GuardController;
import dev.villagefriends.GuardProgression;
import net.minecraft.world.entity.projectile.arrow.AbstractArrow;
import net.minecraft.world.phys.EntityHitResult;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.ModifyArg;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(AbstractArrow.class)
public abstract class GuardArrowMixin {
    @ModifyArg(method = "onHitEntity", at = @At(value = "INVOKE", target = "Lnet/minecraft/world/entity/Entity;hurtOrSimulate(Lnet/minecraft/world/damagesource/DamageSource;F)Z"), index = 1)
    private float villagefriends$leveledArrow(float damage) {
        return GuardProgression.arrowDamage((AbstractArrow)(Object)this, damage);
    }
    @Inject(method = "onHitEntity", at = @At("HEAD"), cancellable = true)
    private void villagefriends$safeImpact(EntityHitResult hit, CallbackInfo ci) {
        var arrow = (AbstractArrow)(Object)this;
        if (GuardController.protectedFromArrow(arrow, hit.getEntity())) { arrow.discard(); ci.cancel(); }
        else if (arrow.getOwner() instanceof net.minecraft.world.entity.npc.villager.Villager v
                && dev.villagefriends.VillageFriends.target(arrow).hasAttached(dev.villagefriends.VillageFriends.GUARD_ARROW_TARGET))
            GuardController.rememberDefense(v, hit.getEntity());
    }
}
