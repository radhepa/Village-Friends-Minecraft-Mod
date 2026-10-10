package dev.villagefriends.stable.ride;

/**
 * How fast a resident's horse goes, pure. A villager on foot moves at its own base speed (0.5) times the walk
 * modifier its routine asks for. On horseback the same modifier would drive the horse at the <b>horse's</b> speed
 * instead (its navigation is the horse's), so a knight would race ahead of the squad on a fast courser and crawl
 * on a draft horse. The modifier is rescaled so the horse covers ground like the walker would: a mounted knight
 * keeps pace with walkers in a mixed squad, and when everyone in the squad rides they trot ({@link #TROT}).
 */
public final class MountedPace {
    /** A villager's base movement speed. */
    public static final double RIDER_BASE = .5;
    /** How much faster a squad goes when every member rides. */
    public static final double TROT = 1.4;
    /** The rescaled modifier never makes a horse crawl or bolt. */
    public static final double MIN = .5, MAX = 3.0;
    /** How much wider mounted followers keep their gaps: a horse is 1.4 blocks wide. */
    public static final double MOUNTED_SPACING = 1.7;

    /**
     * The modifier to give a horse's navigation for a walk at {@code walkModifier}: {@code walkModifier * riderBase /
     * horseSpeed}, times {@link #TROT} when the whole squad is mounted, clamped to {@link #MIN}..{@link #MAX}.
     * A horse with no speed keeps the walk modifier (clamped).
     */
    public static double modifier(double walkModifier, double riderBase, double horseSpeed, boolean squadMounted) {
        if (!(horseSpeed > 0)) return Math.clamp(walkModifier, MIN, MAX);
        return Math.clamp(walkModifier * riderBase / horseSpeed * (squadMounted ? TROT : 1.0), MIN, MAX);
    }

    /** Patrol gap multiplier: wider on horseback. */
    public static double spacing(boolean mounted) { return mounted ? MOUNTED_SPACING : 1.0; }

    /** An errand's time allowance: a head start plus this many ticks per block (a walker covers one in about 7 to 10). */
    public static final long ERRAND_START = 200;
    public static final double TICKS_PER_BLOCK = 12;
    /** Farther than any village reaches: a longer allowance would only keep a resident stuck on a hopeless errand. */
    public static final double ERRAND_BLOCKS = 400;

    /**
     * Ticks a resident gets to walk or ride {@code blocks} (straight-line) to a horse or a stall before giving up:
     * never less than {@code least}, and more for a far one, so a stable on the village's outer streets is still in
     * reach. A distance that isn't a number gets {@code least}.
     */
    public static long errandTicks(double blocks, long least) {
        if (!(blocks > 0)) return least;
        return Math.max(least, ERRAND_START + Math.round(Math.min(blocks, ERRAND_BLOCKS) * TICKS_PER_BLOCK));
    }

    private MountedPace() {}
}
