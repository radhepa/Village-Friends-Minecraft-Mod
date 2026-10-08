package dev.villagefriends;

import static org.junit.jupiter.api.Assertions.*;
import com.mojang.serialization.JsonOps;
import dev.villagefriends.deed.*;
import dev.villagefriends.quest.Board;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

/** What deeds are worth, how repeats fold together and fade, and how they make up a player's standing. */
class DeedScoringTest {
    private static final String ME = "00000000-0000-0000-0000-000000000001";
    private static final long DAY = 24000;
    private static DeedLog log() { return DeedLog.create(ME, "Steve"); }
    private static DeedLog add(DeedLog log, DeedKind kind, String key, long day, long tick, int count) {
        return log.record(kind, key, "", day, tick, List.of("victim"), count, false).log();
    }

    @Test void everyKindHasItsWorthSizeAndPrice() {
        for (var kind : DeedKind.values()) {
            assertEquals(kind, DeedKind.byId(kind.id()), "ids round-trip: " + kind);
            if (kind.good) { assertTrue(kind.points10 >= 0 && kind.halfLifeDays == 0, "good deeds never fade: " + kind); assertTrue(kind.rep >= 0); }
            else { assertTrue(kind.points10 < 0 && kind.halfLifeDays >= 7, "bad deeds fade over weeks: " + kind); assertTrue(kind.rep <= 0); }
        }
        assertEquals(0, DeedKind.NOTICE_ANSWERED.points10, "notices are counted in the board's favors, not twice");
        assertEquals(0, DeedKind.HIT_RESIDENT.rep, "vanilla already prices hitting a villager");
        assertTrue(DeedKind.RAID_WON.big() && DeedKind.REVIVED.big() && DeedKind.KILLED_RESIDENT.big() && DeedKind.KILLED_GOLEM.big());
        assertTrue(DeedKind.HIT_RESIDENT.violent() && !DeedKind.STOLE.violent() && !DeedKind.BROKE_HOME.violent());
    }

    @Test void pointsGrowWithRepeatsUpToTheirCap() {
        assertEquals(10, DeedKind.RAID_DEFENDED.points10(1, false));
        assertEquals(18, DeedKind.RAID_DEFENDED.points10(5, false), "+2 per raider after the first");
        assertEquals(30, DeedKind.RAID_DEFENDED.points10(40, false), "at most +30 for one raid");
        assertEquals(-10, DeedKind.HIT_RESIDENT.points10(1, false));
        assertEquals(-16, DeedKind.HIT_RESIDENT.points10(3, false), "-3 per extra hit");
        assertEquals(-25, DeedKind.HIT_RESIDENT.points10(20, false), "at most -25");
        assertEquals(10, DeedKind.SAVED_FROM_MONSTER.points10(1, false));
        assertEquals(15, DeedKind.SAVED_FROM_MONSTER.points10(1, true), "saving a child counts for more");
        assertEquals(-10, DeedKind.STOLE.points10(7, false));
        assertEquals(-12, DeedKind.STOLE.points10(16, false), "-1 per 8 items taken");
        assertEquals(-30, DeedKind.STOLE.points10(1000, false), "at most -30");
    }

    @Test void repeatsWithinTheMergeWindowFoldIntoOneDeed() {
        var log = add(log(), DeedKind.HIT_RESIDENT, "r:a", 0, 100, 1);
        log = add(log, DeedKind.HIT_RESIDENT, "r:a", 0, 100 + 1199, 1);
        assertEquals(1, log.deeds().size(), "two hits within a minute are one deed");
        assertEquals(2, log.deeds().getFirst().count());
        assertEquals(-13, log.deeds().getFirst().points10());
        log = add(log, DeedKind.HIT_RESIDENT, "r:a", 0, 100 + 1199 + 1300, 1);
        assertEquals(2, log.deeds().size(), "a hit a minute later is a new deed");
        log = add(log, DeedKind.HIT_RESIDENT, "r:b", 0, 100 + 1199 + 1310, 1);
        assertEquals(3, log.deeds().size(), "hitting someone else is another deed");
        // A raid folds every raider into one deed for as long as it lasts.
        var raid = log();
        for (int k = 0; k < 5; k++) raid = add(raid, DeedKind.RAID_DEFENDED, "raid:1", 0, k * 5000L, 1);
        assertEquals(1, raid.deeds().size()); assertEquals(18, raid.deeds().getFirst().points10());
        // Kinds that never merge: each revival is its own deed.
        var revived = add(add(log(), DeedKind.REVIVED, "", 0, 10, 1), DeedKind.REVIVED, "", 0, 20, 1);
        assertEquals(2, revived.deeds().size());
        assertEquals(2, revived.serial(), "serials count up");
    }

