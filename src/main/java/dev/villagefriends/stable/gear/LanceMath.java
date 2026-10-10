package dev.villagefriends.stable.gear;

/**
 * The couched lance's numbers. Pure. The lance is vanilla's kinetic spear with its own tuning in {@code gear.json}:
 * vanilla deals {@link #vanilla} (the attacker's base attack plus the closing speed times the weapon's multiplier,
 * rounded down), and only when the closing speed passes the lance's {@code damage_threshold}, which is set above a
 * sprinting player's speed so the lance lands only from a galloping horse. Stablehand then adds a little for the
 * bond with the horse and whatever add-ons give ({@link #mounted}).
 */
public final class LanceMath {
    /** Blocks per second for one point of a horse's movement-speed attribute (the usual conversion). */
    public static final double BLOCKS_PER_SPEED = 42.16;
    /** A sprinting player on foot covers about this many blocks a second. */
    public static final double SPRINT = 5.612;
    /** Extra damage for each bond tier: a Devoted horse (tier 4) adds 10%. */
    public static final double PER_TIER = 0.025;

    /** Vanilla's kinetic damage: {@code baseAttack + floor(relativeSpeed * multiplier)}, speed in blocks per second. */
    public static double vanilla(double baseAttack, double relativeSpeed, double multiplier) {
        return baseAttack + Math.floor(Math.max(0, relativeSpeed) * multiplier);
    }

    /** A mounted lance hit: the damage times {@code 1 + 0.025 x tier + ridingBonus} (tier 0 to 4, bonus never negative). */
    public static float mounted(float damage, int bondTier, double ridingBonus) {
        return (float) (damage * (1 + PER_TIER * Math.clamp(bondTier, 0, 4) + Math.max(0, ridingBonus)));
    }

    /** Whether a charge is fast enough to land: at least {@code threshold} blocks per second. */
    public static boolean couched(double attackerSpeed, double threshold) { return attackerSpeed >= threshold; }

    /** Horizontal speed in blocks per second from one tick's movement. */
    public static double blocksPerSecond(double dx, double dz) { return Math.sqrt(dx * dx + dz * dz) * 20; }

    /** A horse's top speed in blocks per second from its movement-speed attribute. */
    public static double horseSpeed(double speedAttribute) { return speedAttribute * BLOCKS_PER_SPEED; }

    private LanceMath() {}
}
