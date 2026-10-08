package dev.villagefriends.pet;

import java.util.ArrayList;
import java.util.List;

/**
 * The scripts residents and their pets act out together. Each step names the resident's animation
 * phase (a {@code pet} clip tagged {@code play:<phase>}), the pet's trick (a pose in
 * {@code pet_tricks.json}), how long it lasts, how both of them move, and what happens as it starts
 * ({@code |}-separated events). Steps marked {@code until} end early once the pet (or, for the
 * resident's moves, the resident) gets where it's going. Consecutive steps with the same phase keep
 * the resident's clip playing; a new phase starts a new clip.
 */
public final class PetPlays {
    /** How the pair moves during a step. */
    public enum Move {
        /** Both stay put; the pet faces its person. */
        STAY,
        /** The pet comes to stand just in front of its person. */
        FRONT,
        /** The pet comes in front and sits. */
        SIT,
        /** A cat comes in front and lies down (and purrs). */
        LIE,
        /** The pet runs to where the stick landed. */
        FETCH,
        /** The pet runs back to stand in front of its person. */
        RETURN,
        /** The pet scampers in a circle around its person. */
        CIRCLE,
        /** A cat weaves slowly around its person's ankles, tail up. */
        WEAVE,
        /** The resident runs to the next spot around where the game began; the pet chases them. */
        CHASE,
        /** The resident walks up to a stray. */
        APPROACH,
        /** A stray comes close to sniff the resident's outstretched treat (a cat creeps, a dog sits). */
        COAX,
        /** A stray backs off a few blocks. */
        FLEE
    }
    public record Step(String phase, String trick, int ticks, Move move, String events, boolean until) {
        public Step(String phase, String trick, int ticks, Move move, String events) { this(phase, trick, ticks, move, events, false); }
        public List<String> eventList() { return events.isEmpty() ? List.of() : List.of(events.split("\\|")); }
    }
    private static Step s(String phase, String trick, int ticks, Move move) { return new Step(phase, trick, ticks, move, ""); }
    private static Step s(String phase, String trick, int ticks, Move move, String events) { return new Step(phase, trick, ticks, move, events); }
    private static Step until(String phase, String trick, int ticks, Move move, String events) { return new Step(phase, trick, ticks, move, events, true); }

    /** Games that need a few blocks of open, dry ground. */
    public static boolean roomy(String game) { return game.equals("fetch") || game.equals("chase"); }

