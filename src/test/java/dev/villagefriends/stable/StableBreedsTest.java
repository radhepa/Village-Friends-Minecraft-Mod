package dev.villagefriends.stable;

import static org.junit.jupiter.api.Assertions.*;

import dev.villagefriends.stable.breed.BreedPicker;
import dev.villagefriends.stable.breed.BreedRolls;
import dev.villagefriends.stable.breed.Inheritance;
import dev.villagefriends.stable.data.StableTable;
import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;
import javax.imageio.ImageIO;
import org.junit.jupiter.api.Test;

/** Breed rolls, the biome picker and foals, on the real breed table. */
class StableBreedsTest {
    private static StableTable.Breed breed(String id) { return StableTable.breed(id).orElseThrow(); }
    private static BreedRolls.Stats top(StableTable.Breed b) { return new BreedRolls.Stats(b.health().max(), b.speed().max(), b.jump().max()); }
    private static BreedRolls.Stats bottom(StableTable.Breed b) { return new BreedRolls.Stats(b.health().min(), b.speed().min(), b.jump().min()); }
    private static boolean inside(double v, StableTable.Range r) { return v >= r.min() - 1e-9 && v <= r.max() + 1e-9; }

    @Test void rollsStayInRangeAndCentreOnTheMiddle() {
        var random = new Random(7);
        for (var b : StableTable.breeds()) {
            double health = 0, speed = 0, jump = 0;
            int n = 10_000;
            for (int i = 0; i < n; i++) {
                var s = BreedRolls.roll(b, random);
                assertTrue(inside(s.health(), b.health()) && inside(s.speed(), b.speed()) && inside(s.jump(), b.jump()), b.id() + " rolled " + s);
                assertEquals(Math.rint(s.health()), s.health(), "health is whole hit points");
                health += s.health(); speed += s.speed(); jump += s.jump();
            }
            assertEquals((b.health().min() + b.health().max()) / 2, health / n, b.health().width() * .03, b.id() + " health centres");
            assertEquals((b.speed().min() + b.speed().max()) / 2, speed / n, b.speed().width() * .02, b.id() + " speed centres");
            assertEquals((b.jump().min() + b.jump().max()) / 2, jump / n, b.jump().width() * .02, b.id() + " jump centres");
        }
    }

    @Test void rollsAreSoftInTheMiddleAndRareAtTheEnds() {
        var random = new Random(7);
        var b = breed("courser");
        int middle = 0, ends = 0;
        for (int i = 0; i < 10_000; i++) {
            double f = (BreedRolls.roll(b, random).speed() - b.speed().min()) / b.speed().width();
            if (f > .4 && f < .6) middle++;
            if (f < .1 || f > .9) ends++;
        }
        assertTrue(middle > 3 * ends, "two averaged rolls bunch in the middle: " + middle + " vs " + ends);
    }

    @Test void thePickerOnlyReturnsBreedsWhoseSpawnsMatch() {
        var random = new Random(7);
        var breeds = StableTable.breeds();
        for (var keywords : List.of(Set.of("any", "taiga"), Set.of("any", "plains"), Set.of("any", "desert"), Set.of("any", "savanna", "windswept"),
                Set.of("any", "snowy", "taiga", "windswept"), Set.of("any"))) {
            var allowed = BreedPicker.weights(keywords, breeds).keySet();
            for (int i = 0; i < 2000; i++) {
                String id = BreedPicker.pick(keywords, breeds, random);
                assertTrue(allowed.contains(id), id + " can't be picked in " + keywords);
                var row = breed(id);
                assertTrue(row.spawns().stream().anyMatch(s -> s.biome().equals("any") || keywords.contains(s.biome())), id + " in " + keywords);
            }
        }
        assertEquals(Set.of("rouncey"), BreedPicker.weights(Set.of("any"), breeds).keySet(), "only the rouncey is found anywhere");
        assertTrue(BreedPicker.weights(Set.of("any", "desert"), breeds).containsKey("desert"));
        assertFalse(BreedPicker.weights(Set.of("any", "desert"), breeds).containsKey("fjord"), "no fjords in the desert");
    }

    @Test void thePickerFallsBackToTheRouncey() {
        var random = new Random(7);
        assertEquals("rouncey", BreedPicker.pick(Set.of("plains"), List.of(), random), "an empty table");
        var desertOnly = List.of(breed("desert"));
        assertEquals("rouncey", BreedPicker.pick(Set.of("any", "taiga"), desertOnly, random), "no row names this biome");
        assertEquals(BreedPicker.FALLBACK, "rouncey");
    }

    @Test void thePickerRespectsTheWeights() {
        var random = new Random(7);
        var keywords = Set.of("any", "plains");
        var weights = BreedPicker.weights(keywords, StableTable.breeds());
        // plains: destrier 1, palfrey 4, courser 2, rouncey 5 + any 3, draft 1.
        assertEquals(Map.of("destrier", 1, "palfrey", 4, "courser", 2, "rouncey", 8, "draft", 1), weights);
        int total = weights.values().stream().mapToInt(Integer::intValue).sum(), n = 32_000;
        var counts = new HashMap<String, Integer>();
        for (int i = 0; i < n; i++) counts.merge(BreedPicker.pick(keywords, StableTable.breeds(), random), 1, Integer::sum);
        for (var e : weights.entrySet()) {
            double expected = (double) n * e.getValue() / total;
            int seen = counts.getOrDefault(e.getKey(), 0);
            assertTrue(Math.abs(seen - expected) < 4 * Math.sqrt(expected), e.getKey() + ": " + seen + " picks, expected about " + expected);
        }
    }

