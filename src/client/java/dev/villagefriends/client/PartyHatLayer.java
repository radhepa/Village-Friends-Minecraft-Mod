package dev.villagefriends.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.entity.LivingEntityRenderer;
import net.minecraft.client.renderer.entity.RenderLayerParent;
import net.minecraft.client.renderer.entity.layers.RenderLayer;
import net.minecraft.client.renderer.rendertype.RenderTypes;
import net.minecraft.resources.Identifier;
import net.minecraft.util.Mth;
import org.joml.Quaternionf;

/**
 * A striped party hat with a pompom, worn at a jaunty angle by a resident on their birthday: a twelve-sided
 * cone with the stripes wrapped around it, sitting on top of their hair.
 * Texture layout ({@code textures/entity/party_hat.png}, 16x16): the cone's surface unrolled in x 0-11
 * (around the cone; y 0 at the tip, y 15 at the brim), the pompom at x 12-15, y 0-3.
 */
public final class PartyHatLayer extends RenderLayer<ResidentRenderState, HumanoidModel<ResidentRenderState>> {
    private static final Identifier TEXTURE = Identifier.fromNamespaceAndPath("villagefriends", "textures/entity/party_hat.png");
    private static final int SIDES = 12;
    /** In pixels of the player model: the cone's radius and height, and the pompom's size. */
    private static final float RADIUS = 2.6F, HEIGHT = 7F, POMPOM = 1.1F;

    public PartyHatLayer(RenderLayerParent<ResidentRenderState, HumanoidModel<ResidentRenderState>> parent) { super(parent); }

    @Override public void submit(PoseStack stack, SubmitNodeCollector collector, int light, ResidentRenderState state, float yRot, float xRot) {
        if (!state.partyHat || state.isInvisible || !state.headEquipment.isEmpty()) return;
        var model = getParentModel();
        stack.pushPose();
        model.root().translateAndRotate(stack);
        model.head.translateAndRotate(stack);
        // On top of the hair, a little off-center and tipped to one side. Model space: y points down, 16 pixels to a block.
        float side = (state.motionSeed & 1) == 0 ? 1 : -1;
        stack.translate(side * .9F / 16F, -9.2F / 16F, -.3F / 16F);
        stack.rotate(new Quaternionf().rotationZYX(side * 13 * Mth.DEG_TO_RAD, 0, -7 * Mth.DEG_TO_RAD));
        stack.scale(1 / 16F, 1 / 16F, 1 / 16F);
        int overlay = LivingEntityRenderer.getOverlayCoords(state, 0);
        collector.submitCustomGeometry(stack, RenderTypes.entityTranslucent(TEXTURE), (pose, vc) -> {
            // The cone: one quad per side, its top two corners meeting at the tip.
            float slope = RADIUS / HEIGHT;
            for (int i = 0; i < SIDES; i++) {
                float a0 = i * Mth.TWO_PI / SIDES, a1 = (i + 1) * Mth.TWO_PI / SIDES, mid = (a0 + a1) / 2;
                float u0 = i * 12F / SIDES / 16F, u1 = (i + 1) * 12F / SIDES / 16F;
                // Normals lean upward so the pastel stripes catch the light all the way round.
                float nx = Mth.cos(mid) * .45F, nz = Mth.sin(mid) * .45F, ny = 1 + slope, len = Mth.sqrt(nx * nx + ny * ny + nz * nz);
                nx /= len; ny /= len; nz /= len;
                vertex(vc, pose, Mth.cos(a0) * RADIUS, 0, Mth.sin(a0) * RADIUS, u0, 1, overlay, light, nx, ny, nz);
                vertex(vc, pose, 0, -HEIGHT, 0, u0, 0, overlay, light, nx, ny, nz);
                vertex(vc, pose, 0, -HEIGHT, 0, u1, 0, overlay, light, nx, ny, nz);
                vertex(vc, pose, Mth.cos(a1) * RADIUS, 0, Mth.sin(a1) * RADIUS, u1, 1, overlay, light, nx, ny, nz);
            }
            // The brim's underside, so the hat isn't hollow from below.
            for (int i = 0; i < SIDES; i += 2) {
                float a0 = i * Mth.TWO_PI / SIDES, a1 = (i + 1) * Mth.TWO_PI / SIDES, a2 = (i + 2) * Mth.TWO_PI / SIDES;
                vertex(vc, pose, 0, 0, 0, 2 / 16F, 15 / 16F, overlay, light, 0, -1, 0);
                vertex(vc, pose, Mth.cos(a0) * RADIUS, 0, Mth.sin(a0) * RADIUS, 1 / 16F, 15.5F / 16F, overlay, light, 0, -1, 0);
                vertex(vc, pose, Mth.cos(a1) * RADIUS, 0, Mth.sin(a1) * RADIUS, 2 / 16F, 15.5F / 16F, overlay, light, 0, -1, 0);
                vertex(vc, pose, Mth.cos(a2) * RADIUS, 0, Mth.sin(a2) * RADIUS, 3 / 16F, 15.5F / 16F, overlay, light, 0, -1, 0);
            }
            // The pompom: a little cube at the tip.
            cube(vc, pose, 0, -HEIGHT - POMPOM * .55F, 0, POMPOM, overlay, light);
        });
        stack.popPose();
    }
    /** Normals here face the way the lighting sees them: +y is up, though positions are in model space where +y is down. */
    private static void vertex(VertexConsumer vc, PoseStack.Pose pose, float x, float y, float z, float u, float v, int overlay, int light, float nx, float ny, float nz) {
        vc.addVertex(pose, x, y, z).setColor(0xFFFFFFFF).setUv(u, v).setOverlay(overlay).setLight(light).setNormal(pose, nx, ny, nz);
    }
    private static void cube(VertexConsumer vc, PoseStack.Pose pose, float cx, float cy, float cz, float size, int overlay, int light) {
        float h = size / 2, u0 = 12.5F / 16F, u1 = 15.5F / 16F, v0 = .5F / 16F, v1 = 3.5F / 16F;
        float[][] faces = {
                {0, -1, 0, -h, -h, -h, h, -h, -h, h, -h, h, -h, -h, h}, {0, 1, 0, -h, h, h, h, h, h, h, h, -h, -h, h, -h},
                {0, 0, -1, -h, h, -h, h, h, -h, h, -h, -h, -h, -h, -h}, {0, 0, 1, -h, -h, h, h, -h, h, h, h, h, -h, h, h},
                {-1, 0, 0, -h, h, h, -h, h, -h, -h, -h, -h, -h, -h, h}, {1, 0, 0, h, -h, h, h, -h, -h, h, h, -h, h, h, h}};
        float[][] uv = {{u0, v0}, {u1, v0}, {u1, v1}, {u0, v1}};
        for (var f : faces) for (int c = 0; c < 4; c++)
            vertex(vc, pose, cx + f[3 + c * 3], cy + f[4 + c * 3], cz + f[5 + c * 3], uv[c][0], uv[c][1], overlay, light, f[0], -f[1], f[2]);
    }
}
