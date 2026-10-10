package dev.villagefriends.stable;

import static org.junit.jupiter.api.Assertions.*;

import dev.villagefriends.stable.bond.BondMath;
import dev.villagefriends.stable.bond.BondMath.Source;
import dev.villagefriends.stable.data.HorseBond;
import java.util.Random;
import org.junit.jupiter.api.Test;

/** The bond's gain rules, daily caps, tiers, bonuses and words. */
class StableBondTest {
    private static final String ME = "00000000-0000-0000-0000-000000000001", YOU = "00000000-0000-0000-0000-000000000002";
    private static final double BRIDLE = 1.5;

    private static HorseBond groom(HorseBond b, long day, double m) { return BondMath.gain(b, ME, Source.GROOM, day, m); }
    private static HorseBond feed(HorseBond b, long day, double m) { return BondMath.gain(b, ME, Source.FEED, day, m); }
    private static HorseBond ride(HorseBond b, long day, double m, double blocks) { return BondMath.gain(b, ME, Source.RIDE_BLOCKS, day, m, blocks); }

    /** A day of full care: three grooms, six carrots and {@code blocks} ridden in one-second samples of 10 blocks. */
    private static HorseBond fullDay(HorseBond b, long day, double rideMultiplier, double blocks) {
        for (int i = 0; i < 3; i++) b = groom(b, day, 1);
        for (int i = 0; i < 6; i++) b = feed(b, day, 1);
        for (double done = 0; done < blocks; done += 10) b = ride(b, day, rideMultiplier, 10);
        return b;
    }

    @Test void tiersStartAtTheirFloorsAndABridleAddsCalm() {
        for (int t = 0; t < BondMath.FLOORS.length; t++) {
            assertEquals(t, BondMath.tier(BondMath.FLOORS[t]));
            if (t > 0) assertEquals(t - 1, BondMath.tier(BondMath.FLOORS[t] - 1));
        }
        assertEquals(4, BondMath.tier(BondMath.MAX));
        assertEquals(2, BondMath.calm(2, 0));
        assertEquals(3, BondMath.calm(2, 1));
        assertEquals("Wary", BondMath.tierName(0));
        assertEquals("Devoted", BondMath.tierName(4));
        assertEquals("Devoted", BondMath.tierName(9), "out-of-range tiers clamp");
    }

    @Test void onlyThreeGroomsADayCount() {
        var b = HorseBond.NONE;
        int[] expected = {20, 22, 24, 24, 24};
        for (int want : expected) { b = groom(b, 1, 1); assertEquals(want, b.points()); }
        assertEquals(3, b.groomed());
    }

    @Test void feedingStopsAtThirtyPointsADayCountedAfterTheMultiplier() {
        var b = HorseBond.NONE;
        for (int i = 0; i < 6; i++) b = feed(b, 1, 1);
        assertEquals(30, b.points());
        assertEquals(30, feed(b, 1, 1).points(), "a seventh carrot adds nothing");
        var golden = BondMath.gain(HorseBond.NONE, ME, Source.FEED_GOLDEN, 1, 1);
        assertEquals(15, golden.points());
        golden = BondMath.gain(golden, ME, Source.FEED_GOLDEN, 1, 1);
        golden = BondMath.gain(golden, ME, Source.FEED_GOLDEN, 1, 1);
        assertEquals(30, golden.points(), "golden food fills the cap, never past it");
        // With a 1.5 multiplier (the Riding skill) a carrot is worth 8: the cap fills sooner but stays 30.
        var quick = HorseBond.NONE;
        int carrots = 0;
        while (quick.fed() < BondMath.FEED_CAP) { quick = feed(quick, 1, 1.5); carrots++; }
        assertEquals(30, quick.points());
        assertEquals(4, carrots);
    }

