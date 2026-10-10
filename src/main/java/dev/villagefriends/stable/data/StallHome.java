package dev.villagefriends.stable.data;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.minecraft.core.BlockPos;

/**
 * Where a horse is stabled and whose it is. {@code keeper}: a resident id, {@code "village"} (a communal stable
 * horse) or {@code "player:<uuid>"}. {@code stolenBy}: the uuid of the player who rode or led it away, or "".
 * {@code takenBy}: the uuid of the last player who rode or led it away from its stall since it was last home, or ""
 * (saved, so logging out on the horse or leaving it out for a while never makes that player a stranger to it).
 * {@code awaySince}: game time it was last seen left alone far from its stall, 0 while home. {@code returnedAt}:
 * game time of its last Returned a Horse deed, 0 = never (one good deed per horse per day, so walking the same
 * horse out and back is not a way to farm standing).
 */
public record StallHome(BlockPos stall, String dimension, String village, String keeper, String stolenBy, String takenBy, long awaySince, long returnedAt) {
    public static final Codec<StallHome> CODEC = RecordCodecBuilder.create(i -> i.group(
            BlockPos.CODEC.fieldOf("stall").forGetter(StallHome::stall),
            Codec.STRING.fieldOf("dimension").forGetter(StallHome::dimension),
            Codec.STRING.optionalFieldOf("village", "").forGetter(StallHome::village),
            Codec.STRING.fieldOf("keeper").forGetter(StallHome::keeper),
            Codec.STRING.optionalFieldOf("stolen_by", "").forGetter(StallHome::stolenBy),
            Codec.STRING.optionalFieldOf("taken_by", "").forGetter(StallHome::takenBy),
            Codec.LONG.optionalFieldOf("away_since", 0L).forGetter(StallHome::awaySince),
            Codec.LONG.optionalFieldOf("returned_at", 0L).forGetter(StallHome::returnedAt)
    ).apply(i, StallHome::new));

    /** A resident's or the village's horse: taking it away is theft. */
    public boolean residentOwned() { return !keeper.startsWith("player:"); }
    /** A horse a player stabled here (bought with papers, or their own). */
    public boolean playerKept() { return keeper.startsWith("player:"); }
    /** Stolen, or left far away and lost. */
    public boolean flagged() { return !stolenBy.isEmpty() || awaySince > 0; }
    public StallHome withStolenBy(String who) { return new StallHome(stall, dimension, village, keeper, who, takenBy, awaySince, returnedAt); }
    public StallHome withTakenBy(String who) { return new StallHome(stall, dimension, village, keeper, stolenBy, who, awaySince, returnedAt); }
    public StallHome withAwaySince(long t) { return new StallHome(stall, dimension, village, keeper, stolenBy, takenBy, t, returnedAt); }
    public StallHome withReturnedAt(long t) { return new StallHome(stall, dimension, village, keeper, stolenBy, takenBy, awaySince, t); }
    public StallHome withVillage(String v) { return new StallHome(stall, dimension, v, keeper, stolenBy, takenBy, awaySince, returnedAt); }
    /** Back home: no theft, not lost, nobody's to answer for. */
    public StallHome home() { return new StallHome(stall, dimension, village, keeper, "", "", 0, returnedAt); }
}
