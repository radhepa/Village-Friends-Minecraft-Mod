package dev.villagefriends.client;

import dev.villagefriends.animation.AnimationClip;
import dev.villagefriends.animation.AnimationClip.Bone;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.util.Mth;
import org.joml.Matrix3f;
import org.joml.Vector3f;

/**
 * Adds animation pack clips on top of the resident's live pose (vanilla look direction, gait and
 * breathing). The waist bends the upper body at the hips and the root pivots the whole resident at
 * the feet, so bows and leans keep the feet planted. Rendering is single threaded; scratch buffers
 * are reused so posing allocates nothing.
 */
public final class ResidentPoser {
    private static final int BONES = Bone.ALL.length;
    private static final float[] ROT = new float[BONES * 3], POS = new float[BONES * 3], SAMPLE = new float[3];
    private static final Matrix3f TURN = new Matrix3f(), PART = new Matrix3f();
    private static final Vector3f POINT = new Vector3f(), EULER = new Vector3f();

    public static void apply(HumanoidModel<ResidentRenderState> model, ResidentRenderState s) {
        boolean any = false;
        java.util.Arrays.fill(ROT, 0); java.util.Arrays.fill(POS, 0);
        for (var layer : s.layers) if (layer.active()) { accumulate(layer, s); any = true; }
        if (s.turnWeight > 0) {
            model.head.yRot += s.turnYaw * s.turnWeight * Mth.DEG_TO_RAD;
            model.head.xRot += s.turnPitch * s.turnWeight * Mth.DEG_TO_RAD;
        }
        if (!any) return;
        // Children use half-size bodies; clip offsets are written in adult pixels.
        float scale = model.body.getInitialPose().yScale();
        offset(model.head, Bone.HEAD, scale); offset(model.body, Bone.BODY, scale);
        offset(model.rightArm, Bone.RIGHT_ARM, scale); offset(model.leftArm, Bone.LEFT_ARM, scale);
        offset(model.rightLeg, Bone.RIGHT_LEG, scale); offset(model.leftLeg, Bone.LEFT_LEG, scale);
        if (turns(Bone.WAIST)) {
            float hip = (model.rightLeg.getInitialPose().y() + model.leftLeg.getInitialPose().y()) / 2;
            rotation(Bone.WAIST);
            pivot(model.body, 0, hip, 0); pivot(model.head, 0, hip, 0);
            pivot(model.rightArm, 0, hip, 0); pivot(model.leftArm, 0, hip, 0);
        }
        if (turns(Bone.ROOT)) { rotation(Bone.ROOT); pivot(model.root(), 0, 24, 0); }
        int r = Bone.ROOT.ordinal() * 3;
        model.root().x += POS[r] * scale; model.root().y += POS[r + 1] * scale; model.root().z += POS[r + 2] * scale;
    }

    /** Eyelid closure (0..1) and iris offset from the active clips, before the model's own blinking. */
    public static void eyes(ResidentRenderState s, float[] out) {
        out[0] = out[1] = out[2] = 0;
        for (var layer : s.layers) {
            if (!layer.active()) continue;
            var clip = layer.clip;
            if (clip.lid() != null) { clip.lid().sample(layer.time, SAMPLE, 0); out[0] = Math.max(out[0], SAMPLE[0] * layer.weight); }
            if (clip.look() != null) {
                clip.look().sample(layer.time, SAMPLE, 0);
                out[1] += SAMPLE[0] * layer.weight * (layer.mirror ? -1 : 1); out[2] += SAMPLE[1] * layer.weight;
            }
        }
    }

    private static void accumulate(AnimationLayer layer, ResidentRenderState s) {
        AnimationClip clip = layer.clip;
        for (Bone bone : Bone.ALL) {
            var rotation = clip.rotations()[bone.ordinal()]; var position = clip.positions()[bone.ordinal()];
            if (rotation == null && position == null) continue;
            Bone target = layer.mirror ? bone.mirrored() : bone;
            if (!clip.overrideItems() && holding(target, s)) continue;
            float w = layer.weight * (lower(target) ? layer.lowerBody : 1);
            if (w <= 0) continue;
            int i = target.ordinal() * 3; float side = layer.mirror ? -1 : 1;
            if (rotation != null) {
                rotation.sample(layer.time, SAMPLE, 0);
                ROT[i] += SAMPLE[0] * w; ROT[i + 1] += SAMPLE[1] * side * w; ROT[i + 2] += SAMPLE[2] * side * w;
            }
            if (position != null) {
                position.sample(layer.time, SAMPLE, 0);
                POS[i] += SAMPLE[0] * side * w; POS[i + 1] += SAMPLE[1] * w; POS[i + 2] += SAMPLE[2] * w;
            }
        }
    }
    /** An arm carrying an item keeps the vanilla holding pose unless the clip uses the item. */
    private static boolean holding(Bone bone, ResidentRenderState s) {
        return bone == Bone.RIGHT_ARM && s.rightArmPose != HumanoidModel.ArmPose.EMPTY
                || bone == Bone.LEFT_ARM && s.leftArmPose != HumanoidModel.ArmPose.EMPTY;
    }
    private static boolean lower(Bone bone) {
        return bone == Bone.ROOT || bone == Bone.WAIST || bone == Bone.RIGHT_LEG || bone == Bone.LEFT_LEG;
    }
    private static boolean turns(Bone bone) {
        int i = bone.ordinal() * 3;
        return ROT[i] != 0 || ROT[i + 1] != 0 || ROT[i + 2] != 0;
    }
    private static void offset(ModelPart part, Bone bone, float scale) {
        int i = bone.ordinal() * 3;
        part.xRot += ROT[i] * Mth.DEG_TO_RAD; part.yRot += ROT[i + 1] * Mth.DEG_TO_RAD; part.zRot += ROT[i + 2] * Mth.DEG_TO_RAD;
        part.x += POS[i] * scale; part.y += POS[i + 1] * scale; part.z += POS[i + 2] * scale;
    }
    private static void rotation(Bone bone) {
        int i = bone.ordinal() * 3;
        TURN.rotationZYX(ROT[i + 2] * Mth.DEG_TO_RAD, ROT[i + 1] * Mth.DEG_TO_RAD, ROT[i] * Mth.DEG_TO_RAD);
    }
    /** Turns a part about a fixed point in its parent's space, composing with its own rotation. */
    private static void pivot(ModelPart part, float px, float py, float pz) {
        POINT.set(part.x - px, part.y - py, part.z - pz); TURN.transform(POINT);
        part.x = POINT.x + px; part.y = POINT.y + py; part.z = POINT.z + pz;
        PART.rotationZYX(part.zRot, part.yRot, part.xRot);
        TURN.mul(PART, PART).getEulerAnglesZYX(EULER);
        part.setRotation(EULER.x, EULER.y, EULER.z);
    }
    private ResidentPoser() {}
}