    @Test void ridingStopsAtSixtyPointsADayAndDropsTheRest() {
        var b = ride(HorseBond.NONE, 1, 1, 1200);
        assertEquals(60, b.points());
        assertEquals(0, b.carry(), 1e-9);
        var more = ride(b, 1, 1, 400);
        assertEquals(60, more.points(), "past the day's cap");
        assertEquals(0, more.carry(), 1e-9, "carry past the cap is not banked");
        var part = ride(HorseBond.NONE, 1, 1, 30);
        assertEquals(1, part.points());
        assertEquals(.5, part.carry(), 1e-9, "half a point waits for the next 10 blocks");
        assertEquals(2, ride(part, 1, 1, 10).points());
    }

    @Test void aNewDayResetsTheCountersButKeepsThePoints() {
        var b = fullDay(HorseBond.NONE, 1, 1, 1200);
        assertEquals(114, b.points());
        var next = groom(b, 2, 1);
        assertEquals(134, next.points(), "the first groom of a new day is worth 20 again");
        assertEquals(1, next.groomed());
        assertEquals(0, next.fed());
        assertEquals(0, next.rode());
        assertEquals(2, next.day());
    }

    @Test void aNewPartnerStartsTheBondFromZero() {
        var mine = fullDay(HorseBond.NONE, 1, 1, 1200);
        var yours = BondMath.gain(mine, YOU, Source.GROOM, 1, 1);
        assertEquals(YOU, yours.partner());
        assertEquals(20, yours.points());
        assertEquals(20, BondMath.gained(mine, yours), "a new partner's points count from 0");
        assertEquals(0, BondMath.tierBefore(mine, YOU));
        assertEquals(1, BondMath.tierBefore(mine, ME));
        var twice = groom(groom(HorseBond.NONE, 1, 1), 1, 1);
        assertEquals(2, BondMath.gained(twice, groom(twice, 1, 1)), "the same partner's gain is the difference");
    }

    @Test void theBridleOnlySpeedsUpRiding() {
        assertEquals(1, BondMath.multiplier(Source.GROOM, BRIDLE, 0), 1e-9);
        assertEquals(1, BondMath.multiplier(Source.FEED, BRIDLE, 0), 1e-9);
        assertEquals(BRIDLE, BondMath.multiplier(Source.RIDE_BLOCKS, BRIDLE, 0), 1e-9);
        assertEquals(1.2, BondMath.multiplier(Source.FEED_GOLDEN, BRIDLE, .2), 1e-9, "the Riding skill helps every source");
        assertEquals(1.8, BondMath.multiplier(Source.RIDE_BLOCKS, BRIDLE, .2), 1e-9);
        assertEquals(1, BondMath.multiplier(Source.API, BRIDLE, -3), 1e-9, "a negative bonus is ignored");
        assertEquals(24, fullDayGrooms(BondMath.multiplier(Source.GROOM, BRIDLE, 0)));
    }
    private static int fullDayGrooms(double m) {
        var b = HorseBond.NONE;
        for (int i = 0; i < 3; i++) b = groom(b, 1, m);
        return b.points();
    }

    @Test void pointsStopAtAThousand() {
        var b = BondMath.gain(HorseBond.NONE, ME, Source.API, 1, 1, 5000);
        assertEquals(BondMath.MAX, b.points());
        assertEquals(BondMath.MAX, groom(b, 1, 1).points());
        assertEquals(500, BondMath.gain(HorseBond.NONE, ME, Source.API, 1, 3, 500).points(), "api points are added as given");
        assertEquals(0, BondMath.gain(HorseBond.NONE, ME, Source.API, 1, 1, -40).points(), "never negative");
    }

    @Test void fullCareMakesAHorseLoyalOnDayFive() {
        var b = HorseBond.NONE;
        int[] after = new int[6];
        for (int day = 1; day <= 5; day++) {
            int before = b.points();
            b = fullDay(b, day, 1, 1300);
            assertEquals(114, b.points() - before, "a full day of care on day " + day);
            after[day] = b.points();
        }
        assertEquals(456, after[4]);
        assertEquals(2, BondMath.tier(after[4]), "still Trusting after day 4");
        assertEquals(570, after[5]);
        assertEquals(3, BondMath.tier(after[5]), "Loyal on day 5");
        assertTrue(BondMath.tier(after[5]) >= BondMath.WHISTLE_TIER, "the whistle reaches it now");
    }

