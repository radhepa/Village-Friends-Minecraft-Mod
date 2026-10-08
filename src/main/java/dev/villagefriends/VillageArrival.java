package dev.villagefriends;

/**
 * The ten ways the arrival title card greets a player. Each variant is a small line above the
 * village name and/or a small line below it; the village name itself is always the big line.
 */
public final class VillageArrival {
    public record Line(String above, String below) {
        /** The whole greeting as one sentence, for chat-only clients and tests. */
        public String sentence(String village) {
            return (above.isEmpty() ? "" : above + " ") + village + (below.isEmpty() ? "" : " " + below);
        }
    }
    private static final Line[] LINES = {
        new Line("Welcome to", ""),
        new Line("You are now entering", ""),
        new Line("Now entering", ""),
        new Line("You have arrived in", ""),
        new Line("The road leads to", ""),
        new Line("You have reached", ""),
        new Line("Entering the village of", ""),
        new Line("Now arriving in", ""),
        new Line("", "welcomes you"),
        new Line("Rest a while in", ""),
    };
    public static final int VARIANTS = LINES.length;
    public static Line line(int variant) { return LINES[Math.floorMod(variant, VARIANTS)]; }
    /** A different greeting from the last one, so two arrivals in a row never read the same. */
    public static int next(int previous, int roll) {
        if (previous < 0 || previous >= VARIANTS) return Math.floorMod(roll, VARIANTS);
        return (previous + 1 + Math.floorMod(roll, VARIANTS - 1)) % VARIANTS;
    }
    private VillageArrival() {}
}
