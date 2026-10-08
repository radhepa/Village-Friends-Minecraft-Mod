package dev.villagefriends.talk;

import static org.junit.jupiter.api.Assertions.*;

import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;
import org.junit.jupiter.api.Test;

class TalkTest {
    private static final DialogueBank BANK = DialogueBankTest.BANK;
    private static Talk.Context context(String topic, boolean child, String job, int level, String period, String weather, String routine,
                                        String held, Set<String> states) {
        return new Talk.Context(topic, child, "gentle", job, level, period, weather, routine, false, "new", "plains", held, states, Set.of(),
                Map.of("name", "Mira", "player", "Alex", "village", "Thistlewick", "hobby", "flowers", "time", "9:00", "weekday", "Moonday",
                        "market", "in 5 days", "biome", "the plains", "moon", "new moon", "item", "raw beef"));
    }

    @Test void placeholdersFillOrTheLineIsSkipped() {
        assertEquals("Hello, Alex! Welcome to Thistlewick.", Talk.fill("Hello, {player}! Welcome to {village}.", Map.of("player", "Alex", "village", "Thistlewick")));
        assertNull(Talk.fill("{friend} says hello.", Map.of()), "No best friend yet: skip the line");
        assertEquals("Pell says hello.", Talk.fill("{friend} says hello.", Map.of("friend", "Pell")));
    }

    @Test void timeOfDayAndFriendshipBands() {
        assertEquals("dawn", Talk.period(23500));
        assertEquals("morning", Talk.period(2000));
        assertEquals("noon", Talk.period(6000));
        assertEquals("afternoon", Talk.period(9000));
        assertEquals("evening", Talk.period(12500));
        assertEquals("night", Talk.period(15000));
        assertEquals("late", Talk.period(19000));
        assertEquals("stranger", Talk.band(0)); assertEquals("friend", Talk.band(4)); assertEquals("best", Talk.band(9));
    }

    @Test void theMomentDecidesWhereLinesComeFrom() {
        var rainy = Talk.pools(context("chat", false, "farmer", 3, "afternoon", "rain", "shelter", "", Set.of("wet")));
        assertTrue(rainy.containsKey("weather.rain") && rainy.containsKey("routine.shelter") && rainy.containsKey("player.wet"));
        assertTrue(rainy.get("weather.rain") > rainy.getOrDefault("weather.clear", 0));
        var work = Talk.pools(context("work", false, "cook", 3, "morning", "clear", "work", "", Set.of()));
        assertTrue(work.containsKey("work.cook") && work.containsKey("station.cook") && work.containsKey("work.on"));
        var child = Talk.pools(context("chat", true, "none", 3, "morning", "snow", "play", "", Set.of()));
        assertTrue(child.keySet().stream().allMatch(k -> k.startsWith("baby.")), "Children speak like children: " + child.keySet());
        var greet = Talk.pools(context("greet", false, "mason", 0, "night", "clear", "evening", "sword", Set.of("hurt")));
        assertTrue(greet.containsKey("greet.night") && greet.containsKey("greet.band.stranger") && greet.containsKey("held.sword") && greet.containsKey("player.hurt"));
    }

    @Test void picksCompleteLinesFromTheRightPools() {
        var c = context("work", false, "tavern_keeper", 4, "evening", "clear", "work", "", Set.of());
        var keys = new HashSet<String>(); var random = new Random(3);
        for (int i = 0; i < 200; i++) {
            var line = Talk.pick(BANK, c, random, Set.of());
            assertNotNull(line); assertFalse(line.text().contains("{"));
            keys.add(line.key());
        }
        assertTrue(keys.contains("work.tavern_keeper") && keys.contains("station.tavern_keeper"), "Work talk covers their trade and their station: " + keys);
        assertTrue(keys.stream().allMatch(k -> k.startsWith("work.") || k.startsWith("station.")));
    }

    @Test void questionConditions() {
        var healer = BANK.question("patch_up_healer");
        assertNotNull(healer);
        assertTrue(Talk.eligible(healer, Set.of("hurt", "job:apothecary"), 0));
        assertTrue(Talk.eligible(healer, Set.of("hurt", "job:cleric"), 0), "Either healer");
        assertFalse(Talk.eligible(healer, Set.of("job:apothecary"), 0), "Only when you're hurt");
        var torches = BANK.question("torches_night");
        assertTrue(Talk.eligible(torches, Set.of("night", "dark"), 2));
        assertFalse(Talk.eligible(torches, Set.of("night", "dark", "held:torch"), 2), "Not if you're already holding one");
        assertFalse(Talk.eligible(torches, Set.of("night", "dark"), 1), "Only for friends");
    }

    @Test void offersComeUpOnlyWhenTheyMakeSense() {
        var random = new Random(11);
        var hurtCook = context("chat", false, "cook", 4, "noon", "clear", "work", "raw_food", Set.of("hurt", "hungry"));
        var offered = new HashSet<String>();
        for (int i = 0; i < 300; i++) { var q = Talk.question(BANK, hurtCook, Set.of(), true, random); if (q != null) offered.add(q.id()); }
        assertTrue(offered.containsAll(List.of("cook_for_you", "meal_trade", "patch_up_friend")), "A hurt, hungry friend holding raw meat: " + offered);
        assertFalse(offered.contains("fishing_tip") || offered.contains("torches_night"), "Nothing that doesn't fit: " + offered);
        var fine = context("chat", false, "mason", 0, "noon", "clear", "work", "", Set.of());
        assertNull(Talk.question(BANK, fine, Set.of(), true, random), "A stranger who's fine gets no offers");
        assertNotNull(Talk.question(BANK, fine, Set.of(), false, random), "but may be asked a question");
        var answered = new HashSet<String>();
        for (var q : BANK.questions()) if (!q.offer()) answered.add(q.id());
        assertNull(Talk.question(BANK, fine, answered, false, random), "Questions are asked once");
        assertEquals(2, Talk.answerIndex("answer:sunrise_sunset:2", "sunrise_sunset"));
        assertEquals(-1, Talk.answerIndex("answer:cats_dogs:1", "sunrise_sunset"));
    }
}
