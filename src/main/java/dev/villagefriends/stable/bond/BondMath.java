package dev.villagefriends.stable.bond;

/**
 * The bond's numbers, pure (no world, no registries) so they can be unit tested. Five tiers by points:
 * 0 Wary 0-99, 1 Familiar 100-249, 2 Trusting 250-499, 3 Loyal 500-799, 4 Devoted 800-1000.
 *
 * <p>The foundation's part ({@link #FLOORS}, {@link #MAX}, {@link #WHISTLE_TIER}, {@link #tier} and
 * {@link #calm}) is frozen: the riders package's spook rule calls {@link #calm}. The breeds package adds the
 * gain rules, tier bonuses and text helpers around them.
 */
public final class BondMath {
    /** The lowest points of each tier. */
    public static final int[] FLOORS = {0, 100, 250, 500, 800};
    public static final int MAX = 1000;
    /** From Loyal up, the Horse Whistle calls the horse. */
    public static final int WHISTLE_TIER = 3;

    /** The tier (0-4) for a number of points. */
    public static int tier(int points) {
        int tier = 0;
        for (int i = 0; i < FLOORS.length; i++) if (points >= FLOORS[i]) tier = i;
        return tier;
    }

    /** How steady a horse is near monsters: its bond tier plus its tack's calm (a Bridle adds 1). */
    public static int calm(int tier, int bridleCalm) { return tier + bridleCalm; }

    private BondMath() {}
}
