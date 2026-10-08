package dev.villagefriends.tavern;

import dev.villagefriends.routine.Routine;
import dev.villagefriends.routine.Routine.Block;
import java.util.List;
import java.util.Locale;

/**
 * The tavern's rules of the house, pure and unit-tested: where a resident likes to sit, what is on the
 * menu, how long a meal or a drink lasts. {@link Taverns} applies them to the world.
 */
public final class Patronage {
    /** The kinds of seat a tavern has. */
    public enum Kind { CHAIR, STOOL, BENCH, ARMCHAIR }
    /** What a resident is doing at the tavern, shared with clients as {@code <phase>:<item>}. */
    public enum Phase {
        WAIT, EAT, DRINK, DONE, CARRY,
        /** The keeper wiping down a table someone just left. */
        WIPE;
        public String id() { return name().toLowerCase(Locale.ROOT); }
    }
    /** Someone already sitting at a table, as the newcomer sees them. */
    public record Neighbor(int affinity, boolean family, boolean partner, boolean bestFriend, boolean rival, boolean crush) {
        public static final Neighbor STRANGER = new Neighbor(0, false, false, false, false, false);
    }
    /** Everything about a free seat that makes it more or less inviting. */
    public record Choice(Kind kind, boolean hearth, boolean outdoor, int freeAtTable, List<Neighbor> table, double distance) {}
    /** The moment a resident walks in. */
    public record Mood(String personality, Block block, boolean wet, boolean cold, boolean dark) {
        public boolean meal() { return block == Block.LUNCH_TAVERN || block == Block.SUPPER_TAVERN; }
    }

    public static final double CLOSED = Double.NEGATIVE_INFINITY;

    /**
     * How much a resident wants this seat. Partners, family and best friends pull them in, rivals push them
     * away; friendly residents like a busy table and reserved ones a quiet one; the hearth draws people on cold
     * nights, the terrace on fine days; diners would rather have a table than a bar stool.
     *
     * @param jitter 0..1, so two residents with the same view of the room don't always pick the same chair
     */
    public static double score(Mood mood, Choice seat, double jitter) {
        if (seat.outdoor() && (mood.wet() || mood.cold())) return CLOSED;
        int sociable = Routine.sociable(mood.personality());
        double score = jitter * 1.2 - seat.distance() * .05;
        for (var n : seat.table()) {
            if (n.rival()) score -= 8;
            score += Math.max(-4, Math.min(4, n.affinity() / 25.0));
            if (n.partner()) score += 6; else if (n.crush()) score += 2;
            if (n.family()) score += 3;
            if (n.bestFriend()) score += 4;
            boolean stranger = n.affinity() < 10 && !n.family() && !n.partner() && !n.bestFriend();
            score += stranger ? (sociable < 0 ? -.8 : sociable * .2) : .3 + sociable * .3;
        }
        // Someone who keeps to themselves likes a table to themselves; a sociable one doesn't mind sharing.
        if (seat.table().isEmpty()) score += sociable < 0 ? 1.5 : sociable >= 2 ? -.3 : .4;
        // Leave room for friends who are on their way: a bigger table with space to spare is a good bet.
        score += Math.min(3, seat.freeAtTable()) * .1;
        if (seat.hearth()) score += mood.cold() ? 2.5 : mood.dark() ? 1.4 : .4;
        if (seat.outdoor()) score += mood.dark() ? -1.5 : mood.meal() ? 1.0 : .5;
        switch (seat.kind()) {
            case STOOL -> score += mood.meal() ? -1.5 : seat.table().isEmpty() && sociable < 1 ? .9 : .2;
            case ARMCHAIR -> score += mood.meal() ? -1.0 : .8;
            case BENCH -> score += sociable > 0 ? .3 : 0;
            case CHAIR -> {}
        }
        return score;
    }

    // -- the menu ----------------------------------------------------------------------------------

    /** The cook's dishes in the order they come round, one a day; the next one is supper. */
    public static final List<String> DISHES = List.of("villagefriends:hearty_stew", "villagefriends:shepherds_pie",
            "villagefriends:fresh_village_bread", "villagefriends:ploughmans_lunch");
    public static final String TART = "villagefriends:apple_tart", CIDER = "villagefriends:mug_of_cider", COFFEE = "villagefriends:steaming_coffee_mug";

