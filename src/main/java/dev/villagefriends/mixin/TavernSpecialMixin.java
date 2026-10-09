package dev.villagefriends.mixin;

import dev.villagefriends.hearth.HearthVillage;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.player.Player;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** The tavern keeper puts the cook's dish of the day on sale before a player sees the trades (Hearth & Harvest). */
@Mixin(Villager.class)
abstract class TavernSpecialMixin {
    @Inject(method = "setTradingPlayer", at = @At("HEAD"))
    private void villagefriends$dishOfTheDay(Player player, CallbackInfo ci) {
        if (player != null) HearthVillage.stockKeeper((Villager) (Object) this);
    }
}
