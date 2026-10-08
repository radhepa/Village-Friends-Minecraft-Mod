package dev.villagefriends.pet;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

/**
 * Who a resident's cat or dog is: their name, which resident they belong to ({@code owner} is the
 * resident's profile id, which survives a zombie conversion and cure), their personality, favorite
 * game and treat, the game day they were born and adopted, and how fond they are of each player.
 * {@code former} names the resident who once kept a pet that has since lost them.
 */
public record PetProfile(String owner, String ownerName, String name, String species, String personality,
        String game, String treat, long born, long adopted, String former, Map<String, Fondness> fondness) {

    /** How fond a pet is of one player (0 to 100), and the game days that player last patted them and gave a treat. */
    public record Fondness(int points, long patDay, long treatDay) {
        public static final Fondness NONE = new Fondness(0, -1, -1);
        public static final Codec<Fondness> CODEC = RecordCodecBuilder.create(i -> i.group(
                Codec.INT.optionalFieldOf("points", 0).forGetter(Fondness::points),
                Codec.LONG.optionalFieldOf("pat_day", -1L).forGetter(Fondness::patDay),
                Codec.LONG.optionalFieldOf("treat_day", -1L).forGetter(Fondness::treatDay)
        ).apply(i, Fondness::new));
        public Fondness add(int amount) { return new Fondness(Math.clamp(points + amount, 0, PetKeeping.MAX_FONDNESS), patDay, treatDay); }
        public Fondness patted(long day) { return new Fondness(points, day, treatDay); }
        public Fondness treated(long day) { return new Fondness(points, patDay, day); }
    }

    public static final Codec<PetProfile> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.STRING.optionalFieldOf("owner", "").forGetter(PetProfile::owner),
            Codec.STRING.optionalFieldOf("owner_name", "").forGetter(PetProfile::ownerName),
            Codec.STRING.fieldOf("name").forGetter(PetProfile::name),
            Codec.STRING.fieldOf("species").forGetter(PetProfile::species),
            Codec.STRING.optionalFieldOf("personality", "playful").forGetter(PetProfile::personality),
            Codec.STRING.optionalFieldOf("game", "").forGetter(PetProfile::game),
            Codec.STRING.optionalFieldOf("treat", "").forGetter(PetProfile::treat),
            Codec.LONG.optionalFieldOf("born", 0L).forGetter(PetProfile::born),
            Codec.LONG.optionalFieldOf("adopted", 0L).forGetter(PetProfile::adopted),
            Codec.STRING.optionalFieldOf("former", "").forGetter(PetProfile::former),
            Codec.unboundedMap(Codec.STRING, Fondness.CODEC).optionalFieldOf("fondness", Map.of()).forGetter(PetProfile::fondness)
    ).apply(i, PetProfile::new));

    public boolean cat() { return species.equals(PetKeeping.CAT); }
    public boolean owned() { return !owner.isEmpty(); }
    public Fondness fondness(UUID player) { return fondness.getOrDefault(player.toString(), Fondness.NONE); }
    public PetProfile fondness(UUID player, Fondness next) {
        var map = new HashMap<>(fondness); map.put(player.toString(), next);
        return new PetProfile(owner, ownerName, name, species, personality, game, treat, born, adopted, former, Map.copyOf(map));
    }
    public PetProfile ownerName(String next) {
        return next.equals(ownerName) ? this : new PetProfile(owner, next, name, species, personality, game, treat, born, adopted, former, fondness);
    }
    public PetProfile renamed(String next) {
        return next.equals(name) ? this : new PetProfile(owner, ownerName, next, species, personality, game, treat, born, adopted, former, fondness);
    }
    /** Their resident is gone for good: they remember them, and anyone may give them a new home. */
    public PetProfile released() { return new PetProfile("", "", name, species, personality, game, treat, born, adopted, ownerName, fondness); }
    public PetProfile adoptedBy(String residentId, String residentName, long day) {
        return new PetProfile(residentId, residentName, name, species, personality, game, treat, born, day, former, fondness);
    }
}
