package dev.villagefriends;

import static org.junit.jupiter.api.Assertions.*;

import com.mojang.serialization.JsonOps;
import dev.villagefriends.fishing.Catches;
import dev.villagefriends.fishing.Contest;
import dev.villagefriends.fishing.Fish;
import dev.villagefriends.fishing.FishTable;
import dev.villagefriends.fishing.Gear;
import dev.villagefriends.fishing.Journal;
import dev.villagefriends.fishing.Minigame;
import dev.villagefriends.fishing.Spot;
import dev.villagefriends.fishing.Tales;
import java.util.HashMap;
import java.util.List;
import java.util.Random;
import java.util.Set;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

class FishingTest {
    @BeforeAll static void load() { if (FishTable.all().isEmpty()) FishTable.load(); }

    private static Spot spot(Set<String> waters, String region, int time, boolean rain, String season) {
        return new Spot(waters, region, Spot.times(time), rain, false, season, true);
    }
    private static final Spot PLAINS_RIVER_DAY = spot(Set.of("river"), "plains", 3000, false, null);

    @Test void theTableHasAboutEightyFishAndALegendForEveryVillageType() {
        var all = FishTable.all();
        assertTrue(all.size() >= 80, "about 80 fish: " + all.size());
        assertEquals(4, all.stream().filter(Fish::existing).count(), "vanilla's four are in the table");
        var legends = all.stream().filter(Fish::legendary).toList();
        assertTrue(legends.size() >= 8, "a legend per village type and a few more");
        for (var type : List.of("plains", "desert", "savanna", "snowy", "taiga"))
            assertTrue(legends.stream().anyMatch(f -> f.region().contains(type)), "a legend for " + type + " villages");
        for (var f : all) {
            assertTrue(f.minSize() > 0 && f.minSize() < f.maxSize(), f.id());
            assertTrue(f.legendary() || f.edible() || f.flags().contains("inedible"), f.id() + " is food unless it's a legend or inedible");
            assertFalse(f.legendary() && f.edible(), "legends aren't food");
            assertNotNull(FishTable.byItem(f.item()));
        }
        assertEquals("taiga", FishTable.region("minecraft:old_growth_spruce_taiga"));
        assertNull(FishTable.region("minecraft:river"), "rivers belong to the land around them");
    }

    @Test void fishTellTheTimeLikeAnglers() {
        assertEquals(Set.of("dawn"), Spot.times(23500));
        assertEquals(Set.of("day"), Spot.times(2000));
        assertEquals(Set.of("day", "noon"), Spot.times(6000));
        assertEquals(Set.of("dusk"), Spot.times(12500));
        assertEquals(Set.of("night"), Spot.times(18000));
        assertEquals(Set.of("cave", "deepcave"), Spot.waters(true, -20, "lake", false, false, false));
        assertEquals(Set.of("ocean", "warm", "deep"), Spot.waters(false, 60, "ocean", true, false, true));
        assertEquals(Set.of("lake"), Spot.waters(false, 62, "plains", false, false, false));
    }

    @Test void legendsBiteOnlyWhereAndWhenTheTalesSay() {
        var whiskers = FishTable.get("old_whiskers");
        assertTrue(whiskers.bites(spot(Set.of("river"), "plains", 18000, true, null)), "plains river, a rainy night");
        assertFalse(whiskers.bites(spot(Set.of("river"), "plains", 18000, false, null)), "not on a dry night");
        assertFalse(whiskers.bites(spot(Set.of("river"), "desert", 18000, true, null)), "not in the desert");
        assertFalse(whiskers.bites(spot(Set.of("river"), "plains", 3000, true, null)), "not by day");
        var rimefin = FishTable.get("rimefin");
        assertTrue(rimefin.bites(spot(Set.of("lake"), "snowy", 18000, false, null)), "seasons don't matter without Turning Seasons");
        assertTrue(rimefin.bites(spot(Set.of("lake"), "snowy", 18000, false, "winter")));
        assertFalse(rimefin.bites(spot(Set.of("lake"), "snowy", 18000, false, "summer")), "only in winter with seasons on");
        var cave = spot(Set.of("cave"), "plains", 3000, false, null);
        for (var f : FishTable.biting(cave)) assertTrue(f.water().contains("cave") || f.water().contains("deepcave"), "only cave fish underground: " + f.id());
        assertFalse(FishTable.biting(cave).isEmpty());
        assertFalse(FishTable.biting(PLAINS_RIVER_DAY).stream().anyMatch(f -> f.water().contains("cave")), "no cave fish in the open");
    }

