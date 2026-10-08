package dev.villagefriends.client.mixin;

import net.minecraft.client.model.animal.feline.AbstractFelineModel;
import net.minecraft.client.model.geom.ModelPart;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.gen.Accessor;

@Mixin(AbstractFelineModel.class)
public interface FelineParts {
    @Accessor("head") ModelPart villagefriends$head();
    @Accessor("body") ModelPart villagefriends$body();
    @Accessor("tail1") ModelPart villagefriends$tail();
    @Accessor("tail2") ModelPart villagefriends$tailTip();
    @Accessor("rightFrontLeg") ModelPart villagefriends$rightFrontLeg();
    @Accessor("leftFrontLeg") ModelPart villagefriends$leftFrontLeg();
    @Accessor("rightHindLeg") ModelPart villagefriends$rightHindLeg();
    @Accessor("leftHindLeg") ModelPart villagefriends$leftHindLeg();
}
