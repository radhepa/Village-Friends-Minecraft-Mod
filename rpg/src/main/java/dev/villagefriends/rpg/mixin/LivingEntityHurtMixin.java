package dev.villagefriends.rpg.mixin;

import dev.villagefriends.rpg.Hunt;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.LivingEntity;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.ModifyVariable;

/** Scales damage dealt by and to players before armor, so the RPG bonuses stack like vanilla Strength. */
@Mixin(LivingEntity.class)
public abstract class LivingEntityHurtMixin {
    @ModifyVariable(method = "hurtServer", at = @At("HEAD"), argsOnly = true)
    private float villagefriendsRpg$scale(float amount, ServerLevel level, DamageSource source) {
        return Hunt.adjust((LivingEntity) (Object) this, source, amount);
    }
}
