package dev.villagefriends;

import dev.villagefriends.outfit.*;
import java.util.*;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class ResidentNamesTest {
    private static final ResidentNames.Data DATA = ResidentNames.current();
    private static Set<String> all(String pool, java.util.function.Function<ResidentNames.Pool, List<String>> list) {
        var set = new HashSet<String>();
        for (var p : DATA.pools()) if (pool == null || p.id().equals(pool)) set.addAll(list.apply(p));
        return set;
    }
    private static final Set<String> MALE = all(null, ResidentNames.Pool::male), FEMALE = all(null, ResidentNames.Pool::female),
            UNISEX = all(null, ResidentNames.Pool::unisex);
    private static final Set<String> INDIAN = new HashSet<>();
    static {
        for (var p : DATA.pools()) if (p.id().equals("indian")) { INDIAN.addAll(p.male()); INDIAN.addAll(p.female()); INDIAN.addAll(p.unisex()); INDIAN.addAll(p.surnames()); }
    }
    private static String first(String name) { return name.substring(0, name.indexOf(' ')); }
    private static String last(String name) { return name.substring(name.indexOf(' ') + 1); }

    @Test void everyResidentsFirstNameMatchesTheirGender() {
        for (int i = 0; i < 6000; i++) {
            var id = new UUID(0x5eedL * i, i);
            for (var gender : Gender.values()) for (int skin = 0; skin < 6; skin++) {
                String recipe = new ResidentLook(skin, gender, PaletteID.values()[i % PaletteID.values().length], i).recipe();
                String first = first(ResidentNames.name(id, recipe));
                switch (gender) {
                    case MALE -> assertTrue(MALE.contains(first) || UNISEX.contains(first), "man named " + first);
                    case FEMALE -> assertTrue(FEMALE.contains(first) || UNISEX.contains(first), "woman named " + first);
                    case NON_BINARY -> assertTrue(UNISEX.contains(first), "non-binary resident named " + first);
                }
            }
        }
    }

    @Test void indianNamesOnlyGoToBrownOrDarkerSkin() {
        int indianOnDark = 0;
        for (int i = 0; i < 6000; i++) for (var gender : Gender.values()) for (int skin = 0; skin < 6; skin++) {
            String name = ResidentNames.name(new UUID(i, 0x1234L * i), new ResidentLook(skin, gender, PaletteID.DESERT_SUN, i).recipe());
            boolean indian = INDIAN.contains(first(name)) || INDIAN.contains(last(name));
            if (skin < 2) assertFalse(indian, "light-skinned resident given Indian name " + name);
            else if (indian) indianOnDark++;
        }
        assertTrue(indianOnDark > 1000, "Indian names still appear on brown and darker residents");
    }

    @Test void indianNamesComeWithIndianSurnames() {
        var surnames = new HashSet<>(DATA.pools().stream().filter(p -> p.id().equals("indian")).findFirst().orElseThrow().surnames());
        for (int i = 0; i < 3000; i++) {
            var recipe = new ResidentLook(3, Gender.FEMALE, PaletteID.DESERT_SUN, i).recipe();
            var id = new UUID(i, i * 31L);
            String name = ResidentNames.name(id, recipe);
            if (ResidentNames.legacyName(id, recipe).equals(name)) continue; // a fitting pre-2.18 name is kept as it was
            if (ResidentNames.pool(id, recipe).id().equals("indian")) assertTrue(surnames.contains(last(name)), name);
        }
    }

    @Test void poolsNeverListANameUnderTwoGenders() {
        for (var p : DATA.pools()) {
            var male = new HashSet<>(p.male());
            for (String n : p.female()) assertFalse(male.contains(n), n);
            for (String n : p.unisex()) { assertFalse(male.contains(n), n); assertFalse(p.female().contains(n), n); }
        }
        assertTrue(Collections.disjoint(MALE, FEMALE));
    }

    @Test void fittingOldNamesAreKeptAndMismatchedOnesAreCorrected() {
        int kept = 0, fixed = 0;
        for (int i = 0; i < 4000; i++) {
            var id = new UUID(0xabcL * i, ~i);
            var gender = Gender.values()[i % 3];
            String recipe = new ResidentLook(i % 6, gender, PaletteID.DESERT_SUN, i).recipe();
            String legacy = ResidentNames.legacyName(id, recipe), now = ResidentNames.name(id, recipe);
            if (legacy.equals(now)) { kept++; assertNull(ResidentNames.corrected(id, recipe, legacy)); continue; }
            fixed++;
            assertEquals(now, ResidentNames.corrected(id, recipe, legacy));
            // A surname taken from family survives; a player's own name is left alone.
            String adopted = first(legacy) + " Hollowbrook";
            if (!adopted.equals(legacy)) assertEquals(first(now) + " Hollowbrook", ResidentNames.corrected(id, recipe, adopted));
            assertNull(ResidentNames.corrected(id, recipe, "Captain Biscuit"));
            assertNull(ResidentNames.corrected(id, recipe, legacy + " of Oakridge"));
            assertNull(ResidentNames.corrected(id, recipe, now));
        }
        assertTrue(kept > 500 && fixed > 500, "kept " + kept + ", fixed " + fixed);
    }

    @Test void arrivalCardHasTenGreetingsAndNeverRepeatsBackToBack() {
        assertEquals(10, VillageArrival.VARIANTS);
        var sentences = new HashSet<String>();
        for (int v = 0; v < 10; v++) sentences.add(VillageArrival.line(v).sentence("Oakridge"));
        assertEquals(10, sentences.size());
        assertTrue(sentences.contains("Welcome to Oakridge"));
        assertTrue(sentences.contains("You are now entering Oakridge"));
        for (int prev = -1; prev < 10; prev++) for (int roll = 0; roll < 40; roll++) {
            int next = VillageArrival.next(prev, roll);
            assertTrue(next >= 0 && next < 10);
            if (prev >= 0) assertNotEquals(prev, next);
        }
    }
}
