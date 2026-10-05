package dev.villagefriends.outfit;

import java.util.*;
import static dev.villagefriends.outfit.BodyPart.*;
import static dev.villagefriends.outfit.ColorRole.*;
import static dev.villagefriends.outfit.LayerSlot.*;

/** Solid cuboids in bone-local pixels; material colors come exclusively from declared role islands. */
final class FemaleGeometry {
    private static final Set<Gender> FEMALE=Set.of(Gender.FEMALE);
    private static void range(int value,int min,int max) {
        if (value<min || value>max) throw new IllegalArgumentException("Asset parameter out of range");
    }
    private static VoxelBox box(String id,BodyPart bone,int layer,float x,float y,float z,float w,float h,float d) {
        return new VoxelBox(id,bone,layer,x,y,z,w,h,d,.02F);
    }
    private static void strand(List<VoxelBox> out,String id,int depth,float x,float y,float z,float w,float h,float d) {
        // Expand outward/upward while preserving the authored bottom endpoint and backLength.
        for (int layer=1;layer<=depth;layer++) out.add(box(id+"_layer_"+layer,HEAD,layer,
            x-layer*.055F,y-layer*.09F,z-layer*.07F,w+layer*.11F,h+layer*.09F,d+layer*.14F));
    }
    private static MaskedVoxel material(MaterialMask mask,ColorRole role,String id,BodyPart bone,int layer,
                                         float x,float y,float z,float w,float h,float d) {
        return new MaskedVoxel(box(id,bone,layer,x,y,z,w,h,d),mask.cell(role));
    }
    private static void add(List<MaskedVoxel> out,MaterialMask mask,ColorRole role,String id,BodyPart bone,int layer,
                            float x,float y,float z,float w,float h,float d) {
        out.add(material(mask,role,id,bone,layer,x,y,z,w,h,d));
    }
    private static ClothingLayer layer(String id,LayerSlot slot,List<MaskedVoxel> boxes) { return new ClothingLayer(id,slot,boxes); }
    private static void braid(List<VoxelBox> out,String name,int depth,int length,int volume,int variant,float x,float z) {
        int segments=4+length/2+variant%2; float step=(length+2F)/segments, wide=.75F+volume*.28F;
        for (int i=0;i<segments;i++) strand(out,"braid_"+name+"_"+i,depth,x+(i%2)*.24F,-2+i*step,z+(i%2)*.15F,
            wide,step,wide);
    }
    private static void waves(List<VoxelBox> out,String name,int depth,int length,int volume,int variant,boolean sweep) {
        int segments=3+length/3; float step=(length+5F)/segments;
        for (int column=0;column<4;column++) for (int i=0;i<segments;i++) strand(out,name+"_"+column+"_"+i,depth,
            -4.05F+column*2F+(i%2)*.18F+(sweep?i*.06F:0),-5+i*step,3.95F+(column+variant+i)%2*.23F,
            1.85F+volume*.06F,step,.45F+volume*.17F);
    }

