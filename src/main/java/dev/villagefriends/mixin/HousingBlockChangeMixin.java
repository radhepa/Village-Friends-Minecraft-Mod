package dev.villagefriends.mixin;

import dev.villagefriends.home.Homes;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.block.state.BlockState;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Tells the housing index when a bed, door, plaque or job site changes, so only the house around it is looked
 * at again. Vanilla calls this for every block change, world generation threads included: only main-thread
 * changes count, and everything else returns at once.
 */
@Mixin(ServerLevel.class)
public abstract class HousingBlockChangeMixin {
    @Inject(method = "updatePOIOnBlockStateChange", at = @At("HEAD"))
    private void villagefriends$housing(BlockPos pos, BlockState old, BlockState now, CallbackInfo ci) {
        var level = (ServerLevel) (Object) this;
        if (old != now && level.getServer().isSameThread()) Homes.changed(level, pos, old, now);
    }
}