    @Test void badDeedsFadeByHalfLivesAndApologiesHalveWhatIsLeft() {
        var log = add(log(), DeedKind.KILLED_GOLEM, "", 0, 0, 1);
        assertEquals(-40, Standing.score10(0, log, 0));
        assertEquals(-20, Standing.score10(0, log, 14), "one half-life later");
        assertEquals(-10, Standing.score10(0, log, 28), "two half-lives later");
        var sorry = log.with(log.deeds().getFirst().apologize());
        assertEquals(-20, Standing.score10(0, sorry, 0), "an apology halves it");
        assertEquals(-10, Standing.score10(0, sorry, 14));
        var good = add(log(), DeedKind.REVIVED, "", 0, 0, 1);
        assertEquals(20, Standing.score10(0, good, 365), "good deeds never fade");
        assertEquals(1, Standing.apology(good.with(good.deeds().getFirst().apologize()).deeds().getFirst()), "apologies only touch bad deeds");
    }

    @Test void standingIsNoticesPlusDeedsWithTheSameFiveTitles() {
        assertEquals(30, Standing.score10(3, null, 0), "each notice is worth 10");
        for (int favors = 0; favors <= 25; favors++)
            assertEquals(Board.standing(favors), Standing.tier(Standing.score10(favors, null, 0)), "notices alone keep the board's thresholds: " + favors);
        assertEquals(0, Standing.tier(0)); assertEquals(1, Standing.tier(10)); assertEquals(2, Standing.tier(40));
        assertEquals(3, Standing.tier(100)); assertEquals(4, Standing.tier(200)); assertEquals(4, Standing.tier(5000));
        assertEquals(1, Standing.tier(39)); assertEquals(0, Standing.tier(9));
        assertEquals("Good Neighbor", Standing.title(2, "Ash")); assertEquals("Hero of Ash", Standing.title(4, "Ash"));
        // A revival and a raid won make a Good Neighbor of someone with one notice.
        var log = add(add(log(), DeedKind.REVIVED, "", 0, 0, 1), DeedKind.RAID_WON, "raid:1", 0, 10, 1);
        assertEquals(60, Standing.score10(1, log, 0));
        assertEquals(2, Standing.tier(Standing.score10(1, log, 0)));
        assertEquals("1 more notice to become Pillar of the Community", Standing.hint(90, "Ash"));
        assertEquals("4 more notices to become Pillar of the Community", Standing.hint(60, "Ash"));
    }

    @Test void slightlyNegativeStandingIsStillNewcomer() {
        var log = add(log(), DeedKind.HIT_RESIDENT, "r:a", 0, 0, 1);
        assertEquals(-10, Standing.score10(0, log, 0));
        assertEquals(0, Standing.tier(-10), "a single hit leaves you a Newcomer");
        assertEquals("Newcomer", Standing.title(Standing.tier(-19), "Ash"));
    }

