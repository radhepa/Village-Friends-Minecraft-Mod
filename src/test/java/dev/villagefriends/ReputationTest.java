package dev.villagefriends;

import static org.junit.jupiter.api.Assertions.*;
import dev.villagefriends.deed.*;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

/**
 * Deeds in trade prices (the term added to vanilla's villager reputation) and the Unwelcome standing
 * below Newcomer.
 */
class ReputationTest {
    private static final String ME = "player";
    private static Deed deed(DeedKind kind, long day, String resident, int how) {
        return new Deed(1, kind, "", "", day, day * 24000, List.of(), 1, kind.points10, false, day, Map.of()).learn(resident, Know.of(how, day, ""));
    }
    private static DeedLog log(DeedKind... kinds) {
        var log = DeedLog.create(ME, "Steve");
        for (var kind : kinds) log = log.record(kind, "", "", 0, 0, List.of(), 1, false).log();
        return log;
    }

    @Test void howTheyKnowWeighsWhatItMeansToThem() {
        assertEquals(-20, Standing.reputation(List.of(deed(DeedKind.KNOCKED_OUT_RESIDENT, 0, "r", Know.INVOLVED)), "r", 0));
        assertEquals(-16, Standing.reputation(List.of(deed(DeedKind.KNOCKED_OUT_RESIDENT, 0, "r", Know.FAMILY)), "r", 0));
        assertEquals(-12, Standing.reputation(List.of(deed(DeedKind.KNOCKED_OUT_RESIDENT, 0, "r", Know.SEEN)), "r", 0));
        assertEquals(-6, Standing.reputation(List.of(deed(DeedKind.KNOCKED_OUT_RESIDENT, 0, "r", Know.HEARD)), "r", 0));
        assertEquals(0, Standing.reputation(List.of(deed(DeedKind.KNOCKED_OUT_RESIDENT, 0, "r", Know.SEEN)), "someone else", 0), "only what they know");
        assertEquals(9, Standing.reputation(List.of(deed(DeedKind.REVIVED, 0, "r", Know.SEEN)), "r", 0), "a witness to a revival gives better prices");
        assertEquals(15, Standing.reputation(List.of(deed(DeedKind.REVIVED, 0, "r", Know.INVOLVED)), "r", 400), "good deeds never fade");
    }

    @Test void hittingAResidentAddsNothingBecauseVanillaAlreadyPricesIt() {
        for (int how = Know.INVOLVED; how <= Know.HEARD; how++)
            assertEquals(0, Standing.reputation(List.of(deed(DeedKind.HIT_RESIDENT, 0, "r", how)), "r", 0));
        assertEquals(0, Standing.reputation(List.of(deed(DeedKind.NOTICE_ANSWERED, 0, "r", Know.INVOLVED)), "r", 0), "notices keep their own vanilla gossip");
    }

    @Test void theTermIsClampedSoTheModNeverTurnsGolemsHostileByItself() {
        var bad = List.of(deed(DeedKind.KILLED_RESIDENT, 0, "r", Know.FAMILY), deed(DeedKind.KILLED_GOLEM, 0, "r", Know.SEEN), deed(DeedKind.KILLED_PET, 0, "r", Know.INVOLVED));
        assertEquals(Standing.REP_MIN, Standing.reputation(bad, "r", 0));
        assertTrue(Standing.REP_MIN > -100, "vanilla golems turn hostile at -100");
        var good = List.of(deed(DeedKind.RAID_WON, 0, "r", Know.SEEN), deed(DeedKind.REVIVED, 0, "r", Know.INVOLVED), deed(DeedKind.RAID_DEFENDED, 0, "r", Know.SEEN),
                deed(DeedKind.SAVED_FROM_MONSTER, 0, "r", Know.INVOLVED), deed(DeedKind.BANDAGED, 0, "r", Know.INVOLVED));
        assertEquals(Standing.REP_MAX, Standing.reputation(good, "r", 0));
    }

    @Test void pricesFadeWithTheDeedAndAnApologyHalvesThem() {
        var d = deed(DeedKind.KILLED_GOLEM, 0, "r", Know.INVOLVED);
        assertEquals(-25, Standing.reputation(List.of(d), "r", 0));
        assertEquals(-12, Standing.reputation(List.of(d), "r", 14), "one half-life later");
        assertEquals(-6, Standing.reputation(List.of(d), "r", 28));
        assertEquals(-12, Standing.reputation(List.of(d.apologize()), "r", 0), "an apology halves it");
    }

    @Test void unwelcomeStartsAtMinusTwentyAndOnlyDeedsGetYouThere() {
        assertEquals(0, Standing.tier(-19), "just above the line: Newcomer");
        assertEquals(Standing.UNWELCOME, Standing.tier(-20), "on the line: Unwelcome");
        assertEquals(Standing.UNWELCOME, Standing.tier(-500));
        assertEquals("Unwelcome", Standing.title(Standing.UNWELCOME, "Ash"));
        assertTrue(Standing.hint(-20, "Ash").startsWith("Nobody here will give you work"));
        for (int favors = 0; favors < 30; favors++) assertNotEquals(Standing.UNWELCOME, Standing.tier(Standing.score10(favors, null, 0)), "notices alone never make you Unwelcome");
        // One hit: Newcomer. Hitting the golem and knocking a resident out: Unwelcome.
        assertEquals(0, Standing.tier(Standing.score10(0, log(DeedKind.HIT_RESIDENT), 0)));
        assertEquals(0, Standing.tier(Standing.score10(0, log(DeedKind.HIT_GOLEM, DeedKind.HIT_RESIDENT), 0)), "-15: wary, but still a Newcomer");
        assertEquals(Standing.UNWELCOME, Standing.tier(Standing.score10(0, log(DeedKind.HIT_GOLEM, DeedKind.HURT_PET), 0)), "-20 exactly");
        assertEquals(Standing.UNWELCOME, Standing.tier(Standing.score10(0, log(DeedKind.KNOCKED_OUT_RESIDENT), 0)));
        // Six notices answered don't outweigh a death; seven do.
        assertEquals(Standing.UNWELCOME, Standing.tier(Standing.score10(6, log(DeedKind.KILLED_RESIDENT), 0)));
        assertEquals(0, Standing.tier(Standing.score10(7, log(DeedKind.KILLED_RESIDENT), 0)));
    }

    @Test void unwelcomeWearsOffWithTimeApologiesAndGoodDeeds() {
        var killed = log(DeedKind.KILLED_RESIDENT);
        assertEquals(Standing.UNWELCOME, Standing.tier(Standing.score10(0, killed, 0)));
        assertEquals(Standing.UNWELCOME, Standing.tier(Standing.score10(0, killed, 56)), "two half-lives: -20, still Unwelcome");
        assertEquals(0, Standing.tier(Standing.score10(0, killed, 60)), "fading back to Newcomer");
        var knocked = log(DeedKind.KNOCKED_OUT_RESIDENT);
        var sorry = knocked.with(knocked.deeds().getFirst().apologize());
        assertEquals(0, Standing.tier(Standing.score10(0, sorry, 0)), "an apology takes -30 to -15");
        assertEquals(0, Standing.tier(Standing.score10(0, log(DeedKind.KNOCKED_OUT_RESIDENT, DeedKind.BANDAGED, DeedKind.BIRTHDAY_GIFT, DeedKind.PET_KINDNESS), 0)), "good deeds make up for it (-19)");
        assertEquals(Standing.UNWELCOME, Standing.tier(Standing.score10(0, log(DeedKind.KNOCKED_OUT_RESIDENT, DeedKind.BANDAGED), 0)), "-25: not yet");
    }
}
