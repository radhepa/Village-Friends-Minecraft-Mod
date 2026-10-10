package dev.villagefriends.stable.mixin;

import dev.villagefriends.stable.gear.CombatHooks;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.ModifyVariable;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * The couched lance: a stab's damage at its start, and what it hit at its end. {@code Player} overrides
 * {@code stabAttack} completely (it never calls {@code LivingEntity}'s), so both classes are targets; each stab runs
 * exactly one of them. The handler takes only the damage, so the attacker is {@code this} and the lance is the
 * attacker's item in use (a kinetic charge is an item use; the left-click jab is not).
 */
@Mixin({LivingEntity.class, Player.class})
abstract class StabAttackMixin {
    @ModifyVariable(method = "stabAttack(Lnet/minecraft/world/entity/EquipmentSlot;Lnet/minecraft/world/entity/Entity;FZZZ)Z", at = @At("HEAD"), argsOnly = true, ordinal = 0)
    private float villagefriends$lance(float damage) {
        return CombatHooks.stab((LivingEntity)(Object)this, damage);
    }
    @Inject(method = "stabAttack(Lnet/minecraft/world/entity/EquipmentSlot;Lnet/minecraft/world/entity/Entity;FZZZ)Z", at = @At("RETURN"))
    private void villagefriends$lanceHit(EquipmentSlot slot, Entity target, float damage, boolean dealsDamage, boolean knockback, boolean dismount,
                                         CallbackInfoReturnable<Boolean> cir) {
        CombatHooks.stabbed((LivingEntity)(Object)this, slot, target, damage, cir.getReturnValueZ());
    }
}
