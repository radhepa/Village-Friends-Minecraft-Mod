package dev.villagefriends;

import static org.junit.jupiter.api.Assertions.*;

import dev.villagefriends.routine.Routine;
import dev.villagefriends.routine.Routine.Block;
import dev.villagefriends.routine.Routine.Chronotype;
import dev.villagefriends.routine.Routine.Weather;
import java.util.EnumSet;
import java.util.List;
import org.junit.jupiter.api.Test;

class RoutineTest {
    private static final List<String> JOBS = List.of("farmer", "librarian", "fisherman", "fletcher", "cleric", "cartographer", "armorer", "toolsmith",
            "weaponsmith", "leatherworker", "mason", "shepherd", "butcher", "knight", "archer", "cook", "tavern_keeper", "apothecary", "painter",
            "bard", "tailor", "carpenter", "scholar", "nitwit", "none");
    private static final List<String> PERSONALITIES = List.of("warmhearted", "thoughtful", "playful", "adventurous", "meticulous", "steadfast",
            "reserved", "imaginative", "pragmatic", "curious", "protective", "gentle");
    private static final int WORKDAY = 3, MARKET = 6;

    @Test void clockReadsLikeAVillageClock() {
        assertEquals(0, Routine.at(6, 0));
        assertEquals(6000, Routine.at(12, 0));
        assertEquals(18000, Routine.at(0, 0));
        assertEquals("8:30", Routine.clock(Routine.at(8, 30)));
        assertEquals("23:00", Routine.clock(Routine.at(23, 0)));
    }

    @Test void everyoneSleepsWorksAndEatsEveryDay() {
        for (String job : JOBS) for (String personality : PERSONALITIES) for (int seed = 0; seed < 40; seed++) {
            var day = Routine.day(seed * 7919, job, personality, false, WORKDAY);
            var seen = EnumSet.noneOf(Block.class);
            for (int t = 0; t < 24000; t += 50) seen.add(day.at(t));
            assertTrue(seen.contains(Block.SLEEP), job + " sleeps");
            assertTrue(seen.contains(Block.SUPPER) || seen.contains(Block.BREAKFAST), job + " eats");
            boolean guard = job.equals("knight") || job.equals("archer");
            if (!job.equals("none") && !job.equals("nitwit")) assertTrue(seen.contains(Block.WORK) || guard && seen.contains(Block.NIGHT_WATCH), job + " works on a workday");
            // At least six hours of sleep and no more than eleven and a half.
            int asleep = 0; for (int t = 0; t < 24000; t += 10) if (day.at(t) == Block.SLEEP) asleep += 10;
            assertTrue(asleep >= 6000 && asleep <= 11500, job + " sleeps a sensible amount: " + asleep);
        }
    }

    @Test void residentsKeepTheirOwnHours() {
        int early = 0, owls = 0, regular = 0;
        for (int seed = 0; seed < 600; seed++) {
            switch (Routine.chronotype(seed * 104729, PERSONALITIES.get(seed % PERSONALITIES.size()), "librarian", false)) {
                case EARLY_BIRD -> early++; case NIGHT_OWL -> owls++; case REGULAR -> regular++;
            }
        }
        assertTrue(early > 100 && owls > 80 && regular > 80, "A mix of early birds, night owls and regular hours: " + early + "/" + owls + "/" + regular);
        assertEquals(Chronotype.NIGHT_OWL, Routine.chronotype(1, "steadfast", "tavern_keeper", false));
        assertEquals(Chronotype.EARLY_BIRD, Routine.chronotype(1, "curious", "farmer", false));
        // Two residents with different seeds don't wake at exactly the same moment.
        var a = Routine.day(11, "mason", "pragmatic", false, WORKDAY).slots().stream().filter(s -> s.block() == Block.WAKE).findFirst().orElseThrow();
        var b = Routine.day(12, "mason", "pragmatic", false, WORKDAY).slots().stream().filter(s -> s.block() == Block.WAKE).findFirst().orElseThrow();
        assertNotEquals(a.start(), b.start());
    }

