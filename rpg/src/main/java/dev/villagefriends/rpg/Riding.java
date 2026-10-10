package dev.villagefriends.rpg;

import dev.villagefriends.stable.api.StablehandEvents;

/**
 * The Riding skill, through Stablehand's hooks. Distance on horseback trains it (Life's stat tracking, one point
 * per 5 blocks, donkeys and mules too), and so do caring for your horse (half a point for every bond point that
 * grooming or feeding earns) and landing couched lance hits. Each level gives 0.2% horse speed, 1% faster bond
 * growth, 0.4% lance damage and 0.6% steadier aim from horseback: Stablehand asks through {@code RIDING_BONUS}
 * and applies them itself, so a world without this add-on simply gets nothing extra.
 */
final class Riding {
    /** Skill experience per bond point gained by grooming or feeding, and per couched lance hit. */
    static final double CARE_XP = .5, LANCE_XP = 6;

    static void register() {
        StablehandEvents.RIDING_BONUS.register((player, aspect) -> bonus(Rpg.sheet(player).skill(Skill.RIDING), aspect));
        StablehandEvents.BOND_GAINED.register((player, horse, source, amount, before, after) -> {
            if (amount > 0 && (source.equals("groom") || source.equals("feed"))) Progress.skill(player, Skill.RIDING, amount * CARE_XP);
        });
        StablehandEvents.LANCE_HIT.register((player, target, damage, speed) -> Progress.skill(player, Skill.RIDING, LANCE_XP));
    }

    /** The extra fraction a Riding level gives an aspect (0.1 = +10%). */
    static double bonus(int level, StablehandEvents.Aspect aspect) {
        return switch (aspect) {
            case HORSE_SPEED -> level * Balance.RIDING_SPEED;
            case BOND_GAIN -> level * Balance.RIDING_BOND;
            case LANCE_DAMAGE -> level * Balance.RIDING_LANCE;
            case MOUNTED_AIM -> level * Balance.RIDING_AIM;
        };
    }

    private Riding() {}
}