    static HairModel hair(String id,FemaleHairRegistry.Geometry shape,int volume,int depth,int length,int variant) {
        range(volume,1,3); range(depth,1,3); range(length,0,14); range(variant,0,4);
        float thick=.3F+volume*.16F, shift=(variant-2)*.14F;
        var cubes=new ArrayList<VoxelBox>();
        cubes.add(box("scalp",HEAD,0,-4.06F,-8.22F,-4.06F,8.12F,1.05F+volume*.12F,8.12F));
        cubes.add(box("nape",HEAD,0,-4.1F,-7.3F,3.7F,8.2F,7.3F,thick));
        for (int side:new int[]{-1,1}) cubes.add(box(side<0?"left_shell":"right_shell",HEAD,0,
            side<0?-4.1F-thick:3.9F,-7.25F,-3.55F,thick,4.1F,7.6F));
        for (int i=0;i<4;i++) strand(cubes,"fringe_"+i,depth,-3.95F+i*1.95F+shift,-8.35F+(i+variant)%2*.15F,
            -4.3F,1.85F,1.55F+(variant%3)*.12F,.6F+volume*.13F);
        switch (shape) {
            case NOBLE_BRAIDS,TWIN_BRAID -> {
                for (int side:new int[]{-1,1}) braid(cubes,side<0?"left":"right",depth,length,volume,variant,
                    side<0?-4.7F:3.65F,shape==FemaleHairRegistry.Geometry.NOBLE_BRAIDS?3.1F:-1.3F);
                if (shape==FemaleHairRegistry.Geometry.NOBLE_BRAIDS) for (int i=0;i<5;i++) strand(cubes,"court_crown_"+i,depth,
                    -4+i*1.65F,-8.05F,-4.55F,1.55F,.9F,.75F);
            }
            case ELEGANT_SIDE_BRAID -> {
                braid(cubes,"side",depth,length,volume,variant,3.7F,-.6F);
                strand(cubes,"swept_part",depth,-3.6F+shift,-8.65F,-3.9F,6.2F,1.2F,2.3F);
            }
            case RELAXED_WAVY,LONG_SWEEPING_LOCKS -> waves(cubes,"wave",depth,length,volume,variant,
                shape==FemaleHairRegistry.Geometry.LONG_SWEEPING_LOCKS);
            case MESSY_BOB -> {
                waves(cubes,"bob",depth,length,volume,variant,false);
                for (int side:new int[]{-1,1}) strand(cubes,side<0?"bob_left":"bob_right",depth,
                    side<0?-4.7F:3.95F,-3.6F,-2.8F,.75F,3.6F+length,3.8F);
            }
            case CROWN_BUN -> {
                for (int i=0;i<6;i++) strand(cubes,"bun_coil_"+i,depth,-1.9F+(i%3)*1.2F+shift,
                    -9.7F+(i/3)*1.15F-variant*.07F,1.7F+volume*.3F,1.15F+volume*.12F,1.25F,1.4F);
                if (length>0) strand(cubes,"loose_nape",depth,-1.4F,-1.5F,4.05F,2.8F,1.5F+length,.65F);
            }
            case BRAIDED_CROWN -> {
                for (int i=0;i<6;i++) strand(cubes,"braid_crown_"+i,depth,-4.4F+i*1.5F,-8.15F+(i%2)*.12F,
                    -4.5F,1.4F,.85F,.8F);
                if (length>0) waves(cubes,"crown_fall",depth,length,volume,variant,false);
            }
            case FISHTAIL_BRAID -> {
                braid(cubes,"fishtail",depth,length,volume,variant,-.65F+shift,4.05F);
                for (int side:new int[]{-1,1}) strand(cubes,side<0?"gather_left":"gather_right",depth,
                    side<0?-3.8F:.5F,-6.5F,3.9F,3.25F,4.9F,.7F);
            }
            case CURLY_CASCADE -> {
                int segments=3+length/2; float step=(length+4F)/segments;
                for (int column=0;column<5;column++) for (int i=0;i<segments;i++) strand(cubes,"curl_"+column+"_"+i,depth,
                    -4.3F+column*1.7F+(i%2)*.18F,-4+i*step,3.8F+(i+column+variant)%2*.4F,
                    1.5F+volume*.1F,step,.8F+volume*.16F);
            }
        }
        var ornaments=new ArrayList<ClothingLayer>(); var mask=RegistrySource.FEMALE.material("horizontal");
        if (shape==FemaleHairRegistry.Geometry.NOBLE_BRAIDS || shape==FemaleHairRegistry.Geometry.TWIN_BRAID
            || shape==FemaleHairRegistry.Geometry.ELEGANT_SIDE_BRAID || shape==FemaleHairRegistry.Geometry.FISHTAIL_BRAID) {
            var ties=new ArrayList<MaskedVoxel>();
            for (int side:shape==FemaleHairRegistry.Geometry.NOBLE_BRAIDS || shape==FemaleHairRegistry.Geometry.TWIN_BRAID?
                new int[]{-1,1}:new int[]{1}) {
                float x=shape==FemaleHairRegistry.Geometry.FISHTAIL_BRAID?-.8F+shift:side<0?-4.7F:3.7F;
                float z=shape==FemaleHairRegistry.Geometry.FISHTAIL_BRAID?4.1F:shape==FemaleHairRegistry.Geometry.NOBLE_BRAIDS?3.1F:
                    shape==FemaleHairRegistry.Geometry.TWIN_BRAID?-1.3F:-.6F;
                add(ties,mask,ROLE_ACCENT,"ribbon_"+(side<0?"l":"r"),HEAD,4,x,length-1.4F,z-.1F,1.6F,.45F,1.65F);
                add(ties,mask,ROLE_HARDWARE,"tie_pin_"+(side<0?"l":"r"),HEAD,5,x+.4F,length-1.45F,z-.3F,.65F,.35F,.3F);
            }
            ornaments.add(layer(id+"_ties",HAIR_ORNAMENT,ties));
        } else if (shape==FemaleHairRegistry.Geometry.CROWN_BUN || shape==FemaleHairRegistry.Geometry.BRAIDED_CROWN) {
            ornaments.add(layer(id+"_pin",HAIR_ORNAMENT,List.of(
                material(mask,ROLE_ACCENT,"ribbon",HEAD,4,-1.9F,-8.5F,4.4F,3.8F,.4F,.3F),
                material(mask,ROLE_HARDWARE,"pin",HEAD,5,-.7F,-8.6F,4.6F,1.4F,.5F,.3F))));
        }
        return new HairModel(id,FEMALE,cubes,ornaments);
    }

