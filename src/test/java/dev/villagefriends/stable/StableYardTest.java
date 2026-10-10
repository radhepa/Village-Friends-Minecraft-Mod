package dev.villagefriends.stable;

import static org.junit.jupiter.api.Assertions.*;

import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import dev.villagefriends.stable.data.StableTable;
import dev.villagefriends.stable.yard.StallRules;
import dev.villagefriends.stable.yard.StallRules.Settle;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;
import org.junit.jupiter.api.Test;

class StableYardTest {
    static final List<String> VILLAGER_TYPES = List.of("plains", "desert", "savanna", "snow", "taiga", "jungle", "swamp");
    static final Set<String> OWN_ITEMS = Set.of("grooming_brush", "horse_whistle", "horse_papers", "jousting_lance", "horse_stall", "hay_trough", "saddle_rack");

    // -- stalls -------------------------------------------------------------------------------------

    @Test void playersStallOnlyTheirOwnHorses() {
        assertTrue(StallRules.canStall(true, false, false), "a horse you tamed");
        assertTrue(StallRules.canStall(false, true, false), "a horse already stabled in your name (bought with papers)");
        assertTrue(StallRules.canStall(true, true, false));
        assertFalse(StallRules.canStall(false, false, false), "somebody else's horse, or a wild one");
        assertFalse(StallRules.canStall(true, false, true), "a resident's horse is never yours to re-stall, even tamed");
        assertFalse(StallRules.canStall(false, false, true), "riding off on the village's horse doesn't make it yours");
    }

    @Test void theVillagesHorsesKeepTheirStalls() {
        assertTrue(StallRules.mayEvict(false), "a player's horse moves out for another");
        assertFalse(StallRules.mayEvict(true), "a village horse keeps its stall");
    }

    // -- troughs ------------------------------------------------------------------------------------

    @Test void troughsFillToFourAndNeverPastIt() {
        assertEquals(1, StallRules.fill(0, 1), "wheat is one serving");
        assertEquals(4, StallRules.fill(0, 4), "a hay bale fills it");
        assertEquals(4, StallRules.fill(3, 4), "never past full");
        assertEquals(4, StallRules.fill(4, 1));
        assertEquals(0, StallRules.fill(0, -3));
        for (int hay = 0; hay <= StallRules.MAX_HAY; hay++) for (int add = 0; add <= 4; add++) {
            int filled = StallRules.fill(hay, add);
            assertTrue(filled >= hay && filled <= StallRules.MAX_HAY, hay + " + " + add);
        }
    }

    @Test void onlyHurtHorsesAndFoalsEatAndOnlyWhenThereIsHay() {
        assertTrue(StallRules.eats(1, true, false));
        assertTrue(StallRules.eats(4, false, true));
        assertTrue(StallRules.eats(2, true, true));
        assertFalse(StallRules.eats(4, false, false), "a healthy grown horse leaves the hay alone");
        assertFalse(StallRules.eats(0, true, true), "an empty trough feeds nobody");
        var random = new Random(7);
        int used = 0, meals = 30_000;
        for (int i = 0; i < meals; i++) if (StallRules.usesHay(random.nextInt(3))) used++;
        assertEquals(meals / 3.0, used, meals * .02, "one meal in three takes a serving");
    }

    @Test void theStablehandTopsUpEachTroughOnceADayAndVisitsEachHorseEveryTwoMinutes() {
        assertTrue(StallRules.refill(0, -1, 5), "never topped up");
        assertTrue(StallRules.refill(3, 4, 5), "topped up yesterday");
        assertFalse(StallRules.refill(1, 5, 5), "already topped up today");
        assertFalse(StallRules.refill(4, -1, 5), "full");
        assertTrue(StallRules.visitDue(-1, 100), "never visited");
        assertFalse(StallRules.visitDue(1000, 1000 + StallRules.VISIT_TICKS - 1));
        assertTrue(StallRules.visitDue(1000, 1000 + StallRules.VISIT_TICKS));
    }

    // -- stable horses ------------------------------------------------------------------------------

    @Test void templateHorsesTakeAStallOrTryThreeTimes() {
        for (int tries = 0; tries < 5; tries++) assertEquals(Settle.STALL, StallRules.settle(true, tries), "a free stall is always taken");
        assertEquals(Settle.RETRY, StallRules.settle(false, 0), "the first try failed: look again");
        assertEquals(Settle.RETRY, StallRules.settle(false, 1));
        assertEquals(Settle.GIVE_UP, StallRules.settle(false, 2), "the third failure gives up");
        assertEquals(Settle.GIVE_UP, StallRules.settle(false, 7));
        // Walk the whole life of a horse that never finds a stall: exactly MAX_TRIES looks.
        int looks = 0; Settle s;
        do { s = StallRules.settle(false, looks); looks++; } while (s == Settle.RETRY);
        assertEquals(StallRules.MAX_TRIES, looks);
    }

    @Test void villagerTypesMapToVillageTypes() {
        assertEquals("plains", StallRules.villageType("plains"));
        assertEquals("desert", StallRules.villageType("desert"));
        assertEquals("savanna", StallRules.villageType("savanna"));
        assertEquals("taiga", StallRules.villageType("taiga"));
        assertEquals("snowy", StallRules.villageType("snow"), "vanilla's snow villagers live in snowy villages");
        assertEquals("plains", StallRules.villageType("jungle"));
        assertEquals("plains", StallRules.villageType("swamp"));
    }