    /** The script for one game. {@code rounds} repeats the heart of fetch (1 or 2 throws). */
    public static List<Step> game(String game, String treat, int rounds) {
        var steps = new ArrayList<Step>();
        switch (game) {
            case "fetch" -> {
                steps.add(s("fetch_ready", "play_bow", 24, Move.FRONT, "prop:minecraft:stick|bark"));
                for (int i = 0; i < Math.max(1, rounds); i++) {
                    if (i > 0) steps.add(s("fetch_ready", "play_bow", 16, Move.STAY));
                    steps.add(s("throw", "play_bow", 14, Move.STAY));
                    steps.add(until("watch", "", 100, Move.FETCH, "throw|clear_prop"));
                    steps.add(until("watch", "carry", 100, Move.RETURN, "pickup"));
                    steps.add(s("receive", "carry", 14, Move.SIT));
                    steps.add(s("receive", "wag", 22, Move.SIT, "prop:minecraft:stick"));
                }
                steps.add(s("pat_dog", "happy", 40, Move.SIT, "clear_prop|hearts"));
            }
            case "belly_rub" -> {
                steps.add(s("call", "wag", 24, Move.FRONT));
                steps.add(s("belly_rub", "belly_up", 60, Move.STAY));
                steps.add(s("belly_rub", "belly_up", 60, Move.STAY, "hearts"));
                steps.add(s("giggle", "shake_off", 26, Move.STAY));
            }
            case "beg" -> {
                steps.add(s("treat_show", "", 16, Move.SIT, "prop:" + treat));
                steps.add(s("treat_show", "beg", 40, Move.SIT));
                steps.add(s("treat_toss", "beg", 12, Move.SIT));
                steps.add(s("clap", "catch", 16, Move.STAY, "hop|eat|clear_prop"));
                steps.add(s("pat_dog", "wag", 40, Move.SIT, "hearts"));
            }
            case "shake_paw" -> {
                steps.add(s("call", "wag", 20, Move.FRONT));
                steps.add(s("shake_paw", "", 16, Move.SIT));
                steps.add(s("shake_paw", "paw", 44, Move.SIT));
                steps.add(s("pat_dog", "wag", 36, Move.SIT, "hearts"));
            }
            case "spin" -> {
                steps.add(s("call", "wag", 20, Move.FRONT));
                steps.add(s("spin_cue", "spin", 30, Move.STAY));
                steps.add(s("spin_cue", "spin", 30, Move.STAY, "bark"));
                steps.add(s("clap", "happy", 30, Move.STAY, "hop"));
            }
            case "chase" -> {
                steps.add(s("tag", "play_bow", 20, Move.FRONT, "bark"));
                steps.add(until("", "", 70, Move.CHASE, ""));
                steps.add(until("", "", 70, Move.CHASE, ""));
                steps.add(until("", "", 70, Move.CHASE, "bark"));
                steps.add(s("giggle", "happy", 40, Move.FRONT));
            }
            case "string" -> {
                steps.add(s("dangle", "", 24, Move.SIT, "prop:minecraft:string"));
                steps.add(s("dangle", "bat", 50, Move.SIT));
                steps.add(s("dangle", "crouch_wiggle", 24, Move.STAY));
                steps.add(s("dangle", "pounce", 12, Move.STAY, "pounce"));
                steps.add(s("dangle", "bat", 40, Move.SIT));
                steps.add(s("pat_cat", "lean", 36, Move.SIT, "clear_prop|purr"));
            }
            case "stroke" -> {
                steps.add(s("call", "tail_up", 24, Move.FRONT, "meow"));
                steps.add(s("stroke", "", 140, Move.LIE));
                steps.add(s("stroke", "stretch", 26, Move.FRONT));
            }
            case "chin_scratch" -> {
                steps.add(s("call", "tail_up", 24, Move.FRONT));
                steps.add(s("chin_scratch", "lean", 90, Move.SIT, "purr"));
                steps.add(s("pat_cat", "", 30, Move.SIT, "hearts"));
            }
            case "feather" -> {
                steps.add(s("wave_toy", "", 20, Move.FRONT, "prop:minecraft:feather"));
                steps.add(s("wave_toy", "", 60, Move.CIRCLE));
                steps.add(s("wave_toy", "crouch_wiggle", 20, Move.STAY));
                steps.add(s("wave_toy", "pounce", 12, Move.STAY, "pounce"));
                steps.add(s("wave_toy", "", 50, Move.CIRCLE));
                steps.add(s("pat_cat", "tail_up", 30, Move.FRONT, "clear_prop|meow"));
            }
            case "treat" -> {
                steps.add(s("treat_offer", "tail_up", 24, Move.FRONT, "prop:" + treat + "|meow"));
                steps.add(s("treat_offer", "sniff", 24, Move.FRONT));
                steps.add(s("watch_fond", "", 16, Move.STAY, "eat|clear_prop"));
                steps.add(s("watch_fond", "groom", 70, Move.SIT));
            }
            case "weave" -> {
                steps.add(s("watch_fond", "tail_up", 120, Move.WEAVE, "meow"));
                steps.add(s("pat_cat", "lean", 30, Move.SIT, "purr"));
            }
            default -> throw new IllegalArgumentException("Unknown pet game " + game);
        }
        return List.copyOf(steps);
    }

    /** A resident befriending a stray: walk up, offer a treat, and either win them over or watch them back away. */
    public static List<Step> taming(String species, boolean success) {
        boolean cat = species.equals(PetKeeping.CAT);
        var steps = new ArrayList<Step>();
        steps.add(until("", "", 300, Move.APPROACH, ""));
        steps.add(s("coax", "sniff", 70, Move.COAX, "prop:" + PetKeeping.lure(species) + (cat ? "" : "|interested")));
        if (success) {
            steps.add(s("tamed", cat ? "tail_up" : "happy", 44, Move.STAY, "eat|tame|clear_prop"));
            steps.add(s("pat_" + species, cat ? "lean" : "wag", 36, cat ? Move.SIT : Move.SIT, cat ? "purr" : "bark"));
        } else {
            steps.add(s("coax_fail", "", 34, Move.FLEE, "clear_prop|refuse"));
        }
        return List.copyOf(steps);
    }

    /** Every resident phase and pet trick the scripts use, for checking the animation files cover them. */
    public static List<Step> everyStep() {
        var all = new ArrayList<Step>();
        for (String game : PetKeeping.DOG_GAMES) all.addAll(game(game, "minecraft:cooked_beef", 2));
        for (String game : PetKeeping.CAT_GAMES) all.addAll(game(game, "minecraft:cod", 1));
        for (String species : List.of(PetKeeping.CAT, PetKeeping.DOG)) { all.addAll(taming(species, true)); all.addAll(taming(species, false)); }
        return all;
    }
    private PetPlays() {}
}
