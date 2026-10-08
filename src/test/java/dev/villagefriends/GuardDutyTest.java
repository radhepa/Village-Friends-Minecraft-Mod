package dev.villagefriends;

import static org.junit.jupiter.api.Assertions.*;
import java.util.List;
import org.junit.jupiter.api.Test;

class GuardDutyTest {
    @Test void watchSplitsIntoSquadsOfTwoOrMore() {
        assertEquals(List.of(), GuardPatrols.squadSizes(0));
        assertEquals(List.of(), GuardPatrols.squadSizes(1), "Nobody patrols alone");
        assertEquals(List.of(2), GuardPatrols.squadSizes(2));
        assertEquals(List.of(3), GuardPatrols.squadSizes(3));
        assertEquals(List.of(2, 2), GuardPatrols.squadSizes(4));
        assertEquals(List.of(2, 3), GuardPatrols.squadSizes(5));
        for (int n = 2; n < 40; n++) {
            var sizes = GuardPatrols.squadSizes(n);
            assertEquals(n, sizes.stream().mapToInt(Integer::intValue).sum());
            assertTrue(sizes.stream().allMatch(s -> s == 2 || s == 3));
        }
    }
    @Test void shortHandedWatchCallsUpGuards() {
        assertEquals(0, GuardPatrols.draftsNeeded(1, 0), "A lone guard can't make a squad");
        assertEquals(2, GuardPatrols.draftsNeeded(2, 0));
        assertEquals(1, GuardPatrols.draftsNeeded(5, 1));
        assertEquals(0, GuardPatrols.draftsNeeded(5, 3));
    }
    @Test void knockoutClock() {
        long hour = 60L * 60 * 20;
        var s = KnockoutState.knockedOut(1000);
        assertEquals(24 * hour, s.left(1000), "A full day of play");
        assertEquals("24h 0m", KnockoutState.duration(s.left(1000)));
        assertEquals("under a minute", KnockoutState.duration(5));
        var bandaged = s.bandaged(1000, false);
        assertEquals(36 * hour, bandaged.left(1000));
        assertFalse(bandaged.tended());
        assertTrue(s.bandaged(1000, true).tended(), "The apothecary's visit is remembered");
        var most = bandaged.bandaged(1000, false).bandaged(1000, false);
        assertEquals(48 * hour, most.left(1000), "Bandages stop at two days left");
        assertFalse(most.canBandage(1000));
        assertEquals(0, s.left(s.until() + 50));
    }
}
