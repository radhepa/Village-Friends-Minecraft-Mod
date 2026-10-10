package dev.villagefriends.mixin;

import net.minecraft.world.entity.projectile.FishingHook;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.gen.Accessor;

/** Tall Tales Fishing reads a hook's Luck of the Sea and can hurry its next bite ({@code /fishing bite}). */
@Mixin(FishingHook.class)
public interface FishingHookAccess {
    @Accessor("luck") int villagefriends$luck();
    @Accessor("timeUntilLured") void villagefriends$setTimeUntilLured(int ticks);
    @Accessor("nibble") int villagefriends$nibble();
}
