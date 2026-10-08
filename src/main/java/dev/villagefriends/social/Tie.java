package dev.villagefriends.social;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;

/** What two residents have actually lived through together: days spent side by side and their last quarrel. */
public record Tie(int together, long lastTogether, long quarrel) {
    public static final int MAX_TOGETHER = 40;
    public static final Tie NONE = new Tie(0, -1, -1);
    public static final Codec<Tie> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.INT.optionalFieldOf("together", 0).forGetter(Tie::together),
            Codec.LONG.optionalFieldOf("last_together", -1L).forGetter(Tie::lastTogether),
            Codec.LONG.optionalFieldOf("quarrel", -1L).forGetter(Tie::quarrel)
    ).apply(i, Tie::new));
    public Tie { together = Math.clamp(together, 0, MAX_TOGETHER); }

    /** Counts at most one shared day, however long they stood together. */
    public Tie together(long day) { return lastTogether == day ? this : new Tie(together + 1, day, quarrel); }
    public Tie quarrel(long day) { return new Tie(together, lastTogether, day); }
    /** A quarrel forgiven: it stops counting against them. */
    public Tie reconciled() { return quarrel < 0 ? this : new Tie(together, lastTogether, -1); }
}
