package dev.villagefriends.client.mixin;

import dev.villagefriends.client.PetPoser;
import net.minecraft.client.model.Model;
import net.minecraft.client.model.animal.feline.AdultFelineModel;
import net.minecraft.client.model.animal.feline.BabyFelineModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.renderer.entity.state.FelineRenderState;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** A resident's cat strikes its trick (batting at string, tail up, a big stretch) on top of the cat's own pose. */
@Mixin({AdultFelineModel.class, BabyFelineModel.class})
abstract class FelinePoseMixin {
    @Unique private ModelPart[] villagefriends$parts;

    @Inject(method = "setupAnim(Lnet/minecraft/client/renderer/entity/state/FelineRenderState;)V", at = @At("TAIL"))
    private void villagefriends$trick(FelineRenderState state, CallbackInfo ci) {
        var pose = state.getData(PetPoser.POSE);
        if (pose == null) return;
        if (villagefriends$parts == null) {
            var p = (FelineParts) this;
            villagefriends$parts = new ModelPart[] {((Model<?>) (Object) this).root(), p.villagefriends$head(), p.villagefriends$body(), null,
                    p.villagefriends$tail(), p.villagefriends$tailTip(), p.villagefriends$rightFrontLeg(), p.villagefriends$leftFrontLeg(),
                    p.villagefriends$rightHindLeg(), p.villagefriends$leftHindLeg()};
        }
        PetPoser.apply(pose, villagefriends$parts);
    }
}
