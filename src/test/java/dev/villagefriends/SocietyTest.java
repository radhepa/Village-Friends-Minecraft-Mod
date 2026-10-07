package dev.villagefriends;

import static org.junit.jupiter.api.Assertions.*;
import com.mojang.serialization.JsonOps;
import dev.villagefriends.social.*;
import java.util.*;
import org.junit.jupiter.api.Test;

class SocietyTest {
    private static final String[] GENDERS = {"MALE", "FEMALE", "NON_BINARY"};
    private static final String[] PERSONALITIES = {"warmhearted", "thoughtful", "playful", "adventurous", "meticulous", "steadfast",
            "reserved", "imaginative", "pragmatic", "curious", "protective", "gentle"};

    private static Townsfolk person(int n, boolean adult, long day) {
        return Townsfolk.newcomer("resident-" + n, "Resident " + n, GENDERS[n % 3], "farmer", PERSONALITIES[n % 12], adult, day);
    }
    private static Society village(int adults, int children) {
        var s = Society.create("natural:0:0", 0);
        for (int n = 0; n < adults + children; n++) s = s.register(person(n, n < adults, 0));
        return s;
    }

    @Test void traitsAreDeterministicAndLoveTakesFiftyToAThousandDays() {
        var days = new HashSet<Integer>();
        for (int n = 0; n < 2000; n++) {
            int love = Chemistry.loveDays("a" + n, "b" + n);
            assertTrue(love >= 50 && love <= 1000, "love days " + love);
            assertEquals(love, Chemistry.loveDays("b" + n, "a" + n));
            days.add(love / 100);
        }
        assertTrue(days.size() >= 10, "love timing should spread across the whole range");
        long romantic = java.util.stream.IntStream.range(0, 1000).filter(n -> Chemistry.romantic("r" + n)).count();
        assertTrue(romantic > 700 && romantic < 880, "most, but not all, residents are open to love: " + romantic);
        assertEquals("ANY", Chemistry.attraction("x", "NON_BINARY"));
    }

    @Test void everyoneKnowsEveryoneAndFriendshipsGrowWithTimeAndCompany() {
        var s = village(6, 0);
        for (var a : s.living()) for (var b : s.living()) if (a != b) {
            assertEquals(s.affinity(a.id(), b.id(), 0), s.affinity(b.id(), a.id(), 0));
            assertTrue(Math.abs(s.affinity(a.id(), b.id(), 0)) <= 5, "strangers start as polite neighbors");
        }
        String a = "resident-0", b = "resident-1";
        int later = s.affinity(a, b, 200), apart = later;
        var together = s;
        for (int day = 0; day < 30; day++) together = together.together(a, b, day).together(a, b, day);
        assertEquals(30, together.tie(a, b).together(), "one shared day counts once");
        assertEquals(apart + 15, together.affinity(a, b, 200));
        assertNotEquals(s.affinity(a, b, 0), later);
    }

    @Test void householdsFormCouplesSiblingsAndChildrenWithBloodAwareness() {
        var s = Society.create("v", 0);
        // Find two adults and a child who all bring family, and settle them together.
        var settlers = new ArrayList<Townsfolk>();
        for (int n = 0; settlers.size() < 3 && n < 500; n++) if (Chemistry.bringsFamily("resident-" + n)) settlers.add(person(n, settlers.size() < 2, 0));
        for (var t : settlers) s = s.register(t);
        s = s.household(settlers.get(1).id(), List.of(settlers.get(0).id()), 0);
        s = s.household(settlers.get(2).id(), List.of(settlers.get(0).id()), 0);
        var first = settlers.get(0).id(); var second = settlers.get(1).id(); var child = settlers.get(2).id();
        assertFalse(s.get(second).kin().isEmpty(), "family arrives together");
        assertEquals("parent", s.relation(child, first));
        assertTrue(s.blood(child, first));
        assertEquals(s.get(first).household(), s.get(child).household());
        if (s.get(first).married()) {
            assertEquals("parent", s.relation(child, second), "a married couple share their children");
            assertFalse(s.blood(first, second), "spouses are family but not blood");
        } else assertEquals("sibling", s.relation(first, second));
        assertTrue(s.affinity(child, first, 0) >= 60, "family starts close");
        assertFalse(Relations.label(s, child, first, 0).isEmpty());
        // Someone who does not bring family stays on their own.
        int loner = 0; while (Chemistry.bringsFamily("resident-" + (1000 + loner))) loner++;
        var single = person(1000 + loner, true, 0);
        s = s.register(single).household(single.id(), List.of(first), 0);
        assertTrue(s.get(single.id()).kin().isEmpty());
    }