    @Test void rewardsComeOnlyOnANewHighestTier() {
        var first = Standing.change(1, 2, 1);
        assertTrue(first.reward() && !first.fell(), "reaching Good Neighbor for the first time");
        assertFalse(Standing.change(1, 2, 2).reward(), "reaching it again after a fall brings no second reward");
        assertTrue(Standing.change(2, 1, 2).fell());
        assertFalse(Standing.change(Standing.UNWELCOME, 0, 0).reward(), "climbing back to Newcomer is no reward");
        assertFalse(Standing.change(0, 0, 0).reward());
        assertTrue(Standing.change(0, 4, 3).reward(), "jumping straight to Hero");
        var log = log().peak(2);
        assertEquals(2, log.peak(1).peakTier(), "the peak never goes down");
        assertEquals(3, log.peak(3).peakTier());
    }

    @Test void aFullLogBanksItsOldestGoodDeedsAndForgetsLongFadedBadOnes() {
        var log = log();
        for (int n = 0; n < DeedLog.MAX + 5; n++) log = add(log, DeedKind.BANDAGED, "", 0, n, 1);
        assertEquals(DeedLog.MAX, log.deeds().size());
        assertEquals(25, log.banked10(), "five bandagings banked");
        assertEquals(5 * (DeedLog.MAX + 5), Standing.score10(0, log, 0), "banking loses nothing");
        var bad = add(log(), DeedKind.HIT_GOLEM, "", 0, 0, 1);
        assertEquals(1, bad.pruned(28).deeds().size(), "four half-lives: still remembered");
        assertEquals(0, bad.pruned(29).deeds().size(), "past four half-lives it is forgotten");
    }

    @Test void hearsayIsLetGoAfterTheReactionWindow() {
        var r = log().record(DeedKind.KILLED_GOLEM, "", "", 0, 0, List.of(), 1, false);
        var d = r.deed().learn("a", Know.of(Know.SEEN, 0, "")).learn("b", Know.of(Know.HEARD, 1, "a"));
        var log = r.log().with(d);
        assertEquals(2, log.pruned(Deed.BAD_WINDOW).deeds().getFirst().knowers().size());
        var later = log.pruned(Deed.BAD_WINDOW + 1).deeds().getFirst();
        assertTrue(later.knows("a") && !later.knows("b"), "witnesses remember; hearsay fades");
    }

    @Test void knowingCloserReplacesHowYouKnewButNotWhatYouSaid() {
        var heard = Know.of(Know.HEARD, 1, "x").markTold();
        var seen = heard.closer(Know.of(Know.SEEN, 2, ""));
        assertEquals(Know.SEEN, seen.how()); assertTrue(seen.told());
        assertSame(seen, seen.closer(Know.of(Know.HEARD, 3, "y")), "hearing about it later changes nothing");
        assertTrue(Know.of(Know.INVOLVED, 0, "").firsthand() && Know.of(Know.SEEN, 0, "").firsthand());
        assertFalse(Know.of(Know.FAMILY, 0, "").firsthand() || Know.of(Know.HEARD, 0, "").firsthand());
    }

    @Test void theBookRoundTripsAndStartsEmpty() {
        var log = add(add(log(), DeedKind.REVIVED, "", 3, 3 * DAY, 1), DeedKind.STOLE, "house:v:g:a", 4, 4 * DAY, 16).peak(2);
        var deed = log.deeds().getLast().learn("w", Know.of(Know.SEEN, 4, "")).learn("x", Know.of(Know.HEARD, 5, "w").markTold().markKept()).apologize();
        log = log.with(deed);
        var book = DeedBook.EMPTY.put("natural:0:0", log);
        var json = DeedBook.CODEC.encodeStart(JsonOps.INSTANCE, book).getOrThrow();
        var back = DeedBook.CODEC.parse(JsonOps.INSTANCE, json).getOrThrow();
        assertEquals(book, back);
        assertEquals(DeedBook.FORMAT, back.format());
        assertEquals(DeedBook.EMPTY, DeedBook.CODEC.parse(JsonOps.INSTANCE, new com.google.gson.JsonObject()).getOrThrow(), "absent means empty");
        assertNull(DeedBook.EMPTY.log("natural:0:0", ME));
        assertSame(book, book.put("natural:0:0", log), "putting the same log changes nothing");
        assertEquals(Map.of(), DeedBook.EMPTY.logs("nowhere"));
    }

