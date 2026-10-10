package dev.villagefriends.fishing;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Random;

/**
 * What comes up on the line. First what kind of catch (a fish, junk, or treasure, weighted like vanilla's own
 * fishing table: luck makes junk rarer and treasure likelier, and treasure needs open water), then which fish
 * from those biting here ({@link Fish#bites}), weighted by rarity, luck, bait and the rod, then how big it is.
 * Pure: everything comes in as arguments.
 */
public final class Catches {
    public enum Kind { FISH, JUNK, TREASURE }

    /** What tips the odds: luck (Luck of the Sea, potions, the RPG's Fishing skill), bait, the rod. */
    public record Odds(int luck, Gear.Bait bait, Gear.Tackle tackle, Gear.Rod rod) {
        public static final Odds PLAIN = new Odds(0, null, null, Gear.Rod.PLAIN);
    }

    /** Vanilla's weights: junk 10 (−2 a point of luck), treasure 5 (+2, open water only), fish 85 (−1). */
    public static Kind kind(Random random, int luck, boolean openWater) {
        int junk = Math.max(0, 10 - 2 * luck), treasure = openWater ? Math.max(0, 5 + 2 * luck) : 0, fish = Math.max(1, 85 - luck);
        int roll = random.nextInt(junk + treasure + fish);
        return roll < junk ? Kind.JUNK : roll < junk + treasure ? Kind.TREASURE : Kind.FISH;
    }

    /** How likely this fish is among those biting. */
    public static double weight(Fish f, Odds odds) {
        double w = f.rarity().weight * Math.max(.2, 1 + odds.luck() * f.rarity().luck);
        if (odds.bait() != null) w *= odds.bait().odds(f);
        if (f.rarity().ordinal() >= Fish.Rarity.RARE.ordinal()) w *= odds.rod().rareOdds();
        return w;
    }

    /** A fish biting at this spot, or null when nothing in the table bites here. */
    public static Fish pick(Collection<Fish> table, Spot spot, Odds odds, Random random) {
        List<Fish> biting = new ArrayList<>();
        for (var f : table) if (f.bites(spot)) biting.add(f);
        if (biting.isEmpty()) return null;
        double total = 0;
        for (var f : biting) total += weight(f, odds);
        double roll = random.nextDouble() * total;
        for (var f : biting) { roll -= weight(f, odds); if (roll < 0) return f; }
        return biting.getLast();
    }

    /**
     * Its length, in tenths of a centimetre: most fish are on the small side of their range, luck pushes them
     * bigger, and a perfect catch (the fish never left the zone) adds a little more.
     */
    public static int size(Fish f, Random random, int luck, boolean perfect) {
        double skew = Math.clamp(1.7 - .08 * luck, .9, 2.2);
        double t = Math.pow(random.nextDouble(), skew);
        if (perfect) t = Math.min(1, t + .1);
        return f.clampSize(f.minSize() + (f.maxSize() - f.minSize()) * t);
    }

    /** "54.3 cm". */
    public static String cm(int tenths) { return tenths / 10 + "." + tenths % 10 + " cm"; }

    /** How hard the minigame is for this fish on this gear (0–100 scale, as in the table). */
    public static int difficulty(Fish f) { return f.difficulty(); }

    private Catches() {}
}
