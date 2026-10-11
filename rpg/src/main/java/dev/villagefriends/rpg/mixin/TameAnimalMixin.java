package dev.villagefriends.rpg.mixin;

import dev.villagefriends.rpg.Hunt;
import net.minecraft.advancements.triggers.TameAnimalTrigger;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.animal.Animal;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Taming trains Husbandry. Vanilla fires this advancement trigger for every tamed wolf, cat, parrot and horse,
 * and so do the modpack's pets that tame the vanilla way (Not-So-Vanilla Mobs' pets and mounts, End Friends'
 * Driftrays), so one hook covers them all.
 */
@Mixin(TameAnimalTrigger.class)
public abstract class TameAnimalMixin {
    @Inject(method = "trigger", at = @At("HEAD"))
    private void villagefriendsRpg$tamed(ServerPlayer player, Animal animal, CallbackInfo ci) { Hunt.tamed(player, animal); }
}