    static TopGarment top(String id,FemaleTopRegistry.Family family,OutfitStyle style,int length,int sleeves,int variant,MaterialMask mask) {
        range(length,10,14); range(sleeves,6,10); range(variant,0,8);
        var under=new ArrayList<MaskedVoxel>(); var shell=new ArrayList<MaskedVoxel>();
        var trim=new ArrayList<MaskedVoxel>(); var hardware=new ArrayList<MaskedVoxel>();
        boolean blouse=family==FemaleTopRegistry.Family.OFF_SHOULDER_BLOUSE, mantle=family==FemaleTopRegistry.Family.HOODED_MANTLE;
        float start=blouse?2.6F:1F, spread=4.22F+variant*.018F;
        add(under,mask,ROLE_SECONDARY,"chemise",TORSO,0,-4.04F,start,-2.04F,8.08F,11-start,4.08F);
        for (var bone:List.of(LEFT_ARM,RIGHT_ARM)) {
            String side=bone==LEFT_ARM?"left":"right"; float x=bone==LEFT_ARM?-1.05F:-3.05F;
            float sleeveStart=blouse?.8F:-1.9F;
            add(under,mask,ROLE_SECONDARY,side+"_chemise_sleeve",bone,0,x,sleeveStart,-2.05F,4.1F,sleeves-sleeveStart-1.9F,4.1F);
            add(trim,mask,ROLE_ACCENT,side+"_cuff",bone,2,x-.15F,sleeves-2.3F,-2.2F,4.4F,.5F,4.4F);
            if (family==FemaleTopRegistry.Family.KNIT_SWEATER || family==FemaleTopRegistry.Family.WRAP_TUNIC
                || family==FemaleTopRegistry.Family.EMPIRE_TOP) add(shell,mask,ROLE_PRIMARY,side+"_sleeve",bone,1,
                    x-.1F,-1.85F,-2.15F,4.3F,sleeves-1F,4.3F);
        }
        float bodyStart=family==FemaleTopRegistry.Family.CORSET_VEST?3.2F:blouse?2.6F:.6F;
        float waist=family==FemaleTopRegistry.Family.EMPIRE_TOP?5.1F:9.1F;
        add(shell,mask,ROLE_PRIMARY,"back",TORSO,1,-spread,bodyStart,2.08F,spread*2,length-bodyStart,.4F);
        for (int side:new int[]{-1,1}) {
            add(shell,mask,ROLE_PRIMARY,side<0?"side_left":"side_right",TORSO,1,side<0?-spread:spread-.4F,
                bodyStart,-2.08F,.4F,length-bodyStart,4.16F);
            if (!mantle) add(shell,mask,ROLE_PRIMARY,side<0?"front_left":"front_right",TORSO,1,
                side<0?-spread:family==FemaleTopRegistry.Family.CORSET_VEST?.7F:0,bodyStart,-2.5F,
                family==FemaleTopRegistry.Family.CORSET_VEST?spread-.7F:spread,length-bodyStart,.4F);
        }
        add(trim,mask,ROLE_ACCENT,"waistband",TORSO,2,-4.32F,waist,-2.7F,8.64F,.55F,.3F);
        add(trim,mask,ROLE_ACCENT,"hem",TORSO,2,-spread-.08F,length-.5F,-2.65F,spread*2+.16F,.5F,.28F);
        switch (family) {
            case CORSET_VEST -> {
                for (int i=0;i<4+variant%3;i++) {
                    add(trim,mask,ROLE_ACCENT,"lace_"+i,TORSO,2,i%2==0?-.7F:-.35F,3.6F+i*.8F,-2.77F,1.05F,.2F,.25F);
                    for (int side:new int[]{-1,1}) add(hardware,mask,ROLE_HARDWARE,"eyelet_"+i+"_"+(side<0?"l":"r"),TORSO,3,
                        side<0?-.9F:.65F,3.5F+i*.8F,-2.86F,.25F,.3F,.2F);
                }
                for (int side:new int[]{-1,1}) add(shell,mask,ROLE_PRIMARY,side<0?"strap_left":"strap_right",TORSO,1,
                    side<0?-3.1F:2.3F,.5F,-2.48F,.8F,3.1F,.4F);
            }
            case EMPIRE_TOP -> {
                for (int i=0;i<5;i++) add(shell,mask,ROLE_PRIMARY,"gather_"+i,TORSO,2,-4+i*1.6F,5.7F,-2.7F,
                    1.55F,length-5.7F,.35F+variant*.018F);
                add(trim,mask,ROLE_ACCENT,"empire_bow",TORSO,3,2.4F,5,-3F,1.5F,.8F,.45F);
            }
            case OFF_SHOULDER_BLOUSE -> {
                for (int i=0;i<6;i++) add(under,mask,ROLE_SECONDARY,"neck_ruffle_"+i,TORSO,2,-4.2F+i*1.4F,
                    2.45F+(i%2)*.18F,-2.8F,1.4F,.6F,.45F);
                add(trim,mask,ROLE_ACCENT,"neck_ribbon",TORSO,3,-1.3F,2.85F,-3F,2.6F,.4F,.25F);
            }
            case WRAP_TUNIC -> {
                for (int i=0;i<5;i++) add(under,mask,ROLE_SECONDARY,"wrap_lapel_"+i,TORSO,2,-2.7F+i*.8F,
                    .9F+i*1.65F,-2.85F,1.4F,1.85F,.35F);
                add(trim,mask,ROLE_ACCENT,"wrap_knot",TORSO,3,2.7F,8.8F,-3.1F,1.4F,1,.6F);
                add(trim,mask,ROLE_ACCENT,"wrap_tail",TORSO,3,3.1F,9.6F,-3F,.7F,3+variant*.09F,.35F);
            }
            case HOODED_MANTLE -> {
                add(shell,mask,ROLE_PRIMARY,"hood_cap",HEAD,3,-5.15F,-9.65F,-5.1F,10.3F,.6F,10.4F);
                add(shell,mask,ROLE_PRIMARY,"hood_back",HEAD,3,-5.15F,-9.05F,4.75F,10.3F,8.4F,.55F);
                for (int side:new int[]{-1,1}) {
                    add(shell,mask,ROLE_PRIMARY,side<0?"hood_left":"hood_right",HEAD,3,side<0?-5.15F:4.6F,-9.05F,-4.5F,.55F,8.4F,9.25F);
                    add(under,mask,ROLE_SECONDARY,side<0?"hood_lining_left":"hood_lining_right",HEAD,4,
                        side<0?-4.6F:4.2F,-8.8F,-5.2F,.4F,6.7F,.4F);
                    add(shell,mask,ROLE_PRIMARY,side<0?"mantle_left":"mantle_right",TORSO,2,
                        side<0?-5.1F:1.1F,.4F,-2.75F,4,3.2F,.6F);
                }
                add(trim,mask,ROLE_ACCENT,"mantle_edge",TORSO,3,-5.15F,3.1F,-2.9F,10.3F,.5F,.3F);
            }
            case KNIT_SWEATER -> {
                for (int i=0;i<5+variant%3;i++) add(shell,mask,ROLE_PRIMARY,"knit_rib_"+i,TORSO,2,-3.9F+i*1.1F,
                    1.5F,-2.68F,.3F,length-2.1F,.25F);
                add(under,mask,ROLE_SECONDARY,"rolled_collar",TORSO,2,-2.4F,.25F,-2.8F,4.8F,1.1F,.55F);
            }
        }
        add(hardware,mask,ROLE_HARDWARE,"clasp",TORSO,4,-.55F,mantle?1.5F:waist-.05F,-3.2F,1.1F,.65F,.3F);
        if (variant%2==1) add(shell,mask,ROLE_PRIMARY,"pocket",TORSO,2,-3.8F,6.2F+variant*.1F,-2.95F,2.1F,2,.4F);
        if (variant>=4) for (int i=0;i<variant-2;i++) add(hardware,mask,ROLE_HARDWARE,"button_"+i,TORSO,3,
            1.3F,2.2F+i*1.15F,-2.95F,.35F,.35F,.25F);
        return new TopGarment(id,FEMALE,style,List.of(layer(id+"_under",UNDERLAYER,under),layer(id+"_shell",OUTERWEAR,shell),
            layer(id+"_trim",TRIM,trim),layer(id+"_hardware",HARDWARE,hardware)));
    }

