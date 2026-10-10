package dev.villagefriends.stable.mixin;

import dev.villagefriends.stable.gear.PackHooks;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Tack changes resize the pack at once. {@code setItemSlot} stores the item and then calls {@code onEquipItem}, so at
 * its start the new item is already worn. The start, not the end, on purpose: the method returns early on the
 * client, for spectators, for the same item and on an entity's first tick, and a horse spawned and saddled in one
 * go is equipped in its first tick. {@code onEquipItem} is declared only in {@code LivingEntity}.
 */
@Mixin(LivingEntity.class)
abstract class HorseEquipMixin {
    @Inject(method = "onEquipItem(Lnet/minecraft/world/entity/EquipmentSlot;Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/item/ItemStack;)V", at = @At("HEAD"))
    private void villagefriends$tackChanged(EquipmentSlot slot, ItemStack old, ItemStack now, CallbackInfo ci) {
        PackHooks.equipped((LivingEntity)(Object)this, slot, old, now);
    }
}
