package dev.villagefriends.stable;

import static org.junit.jupiter.api.Assertions.*;

import dev.villagefriends.stable.bond.BondMath;
import dev.villagefriends.stable.data.StableTable;
import java.io.StringReader;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import org.junit.jupiter.api.Test;

/** The breed and gear tables as the game reads them (from the classpath), and the frozen bond numbers. */
class StableTableTest {
    private static final Set<String> KEYWORDS = Set.of("plains", "meadow", "forest", "savanna", "desert", "badlands", "taiga", "snowy", "windswept", "any");
    private static final Set<String> MARKINGS = Set.of("none", "white", "white_field", "white_dots", "black_dots");
    /** A sprinting player covers about 5.6 blocks a second; the lance must need more than that. */
    private static final double SPRINT = 5.6;

    @Test void bothTablesLoadFromTheClasspath() {
        var t = StableTable.load();
        assertFalse(t.breeds().isEmpty());
        assertFalse(t.gear().isEmpty());
        assertNotNull(t.lance());
        assertSame(t, StableTable.load(), "the tables are read once");
    }

    @Test void thereAreEightBreedsWithTheirOwnIds() {
        var ids = StableTable.breeds().stream().map(StableTable.Breed::id).toList();
        assertEquals(List.of("destrier", "palfrey", "courser", "rouncey", "draft", "desert", "steppe_pony", "fjord"), ids);
        assertEquals(ids.size(), new HashSet<>(ids).size(), "no breed twice");
        assertTrue(StableTable.breed("fjord").isPresent() && StableTable.breed("unicorn").isEmpty());
        assertEquals(ids.size(), StableTable.breedsById().size());
    }

    @Test void everyBreedHasSaneRangesSpawnsAndMarkings() {
        for (var b : StableTable.breeds()) {
            for (var r : List.of(b.health(), b.speed(), b.jump())) assertTrue(r.min() < r.max() && r.width() > 0, b.id() + " range " + r);
            assertTrue(b.health().min() >= 10 && b.health().max() <= 40, b.id() + " health " + b.health());
            assertTrue(b.speed().min() >= 0.1 && b.speed().max() <= 0.36, b.id() + " speed " + b.speed());
            assertTrue(b.jump().min() >= 0.35 && b.jump().max() <= 1.05, b.id() + " jump " + b.jump());
            assertFalse(b.spawns().isEmpty(), b.id() + " is picked somewhere");
            for (var s : b.spawns()) assertTrue(KEYWORDS.contains(s.biome()) && s.weight() > 0, b.id() + " spawn " + s);
            for (var s : b.extraSpawns()) assertTrue(KEYWORDS.contains(s.biome()) && s.weight() > 0 && 1 <= s.min() && s.min() <= s.max(), b.id() + " extra spawn " + s);
            assertFalse(b.markings().isEmpty());
            assertTrue(MARKINGS.containsAll(b.markings()), b.id() + " markings " + b.markings());
            assertTrue(b.coats() >= 1, b.id() + " has a coat");
            assertFalse(b.village().isEmpty(), b.id() + " lives in some village's stable");
            assertEquals(b.id(), b.raw().get("id").getAsString(), "rows keep their raw JSON");
        }
    }

    @Test void bardingGetsStrongerTierByTier() {
        int[] defense = List.of("caparison", "leather_barding", "mail_barding", "plate_barding").stream()
                .mapToInt(id -> StableTable.gear(id).orElseThrow().defense()).toArray();
        for (int i = 1; i < defense.length; i++) assertTrue(defense[i] > defense[i - 1], "defense rises: " + java.util.Arrays.toString(defense));
        for (var g : StableTable.gear()) {
            if (!g.barding()) continue;
            assertEquals("body", g.slot());
            assertTrue(g.repair().startsWith("minecraft:") && g.enchantability() > 0, g.id());
        }
        var caparison = StableTable.gear("caparison").orElseThrow();
        assertTrue(caparison.dyeable());
        assertEquals(-6537410, caparison.undyed(), "red cloth when undyed");
    }