    private static void skirtShell(List<MaskedVoxel> out,MaterialMask mask,String name,ColorRole role,int layer,
                                    float y,float height,float spread,float front) {
        add(out,mask,role,name+"_front",TORSO,layer,-spread,y,-front,spread*2,height,.45F);
        add(out,mask,role,name+"_back",TORSO,layer,-spread,y,front-.45F,spread*2,height,.45F);
        for (int side:new int[]{-1,1}) add(out,mask,role,name+(side<0?"_left":"_right"),TORSO,layer,
            side<0?-spread:spread-.45F,y,-front+.45F,.45F,height,front*2-.9F);
    }
    static BottomGarment bottom(String id,FemaleBottomRegistry.Family family,Set<OutfitStyle> styles,int length,int variant,MaterialMask mask) {
        range(length,9,12); range(variant,0,9);
        var fabric=new ArrayList<MaskedVoxel>(); var trim=new ArrayList<MaskedVoxel>(); var hardware=new ArrayList<MaskedVoxel>();
        boolean trousers=family==FemaleBottomRegistry.Family.FITTED_TROUSERS;
        float waist=family==FemaleBottomRegistry.Family.HIGH_WAIST_SKIRT || (trousers && variant==6)?9.65F:11.3F;
        float hem=11.7F+length, spread=4.45F+variant*.035F;
        if (trousers) {
            for (var bone:List.of(LEFT_LEG,RIGHT_LEG)) {
                String side=bone==LEFT_LEG?"left":"right"; float wide=4.08F+(variant%3)*.07F;
                add(fabric,mask,ROLE_SECONDARY,side+"_leg",bone,0,-wide/2,0,-2.06F,wide,length,4.12F);
                add(fabric,mask,ROLE_PRIMARY,side+"_side_seam",bone,1,bone==LEFT_LEG?1.82F:-2.17F,.5F,-2.12F,.35F,length-1,4.24F);
                add(trim,mask,ROLE_ACCENT,side+"_cuff",bone,2,-wide/2-.06F,length-.5F,-2.18F,wide+.12F,.5F,4.36F);
                if (variant==2 || variant==3 || variant==9) add(fabric,mask,ROLE_PRIMARY,side+"_knee_patch",bone,1,
                    -1.45F,4.5F,-2.35F,2.9F,2.1F,.35F);
                if (variant==7) add(fabric,mask,ROLE_PRIMARY,side+"_pocket",bone,1,bone==LEFT_LEG?1.9F:-2.5F,
                    1.5F,-1.7F,.6F,2.8F,3.4F);
                if (variant==8) add(trim,mask,ROLE_ACCENT,side+"_split_cuff",bone,3,-.3F,length-1.5F,-2.4F,.6F,1.5F,.3F);
                if (variant==1) add(fabric,mask,ROLE_SECONDARY,side+"_front_crease",bone,1,-.16F,.4F,-2.23F,.32F,length-1,.2F);
                if (variant==4) add(trim,mask,ROLE_ACCENT,side+"_ankle_cinch",bone,3,-1.1F,length-1.1F,-2.35F,2.2F,.35F,.25F);
            }
        } else {
            skirtShell(fabric,mask,"underskirt",ROLE_SECONDARY,0,waist,hem-waist,spread,2.65F);
            switch (family) {
                case HIGH_WAIST_SKIRT -> {
                    skirtShell(fabric,mask,"high_waist",ROLE_PRIMARY,1,waist,2.1F,4.3F,2.85F);
                    for (int i=0;i<5;i++) add(fabric,mask,ROLE_SECONDARY,"gather_"+i,TORSO,1,-4.35F+i*1.75F,
                        11.5F,-2.82F,1.7F,hem-11.5F,.3F+variant*.012F);
                    add(trim,mask,ROLE_ACCENT,"cinch_knot",TORSO,3,2.7F,waist+.2F,-3.2F,1.4F,.9F,.6F);
                    add(trim,mask,ROLE_ACCENT,"cinch_tail",TORSO,2,3.1F,waist+.95F,-3.1F,.65F,2.5F+variant*.1F,.35F);
                }
                case LAYERED_LONG_DRESS -> {
                    int tiers=2+variant%2; float step=(hem-waist)/tiers;
                    for (int i=0;i<tiers;i++) skirtShell(fabric,mask,"dress_tier_"+i,i==0?ROLE_PRIMARY:ROLE_SECONDARY,1+i,
                        waist+i*step,step-.35F,spread+.12F*(i+1),2.95F+.12F*i);
                    for (int i=0;i<tiers;i++) add(trim,mask,ROLE_ACCENT,"tier_edge_"+i,TORSO,4,-spread-.2F,
                        waist+(i+1)*step-.65F,-3.2F-i*.12F,spread*2+.4F,.35F,.25F);
                }
                case PLEATED_SKIRT -> {
                    for (int i=0;i<8;i++) add(fabric,mask,i%4==variant%4?ROLE_PRIMARY:ROLE_SECONDARY,"pleat_"+i,TORSO,1,
                        -spread+i*(spread*2/8),waist,-2.95F-(i%2)*.18F,spread*2/8+.03F,hem-waist,.4F);
                }
                case WRAP_ROBE_BOTTOM -> {
                    for (int i=0;i<4;i++) add(fabric,mask,ROLE_PRIMARY,"wrap_overlap_"+i,TORSO,1,-3.2F+i*1.35F,
                        waist+i*.3F,-3.05F-i*.07F,1.45F,hem-waist-i*.3F,.35F);
                    add(trim,mask,ROLE_ACCENT,"robe_sash",TORSO,3,-3.7F,waist+.25F,-3.3F,1.4F,.8F,.6F);
                    add(trim,mask,ROLE_ACCENT,"robe_sash_tail",TORSO,2,-3.35F,waist+.9F,-3.2F,.7F,3+variant*.12F,.3F);
                }
                default -> throw new IllegalArgumentException("Unsupported skirt family");
            }
            add(trim,mask,ROLE_ACCENT,"hem",TORSO,4,-spread-.2F,hem-.45F,-3.6F,spread*2+.4F,.4F,.25F);
            if (variant==1 || variant==7) for (int side:new int[]{-1,1}) add(fabric,mask,ROLE_PRIMARY,
                side<0?"pocket_left":"pocket_right",TORSO,2,side<0?-spread-.35F:spread-.1F,12.3F,-1.7F,.45F,2.5F,3.4F);
            if (variant==4) add(fabric,mask,ROLE_PRIMARY,"split_overlay",TORSO,2,1.3F,12,-3.35F,3.2F,length-1,.4F);
            if (variant==6 || variant==8) add(trim,mask,ROLE_ACCENT,"second_cinch",TORSO,3,-3.7F,waist+.35F,-3.35F,1.3F,.8F,.4F);
        }
        add(trim,mask,ROLE_ACCENT,"waistband",TORSO,3,-4.4F,waist,-3F,8.8F,.55F,.35F);
        add(hardware,mask,ROLE_HARDWARE,"waist_clasp",TORSO,4,-.55F,waist-.05F,-3.4F,1.1F,.7F,.3F);
        for (int i=0;i<1+variant%3;i++) add(hardware,mask,ROLE_HARDWARE,"fastener_"+i,TORSO,4,2.3F,
            waist+.7F+i*.6F,-3.1F,.35F,.35F,.25F);
        return new BottomGarment(id,FEMALE,styles,List.of(layer(id+"_fabric",BOTTOM,fabric),layer(id+"_trim",TRIM,trim),
            layer(id+"_hardware",HARDWARE,hardware)));
    }
    private FemaleGeometry() {}
}
