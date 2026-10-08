package dev.villagefriends.talk;

import static org.junit.jupiter.api.Assertions.*;

import dev.villagefriends.routine.Routine;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;
import org.junit.jupiter.api.Test;

class DialogueBankTest {
    static final DialogueBank BANK = DialogueBank.builtin();
    static final List<String> PERSONALITIES = List.of("warmhearted", "thoughtful", "playful", "adventurous", "meticulous", "steadfast",
            "reserved", "imaginative", "pragmatic", "curious", "protective", "gentle");
    static final List<String> JOBS = List.of("farmer", "librarian", "fisherman", "fletcher", "cleric", "cartographer", "armorer", "toolsmith",
            "weaponsmith", "leatherworker", "mason", "shepherd", "butcher", "knight", "archer", "cook", "tavern_keeper", "apothecary", "painter",
            "bard", "tailor", "carpenter", "scholar", "nitwit", "none");
    static final List<String> PERIODS = List.of("dawn", "morning", "noon", "afternoon", "evening", "night", "late");
    static final List<String> HOMES = List.of("plains", "desert", "savanna", "snow", "taiga", "jungle", "swamp");
    static final Set<String> EFFECTS = Set.of("heal", "meal", "shelter", "torch", "cook_held", "mend_held", "directions", "fish", "study",
            "flower", "apple", "bread", "cookie", "seeds", "emerald_tip");

    private static void has(String key) { assertTrue(BANK.has(key), "Missing dialogue pool " + key); }

    @Test void thereAreMoreThanFiveThousandPiecesOfDialogue() {
        int lines = 0;
        for (var pool : BANK.pools().values()) lines += pool.size();
        int asks = 0, replies = 0;
        for (var q : BANK.questions()) { asks += q.ask().size(); replies += q.answers().size(); }
        assertTrue(BANK.size() >= 5000, "At least 5,000 pieces of dialogue: " + BANK.size());
        assertTrue(lines + asks + replies >= 5000, "Even without counting answer labels: " + (lines + asks + replies));
        assertTrue(BANK.questions().size() >= 120, "Plenty of questions: " + BANK.questions().size());
    }

    @Test void noLineIsWrittenTwice() {
        var seen = new HashSet<String>();
        for (var pool : BANK.pools().entrySet()) for (var line : pool.getValue()) assertTrue(seen.add(line), "Duplicate line in " + pool.getKey() + ": " + line);
    }

    @Test void everyPersonalityJobAndMomentHasSomethingToSay() {
        for (String p : PERSONALITIES) { has("chat." + p); has("greet.personality." + p); has("adventure." + p); has("joke." + p); }
        for (String job : JOBS) { has("work." + job); has("joke.job." + job); if (!job.equals("nitwit") && !job.equals("none")) has("station." + job); }
        for (var block : Routine.Block.values()) { has("greet.routine." + block.id()); has("routine." + block.id()); }
        for (String w : List.of("clear", "clearing", "rain", "thunder", "snow", "hot")) has("weather." + w);
        for (String w : List.of("clearing", "rain", "thunder", "snow", "hot")) has("greet.weather." + w);
        for (String period : PERIODS) { has("greet." + period); has("time." + period); has("baby.time." + period); }
        for (String band : List.of("stranger", "acquaintance", "friend", "close", "best")) has("greet.band." + band);
        for (String moon : Talk.MOONS) has("moon." + moon);
        for (String home : HOMES) has("home." + home);
        for (String topic : List.of("greet", "chat", "work", "adventure", "joke", "market")) has("baby." + topic);
        for (String key : List.of("chat.general", "chat.new", "chat.friendly", "chat.close", "work.general", "work.on", "work.off",
                "adventure.general", "adventure.place", "joke.general", "day.market", "day.week", "greet.market")) has(key);
    }

    @Test void questionsAreWellFormedAndAnswersAreRemembered() {
        var ids = new HashSet<String>();
        for (var q : BANK.questions()) {
            assertTrue(ids.add(q.id()), "Unique id " + q.id());
            assertTrue(q.answers().size() >= 2 && q.answers().size() <= 4, q.id());
            for (var a : q.answers()) {
                assertTrue(a.label().length() <= 30, "Short label: " + a.label());
                if (a.effect() != null) assertTrue(EFFECTS.contains(a.effect()), "Known effect " + a.effect());
                if (a.flag() != null) has("remember." + a.flag().replace(':', '_'));
            }
            if (q.offer()) assertTrue(q.answers().stream().anyMatch(a -> a.effect() != null || a.points() > 0), "Offer " + q.id() + " does something");
        }
    }

    @Test void placeholdersCanBeFilled() {
        Map<String, String> all = Map.ofEntries(Map.entry("name", "Mira"), Map.entry("player", "Alex"), Map.entry("village", "Thistlewick"),
                Map.entry("job", "farmer"), Map.entry("hobby", "baking"), Map.entry("love", "cookie"), Map.entry("friend", "Pell"),
                Map.entry("partner", "Rowan"), Map.entry("rival", "Gus"), Map.entry("time", "8:30"), Map.entry("day", "12"), Map.entry("item", "iron sword"),
                Map.entry("biome", "the plains"), Map.entry("moon", "full moon"), Map.entry("market", "tomorrow"), Map.entry("neighbor", "Tamsin"),
                Map.entry("weekday", "Bellday"), Map.entry("celebrant", "Mira"), Map.entry("birthday", "Summer 12"), Map.entry("when", "in 3 days"),
                Map.entry("mobs", "5 zombies"), Map.entry("wanted", "12 wheat"), Map.entry("recipient", "Tobin"), Map.entry("sender", "Mira"),
                Map.entry("season", "Summer"));
        for (var pool : BANK.pools().entrySet()) for (var line : pool.getValue()) {
            String filled = Talk.fill(line, all);
            assertNotNull(filled, "Fillable: " + line);
            assertFalse(filled.contains("{"), "No leftover braces: " + filled);
        }
    }

    @Test void aWholeConversationRarelyRepeats() {
        var context = new Talk.Context("chat", false, "playful", "farmer", 4, "afternoon", "rain", "hobby", false, "full", "plains", "",
                Set.of(), Set.of(), Map.of("name", "Mira", "player", "Alex", "village", "Thistlewick", "hobby", "music", "time", "15:00", "weekday", "Bellday", "market", "in 2 days", "biome", "the plains", "moon", "full moon"));
        var recent = new java.util.ArrayDeque<String>(); var said = new HashSet<String>(); var random = new Random(7);
        for (int i = 0; i < 60; i++) {
            var line = Talk.pick(BANK, context, random, recent);
            assertNotNull(line);
            assertFalse(recent.contains(line.id()), "Not one of the last twelve lines");
            said.add(line.text());
            recent.addLast(line.id()); if (recent.size() > 12) recent.removeFirst();
        }
        assertTrue(said.size() >= 55, "Sixty chats, nearly all different: " + said.size());
    }
}
