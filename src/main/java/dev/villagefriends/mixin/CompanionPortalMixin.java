package dev.villagefriends.mixin;

import dev.villagefriends.CompanionController;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.level.Level;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(Entity.class)
public abstract class CompanionPortalMixin {
    @Inject(method = "canTeleport", at = @At("HEAD"), cancellable = true)
    private void villagefriends$stayInOverworld(Level from, Level to, CallbackInfoReturnable<Boolean> cir) {
        if ((Object)this instanceof Villager v && CompanionController.state(v).active()) cir.setReturnValue(false);
    }
}