    @Test void commonFishDominateAndLuckBaitAndTheRodTipTheOdds() {
        var random = new Random(1);
        var counts = new HashMap<Fish.Rarity, Integer>();
        for (int i = 0; i < 20000; i++) counts.merge(Catches.pick(FishTable.all(), PLAINS_RIVER_DAY, Catches.Odds.PLAIN, random).rarity(), 1, Integer::sum);
        assertTrue(counts.getOrDefault(Fish.Rarity.COMMON, 0) > counts.getOrDefault(Fish.Rarity.UNCOMMON, 0));
        assertTrue(counts.getOrDefault(Fish.Rarity.UNCOMMON, 0) > counts.getOrDefault(Fish.Rarity.RARE, 0));
        var night = spot(Set.of("river", "lake"), "plains", 18000, true, null);
        int plain = legends(night, Catches.Odds.PLAIN), lured = legends(night, new Catches.Odds(0, Gear.Bait.LEGEND_LURE, null, Gear.Rod.ANGLERS)),
                lucky = legends(night, new Catches.Odds(3, null, null, Gear.Rod.PLAIN));
        assertTrue(plain > 0, "Old Whiskers does bite on a rainy plains night");
        assertTrue(lured > plain * 3, "a Legend Lure on an Angler's Rod: " + lured + " vs " + plain);
        assertTrue(lucky > plain, "luck helps: " + lucky + " vs " + plain);
        assertTrue(Catches.weight(FishTable.get("perch"), new Catches.Odds(0, Gear.Bait.BAIT_WORMS, null, Gear.Rod.PLAIN))
                > Catches.weight(FishTable.get("perch"), Catches.Odds.PLAIN), "freshwater fish like worms");
        assertEquals(Catches.weight(FishTable.get("herring"), new Catches.Odds(0, Gear.Bait.BAIT_WORMS, null, Gear.Rod.PLAIN)),
                Catches.weight(FishTable.get("herring"), Catches.Odds.PLAIN), "sea fish don't care for worms");
    }
    private static int legends(Spot spot, Catches.Odds odds) {
        var random = new Random(7); int n = 0;
        for (int i = 0; i < 20000; i++) if (Catches.pick(FishTable.all(), spot, odds, random).legendary()) n++;
        return n;
    }

    @Test void junkAndTreasureFollowVanillasWeights() {
        var random = new Random(3); int junk = 0, treasure = 0;
        for (int i = 0; i < 20000; i++) {
            var k = Catches.kind(random, 0, true);
            if (k == Catches.Kind.JUNK) junk++; else if (k == Catches.Kind.TREASURE) treasure++;
        }
        assertEquals(.10, junk / 20000.0, .015);
        assertEquals(.05, treasure / 20000.0, .01);
        for (int i = 0; i < 2000; i++) assertNotEquals(Catches.Kind.TREASURE, Catches.kind(random, 3, false), "treasure needs open water");
    }

    @Test void sizesStayInRangeAndPerfectCatchesRunBigger() {
        var pike = FishTable.get("pike"); var random = new Random(5);
        double plain = 0, perfect = 0;
        for (int i = 0; i < 4000; i++) {
            int a = Catches.size(pike, random, 0, false), b = Catches.size(pike, random, 0, true);
            assertTrue(a >= pike.minSize() * 10 && a <= pike.maxSize() * 10 && b <= pike.maxSize() * 10);
            plain += a; perfect += b;
        }
        assertTrue(perfect > plain);
        assertEquals("54.3 cm", Catches.cm(543));
    }

