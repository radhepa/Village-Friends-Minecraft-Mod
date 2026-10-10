package dev.villagefriends.stable.mixin;

import dev.villagefriends.stable.breed.BreedHooks;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.animal.Animal;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * A foal gets its breed the moment it is born: the end of {@code finalizeSpawnChildFromBreeding} runs after vanilla
 * mixed the parents' stats and before the foal is added to the world.
 */
@Mixin(Animal.class)
abstract class AnimalBreedingMixin {
    @Inject(method = "finalizeSpawnChildFromBreeding(Lnet/minecraft/server/level/ServerLevel;Lnet/minecraft/world/entity/animal/Animal;Lnet/minecraft/world/entity/AgeableMob;)V", at = @At("TAIL"))
    private void villagefriends$bred(ServerLevel level, Animal partner, AgeableMob child, CallbackInfo ci) {
        BreedHooks.bred((Animal)(Object)this, level, partner, child);
    }
}
