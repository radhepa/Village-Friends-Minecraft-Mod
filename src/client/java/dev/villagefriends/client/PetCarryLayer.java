package dev.villagefriends.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.math.Axis;
import dev.villagefriends.client.mixin.WolfHeadAccessor;
import net.minecraft.client.model.animal.wolf.WolfModel;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.entity.RenderLayerParent;
import net.minecraft.client.renderer.entity.layers.RenderLayer;
import net.minecraft.client.renderer.entity.state.WolfRenderState;
import net.minecraft.client.renderer.texture.OverlayTexture;

/** The stick a resident's dog carries back in its mouth during a game of fetch, held crosswise like a real dog would. */
public final class PetCarryLayer extends RenderLayer<WolfRenderState, WolfModel> {
    public PetCarryLayer(RenderLayerParent<WolfRenderState, WolfModel> renderer) { super(renderer); }

    @Override public void submit(PoseStack pose, SubmitNodeCollector collector, int light, WolfRenderState state, float yRot, float xRot) {
        var item = state.getData(PetPoser.CARRIED);
        if (item == null || item.isEmpty()) return;
        var model = getParentModel();
        pose.pushPose();
        model.root().translateAndRotate(pose);
        ((WolfHeadAccessor) model).villagefriends$head().translateAndRotate(pose);
        // The middle of the jaws, in the head's own pixels.
        if (state.isBaby) pose.translate(0, 2.2F / 16F, -4.8F / 16F);
        else pose.translate(1 / 16F, 3.4F / 16F, -5.2F / 16F);
        pose.rotateDegrees(Axis.YP, 45);
        pose.rotateDegrees(Axis.XP, 90);
        if (state.isBaby) pose.scale(.8F, .8F, .8F); else pose.scale(1.3F, 1.3F, 1.3F);
        item.submit(pose, collector, light, OverlayTexture.NO_OVERLAY, state.outlineColor);
        pose.popPose();
    }
}
