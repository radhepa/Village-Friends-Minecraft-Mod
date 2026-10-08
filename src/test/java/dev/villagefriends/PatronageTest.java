package dev.villagefriends;

import static org.junit.jupiter.api.Assertions.*;

import dev.villagefriends.routine.Routine.Block;
import dev.villagefriends.tavern.Patronage;
import dev.villagefriends.tavern.Patronage.Choice;
import dev.villagefriends.tavern.Patronage.Kind;
import dev.villagefriends.tavern.Patronage.Mood;
import dev.villagefriends.tavern.Patronage.Neighbor;
import dev.villagefriends.tavern.Patronage.Phase;
import java.util.List;
import org.junit.jupiter.api.Test;

class PatronageTest {
    private static final Mood LUNCH = new Mood("pragmatic", Block.LUNCH_TAVERN, false, false, false);
    private static final Mood EVENING = new Mood("pragmatic", Block.TAVERN, false, false, true);
    private static Neighbor friend(int affinity) { return new Neighbor(affinity, false, false, false, false, false); }
    private static Choice chair(List<Neighbor> table) { return new Choice(Kind.CHAIR, false, false, 3, table, 6); }

    @Test void friendsSitTogetherAndRivalsApart() {
        var partner = new Neighbor(40, false, true, false, false, false);
        var bestFriend = new Neighbor(70, false, false, true, false, false);
        var rival = new Neighbor(-40, false, false, false, true, false);
        double empty = Patronage.score(LUNCH, chair(List.of()), .5);
        assertTrue(Patronage.score(LUNCH, chair(List.of(partner)), .5) > empty + 4, "A partner's table beats an empty one");
        assertTrue(Patronage.score(LUNCH, chair(List.of(bestFriend)), .5) > empty + 3);
        assertTrue(Patronage.score(LUNCH, chair(List.of(rival)), .5) < empty - 5, "Nobody sits with their rival");
        assertTrue(Patronage.score(LUNCH, chair(List.of(friend(60), friend(50))), .5) > Patronage.score(LUNCH, chair(List.of(friend(60))), .5));
    }

    @Test void personalitiesLikeDifferentTables() {
        var strangers = List.of(friend(0), friend(0));
        var reserved = new Mood("reserved", Block.TAVERN, false, false, true);
        var playful = new Mood("playful", Block.TAVERN, false, false, true);
        assertTrue(Patronage.score(reserved, chair(List.of()), .5) > Patronage.score(reserved, chair(strangers), .5), "The reserved want a quiet table");
        assertTrue(Patronage.score(playful, chair(strangers), .5) > Patronage.score(playful, chair(List.of()), .5), "The playful want company");
    }

    @Test void theRoomItselfMatters() {
        var hearth = new Choice(Kind.ARMCHAIR, true, false, 1, List.of(), 6);
        var plain = new Choice(Kind.CHAIR, false, false, 1, List.of(), 6);
        var cold = new Mood("pragmatic", Block.TAVERN, false, true, true);
        assertTrue(Patronage.score(cold, hearth, .5) > Patronage.score(cold, plain, .5) + 1, "A cold night draws people to the fire");
        var terrace = new Choice(Kind.BENCH, false, true, 2, List.of(), 6);
        assertEquals(Patronage.CLOSED, Patronage.score(new Mood("pragmatic", Block.LUNCH_TAVERN, true, false, false), terrace, .5), "Nobody eats outside in the rain");
        assertTrue(Patronage.score(LUNCH, terrace, .5) > Patronage.score(LUNCH, plain, .5), "A fine lunch hour fills the terrace");
        var stool = new Choice(Kind.STOOL, false, false, 4, List.of(), 6);
        assertTrue(Patronage.score(LUNCH, stool, .5) < Patronage.score(LUNCH, plain, .5), "Diners would rather have a table");
        assertTrue(Patronage.score(new Mood("reserved", Block.TAVERN, false, false, true), stool, .5) > Patronage.score(LUNCH, stool, .5), "A quiet drink at the bar");
        assertTrue(Patronage.score(EVENING, plain, .5) > Patronage.score(EVENING, new Choice(Kind.CHAIR, false, false, 1, List.of(), 30), .5), "Closer seats win a tie");
    }

    @Test void theMenuGoesCourseByCourse() {
        long day = 3;
        String lunch = Patronage.order(Block.LUNCH_TAVERN, 0, day, 7, true, 10);
        assertEquals(Patronage.dishOfTheDay(day), lunch, "Lunch is the cook's dish of the day");
        assertEquals("villagefriends:ploughmans_lunch", Patronage.order(Block.LUNCH_TAVERN, 0, day, 7, false, 10), "A cold lunch when nobody is cooking");
        assertTrue(Patronage.drink(Patronage.order(Block.LUNCH_TAVERN, 1, day, 7, true, 10)), "then a drink");
        assertNull(Patronage.order(Block.LUNCH_TAVERN, 2, day, 7, true, 10), "and back to work");
        assertNotEquals(Patronage.dishOfTheDay(day), Patronage.order(Block.SUPPER_TAVERN, 0, day, 7, true, 10), "Supper is a different dish");
        for (int roll = 0; roll < 50; roll++) {
            String evening = Patronage.order(Block.TAVERN, 0, day, roll, true, roll);
            assertTrue(Patronage.drink(evening), "An evening starts with a drink: " + evening);
        }
        for (long d = 0; d < 8; d++) assertNotEquals(Patronage.dishOfTheDay(d), Patronage.supperDish(d));
    }

    @Test void dishesHaveKindsLeftoversAndTimes() {
        assertEquals("stew", Patronage.kind("villagefriends:hearty_stew"));
        assertEquals("pie", Patronage.kind("villagefriends:shepherds_pie"));
        assertEquals("cider", Patronage.kind(Patronage.CIDER));
        assertEquals("minecraft:bowl", Patronage.leftover("villagefriends:hearty_stew"));
        assertEquals("villagefriends:empty_coffee_mug", Patronage.leftover(Patronage.COFFEE));
        assertNull(Patronage.leftover("villagefriends:fresh_village_bread"));
        for (int roll = 0; roll < 400; roll += 37) {
            assertTrue(Patronage.duration("villagefriends:hearty_stew", roll) < 600, "A lunch fits in the lunch hour");
            assertTrue(Patronage.duration(Patronage.CIDER, roll) >= 500);
        }
    }

    @Test void statesRoundTrip() {
        String state = Patronage.state(Phase.EAT, "villagefriends:hearty_stew");
        assertEquals("eat:villagefriends:hearty_stew", state);
        assertEquals(Phase.EAT, Patronage.phase(state));
        assertEquals("villagefriends:hearty_stew", Patronage.item(state));
        assertEquals(Phase.WAIT, Patronage.phase(Patronage.state(Phase.WAIT, null)));
        assertNull(Patronage.item("wait"));
        assertNull(Patronage.phase(""));
    }
}
