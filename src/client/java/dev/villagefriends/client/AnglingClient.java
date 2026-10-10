package dev.villagefriends.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import dev.villagefriends.fishing.DockAnglers;
import net.fabricmc.fabric.api.attachment.v1.AttachmentTarget;
import net.minecraft.client.Minecraft;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.rendertype.RenderType;
import net.minecraft.client.renderer.rendertype.RenderTypes;
import net.minecraft.client.renderer.state.level.CameraRenderState;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.Identifier;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;

/**
 * Residents fishing ({@link DockAnglers}): a fishing rod in their right hand (the fish they caught while they show
 * it off), and a line from the rod tip to a bobber floating where they cast, dipping when something bites. The
 * rod tip is worked out from their body turn, as vanilla does for a player seen from outside.
 */
public final class AnglingClient {
    private static final Identifier HOOK = Identifier.withDefaultNamespace("textures/entity/fishing/fishing_hook.png");
    private static final RenderType BOBBER = RenderTypes.entityCutoutCull(HOOK);
    private static ItemStack rod;

    static void register() {}

    /** The part of their fishing a resident is on ("cast", "wait", "bite", "reel", "catch", "lost"), or null. */
    public static String phase(Villager v) {
        String s = ((AttachmentTarget) v).getAttached(DockAnglers.STATE);
        if (s == null || s.isEmpty()) return null;
        int bar = s.indexOf('|');
        return bar < 0 ? s : s.substring(0, bar);
    }

    static void extract(Villager v, ResidentRenderState s, boolean portrait, float partial) {
        s.lineShown = false;
        String raw = ((AttachmentTarget) v).getAttached(DockAnglers.STATE);
        if (raw == null || portrait) return;
        var parts = raw.split("\\|", -1);
        if (parts.length < 5) return;
        String phase = parts[0];
        var resolver = Minecraft.getInstance().getItemModelResolver();
        if (rod == null) rod = new ItemStack(Items.FISHING_ROD);
        ItemStack held = rod;
        if (phase.equals("catch") && !parts[4].isEmpty()) {
            var item = BuiltInRegistries.ITEM.getValue(Identifier.parse(parts[4]));
            if (item != Items.AIR) held = new ItemStack(item);
        }
        resolver.updateForLiving(s.rightHandItemState, held, ItemDisplayContext.THIRD_PERSON_RIGHT_HAND, v);
        s.rightHandItemStack = held; s.rightArmPose = HumanoidModel.ArmPose.ITEM;
        if (phase.equals("catch") || phase.equals("lost")) return;
        double bx, by, bz;
        try { bx = Integer.parseInt(parts[1]) + .5; by = Integer.parseInt(parts[2]) + .88; bz = Integer.parseInt(parts[3]) + .5; }
        catch (NumberFormatException e) { return; }
        float age = v.tickCount + partial;
        by += Mth.sin(age * .12F) * .03F;
        if (phase.equals("bite")) by -= .12 + Mth.sin(age * 1.7F) * .05;
        if (phase.equals("reel")) by -= .05;
        // The rod tip: out in front of them and to the right, about head height, as vanilla places a player's.
        float yaw = Mth.lerp(partial, v.yBodyRotO, v.yBodyRot) * Mth.DEG_TO_RAD;
        double sin = Mth.sin(yaw), cos = Mth.cos(yaw), right = .35, forward = .8;
        double x = Mth.lerp(partial, v.xo, v.getX()), y = Mth.lerp(partial, v.yo, v.getY()), z = Mth.lerp(partial, v.zo, v.getZ());
        s.rodX = -cos * right - sin * forward;
        s.rodY = v.getEyeHeight() - .45 + .35;
        s.rodZ = -sin * right + cos * forward;
        if (phase.equals("cast")) {
            // Mid-cast the bobber is still in the air between them and the water.
            s.bobberX = (bx - x) * .5 + s.rodX * .5; s.bobberY = s.rodY + .8; s.bobberZ = (bz - z) * .5 + s.rodZ * .5;
        } else { s.bobberX = bx - x; s.bobberY = by - y; s.bobberZ = bz - z; }
        s.lineShown = true;
    }

    static void submit(ResidentRenderState s, PoseStack pose, SubmitNodeCollector collector, CameraRenderState camera) {
        if (!s.lineShown) return;
        pose.pushPose();
        pose.translate(s.bobberX, s.bobberY, s.bobberZ);
        pose.pushPose();
        pose.scale(.5F, .5F, .5F);
        pose.rotate(camera.orientation);
        collector.submitCustomGeometry(pose, BOBBER, (p, buffer) -> {
            vertex(buffer, p, s.lightCoords, 0, 0, 0, 1);
            vertex(buffer, p, s.lightCoords, 1, 0, 1, 1);
            vertex(buffer, p, s.lightCoords, 1, 1, 1, 0);
            vertex(buffer, p, s.lightCoords, 0, 1, 0, 0);
        });
        pose.popPose();
        float xa = (float) (s.rodX - s.bobberX), ya = (float) (s.rodY - s.bobberY), za = (float) (s.rodZ - s.bobberZ);
        float width = Minecraft.getInstance().gameRenderer.gameRenderState().windowRenderState.appropriateLineWidth;
        collector.submitCustomGeometry(pose, RenderTypes.lines(), (p, buffer) -> {
            for (int i = 0; i < 16; i++) {
                float a0 = i / 16F, a1 = (i + 1) / 16F;
                line(xa, ya, za, buffer, p, a0, a1, width);
                line(xa, ya, za, buffer, p, a1, a0, width);
            }
        });
        pose.popPose();
    }
    private static void vertex(VertexConsumer buffer, PoseStack.Pose pose, int light, float x, int y, int u, int v) {
        buffer.addVertex(pose, x - .5F, y - .5F, 0).setColor(-1).setUv(u, v).setOverlay(OverlayTexture.NO_OVERLAY).setLight(light).setNormal(pose, 0, 1, 0);
    }
    /** One segment of the sagging line, as vanilla draws a player's. */
    private static void line(float xa, float ya, float za, VertexConsumer buffer, PoseStack.Pose pose, float a, float next, float width) {
        float x = xa * a, y = ya * (a * a + a) * .5F + .25F, z = za * a;
        float nx = xa * next - x, ny = ya * (next * next + next) * .5F + .25F - y, nz = za * next - z;
        float len = Mth.sqrt(nx * nx + ny * ny + nz * nz);
        buffer.addVertex(pose, x, y, z).setColor(0xFF000000).setNormal(pose, nx / len, ny / len, nz / len).setLineWidth(width);
    }

    private AnglingClient() {}
}