    /** Holds the button when the zone is about to drift below the fish: a decent player, who allows for its momentum. */
    private static boolean hold(Minigame game, float target) { return game.barPos() + game.zone() / 2 + game.barSpeed() * 6 > target; }
    private static boolean play(Fish f, Minigame.Tuning tuning, long seed, boolean bot) {
        var game = new Minigame(seed, f.behavior(), f.difficulty(), tuning);
        while (!game.done()) game.tick(bot && hold(game, game.fishPos() + Minigame.FISH / 2));
        if (game.won()) assertTrue(game.ticks() >= Minigame.quickest(tuning), "no catch is quicker than the meter can fill");
        return game.won();
    }
    private static double winRate(String fish, Minigame.Tuning tuning) {
        int wins = 0;
        for (long s = 0; s < 200; s++) if (play(FishTable.get(fish), tuning, s, true)) wins++;
        return wins / 200.0;
    }

    @Test void theMinigameIsFairToADecentPlayerAndBetterGearHelps() {
        var plain = Minigame.Tuning.of(Gear.Rod.PLAIN, null, false);
        assertTrue(winRate("minnow", plain) > .95, "a minnow is easy");
        assertTrue(winRate("perch", plain) > .85, "so is a perch");
        double pike = winRate("pike", plain), pikeAngler = winRate("pike", Minigame.Tuning.of(Gear.Rod.ANGLERS, Gear.Tackle.CORK_BOBBER, false));
        assertTrue(pikeAngler >= pike, "an Angler's Rod and a cork bobber help: " + pikeAngler + " vs " + pike);
        double legend = winRate("stormjaw", plain);
        assertTrue(legend < winRate("perch", plain), "a legend is much harder: " + legend);
        assertTrue(winRate("stormjaw", Minigame.Tuning.of(Gear.Rod.ANGLERS, Gear.Tackle.CORK_BOBBER, false).widen(60)) > legend, "and gear and skill make it fair");
        for (long s = 0; s < 20; s++) assertFalse(play(FishTable.get("perch"), plain, s, false), "doing nothing loses the fish");
        // The same seed plays out the same way.
        var a = new Minigame(42, Fish.Behavior.DART, 60, plain); var b = new Minigame(42, Fish.Behavior.DART, 60, plain);
        for (int i = 0; i < 300; i++) { boolean hold = i % 7 < 3; a.tick(hold); b.tick(hold); }
        assertEquals(a.fishPos(), b.fishPos()); assertEquals(a.progress(), b.progress());
    }

    @Test void treasureCanBeCollectedAlongTheWay() {
        var tuning = Minigame.Tuning.of(Gear.Rod.ANGLERS, Gear.Tackle.CORK_BOBBER, true);
        int collected = 0;
        for (long s = 0; s < 100; s++) {
            var game = new Minigame(s, Fish.Behavior.SMOOTH, 10, tuning);
            while (!game.done()) {
                // Go for the chest while it's showing, then back to the fish.
                float target = game.treasureShown() ? game.treasurePos() : game.fishPos() + Minigame.FISH / 2;
                game.tick(hold(game, target));
            }
            if (game.treasureCaught()) collected++;
        }
        assertTrue(collected > 50, "treasure is reachable: " + collected);
    }

    @Test void theJournalRemembersFirstsRecordsAndTales() {
        var j = Journal.EMPTY.record("pike", 543, 10);
        assertTrue(j.first() && j.record());
        var again = j.journal().record("pike", 400, 12);
        assertFalse(again.first()); assertFalse(again.record());
        var better = again.journal().record("pike", 801, 15);
        assertTrue(better.record()); assertEquals(543, better.previousBest());
        var journal = better.journal().hear("old_whiskers");
        assertEquals(3, journal.entry("pike").count()); assertEquals(801, journal.entry("pike").best()); assertEquals(10, journal.entry("pike").first());
        assertTrue(journal.heard("old_whiskers")); assertSame(journal, journal.hear("old_whiskers"));
        var json = Journal.CODEC.encodeStart(JsonOps.INSTANCE, journal).getOrThrow();
        assertEquals(journal, Journal.CODEC.parse(JsonOps.INSTANCE, json).getOrThrow());
    }

