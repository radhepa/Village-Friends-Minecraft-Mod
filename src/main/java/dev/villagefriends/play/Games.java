package dev.villagefriends.play;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Random;

/**
 * The games the village's children play together, and how a child's free time goes: they play on their
 * own for a while (vanilla's play), get bored, and then either round up the other children for a game or,
 * now and then, go and see what a nearby player is up to. Pure and unit-tested; {@code Playground} runs the
 * games in the world and shares each child's part ({@link #state}) with clients for animation.
 */
public final class Games {
    public enum Game {
        /** One child is "it" and chases the others; whoever is tagged is it next. */
        TAG("Tag", "Playing tag", 2, 6, 2400),
        /** One counts at home base while the others hide behind houses and trees, then goes looking for them. */
        HIDE_AND_SEEK("Hide-and-seek", "Playing hide-and-seek", 2, 6, 3600),
        /** Hands joined in a ring, round and round, and they all fall down. */
        RING("Ring-around-the-rosie", "Playing ring-around-the-rosie", 3, 7, 1500),
        /** A line of children copies everything the leader does. */
        FOLLOW_THE_LEADER("Follow the leader", "Playing follow the leader", 3, 6, 2000),
        /** Two or three children toss a leather ball back and forth. */
        CATCH("Catch", "Playing catch", 2, 3, 2000);

        public final String label, doing; public final int min, max, length;
        Game(String label, String doing, int min, int max, int length) { this.label = label; this.doing = doing; this.min = min; this.max = max; this.length = length; }
        public String id() { return name().toLowerCase(Locale.ROOT); }
        public static Game byId(String id) {
            for (var g : values()) if (g.id().equals(id)) return g;
            return null;
        }
    }

    /** A bored child following a player around to see what they're up to. Not a game, but shared the same way. */
    public static final String CURIOUS = "curious";

    /** Moves the leader shows and the line copies, with their length in ticks (the clips in the Village Life pack match). */
    public enum Move {
        HOP("hop", 54), STAR("star", 56), SPIN("spin", 50), FLAP("flap", 60), STOMP("stomp", 56), SALUTE("salute", 44);
        public final String id; public final int ticks;
        Move(String id, int ticks) { this.id = id; this.ticks = ticks; }
    }

    /** How much a personality likes a game, as a weight. Everyone plays everything; some have favorites. */
    public static int appeal(Game game, String personality) {
        return switch (game) {
            case TAG -> switch (personality) { case "playful", "adventurous" -> 6; case "reserved", "meticulous", "thoughtful" -> 2; default -> 4; };
            case HIDE_AND_SEEK -> switch (personality) { case "imaginative", "curious", "reserved" -> 6; case "playful" -> 5; default -> 4; };
            case RING -> switch (personality) { case "warmhearted", "gentle", "playful" -> 6; case "adventurous", "pragmatic" -> 2; default -> 3; };
            case FOLLOW_THE_LEADER -> switch (personality) { case "steadfast", "protective", "imaginative" -> 5; default -> 3; };
            case CATCH -> switch (personality) { case "pragmatic", "steadfast", "adventurous" -> 5; default -> 3; };
        };
    }

    /**
     * The game a group settles on: one that suits how many they are, weighted by what they each like.
     * The game they just played is much less likely to come up again straight away.
     */
    public static Game choose(int players, List<String> personalities, Game last, Random random) {
        var options = new ArrayList<Game>(); var weights = new ArrayList<Integer>();
        int total = 0;
        for (var game : Game.values()) {
            if (players < game.min) continue;
            int weight = 0;
            for (var p : personalities) weight += appeal(game, p);
            // Catch is for two or three; a big group would rather run about.
            if (game == Game.CATCH && players > game.max) continue;
            if (game == last) weight = Math.max(1, weight / 4);
            options.add(game); weights.add(weight); total += weight;
        }
        if (options.isEmpty()) return null;
        int roll = random.nextInt(total);
        for (int i = 0; i < options.size(); i++) { roll -= weights.get(i); if (roll < 0) return options.get(i); }
        return options.getLast();
    }

    /** Seconds of playing on their own before a child gets bored: the lively ones soonest. */
    public static int boredAfter(String personality) {
        return switch (personality) {
            case "playful", "adventurous" -> 20;
            case "curious", "imaginative", "warmhearted" -> 30;
            case "reserved", "meticulous", "thoughtful" -> 55;
            default -> 40;
        };
    }

    /**
     * Out of 100, how likely a bored child is to go and follow a nearby player around instead of starting a game.
     * Curious children are the likeliest; with nobody else to play with, everyone is more tempted.
     */
    public static int curiosity(String personality, boolean playmates) {
        int base = switch (personality) {
            case "curious" -> 50; case "adventurous", "playful" -> 35; case "imaginative" -> 30; case "warmhearted" -> 25;
            case "gentle", "thoughtful" -> 18; case "meticulous" -> 10; case "reserved" -> 6; default -> 20;
        };
        return playmates ? base : Math.min(90, base + 30);
    }
    /** How long a curious child tags along, in ticks: somewhere between forty seconds and two minutes. */
    public static int curiousFor(Random random) { return 800 + random.nextInt(1600); }
    /** A breather after a game, in ticks, before boredom starts building again. */
    public static int restAfter(Random random) { return 500 + random.nextInt(900); }

    /** What a child is doing in a game, shared with clients: {@code tag:it}, {@code catch:throw:42}, {@code curious:watch}. */
    public static String state(Game game, String role) { return game.id() + ":" + role; }
    public static String curious(String role) { return CURIOUS + ":" + role; }
    /** The game (or {@link #CURIOUS}) part of a state, or null. */
    public static String game(String state) {
        if (state == null || state.isEmpty()) return null;
        int colon = state.indexOf(':');
        return colon < 0 ? state : state.substring(0, colon);
    }
    /** The role part of a state: {@code it}, {@code throw}, {@code do}... or null. */
    public static String role(String state) {
        if (state == null) return null;
        String[] parts = state.split(":", 3);
        return parts.length > 1 ? parts[1] : null;
    }
    /** Whatever follows the role: the move being copied, who the ball is thrown to... or null. */
    public static String detail(String state) {
        if (state == null) return null;
        String[] parts = state.split(":", 3);
        return parts.length > 2 ? parts[2] : null;
    }

    /** "Playing tag", "Hiding", "Following you around": what a child is doing, for the Ledger and conversations. */
    public static String doing(String state) {
        String game = game(state), role = role(state);
        if (game == null) return null;
        if (game.equals(CURIOUS)) return "Following you around";
        var g = Game.byId(game);
        if (g == null) return null;
        if (g == Game.HIDE_AND_SEEK && role != null) {
            switch (role) {
                case "hide", "hidden" -> { return "Hiding"; }
                case "count" -> { return "Counting to twenty"; }
                case "seek" -> { return "Seeking"; }
                default -> {}
            }
        }
        if (g == Game.TAG && "it".equals(role)) return "It, at tag";
        if (g == Game.FOLLOW_THE_LEADER && "lead".equals(role)) return "Leading follow the leader";
        return g.doing;
    }

    private Games() {}
}
