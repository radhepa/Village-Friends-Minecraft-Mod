package dev.villagefriends;

/**
 * Ten friendship levels on top of the five relationship tiers. Each tier spans two levels, so the
 * existing story gates still decide how far points alone can go; each level has a name and unlocks
 * something new to do or hear.
 */
public final class FriendshipLevels {
    public static final int MAX = 10;
    private static final int[] THRESHOLDS = {0, 5, 15, 28, 40, 58, 80, 105, 140, 170, 200};
    private static final String[] NAMES = {"New Neighbor", "Familiar Face", "Acquaintance", "Friendly Neighbor", "Friend",
            "Good Friend", "Close Friend", "Trusted Friend", "Best Friend", "Kindred Spirit", "Lifelong Friend"};
    private static final String[] PERKS = {"", "They'll remember you between visits.", "They share their favorite things, and you can spend time together.",
            "They tell you the village news.", "Adventures together, and picnic invitations.", "Heart-to-heart talks about love and family.",
            "They trust you with village secrets.", "They wave you over with a heart.", "Best-friend greetings.",
            "They save you a small gift each day.", "A friend for life."};
    /** Highest level each tier gate allows, and the lowest level an already-earned tier keeps. */
    private static final int[] GATE_CAP = {3, 3, 5, 7, 10}, TIER_FLOOR = {0, 2, 4, 6, 8};
    /** Levels at which the matching features open. */
    public static final int PREFERENCES = 2, NEWS = 3, HEART_TO_HEART = 5, SECRETS = 6, HEART_GREETING = 7, DAILY_GIFT = 9;

    public static int byPoints(int points) {
        int level = 0;
        while (level < MAX && points >= THRESHOLDS[level + 1]) level++;
        return level;
    }
    public static int level(FriendshipState affinity, BondState bond) {
        int legacy = TIER_FLOOR[Math.clamp(bond.legacyLevel(), 0, 4)];
        return Math.max(legacy, Math.min(byPoints(affinity.points()), GATE_CAP[Math.clamp(bond.gate(), 0, 4)]));
    }
    /** The relationship tier (New Neighbor to Best Friend) a level belongs to. */
    public static int tier(int level) { return level >= 8 ? 4 : level >= 6 ? 3 : level >= 4 ? 2 : level >= 2 ? 1 : 0; }
    public static String name(int level) { return NAMES[Math.clamp(level, 0, MAX)]; }
    public static String perk(int level) { return PERKS[Math.clamp(level, 0, MAX)]; }
    public static int threshold(int level) { return THRESHOLDS[Math.clamp(level, 0, MAX)]; }

    /** What the player needs to do to reach the next level. */
    public static String goal(FriendshipState affinity, BondState bond) {
        int level = level(affinity, bond);
        if (level >= MAX) return "Lifelong friends!";
        int points = affinity.points(), next = threshold(level + 1);
        if (points >= next) return switch (bond.gate()) {
            case 1 -> "Share an experience together (Time) to grow closer.";
            case 2 -> "Hear their personal story (Story) to grow closer.";
            default -> "Finish their story across five visiting days to grow closer.";
        };
        return (next - points) + " more to Lv. " + (level + 1) + ": " + perk(level + 1);
    }
    private FriendshipLevels() {}
}
