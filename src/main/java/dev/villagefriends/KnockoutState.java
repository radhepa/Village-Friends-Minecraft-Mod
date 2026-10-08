package dev.villagefriends;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;

/**
 * A knocked-out resident. Times are server game ticks, which only advance while the world is being
 * played, so the clock stops whenever nobody is in the world.
 * @param since when they were knocked out
 * @param until when they die of their injuries unless revived
 * @param bandages how many Bandage Wraps (from players or the village apothecary) bought them more time
 * @param tended whether the village apothecary has already dressed their wounds
 */
public record KnockoutState(long since, long until, int bandages, boolean tended) {
    public static final Codec<KnockoutState> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.LONG.optionalFieldOf("since", 0L).forGetter(KnockoutState::since),
            Codec.LONG.optionalFieldOf("until", 0L).forGetter(KnockoutState::until),
            Codec.INT.optionalFieldOf("bandages", 0).forGetter(KnockoutState::bandages),
            Codec.BOOL.optionalFieldOf("tended", false).forGetter(KnockoutState::tended)
    ).apply(i, KnockoutState::new));

    /** A full day of play: 24 real hours of ticks. */
    public static final long DAY = 24L * 60 * 60 * 20;
    /** What one Bandage Wrap adds. */
    public static final long BANDAGE = 12L * 60 * 60 * 20;
    /** Bandages can't stretch the clock past this much time left. */
    public static final long MOST_LEFT = 2 * DAY;

    public static KnockoutState knockedOut(long now) { return new KnockoutState(now, now + DAY, 0, false); }
    public long left(long now) { return Math.max(0, until - now); }
    /** One more bandage: twelve more hours, up to two days left. */
    public KnockoutState bandaged(long now, boolean byApothecary) {
        return new KnockoutState(since, Math.min(until + BANDAGE, now + MOST_LEFT), bandages + 1, tended || byApothecary);
    }
    public boolean canBandage(long now) { return left(now) + 20 * 60 < MOST_LEFT; }
    /** "23h 59m", "41m", "under a minute". */
    public static String duration(long ticks) {
        long minutes = ticks / 1200, hours = minutes / 60;
        if (hours > 0) return hours + "h " + (minutes % 60) + "m";
        return minutes > 0 ? minutes + "m" : "under a minute";
    }
}
