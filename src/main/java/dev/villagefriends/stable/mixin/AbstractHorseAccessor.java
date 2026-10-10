package dev.villagefriends.stable.mixin;

import net.minecraft.world.SimpleContainer;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.gen.Accessor;
import org.spongepowered.asm.mixin.gen.Invoker;

/** The horse's container (saddle row and pack slots) and vanilla's resize, which copies the slots that still fit. */
@Mixin(AbstractHorse.class)
public interface AbstractHorseAccessor {
    @Accessor("inventory") SimpleContainer villagefriends$inventory();
    @Invoker("createInventory") void villagefriends$createInventory();
}
