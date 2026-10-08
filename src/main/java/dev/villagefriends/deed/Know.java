package dev.villagefriends.deed;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;

/**
 * How one resident knows about a deed: it happened to them ({@link #INVOLVED}), to their family
 * ({@link #FAMILY}), they saw it ({@link #SEEN}) or someone told them ({@link #HEARD}, {@code from} that
 * neighbor's id, or "" for village news). {@code day} is when they learned it, {@code told} whether they
 * have brought it up with the player yet, {@code kept} whether it went into their Journal for good.
 */
public record Know(int how, long day, String from, boolean told, boolean kept) {
    public static final int INVOLVED = 0, FAMILY = 1, SEEN = 2, HEARD = 3;
    public static final Codec<Know> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.INT.optionalFieldOf("how", HEARD).forGetter(Know::how),
            Codec.LONG.optionalFieldOf("day", 0L).forGetter(Know::day),
            Codec.STRING.optionalFieldOf("from", "").forGetter(Know::from),
            Codec.BOOL.optionalFieldOf("told", false).forGetter(Know::told),
            Codec.BOOL.optionalFieldOf("kept", false).forGetter(Know::kept)
    ).apply(i, Know::new));

    public Know {
        how = Math.clamp(how, INVOLVED, HEARD);
        from = from == null ? "" : from;
    }
    public static Know of(int how, long day, String from) { return new Know(how, day, from, false, false); }

    /** Saw it or lived it, as opposed to hearing about it: picks the "seen" dialogue. */
    public boolean firsthand() { return how == INVOLVED || how == SEEN; }
    /** How much this knowledge weighs in their prices: 1.0 involved, .8 family, .6 seen, .3 heard. */
    public double weight() { return switch (how) { case INVOLVED -> 1; case FAMILY -> .8; case SEEN -> .6; default -> .3; }; }
    public Know markTold() { return new Know(how, day, from, true, kept); }
    public Know markKept() { return new Know(how, day, from, told, true); }
    /** Knowing it more closely (seeing it after hearing it) replaces how they knew it, but never what they already said. */
    public Know closer(Know other) { return other.how < how ? new Know(other.how, other.day, other.from, told, kept) : this; }
}
