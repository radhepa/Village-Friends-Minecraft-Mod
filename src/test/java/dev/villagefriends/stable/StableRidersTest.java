package dev.villagefriends.stable;

import static org.junit.jupiter.api.Assertions.*;

import dev.villagefriends.stable.bond.BondMath;
import dev.villagefriends.stable.ride.MountedPace;
import dev.villagefriends.stable.ride.SpookRule;
import dev.villagefriends.stable.ride.SpookRule.Reaction;
import dev.villagefriends.stable.ride.TheftRule;
import dev.villagefriends.stable.ride.TheftRule.Seen;
import dev.villagefriends.stable.ride.TheftRule.Verdict;
import java.util.Random;
import org.junit.jupiter.api.Test;

/** Residents' horses: squad pace, horse theft and returns, and horses taking fright. */
class StableRidersTest {
    private static final double INF = Double.POSITIVE_INFINITY;
    /**
     * Horse speeds from a slow draft horse to the fastest courser (vanilla: 0.1125 to 0.3375). Below 1/6 the
     * {@link MountedPace#MAX} clamp keeps a very slow horse from being driven harder than x3, so it lags a little.
     */
    private static final double[] HORSE_SPEEDS = {0.17, 0.18, 0.2, 0.225, 0.26, 0.3, 0.3375};

    // -- MountedPace -----------------------------------------------------------------------------------

    @Test void aHorseInAMixedSquadCoversGroundLikeTheWalkers() {
        for (double walk : new double[]{.45, .5, .55, .6, .7}) for (double horse : HORSE_SPEEDS) {
            double pace = MountedPace.modifier(1, MountedPace.RIDER_BASE, horse, false);
            assertEquals(MountedPace.RIDER_BASE * walk, horse * walk * pace, 1e-9, "walk " + walk + " on a horse of speed " + horse);
            assertEquals(walk * pace, MountedPace.modifier(walk, MountedPace.RIDER_BASE, horse, false), 1e-9, "scaling the walk modifier is the same thing");
        }
    }

    @Test void aWhollyMountedSquadTrots() {
        for (double horse : HORSE_SPEEDS) {
            double walkers = MountedPace.modifier(.45, .5, horse, false), riders = MountedPace.modifier(.45, .5, horse, true);
            if (riders < MountedPace.MAX) assertEquals(MountedPace.TROT, riders / walkers, 1e-9, "speed " + horse);
            assertTrue(riders > walkers, "an all-mounted squad is faster than walkers on speed " + horse);
        }
    }

    @Test void thePaceIsClampedAndSafeWithAStoppedHorse() {
        assertEquals(MountedPace.MAX, MountedPace.modifier(1, .5, 0.01, true), 1e-9, "a near-motionless horse is not driven at x50");
        assertEquals(MountedPace.MIN, MountedPace.modifier(.1, .5, 10, false), 1e-9, "a very fast horse never crawls");
        assertEquals(1, MountedPace.modifier(1, .5, 0, false), 1e-9);
        assertEquals(1, MountedPace.modifier(1, .5, Double.NaN, true), 1e-9);
        var r = new Random(7);
        for (int i = 0; i < 10_000; i++) {
            double m = MountedPace.modifier(r.nextDouble() * 3, .5, r.nextDouble() * .5, r.nextBoolean());
            assertTrue(m >= MountedPace.MIN && m <= MountedPace.MAX, "clamped: " + m);
        }
    }

    @Test void mountedFollowersKeepWiderGaps() {
        assertEquals(1.0, MountedPace.spacing(false));
        assertEquals(1.7, MountedPace.spacing(true));
        assertTrue(2.5 * MountedPace.spacing(true) > 1.4 * 2, "two horses side by side never overlap at the follow distance");
    }

    // -- TheftRule -------------------------------------------------------------------------------------

    private static Verdict ridden(double distance, boolean found, boolean byThief, String stolenBy, long awaySince, long returnedAt, long now) {
        return TheftRule.assess(Seen.withPlayer(distance, found, byThief), !stolenBy.isEmpty(), awaySince, returnedAt, now);
    }
    private static Verdict alone(double distance, boolean loose, long alone, double nearestPlayer, String stolenBy, long awaySince, long now) {
        return TheftRule.assess(Seen.withoutPlayer(distance, loose, alone, nearestPlayer), !stolenBy.isEmpty(), awaySince, 0, now);
    }

