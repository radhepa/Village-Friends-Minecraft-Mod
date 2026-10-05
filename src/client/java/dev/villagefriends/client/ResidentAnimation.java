package dev.villagefriends.client;

import dev.villagefriends.ResidentMotion;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.Pose;

/** The body and equipment share the same poses, including child scaling. */
public final class ResidentAnimation {
    public static boolean canMove(ResidentRenderState s) {
        return s.onGround && s.hasPose(Pose.STANDING) && s.deathTime==0 && !s.isPassenger
                && !s.isInWater && !s.isFallFlying && !s.isCrouching && s.swimAmount==0
                && !s.isUsingItem && s.currentSwing==null;
    }
    public static void apply(HumanoidModel<ResidentRenderState> model, ResidentRenderState s) {
        if(!canMove(s)) return;
        var gait=ResidentMotion.gait(s.motionSeed);
        float unique=ResidentMotion.variation(s.motionSeed), phase=ResidentMotion.phase(s.motionSeed);
        float move=Mth.clamp(s.walkAnimationSpeed, 0, 1);
        float weight=ResidentMotion.smooth(move/.28F);
        float cycle=s.walkAnimationPos*.6662F*gait.cadence*unique*(s.isBaby?1.12F:1);
        float step=Mth.cos(cycle), lift=Mth.sin(cycle*2)*.09F;
        float stride=move*1.4F*gait.stride*(s.isBaby?.87F:1);
        model.rightLeg.xRot=(step+lift)*stride;
        model.leftLeg.xRot=(-step+lift)*stride;
        // Swing from the shoulder, with a slight lag behind the feet.
        float armStep=Mth.cos(cycle-.16F)*move*gait.arms;
        if(s.rightArmPose==HumanoidModel.ArmPose.EMPTY) model.rightArm.xRot=-armStep;
        if(s.leftArmPose==HumanoidModel.ArmPose.EMPTY) model.leftArm.xRot=armStep;
        float breath=Mth.sin(s.ageInTicks*(.055F+.004F*unique)+phase)*(1-weight);
        float roll=Mth.sin(cycle)*gait.sway*weight;
        float bounce=(Mth.cos(cycle*2)-1)*gait.bounce*weight*(s.isBaby?.65F:1);
        model.root().y+=bounce;
        model.root().zRot+=roll;
        model.body.xRot+=gait.lean*weight+breath*.009F;
        float twist=Mth.sin(cycle)*.026F*weight;
        model.body.yRot+=twist;
        model.rightArm.z+=twist*5;
        model.leftArm.z-=twist*5;
        model.head.zRot-=roll*.55F;
        model.head.xRot+=Mth.sin(cycle*2-.3F)*.012F*weight+breath*.008F;
        float idle=Mth.sin(s.ageInTicks*.035F+phase)*.012F*(1-weight);
        model.head.zRot+=idle;
        model.rightArm.zRot+=breath*.012F;
        model.leftArm.zRot-=breath*.012F;
    }
    private ResidentAnimation() {}
}
