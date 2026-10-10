package dev.villagefriends.stable.gear;

/**
 * Steadier shots from horseback. Pure. Two things make mounted archery wild: the bow's own spread
 * ({@link #uncertainty}) and the horse's movement, which vanilla adds to every arrow ({@link #damping} takes part of
 * it back). Any rider gets a little help; a bonded horse (tier 0 Wary to 4 Devoted) and add-ons give more, with caps
 * so a shot is never perfect and an arrow always keeps some of the horse's speed.
 */
public final class ArcheryMath {
    /** The most spread a horse can take away (75%). */
    public static final double MAX_STEADY = 0.75;
    /** The most of the horse's movement a shot can shed (90%). */
    public static final double MAX_DAMPING = 0.9;

    /** The spread a mounted shot is fired with: {@code base x (1 - min(0.75, 0.10 + 0.10 x tier + bonus))}. */
    public static float uncertainty(float base, int bondTier, double ridingBonus) {
        return (float) (base * (1 - Math.min(MAX_STEADY, 0.10 + 0.10 * Math.clamp(bondTier, 0, 4) + Math.max(0, ridingBonus))));
    }

    /** How much of the horse's sideways movement a mounted shot sheds: {@code min(0.9, 0.5 + 0.1 x tier + bonus)}. */
    public static double damping(int bondTier, double ridingBonus) {
        return Math.min(MAX_DAMPING, 0.5 + 0.1 * Math.clamp(bondTier, 0, 4) + Math.max(0, ridingBonus));
    }

    private ArcheryMath() {}
}
