package dev.villagefriends.mixin;

import dev.villagefriends.GuardController;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.npc.villager.Villager;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Villagers inherit empty armor-wear hooks; delegate guards to the native equipment implementation. */
@Mixin(LivingEntity.class)
public abstract class GuardArmorMixin {
    @Shadow protected abstract void doHurtEquipment(DamageSource source, float damage, EquipmentSlot... slots);
    @Inject(method = "hurtArmor", at = @At("HEAD"))
    private void villagefriends$armorWear(DamageSource source, float damage, CallbackInfo ci) {
        if ((Object)this instanceof Villager v && GuardController.isGuard(v))
            doHurtEquipment(source, damage, EquipmentSlot.HEAD, EquipmentSlot.CHEST, EquipmentSlot.LEGS, EquipmentSlot.FEET);
    }
    @Inject(method = "hurtHelmet", at = @At("HEAD"))
    private void villagefriends$helmetWear(DamageSource source, float damage, CallbackInfo ci) {
        if ((Object)this instanceof Villager v && GuardController.isGuard(v)) doHurtEquipment(source, damage, EquipmentSlot.HEAD);
    }
}