    @Test void jobsShapeTheDay() {
        var farmer = Routine.day(5, "farmer", "steadfast", false, WORKDAY);
        var painter = Routine.day(5, "painter", "imaginative", false, WORKDAY);
        assertEquals(Block.WORK, farmer.at(Routine.at(7, 0)), "Farmers are out early");
        assertNotEquals(Block.WORK, painter.at(Routine.at(7, 0)), "Painters wait for good light");
        var keeper = Routine.day(5, "tavern_keeper", "warmhearted", false, WORKDAY);
        assertEquals(Block.WORK, keeper.at(Routine.at(19, 0)), "The tavern keeper works the evening");
        var bard = Routine.day(5, "bard", "playful", false, WORKDAY);
        assertEquals(Block.PERFORM, bard.at(Routine.at(18, 30)), "The bard performs in the evening");
        var cleric = Routine.day(5, "cleric", "gentle", false, WORKDAY);
        assertTrue(cleric.slots().stream().anyMatch(s -> s.block() == Block.PRAYER), "Clerics begin with prayers");
        var nitwit = Routine.day(5, "nitwit", "playful", false, WORKDAY);
        assertEquals(Block.NAP, nitwit.at(Routine.at(13, 0)), "Free spirits nap after lunch");
        var child = Routine.day(5, "none", "playful", true, WORKDAY);
        assertEquals(Block.LESSONS, child.at(Routine.at(10, 30)));
        assertEquals(Block.PLAY, child.at(Routine.at(14, 0)));
        assertEquals(Block.SLEEP, child.at(Routine.at(22, 0)));
    }

    @Test void halfTheGuardsKeepTheNightWatch() {
        int night = 0;
        for (int seed = 0; seed < 200; seed++) {
            boolean watch = Routine.nightWatch(seed * 31337, "knight");
            var day = Routine.day(seed * 31337, "knight", "protective", false, WORKDAY);
            if (watch) {
                night++;
                assertEquals(Block.NIGHT_WATCH, day.at(Routine.at(1, 0)), "Night watch guards are up at 1:00");
                assertEquals(Block.SLEEP, day.at(Routine.at(11, 0)), "and asleep in the late morning");
            } else assertEquals(Block.SLEEP, day.at(Routine.at(1, 0)));
        }
        assertTrue(night > 70 && night < 130, "About half: " + night);
        assertFalse(Routine.nightWatch(4, "farmer"));
    }

    @Test void marketDayComesEveryWeek() {
        assertFalse(Routine.marketDay(WORKDAY)); assertTrue(Routine.marketDay(MARKET)); assertTrue(Routine.marketDay(MARKET + 7));
        var mason = Routine.day(9, "mason", "pragmatic", false, MARKET);
        assertEquals(Block.MARKET, mason.at(Routine.at(10, 0)), "Everyone goes to the market");
        assertTrue(mason.slots().stream().noneMatch(s -> s.block() == Block.WORK), "and nobody works");
        var cook = Routine.day(9, "cook", "warmhearted", false, MARKET);
        assertEquals(Block.WORK, cook.at(Routine.at(10, 0)), "except the cook");
        assertTrue(Routine.day(9, "mason", "pragmatic", false, MARKET).marketDay());
    }