    @Test void stableBreedsComeFromTheVillagesOwnBreedsByWeight() {
        var breeds = StableTable.breeds();
        var random = new Random(7);
        for (String type : List.of("plains", "desert", "savanna", "taiga", "snowy")) {
            var counts = new HashMap<String, Integer>();
            int rolls = 20_000, total = 0;
            for (int i = 0; i < rolls; i++) counts.merge(StallRules.stableBreed(breeds, type, random), 1, Integer::sum);
            for (var b : breeds) if (b.village().contains(type)) total += b.spawns().stream().mapToInt(StableTable.Spawn::weight).sum();
            for (var e : counts.entrySet()) {
                var breed = StableTable.breed(e.getKey()).orElseThrow();
                assertTrue(breed.village().contains(type), type + " villages don't keep " + e.getKey());
                double expected = rolls * breed.spawns().stream().mapToInt(StableTable.Spawn::weight).sum() / (double) total;
                assertEquals(expected, e.getValue(), rolls * .02 + 1, type + ": " + e.getKey());
            }
            for (var b : breeds) if (b.village().contains(type)) assertTrue(counts.containsKey(b.id()), type + " stables sometimes keep " + b.id());
        }
        assertEquals("rouncey", StallRules.stableBreed(breeds, "nether", random), "a village type with no breeds falls back to the common horse");
        assertEquals("rouncey", StallRules.stableBreed(List.of(), "plains", random));
    }

    // -- trades -------------------------------------------------------------------------------------

    private static JsonObject json(String path) {
        var in = StableYardTest.class.getResourceAsStream(path);
        assertNotNull(in, path + " is on the classpath (run tools/stablehand/stablehand.py)");
        return JsonParser.parseReader(new InputStreamReader(in, StandardCharsets.UTF_8)).getAsJsonObject();
    }
    private static JsonObject trade(String id) {
        assertTrue(id.startsWith("villagefriends:stablehand/"), id);
        return json("/data/villagefriends/villager_trade/" + id.substring("villagefriends:".length()) + ".json");
    }
    /** The villager types a trade is offered to (every type when it has no merchant predicate). */
    private static Set<String> offeredTo(JsonObject trade) {
        if (!trade.has("merchant_predicate")) return new HashSet<>(VILLAGER_TYPES);
        var variants = trade.getAsJsonObject("merchant_predicate").getAsJsonObject("predicate").getAsJsonObject("minecraft:predicates")
                .getAsJsonArray("minecraft:villager/variant");
        var out = new HashSet<String>();
        for (JsonElement v : variants) out.add(v.getAsString().substring("minecraft:".length()));
        return out;
    }

    @Test void everyTradeUsesRealStablehandItemsAndBreeds() {
        var known = new HashSet<>(OWN_ITEMS);
        for (var g : StableTable.gear()) known.add(g.id());
        known.add(StableTable.lance().id());
        var breeds = new HashSet<String>(List.of("donkey", "mule"));
        for (var b : StableTable.breeds()) breeds.add(b.id());
        var papersSold = new HashSet<String>();
        for (int level = 1; level <= 5; level++) {
            var set = json("/data/villagefriends/trade_set/stablehand/level_" + level + ".json");
            assertEquals("villagefriends:trade_set/stablehand/level_" + level, set.get("random_sequence").getAsString());
            for (JsonElement id : set.getAsJsonArray("trades")) {
                var t = trade(id.getAsString());
                for (String side : List.of("wants", "gives")) {
                    var item = t.getAsJsonObject(side);
                    String itemId = item.get("id").getAsString();
                    if (itemId.startsWith("villagefriends:")) assertTrue(known.contains(itemId.substring("villagefriends:".length())), id + ": " + itemId);
                    else assertTrue(itemId.startsWith("minecraft:"), id + ": " + itemId);
                    if (item.has("components")) {
                        assertEquals("villagefriends:horse_papers", itemId, id + ": only papers carry a component");
                        String breed = item.getAsJsonObject("components").getAsJsonObject("villagefriends:horse_papers").get("breed").getAsString();
                        assertTrue(breeds.contains(breed), id + ": papers for an unknown breed " + breed);
                        papersSold.add(breed);
                    }
                }
                assertTrue(t.get("max_uses").getAsInt() > 0 && t.get("xp").getAsInt() > 0, id.getAsString());
            }
        }
        assertTrue(papersSold.containsAll(List.of("rouncey", "palfrey", "destrier", "donkey", "mule")), "The stablehand sells the usual horses: " + papersSold);
    }

    @Test void everyStablehandHasEnoughOffersAtEveryLevelAndSellsTheirOwnVillagesHorse() {
        for (int level = 1; level <= 5; level++) {
            var set = json("/data/villagefriends/trade_set/stablehand/level_" + level + ".json");
            int amount = set.get("amount").getAsInt();
            Map<String, Integer> offers = new HashMap<>();
            Map<String, List<String>> localPapers = new HashMap<>();
            for (JsonElement id : set.getAsJsonArray("trades")) {
                var t = trade(id.getAsString());
                for (String type : offeredTo(t)) {
                    assertTrue(VILLAGER_TYPES.contains(type), id + " names an unknown villager type " + type);
                    offers.merge(type, 1, Integer::sum);
                    if (t.has("merchant_predicate")) localPapers.computeIfAbsent(type, k -> new ArrayList<>()).add(id.getAsString());
                }
            }
            for (String type : VILLAGER_TYPES) {
                assertTrue(offers.getOrDefault(type, 0) >= amount, "A " + type + " stablehand has " + amount + " offers to pick from at level " + level);
                if (level == 4) assertEquals(1, localPapers.getOrDefault(type, List.of()).size(), "A " + type + " stablehand sells one local horse: " + localPapers.get(type));
            }
            if (level != 4) assertTrue(localPapers.isEmpty(), "Only level 4 depends on where the stablehand lives");
        }
    }
}
