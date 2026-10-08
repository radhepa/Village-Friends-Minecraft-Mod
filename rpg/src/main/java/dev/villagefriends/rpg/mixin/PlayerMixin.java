package dev.villagefriends.rpg.mixin;

import dev.villagefriends.rpg.Life;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.block.state.BlockState;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.ModifyVariable;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Hunger drain, tool-skill mining speed and Arcana's vanilla experience bonus. */
@Mixin(Player.class)
public abstract class PlayerMixin {
    @ModifyVariable(method = "causeFoodExhaustion", at = @At("HEAD"), argsOnly = true)
    private float villagefriendsRpg$hunger(float amount) { return Life.hunger((Player) (Object) this, amount); }

    @Inject(method = "getDestroySpeed", at = @At("RETURN"), cancellable = true)
    private void villagefriendsRpg$toolSkill(BlockState state, CallbackInfoReturnable<Float> cir) {
        float f = Life.toolSpeed((Player) (Object) this, state);
        if (f != 1) cir.setReturnValue(cir.getReturnValue() * f);
    }

    @ModifyVariable(method = "giveExperiencePoints", at = @At("HEAD"), argsOnly = true)
    private int villagefriendsRpg$arcana(int amount) { return Life.vanillaXp((Player) (Object) this, amount); }
}
