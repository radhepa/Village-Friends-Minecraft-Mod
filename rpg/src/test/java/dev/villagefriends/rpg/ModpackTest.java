package dev.villagefriends.rpg;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

import java.util.HashSet;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

/** The add-on's links to the rest of the Village Friends modpack: monsters, places, jobs and seasons. */
class ModpackTest {
    @AfterEach void everyModInstalledAgain() { Modpack.detect(id -> true); }

    @Test void modpackMonstersFindTheirFamilies() {
        assertEquals("zombie", Bestiary.of("nsvmobs:sporeling").id());
        assertEquals("zombie", Bestiary.of("nsvmobs:scarecrow").id());
        assertEquals("skeleton", Bestiary.of("nsvmobs:soulpyre").id());
        assertEquals("phantom", Bestiary.of("nsvmobs:vulture").id());
        assertEquals("slime", Bestiary.of("nsvmobs:bog_lurker").id());
        assertEquals("challenger", Bestiary.of("nsvmobs:broodmother").id());
        assertEquals("challenger", Bestiary.of("nsvmobs:oregorger").id());
        assertEquals("plata", Bestiary.of("plataclan:plata_warden").id());
        assertEquals("silver_mother", Bestiary.of("plataclan:silver_mother").id());
        assertNull(Bestiary.of("endexpansion:shulkin"), "peoples are never prey");
        assertNull(Bestiary.of("seafriends:merfolk"));
        // Village Friends' own monsters (and other mods' by path) still go through ofMob.
        assertEquals("illager", Bestiary.of("minecraft:vindicator").id());
        // All ten Challengers and every NSV monster the add-on lists map to a real family.
        assertEquals(10, Bestiary.byId("challenger").mobs().size());
        Bestiary.modpackMobs().forEach((mob, family) -> assertNotNull(Bestiary.byId(family), mob));
        assertTrue(Bestiary.modpackMobs().size() >= 29, "modpack mobs " + Bestiary.modpackMobs().size());
    }

    @Test void newFamiliesFollowTheRules() {
        for (var id : List.of("challenger", "plata", "silver_mother")) {
            var f = Bestiary.byId(id);
            assertFalse(f.mod().isEmpty(), id);
            assertEquals(List.of(3, 5, 5), f.perks().stream().map(Bestiary.Perk::tier).toList(), id);
            assertEquals("active", f.active().kind(), id);
        }
        assertTrue(Bestiary.byId("silver_mother").boss());
        assertEquals(Bestiary.Rarity.ELITE, Bestiary.byId("challenger").rarity());
        var s = Sheet.NEW.kill("plata", 300).kill("silver_mother", 8).kill("challenger", 15);
        assertTrue(s.special("plata_sight"));
        assertEquals(.20, s.perk("resist", "projectile"), 1e-9);
        assertEquals(.30, s.perk("resist", "silver"), 1e-9);
        assertEquals(6, s.perk("attr", "max_health"), 1e-9);
        assertTrue(s.special("trophy_hunter"));
        // Without their mods, those families are hidden.
        Modpack.detect(id -> false);
        assertTrue(Bestiary.shown().stream().allMatch(f -> f.mod().isEmpty()));
        assertEquals(22, Bestiary.shown().size());
    }

    @Test void atlasListsEveryPlaceOnce() {
        var ids = new HashSet<String>(); var structures = new HashSet<String>();
        for (var pl : Atlas.PLACES) {
            assertTrue(ids.add(pl.id()), pl.id());
            assertTrue(pl.tier() >= 1 && pl.tier() <= 5, pl.id());
            assertTrue(Modpack.MODS.containsKey(pl.mod()), pl.id());
            for (var st : pl.structures()) { assertTrue(structures.add(st), st); assertEquals(pl.mod(), Modpack.modOf(st)); assertSame(pl, Atlas.ofStructure(st)); }
        }
        assertEquals(12, Atlas.byId("plataclan:den").structures().size() + Atlas.byId("plataclan:warren").structures().size());
        assertEquals("Find the Sunken Forge", Atlas.byId("caveexpansion:forge").findLabel());
        for (int t = 1; t <= 5; t++) assertFalse(Atlas.questsAt(t).isEmpty(), "tier " + t);
        Modpack.detect(id -> id.equals("villagefriends"));
        assertTrue(Atlas.shown().stream().allMatch(pl -> pl.mod().equals("villagefriends")));
        assertTrue(Atlas.questsAt(5).isEmpty());
        // Discoveries pay more for farther places, and something at every level.
        for (int level : new int[]{1, 30, 100}) {
            assertTrue(Balance.discoveryXp(1, level) > 0);
            assertTrue(Balance.discoveryXp(5, level) > 2 * Balance.discoveryXp(1, level), "level " + level);
        }
    }