    @Test void sameBreedFoalsKeepTheBreedAndAParentsCoat() {
        var random = new Random(7);
        var d = breed("destrier");
        assertTrue(d.coats() >= 2, "destriers come in more than one coat");
        int greys = 0;
        for (int i = 0; i < 1000; i++) {
            var foal = Inheritance.foal(d, BreedRolls.roll(d, random), 0, d, BreedRolls.roll(d, random), 1, random);
            assertEquals("destrier", foal.breed());
            assertTrue(foal.coat() == 0 || foal.coat() == 1, "a parent's coat: " + foal.coat());
            if (foal.coat() == 1) greys++;
            assertEquals(1, Inheritance.foal(d, BreedRolls.roll(d, random), 1, d, BreedRolls.roll(d, random), 1, random).coat(), "two greys have a grey");
        }
        assertTrue(greys > 400 && greys < 600, "either parent's coat, about evenly: " + greys);
    }

    @Test void mixedFoalsSplitAboutEvenly() {
        var random = new Random(7);
        var d = breed("destrier");
        var c = breed("courser");
        int destriers = 0, n = 10_000;
        for (int i = 0; i < n; i++) {
            var foal = Inheritance.foal(d, BreedRolls.roll(d, random), 0, c, BreedRolls.roll(c, random), 0, random);
            assertTrue(Set.of("destrier", "courser").contains(foal.breed()));
            assertTrue(foal.coat() >= 0 && foal.coat() < breed(foal.breed()).coats());
            if (foal.breed().equals("destrier")) destriers++;
        }
        assertTrue(Math.abs(destriers - n / 2) < 300, destriers + " destriers of " + n);
    }

    @Test void foalStatsAlwaysStayInsideTheWidenedRange() {
        var random = new Random(7);
        var breeds = StableTable.breeds();
        for (int i = 0; i < 20_000; i++) {
            var a = breeds.get(random.nextInt(breeds.size()));
            var b = breeds.get(random.nextInt(breeds.size()));
            // Parents anywhere in vanilla's wild ranges and beyond (a horse that never had a breed, or a bred champion).
            var sa = new BreedRolls.Stats(10 + random.nextDouble() * 30, .1 + random.nextDouble() * .26, .35 + random.nextDouble() * .7);
            var sb = i % 2 == 0 ? BreedRolls.roll(b, random) : new BreedRolls.Stats(40, .36, 1.05);
            var foal = Inheritance.foal(a, sa, 0, b, sb, 0, random);
            var row = breed(foal.breed());
            var s = foal.stats();
            assertTrue(inside(s.health(), Inheritance.widened(row.health())), foal + " health");
            assertTrue(inside(s.speed(), Inheritance.widened(row.speed())), foal + " speed");
            assertTrue(inside(s.jump(), Inheritance.widened(row.jump())), foal + " jump");
        }
        var w = Inheritance.widened(new StableTable.Range(20, 30));
        assertEquals(19, w.min(), 1e-9);
        assertEquals(31, w.max(), 1e-9);
    }

    @Test void foalsOfTopParentsAverageHigherThanFoalsOfBottomParents() {
        var random = new Random(7);
        for (var b : StableTable.breeds()) {
            double high = 0, low = 0;
            for (int i = 0; i < 2000; i++) {
                var up = Inheritance.foal(b, top(b), 0, b, top(b), 0, random).stats();
                var down = Inheritance.foal(b, bottom(b), 0, b, bottom(b), 0, random).stats();
                high += up.health() / b.health().width() + up.speed() / b.speed().width() + up.jump() / b.jump().width();
                low += down.health() / b.health().width() + down.speed() / b.speed().width() + down.jump() / b.jump().width();
            }
            assertTrue(high > low, b.id() + ": careful breeding pays");
        }
        // Two top destriers can edge past the wild top, never past the widened one.
        var d = breed("destrier");
        double best = 0;
        for (int i = 0; i < 5000; i++) best = Math.max(best, Inheritance.foal(d, top(d), 0, d, top(d), 0, random).stats().health());
        assertTrue(best > d.health().max(), "a little past the wild range");
        assertTrue(best <= Inheritance.widened(d.health()).max() + 1e-9);
    }

    @Test void everyBreedHasAPaintedAdultAndFoalCoat() throws IOException {
        for (var b : StableTable.breeds()) for (int coat = 0; coat < b.coats(); coat++) for (var baby : List.of("", "_baby")) {
            String path = "/assets/villagefriends/textures/entity/horse/" + b.id() + (coat > 0 ? "_" + coat : "") + baby + ".png";
            try (var in = StableBreedsTest.class.getResourceAsStream(path)) {
                assertNotNull(in, path + " is painted (run tools/stablehand/stablehand.py)");
                var image = ImageIO.read(in);
                assertEquals(64, image.getWidth(), path);
                assertEquals(64, image.getHeight(), path + " fits the vanilla horse's UV layout");
            }
        }
    }
}
