package dev.villagefriends.mixin;
import dev.villagefriends.CompanionController;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.npc.villager.Villager;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
@Mixin(Villager.class)
public abstract class VillagerCompanionMixin {
    @Inject(method = "customServerAiStep", at = @At("HEAD"), cancellable = true)
    private void villagefriends$travel(ServerLevel level, CallbackInfo ci) {
        var villager = (Villager)(Object)this;
        if (CompanionController.state(villager).active()) { CompanionController.drive(villager, level); ci.cancel(); }
    }
}