    @Test void tallTalesSayWhereAndWhenInPlainWords() {
        assertEquals("the rivers and lakes of the plains", Tales.where(FishTable.get("old_whiskers")));
        assertEquals("on rainy nights", Tales.when(FishTable.get("old_whiskers")));
        assertEquals("the pools and rivers of the desert", Tales.where(FishTable.get("sunscale")));
        assertEquals("at noon under a clear sky in summer", Tales.when(FishTable.get("sunscale")));
        assertEquals("at dawn in the autumn rains", Tales.when(FishTable.get("old_mossback")));
        assertEquals("on clear, starry nights in winter", Tales.when(FishTable.get("rimefin")));
        assertEquals("whenever thunder rolls", Tales.when(FishTable.get("stormjaw")));
        assertEquals("the deep sea", Tales.where(FishTable.get("stormjaw")));
        assertEquals("the black water of the swamps", Tales.where(FishTable.get("bog_lantern")));
        assertEquals("the black water below the world", Tales.where(FishTable.get("deepglow")));
        for (var f : FishTable.all()) { assertFalse(Tales.where(f).isBlank(), f.id()); assertFalse(Tales.when(f).contains("  "), f.id()); }
        // Residents mostly tell of their own region's legend.
        var random = new Random(9); int local = 0;
        for (int i = 0; i < 300; i++) if (Tales.legend(FishTable.all(), "desert", Set.of(), random).id().equals("sunscale")) local++;
        assertTrue(local > 150, "desert folk talk of Sunscale: " + local);
    }

    @Test void theContestIsOnTheTwelfthAndTheBiggestFishWins() {
        assertTrue(Contest.contestDay(11)); assertFalse(Contest.contestDay(12));
        assertTrue(Contest.contestDay(11 + 28)); assertEquals(1, Contest.daysUntil(10)); assertEquals(0, Contest.daysUntil(11));
        assertEquals(Contest.Phase.OPEN, Contest.phase(11, 3000)); assertEquals(Contest.Phase.WEIGH_IN, Contest.phase(11, 10700));
        assertEquals(Contest.Phase.OVER, Contest.phase(11, 12000)); assertEquals(Contest.Phase.NONE, Contest.phase(12, 3000));
        assertEquals("Spring 12", Contest.nextDate(3));
        List<Contest.Entry> s = List.of();
        s = Contest.add(s, new Contest.Entry("a", "Ada", true, "perch", 300));
        s = Contest.add(s, new Contest.Entry("b", "Bram", false, "pike", 700));
        s = Contest.add(s, new Contest.Entry("a", "Ada", true, "roach", 200));
        assertEquals(2, s.size(), "one entry each: their best");
        assertEquals("b", s.getFirst().key()); assertEquals(300, s.get(1).size());
        s = Contest.add(s, new Contest.Entry("a", "Ada", true, "carp", 750));
        assertEquals(1, Contest.place(s, "a")); assertEquals(0, Contest.place(s, "c"));
        assertFalse(Contest.prizes(1).isEmpty()); assertTrue(Contest.prizes(4).isEmpty());
        var e = Contest.residentCatch("r1", "Wren", FishTable.all(), PLAINS_RIVER_DAY, 2, new Random(2));
        assertNotNull(e); assertFalse(FishTable.get(e.fish()).legendary());
    }

    @Test void gearIsModest() {
        assertTrue(Gear.quicker(Gear.Bait.BAIT_WORMS, Gear.Tackle.SPINNER, 400) <= 240, "bait never cuts the wait by more than 60%");
        assertEquals(0, Gear.quicker(null, null, 400));
        assertTrue(Gear.Rod.ANGLERS.rareOdds() > Gear.Rod.REINFORCED.rareOdds());
        assertTrue(Minigame.Tuning.of(Gear.Rod.ANGLERS, Gear.Tackle.CORK_BOBBER, false).zone() > Minigame.Tuning.of(Gear.Rod.PLAIN, null, false).zone());
    }
}
