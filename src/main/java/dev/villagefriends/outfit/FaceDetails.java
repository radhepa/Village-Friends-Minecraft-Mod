package dev.villagefriends.outfit;

/**
 * The resident face: two pixel-art eye styles, fine brows, a small mouth and, for feminine faces,
 * a lash wing and blush. Every feature is a plane in front of the skin that samples either the
 * native eye row (whites at x 9/14, irises at x 10/13, skin at x 12, all on y 12) or a swatch
 * baked beside the skin at (64..71, 0). Face coordinates are model pixels: x runs from -4 (the
 * viewer's left edge of the face) to 4, y from -8 (top of the head) to 0 (chin).
 */
public final class FaceDetails {
    /** Each resident keeps one eye style for life, chosen from their motion seed. */
    public enum EyeStyle {
        /** Lash line, a tinted-white over dark-pupil row, then a glint over the iris: three rows tall. */
        STARLIT,
        /** Lash line over a glint and the iris: two rows tall, lower and softer. */
        SOFT_GLINT
    }

    public static final int BROW_U=64,LASH_U=65,SHADOW_U=66,TINT_U=67,PUPIL_U=68,LIP_U=69,ROSE_LIP_U=70,BLUSH_U=71,V=0;
    /** The open eye always ends on the bottom of face row 5. */
    public static final float EYE_BOTTOM=-2F;

    public static EyeStyle eyeStyle(int seed) { return (mix(seed^0x51A7E5) & 1)==0 ? EyeStyle.STARLIT : EyeStyle.SOFT_GLINT; }
    /** Women wear the feminine details; non-binary residents get them from their seed. */
    public static boolean feminine(Gender gender,int seed) {
        return switch (gender) { case FEMALE -> true; case MALE -> false; case NON_BINARY -> (mix(seed^0x7E11A5) & 1)==0; };
    }
    /** Top of the open eye, below its lash line. */
    public static float eyeTop(EyeStyle style) { return style==EyeStyle.STARLIT ? -4F : -3F; }
    /** Top of the brows: higher over the taller Starlit eye, always a clear gap above the lashes. */
    public static float browTop(EyeStyle style) { return style==EyeStyle.STARLIT ? -6F : -5.6F; }
    /** The lash line rests on the eye and thins a little as it sweeps down to close it. */
    public static float lashHeight(float blink) { return 1-.4F*blink; }
    public static float lashBottom(EyeStyle style,float blink) { float top=eyeTop(style); return top+(EYE_BOTTOM-top)*blink; }
    /** The feminine wing: below the Starlit lash, above the Soft Glint lash; it joins the closed lash line. */
    public static float wingTop(EyeStyle style,float blink) { float rest=style==EyeStyle.STARLIT ? -4F : -5F; return rest+(-2.8F-rest)*blink; }
    public static float wingHeight(float blink) { return 1-.5F*blink; }

    public static boolean protectedUv(int x,int y) { return y==12 && x>=8 && x<16; }
    /** The baked face swatches beside the skin: per-resident colors, not palette keys. */
    public static boolean swatch(int x,int y) { return y==V && x>=BROW_U && x<=BLUSH_U; }
    public static int brow(int hairRgb) { return shade(0xFF000000|hairRgb,.8F); }
    public static int lash(int hairRgb) { return shade(0xFF000000|hairRgb,.35F); }
    public static int shadow(int skinArgb) { return shade(skinArgb,.9F); }
    /** The Starlit eye's upper white: the iris lifted most of the way to the eye white. */
    public static int tint(int irisArgb,int whiteArgb) { return blend(blend(irisArgb,0xFFFFFFFF,.4F),whiteArgb,.68F); }
    public static int pupil(int irisArgb) { return shade(irisArgb,.5F); }
    public static int lip(int skinArgb) { return blend(shade(skinArgb,.78F),0xFFA04648,.18F); }
    public static int roseLip(int skinArgb) { return blend(shade(skinArgb,.84F),0xFFCD4E62,.42F); }
    public static int blush(int skinArgb) { return blend(skinArgb,0xFFEC6876,.32F); }

    private static int shade(int argb,float factor) {
        int result=argb&0xFF000000;
        for (int shift=16;shift>=0;shift-=8) result|=Math.round(((argb>>>shift)&255)*factor)<<shift;
        return result;
    }
    private static int blend(int from,int to,float amount) {
        int result=from&0xFF000000;
        for (int shift=16;shift>=0;shift-=8) {
            int a=(from>>>shift)&255,b=(to>>>shift)&255;
            result|=Math.round(a+(b-a)*amount)<<shift;
        }
        return result;
    }
    private static int mix(int value) {
        value^=value>>>16; value*=0x7feb352d; value^=value>>>15; value*=0x846ca68b;
        return value^(value>>>16);
    }
    private FaceDetails() {}
}
