package dev.villagefriends;

import static org.junit.jupiter.api.Assertions.*;
import dev.villagefriends.deed.*;
import dev.villagefriends.social.*;
import java.util.*;
import org.junit.jupiter.api.Test;

/** How word of a deed gets around a village: witnesses, neighbors standing together, daily gossip and news. */
class RumorTest {
    private static final String[] PERSONALITIES = {"warmhearted", "thoughtful", "playful", "adventurous", "meticulous", "steadfast",
            "reserved", "imaginative", "pragmatic", "curious", "protective", "gentle"};
    private static String id(int n) { return "resident-" + n; }

    /**
     * {@code size} neighbors. Each has spent days with the two next door and with {@link #FRIENDS} others
     * they meet at work, lunch or the tavern (a fixed draw), so about {@code 2 + 2·FRIENDS} close ties each.
     */
    private static Society village(int size) {
        var s = Society.create("natural:0:0", 0);
        for (int n = 0; n < size; n++)
            s = s.register(Townsfolk.newcomer(id(n), "Resident " + n, n % 2 == 0 ? "MALE" : "FEMALE", "farmer", PERSONALITIES[n % 12], true, 0));
        var random = new Random(size);
        for (int n = 0; n < size; n++) {
            var friends = new ArrayList<Integer>(List.of((n + 1) % size));
            for (int k = 0; k < FRIENDS; k++) friends.add(random.nextInt(size));
            for (int day = 1; day <= Rumors.CLOSE_TIE; day++) for (int f : friends) s = s.together(id(n), id(f), day);
        }
        return s;
    }
    private static final int FRIENDS = 3;
    /** A deed done on day {@code day}, seen by residents 0 to {@code witnesses - 1}. */
    private static Deed deed(DeedKind kind, int serial, long day, int witnesses) {
        var d = new Deed(serial, kind, "", "", day, day * 24000, List.of(), 1, kind.points10, false, day, Map.of());
        for (int n = 0; n < witnesses; n++) d = d.learn(id(n), Know.of(Know.SEEN, day, ""));
        return d;
    }
    private static double share(Deed d, Society s) { return d.knowers().size() / (double) s.living().size(); }

    @Test void witnessesKnowOnTheDayAndNobodyElseYet() {
        var s = village(30); var d = deed(DeedKind.HIT_RESIDENT, 1, 10, 3);
        assertEquals(3, d.knowers().size());
        assertTrue(d.knowers().values().stream().allMatch(k -> k.how() == Know.SEEN && k.day() == 10));
        assertSame(d, Rumors.daily(d, s, 10), "nothing spreads on the day itself");
    }

    @Test void theSameSeedSpreadsTheSameWay() {
        var s = village(30); var d = deed(DeedKind.HIT_RESIDENT, 7, 10, 2);
        assertEquals(Rumors.daily(d, s, 14), Rumors.daily(d, s, 14));
        // Living day by day or catching up four unloaded days at once comes out the same.
        var stepped = d;
        for (long day = 11; day <= 14; day++) stepped = Rumors.daily(stepped, s, day);
        assertEquals(Rumors.daily(d, s, 14).knowers(), stepped.knowers());
        assertSame(stepped, Rumors.daily(stepped, s, 14), "once a day");
    }

    @Test void aboutHalfTheVillageHearsANotableDeedInThreeDaysAndMostInSix() {
        var s = village(40); double three = 0, six = 0; int trials = 60;
        for (int serial = 1; serial <= trials; serial++) {
            var d = deed(DeedKind.HIT_RESIDENT, serial, 10, 3);
            three += share(Rumors.daily(d, s, 13), s); six += share(Rumors.daily(d, s, 16), s);
        }
        three /= trials; six /= trials;
        assertTrue(three > .35 && three < .75, "about half know within three days: " + three);
        assertTrue(six > .85, "most know within six days: " + six);
        // Hearsay names who told them.
        var d = Rumors.daily(deed(DeedKind.HIT_RESIDENT, 3, 10, 1), s, 13);
        for (var e : d.knowers().entrySet()) if (e.getValue().how() == Know.HEARD) {
            assertTrue(d.knows(e.getValue().from()), "the teller knew first");
            assertTrue(d.know(e.getValue().from()).day() < e.getValue().day());
        }
    }

