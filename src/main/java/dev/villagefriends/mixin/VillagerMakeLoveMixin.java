package dev.villagefriends.mixin;
import dev.villagefriends.VillageSocieties;
import net.minecraft.world.entity.ai.behavior.VillagerMakeLove;
import net.minecraft.world.entity.ai.memory.MemoryModuleType;
import net.minecraft.world.entity.npc.villager.Villager;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;
/** Relatives never start a family together, and a resident in love only starts one with their partner. */
@Mixin(VillagerMakeLove.class)
public abstract class VillagerMakeLoveMixin {
    @Inject(method = "isBreedingPossible", at = @At("RETURN"), cancellable = true)
    private void villagefriends$family(Villager villager, CallbackInfoReturnable<Boolean> cir) {
        if (!cir.getReturnValueZ()) return;
        villager.getBrain().getMemory(MemoryModuleType.BREED_TARGET).ifPresent(target -> {
            if (target instanceof Villager partner && !VillageSocieties.mayBreed(villager, partner)) cir.setReturnValue(false);
        });
    }
}
