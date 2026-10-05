package dev.villagefriends;

import java.util.UUID;

/** Stable, small differences in movement; no randomness or saved-world changes per frame. */
public final class ResidentMotion {
    public enum Gait {
        EASY("Easygoing", .98F, 1.00F, .78F, .20F, .024F, .015F),
        SPRIGHTLY("Sprightly", 1.09F, .90F, .98F, .32F, .033F, .025F),
        MEASURED("Measured", .91F, 1.06F, .58F, .13F, .017F, .032F),
        NIMBLE("Nimble", 1.14F, .84F, .82F, .24F, .022F, .035F),
        UNHURRIED("Unhurried", .93F, .94F, .68F, .15F, .031F, .009F),
        CURIOUS("Curious", 1.02F, .96F, .86F, .23F, .028F, .018F);

        public final String label;
        public final float cadence, stride, arms, bounce, sway, lean;
        Gait(String label, float cadence, float stride, float arms, float bounce, float sway, float lean) {
            this.label=label; this.cadence=cadence; this.stride=stride; this.arms=arms;
            this.bounce=bounce; this.sway=sway; this.lean=lean;
        }
    }

    private static final Gait[] GAITS=Gait.values();
    public static int seed(UUID id) {
        return mix(Long.hashCode(id.getMostSignificantBits() ^ Long.rotateLeft(id.getLeastSignificantBits(), 23)));
    }
    public static Gait gait(int seed) { return GAITS[Math.floorMod(seed, GAITS.length)]; }
    public static float variation(int seed) { return .94F + Math.floorMod(seed >>> 8, 101) * .0012F; }
    public static float phase(int seed) { return Math.floorMod(seed >>> 12, 6283) * .001F; }
    public static int blinkPeriod(int seed) { return 97 + Math.floorMod(seed >>> 3, 67); }
    public static float blink(float age, int seed) {
        int period=blinkPeriod(seed);
        float time=age+Math.floorMod(seed, period);
        int cycle=(int)Math.floor(time/period);
        float local=time-cycle*period;
        // Vary the moment within each cycle, with an occasional natural double blink.
        float start=12+Math.floorMod(mix(seed^cycle), period-28);
        float first=blinkPulse(local-start);
        return Math.floorMod(mix(seed+cycle), 7)==0 ? Math.max(first, blinkPulse(local-start-7)) : first;
    }
    private static float blinkPulse(float time) {
        if(time<0 || time>3.9F) return 0;
        if(time<1.2F) return smooth(time/1.2F);
        if(time<1.5F) return 1;
        return 1-smooth((time-1.5F)/2.4F);
    }
    public static float smooth(float value) {
        float t=Math.max(0, Math.min(1, value)); return t*t*(3-2*t);
    }
    private static int mix(int value) {
        value^=value>>>16; value*=0x7feb352d; value^=value>>>15; value*=0x846ca68b;
        return value^(value>>>16);
    }
    private ResidentMotion() {}
}
