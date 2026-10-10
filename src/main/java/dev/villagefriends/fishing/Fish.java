package dev.villagefriends.fishing;

import java.util.Locale;
import java.util.Set;

/**
 * One fish from the fish table: where and when it bites ({@link #bites}), how big it grows, how rare it is and
 * how it fights in the catch-bar minigame. Empty condition sets mean "anywhere" or "any time".
 */
public record Fish(String id, String item, String name, Rarity rarity, Set<String> water, Set<String> region, Set<String> time,
                   String weather, Set<String> season, int minSize, int maxSize, Behavior behavior, int difficulty,
                   int food, float saturation, Set<String> flags, String text) {

    public enum Rarity {
        COMMON(60, 0, "Common"), UNCOMMON(24, .08, "Uncommon"), RARE(9, .16, "Rare"), EPIC(3, .25, "Epic"), LEGENDARY(.8, .35, "Legendary");
        /** How often it bites, before luck, bait and the rod. */
        public final double weight;
        /** Each point of luck makes it this much likelier. */
        public final double luck;
        public final String label;
        Rarity(double weight, double luck, String label) { this.weight = weight; this.luck = luck; this.label = label; }
        public int stars() { return ordinal() + 1; }
        public static Rarity byId(String id) { return valueOf(id.toUpperCase(Locale.ROOT)); }
    }

    /** How a fish moves up and down the track in the minigame. */
    public enum Behavior {
        /** Glides between targets. */ SMOOTH,
        /** Changes its mind often. */ MIXED,
        /** Sudden dashes. */ DART,
        /** Hugs the bottom, with short lunges up. */ SINKER,
        /** Rides near the top, ducking down now and then. */ FLOATER;
        public static Behavior byId(String id) { return valueOf(id.toUpperCase(Locale.ROOT)); }
        public String id() { return name().toLowerCase(Locale.ROOT); }
    }

    public boolean legendary() { return rarity == Rarity.LEGENDARY; }
    public boolean existing() { return flags.contains("existing"); }
    public boolean edible() { return food > 0; }
    public boolean shellfish() { return flags.contains("shellfish"); }
    /** Cats and dogs will eat it as a treat. */
    public boolean treat() { return edible() && !flags.contains("notreat") && !flags.contains("poison"); }

    /** Whether it bites here and now. */
    public boolean bites(Spot spot) {
        if (!water.isEmpty() && water.stream().noneMatch(spot.waters()::contains)) return false;
        // Cave fish live only underground, and nothing but cave fish lives in underground water.
        boolean caveFish = water.contains("cave") || water.contains("deepcave");
        if (spot.waters().contains("cave") != caveFish && !water.isEmpty()) return false;
        if (!region.isEmpty() && !region.contains(spot.region())) return false;
        if (!time.isEmpty() && time.stream().noneMatch(spot.times()::contains)) return false;
        switch (weather) {
            case "clear" -> { if (spot.raining()) return false; }
            case "rain" -> { if (!spot.raining()) return false; }
            case "thunder" -> { if (!spot.thundering()) return false; }
            default -> {}
        }
        return season.isEmpty() || spot.season() == null || season.contains(spot.season());
    }

    /** A size picked within its range, in tenths of a centimetre. */
    public int clampSize(double cm) { return (int) Math.round(Math.clamp(cm, minSize, maxSize) * 10); }
}
