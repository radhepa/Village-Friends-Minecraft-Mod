package dev.villagefriends.social;

import java.util.Map;

/**
 * Deterministic traits that make each resident and each pair of residents their own: how well two
 * people click, who is open to romance and to whom, how long love takes to grow, and who arrived in
 * the village with family. Everything derives from stable resident IDs, so a village tells the same
 * story after every reload and on every machine.
 */
public final class Chemistry {
    /** Love takes at least this many days of knowing each other, and at most {@link #LOVE_MAX}. */
    public static final int LOVE_MIN = 50, LOVE_MAX = 1000;
    /** About one resident in five is happy on their own and never falls in love. */
    static final int ROMANTIC_PERCENT = 80;
    /** Share of residents who arrive with relatives when a village is first settled. */
    static final int FAMILY_PERCENT = 55;

    // Personalities that tend to click (+) or clash (-), on top of a shared personality's shared hobby.
    private static final Map<String, Double> MATCHES = Map.ofEntries(
            Map.entry("gentle|warmhearted", .2), Map.entry("playful|warmhearted", .15), Map.entry("adventurous|playful", .15),
            Map.entry("adventurous|curious", .2), Map.entry("curious|thoughtful", .15), Map.entry("imaginative|thoughtful", .15),
            Map.entry("meticulous|pragmatic", .2), Map.entry("protective|steadfast", .2), Map.entry("gentle|steadfast", .1),
            Map.entry("reserved|thoughtful", .15), Map.entry("pragmatic|steadfast", .1), Map.entry("gentle|protective", .15),
            Map.entry("curious|imaginative", .1), Map.entry("playful|reserved", -.2), Map.entry("meticulous|playful", -.15),
            Map.entry("imaginative|pragmatic", -.2), Map.entry("adventurous|protective", -.1), Map.entry("imaginative|meticulous", -.15),
            Map.entry("adventurous|reserved", -.1), Map.entry("playful|pragmatic", -.1));

    static long mix(long z) {
        z = (z ^ (z >>> 30)) * 0xbf58476d1ce4e5b9L;
        z = (z ^ (z >>> 27)) * 0x94d049bb133111ebL;
        return z ^ (z >>> 31);
    }
    static long hash(String s) {
        long h = 0xcbf29ce484222325L;
        for (int i = 0; i < s.length(); i++) { h ^= s.charAt(i); h *= 0x100000001b3L; }
        return mix(h);
    }
    public static String pair(String a, String b) { return a.compareTo(b) < 0 ? a + "|" + b : b + "|" + a; }
    static long pairSeed(String a, String b, long salt) {
        String lo = a.compareTo(b) < 0 ? a : b, hi = lo.equals(a) ? b : a;
        return mix(hash(lo) ^ Long.rotateLeft(hash(hi), 21) ^ salt);
    }
    /** A uniform number in [0, 1) from a seed. */
    static double unit(long seed) { return (mix(seed) >>> 11) * 0x1.0p-53; }

    /** How naturally two residents get along, from -1 (oil and water) to 1 (kindred spirits). */
    public static double chemistry(Townsfolk x, Townsfolk y) {
        double spark = unit(pairSeed(x.id(), y.id(), 0x5eed_c4e3L)) * 2 - 1;
        double bonus = x.personality().equals(y.personality()) ? .25 : MATCHES.getOrDefault(pair(x.personality(), y.personality()), 0.0);
        if (x.personality().equals("warmhearted") || y.personality().equals("warmhearted")) bonus += .1;
        return Math.clamp(spark * .75 + bonus, -1, 1);
    }
    public static boolean romantic(String id) { return Math.floorMod(mix(hash(id) ^ 0x10_7e5L), 100) < ROMANTIC_PERCENT; }
    /** "FEMALE", "MALE" or "ANY": whom this resident could fall in love with. */
    public static String attraction(String id, String gender) {
        if (!gender.equals("MALE") && !gender.equals("FEMALE")) return "ANY";
        int roll = (int) Math.floorMod(mix(hash(id) ^ 0xa77_2acL), 100);
        String other = gender.equals("MALE") ? "FEMALE" : "MALE";
        return roll < 82 ? other : roll < 91 ? gender : "ANY";
    }
    static boolean attracted(Townsfolk x, Townsfolk y) {
        String want = attraction(x.id(), x.gender());
        return want.equals("ANY") || want.equals(y.gender());
    }
    public static boolean compatible(Townsfolk x, Townsfolk y) {
        return romantic(x.id()) && romantic(y.id()) && attracted(x, y) && attracted(y, x);
    }
    /** Days two compatible residents must know each other before they can fall in love: 50 to 1000. */
    public static int loveDays(String a, String b) {
        return LOVE_MIN + (int) Math.floorMod(pairSeed(a, b, 0x10_4e_da75L), LOVE_MAX - LOVE_MIN + 1);
    }
    /** Days sweethearts court before marrying: 30 to 150. */
    public static int marryDays(String a, String b) { return 30 + (int) Math.floorMod(pairSeed(a, b, 0x3a_771eL), 121); }
    public static boolean bringsFamily(String id) { return Math.floorMod(mix(hash(id) ^ 0xfa_311eL), 100) < FAMILY_PERCENT; }
    /** Whether two compatible adults who arrive together are a couple rather than siblings. */
    static boolean arriveAsCouple(String a, String b) { return Math.floorMod(pairSeed(a, b, 0xc0_391eL), 100) < 70; }

    private Chemistry() {}
}