    @Test void aHorseIsStolenOnlyWhenAPlayerTakesItBeyondFortyEightBlocks() {
        for (double d : new double[]{0, 5, 8, 20, 47.9, 48}) assertEquals(Verdict.NONE, ridden(d, false, false, "", 0, 0, 1000), "still near home at " + d);
        assertEquals(Verdict.STOLEN, ridden(48.1, false, false, "", 0, 0, 1000));
        assertEquals(Verdict.STOLEN, ridden(500, false, false, "", 0, 0, 1000));
        assertEquals(Verdict.STOLEN, ridden(INF, false, false, "", 0, 0, 1000), "taken to another dimension");
        assertEquals(Verdict.NONE, ridden(60, false, true, "thief", 0, 0, 1000), "already flagged: one deed per theft");
        // Without a player it is never theft, however far it goes (a knight's patrol, a horse that bolted).
        for (double d : new double[]{49, 100, INF}) assertNotEquals(Verdict.STOLEN, alone(d, false, 0, INF, "", 0, 1000));
    }

    @Test void aHorseFoundFarFromHomeIsLostNotStolen() {
        assertEquals(Verdict.LOST, ridden(60, true, false, "", 0, 0, 1000), "picked up out there: the finder is not a thief");
        assertEquals(Verdict.NONE, ridden(60, true, false, "", 500, 0, 1000), "already known to be lost");
        assertEquals(Verdict.NONE, ridden(30, true, false, "", 0, 0, 1000), "picked up near home is just a ride");
    }

    @Test void onlyAHorseNoPlayerHasHadForAMinuteIsFound() {
        long now = 90_000;
        assertTrue(TheftRule.found(-1, now), "no player has had it since the server started (a knight left it out)");
        assertTrue(TheftRule.found(now - TheftRule.ALONE - 1, now), "nobody has had it for over a minute");
        assertFalse(TheftRule.found(now - TheftRule.ALONE, now), "exactly a minute is not over a minute");
        assertFalse(TheftRule.found(now - 40, now), "let go a moment ago");
        // Riding a village horse to 47 blocks, hopping off and straight back on, then riding on is still theft.
        for (long off : new long[]{0, 40, 80, 600, TheftRule.ALONE}) {
            boolean found = TheftRule.found(now - off, now);
            assertEquals(Verdict.STOLEN, ridden(49, found, false, "", 0, 0, now), "back in the saddle after " + off + " ticks");
        }
    }

    @Test void aHorseLeftAloneFarAwayIsLostAfterAMinute() {
        assertEquals(Verdict.NONE, alone(60, true, TheftRule.ALONE, INF, "", 0, 5000), "exactly a minute is not over a minute");
        assertEquals(Verdict.LOST, alone(60, true, TheftRule.ALONE + 1, INF, "", 0, 5000));
        assertEquals(Verdict.LOST, alone(60, true, TheftRule.ALONE + 1, 5, "", 0, 5000), "a player standing nearby doesn't change that");
        assertEquals(Verdict.LOST, alone(60, true, 5000, INF, "thief", 0, 6000), "a stolen horse left far away is lost too");
        assertEquals(Verdict.NONE, alone(60, true, 5000, INF, "", 3000, 9000), "lost once, not again");
        assertEquals(Verdict.DRIFT, alone(30, true, 5000, 40, "", 0, 9000), "within 48 blocks it isn't lost: it drifts home when nobody is near");
        assertEquals(Verdict.NONE, alone(30, true, 5000, 10, "", 0, 9000), "and waits while a player is close");
    }

    @Test void aNonThiefBringingItHomeEarnsReturnedAHorse() {
        assertEquals(Verdict.RETURNED, ridden(8, false, false, "thief", 0, 0, 10_000), "a stolen horse brought within 8 blocks");
        assertEquals(Verdict.RETURNED, ridden(3, false, false, "", 4000, 0, 10_000), "a lost horse brought home");
        assertEquals(Verdict.NONE, ridden(8.5, false, false, "thief", 0, 0, 10_000), "not quite home yet");
        assertEquals(Verdict.NONE, ridden(4, false, false, "", 0, 0, 10_000), "an unflagged horse ridden home is nothing special");
    }

    @Test void theThiefBringingItBackOnlyClearsTheFlags() {
        assertEquals(Verdict.HOME, ridden(5, false, true, "thief", 0, 0, 10_000));
        assertEquals(Verdict.HOME, ridden(5, false, true, "thief", 4000, 0, 10_000), "even after it was also lost");
    }

