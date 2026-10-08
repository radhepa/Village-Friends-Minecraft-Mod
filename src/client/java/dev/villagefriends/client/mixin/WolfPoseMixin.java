package dev.villagefriends.client.mixin;

import dev.villagefriends.client.PetPoser;
import net.minecraft.client.model.Model;
import net.minecraft.client.model.animal.wolf.WolfModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.renderer.entity.state.WolfRenderState;
import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** A resident's dog strikes its trick (a play bow, rolling over, begging) on top of the wolf's own pose. */
@Mixin(WolfModel.class)
abstract class WolfPoseMixin {
    @Shadow @Final protected ModelPart head, body, rightHindLeg, leftHindLeg, rightFrontLeg, leftFrontLeg, tail;
    @Unique private ModelPart[] villagefriends$parts;

    @Inject(method = "setupAnim(Lnet/minecraft/client/renderer/entity/state/WolfRenderState;)V", at = @At("TAIL"))
    private void villagefriends$trick(WolfRenderState state, CallbackInfo ci) {
        var pose = state.getData(PetPoser.POSE);
        if (pose == null) return;
        if (villagefriends$parts == null) {
            var root = ((Model<?>) (Object) this).root();
            villagefriends$parts = new ModelPart[] {root, head, body, root.hasChild("upper_body") ? root.getChild("upper_body") : null, tail, null,
                    rightFrontLeg, leftFrontLeg, rightHindLeg, leftHindLeg};
        }
        PetPoser.apply(pose, villagefriends$parts);
    }
}
