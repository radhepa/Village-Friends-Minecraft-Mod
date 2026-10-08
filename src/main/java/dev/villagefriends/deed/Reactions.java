package dev.villagefriends.deed;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashSet;
import java.util.List;

/**
 * What a resident says the first time they see a player after learning about one of their deeds. Pure:
 * picks the deed they bring up and the dialogue pools to say it from; the world fills in the names.
 *
 * <p>Pools: {@code deed.<kind>.self} (it happened to them), {@code .family} (to their family),
 * {@code .seen} or {@code .heard}; now and then (30%) the personality's own take,
 * {@code deed.<good|bad>.<seen|heard>.<personality>}. Children say {@code baby.deed.<kind>.self},
 * {@code baby.deed.<good|bad>.family} or {@code baby.deed.<good|bad>.<seen|heard>}.
 */
public final class Reactions {
    /** Out of 100: how often the deed's own lines are chosen over the personality's. */
    public static final int KIND_WEIGHT = 70;

    /**
     * The deed {@code resident} wants to talk about: one they know of and haven't mentioned, still fresh,
     * closest to them first (it happened to them, their family, they saw it, they heard it), then the
     * biggest, then the newest. Null if none.
     */
    public static Deed pick(List<Deed> deeds, String resident, long today) {
        return deeds.stream().filter(d -> d.fresh(today) && d.knows(resident) && !d.know(resident).told())
                .filter(d -> d.kind() != DeedKind.NOTICE_ANSWERED || d.know(resident).how() != Know.INVOLVED)
                .min(Comparator.comparingInt((Deed d) -> d.know(resident).how())
                        .thenComparing(Comparator.comparingInt((Deed d) -> Math.abs(d.points10())).reversed())
                        .thenComparing(Comparator.comparingLong(Deed::tick).reversed()))
                .orElse(null);
    }

    /** The pools to try, in order, for a reaction to {@code kind} known {@code know}-wise. {@code roll} is 0-99. */
    public static List<String> pools(DeedKind kind, Know know, String personality, boolean child, int roll) {
        String side = kind.good ? "good" : "bad", seen = know.firsthand() ? "seen" : "heard";
        var out = new LinkedHashSet<String>();
        if (child) {
            if (know.how() == Know.INVOLVED) out.add("baby.deed." + kind.id() + ".self");
            if (know.how() == Know.FAMILY) out.add("baby.deed." + side + ".family");
            out.add("baby.deed." + side + "." + seen);
            return List.copyOf(out);
        }
        var own = new ArrayList<String>();
        switch (know.how()) {
            case Know.INVOLVED -> { own.add("deed." + kind.id() + ".self"); own.add("deed." + kind.id() + ".seen"); }
            case Know.FAMILY -> { own.add("deed." + kind.id() + ".family"); own.add("deed." + kind.id() + ".heard"); }
            default -> own.add("deed." + kind.id() + "." + seen);
        }
        String flavor = "deed." + side + "." + seen + "." + personality;
        if (Math.floorMod(roll, 100) >= KIND_WEIGHT) out.add(flavor);
        out.addAll(own);
        out.add(flavor);
        return List.copyOf(out);
    }

    /**
     * Where an Unwelcome player's cold hello comes from: children say {@code baby.greet.unwelcome}; grown-ups
     * their personality's {@code greet.unwelcome.<personality>} now and then (30%), else {@code greet.unwelcome}.
     */
    public static List<String> unwelcome(String personality, boolean child, int roll) {
        if (child) return List.of("baby.greet.unwelcome");
        String own = "greet.unwelcome." + personality;
        return Math.floorMod(roll, 100) >= KIND_WEIGHT ? List.of(own, "greet.unwelcome") : List.of("greet.unwelcome", own);
    }
    /** The Journal line kept for good by someone saved ({@code deed.kept.<kind>.self}) or by their family ({@code .family}). */
    public static String kept(DeedKind kind, boolean family) { return "deed.kept." + kind.id() + (family ? ".family" : ".self"); }

    private Reactions() {}
}
