package dev.villagefriends.rpg.mixin;

import dev.villagefriends.rpg.Rpg;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.monster.piglin.PiglinAi;
import net.minecraft.world.entity.player.Player;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Gilded Guile (Slayer of Piglins): piglins treat you as if you wore gold. */
@Mixin(PiglinAi.class)
public abstract class PiglinGoldMixin {
    @Inject(method = "isWearingSafeArmor", at = @At("HEAD"), cancellable = true)
    private static void villagefriendsRpg$guile(LivingEntity entity, CallbackInfoReturnable<Boolean> cir) {
        if (entity instanceof Player p && Rpg.sheet(p).special("gilded_guile")) cir.setReturnValue(true);
    }
}