    @Test void residentsBringUpWhatTouchedThemMostFirst() {
        var log = log();
        var heard = log.record(DeedKind.KILLED_GOLEM, "", "", 0, 0, List.of(), 1, false);
        var help = heard.log().record(DeedKind.BANDAGED, "r:k", "", 0, 10, List.of("k"), 1, false);
        log = help.log().with(heard.deed().learn("me", Know.of(Know.HEARD, 1, "x")))
                .with(help.deed().learn("me", Know.of(Know.FAMILY, 0, "k")));
        assertEquals(DeedKind.BANDAGED, Reactions.pick(log.deeds(), "me", 1).kind(), "family before hearsay, however big");
        var told = log.with(log.find(2).replace("me", log.find(2).know("me").markTold()));
        assertEquals(DeedKind.KILLED_GOLEM, Reactions.pick(told.deeds(), "me", 1).kind(), "then the next one");
        assertNull(Reactions.pick(told.deeds(), "me", 1 + Deed.BAD_WINDOW + 1), "stale deeds aren't brought up");
        assertNull(Reactions.pick(told.deeds(), "stranger", 1));
        // The poster of an answered notice says thank you their own way.
        var notice = log().record(DeedKind.NOTICE_ANSWERED, "", "", 0, 0, List.of("poster"), 1, false).deed().learn("poster", Know.of(Know.INVOLVED, 0, ""));
        assertNull(Reactions.pick(List.of(notice), "poster", 0));
    }

    @Test void reactionPoolsFollowHowTheyKnowAndWhoTheyAre() {
        var seen = Know.of(Know.SEEN, 0, ""); var heard = Know.of(Know.HEARD, 0, "t");
        var self = Know.of(Know.INVOLVED, 0, ""); var family = Know.of(Know.FAMILY, 0, "v");
        assertEquals(List.of("deed.hit_golem.seen", "deed.bad.seen.curious"), Reactions.pools(DeedKind.HIT_GOLEM, seen, "curious", false, 0));
        assertEquals(List.of("deed.bad.heard.curious", "deed.hit_golem.heard"), Reactions.pools(DeedKind.HIT_GOLEM, heard, "curious", false, 99));
        assertEquals("deed.revived.self", Reactions.pools(DeedKind.REVIVED, self, "gentle", false, 0).getFirst());
        assertTrue(Reactions.pools(DeedKind.REVIVED, self, "gentle", false, 0).contains("deed.revived.seen"), "falls back to what a witness says");
        assertEquals("deed.revived.family", Reactions.pools(DeedKind.REVIVED, family, "gentle", false, 0).getFirst());
        assertEquals(List.of("baby.deed.revived.self", "baby.deed.good.seen"), Reactions.pools(DeedKind.REVIVED, self, "gentle", true, 0));
        assertEquals(List.of("baby.deed.bad.family", "baby.deed.bad.heard"), Reactions.pools(DeedKind.KILLED_PET, family, "gentle", true, 0));
        int flavored = 0;
        for (int roll = 0; roll < 100; roll++) if (Reactions.pools(DeedKind.RAID_WON, seen, "playful", false, roll).getFirst().startsWith("deed.good.")) flavored++;
        assertEquals(100 - Reactions.KIND_WEIGHT, flavored, "the personality speaks first 30% of the time");
        assertEquals("deed.kept.revived.family", Reactions.kept(DeedKind.REVIVED, true));
        assertEquals(List.of("baby.greet.unwelcome"), Reactions.unwelcome("gentle", true, 50));
        assertEquals(List.of("greet.unwelcome", "greet.unwelcome.gentle"), Reactions.unwelcome("gentle", false, 10));
        assertEquals(List.of("greet.unwelcome.gentle", "greet.unwelcome"), Reactions.unwelcome("gentle", false, 90));
    }
}
