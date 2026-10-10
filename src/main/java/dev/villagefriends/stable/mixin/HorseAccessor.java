package dev.villagefriends.stable.mixin;

import net.minecraft.world.entity.animal.equine.Horse;
import net.minecraft.world.entity.animal.equine.Markings;
import net.minecraft.world.entity.animal.equine.Variant;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.gen.Invoker;

/** Sets a horse's vanilla colour and markings together (vanilla keeps both in one synced number). */
@Mixin(Horse.class)
public interface HorseAccessor {
    @Invoker("setVariantAndMarkings") void villagefriends$setVariantAndMarkings(Variant variant, Markings markings);
}
