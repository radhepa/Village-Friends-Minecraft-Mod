package dev.villagefriends.client;

import dev.villagefriends.ResidentMotion;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.Pose;

/** The body and equipment share the same poses, including child scaling. */
public final class ResidentAnimation {
    public static boolean canMove(ResidentRenderState s) {
        return s.onGround && canAnimate(s);
    }
    /** Animation pack clips also play mid-air (a flinch from knockback), but never in vanilla's special poses. */
    public static boolean canAnimate(ResidentRenderState s) {
        return s.hasPose(Pose.STANDING) && s.deathTime==0 && (!s.isPassenger || s.seated)
                && !s.isInWater && !s.isFallFlying && !s.isCrouching && s.swimAmount==0
                && !s.isUsingItem && s.currentSwing==null;
    }
    public static void apply(HumanoidModel<ResidentRenderState> model, ResidentRenderState s) {
        if(s.injured) { injured(model,s); return; }
        if(canMove(s)) gait(model,s);
        if(canAnimate(s)) ResidentPoser.apply(model,s);
    }
    /**
     * Lying hurt: head lolled to one side, one arm across the stomach, the other flung out, a knee raised,
     * and slow, shallow breaths. Which side is which comes from the resident's motion seed.
     */
    private static void injured(HumanoidModel<ResidentRenderState> model, ResidentRenderState s) {
        boolean flip=(s.motionSeed&1)!=0;
        float breath=Mth.sin(s.ageInTicks*.045F+ResidentMotion.phase(s.motionSeed));
        var across=flip?model.leftArm:model.rightArm; var flung=flip?model.rightArm:model.leftArm;
        var bent=flip?model.leftLeg:model.rightLeg; var straight=flip?model.rightLeg:model.leftLeg;
        float out=flip?-1:1;
        model.head.xRot=.12F; model.head.yRot=.55F*out; model.head.zRot=.12F*out;
        model.body.xRot=model.body.yRot=model.body.zRot=0;
        across.xRot=-.55F+breath*.04F; across.yRot=0; across.zRot=-.32F*out;
        flung.xRot=.08F; flung.yRot=0; flung.zRot=-1.05F*out+breath*.02F;
        bent.xRot=-.42F; bent.yRot=0; bent.zRot=.1F*out;
        straight.xRot=.04F; straight.yRot=0; straight.zRot=-.06F*out;
    }
    private static void gait(HumanoidModel<ResidentRenderState> model, ResidentRenderState s) {
        var gait=ResidentMotion.gait(s.motionSeed);
        float unique=ResidentMotion.variation(s.motionSeed), phase=ResidentMotion.phase(s.motionSeed);
        float move=Mth.clamp(s.walkAnimationSpeed, 0, 1);
        float weight=ResidentMotion.smooth(move/.28F), rest=1-weight;
        // Fleeing or hurrying: a forward lean and bigger arm swing once the pace picks up.
        float hurry=ResidentMotion.smooth((move-.5F)/.35F);
        float cycle=s.walkAnimationPos*.6662F*gait.cadence*unique*(s.isBaby?1.12F:1);
        float step=Mth.cos(cycle), lift=Mth.sin(cycle*2)*.09F;
        float stride=move*1.4F*gait.stride*(s.isBaby?.87F:1)*(1+hurry*.15F);
        model.rightLeg.xRot=(step+lift)*stride;
        model.leftLeg.xRot=(-step+lift)*stride;
        // Swing from the shoulder, with a slight lag behind the feet.
        float armStep=Mth.cos(cycle-.16F)*move*gait.arms*(1+hurry*.7F);
        if(s.rightArmPose==HumanoidModel.ArmPose.EMPTY) model.rightArm.xRot=-armStep;
        if(s.leftArmPose==HumanoidModel.ArmPose.EMPTY) model.leftArm.xRot=armStep;
        float breath=Mth.sin(s.ageInTicks*(.055F+.004F*unique)+phase)*rest;
        float roll=Mth.sin(cycle)*gait.sway*weight;
        float bounce=(Mth.cos(cycle*2)-1)*gait.bounce*weight*(s.isBaby?.65F:1);
        model.root().y+=bounce;
        model.root().zRot+=roll;
        model.body.xRot+=gait.lean*weight+breath*.012F+hurry*.13F;
        model.head.xRot-=hurry*.07F;
        float twist=Mth.sin(cycle)*.026F*weight;
        model.body.yRot+=twist;
        model.rightArm.z+=twist*5;
        model.leftArm.z-=twist*5;
        model.head.zRot-=roll*.55F;
        model.head.xRot+=Mth.sin(cycle*2-.3F)*.012F*weight+breath*.01F;
        float idle=Mth.sin(s.ageInTicks*.035F+phase)*.012F*rest;
        model.head.zRot+=idle;
        // Breathing lifts the shoulders a touch.
        model.rightArm.y-=(breath+rest)*.09F;
        model.leftArm.y-=(breath+rest)*.09F;
        model.rightArm.zRot+=breath*.014F;
        model.leftArm.zRot-=breath*.014F;
        // A slow weight shift from hip to hip: the relaxed leg eases out, the torso and head counter-balance.
        float shift=Mth.sin(s.ageInTicks*(.0135F+.002F*unique)+phase*2)*rest;
        model.body.zRot+=shift*.018F;
        model.head.zRot-=shift*.014F;
        model.rightLeg.zRot+=Math.max(0,shift)*.04F;
        model.leftLeg.zRot+=Math.min(0,shift)*.04F;
        model.rightArm.zRot+=shift*.018F;
        model.leftArm.zRot+=shift*.018F;
        // Between the AI's look targets the head keeps drifting, as if taking in the village.
        float drift=(Mth.sin(s.ageInTicks*.021F+phase*3)*.7F+Mth.sin(s.ageInTicks*.047F+phase)*.3F)*rest*(1-s.attention);
        model.head.yRot+=drift*.085F;
        model.head.xRot+=Mth.sin(s.ageInTicks*.017F+phase)*.03F*rest;
    }
    private ResidentAnimation() {}
}
