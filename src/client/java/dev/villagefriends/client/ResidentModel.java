package dev.villagefriends.client;

import dev.villagefriends.ResidentMotion;
import dev.villagefriends.outfit.FaceDetails;
import dev.villagefriends.outfit.FaceDetails.EyeStyle;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.player.PlayerModel;
import net.minecraft.client.model.geom.*;
import net.minecraft.client.model.geom.builders.*;
import net.minecraft.client.renderer.rendertype.RenderTypes;
import net.minecraft.core.Direction;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.Pose;

/**
 * The player mesh, whose hat/jacket/sleeve/pants overlays carry the painted clothing and hair, with
 * the Living Eyes face planes. Garments' 3D pieces are drawn on top of it by {@link WardrobeLayer},
 * so the model stays one body no matter how large the wardrobe grows.
 */
public final class ResidentModel extends HumanoidModel<ResidentRenderState> {
    private final ModelPart[] scleras=new ModelPart[2], pupils=new ModelPart[2], irises=new ModelPart[2], lids=new ModelPart[2];
    private final ModelPart[] lashes=new ModelPart[2], wings=new ModelPart[2], brows=new ModelPart[2], browTails=new ModelPart[2], blushes=new ModelPart[2];
    private final ModelPart mouth, lips;
    public ResidentModel(boolean baby) {
        super(layer(baby).bakeRoot(), RenderTypes::entityTranslucent);
        for (int i=0;i<2;i++) {
            var eye=head.getChild("eye"+i);
            scleras[i]=eye.getChild("sclera"); pupils[i]=eye.getChild("pupil"); irises[i]=eye.getChild("iris");
            lids[i]=eye.getChild("lid"); lashes[i]=eye.getChild("lash"); wings[i]=eye.getChild("wing");
            brows[i]=head.getChild("brow"+i); browTails[i]=head.getChild("browTail"+i); blushes[i]=head.getChild("blush"+i);
        }
        mouth=head.getChild("mouth"); lips=head.getChild("lips");
    }
    public static LayerDefinition layer(boolean baby) {
        var mesh=PlayerModel.createMesh(CubeDeformation.NONE,false); var root=mesh.getRoot(); var head=root.getChild("head");
        for(int i=0;i<2;i++) {
            int side=i==0?-1:1;
            // The eye whites and irises keep sampling the resident's own face row; the upper white,
            // pupil, lashes and brows sample swatches baked from it and the hair color.
            var eye=head.addOrReplaceChild("eye"+i,CubeListBuilder.create(),PartPose.ZERO);
            plane(eye,"sclera",FaceDetails.TINT_U,FaceDetails.V,side*2F,-3.5F,-4.03F,2,1);
            plane(eye,"white",i==0?9:14,12,side*2F,-2.5F,-4.03F,2,1);
            plane(eye,"pupil",FaceDetails.PUPIL_U,FaceDetails.V,side*1.5F,-3.5F,-4.045F,1,1);
            plane(eye,"iris",i==0?10:13,12,side*1.5F,-2.5F,-4.045F,1,1);
            plane(eye,"lid",12,12,side*2F,-4.5F,-4.065F,2,0);
            plane(eye,"lash",FaceDetails.LASH_U,FaceDetails.V,side*2F,-4.5F,-4.08F,2,1);
            plane(eye,"wing",FaceDetails.LASH_U,FaceDetails.V,side*3.5F,-3.5F,-4.08F,1,1);
            plane(head,"brow"+i,FaceDetails.BROW_U,FaceDetails.V,side*2F,-5.725F,-4.03F,2,.55F);
            plane(head,"browTail"+i,FaceDetails.BROW_U,FaceDetails.V,side*2.75F,-5.625F,-4.03F,.5F,.35F);
            plane(head,"blush"+i,FaceDetails.BLUSH_U,FaceDetails.V,side*2.875F,-1.725F,-4.02F,1.25F,.55F);
        }
        plane(head,"mouth",FaceDetails.LIP_U,FaceDetails.V,0,-1.425F,-4.02F,1.5F,.45F);
        plane(head,"lips",FaceDetails.ROSE_LIP_U,FaceDetails.V,0,-1.45F,-4.02F,1,.5F);
        plane(root.getChild("body"),"neckShade",FaceDetails.SHADOW_U,FaceDetails.V,0,.35F,-2.055F,4,.7F);

        var layer=LayerDefinition.create(mesh,OutfitAtlas.WIDTH,OutfitAtlas.HEIGHT);
        return baby?layer.apply(HumanoidModel.BABY_TRANSFORMER):layer;
    }
    private static void plane(PartDefinition parent,String name,int u,int v,float x,float y,float z,float w,float h) {
        parent.addOrReplaceChild(name,CubeListBuilder.create().texOffs(u,v)
            .addBox(-.5F,-.5F,0,1,1,0,java.util.Set.of(Direction.NORTH)),
            PartPose.ZERO.scaled(w,h,1).translated(x,y,z));
    }
    @Override public void setupAnim(ResidentRenderState state) {
        super.setupAnim(state); ResidentAnimation.apply(this,state); animateFace(state);
        // A helmet hides the painted hair layer; WardrobeLayer hides the hair pieces.
        hat.visible=state.outfit!=null && state.headEquipment.isEmpty();
    }
    private final float[] clipEyes=new float[3];
    private void animateFace(ResidentRenderState s) {
        boolean sleeping=s.hasPose(Pose.SLEEPING) || s.deathTime>0;
        // Animation pack clips can squint, close or redirect the eyes (a yawn, a laugh, reading).
        if(ResidentAnimation.canAnimate(s)) ResidentPoser.eyes(s,clipEyes); else clipEyes[0]=clipEyes[1]=clipEyes[2]=0;
        float blink=Mth.clamp(sleeping?1:Math.max(ResidentMotion.blink(s.ageInTicks,s.motionSeed),clipEyes[0]),0,1);
        float phase=ResidentMotion.phase(s.motionSeed);
        float glance=Mth.sin(s.ageInTicks*.031F+phase)*Mth.sin(s.ageInTicks*.013F+phase)*.18F;
        float gazeX=Mth.clamp(s.eyeLookX+glance*(1-s.attention)+clipEyes[1]*.28F,-.28F,.28F);
        float gazeY=Mth.clamp(s.eyeLookY+clipEyes[2]*.12F,-.09F,.09F);

        EyeStyle style=FaceDetails.eyeStyle(s.motionSeed);
        boolean starlit=style==EyeStyle.STARLIT;
        boolean feminine=s.outfit!=null && FaceDetails.feminine(s.outfit.gender(),s.motionSeed);
        float top=FaceDetails.eyeTop(style),bottom=FaceDetails.EYE_BOTTOM;
        float lashHeight=FaceDetails.lashHeight(blink),lashBottom=FaceDetails.lashBottom(style,blink);
        float lidTop=top-1,lidBottom=lashBottom-lashHeight;
        float wingHeight=FaceDetails.wingHeight(blink),wingTop=FaceDetails.wingTop(style,blink);
        float browTop=FaceDetails.browTop(style);
        for(int i=0;i<2;i++) {
            float side=i==0?-1:1,inner=side*1.5F,near=side<0?-3:1,far=side<0?-1:3;
            // The iris rests in the inner column and glances by sliding, trimmed to the eye's edges.
            scleras[i].visible=starlit;
            fit(pupils[i],starlit,inner+gazeX,-3.5F+gazeY,near,far,top,bottom);
            fit(irises[i],true,inner+gazeX,-2.5F+gazeY,near,far,top,bottom);
            // The lash line sweeps down over the eye; the skin lid follows behind it.
            lids[i].visible=lidBottom-lidTop>.001F;
            lids[i].y=(lidTop+lidBottom)/2; lids[i].yScale=lidBottom-lidTop;
            lashes[i].y=lashBottom-lashHeight/2; lashes[i].yScale=lashHeight;
            wings[i].visible=feminine;
            wings[i].y=wingTop+wingHeight/2; wings[i].yScale=wingHeight;
            // Straight, fuller brows for masculine faces; a finer arch with a dipping tail for feminine.
            browTails[i].visible=feminine; blushes[i].visible=feminine;
            if(feminine) {
                brows[i].x=side*1.75F; brows[i].xScale=1.5F; brows[i].y=browTop+.175F; brows[i].yScale=.45F;
                browTails[i].y=browTop+.375F;
            } else brows[i].y=browTop+.275F;
        }
        mouth.visible=!feminine; lips.visible=feminine;
    }
    /** Places a one-pixel plane at a center, trimmed to the open eye. */
    private static void fit(ModelPart part,boolean shown,float x,float y,float left,float right,float top,float bottom) {
        float x0=Math.max(x-.5F,left),x1=Math.min(x+.5F,right),y0=Math.max(y-.5F,top),y1=Math.min(y+.5F,bottom);
        part.visible=shown && x1>x0 && y1>y0;
        part.x=(x0+x1)/2; part.y=(y0+y1)/2; part.xScale=Math.max(0,x1-x0); part.yScale=Math.max(0,y1-y0);
    }
}