    @Test void rainSendsMostPeopleIndoors() {
        int sheltered = 0, rainLovers = 0;
        for (int seed = 0; seed < 400; seed++) {
            String personality = PERSONALITIES.get(seed % PERSONALITIES.size());
            var day = Routine.day(seed, "librarian", personality, false, WORKDAY);
            var plan = Routine.plan(day, Routine.at(16, 45), Weather.RAIN, seed, "librarian", personality, false, true);
            assertEquals(Block.SOCIAL, plan.scheduled());
            if (plan.block() == Block.SHELTER) sheltered++;
            if (plan.block() == Block.RAIN_WALK) rainLovers++;
        }
        assertTrue(sheltered > 250, "Most head home: " + sheltered);
        assertTrue(rainLovers > 20, "A few love the rain: " + rainLovers);
        // Indoor work goes on; hardy trades keep working outdoors; others stop.
        var librarian = Routine.day(3, "librarian", "thoughtful", false, WORKDAY);
        assertEquals(Block.WORK, Routine.plan(librarian, Routine.at(10, 0), Weather.RAIN, 3, "librarian", "thoughtful", false, true).block());
        assertEquals(Block.SHELTER, Routine.plan(librarian, Routine.at(10, 0), Weather.RAIN, 3, "librarian", "thoughtful", false, false).block());
        var farmer = Routine.day(3, "farmer", "steadfast", false, WORKDAY);
        var wet = Routine.plan(farmer, Routine.at(10, 0), Weather.RAIN, 3, "farmer", "steadfast", false, false);
        assertEquals(Block.WORK, wet.block()); assertEquals("Working in the rain", wet.label());
        // Home stays home.
        assertEquals(Block.SUPPER, Routine.plan(librarian, Routine.at(17, 45), Weather.THUNDER, 3, "librarian", "thoughtful", false, true).block());
    }

    @Test void stormsSendEveryoneButTheGuardsInside() {
        for (int seed = 0; seed < 100; seed++) {
            var day = Routine.day(seed, "mason", "adventurous", false, WORKDAY);
            assertEquals(Block.STORM, Routine.plan(day, Routine.at(16, 45), Weather.THUNDER, seed, "mason", "adventurous", false, true).block());
        }
        for (int seed = 0; seed < 100; seed++) {
            if (!Routine.nightWatch(seed, "archer")) continue;
            var day = Routine.day(seed, "archer", "protective", false, WORKDAY);
            var plan = Routine.plan(day, Routine.at(23, 0), Weather.THUNDER, seed, "archer", "protective", false, false);
            assertEquals(Block.NIGHT_WATCH, plan.block()); assertEquals("Standing guard in the storm", plan.label());
        }
    }

    @Test void snowIsForPlaying() {
        int playing = 0;
        for (int seed = 0; seed < 100; seed++) {
            var day = Routine.day(seed, "none", "gentle", true, WORKDAY);
            var plan = Routine.plan(day, Routine.at(14, 0), Weather.SNOW, seed, "none", "gentle", true, true);
            if (plan.block() == Block.SNOW_PLAY) playing++;
        }
        assertTrue(playing > 70, "Most children play in the snow: " + playing);
        var reserved = Routine.day(8, "librarian", "reserved", false, WORKDAY);
        int indoors = 0;
        for (int seed = 0; seed < 100; seed++)
            if (Routine.plan(Routine.day(seed, "librarian", "reserved", false, WORKDAY), Routine.at(15, 30), Weather.SNOW, seed, "librarian", "reserved", false, true).block() == Block.SNOWED_IN) indoors++;
        assertTrue(indoors > 70, "Reserved residents stay in by the fire: " + indoors);
        assertEquals(Block.WORK, Routine.plan(reserved, Routine.at(10, 0), Weather.SNOW, 8, "librarian", "reserved", false, false).block(), "Work goes on in the snow");
    }

