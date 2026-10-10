package dev.villagefriends.stable.mixin;

import dev.villagefriends.stable.gear.CombatHooks;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.projectile.Projectile;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.ModifyVariable;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Steadier shots from a bonded horse. {@code shoot(x, y, z, power, inaccuracy)} is reached by bows (through
 * {@code shootFromRotation}) and crossbows, and arrows' own {@code shoot} calls this one; the shooter is the
 * projectile's owner, set before shooting. {@code shootFromRotation} ends by adding the shooter's own movement,
 * which the gear package damps for a mounted shooter.
 */
@Mixin(Projectile.class)
abstract class ProjectileSteadyMixin {
    @ModifyVariable(method = "shoot(DDDFF)V", at = @At("HEAD"), argsOnly = true, ordinal = 1)
    private float villagefriends$steady(float inaccuracy) {
        return CombatHooks.aim((Projectile)(Object)this, inaccuracy);
    }
    @Inject(method = "shootFromRotation(Lnet/minecraft/world/entity/Entity;FFFFF)V", at = @At("TAIL"))
    private void villagefriends$shot(Entity shooter, float xRot, float yRot, float roll, float power, float inaccuracy, CallbackInfo ci) {
        CombatHooks.shot((Projectile)(Object)this, shooter);
    }
}
