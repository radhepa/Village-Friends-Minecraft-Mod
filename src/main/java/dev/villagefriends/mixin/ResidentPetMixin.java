package dev.villagefriends.mixin;

import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.animal.golem.IronGolem;
import net.minecraft.world.entity.animal.wolf.Wolf;
import net.minecraft.world.entity.npc.villager.AbstractVillager;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.player.Player;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** A resident's dog defends them from monsters, but never bites a player, a neighbor or an iron golem on their behalf. */
@Mixin(Wolf.class)
abstract class ResidentPetMixin {
    @Inject(method = "wantsToAttack", at = @At("HEAD"), cancellable = true)
    private void villagefriends$gentle(LivingEntity target, LivingEntity owner, CallbackInfoReturnable<Boolean> cir) {
        if (owner instanceof Villager && (target instanceof Player || target instanceof AbstractVillager || target instanceof IronGolem)) cir.setReturnValue(false);
    }
}