    @Test void tackFitsTheMountScreenAndSuitsItsAnimals() {
        for (var g : StableTable.gear()) {
            assertTrue(g.barding() || g.tack(), g.id());
            assertTrue(g.columns() >= 0 && g.columns() <= 5, g.id() + " columns " + g.columns());
            assertTrue(Set.of("horse", "donkey", "mule").containsAll(g.animals()) && !g.animals().isEmpty(), g.id());
            assertTrue(g.bondRide() >= 1 && g.calm() >= 0, g.id());
            if (g.tack()) assertEquals("saddle", g.slot());
        }
        assertEquals(2, StableTable.gear("saddlebags").orElseThrow().columns());
        assertEquals(5, StableTable.gear("pack_saddle").orElseThrow().columns());
        var bridle = StableTable.gear("bridle").orElseThrow();
        assertEquals(1.5, bridle.bondRide());
        assertEquals(1, bridle.calm());
    }

    @Test void theLanceLandsOnlyAtAGallop() {
        var l = StableTable.lance();
        assertEquals("jousting_lance", l.id());
        assertTrue(l.damageThreshold() > SPRINT, "a sprinting player can't couch it: " + l.damageThreshold());
        assertEquals(6, l.reach().length);
        assertTrue(l.reach()[0] < l.reach()[1] && l.reach()[2] < l.reach()[3], "min reach below max reach");
        assertTrue(l.damageMultiplier() > 0 && l.attackDuration() > 0);
    }

    @Test void parseReadsAnyReaderAndKeepsExtraKeys() {
        var breeds = "{\"breeds\": [{\"id\": \"cob\", \"health\": [20, 24], \"speed\": [0.2, 0.25], \"jump\": [0.5, 0.6],"
                + " \"spawns\": [{\"biome\": \"any\", \"weight\": 1}], \"markings\": [\"none\"], \"village\": [\"plains\"], \"temper\": \"calm\"}]}";
        var gear = "{\"gear\": [{\"id\": \"halter\", \"kind\": \"tack\", \"slot\": \"saddle\", \"animals\": [\"horse\"]}],"
                + " \"lance\": {\"id\": \"l\", \"material\": \"wood\", \"attack_duration\": 1, \"damage_multiplier\": 1, \"delay\": 1,"
                + " \"dismount_time\": 1, \"dismount_threshold\": 1, \"knockback_time\": 1, \"knockback_threshold\": 1, \"damage_time\": 1,"
                + " \"damage_threshold\": 1, \"reach\": [1, 2, 1, 2, 0, 0]}}";
        var t = StableTable.parse(new StringReader(breeds), new StringReader(gear));
        var cob = t.breeds().getFirst();
        assertEquals(1, cob.coats(), "coats default to one");
        assertTrue(cob.extraSpawns().isEmpty());
        assertEquals("calm", cob.raw().get("temper").getAsString(), "an unknown key stays readable");
        var halter = t.gear().getFirst();
        assertEquals(0, halter.columns());
        assertEquals(1.0, halter.bondRide(), "bond_ride defaults to no change");
        assertFalse(halter.dyeable());
    }

    @Test void bondTiersAndCalmAreTheFrozenNumbers() {
        assertArrayEquals(new int[]{0, 100, 250, 500, 800}, BondMath.FLOORS);
        assertEquals(1000, BondMath.MAX);
        assertEquals(3, BondMath.WHISTLE_TIER);
        assertEquals(0, BondMath.tier(0)); assertEquals(0, BondMath.tier(99));
        assertEquals(1, BondMath.tier(100)); assertEquals(1, BondMath.tier(249));
        assertEquals(2, BondMath.tier(250)); assertEquals(3, BondMath.tier(500)); assertEquals(3, BondMath.tier(799));
        assertEquals(4, BondMath.tier(800)); assertEquals(4, BondMath.tier(BondMath.MAX));
        assertEquals(0, BondMath.tier(-5), "negative points are still Wary");
        assertEquals(0, BondMath.calm(0, 0));
        assertEquals(4, BondMath.calm(3, 1), "a bridle steadies a Loyal horse");
    }
}
