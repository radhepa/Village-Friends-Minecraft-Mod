package dev.villagefriends.stable.ride;

/**
 * How a horse reacts to a monster, pure. {@code calm} is {@code BondMath.calm(bond tier, tack calm)}: 0 for a
 * stranger's or a fresh horse, up to 4 for a Devoted one, plus 1 under a Bridle.
 *
 * <ul>
 * <li>A Not-So-Vanilla Mobs challenger within {@link #CHALLENGER_REACH} blocks frightens <b>every</b> horse:
 * calm 0-1 bolts (or throws its rider), calm 2-3 rears, calm 4 and up stands its ground ({@link #standsGround}).</li>
 * <li>Any other monster within {@link #MONSTER_REACH} blocks only bothers a horse someone cares for (a bond
 * partner, or a player's stall) that is still at calm 0: it bolts, or rears under a rider. Wild horses and the
 * village's stable horses keep vanilla's behaviour around ordinary monsters; otherwise every zombie at night
 * would chase the stable horses out of their stalls and raise false "lost horse" flags.</li>
 * </ul>
 * A horse reacts at most once every {@link #COOLDOWN} ticks.
 */
public final class SpookRule {
    /** Strongest last, so a stronger reaction to one monster wins over a weaker one to another. */
    public enum Reaction { NONE, REAR, BOLT, THROW }

    public static final double CHALLENGER_REACH = 16, MONSTER_REACH = 4;
    public static final long COOLDOWN = 200;
    /** From this calm a horse no longer flinches at a challenger (a Devoted horse, or Loyal under a Bridle). */
    public static final int STEADY = 4;

    /**
     * The reaction to one monster {@code distance} blocks away. {@code ridden}: a player is in the saddle (only then
     * can it throw; a bolting horse without a rider just runs). {@code cared}: it has a bond partner or a player's
     * stall.
     */
    public static Reaction react(int calm, boolean challenger, double distance, boolean ridden, boolean cared) {
        if (challenger && distance <= CHALLENGER_REACH) {
            if (calm <= 1) return ridden ? Reaction.THROW : Reaction.BOLT;
            return calm < STEADY ? Reaction.REAR : Reaction.NONE;
        }
        if (cared && calm <= 0 && distance <= MONSTER_REACH) return ridden ? Reaction.REAR : Reaction.BOLT;
        return Reaction.NONE;
    }

    /**
     * A horse steady enough (calm {@value #STEADY} and up) to face a challenger within reach instead of fleeing: it
     * stands its ground and lets out a challenge neigh.
     */
    public static boolean standsGround(int calm, boolean challenger, double distance) {
        return challenger && distance <= CHALLENGER_REACH && calm >= STEADY && react(calm, true, distance, true, true) == Reaction.NONE;
    }

    /** The stronger of two reactions. */
    public static Reaction stronger(Reaction a, Reaction b) { return a.ordinal() >= b.ordinal() ? a : b; }

    /** True when a horse last spooked at {@code last} (negative = never) may spook again at {@code now}. */
    public static boolean ready(long last, long now) { return last < 0 || now - last >= COOLDOWN; }

    private SpookRule() {}
}
