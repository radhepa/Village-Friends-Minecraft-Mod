package dev.villagefriends.client.mixin;

import dev.villagefriends.client.ResidentLife;
import net.minecraft.world.entity.npc.villager.Villager;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Hearts, angry clouds, happy sparkles and nervous sweat also move the resident's body. */
@Mixin(Villager.class)
abstract class VillagerEventMixin {
    @Inject(method = "handleEntityEvent", at = @At("HEAD"))
    private void villagefriends$react(byte id, CallbackInfo info) {
        var villager = (Villager) (Object) this;
        if (villager.level().isClientSide()) ResidentLife.entityEvent(villager, id);
    }
}
