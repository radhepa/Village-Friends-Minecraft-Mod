package dev.villagefriends.client;

import com.mojang.blaze3d.vertex.PoseStack;
import dev.villagefriends.outfit.BodyPart;
import dev.villagefriends.outfit.Garment;
import dev.villagefriends.outfit.Piece;
import dev.villagefriends.outfit.Wardrobe;
import java.util.ArrayList;
import java.util.IdentityHashMap;
import java.util.List;
import java.util.Map;
import java.util.function.BiConsumer;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.*;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.entity.LivingEntityRenderer;
import net.minecraft.client.renderer.entity.RenderLayerParent;
import net.minecraft.client.renderer.entity.layers.RenderLayer;
import net.minecraft.client.renderer.rendertype.RenderTypes;
import net.minecraft.util.Mth;
import org.joml.Quaternionf;

/**
 * Draws the 3D pieces of the three garments a resident wears (hair, top, bottom) on the posed
 * player mesh. Every garment's pieces are baked once as plain cubes with no pose of their own;
 * this layer places them on their bone each frame. The model therefore stays the size of one
 * body, and the per-frame cost depends on what a resident wears, not on the size of the wardrobe.
 */
public final class WardrobeLayer extends RenderLayer<ResidentRenderState, HumanoidModel<ResidentRenderState>> {
    public record Shown(Garment garment, Piece piece, ModelPart part) {}
    private record Baked(Piece piece, ModelPart part) {}
    private static Map<Garment, List<Baked>> baked;

    public WardrobeLayer(RenderLayerParent<ResidentRenderState, HumanoidModel<ResidentRenderState>> parent) { super(parent); }

    private static String partName(Garment garment, Piece piece) { return "wardrobe_" + garment.id() + "_" + piece.id(); }

    /** Cube-only parts for every garment piece, textured from the garment's atlas slot. */
    private static synchronized Map<Garment, List<Baked>> baked() {
        if (baked != null) return baked;
        var mesh = new MeshDefinition(); var root = mesh.getRoot();
        for (var garment : Wardrobe.ALL) {
            var block = OutfitAtlas.block(garment);
            for (var p : garment.pieces()) {
                var o = p.origin();
                root.addOrReplaceChild(partName(garment, p), CubeListBuilder.create().texOffs(block.x() + p.u(), block.y() + p.v())
                    .addBox(o.x(), o.y(), o.z(), p.width(), p.height(), p.depth(), new CubeDeformation(p.inflate())), PartPose.ZERO);
            }
        }
        var part = LayerDefinition.create(mesh, OutfitAtlas.WIDTH, OutfitAtlas.HEIGHT).bakeRoot();
        var map = new IdentityHashMap<Garment, List<Baked>>();
        for (var garment : Wardrobe.ALL) {
            var list = new ArrayList<Baked>();
            for (var p : garment.pieces()) list.add(new Baked(p, part.getChild(partName(garment, p))));
            map.put(garment, List.copyOf(list));
        }
        return baked = map;
    }

    /** The pieces a resident shows: armor hides what it covers, and a top's own belt or long hem hides the bottom's waist pieces. */
    public static List<Shown> shown(ResidentRenderState state) {
        var outfit = state.outfit;
        if (outfit == null) return List.of();
        boolean helmet = !state.headEquipment.isEmpty(), chest = !state.chestEquipment.isEmpty(), legs = !state.legsEquipment.isEmpty();
        var list = new ArrayList<Shown>();
        for (var garment : outfit.garments()) for (var b : baked().getOrDefault(garment, List.of())) {
            var piece = b.piece();
            boolean covered = switch (garment.kind()) {
                case HAIR -> helmet;
                case TOP -> chest;
                case BOTTOM -> legs || (piece.bone() == BodyPart.TORSO && chest);
            };
            if (!covered && outfit.shows(garment, piece)) list.add(new Shown(garment, piece, b.part()));
        }
        return list;
    }

    private static ModelPart bone(HumanoidModel<?> model, BodyPart bone) {
        return switch (bone) {
            case HEAD -> model.head; case TORSO -> model.body;
            case LEFT_ARM -> model.leftArm; case RIGHT_ARM -> model.rightArm;
            case LEFT_LEG -> model.leftLeg; case RIGHT_LEG -> model.rightLeg;
        };
    }

    /**
     * Places every shown piece on its posed bone and hands it to {@code draw}. Long hems ride on
     * the leading or trailing leg so a stride never pokes through them; tails and tassels sway.
     */
    public static void pose(HumanoidModel<ResidentRenderState> model, ResidentRenderState state, PoseStack stack, BiConsumer<ModelPart, PoseStack> draw) {
        float forward = Math.min(0, Math.min(model.leftLeg.xRot, model.rightLeg.xRot));
        float backward = Math.max(0, Math.max(model.leftLeg.xRot, model.rightLeg.xRot));
        boolean moving = ResidentAnimation.canMove(state);
        for (var s : shown(state)) {
            var p = s.piece(); var r = p.rotation(); var scale = p.scale();
            float swingX = 0, swingZ = 0;
            switch (p.motion()) {
                case FLAP_FRONT -> swingX = forward;
                case FLAP_BACK -> swingX = backward;
                case SWAY -> { if (moving) {
                    swingZ = Mth.sin(state.walkAnimationPos * .6662F - .6F) * state.walkAnimationSpeed * .09F;
                    swingX = Math.abs(Mth.cos(state.walkAnimationPos * .6662F)) * state.walkAnimationSpeed * .12F;
                } }
                case NONE -> {}
            }
            stack.pushPose();
            model.root().translateAndRotate(stack);
            bone(model, p.bone()).translateAndRotate(stack);
            // The same transform a posed ModelPart applies: pivot, then Z*Y*X rotation, then scale.
            stack.translate(p.pivot().x() / 16F, p.pivot().y() / 16F, p.pivot().z() / 16F);
            float xRot = r.x() * Mth.DEG_TO_RAD + swingX, yRot = r.y() * Mth.DEG_TO_RAD, zRot = r.z() * Mth.DEG_TO_RAD + swingZ;
            if (xRot != 0 || yRot != 0 || zRot != 0) stack.rotate(new Quaternionf().rotationZYX(zRot, yRot, xRot));
            if (!scale.equals(Piece.Vec3.ONE)) stack.scale(scale.x(), scale.y(), scale.z());
            draw.accept(s.part(), stack);
            stack.popPose();
        }
    }

    @Override public void submit(PoseStack stack, SubmitNodeCollector collector, int light, ResidentRenderState state, float yRot, float xRot) {
        if (state.outfit == null || state.texture == null || state.isInvisible) return;
        var type = RenderTypes.entityTranslucent(state.texture);
        int overlay = LivingEntityRenderer.getOverlayCoords(state, 0);
        pose(getParentModel(), state, stack, (part, posed) -> collector.submitModelPart(part, posed, type, light, overlay, null));
    }
}
