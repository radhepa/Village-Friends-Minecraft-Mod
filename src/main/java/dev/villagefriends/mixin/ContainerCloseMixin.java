package dev.villagefriends.mixin;

import dev.villagefriends.deed.Deeds;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Closing a container a player opened in a resident's house: anything taken from it is theft. */
@Mixin(AbstractContainerMenu.class)
public abstract class ContainerCloseMixin {
    @Inject(method = "removed", at = @At("HEAD"))
    private void villagefriends$closed(Player player, CallbackInfo ci) {
        Deeds.closed(player, (AbstractContainerMenu) (Object) this);
    }
}
