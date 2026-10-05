package dev.villagefriends.client;

import dev.villagefriends.ResidentMotion;
import dev.villagefriends.outfit.BodyPart;
import dev.villagefriends.outfit.FaceDetails;
import dev.villagefriends.outfit.Garment;
import dev.villagefriends.outfit.Piece;
import dev.villagefriends.outfit.Wardrobe;
import java.util.ArrayList;
import java.util.List;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.player.PlayerModel;
import net.minecraft.client.model.geom.*;
import net.minecraft.client.model.geom.builders.*;
import net.minecraft.client.renderer.rendertype.RenderTypes;
import net.minecraft.core.Direction;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.Pose;

/**
 * The player mesh (with its hat/jacket/sleeve/pants overlays carrying painted clothing and hair)
 * plus every wardrobe garment's 3D pieces, baked once; each resident shows only its outfit's.
 */
public final class ResidentModel extends HumanoidModel<ResidentRenderState> {
    private record Attached(Garment garment, Piece piece, ModelPart part) {}
    private final List<Attached> pieces = new ArrayList<>();
    private final ModelPart[] eyes=new ModelPart[2], irises=new ModelPart[2], lids=new ModelPart[2], lowerLids=new ModelPart[2], creases=new ModelPart[2];
    private final ModelPart[] lashes=new ModelPart[2];
    public ResidentModel(boolean baby) {
        super(layer(baby).bakeRoot(), RenderTypes::entityTranslucent);
        for (var garment : Wardrobe.ALL) for (var piece : garment.pieces())
            pieces.add(new Attached(garment, piece, bone(piece.bone()).getChild(partName(garment, piece))));
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
    private static String partName(Garment garment, Piece piece) { return "wardrobe_"+garment.id()+"_"+piece.id(); }
    public static LayerDefinition layer(boolean baby) {
        var mesh=PlayerModel.createMesh(CubeDeformation.NONE,false); var root=mesh.getRoot(); var head=root.getChild("head");
        for (var garment : Wardrobe.ALL) {
            var block=OutfitAtlas.block(garment);
            for (var p : garment.pieces()) {
                var o=p.origin(); var r=p.rotation(); var s=p.scale();
                var pose=PartPose.offsetAndRotation(p.pivot().x(),p.pivot().y(),p.pivot().z(),
                    r.x()*Mth.DEG_TO_RAD,r.y()*Mth.DEG_TO_RAD,r.z()*Mth.DEG_TO_RAD);
                if (!s.equals(Piece.Vec3.ONE)) pose=pose.scaled(s.x(),s.y(),s.z());
                root.getChild(boneName(p.bone())).addOrReplaceChild(partName(garment,p),
                    CubeListBuilder.create().texOffs(block.x()+p.u(),block.y()+p.v())
                        .addBox(o.x(),o.y(),o.z(),p.width(),p.height(),p.depth(),new CubeDeformation(p.inflate())),pose);
            }
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
        super.setupAnim(state); ResidentAnimation.apply(this,state); animateEyes(state);
        boolean helmet=!state.headEquipment.isEmpty(), chest=!state.chestEquipment.isEmpty();
        boolean legs=!state.legsEquipment.isEmpty();
        var outfit=state.outfit;
        hat.visible=outfit!=null && !helmet;
        float forward=Math.min(0,Math.min(leftLeg.xRot,rightLeg.xRot)), backward=Math.max(0,Math.max(leftLeg.xRot,rightLeg.xRot));
        boolean moving=ResidentAnimation.canMove(state);
        for (var attached : pieces) {
            var garment=attached.garment(); var piece=attached.piece(); var part=attached.part();
            boolean worn=outfit!=null && (garment==outfit.hair() || garment==outfit.top() || garment==outfit.bottom()) && outfit.shows(garment,piece);
            boolean covered=switch(garment.kind()) {
                case HAIR -> helmet;
                case TOP -> chest;
                case BOTTOM -> legs || (piece.bone()==BodyPart.TORSO && chest);
            };
            part.visible=worn && !covered;
            if (!part.visible) continue;
            switch (piece.motion()) {
                // Long hems ride on the leading/trailing leg so a stride never pokes through them.
                case FLAP_FRONT -> part.xRot+=forward;
                case FLAP_BACK -> part.xRot+=backward;
                case SWAY -> { if (moving) {
                    part.zRot+=Mth.sin(state.walkAnimationPos*.6662F-.6F)*state.walkAnimationSpeed*.09F;
                    part.xRot+=Math.abs(Mth.cos(state.walkAnimationPos*.6662F))*state.walkAnimationSpeed*.12F;
                } }
                case NONE -> {}
            }
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
