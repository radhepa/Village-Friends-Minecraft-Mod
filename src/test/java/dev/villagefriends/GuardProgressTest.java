package dev.villagefriends;

import static org.junit.jupiter.api.Assertions.*;
import com.google.gson.JsonParser;
import com.mojang.serialization.JsonOps;
import java.util.Random;
import java.util.UUID;
import org.junit.jupiter.api.Test;

class GuardProgressTest {
    @Test void veteransHaveStableLevelsInRangeWithMostNearTheMiddle() {
        var ids = new Random(397);
        int middle = 0, total = 0;
        for (int i = 0; i < 5000; i++) {
            var id = new UUID(ids.nextLong(), ids.nextLong());
            var guard = GuardProgress.initialize(null, id, false, false);
            assertTrue(guard.level() >= 15 && guard.level() <= 30);
            assertEquals(guard, GuardProgress.initialize(null, id, false, false));
            if (guard.level() >= 20 && guard.level() <= 25) middle++;
            total += guard.level();
        }
        assertTrue(middle > 2500);
        assertTrue(total / 5000D > 21 && total / 5000D < 24);
    }
    @Test void trainedGuardsStartAtZeroAndInitializationNeverRerollsSavedProgress() {
        var id = new UUID(73, 96);
        var rookie = GuardProgress.initialize(null, id, true, true);
        assertEquals(0, rookie.level()); assertEquals("trained", rookie.origin());
        var progressed = rookie.award(29.5).lock("villagefriends:archer");
        assertSame(progressed, GuardProgress.initialize(progressed, new UUID(99, 87), false, false));
        assertEquals("migrated", GuardProgress.initialize(null, id, false, true).origin());
    }
    @Test void fractionalCreditCarriesThroughSeveralLevelsWithoutRoundingAway() {
        var rookie = new GuardProgress(0, 0, "trained", "");
        assertEquals(0, rookie.award(19.75).level());
        assertEquals(1, rookie.award(19.75).award(.25).level());
        var next = rookie.award(20 + 23 + 26 + .75);
        assertEquals(3, next.level()); assertEquals(.75, next.xp(), 1e-9);
        assertEquals(80, GuardProgress.nextLevelXp(20));
    }
    @Test void ceilingAndInvalidAwardsCannotProduceUnboundedStats() {
        var last = new GuardProgress(49, 166, "trained", "").award(1);
        assertEquals(50, last.level()); assertEquals(0, last.xp());
        assertEquals(last, last.award(100000));
        assertEquals(10, last.extraHealth(), 1e-9); assertEquals(1.25, last.damageMultiplier(), 1e-9);
        assertEquals(3, new GuardProgress(15, 0, "generated", "").extraHealth(), 1e-9);
        assertEquals(1.15, new GuardProgress(30, 0, "generated", "").damageMultiplier(), 1e-9);
        assertEquals(last, last.award(Double.POSITIVE_INFINITY));
        var rookie = new GuardProgress(0, 0, "trained", "");
        assertEquals(rookie, rookie.award(-10)); assertEquals(rookie, rookie.award(Double.NaN));
    }
    @Test void repeatedFractionalAssistsReachTheWholeLevelThresholdDespiteFloatingPointDust() {
        var rookie = new GuardProgress(0, 0, "trained", "");
        for (int n = 0; n < 60; n++) rookie = rookie.award(1D / 3);
        assertEquals(1, rookie.level()); assertEquals(0, rookie.xp(), 1e-9);
    }
    @Test void firstValidProfessionLockCannotChangeToAnotherRoleOrNamespace() {
        var rookie = new GuardProgress(0, 1.25, "trained", "");
        assertEquals(rookie, rookie.lock("minecraft:knight"));
        var locked = rookie.lock("villagefriends:knight");
        assertEquals("villagefriends:knight", locked.lockedProfession());
        assertEquals(locked, locked.lock("villagefriends:archer"));
    }
    @Test void codecKeepsFractionalXpOriginAndProfessionAndNormalizesInvalidValues() {
        var saved = new GuardProgress(22, 12.375, "migrated", "villagefriends:archer");
        assertEquals(saved, GuardProgress.CODEC.parse(JsonOps.INSTANCE, GuardProgress.CODEC.encodeStart(JsonOps.INSTANCE, saved).getOrThrow()).getOrThrow());
        var bad = GuardProgress.CODEC.parse(JsonOps.INSTANCE, JsonParser.parseString("{\"level\":-9,\"xp\":-20,\"origin\":\"other\",\"locked_profession\":\"minecraft:knight\"}")).getOrThrow();
        assertEquals(new GuardProgress(0, 0, "trained", ""), bad);
    }
    @Test void strongerThreatsHaveHigherXpPools() {
        assertEquals(10, GuardProgress.killXp("minecraft:zombie"));
        assertEquals(10, GuardProgress.killXp("modded:actual_villager_attacker"));
        assertEquals(15, GuardProgress.killXp("minecraft:pillager"));
        assertEquals(20, GuardProgress.killXp("minecraft:vindicator"));
        assertEquals(20, GuardProgress.killXp("minecraft:illusioner"));
        assertEquals(20, GuardProgress.killXp("minecraft:zoglin"));
        assertEquals(30, GuardProgress.killXp("minecraft:evoker"));
        assertEquals(50, GuardProgress.killXp("minecraft:ravager"));
    }
}