    @Test void oneReturnedAHorsePerHorsePerDay() {
        long first = 50_000;
        assertEquals(Verdict.RETURNED, ridden(2, false, false, "", 1, 0, first));
        assertEquals(Verdict.HOME, ridden(2, false, false, "", 1, first, first + 1), "led out and straight back: no second deed");
        assertEquals(Verdict.HOME, ridden(2, false, false, "thief", 0, first, first + TheftRule.COOLDOWN - 1), "a day minus a tick");
        assertEquals(Verdict.RETURNED, ridden(2, false, false, "thief", 0, first, first + TheftRule.COOLDOWN), "a full day later it counts");
        assertTrue(TheftRule.cooled(0, 5) && !TheftRule.cooled(10, 10 + TheftRule.COOLDOWN - 1) && TheftRule.cooled(10, 10 + TheftRule.COOLDOWN));
    }

    @Test void aFlaggedHorseBackHomeWithoutAPlayerIsHome() {
        assertEquals(Verdict.HOME, alone(6, true, 0, INF, "", 3000, 9000));
        assertEquals(Verdict.HOME, alone(6, true, 0, 2, "thief", 0, 9000));
        assertEquals(Verdict.NONE, alone(6, true, 0, INF, "", 0, 9000), "an unflagged horse at home needs nothing");
    }

    @Test void onlyAnUnflaggedLooseHorseWithNobodyNearDrifts() {
        for (double d : new double[]{8.1, 20, 48}) assertEquals(Verdict.DRIFT, alone(d, true, 0, 32.1, "", 0, 9000), "drifts from " + d);
        assertEquals(Verdict.DRIFT, alone(20, true, 0, INF, "", 0, 9000), "no player in the world at all");
        assertEquals(Verdict.NONE, alone(8, true, 0, INF, "", 0, 9000), "within 8 blocks it is home");
        assertEquals(Verdict.NONE, alone(20, true, 0, 32, "", 0, 9000), "a player 32 blocks away would see it move");
        assertEquals(Verdict.NONE, alone(20, false, 0, INF, "", 0, 9000), "a knight is riding it, or it is tied up");
        assertEquals(Verdict.NONE, alone(20, true, 0, INF, "thief", 0, 9000), "a stolen horse doesn't sneak home");
        assertEquals(Verdict.NONE, alone(20, true, 0, INF, "", 3000, 9000), "nor does a lost one");
        assertNotEquals(Verdict.DRIFT, alone(48.1, true, 0, INF, "", 0, 9000), "beyond 48 blocks it waits to be found");
        assertNotEquals(Verdict.DRIFT, ridden(20, false, false, "", 0, 0, 9000), "never while a player rides it");
    }

    @Test void everyCombinationGivesOneSensibleVerdict() {
        var r = new Random(7);
        for (int i = 0; i < 20_000; i++) {
            double d = r.nextInt(10) == 0 ? INF : r.nextDouble() * 120;
            boolean player = r.nextBoolean(), found = r.nextBoolean(), thief = r.nextBoolean(), loose = r.nextBoolean();
            boolean stolen = r.nextBoolean(); long away = r.nextBoolean() ? 0 : 1 + r.nextInt(50_000);
            long returned = r.nextBoolean() ? 0 : 1 + r.nextInt(50_000), now = 60_000 + r.nextInt(50_000), aloneFor = r.nextInt(3000);
            var seen = player ? Seen.withPlayer(d, found, thief && stolen) : Seen.withoutPlayer(d, loose, aloneFor, r.nextDouble() * 80);
            var v = TheftRule.assess(seen, stolen, away, returned, now);
            boolean flagged = stolen || away > 0;
            if (v == Verdict.STOLEN) assertTrue(player && !flagged && !found && d > TheftRule.FAR);
            if (v == Verdict.RETURNED) assertTrue(player && flagged && !(thief && stolen) && d <= TheftRule.NEAR && TheftRule.cooled(returned, now));
            if (v == Verdict.DRIFT) assertTrue(!player && !flagged && loose && d > TheftRule.NEAR && d <= TheftRule.FAR);
            if (v == Verdict.HOME) assertTrue(flagged && d <= TheftRule.NEAR);
            if (v == Verdict.LOST) assertTrue(away == 0 && d > TheftRule.FAR);
            if (flagged && d <= TheftRule.NEAR) assertTrue(v == Verdict.HOME || v == Verdict.RETURNED, "a flagged horse at home always clears");
        }
    }

