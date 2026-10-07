package dev.villagefriends.animation;

import java.util.Set;

/** Pure situation rules shared by the client director and its tests. */
public final class ResidentBehavior {
    /** Village time of day as a pack tag, from the overworld clock. */
    public static String timeTag(long clock) {
        long t = Math.floorMod(clock, 24000L);
        if (t >= 23000 || t < 2500) return "morning";
        if (t < 11000) return "day";
        if (t < 13500) return "evening";
        return "night";
    }
    /** Shared tags for trades that move alike, plus the profession itself. */
    public static void jobTags(String job, Set<String> tags) {
        tags.add("job:" + job);
        switch (job) {
            case "armorer", "toolsmith", "weaponsmith" -> tags.add("smith");
            case "knight", "archer" -> tags.add("guard");
            default -> {}
        }
    }
    /** How restless a personality is: shorter pauses between idles for lively residents. */
    public static float energy(String personality, boolean child) {
        if (child) return 1.6F;
        if (personality == null) return 1;
        return switch (personality) {
            case "playful", "adventurous", "curious" -> 1.35F;
            case "warmhearted", "imaginative", "protective" -> 1.1F;
            case "reserved", "thoughtful", "gentle" -> .8F;
            default -> 1;
        };
    }
    /** Roughly one resident in nine leads with the left hand. */
    public static boolean leftHanded(int seed) { return Math.floorMod(seed >>> 20, 9) == 0; }
    /** Ticks of rest after a clip; lively residents fidget sooner. */
    public static int pause(float energy, float roll) { return Math.round((30 + roll * 90) / energy); }
    private ResidentBehavior() {}
}
