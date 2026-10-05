package dev.villagefriends;
import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
public record ResidentHome(String village, String baseName, String dimension) {
    public static final Codec<ResidentHome> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.STRING.fieldOf("village").forGetter(ResidentHome::village), Codec.STRING.fieldOf("base_name").forGetter(ResidentHome::baseName),
            Codec.STRING.optionalFieldOf("dimension","minecraft:overworld").forGetter(ResidentHome::dimension)
    ).apply(i,ResidentHome::new));
    public ResidentHome(String village,String baseName) { this(village,baseName,"minecraft:overworld"); }
}
