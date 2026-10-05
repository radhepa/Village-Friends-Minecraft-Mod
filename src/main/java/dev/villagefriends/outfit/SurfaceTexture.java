package dev.villagefriends.outfit;

import java.util.List;

/** Deterministic HSV microtexture and geometry-derived occlusion, baked once per equipped outfit. */
public final class SurfaceTexture {
    public enum Material { WOVEN, LEATHER, HAIR, METAL }
    public enum Face { TOP, BOTTOM, LEFT, FRONT, RIGHT, BACK }
    public static int pixel(int argb,Material material,int x,int y,int seed,float occlusion,Face face) {
        float random=unit(hash(seed^x*0x1f123bb5^y*0x5f356495))*2-1;
        float pattern=switch(material) {
            case WOVEN -> ((x+y)&1)==0?.022F:-.022F;
            case LEATHER -> unit(hash(seed^((x/2)*31+(y/2)*733)))*.044F-.022F;
            case HAIR -> (x%3==0?.025F:-.0125F);
            case METAL -> (y%3==0?.018F:-.009F);
        };
        float noise=Math.clamp(pattern+random*.025F,-.05F,.05F);
        float light=switch(face) { case BOTTOM -> .84F; case LEFT -> .94F; case RIGHT -> .91F; case BACK -> .95F; default -> 1F; };
        return hsv(argb,1+noise,1+random*.05F,light*(1-Math.clamp(occlusion,0,.2F)));
    }
    /** Multiplicative HSV value/saturation changes keep the role's hue; alpha is independent. */
    public static int hsv(int argb,float valueScale,float saturationScale,float light) {
        int r=(argb>>>16)&255,g=(argb>>>8)&255,b=argb&255;
        float max=Math.max(r,Math.max(g,b)),min=Math.min(r,Math.min(g,b)),range=max-min;
        if (max==0) return argb&0xFF000000;
        float value=Math.clamp(max*valueScale,0,255)*light;
        float saturation=Math.clamp(range/max*saturationScale,0,1);
        int rgb=argb&0xFF000000;
        int[] channels={r,g,b}; int shift=16;
        for (int c:channels) {
            float chroma=range==0?0:(c-min)/range;
            rgb|=Math.clamp(Math.round(value*(1-saturation+saturation*chroma)),0,255)<<shift; shift-=8;
        }
        return rgb;
    }
    private static int hash(int value) { value^=value>>>16;value*=0x7feb352d;value^=value>>>15;value*=0x846ca68b;return value^(value>>>16); }
    private static float unit(int value) { return (value&0xFFFF)/65535F; }
    private static float ox(BodyPart bone) { return switch(bone) { case LEFT_ARM -> 5; case RIGHT_ARM -> -5; case LEFT_LEG -> 1.9F; case RIGHT_LEG -> -1.9F; default -> 0; }; }
    private static float oy(BodyPart bone) { return switch(bone) { case LEFT_ARM,RIGHT_ARM -> 2; case LEFT_LEG,RIGHT_LEG -> 12; default -> 0; }; }
    private static float outside(float value,float min,float max) { return Math.max(0,Math.max(min-value,value-max)); }
    /** Front-facing protruding collars/belts/fringes darken nearby pixels by 15-20%, including across adjacent bones. */
    public static float occlusion(VoxelBox box,Face face,float u,float v,List<VoxelBox> nearby) {
        float x=box.x()+ox(box.bone()),y=box.y()+oy(box.bone()),z=box.z();
        float w=box.width(),h=box.height(),d=box.depth();
        float px=x,py=y,pz=z;
        switch(face) {
            case FRONT -> { px+=u*w;py+=v*h; }
            case BACK -> { px+=(1-u)*w;py+=v*h;pz+=d; }
            case LEFT -> { py+=v*h;pz+=(1-u)*d; }
            case RIGHT -> { px+=w;py+=v*h;pz+=u*d; }
            case TOP -> { px+=u*w;pz+=(1-v)*d; }
            case BOTTOM -> { px+=u*w;py+=h;pz+=v*d; }
        }
        float best=0;
        // Contact between the trouser legs is a baked seam shadow, never an added rectangle.
        if (face==Face.FRONT && box.id().endsWith("_trouser")
            && ((box.bone()==BodyPart.LEFT_LEG && u*box.width()<.55F)
                || (box.bone()==BodyPart.RIGHT_LEG && (1-u)*box.width()<.55F))) best=.17F;
        for (var other:nearby) {
            if (other==box) continue;
            float a=other.x()+ox(other.bone()),b=other.y()+oy(other.bone()),c=other.z();
            float aw=other.width(),bh=other.height(),cd=other.depth(),normalGap,du,dv;
            switch(face) {
                case FRONT -> { normalGap=pz-c;du=outside(px,a,a+aw);dv=outside(py,b,b+bh); }
                case BACK -> { normalGap=c+cd-pz;du=outside(px,a,a+aw);dv=outside(py,b,b+bh); }
                case LEFT -> { normalGap=px-a;du=outside(py,b,b+bh);dv=outside(pz,c,c+cd); }
                case RIGHT -> { normalGap=a+aw-px;du=outside(py,b,b+bh);dv=outside(pz,c,c+cd); }
                case TOP -> { normalGap=py-b;du=outside(px,a,a+aw);dv=outside(pz,c,c+cd); }
                case BOTTOM -> { normalGap=b+bh-py;du=outside(px,a,a+aw);dv=outside(pz,c,c+cd); }
                default -> throw new IllegalStateException();
            }
            float distance=(float)Math.sqrt(du*du+dv*dv);
            if (normalGap>.035F && normalGap<1.85F && distance<1.4F) best=Math.max(best,.15F+.05F*(1-distance/1.4F));
        }
        return best;
    }
    public static Material material(String part,boolean hair) {
        if (hair) return Material.HAIR;
        if (part.contains("boot") || (part.contains("belt") && !part.contains("buckle"))) return Material.LEATHER;
        if (part.contains("button") || part.contains("buckle") || part.contains("clasp") || part.contains("pin")) return Material.METAL;
        return Material.WOVEN;
    }
    private SurfaceTexture() {}
}
