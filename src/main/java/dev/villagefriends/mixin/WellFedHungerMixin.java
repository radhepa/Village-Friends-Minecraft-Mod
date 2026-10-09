package dev.villagefriends.mixin;

import dev.villagefriends.hearth.WellFed;
import net.minecraft.world.entity.player.Player;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.ModifyVariable;

/** Well Fed: hunger drains slower while a good meal lasts (Hearth & Harvest). */
@Mixin(Player.class)
abstract class WellFedHungerMixin {
    @ModifyVariable(method = "causeFoodExhaustion", at = @At("HEAD"), argsOnly = true)
    private float villagefriends$wellFed(float exhaustion) { return WellFed.exhaustion((Player) (Object) this, exhaustion); }
}
