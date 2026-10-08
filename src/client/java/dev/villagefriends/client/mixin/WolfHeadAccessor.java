package dev.villagefriends.client.mixin;

import net.minecraft.client.model.animal.wolf.WolfModel;
import net.minecraft.client.model.geom.ModelPart;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.gen.Accessor;

/** Where a dog's mouth is, for the stick it brings back. */
@Mixin(WolfModel.class)
public interface WolfHeadAccessor {
    @Accessor("head") ModelPart villagefriends$head();
}
