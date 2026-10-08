package dev.villagefriends;

import static org.junit.jupiter.api.Assertions.*;
import com.mojang.serialization.JsonOps;
import dev.villagefriends.routine.Routine;
import dev.villagefriends.social.*;
import dev.villagefriends.social.Calendar;
import java.util.*;
import org.junit.jupiter.api.Test;

class BirthdayTest {
    private static Townsfolk person(int n, boolean adult, long day) {
        return Townsfolk.newcomer("resident-" + n, "Resident " + n, n % 2 == 0 ? "MALE" : "FEMALE", "farmer", "warmhearted", adult, day);
    }

    @Test void theCalendarHasFourSeasonsOfFourWeeks() {
        assertEquals("Spring 1", Calendar.date(0));
        assertEquals("Spring 28", Calendar.date(27));
        assertEquals("Summer 1", Calendar.date(28));
        assertEquals("Winter 28", Calendar.date(111));
        assertEquals("Spring 1", Calendar.date(112));
        assertEquals(2, Calendar.year(112));
        assertEquals("Moonday, Spring 1, Year 1", Calendar.longDate(0));
        // Every season starts on a Moonday, and Market Day falls on the 7th, 14th, 21st and 28th.
        for (long day = 0; day < Calendar.YEAR * 3; day++) {
            if (Calendar.dayOfSeason(day) == 1) assertEquals("Moonday", Routine.weekday(day));
            assertEquals(Calendar.dayOfSeason(day) % 7 == 0, Routine.marketDay(day), "day " + day);
        }
        assertEquals("today", Calendar.when(0)); assertEquals("tomorrow", Calendar.when(1)); assertEquals("in 3 days", Calendar.when(3));
    }

    @Test void birthdaysAreStableAndSpreadAcrossTheYear() {
        var days = new HashSet<Integer>();
        int[] seasons = new int[4];
        for (int n = 0; n < 2000; n++) {
            String id = UUID.nameUUIDFromBytes(("resident" + n).getBytes()).toString();
            int b = Calendar.birthday(id);
            assertEquals(b, Calendar.birthday(id));
            assertTrue(b >= 0 && b < Calendar.YEAR);
            days.add(b); seasons[b / Calendar.SEASON_DAYS]++;
        }
        assertEquals(Calendar.YEAR, days.size(), "every day of the year is someone's birthday");
        for (int s : seasons) assertTrue(s > 400 && s < 600, "seasons share birthdays evenly: " + Arrays.toString(seasons));
        assertEquals(0, Calendar.daysUntil(40, 40)); assertEquals(1, Calendar.daysUntil(40, 39)); assertEquals(111, Calendar.daysUntil(40, 41));
        assertTrue(Calendar.isBirthday(40, 40 + Calendar.YEAR));
    }

    @Test void babiesHaveTheirBirthdayOnTheDayTheyWereBorn() {
        var s = Society.create("v", 0).register(person(0, true, 0)).register(person(1, true, 0));
        s = s.register(person(2, false, 150)).born("resident-2", "resident-0", "resident-1", 150);
        assertEquals(Calendar.dayOfYear(150), s.get("resident-2").birthday());
        assertEquals(Calendar.birthday("resident-0"), s.get("resident-0").birthday(), "newcomers keep the birthday drawn from their ID");
        // Saved and loaded with the village.
        var json = Society.CODEC.encodeStart(JsonOps.INSTANCE, s).getOrThrow();
        var back = Society.CODEC.parse(JsonOps.INSTANCE, json).getOrThrow();
        assertEquals(s.get("resident-2").birthday(), back.get("resident-2").birthday());
        assertEquals(-1, back.get("resident-0").born());
    }

    @Test void theVillageCelebratesBirthdaysAndTalksAboutThem() {
        var s = Society.create("v", 0);
        for (int n = 0; n < 6; n++) s = s.register(person(n, true, 0));
        String id = "resident-3";
        int birthday = s.get(id).birthday();
        long day = birthday + Calendar.YEAR; // a year after they arrived
        s = s.advance(day - 1);
        assertTrue(s.celebrants(day - 1).stream().noneMatch(t -> t.id().equals(id)));
        s = s.advance(day);
        assertTrue(s.celebrants(day).stream().anyMatch(t -> t.id().equals(id)));
        var news = s.recent(day, 0).stream().filter(n -> n.kind().equals("birthday") && n.a().equals(id)).toList();
        assertEquals(1, news.size(), "the birthday is village news");
        assertEquals("It's Resident 3's birthday! Party by the bell this evening.", news.getFirst().headline(s));
        assertEquals(id, s.birthdays(day, 1).getFirst().id(), "today's birthday comes first");
        assertTrue(Gossip.about(s, id, day).contains("Birthday: " + Calendar.birthdayDate(birthday) + " (today!)"));
        assertTrue(Gossip.about(s, id, day - 3).contains("Birthday: " + Calendar.birthdayDate(birthday) + " (in 3 days)"));
        // Nobody celebrates while cursed.
        var cursed = s.cursed(id, day);
        assertTrue(cursed.celebrants(day).stream().noneMatch(t -> t.id().equals(id)));
    }

    @Test void partiesTakeTheEveningButNotBedsWatchesOrRain() {
        var day = Routine.day(7, "farmer", "warmhearted", false, 3);
        int party = Routine.at(17, 0);
        var clear = Routine.plan(day, party, Routine.Weather.CLEAR, 7, "farmer", "warmhearted", false, true);
        assertEquals(Routine.Block.PARTY, Routine.party(clear, party, false).block());
        assertEquals(clear, Routine.party(clear, Routine.at(15, 0), false), "only from 16:30 to 18:30");
        assertEquals(clear, Routine.party(clear, Routine.at(18, 45), false));
        var rain = Routine.plan(day, party, Routine.Weather.RAIN, 7, "farmer", "warmhearted", false, true);
        assertNotEquals(Routine.Block.PARTY, Routine.party(rain, party, false).block(), "rain keeps everyone in");
        // The tavern keeper works through a guest's party, but takes their own birthday off.
        var keeper = Routine.plan(Routine.day(7, "tavern_keeper", "warmhearted", false, 3), party, Routine.Weather.CLEAR, 7, "tavern_keeper", "warmhearted", false, true);
        assertEquals(Routine.Block.WORK, Routine.party(keeper, party, false).block());
        assertEquals(Routine.Block.PARTY, Routine.party(keeper, party, true).block());
        assertEquals("party", Routine.brief(Routine.Block.PARTY));
    }
}
