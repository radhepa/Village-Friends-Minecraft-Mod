package dev.villagefriends;

import static org.junit.jupiter.api.Assertions.*;
import java.util.UUID;
import org.junit.jupiter.api.Test;

class GuardDamageLedgerTest {
    private static final UUID FIRST = new UUID(0, 1), SECOND = new UUID(0, 2);
    @Test void guardsReceiveOnlyTheirDamageShareIncludingPlayerAndOtherDamage() {
        var ledger = new GuardDamageLedger();
        ledger.record(0, 20, 15, null);
        ledger.record(1, 15, 10, FIRST);
        ledger.record(2, 10, 0, SECOND);
        var shares = ledger.shares(2, 10);
        assertEquals(2.5, shares.get(FIRST), 1e-9); assertEquals(5, shares.get(SECOND), 1e-9);
        assertEquals(7.5, shares.values().stream().mapToDouble(Double::doubleValue).sum(), 1e-9);
    }
    @Test void mitigatedHealthDamageCountsAndOverkillCannotInflateContribution() {
        var ledger = new GuardDamageLedger();
        ledger.record(0, 20, 18, FIRST); // Only two HP lost after armor.
        ledger.record(1, 18, -100, null); // Only the remaining 18 HP count.
        assertEquals(1, ledger.shares(1, 10).get(FIRST), 1e-9);
    }
    @Test void blockedDamageHealingAndInvalidNumbersEarnNoCredit() {
        var ledger = new GuardDamageLedger();
        assertFalse(ledger.record(0, 20, 20, FIRST));
        assertFalse(ledger.record(0, 10, 15, FIRST));
        assertFalse(ledger.record(0, Double.NaN, 0, FIRST));
        assertTrue(ledger.shares(0, 10).isEmpty());
    }
    @Test void creditExpiresAtThirtySecondsWhileRecentContributionsRemain() {
        var ledger = new GuardDamageLedger();
        ledger.record(0, 20, 10, FIRST);
        ledger.record(100, 10, 0, SECOND);
        assertEquals(5, ledger.shares(599, 10).get(FIRST), 1e-9);
        var remaining = ledger.shares(600, 10);
        assertFalse(remaining.containsKey(FIRST)); assertEquals(10, remaining.get(SECOND), 1e-9);
        assertTrue(ledger.empty(700));
    }
    @Test void unloadingAGuardClearsItsCreditWithoutRedistributingItsDamage() {
        var ledger = new GuardDamageLedger();
        ledger.record(0, 20, 10, FIRST); ledger.record(0, 10, 0, SECOND);
        ledger.forgetGuard(FIRST);
        assertFalse(ledger.shares(0, 10).containsKey(FIRST));
        assertEquals(5, ledger.shares(0, 10).get(SECOND), 1e-9);
    }
}
