package dev.villagefriends.outfit;

/** Dedicated facial swatches leave the Living Eyes base sampling grid unchanged. */
public final class FaceDetails {
    public static final int BROW_U=64,LASH_U=65,SOCKET_U=66,CHIN_U=67,V=0;
    public static final float BROW_Y=-6.5F,LASH_Y=-4.5F,SOCKET_Y=-2.5F;
    public static boolean protectedUv(int x,int y) { return (y==12 && x>=8 && x<16) || (x==11 && y==14); }
    public static int brow(int hairRgb) { return shade(0xFF000000|hairRgb,.8F); }
    public static int lash(int hairRgb) { return shade(0xFF000000|hairRgb,.35F); }
    public static int shadow(int skinArgb) { return shade(skinArgb,.9F); }
    private static int shade(int argb,float factor) {
        int result=argb&0xFF000000;
        for (int shift=16;shift>=0;shift-=8) result|=Math.round(((argb>>>shift)&255)*factor)<<shift;
        return result;
    }
    private FaceDetails() {}
}
