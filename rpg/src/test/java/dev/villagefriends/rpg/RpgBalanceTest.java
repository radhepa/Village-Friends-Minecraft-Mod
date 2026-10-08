package dev.villagefriends.rpg;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

/** The promises the balance makes: a weak start, a long climb, builds, and bosses that stay bosses. */
class RpgBalanceTest {
    @Test void weakStartReachesVanillaThenGrows() {
        assertEquals(12, Balance.baseHealth(1));
        assertEquals(20, Balance.baseHealth(20));
        assertEquals(36, Balance.baseHealth(100));
        assertEquals(1.4, Balance.hungerRate(1), 1e-9);
        assertEquals(1.0, Balance.hungerRate(20), 1e-9);
        assertEquals(.85, Balance.hungerRate(100), 1e-9);
        assertEquals(.75, Balance.meleeBase(1), 1e-9);
        assertEquals(.6, Balance.mineBase(1), 1e-9);
        assertEquals(1, Balance.mineBase(15), 1e-9);
        assertEquals(1, Balance.meleeBase(15), 1e-9);
        for (int l = 1; l < 100; l++) assertTrue(Balance.need(l + 1) > Balance.need(l));
    }
    @Test void levelHundredIsALongRoad() {
        long total = Balance.total(100);
        assertTrue(total > 500_000 && total < 1_000_000, "total " + total);
        // Points: 317 by level 100, can't max all ten attributes (500), so characters specialise.
        assertEquals(317, Balance.pointsThrough(100));
        assertTrue(Balance.pointsThrough(100) < Attr.values().length * Balance.ATTR_CAP);
        var s = Sheet.NEW.gain(total);
        assertEquals(100, s.level());
        assertEquals(317, s.points());
        assertEquals(2, Sheet.NEW.gain(Balance.need(1)).level());
    }
    @Test void bossesSurviveAMaxedCharacter() {
        // Max melee: level, 50 Strength, 50 Swordsmanship, Legend mastery, both boss perks, and a crit.
        double m = Balance.meleeBase(100) + .5 + .2 + .1 + .2 + Balance.CRIT_BONUS;
        float sharpVCrit = (8 + 3) * 1.5F;
        float hit = Balance.outgoing(sharpVCrit, m, true, 500);
        assertTrue(hit <= sharpVCrit + 500 * Balance.bossHitCap + 1e-3);
        assertTrue(500 / hit >= 15, "Warden must take 15+ hits, took " + 500 / hit);
        assertTrue(200 / Balance.outgoing(sharpVCrit, m, true, 200) >= 7);
        // Ordinary mobs get the full bonus, and the weak start applies to bosses too.
        assertEquals(sharpVCrit * m, Balance.outgoing(sharpVCrit, m, false, 20), 1e-3);
        assertEquals(10 * .75F, Balance.outgoing(10, Balance.meleeBase(1), true, 500), 1e-3);
        assertEquals(2.5F, Balance.incoming(10, 2), 1e-3);
    }
    @Test void repeatKillsAndMassKillsPayLess() {
        assertEquals(1, Balance.fatigue(1, 1), 1e-9);
        assertEquals(.5, Balance.fatigue(2, 1), 1e-9);
        assertEquals(.5, Balance.fatigue(10, 1), 1e-9);
        assertEquals(.4, Balance.fatigue(11, 1), 1e-9);
        assertTrue(Balance.fatigue(25, 1) < .05 + 1e-9);
        assertEquals(.25, Balance.fatigue(1, 5), 1e-9);
        assertEquals(.05, Balance.fatigue(2, 10), 1e-9);
    }
    @Test void skillsClimbToFifty() {
        assertEquals(0, Balance.skillLevel(0));
        assertEquals(1, Balance.skillLevel(Balance.skillNeed(0)));
        long all = 0; for (int s = 0; s < Balance.SKILL_CAP; s++) all += Balance.skillNeed(s);
        assertEquals(50, Balance.skillLevel(all));
        assertEquals(50, Balance.skillLevel(all * 10));
        for (var sk : Skill.values()) assertFalse(sk.effect(25).isBlank());
    }
    @Test void bestiaryTiersAndPerks() {
        assertEquals(22, Bestiary.FAMILIES.size());
        for (var f : Bestiary.FAMILIES) {
            for (int t = 1; t < 5; t++) assertTrue(f.rarity().tiers[t] > f.rarity().tiers[t - 1]);
            assertEquals(List.of(3, 5, 5), f.perks().stream().map(Bestiary.Perk::tier).toList(), f.id());
            assertEquals("active", f.active().kind(), f.id());
            assertTrue(f.active().amount() >= 8 && f.active().count() >= 1, f.id());
            assertEquals(0, f.tier(0)); assertEquals(5, f.tier(1_000_000)); assertEquals(-1, f.next(1_000_000));
        }
        assertEquals("zombie", Bestiary.ofMob("husk").id());
        var s = Sheet.NEW.kill("creeper", 1500).kill("enderman", 180);
        assertEquals(.6, s.perk("resist", "explosion"), 1e-9);
        assertEquals(1, s.perk("resist", "pearl"), 1e-9);
        assertFalse(s.special("steady_gaze"));
        assertTrue(Sheet.NEW.kill("witch", 900).immune("slowness"));
    }
    @Test void everyQuestGiverHasWorkAtEveryTier() {
        for (var job : List.of("armorer", "weaponsmith", "toolsmith", "mason", "farmer", "cook", "tavern_keeper", "fisherman", "butcher", "leatherworker",
                "tailor", "shepherd", "librarian", "scholar", "cartographer", "painter", "bard", "fletcher", "archer", "knight", "cleric", "apothecary", "carpenter")) {
            var pools = QuestBook.pools(job, false);
            assertFalse(pools.isEmpty(), job);
            for (int level : new int[]{1, 10, 25, 45, 70, 100}) for (long seed = 0; seed < 40; seed++) {
                var q = QuestBook.offer(pools, seed, level, "id", "giver", "Name", job);
                assertNotNull(q, job + " " + level);
                assertTrue(q.need() >= 1 && q.xp() > 0 && q.emeralds() > 0 && !q.label().isBlank(), q.toString());
                if (q.kind().equals("slay")) assertNotNull(Bestiary.byId(q.target()), q.target());
            }
        }
        assertTrue(QuestBook.pools("nitwit", false).isEmpty());
        assertEquals(List.of("guard"), QuestBook.pools("none", true));
        assertEquals("Explore the Ice Spikes", QuestBook.label("explore", "biome:minecraft:ice_spikes", 1));
        assertEquals("Bring 16 rotten flesh", QuestBook.label("gather", "minecraft:rotten_flesh", 16));
    }
    @Test void sheetRoundTripsThroughItsCodec() {
        var s = Sheet.NEW.gain(5000).spend(Attr.VITALITY, 3).skillGain(Skill.MINING, 400).kill("zombie", 30).mark("seen:fish", 4)
                .withQuests(List.of(new Quest("a:1", "slay", "zombie", 8, 3, "a", "Ada", "armorer", 50, 4, 8, "Slay 8 Zombies")));
        var json = Sheet.CODEC.encodeStart(com.mojang.serialization.JsonOps.INSTANCE, s).getOrThrow();
        assertEquals(s, Sheet.CODEC.parse(com.mojang.serialization.JsonOps.INSTANCE, json).getOrThrow());
        assertEquals(s.points() + 3, s.respec().points());
        assertEquals(s.level(), s.penalized(.25).level());
    }
}
