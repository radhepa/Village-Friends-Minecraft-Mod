package dev.villagefriends;
import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import java.util.UUID;
public record ResidentProfile(String id, String personality, String hobby, String value,
        String love, String dislike, String story, String look) {
    public static final Codec<ResidentProfile> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.STRING.fieldOf("id").forGetter(ResidentProfile::id),
            Codec.STRING.fieldOf("personality").forGetter(ResidentProfile::personality),
            Codec.STRING.fieldOf("hobby").forGetter(ResidentProfile::hobby),
            Codec.STRING.fieldOf("value").forGetter(ResidentProfile::value),
            Codec.STRING.fieldOf("love").forGetter(ResidentProfile::love),
            Codec.STRING.fieldOf("dislike").forGetter(ResidentProfile::dislike),
            Codec.STRING.fieldOf("story").forGetter(ResidentProfile::story),
            Codec.STRING.fieldOf("look").forGetter(ResidentProfile::look)
    ).apply(i, ResidentProfile::new));
    public static ResidentProfile generate(UUID id, String look) {
        var content = NarrativeContent.current();
        var archetype = content.personalities().get(pick(id, 31, content.personalities().size()));
        var arc = content.stories().get(pick(id, 67, content.stories().size()));
        return new ResidentProfile(id.toString(), archetype.id(), archetype.hobby(), archetype.value(),
                archetype.loves().get(pick(id, 97, archetype.loves().size())),
                archetype.dislikes().get(pick(id, 131, archetype.dislikes().size())), arc.id(),
                dev.villagefriends.outfit.ResidentLook.parse(look) == null ? ResidentAppearance.generate(id) : look);
    }
    private static int pick(UUID id, int salt, int bound) {
        long bits = id.getMostSignificantBits() ^ Long.rotateLeft(id.getLeastSignificantBits(), salt & 63) ^ salt;
        return Math.floorMod(Long.hashCode(bits), bound);
    }
}
