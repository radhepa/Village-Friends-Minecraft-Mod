package dev.villagefriends.stable.data;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;

/** The {@code villagefriends:horse_papers} component: the animal these papers are for (a breed id, "donkey" or "mule"). */
public record HorsePapers(String breed) {
    public static final Codec<HorsePapers> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.STRING.fieldOf("breed").forGetter(HorsePapers::breed)
    ).apply(i, HorsePapers::new));
    public static final StreamCodec<ByteBuf, HorsePapers> STREAM_CODEC = StreamCodec.composite(
            ByteBufCodecs.STRING_UTF8, HorsePapers::breed, HorsePapers::new);
}
