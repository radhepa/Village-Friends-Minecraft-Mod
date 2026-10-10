package dev.villagefriends.stable.data;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;

/**
 * The bond between a horse and its one partner (its owner, as a UUID string). {@code points} grow from 0 to
 * {@code BondMath.MAX}. The daily counters ({@code groomed} grooms, {@code fed} and {@code rode} points gained)
 * belong to game day {@code day} and reset when the day changes; {@code carry} holds the fraction of a riding
 * point not yet earned. Saved only (nothing on the client reads it).
 */
public record HorseBond(String partner, int points, long day, int groomed, int fed, int rode, double carry) {
    public static final HorseBond NONE = new HorseBond("", 0, -1, 0, 0, 0, 0);
    public static final Codec<HorseBond> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.STRING.optionalFieldOf("partner", NONE.partner).forGetter(HorseBond::partner),
            Codec.INT.optionalFieldOf("points", NONE.points).forGetter(HorseBond::points),
            Codec.LONG.optionalFieldOf("day", NONE.day).forGetter(HorseBond::day),
            Codec.INT.optionalFieldOf("groomed", NONE.groomed).forGetter(HorseBond::groomed),
            Codec.INT.optionalFieldOf("fed", NONE.fed).forGetter(HorseBond::fed),
            Codec.INT.optionalFieldOf("rode", NONE.rode).forGetter(HorseBond::rode),
            Codec.DOUBLE.optionalFieldOf("carry", NONE.carry).forGetter(HorseBond::carry)
    ).apply(i, HorseBond::new));
}
