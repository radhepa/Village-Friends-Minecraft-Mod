package dev.villagefriends.client;

import dev.villagefriends.ResidentMotion;
import dev.villagefriends.outfit.BodyPart;
import dev.villagefriends.outfit.FaceDetails;
import java.util.LinkedHashMap;
import java.util.Map;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.player.PlayerModel;
import net.minecraft.client.model.geom.*;
import net.minecraft.client.model.geom.builders.*;
import net.minecraft.client.renderer.rendertype.RenderTypes;
import net.minecraft.core.Direction;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.Pose;

/** New role-masked wardrobe, with solid head geometry and articulated bone attachments. */
public final class ResidentModel extends HumanoidModel<ResidentRenderState> {
    private final Map<OutfitAtlas.Entry, ModelPart> outfitParts = new LinkedHashMap<>();
    private final ModelPart[] eyes=new ModelPart[2], irises=new ModelPart[2], lids=new ModelPart[2], lowerLids=new ModelPart[2], creases=new ModelPart[2];
    private final ModelPart[] lashes=new ModelPart[2];
    public ResidentModel(boolean baby) {
        super(layer(baby).bakeRoot(), RenderTypes::entityTranslucent);
        for (var entry : OutfitAtlas.ENTRIES) outfitParts.put(entry, bone(entry.box().bone()).getChild(entry.partName()));
        for (int i=0;i<2;i++) {
            eyes[i]=head.getChild("eye"+i); irises[i]=eyes[i].getChild("iris"); lids[i]=eyes[i].getChild("lid");
            lowerLids[i]=eyes[i].getChild("lowerLid"); creases[i]=eyes[i].getChild("crease");
            lashes[i]=eyes[i].getChild("lash");
        }
    }
    private ModelPart bone(BodyPart bone) {
        return switch (bone) {
            case HEAD -> head; case TORSO -> body;
            case LEFT_ARM -> leftArm; case RIGHT_ARM -> rightArm;
            case LEFT_LEG -> leftLeg; case RIGHT_LEG -> rightLeg;
        };
    }
    private static String boneName(BodyPart bone) {
        return switch (bone) {
            case HEAD -> "head"; case TORSO -> "body";
            case LEFT_ARM -> "left_arm"; case RIGHT_ARM -> "right_arm";
            case LEFT_LEG -> "left_leg"; case RIGHT_LEG -> "right_leg";
        };
    }
    public static LayerDefinition layer(boolean baby) {
        var mesh=PlayerModel.createMesh(CubeDeformation.NONE,false); var root=mesh.getRoot(); var head=root.getChild("head");
        for (var entry : OutfitAtlas.ENTRIES) {
            var b=entry.box(); float pad=b.inflation();
            root.getChild(boneName(b.bone())).addOrReplaceChild(entry.partName(),
                CubeListBuilder.create().texOffs(entry.u(),entry.v()).addBox(0,0,0,entry.tw(),entry.th(),entry.td()),
                PartPose.ZERO.scaled((b.width()+2*pad)/entry.tw(),(b.height()+2*pad)/entry.th(),(b.depth()+2*pad)/entry.td())
                    .translated(b.x()-pad,b.y()-pad,b.z()-pad));
        }
        for(int i=0;i<2;i++) {
            int side=i==0?-1:1;
            // One-pixel swatches from this resident's own face keep their original colors.
            // Patches sample the preserved face region in the new body atlas.
            var eye=head.addOrReplaceChild("eye"+i,CubeListBuilder.create(),PartPose.ZERO);
            plane(eye,"white",i==0?9:14,12,side*2F,-3.5F,-4.025F,2,1);
            plane(eye,"iris",i==0?10:13,12,side*1.75F,-3.5F,-4.045F,.9F,1);
            eye.addOrReplaceChild("lid",CubeListBuilder.create().texOffs(12,12)
                    .addBox(-1,0,0,1,1,0,java.util.Set.of(Direction.NORTH)),
                    PartPose.ZERO.scaled(2,1,1).translated(side*2F+1,-4,-4.065F));
            eye.addOrReplaceChild("lowerLid",CubeListBuilder.create().texOffs(12,12)
                    .addBox(-1,-1,0,1,1,0,java.util.Set.of(Direction.NORTH)),
                    PartPose.ZERO.scaled(2,1,1).translated(side*2F+1,-3,-4.065F));
            plane(eye,"crease",11,14,side*2F,-3.5F,-4.075F,1.45F,.08F);
            plane(head,"brow"+i,FaceDetails.BROW_U,FaceDetails.V,side*2F,FaceDetails.BROW_Y,-4.10F,2,1);
            plane(eye,"lash",FaceDetails.LASH_U,FaceDetails.V,side*2F,FaceDetails.LASH_Y,-4.09F,2,1);
            plane(eye,"socket",FaceDetails.SOCKET_U,FaceDetails.V,side*2F,FaceDetails.SOCKET_Y,-4.08F,2,1);
        }
        plane(head,"chinShade",FaceDetails.CHIN_U,FaceDetails.V,0,-.45F,-4.08F,6,.9F);
        plane(root.getChild("body"),"neckShade",FaceDetails.SOCKET_U,FaceDetails.V,0,.35F,-2.055F,4,.7F);

        var layer=LayerDefinition.create(mesh,OutfitAtlas.WIDTH,OutfitAtlas.HEIGHT);
        return baby?layer.apply(HumanoidModel.BABY_TRANSFORMER):layer;
    }
    private static void plane(PartDefinition parent,String name,int u,int v,float x,float y,float z,float w,float h) {
        parent.addOrReplaceChild(name,CubeListBuilder.create().texOffs(u,v)
            .addBox(-.5F,-.5F,0,1,1,0,java.util.Set.of(Direction.NORTH)),
            PartPose.ZERO.scaled(w,h,1).translated(x,y,z));
    }
    @Override public void setupAnim(ResidentRenderState state) {
        super.setupAnim(state); ResidentAnimation.apply(this,state); animateEyes(state); hat.visible=false;
        boolean helmet=!state.headEquipment.isEmpty(), chest=!state.chestEquipment.isEmpty();
        boolean legs=!state.legsEquipment.isEmpty();
        for (var item : outfitParts.entrySet()) {
            var entry=item.getKey(); var part=item.getValue();
            boolean covered=switch(entry.box().bone()) {
                case HEAD -> helmet;
                case TORSO, LEFT_ARM, RIGHT_ARM -> chest;
                case LEFT_LEG, RIGHT_LEG -> legs;
            };
            part.visible=state.outfit!=null && entry.selected(state.outfit) && !covered;
            if (part.visible && entry.kind().equals("hair") && entry.box().id().startsWith("braid_") && ResidentAnimation.canMove(state))
                part.zRot+=Mth.sin(state.walkAnimationPos*.6662F-.5F)*state.walkAnimationSpeed*.035F;
        }
    }
    private void animateEyes(ResidentRenderState s) {
        boolean sleeping=s.hasPose(Pose.SLEEPING) || s.deathTime>0;
        float blink=sleeping?1:ResidentMotion.blink(s.ageInTicks,s.motionSeed);
        float phase=ResidentMotion.phase(s.motionSeed);
        float glance=Mth.sin(s.ageInTicks*.031F+phase)*Mth.sin(s.ageInTicks*.013F+phase)*.18F;
        float gazeX=Mth.clamp(s.eyeLookX+glance*(1-s.attention),-.28F,.28F);
        float gazeY=Mth.clamp(s.eyeLookY,-.12F,.12F);
        for(int i=0;i<2;i++) {
            irises[i].x+=gazeX;
            // Compress the iris within the original one-pixel eye line, never outside it.
            irises[i].yScale=.82F;
            irises[i].y+=Mth.clamp(gazeY,-.09F,.09F);
            lids[i].visible=blink>.001F;
            lowerLids[i].visible=lids[i].visible;
            lids[i].yScale=lowerLids[i].yScale=blink*.5F;
            lashes[i].y+=blink*.5F;
            creases[i].visible=blink>.65F;
            creases[i].yScale=.08F*ResidentMotion.smooth((blink-.65F)/.35F);
        }
    }
}