    @Test void familyTellsFamilyMoreOften() {
        var s = village(20);
        s = s.register(Townsfolk.newcomer("kid", "Kid", "MALE", "none", "playful", false, 0)).born("kid", id(10), "", 0);
        int told = 0;
        for (int serial = 1; serial <= 400; serial++) {
            var d = new Deed(serial, DeedKind.HIT_GOLEM, "", "", 0, 0, List.of(), 1, -5, false, 0, Map.of()).learn(id(10), Know.of(Know.SEEN, 0, ""));
            if (Rumors.daily(d, s, 1).knows("kid")) told++;
        }
        assertTrue(Math.abs(told / 400.0 - Rumors.DAILY_FAMILY) < .08, "a parent tells their child half the time each day: " + told);
    }

    @Test void neighborsStandingTogetherPassItOnMoreOverLunchAndAtTheTavern() {
        assertEquals(Rumors.TOGETHER, Rumors.chance(false, false));
        assertEquals(3 * Rumors.TOGETHER, Rumors.chance(true, false), 1e-9);
        assertEquals(6 * Rumors.TOGETHER, Rumors.chance(true, true), 1e-9);
        var s = village(4); int plain = 0, tavern = 0, n = 4000;
        for (int check = 0; check < n; check++) {
            var d = deed(DeedKind.HIT_GOLEM, check % 97 + 1, 5, 1);
            if (Rumors.together(d, s, id(0), "work", id(2), "wander", 5, check).knows(id(2))) plain++;
            if (Rumors.together(d, s, id(0), "lunch_tavern", id(2), "tavern", 5, check).knows(id(2))) tavern++;
        }
        boolean close = Rumors.close(s, id(0), id(2), 5);
        double base = Rumors.chance(false, close), boosted = Rumors.chance(true, close);
        assertEquals(base, plain / (double) n, .03, "standing together at work");
        assertEquals(boosted, tavern / (double) n, .04, "three times as likely at the tavern");
        assertTrue(tavern > 2 * plain);
    }

    @Test void aPairPassesADeedOnOnceAndTheSameCheckRollsTheSame() {
        var s = village(4); var d = deed(DeedKind.HIT_GOLEM, 5, 5, 1);
        long check = 0; Deed heard = d;
        while (heard == d) heard = Rumors.together(d, s, id(0), "tavern", id(1), "tavern", 5, ++check);
        assertEquals(heard, Rumors.together(d, s, id(0), "tavern", id(1), "tavern", 5, check), "deterministic per check");
        var k = heard.know(id(1));
        assertEquals(Know.HEARD, k.how()); assertEquals(id(0), k.from()); assertEquals(5, k.day());
        for (long c = check + 1; c < check + 50; c++) assertSame(heard, Rumors.together(heard, s, id(1), "tavern", id(0), "tavern", 5, c), "both know: nothing to tell");
        assertSame(d, Rumors.together(d, s, id(2), "tavern", id(3), "tavern", 5, 1), "neither knows: nothing to tell");
        assertSame(d, Rumors.together(d, s, id(0), "tavern", id(1), "tavern", 5 + Deed.BAD_WINDOW + 1, 1), "stale deeds aren't gossiped");
    }

    @Test void aBigDeedIsVillageNewsAndEveryoneHasHeardTheNextDay() {
        var s = village(30); var d = deed(DeedKind.RAID_WON, 1, 10, 2);
        var next = Rumors.daily(d, s, 11);
        assertEquals(30, next.knowers().size());
        assertTrue(next.knowers().entrySet().stream().filter(e -> !e.getKey().equals(id(0)) && !e.getKey().equals(id(1)))
                .allMatch(e -> e.getValue().how() == Know.HEARD && e.getValue().from().isEmpty()), "heard as village news");
        assertEquals(Know.SEEN, next.know(id(0)).how(), "witnesses still saw it");
    }

    @Test void theDeadAndTheCursedTellNobodyAndHearNothing() {
        var s = village(12).passed(id(0), 9).cursed(id(5), 9);
        int heardFromDead = 0;
        for (int serial = 1; serial <= 50; serial++) {
            var d = Rumors.daily(deed(DeedKind.HIT_RESIDENT, serial, 10, 1), s, 20);
            if (d.knowers().size() > 1) heardFromDead++;
        }
        assertEquals(0, heardFromDead, "a dead witness tells no one");
        var alive = deed(DeedKind.HIT_RESIDENT, 1, 10, 0).learn(id(1), Know.of(Know.SEEN, 10, ""));
        assertFalse(Rumors.daily(alive, s, 20).knows(id(5)), "the cursed don't hear");
        assertFalse(Rumors.daily(deed(DeedKind.RAID_WON, 1, 10, 0).learn(id(1), Know.of(Know.SEEN, 10, "")), s, 11).knows(id(0)), "nor the dead");
        assertSame(alive, Rumors.together(alive, s, id(1), "tavern", id(5), "tavern", 10, 3), "nobody gossips with the cursed");
    }
}
