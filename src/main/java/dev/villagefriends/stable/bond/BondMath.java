package dev.villagefriends.stable.bond;

import dev.villagefriends.stable.data.HorseBond;
import java.util.Locale;

/**
 * The bond's numbers, pure (no world, no registries) so they can be unit tested. Five tiers by points:
 * 0 Wary 0-99, 1 Familiar 100-249, 2 Trusting 250-499, 3 Loyal 500-799, 4 Devoted 800-1000.
 *
 * <p>The foundation's part ({@link #FLOORS}, {@link #MAX}, {@link #WHISTLE_TIER}, {@link #tier} and
 * {@link #calm}) is frozen: the riders package's spook rule calls {@link #calm}. The breeds package adds the
 * gain rules, tier bonuses and text helpers around them.
 *
 * <p>Daily care is capped so a bond takes days, not one long brushing session: three grooms (20 points for the
 * first, 2 for the next two), 30 points of feeding and 60 points of riding (a point per 20 blocks) a day. The caps
 * count points <i>after</i> the multiplier, so a bridle or the Riding skill fills a day's cap sooner but never raises
 * it. Full care without bonuses is 24 + 30 + 60 = 114 points a day, so a horse becomes Loyal on day 5.
 */
public final class BondMath {
    /** The lowest points of each tier. */
    public static final int[] FLOORS = {0, 100, 250, 500, 800};
    public static final int MAX = 1000;
    /** From Loyal up, the Horse Whistle calls the horse. */
    public static final int WHISTLE_TIER = 3;

    /** The tier (0-4) for a number of points. */
    public static int tier(int points) {
        int tier = 0;
        for (int i = 0; i < FLOORS.length; i++) if (points >= FLOORS[i]) tier = i;
        return tier;
    }

    /** How steady a horse is near monsters: its bond tier plus its tack's calm (a Bridle adds 1). */
    public static int calm(int tier, int bridleCalm) { return tier + bridleCalm; }

    // -- gains (breeds package) ---------------------------------------------------------------------------

    /** What earned the points. {@link #label} is the source name {@code StablehandEvents.BOND_GAINED} reports. */
    public enum Source {
        GROOM, FEED, FEED_GOLDEN, RIDE_BLOCKS, API;
        public String label() {
            return switch (this) { case GROOM -> "groom"; case FEED, FEED_GOLDEN -> "feed"; case RIDE_BLOCKS -> "ride"; case API -> "api"; };
        }
    }
    public static final String[] TIERS = {"Wary", "Familiar", "Trusting", "Loyal", "Devoted"};
    public static final int GROOM_FIRST = 20, GROOM_AGAIN = 2, GROOMS_A_DAY = 3;
    public static final int FEED = 5, FEED_GOLDEN = 15, FEED_CAP = 30;
    public static final int RIDE_CAP = 60;
    public static final double BLOCKS_PER_POINT = 20;
    /** Tier bonuses, per tier: speed and jump as a fraction of the base value, health in hit points. */
    public static final double SPEED_PER_TIER = 0.015, JUMP_PER_TIER = 0.0125, HEALTH_PER_TIER = 1;

    /** {@link #gain(HorseBond, String, Source, long, double, double)} for a groom or a feed (no amount). */
    public static HorseBond gain(HorseBond b, String partner, Source source, long day, double multiplier) {
        return gain(b, partner, source, day, multiplier, 0);
    }

