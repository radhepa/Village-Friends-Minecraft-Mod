package dev.villagefriends;

import static org.junit.jupiter.api.Assertions.*;
import java.util.UUID;
import org.junit.jupiter.api.Test;

class GuardPolicyTest {
    @Test void villagersPredatorsAndActualAttackersQualifyButCreepersNeverDo() {
        assertTrue(GuardPolicy.threat(false, true, false, false));
        assertTrue(GuardPolicy.threat(false, false, true, false));
        assertTrue(GuardPolicy.threat(false, false, false, true));
        assertFalse(GuardPolicy.threat(false, false, false, false));
        for (int mask = 0; mask < 8; mask++)
            assertFalse(GuardPolicy.threat(true, (mask & 1) != 0, (mask & 2) != 0, (mask & 4) != 0));
    }
    @Test void forgivenessUsesTheEffectiveFriendTierRatherThanPointsAlone() {
        var forty = new FriendshipState(40, -1, -1, 0, "");
        assertFalse(GuardPolicy.forgives(BondState.NEW, forty));
        assertTrue(GuardPolicy.forgives(BondState.NEW.flag("shared_experience"), forty));
        assertFalse(GuardPolicy.forgives(BondState.NEW.flag("shared_experience"), new FriendshipState(39,-1,-1,0,"")));
        assertTrue(GuardPolicy.forgives(BondState.migrated(2), FriendshipState.NEW));
    }
    @Test void angerExpiresExactlyAtItsDeadlineAndCanBeRefreshed() {
        long firstHit = 50, secondHit = 100;
        assertTrue(GuardPolicy.angerActive(firstHit + 1199, firstHit + GuardPolicy.ANGER_TICKS));
        assertFalse(GuardPolicy.angerActive(firstHit + 1200, firstHit + GuardPolicy.ANGER_TICKS));
        assertTrue(GuardPolicy.angerActive(firstHit + 1200, secondHit + GuardPolicy.ANGER_TICKS));
    }
    @Test void armorAlwaysHasTwoDistinctIronSlotsAndIsStableAcrossLoads() {
        for (int n = 0; n < 100; n++) {
            var id = new UUID(n * 37L, n * 113L);
            var slots = GuardPolicy.ironSlots(id);
            assertEquals(2, slots.size()); assertEquals(2, slots.stream().distinct().count());
            assertTrue(slots.stream().allMatch(s -> s >= 0 && s < 4));
            assertEquals(slots, GuardPolicy.ironSlots(id));
        }
    }
}
