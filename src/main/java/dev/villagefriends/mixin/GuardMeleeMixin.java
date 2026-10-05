package dev.villagefriends.mixin;

import dev.villagefriends.GuardProgression;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.npc.villager.Villager;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.ModifyArg;

/** Scale the finished native weapon/enchantment calculation before the target's armor absorbs it. */
@Mixin(Mob.class)
public abstract class GuardMeleeMixin {
    @ModifyArg(method = "doHurtTarget", at = @At(value = "INVOKE", target = "Lnet/minecraft/world/entity/Entity;hurtServer(Lnet/minecraft/server/level/ServerLevel;Lnet/minecraft/world/damagesource/DamageSource;F)Z"), index = 2)
    private float villagefriends$leveledMelee(float damage) {
        return (Object)this instanceof Villager v ? (float)(damage * GuardProgression.damageMultiplier(v)) : damage;
    }
}
