package dev.villagefriends;

import static org.junit.jupiter.api.Assertions.*;

import dev.villagefriends.homestead.Dwelling;
import dev.villagefriends.homestead.Dwelling.Role;
import dev.villagefriends.outfit.Gender;
import dev.villagefriends.routine.Routine;
import dev.villagefriends.routine.Routine.Block;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import org.junit.jupiter.api.Test;

class HomesteadTest {
    @Test void theTemplateTagsSayWhoLivesThere() {
        assertEquals(Role.PARIAH, Dwelling.role(Set.of("villagefriends.dweller.pariah")));
        assertEquals(Role.HOMESTEADER, Dwelling.role(List.of("something.else", "villagefriends.dweller.homesteader", "villagefriends.gender.female")));
        assertNull(Dwelling.role(Set.of("villagefriends.dweller.wizard")), "Unknown roles are ignored");
        assertNull(Dwelling.role(Set.of()));
        assertEquals(Gender.FEMALE, Dwelling.gender(Set.of("villagefriends.gender.female")));
        assertEquals(Gender.MALE, Dwelling.gender(Set.of("villagefriends.dweller.homesteader", "villagefriends.gender.male")));
        assertNull(Dwelling.gender(Set.of("villagefriends.dweller.pariah")), "No gender tag: they keep their own");
    }

    @Test void everyHomesteadHasANameThatFitsIt() {
        for (var role : Role.values()) {
            var names = new HashSet<String>();
            for (long seed = 0; seed < 200; seed++) names.add(Dwelling.placeName(role, seed * 7919));
            assertTrue(names.size() >= 10, role + " homesteads are named differently: " + names);
            assertEquals(Dwelling.placeName(role, 42), Dwelling.placeName(role, 42), "The same place keeps its name");
        }
        assertTrue(Dwelling.placeName(Role.PARIAH, 9).endsWith("House"));
        assertTrue(Dwelling.placeName(Role.VETERAN, 9).matches(".*(Tower|spire|watch)"));
        for (long seed = 0; seed < 100; seed++) assertTrue(Dwelling.complexion(seed) >= 0 && Dwelling.complexion(seed) <= 5);
    }

    @Test void nameplatesSayWhereTheyLiveExceptForThePariah() {
        assertEquals("Edwin Hale of Cloverbrook Farm", Dwelling.label(Role.HOMESTEADER, "Edwin Hale", "Cloverbrook Farm"));
        assertEquals("Corvin Vane, the Outcast", Dwelling.label(Role.PARIAH, "Corvin Vane", "Blackthorn House"));
    }

    @Test void personalitiesFitTheLife() {
        assertEquals("steadfast", Role.HOMESTEADER.personality(Gender.MALE));
        assertEquals("warmhearted", Role.HOMESTEADER.personality(Gender.FEMALE));
        assertEquals("reserved", Role.PARIAH.personality(Gender.FEMALE));
        assertEquals("protective", Role.VETERAN.personality(null));
    }

    @Test void outHereThereIsNoTavernBellOrMarket() {
        var village = Set.of(Block.TAVERN, Block.LUNCH_TAVERN, Block.SUPPER_TAVERN, Block.PERFORM, Block.MARKET, Block.SOCIAL, Block.LESSONS,
                Block.PARTY, Block.LUNCH);
        for (var role : Role.values()) for (var block : Block.values()) for (int hour = 0; hour < 24; hour++) {
            var out = Dwelling.adjust(role, block, Routine.at(hour, 0));
            assertFalse(village.contains(out), role + " at " + hour + ":00 doesn't go to " + out);
            if (role != Role.VETERAN) assertNotEquals(Block.NIGHT_WATCH, out, role + " keeps no watch");
        }
        assertEquals(Block.LUNCH_HOME, Dwelling.adjust(Role.PARIAH, Block.LUNCH_TAVERN, Routine.at(12, 0)));
        assertEquals(Block.EVENING, Dwelling.adjust(Role.SHEPHERD, Block.TAVERN, Routine.at(19, 0)));
        assertEquals(Block.WORK, Dwelling.adjust(Role.HOMESTEADER, Block.MARKET, Routine.at(10, 0)), "Market Day is a working day on the farm");
        assertEquals(Block.HOBBY, Dwelling.adjust(Role.HERBALIST, Block.SOCIAL, Routine.at(16, 0)));
        assertEquals(Block.WORK, Dwelling.adjust(Role.PARIAH, Block.WORK, Routine.at(9, 0)), "Everything else is left alone");
    }

    @Test void theVeteranKeepsTheWatchUntilMidnightWhateverTheWeather() {
        for (var block : List.of(Block.EVENING, Block.SLEEP, Block.STORM, Block.SHELTER))
            assertEquals(Block.NIGHT_WATCH, Dwelling.adjust(Role.VETERAN, block, Routine.at(21, 30)), block + " at 21:30");
        assertEquals(Block.SLEEP, Dwelling.adjust(Role.VETERAN, Block.SLEEP, Routine.at(2, 0)), "After midnight they sleep");
        assertEquals(Block.EVENING, Dwelling.adjust(Role.VETERAN, Block.EVENING, Routine.at(19, 0)), "Not before half past eight");
        assertEquals(Block.NIGHT_WATCH, Dwelling.adjust(Role.VETERAN, Block.NIGHT_WATCH, Routine.at(3, 0)), "A scheduled watch stands");
    }

    @Test void theirWindowSaysWhatTheyAreDoing() {
        assertEquals("Mending the old house", Dwelling.doing(Role.PARIAH, "none", Block.WORK, false));
        assertEquals("Keeping house", Dwelling.doing(Role.HOMESTEADER, "cook", Block.WORK, false));
        assertEquals("Working the fields", Dwelling.doing(Role.HOMESTEADER, "farmer", Block.WORK, false));
        assertEquals("Tending the flock", Dwelling.doing(Role.SHEPHERD, "shepherd", Block.WORK, false));
        assertEquals("Keeping the watch in the storm", Dwelling.doing(Role.VETERAN, "archer", Block.NIGHT_WATCH, true));
        assertNull(Dwelling.doing(Role.HERBALIST, "apothecary", Block.SLEEP, false), "The usual words otherwise");
        for (var role : Role.values()) assertNotNull(Dwelling.doing(role, "farmer", Block.WORK, false), role + " at work");
    }

    @Test void greetingsFollowTheTimeOfDay() {
        assertEquals("morning", Dwelling.greetingTime("dawn"));
        assertEquals("night", Dwelling.greetingTime("late"));
        assertNull(Dwelling.greetingTime("noon"));
    }
}