    /**
     * The bond after one gain. {@code amount} is the blocks ridden for {@link Source#RIDE_BLOCKS} and the points for
     * {@link Source#API} (added as given, capped only at {@link #MAX}); grooms and feeds ignore it. A new game day
     * resets the day's counters; a different partner starts the bond again from 0 (the horse changed owner).
     */
    public static HorseBond gain(HorseBond b, String partner, Source source, long day, double multiplier, double amount) {
        if (!b.partner().equals(partner)) b = new HorseBond(partner, 0, day, 0, 0, 0, 0);
        else if (b.day() != day) b = new HorseBond(partner, b.points(), day, 0, 0, 0, b.carry());
        int groomed = b.groomed(), fed = b.fed(), rode = b.rode(), gain = 0;
        double carry = b.carry(), m = Math.max(0, multiplier);
        switch (source) {
            case GROOM -> {
                if (groomed >= GROOMS_A_DAY) return b;
                gain = (int) Math.round((groomed == 0 ? GROOM_FIRST : GROOM_AGAIN) * m);
                groomed++;
            }
            case FEED, FEED_GOLDEN -> {
                gain = Math.max(0, Math.min((int) Math.round((source == Source.FEED ? FEED : FEED_GOLDEN) * m), FEED_CAP - fed));
                fed += gain;
            }
            case RIDE_BLOCKS -> {
                carry += Math.max(0, amount) / BLOCKS_PER_POINT * m;
                int whole = (int) Math.floor(carry);
                carry -= whole;
                gain = Math.max(0, Math.min(whole, RIDE_CAP - rode));
                if (gain < whole) carry = 0; // past the day's cap: the rest is not banked
                rode += gain;
            }
            case API -> gain = (int) Math.max(0, Math.round(amount));
        }
        return new HorseBond(partner, Math.min(MAX, b.points() + gain), day, groomed, fed, rode, carry);
    }

    /** The points a gain added (a new partner's bond counts from 0). */
    public static int gained(HorseBond before, HorseBond after) {
        return after.partner().equals(before.partner()) ? after.points() - before.points() : after.points();
    }

    /** The tier the bond with {@code partner} had before a gain (0 when the horse was bonded to someone else). */
    public static int tierBefore(HorseBond before, String partner) { return before.partner().equals(partner) ? tier(before.points()) : 0; }

    /** The gain multiplier: the tack's {@code bond_ride} for riding only, times 1 + the Riding skill's bond bonus for every source. */
    public static double multiplier(Source source, double bondRide, double ridingBonus) {
        return (source == Source.RIDE_BLOCKS ? Math.max(0, bondRide) : 1) * (1 + Math.max(0, ridingBonus));
    }

    public static double speedBonus(int tier) { return SPEED_PER_TIER * tier; }
    public static double jumpBonus(int tier) { return JUMP_PER_TIER * tier; }
    public static double healthBonus(int tier) { return HEALTH_PER_TIER * tier; }

    // -- words ---------------------------------------------------------------------------------------------

    public static String tierName(int tier) { return TIERS[Math.clamp(tier, 0, TIERS.length - 1)]; }

    /** The points that reach the next tier ({@link #MAX} once Devoted). */
    public static int nextFloor(int points) {
        int t = tier(points);
        return t + 1 < FLOORS.length ? FLOORS[t + 1] : MAX;
    }

    /** A horse's speed attribute in blocks per second (vanilla moves a ridden horse about 42.16 blocks a second per unit). */
    public static double blocksPerSecond(double speed) { return speed * 42.16; }

    /** How many blocks high a jump strength clears at full charge (the standard fit of vanilla's jump arc). */
    public static double jumpHeight(double j) { return -0.1817584952 * j * j * j + 3.689713992 * j * j + 2.128599134 * j - 0.343930367; }

    /** What to call a horse in a sentence: its own name, or "your destrier" ("Your destrier" to start one). */
    public static String call(String customName, String kind, boolean startOfSentence) {
        if (customName != null && !customName.isBlank()) return customName;
        return (startOfSentence ? "Your " : "your ") + kind.toLowerCase(Locale.ROOT);
    }

    /** The brush's line: "Bucephalus, Destrier. Bond: Trusting (312/500). 11.2 blocks/s, jumps 3.1, 32 health." */
    public static String describe(String customName, String kind, int points, double speed, double jump, double health) {
        String who = customName == null || customName.isBlank() ? kind : customName + ", " + kind;
        return String.format(Locale.ROOT, "%s. Bond: %s (%d/%d). %.1f blocks/s, jumps %.1f, %d health.", who, tierName(tier(points)),
                points, nextFloor(points), blocksPerSecond(speed), jumpHeight(jump), Math.round(health));
    }

    /** "Your destrier trusts you more: Loyal." */
    public static String trustLine(String customName, String kind, int tier) {
        return call(customName, kind, true) + " trusts you more: " + tierName(tier) + ".";
    }

    /** "Your whistle will reach your destrier now." */
    public static String whistleLine(String customName, String kind) { return "Your whistle will reach " + call(customName, kind, false) + " now."; }

    private BondMath() {}
}
