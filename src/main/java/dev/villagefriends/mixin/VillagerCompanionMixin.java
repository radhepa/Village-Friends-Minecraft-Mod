package dev.villagefriends.mixin;
import dev.villagefriends.CompanionController;
import dev.villagefriends.GuardController;
import dev.villagefriends.GuardProgression;
import dev.villagefriends.Knockouts;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.npc.villager.VillagerData;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.ModifyVariable;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
@Mixin(Villager.class)
public abstract class VillagerCompanionMixin {
    @ModifyVariable(method = "setVillagerData", at = @At("HEAD"), argsOnly = true)
    private VillagerData villagefriends$lockedGuard(VillagerData data) {
        return GuardProgression.lockedData((Villager)(Object)this, data);
    }
    @Inject(method = "setVillagerData", at = @At("TAIL"))
    private void villagefriends$newGuard(VillagerData data, CallbackInfo ci) {
        var villager = (Villager)(Object)this;
        if (villager.level() instanceof ServerLevel && CompanionController.loaded.contains(villager)) {
            GuardController.initializeEquipment(villager);
        }
    }
    /** No trading with someone lying hurt on the ground; a name tag still works. */
    @Inject(method = "mobInteract", at = @At("HEAD"), cancellable = true)
    private void villagefriends$injured(Player player, InteractionHand hand, CallbackInfoReturnable<InteractionResult> cir) {
        if (Knockouts.injured((Villager)(Object)this)) cir.setReturnValue(InteractionResult.PASS);
    }
    @Inject(method = "customServerAiStep", at = @At("HEAD"), cancellable = true)
    private void villagefriends$travel(ServerLevel level, CallbackInfo ci) {
        var villager = (Villager)(Object)this;
        if (Knockouts.drive(villager, level)) ci.cancel();
        else if (CompanionController.state(villager).active()) { CompanionController.drive(villager, level); ci.cancel(); }
        else if (GuardController.drive(villager, level, false)) ci.cancel();
    }
}