    // -- SpookRule -------------------------------------------------------------------------------------

    @Test void aChallengerFrightensEveryHorseByItsCalm() {
        for (boolean cared : new boolean[]{false, true}) {
            for (int calm : new int[]{0, 1}) {
                assertEquals(Reaction.THROW, SpookRule.react(calm, true, 10, true, cared), "calm " + calm + " throws its rider");
                assertEquals(Reaction.BOLT, SpookRule.react(calm, true, 10, false, cared), "calm " + calm + " bolts");
            }
            for (int calm : new int[]{2, 3}) for (boolean ridden : new boolean[]{false, true})
                assertEquals(Reaction.REAR, SpookRule.react(calm, true, 10, ridden, cared), "calm " + calm + " rears");
            for (int calm : new int[]{4, 5}) for (boolean ridden : new boolean[]{false, true})
                assertEquals(Reaction.NONE, SpookRule.react(calm, true, 3, ridden, cared), "calm " + calm + " stands its ground");
        }
    }

    @Test void aChallengerReachesSixteenBlocks() {
        assertEquals(Reaction.BOLT, SpookRule.react(0, true, 16, false, false));
        assertEquals(Reaction.NONE, SpookRule.react(0, true, 16.01, false, false));
        assertEquals(Reaction.NONE, SpookRule.react(0, true, 40, true, true));
    }

    @Test void ordinaryMonstersOnlyBotherACaredForHorseWithNoBondYet() {
        assertEquals(Reaction.BOLT, SpookRule.react(0, false, 3, false, true));
        assertEquals(Reaction.REAR, SpookRule.react(0, false, 4, true, true), "under a rider it rears, never throws");
        assertEquals(Reaction.NONE, SpookRule.react(0, false, 4.01, false, true), "four blocks is the reach");
        for (int calm = 1; calm <= 5; calm++) for (boolean ridden : new boolean[]{false, true})
            assertEquals(Reaction.NONE, SpookRule.react(calm, false, 1, ridden, true), "a little bond (or a bridle) is enough: calm " + calm);
        assertEquals(Reaction.NONE, SpookRule.react(BondMath.calm(0, 1), false, 1, true, true), "a Bridle steadies a fresh horse");
    }

    @Test void ordinaryMonstersNeverSpookAnUncaredHorse() {
        var r = new Random(7);
        for (int i = 0; i < 10_000; i++) {
            int calm = r.nextInt(6); double d = r.nextDouble() * 20;
            assertEquals(Reaction.NONE, SpookRule.react(calm, false, d, r.nextBoolean(), false), "wild and village horses keep vanilla behaviour");
        }
    }

    @Test void aSteadyHorseStandsItsGroundAgainstAChallenger() {
        assertTrue(SpookRule.standsGround(BondMath.calm(4, 0), true, 10), "a Devoted horse");
        assertTrue(SpookRule.standsGround(BondMath.calm(3, 1), true, 16), "a Loyal horse under a Bridle");
        assertFalse(SpookRule.standsGround(BondMath.calm(3, 0), true, 10), "a Loyal horse without one still rears");
        assertFalse(SpookRule.standsGround(5, true, 16.5), "out of reach there is nothing to face");
        assertFalse(SpookRule.standsGround(5, false, 2), "ordinary monsters get no challenge neigh");
        for (int calm = 0; calm < 8; calm++)
            assertEquals(SpookRule.standsGround(calm, true, 8), SpookRule.react(calm, true, 8, true, true) == Reaction.NONE, "standing firm is exactly not reacting: calm " + calm);
    }

    @Test void theStrongerReactionWinsAndThereIsACooldown() {
        assertEquals(Reaction.THROW, SpookRule.stronger(Reaction.REAR, Reaction.THROW));
        assertEquals(Reaction.BOLT, SpookRule.stronger(Reaction.BOLT, Reaction.REAR));
        assertEquals(Reaction.NONE, SpookRule.stronger(Reaction.NONE, Reaction.NONE));
        assertTrue(SpookRule.ready(-1, 0), "never spooked");
        assertFalse(SpookRule.ready(100, 100 + SpookRule.COOLDOWN - 1));
        assertTrue(SpookRule.ready(100, 100 + SpookRule.COOLDOWN));
        assertEquals(200, SpookRule.COOLDOWN, "ten seconds between frights");
    }
}