    @Test void babiesJoinTheirParentsAndSiblings() {
        var s = village(2, 2);
        s = s.born("resident-2", "resident-0", "resident-1", 5).born("resident-3", "resident-0", "resident-1", 9);
        assertEquals("parent", s.relation("resident-2", "resident-0"));
        assertEquals("sibling", s.relation("resident-2", "resident-3"));
        assertEquals("child", s.relation("resident-1", "resident-3"));
        assertEquals("born", s.news().getLast().kind());
        assertTrue(s.news().getLast().headline(s).contains("Resident 3 was born to Resident 0 and Resident 1"));
        // Grandchildren and cousins are recognized.
        s = s.register(person(10, false, 20)).born("resident-10", "resident-2", "", 20);
        assertEquals("grandparent", s.relation("resident-10", "resident-0"));
        assertEquals("aunt_uncle", s.relation("resident-10", "resident-3"));
        assertEquals("Grandmother", Relations.kin("grandparent", "FEMALE"));
    }

    @Test void loveIsSlowNeverBetweenRelativesAndSomeNeverFallInLove() {
        var s = village(24, 0);
        // Make two residents siblings: they must never become a couple.
        s = s.born("resident-1", "resident-0", "", 0);
        long started = System.nanoTime();
        long firstLove = -1; int couples = 0, weddings = 0;
        for (long day = 1; day <= 1100; day++) {
            s = s.advance(day);
            if (day % 3 == 0) for (var t : s.living()) for (var u : s.living())
                if (t.id().compareTo(u.id()) < 0 && s.affinity(t.id(), u.id(), day) > 20) s = s.together(t.id(), u.id(), day);
            for (var n : s.news()) if (n.kind().equals("married") && n.day() == day) weddings++;
            for (var n : s.news()) if (n.kind().equals("sweethearts") && n.day() == day) {
                couples++; if (firstLove < 0) firstLove = day;
                assertTrue(s.known(n.a(), n.b(), day) >= Chemistry.loveDays(n.a(), n.b()), "nobody falls in love before their pair's time");
                assertFalse(s.blood(n.a(), n.b()));
            }
        }
        assertTrue(firstLove >= 50, "love never comes before fifty days: " + firstLove);
        assertTrue(couples >= 2, "a village sees some romances in three years: " + couples);
        long single = s.living().stream().filter(Townsfolk::single).count();
        assertTrue(single >= 4, "some residents never fall in love: " + single);
        assertNotEquals("resident-1", s.get("resident-0").partner());
        assertTrue(weddings >= 1, "sweethearts eventually marry: " + weddings + " of " + couples);
        for (var t : s.living()) if (!t.single()) assertEquals(t.id(), s.get(t.partner()).partner(), "partners are mutual");
        assertTrue((System.nanoTime() - started) / 1_000_000 < 20_000, "a long simulation stays cheap");
    }

    @Test void crushesComeBeforeLove() {
        var s = village(24, 0);
        boolean sawCrush = false;
        for (long day = 1; day <= 700 && !sawCrush; day++) {
            s = s.advance(day);
            for (var t : s.living()) if (!s.crush(t.id(), day).isEmpty()) {
                sawCrush = true;
                var other = s.crush(t.id(), day);
                assertEquals("smitten", s.romance(t.id(), other, day));
                assertTrue(s.known(t.id(), other, day) * 10 >= Chemistry.loveDays(t.id(), other) * 6L);
            }
        }
        assertTrue(sawCrush);
    }

    @Test void deathsCursesAndCuresAreRemembered() {
        var s = village(3, 0);
        var a = s.get("resident-0").partner("resident-1", 0, true); var b = s.get("resident-1").partner("resident-0", 0, true);
        s = new Society(s.village(), Map.of(a.id(), a, b.id(), b, "resident-2", s.get("resident-2")), s.ties(), s.news(), s.day());
        s = s.passed("resident-0", 10);
        assertFalse(s.get("resident-0").living());
        assertTrue(s.get("resident-1").single(), "a widowed partner is single again");
        assertEquals(2, s.living().size()); assertEquals(3, s.everyone().size());
        s = s.cursed("resident-2", 11);
        assertEquals(Townsfolk.CURSED, s.get("resident-2").status());
        s = s.cured("resident-2", 12);
        assertTrue(s.get("resident-2").home());
        assertEquals(List.of("cured", "cursed", "passed"), s.recent(12, 5).stream().map(News::kind).toList());
    }

    @Test void societiesRoundTripThroughCodecs() {
        var s = village(8, 2).born("resident-8", "resident-0", "resident-1", 3).together("resident-2", "resident-3", 4);
        for (long day = 1; day < 90; day++) s = s.advance(day);
        var book = SocietyBook.EMPTY.put(s);
        var json = SocietyBook.CODEC.encodeStart(JsonOps.INSTANCE, book).getOrThrow();
        assertEquals(book, SocietyBook.CODEC.parse(JsonOps.INSTANCE, json).getOrThrow());
        assertEquals(89, book.get("natural:0:0", 0).day());
        assertTrue(book.get("elsewhere", 7).folk().isEmpty());
    }

    @Test void newsIsBoundedAndCatchUpIsCapped() {
        var s = village(4, 0);
        for (int i = 0; i < 60; i++) s = s.cursed("resident-0", i).cured("resident-0", i);
        assertEquals(Society.MAX_NEWS, s.news().size());
        var jumped = village(4, 0).advance(100_000);
        assertEquals(100_000, jumped.day());
    }
}