    @Test void withABridleTheRideCapComesAfter800Blocks() {
        var b = HorseBond.NONE;
        int blocks = 0;
        while (b.rode() < BondMath.RIDE_CAP) { b = ride(b, 1, BRIDLE, 10); blocks += 10; }
        assertEquals(800, blocks);
        var plain = HorseBond.NONE;
        int plainBlocks = 0;
        while (plain.rode() < BondMath.RIDE_CAP) { plain = ride(plain, 1, 1, 10); plainBlocks += 10; }
        assertEquals(1200, plainBlocks);
        assertEquals(114, fullDay(HorseBond.NONE, 1, BRIDLE, 1300).points(), "a full day is still 114");
    }

    @Test void randomCareNeverBreaksTheDailyCaps() {
        var random = new Random(7);
        var b = HorseBond.NONE;
        for (int step = 0; step < 20_000; step++) {
            long day = step / 500;
            var before = b;
            b = switch (random.nextInt(4)) {
                case 0 -> groom(b, day, 1 + random.nextDouble());
                case 1 -> feed(b, day, 1 + random.nextDouble());
                case 2 -> BondMath.gain(b, ME, Source.FEED_GOLDEN, day, 1 + random.nextDouble());
                default -> ride(b, day, 1 + random.nextDouble(), random.nextDouble() * 15);
            };
            assertTrue(b.groomed() <= BondMath.GROOMS_A_DAY && b.fed() <= BondMath.FEED_CAP && b.rode() <= BondMath.RIDE_CAP, b.toString());
            assertTrue(b.points() >= (before.partner().equals(ME) ? before.points() : 0) && b.points() <= BondMath.MAX, b.toString());
        }
    }

    @Test void tierBonusesGrowEvenly() {
        assertEquals(0, BondMath.speedBonus(0));
        assertEquals(.06, BondMath.speedBonus(4), 1e-9);
        assertEquals(.05, BondMath.jumpBonus(4), 1e-9);
        assertEquals(4, BondMath.healthBonus(4), 1e-9);
        assertEquals(500, BondMath.nextFloor(312));
        assertEquals(1000, BondMath.nextFloor(850), "Devoted counts toward the maximum");
    }

    @Test void speedAndJumpAreDescribedInPlainNumbers() {
        assertEquals(11.2, BondMath.blocksPerSecond(.2657), .01);
        assertEquals(3.25, BondMath.jumpHeight(.75), .01);
        assertEquals(5.29, BondMath.jumpHeight(1.0), .01, "vanilla's best jump clears about five blocks");
        assertEquals("Bucephalus, Destrier. Bond: Trusting (312/500). 11.2 blocks/s, jumps 3.3, 32 health.",
                BondMath.describe("Bucephalus", "Destrier", 312, .2657, .75, 32.2));
        assertEquals("Fjord Horse. Bond: Devoted (850/1000). 8.4 blocks/s, jumps 1.9, 27 health.",
                BondMath.describe(null, "Fjord Horse", 850, .2, .55, 26.6));
        assertEquals("Your fjord horse trusts you more: Loyal.", BondMath.trustLine(null, "Fjord Horse", 3));
        assertEquals("Bucephalus trusts you more: Devoted.", BondMath.trustLine("Bucephalus", "Destrier", 4));
        assertEquals("Your whistle will reach your mule now.", BondMath.whistleLine("", "Mule"));
        assertEquals("groom", Source.GROOM.label());
        assertEquals("feed", Source.FEED_GOLDEN.label());
        assertEquals("ride", Source.RIDE_BLOCKS.label());
    }
}
