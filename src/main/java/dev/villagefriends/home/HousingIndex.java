package dev.villagefriends.home;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import net.minecraft.core.BlockPos;

/**
 * Everything one village knows about its houses: the houses, whose bed is whose, who has no bed of their
 * own, which households need a bigger house, and the beds left empty by residents who passed away or left
 * (kept for a later memorial or mourning feature).
 *
 * @param beds resident id to their bed
 * @param homeless residents with no bed of their own, by id
 * @param needs a household's first member to what it needs ({@link Need})
 * @param vacated the last {@link #MAX_VACATED} beds that were freed, oldest first
 * @param moved resident id to the day they moved into the house they live in now
 * @param cursed resident id to the day they were found turned into a zombie villager (their bed waits a week)
 * @param stamp a fingerprint of the village's society when beds were last assigned
 * @param surveyed whether the village's own buildings have been read from its structure (or found around its beds)
 */
public record HousingIndex(String village, List<House> houses, Map<String, BedKey> beds, List<String> homeless, Map<String, Need> needs,
        List<Vacancy> vacated, Map<String, Long> moved, Map<String, Long> cursed, long stamp, boolean surveyed) {
    public static final int MAX_VACATED = 32;
    public static final String HOMELESS = "homeless", CROWDED = "crowded", NEWBORN = "newborn";

    /** A resident's bed: the house and the bed's head. */
    public record BedKey(String house, BlockPos head) {
        public static final Codec<BedKey> CODEC = RecordCodecBuilder.create(i -> i.group(
                Codec.STRING.fieldOf("house").forGetter(BedKey::house),
                BlockPos.CODEC.fieldOf("head").forGetter(BedKey::head)
        ).apply(i, BedKey::new));
    }
    /** A bed someone left empty, and why: "passed", "moved" or "cursed". */
    public record Vacancy(String resident, String name, String house, BlockPos bed, long day, String why) {
        public static final Codec<Vacancy> CODEC = RecordCodecBuilder.create(i -> i.group(
                Codec.STRING.fieldOf("resident").forGetter(Vacancy::resident),
                Codec.STRING.optionalFieldOf("name", "").forGetter(Vacancy::name),
                Codec.STRING.fieldOf("house").forGetter(Vacancy::house),
                BlockPos.CODEC.fieldOf("bed").forGetter(Vacancy::bed),
                Codec.LONG.optionalFieldOf("day", 0L).forGetter(Vacancy::day),
                Codec.STRING.optionalFieldOf("why", "passed").forGetter(Vacancy::why)
        ).apply(i, Vacancy::new));
    }
    /**
     * A household without room enough: {@code kind} is {@link #HOMELESS} (no beds at all), {@link #CROWDED} (split
     * between houses, or lodging in guest rooms or barracks that aren't theirs) or {@link #NEWBORN} (a baby born in
     * the village with no bed yet). {@code members} are the whole household; {@code beds} how many of them have one.
     */
    public record Need(String kind, List<String> members, int beds) {
        public static final Codec<Need> CODEC = RecordCodecBuilder.create(i -> i.group(
                Codec.STRING.fieldOf("kind").forGetter(Need::kind),
                Codec.STRING.listOf().optionalFieldOf("members", List.of()).forGetter(Need::members),
                Codec.INT.optionalFieldOf("beds", 0).forGetter(Need::beds)
        ).apply(i, Need::new));
        public Need { members = List.copyOf(members); }
    }

    public static final Codec<HousingIndex> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.STRING.fieldOf("village").forGetter(HousingIndex::village),
            House.CODEC.listOf().optionalFieldOf("houses", List.of()).forGetter(HousingIndex::houses),
            Codec.unboundedMap(Codec.STRING, BedKey.CODEC).optionalFieldOf("beds", Map.of()).forGetter(HousingIndex::beds),
            Codec.STRING.listOf().optionalFieldOf("homeless", List.of()).forGetter(HousingIndex::homeless),
            Codec.unboundedMap(Codec.STRING, Need.CODEC).optionalFieldOf("needs", Map.of()).forGetter(HousingIndex::needs),
            Vacancy.CODEC.listOf().optionalFieldOf("vacated", List.of()).forGetter(HousingIndex::vacated),
            Codec.unboundedMap(Codec.STRING, Codec.LONG).optionalFieldOf("moved", Map.of()).forGetter(HousingIndex::moved),
            Codec.unboundedMap(Codec.STRING, Codec.LONG).optionalFieldOf("cursed", Map.of()).forGetter(HousingIndex::cursed),
            Codec.LONG.optionalFieldOf("stamp", 0L).forGetter(HousingIndex::stamp),
            Codec.BOOL.optionalFieldOf("surveyed", false).forGetter(HousingIndex::surveyed)
    ).apply(i, HousingIndex::new));

    public HousingIndex {
        houses = List.copyOf(houses); beds = Map.copyOf(beds); homeless = List.copyOf(homeless); needs = Map.copyOf(needs);
        vacated = List.copyOf(vacated.subList(Math.max(0, vacated.size() - MAX_VACATED), vacated.size()));
        moved = Map.copyOf(moved); cursed = Map.copyOf(cursed);
    }
    public static HousingIndex empty(String village) { return new HousingIndex(village, List.of(), Map.of(), List.of(), Map.of(), List.of(), Map.of(), Map.of(), 0, false); }

    // -- reading -----------------------------------------------------------------------------------

    public House house(String id) {
        for (var h : houses) if (h.id().equals(id)) return h;
        return null;
    }
    /** The house a resident sleeps in, or null. */
    public House houseOf(String resident) {
        var key = beds.get(resident);
        return key == null ? null : house(key.house());
    }
    /** A resident's bed, if they have one. */
    public Optional<House.Bed> bedOf(String resident) {
        var key = beds.get(resident); var h = key == null ? null : house(key.house());
        return h == null ? Optional.empty() : Optional.ofNullable(h.bed(key.head()));
    }
    /** Who sleeps in a house, in bed order. */
    public List<String> residents(String house) {
        var h = house(house); if (h == null) return List.of();
        var out = new ArrayList<String>();
        for (var b : h.beds()) for (var e : beds.entrySet()) if (e.getValue().house().equals(house) && e.getValue().head().equals(b.head())) out.add(e.getKey());
        return out;
    }
    /** The resident whose bed has its head at {@code head}, or null. */
    public String owner(BlockPos head) {
        for (var e : beds.entrySet()) if (e.getValue().head().equals(head)) return e.getKey();
        return null;
    }
    /** The need of the household a resident belongs to, or null. */
    public Need needOf(String resident) {
        for (var n : needs.values()) if (n.members().contains(resident)) return n;
        return null;
    }

    // -- changes -----------------------------------------------------------------------------------

    public HousingIndex withHouses(List<House> next) { return new HousingIndex(village, next, beds, homeless, needs, vacated, moved, cursed, stamp, surveyed); }
    public HousingIndex withHouse(House house) {
        var next = new ArrayList<House>(); boolean found = false;
        for (var h : houses) { if (h.id().equals(house.id())) { next.add(house); found = true; } else next.add(h); }
        if (!found) next.add(house);
        return withHouses(next);
    }
    public HousingIndex surveyed(List<House> found) {
        var next = new ArrayList<>(houses);
        for (var h : found) if (house(h.id()) == null) next.add(h);
        return new HousingIndex(village, next, beds, homeless, needs, vacated, moved, cursed, stamp, true);
    }
    public HousingIndex withoutHouse(String id) {
        var next = new ArrayList<House>();
        for (var h : houses) if (!h.id().equals(id)) next.add(h);
        var nextBeds = new HashMap<>(beds); nextBeds.values().removeIf(k -> k.house().equals(id));
        return new HousingIndex(village, next, nextBeds, homeless, needs, vacated, moved, cursed, stamp, surveyed);
    }
    /** A resident leaves their bed for good ("moved" to another village, say): it is freed and remembered. */
    public HousingIndex vacate(String resident, String name, long day, String why) {
        var key = beds.get(resident); if (key == null) return this;
        var nextBeds = new HashMap<>(beds); nextBeds.remove(resident);
        var nextVacated = new ArrayList<>(vacated); nextVacated.add(new Vacancy(resident, name, key.house(), key.head(), day, why));
        var nextMoved = new HashMap<>(moved); nextMoved.remove(resident);
        return new HousingIndex(village, houses, nextBeds, homeless, needs, nextVacated, nextMoved, cursed, stamp, surveyed);
    }
}
