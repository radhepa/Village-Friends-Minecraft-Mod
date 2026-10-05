package dev.villagefriends.outfit;

import java.util.*;
import static dev.villagefriends.outfit.BodyPart.*;
import static dev.villagefriends.outfit.ColorRole.*;
import static dev.villagefriends.outfit.LayerSlot.*;

/** Fifteen connected starter constructions: stepped hair, fitted cloth, one bottom-owned waist belt. */
final class MaleGeometry {
    private static final Set<Gender> MALE=Set.of(Gender.MALE);
    private static VoxelBox box(String id,BodyPart bone,int layer,float x,float y,float z,float w,float h,float d) {
        return new VoxelBox(id,bone,layer,x,y,z,w,h,d,.015F);
    }
    private static void add(List<MaskedVoxel> out,MaterialMask mask,ColorRole role,String id,BodyPart bone,int layer,
                            float x,float y,float z,float w,float h,float d) {
        out.add(new MaskedVoxel(box(id,bone,layer,x,y,z,w,h,d),mask.cell(role)));
    }
    private static ClothingLayer layer(String id,LayerSlot slot,List<MaskedVoxel> out) { return new ClothingLayer(id,slot,out); }
    static TopGarment top(String id,MaleTopRegistry.Family family,OutfitStyle style,int length,int sleeve,int variant,MaterialMask mask) {
        if (length<10 || length>19 || sleeve<8 || sleeve>10 || variant<0 || variant>4) throw new IllegalArgumentException("Invalid top parameters");
        var shirt=new ArrayList<MaskedVoxel>(); var cloth=new ArrayList<MaskedVoxel>();
        var trim=new ArrayList<MaskedVoxel>(); var metal=new ArrayList<MaskedVoxel>();
        add(shirt,mask,ROLE_SECONDARY,"shirt_body",TORSO,0,-4.02F,.7F,-2.02F,8.04F,10.6F,4.04F);
        boolean open=family!=MaleTopRegistry.Family.TUNIC, vest=family==MaleTopRegistry.Family.VEST;
        float start=vest?2.4F:.7F, half=4.12F, gap=open?1.4F:0, panel=half-gap;
        add(cloth,mask,ROLE_PRIMARY,"coat_back",TORSO,1,-half,start,2.04F,half*2,length-start,.28F);
        for (int side:new int[]{-1,1}) {
            String name=side<0?"left":"right";
            add(cloth,mask,ROLE_PRIMARY,name+"_front",TORSO,1,side<0?-half:gap,start,-2.3F,panel,length-start,.28F);
            add(cloth,mask,ROLE_PRIMARY,name+"_side",TORSO,1,side<0?-half:half-.28F,start,-2.02F,.28F,length-start,4.06F);
            if (length>12) {
                add(trim,mask,ROLE_ACCENT,name+"_coat_hem",TORSO,2,side<0?-half:gap,length-.4F,-2.39F,panel,.4F,.16F);
                add(trim,mask,ROLE_ACCENT,name+"_side_hem",TORSO,2,side<0?-4.2F:4.04F,length-.4F,-2.02F,.16F,.4F,4.2F);
            }
            var bone=side<0?LEFT_ARM:RIGHT_ARM; float armX=bone==LEFT_ARM?-1.04F:-3.04F;
            add(shirt,mask,ROLE_SECONDARY,name+"_shirt_sleeve",bone,0,armX,-1.94F,-2.04F,4.08F,sleeve,4.08F);
            if (!vest) add(cloth,mask,ROLE_PRIMARY,name+"_coat_sleeve",bone,1,armX-.07F,-1.94F,-2.11F,4.22F,sleeve-.45F,4.22F);
            add(trim,mask,ROLE_ACCENT,name+"_sleeve_cuff",bone,2,armX-.1F,sleeve-2.4F,-2.14F,4.28F,.4F,4.28F);
            add(trim,mask,ROLE_ACCENT,name+"_collar_edge",TORSO,2,side<0?-2.8F:1.5F,.5F,-2.42F,1.3F,.45F,.16F);
            if (open) for (int i=0;i<3;i++) add(trim,mask,ROLE_ACCENT,name+"_lapel_"+i,TORSO,2,
                side<0?-2.75F+i*.3F:1.45F-i*.3F,.9F+i*.9F,-2.41F,1.05F,.95F,.17F);
        }
        if (length>12) add(trim,mask,ROLE_ACCENT,"back_coat_hem",TORSO,2,-4.2F,length-.4F,2.22F,8.4F,.4F,.16F);
        for (int i=0;i<(open?3:2);i++) add(metal,mask,ROLE_HARDWARE,"button_"+i,TORSO,3,open?1.5F:-.16F,
            4.5F+i*1.45F,-2.49F,.32F,.32F,.18F);
        return new TopGarment(id,MALE,style,List.of(layer(id+"_shirt",UNDERLAYER,shirt),layer(id+"_cloth",OUTERWEAR,cloth),
            layer(id+"_trim",TRIM,trim),layer(id+"_hardware",HARDWARE,metal)));
    }
    static BottomGarment bottom(String id,MaleBottomRegistry.Family family,Set<OutfitStyle> styles,int length,int variant,MaterialMask mask) {
        if (length<10 || length>12 || variant<0 || variant>4) throw new IllegalArgumentException("Invalid bottom parameters");
        var fabric=new ArrayList<MaskedVoxel>(); var trim=new ArrayList<MaskedVoxel>(); var metal=new ArrayList<MaskedVoxel>();
        float wide=switch(family) { case HEAVY_TROUSERS -> 4.3F; case TRAVEL_BREECHES -> 4.06F; case TAILORED_TROUSERS -> 4.1F; default -> 4.18F; };
        for (var bone:List.of(LEFT_LEG,RIGHT_LEG)) {
            String side=bone==LEFT_LEG?"left":"right";
            add(fabric,mask,ROLE_SECONDARY,side+"_trouser",bone,0,-wide/2,0,-2.04F,wide,length,4.08F);
            add(fabric,mask,ROLE_PRIMARY,side+"_boot_shaft",bone,1,-2.2F,9.7F,-2.18F,4.4F,2.3F,4.36F);
            add(fabric,mask,ROLE_PRIMARY,side+"_boot_toe",bone,1,-2.2F,11.15F,-2.55F,4.4F,.85F,4.73F);
            if (family==MaleBottomRegistry.Family.CUFFED_DENIM) add(fabric,mask,ROLE_PRIMARY,side+"_folded_cuff",bone,1,
                -wide/2-.06F,length-.65F,-2.1F,wide+.12F,.65F,4.2F);
        }
        add(fabric,mask,ROLE_PRIMARY,"waist_facing",TORSO,1,-4.14F,10.7F,-2.12F,8.28F,1.1F,4.24F);
        // This is the outfit's only belt. No detached leg ornaments or second top belt exist.
        add(trim,mask,ROLE_ACCENT,"waist_belt_front",TORSO,2,-4.24F,11.1F,-2.34F,8.48F,.5F,.18F);
        add(trim,mask,ROLE_ACCENT,"waist_belt_back",TORSO,2,-4.24F,11.1F,2.16F,8.48F,.5F,.18F);
        for (int side:new int[]{-1,1}) add(trim,mask,ROLE_ACCENT,side<0?"waist_belt_left":"waist_belt_right",TORSO,2,
            side<0?-4.24F:4.06F,11.1F,-2.16F,.18F,.5F,4.32F);
        add(metal,mask,ROLE_HARDWARE,"belt_buckle",TORSO,3,-.45F,11F,-2.52F,.9F,.7F,.18F);
        return new BottomGarment(id,MALE,styles,List.of(layer(id+"_fabric",BOTTOM,fabric),layer(id+"_trim",TRIM,trim),layer(id+"_hardware",HARDWARE,metal)));
    }
    private MaleGeometry() {}
}
