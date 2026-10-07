package dev.villagefriends.mixin;
import dev.villagefriends.VillageSocieties;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.npc.villager.Villager;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;
/** Babies remember who their parents are, so they join the right family in the village census. */
@Mixin(Villager.class)
public abstract class VillagerFamilyMixin {
    @Inject(method = "getBreedOffspring(Lnet/minecraft/server/level/ServerLevel;Lnet/minecraft/world/entity/AgeableMob;)Lnet/minecraft/world/entity/npc/villager/Villager;", at = @At("RETURN"))
    private void villagefriends$parents(ServerLevel level, AgeableMob partner, CallbackInfoReturnable<Villager> cir) {
        VillageSocieties.conceived((Villager)(Object)this, partner, cir.getReturnValue());
    }
}