    @Test void theModpacksFolkGiveWork() {
        for (var job : List.of("miner", "lightkeeper", "smuggler", "pearl_diver", "kelp_farmer", "shellwright", "tide_singer", "lightwright", "spongekeeper")) {
            var pools = QuestBook.pools(job, false);
            assertFalse(pools.isEmpty(), job);
            for (int level : new int[]{1, 10, 25, 45, 70, 100}) for (long seed = 0; seed < 40; seed++) {
                var q = QuestBook.offer(pools, seed, level, "id", "giver", "Name", job);
                assertNotNull(q, job + " " + level);
                assertFalse(q.label().isBlank());
            }
        }
        // Every template's names make sense, whatever mod they come from.
        for (var pool : QuestBook.poolNames()) for (var t : QuestBook.pool(pool)) {
            assertTrue(t.minTier() >= 1 && t.minTier() <= 5 && t.base() >= 1, pool + " " + t);
            assertTrue(t.when().isEmpty() || t.when().matches("[@!](spring|summer|autumn|winter)(\\|(spring|summer|autumn|winter))*"), pool + " " + t);
            if (t.kind().equals("slay")) assertNotNull(Bestiary.byId(t.target()), pool + " " + t);
            if (t.kind().equals("explore") && !t.target().equals("*")) assertNotNull(Atlas.byId(t.target().substring(6)), pool + " " + t);
            if (!t.mod().isEmpty()) assertTrue(Modpack.MODS.containsKey(t.mod()), pool + " " + t);
        }
        assertEquals("Find the Sunken Forge", QuestBook.label("explore", "place:caveexpansion:forge", 1));
        assertEquals("Defeat a Challenger", QuestBook.label("slay", "challenger", 1));
        assertEquals("Unmask 3 Plata", QuestBook.label("slay", "plata", 3));
        assertEquals("Defeat The Silver Mother", QuestBook.label("slay", "silver_mother", 1));
        assertEquals("Bring 2 pearl", QuestBook.label("gather", "oceanexpansion:pearl", 2));
    }

    @Test void missingModsNeverSetJobs() {
        Modpack.detect(id -> id.equals("villagefriends"));
        assertTrue(QuestBook.pools("miner", false).size() > 0, "the pool exists, but its modded work is filtered");
        for (var job : List.of("armorer", "cleric", "fisherman", "cartographer", "painter", "librarian", "knight", "cook", "miner", "smuggler", "pearl_diver"))
            for (int level : new int[]{1, 25, 45, 70, 100}) for (long seed = 0; seed < 60; seed++) {
                var q = QuestBook.offer(QuestBook.pools(job, job.equals("knight")), seed, level, "id", "g", "N", job);
                if (q == null) continue;
                var mod = new QuestBook.Template(q.kind(), q.target().replaceFirst("^minecraft:", ""), 1, 1, 0).mod();
                assertTrue(mod.isEmpty() || mod.equals("villagefriends"), job + " offered " + q);
            }
    }

    @Test void jobsFollowTheSeasons() {
        var farm = List.of("farm");
        boolean harvestInAutumn = false;
        for (long seed = 0; seed < 400; seed++) {
            var winter = QuestBook.offer(farm, seed, 30, "id", "g", "N", "farmer", "winter");
            assertNotEquals("harvest", winter.kind(), "no crop jobs in winter: " + winter);
            assertNotEquals("minecraft:wheat_seeds", winter.target());
            var autumn = QuestBook.offer(farm, seed, 30, "id", "g", "N", "farmer", "autumn");
            assertNotEquals("minecraft:hay_block", autumn.target());
            harvestInAutumn |= autumn.kind().equals("harvest");
        }
        assertTrue(harvestInAutumn);
        assertTrue(new QuestBook.Template("gather", "hay_block", 1, 1, .1, "@winter").inSeason(""), "no seasons mod: everything is open");
    }
}