    /** The cook's dish of the day. */
    public static String dishOfTheDay(long day) { return DISHES.get((int) Math.floorMod(day, DISHES.size())); }
    /** Supper is the next dish in the rotation, so lunch and supper differ. */
    public static String supperDish(long day) { return DISHES.get((int) Math.floorMod(day + 1, DISHES.size())); }

    /**
     * What a resident orders, course by course. Lunch and supper start with the cook's dish (a ploughman's
     * lunch when nobody is cooking) and go on to a drink; evenings are drinks, now and then with a tart.
     *
     * @param course 0 for the first thing they order this visit
     * @param cooking whether the cook has the stove going
     */
    public static String order(Block block, int course, long day, int seed, boolean cooking, int roll) {
        boolean coffeeDrinker = Math.floorMod(Routine.mix(seed ^ 0xC0FE), 3) == 0;
        String drink = block == Block.LUNCH_TAVERN ? (coffeeDrinker || roll % 4 == 0 ? COFFEE : CIDER) : coffeeDrinker && roll % 3 == 0 ? COFFEE : CIDER;
        if (block == Block.LUNCH_TAVERN || block == Block.SUPPER_TAVERN) {
            if (course == 0) return !cooking ? "villagefriends:ploughmans_lunch" : block == Block.LUNCH_TAVERN ? dishOfTheDay(day) : supperDish(day);
            if (course == 1) return drink;
            return block == Block.SUPPER_TAVERN && course == 2 && roll % 3 == 0 ? TART : null;
        }
        // An evening out, an afternoon pint, the bard's drink after the show.
        if (course > 0 && roll % 5 == 0) return TART;
        return drink;
    }
    /** Most courses come one after another; an evening's drinks have no end until it's time to go. */
    public static int maxCourses(Block block) {
        return block == Block.LUNCH_TAVERN ? 2 : block == Block.SUPPER_TAVERN ? 3 : 4;
    }
    public static boolean drink(String item) { return item.equals(CIDER) || item.equals(COFFEE); }
    /** "stew", "pie", "bread", "platter", "tart", "cider", "coffee": the animation tag for a dish. */
    public static String kind(String item) {
        return switch (item) {
            case "villagefriends:hearty_stew" -> "stew"; case "villagefriends:shepherds_pie" -> "pie";
            case "villagefriends:fresh_village_bread" -> "bread"; case "villagefriends:ploughmans_lunch" -> "platter";
            case TART -> "tart"; case CIDER -> "cider"; case COFFEE -> "coffee";
            default -> "food";
        };
    }
    /** What is left of it afterwards, on the table or in hand: an empty bowl or mug, or nothing. */
    public static String leftover(String item) {
        return switch (kind(item)) {
            case "stew" -> "minecraft:bowl"; case "cider", "coffee" -> "villagefriends:empty_coffee_mug";
            default -> null;
        };
    }

    // -- timing (ticks) ----------------------------------------------------------------------------

    /** How long a dish takes to eat, or a mug to drink, varying with each resident and course. */
    public static int duration(String item, int roll) {
        int spread = Math.floorMod(roll, 200);
        return drink(item) ? 500 + spread * 2 : kind(item).equals("tart") ? 200 + spread : 360 + spread;
    }
    /** A pause between courses, for talking. */
    public static int pause(Block block, int roll) {
        int spread = Math.floorMod(roll, 160);
        return block == Block.LUNCH_TAVERN ? 40 + spread / 2 : 120 + spread;
    }
    /** Without anyone behind the bar, patrons help themselves after a moment. */
    public static int selfService(int roll) { return 100 + Math.floorMod(roll, 80); }

    /** "wait", "eat:villagefriends:hearty_stew"... and back. */
    public static String state(Phase phase, String item) { return item == null ? phase.id() : phase.id() + ":" + item; }
    public static Phase phase(String state) {
        if (state == null || state.isEmpty()) return null;
        int colon = state.indexOf(':');
        String id = colon < 0 ? state : state.substring(0, colon);
        for (var p : Phase.values()) if (p.id().equals(id)) return p;
        return null;
    }
    public static String item(String state) {
        if (state == null) return null;
        int colon = state.indexOf(':');
        return colon < 0 ? null : state.substring(colon + 1);
    }

    private Patronage() {}
}