    @Test void residentsEatAndSpendEveningsAtTheTavern() {
        int lunches = 0, suppers = 0, evenings = 0, marketEvenings = 0, n = 0;
        for (int seed = 0; seed < 1200; seed++) {
            String personality = PERSONALITIES.get(seed % PERSONALITIES.size());
            var day = Routine.day(seed * 7919, "librarian", personality, false, WORKDAY);
            n++;
            if (day.at(Routine.at(11, 45)) == Block.LUNCH_TAVERN) lunches++;
            if (day.at(Routine.at(17, 45)) == Block.SUPPER_TAVERN) suppers++;
            if (day.at(Routine.at(19, 0)) == Block.TAVERN) evenings++;
            if (Routine.day(seed * 7919, "librarian", personality, false, MARKET).at(Routine.at(19, 0)) == Block.TAVERN) marketEvenings++;
        }
        assertTrue(lunches > n / 5 && lunches < n / 2, "A good lunch crowd, not the whole village: " + lunches + "/" + n);
        assertTrue(suppers > n / 10 && suppers < n * 35 / 100, "About one supper in five: " + suppers + "/" + n);
        assertTrue(evenings > n / 5 && evenings < n * 45 / 100, "About one evening in three: " + evenings + "/" + n);
        assertTrue(marketEvenings > n / 2 && marketEvenings < n * 85 / 100, "Most of the village on Market Day evening: " + marketEvenings + "/" + n);
        // Sociable residents go out more than reserved ones.
        int playful = 0, reserved = 0;
        for (int seed = 0; seed < 400; seed++) for (long d = 0; d < 6; d++) {
            if (Routine.tavernNight(seed, "playful", d)) playful++;
            if (Routine.tavernNight(seed, "reserved", d)) reserved++;
        }
        assertTrue(playful > reserved * 1.3, "Playful " + playful + " vs reserved " + reserved);
    }

    @Test void tavernMealsHaveTheirOwnHours() {
        for (int seed = 0; seed < 300; seed++) {
            var day = Routine.day(seed, "mason", "warmhearted", false, WORKDAY);
            if (!Routine.tavernSupper(seed, "warmhearted", WORKDAY)) continue;
            assertEquals(Block.SUPPER_TAVERN, day.at(Routine.at(17, 20)), "Tavern suppers start early to get a table");
            assertNotEquals(Block.SUPPER_TAVERN, day.at(Routine.at(18, 40)));
        }
        var keeper = Routine.day(5, "tavern_keeper", "warmhearted", false, WORKDAY);
        assertEquals(Block.WORK, keeper.at(Routine.at(20, 30)), "The keeper serves the evening crowd");
        assertEquals(Block.EVENING, keeper.at(Routine.at(21, 10)), "and closes up at nine");
        var cook = Routine.day(5, "cook", "warmhearted", false, WORKDAY);
        assertEquals(Block.WORK, cook.at(Routine.at(17, 0)), "The cook comes back for the supper service");
        assertEquals(Block.SUPPER, cook.at(Routine.at(19, 0)));
        var bard = Routine.day(5, "bard", "playful", false, WORKDAY);
        assertEquals(Block.TAVERN, bard.at(Routine.at(20, 30)), "The bard stays for a drink after the show");
        // Children don't go to the tavern.
        for (int seed = 0; seed < 100; seed++) for (int t = 0; t < 24000; t += 100)
            assertFalse(Routine.atTavern(Routine.day(seed, "none", "playful", true, MARKET).at(t)));
    }

    @Test void aWetLunchHourFillsTheTavern() {
        int moved = 0, checked = 0;
        for (int seed = 0; seed < 400 && checked < 40; seed++) {
            var day = Routine.day(seed, "mason", "pragmatic", false, WORKDAY);
            if (day.at(Routine.at(11, 45)) != Block.LUNCH) continue;
            checked++;
            var plan = Routine.plan(day, Routine.at(11, 45), Weather.RAIN, seed, "mason", "pragmatic", false, true);
            if (plan.block() == Block.LUNCH_TAVERN) moved++;
            assertEquals(Block.LUNCH, plan.scheduled());
        }
        assertTrue(checked > 10 && moved == checked, "Everyone lunching at the bell heads into the tavern: " + moved + "/" + checked);
    }

    @Test void summariesReadFromMorningToNight() {
        var summary = Routine.summary(Routine.day(3, "mason", "pragmatic", false, WORKDAY));
        assertTrue(summary.contains(" up") && summary.contains("work") && summary.endsWith("bed"), summary);
        assertTrue(summary.length() < 240, "Fits a ledger line: " + summary.length());
        for (var block : Block.values()) assertEquals(block, Block.byId(block.id()));
    }
}
