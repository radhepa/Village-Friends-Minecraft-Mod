package dev.villagefriends.stable.data;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;

/**
 * A horse's breed (an id from {@code breeds.json}) and which of its painted coats it wears. Saved, and synced
 * to every client, because the coat is swapped by a client render hook that reads it.
 */
public record HorseBreed(String breed, int coat) {
    public static final Codec<HorseBreed> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.STRING.fieldOf("breed").forGetter(HorseBreed::breed),
            Codec.INT.optionalFieldOf("coat", 0).forGetter(HorseBreed::coat)
    ).apply(i, HorseBreed::new));
    public static final StreamCodec<ByteBuf, HorseBreed> STREAM_CODEC = StreamCodec.composite(
            ByteBufCodecs.STRING_UTF8, HorseBreed::breed, ByteBufCodecs.VAR_INT, HorseBreed::coat, HorseBreed::new);
}
