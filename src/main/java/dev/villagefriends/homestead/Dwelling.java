package dev.villagefriends.homestead;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import dev.villagefriends.outfit.Gender;
import dev.villagefriends.routine.Routine;
import dev.villagefriends.routine.Routine.Block;
import java.util.Collection;
import java.util.List;
import java.util.Locale;

/**
 * Who lives out in the wild, away from any village: the farmstead couple, the pariah cast out of their
 * village, the hill shepherd, the hedge-herbalist and the old soldier who keeps a watch nobody ordered.
 * Their homestead's template tags each of them with a role ({@code villagefriends.dweller.<role>}); this
 * class turns the role into a personality, a place name, a nameplate and a day without taverns, bells or
 * market squares. Pure and unit-tested; {@link Homesteads} applies it to the world.
 */
public final class Dwelling {
    public static final String TAG = "villagefriends.dweller.";
    public static final String GENDER_TAG = "villagefriends.gender.";
    /** How far a homestead resident strays from the middle of their homestead before heading back. */
    public static final int TETHER = 26;

    public enum Role {
        HOMESTEADER("steadfast", "warmhearted", List.of("Cloverbrook Farm", "Barleycombe Farm", "Larkspur Farm", "Hollin Croft", "Meadowsweet Farm",
                "Thistledown Farm", "Willowbrook Farm", "Sorrel Hill Farm", "Hazelcroft", "Rowan Lea Farm", "Applegarth Farm", "Honeyfield Farm",
                "Fallowmere Farm", "Brightwater Farm", "Oakhollow Farm", "Bramble End Farm", "Wheatley Croft", "Longacre Farm")),
        PARIAH("reserved", "reserved", List.of("Blackthorn House", "Greymoor House", "Crowhurst House", "Cinderwick House", "Ravenholt House",
                "Bittermere House", "Hollowgate House", "Thornfield House", "Dunmarrow House", "Coldharbour House", "Nightjar House",
                "Wormwood House", "Blackwater House", "Hemlock House", "Stillwater House", "Ironmoor House")),
        SHEPHERD("curious", "curious", List.of("Windy Fold", "Cloudtop Fold", "Fellside Fold", "Heatherhope Fold", "Cairn Fold", "Larkrise Fold",
                "Brackenrigg Fold", "High Tor Fold", "Mistcote", "Lambsknoll Fold", "Gorse Hill Fold", "Shepherd's Rest", "Stonecrop Fold",
                "Curlew Fold", "Ravensrigg Fold", "Skylark Fold")),
        HERBALIST("meticulous", "meticulous", List.of("Nettlebank Cottage", "Foxglove Cottage", "Yarrow Dell", "Mossmere Cottage", "Elderwood Cottage",
                "Tansy Hollow", "Rue Cottage", "Bramblewick", "Hagstone Cottage", "Willowherb Cottage", "Feverfew Cottage", "Mugwort Hollow",
                "Toadflax Cottage", "Old Sorrel's Cottage", "Henbane Hollow", "Lantern Moss Cottage")),
        VETERAN("protective", "protective", List.of("Greywatch Tower", "Stormguard Tower", "Old Hawk Tower", "Emberwatch Tower", "Ironspire",
                "Longward Tower", "Lantern Tower", "Highcairn Tower", "Coldwatch Tower", "Stonehelm Tower", "Harrow Tower", "Beacon Hill Tower",
                "Westerwatch", "Ashguard Tower", "Kestrel Tower", "Wolfsbane Tower"));

        final String man, woman; final List<String> places;
        Role(String man, String woman, List<String> places) { this.man = man; this.woman = woman; this.places = places; }
        public String id() { return name().toLowerCase(Locale.ROOT); }
        /** The personality that fits how they live (it also sets their hobby, values, likes and body language). */
        public String personality(Gender gender) { return gender == Gender.FEMALE ? woman : man; }
        public static Role byId(String id) {
            for (var r : values()) if (r.id().equals(id)) return r;
            return null;
        }
    }

    /**
     * What a homestead resident keeps about where they live: their role, their own name (without the
     * nameplate's "of ..."), the homestead's name and id, and its middle, which they don't stray far from.
     */
    public record Dweller(String role, String name, String place, String dwelling, int x, int y, int z) {
        public static final Codec<Dweller> CODEC = RecordCodecBuilder.create(i -> i.group(
                Codec.STRING.fieldOf("role").forGetter(Dweller::role), Codec.STRING.fieldOf("name").forGetter(Dweller::name),
                Codec.STRING.fieldOf("place").forGetter(Dweller::place), Codec.STRING.fieldOf("dwelling").forGetter(Dweller::dwelling),
                Codec.INT.fieldOf("x").forGetter(Dweller::x), Codec.INT.fieldOf("y").forGetter(Dweller::y), Codec.INT.fieldOf("z").forGetter(Dweller::z)
        ).apply(i, Dweller::new));
        public Role kind() { return Role.byId(role); }
        /** Squared horizontal distance from the middle of their homestead. */
        public long away(double px, double pz) { double dx = px - (x + .5), dz = pz - (z + .5); return (long) (dx * dx + dz * dz); }
    }

    /** The role an entity's tags give it, or null. */
    public static Role role(Collection<String> tags) {
        for (var tag : tags) if (tag.startsWith(TAG)) { var r = Role.byId(tag.substring(TAG.length())); if (r != null) return r; }
        return null;
    }
    /** The gender the template asks for ({@code villagefriends.gender.male|female}), or null to keep their own. */
    public static Gender gender(Collection<String> tags) {
        for (var tag : tags) if (tag.startsWith(GENDER_TAG)) return switch (tag.substring(GENDER_TAG.length())) {
            case "male" -> Gender.MALE; case "female" -> Gender.FEMALE; default -> null; };
        return null;
    }
    /** The homestead's name: the same for everyone who lives there, different from homestead to homestead. */
    public static String placeName(Role role, long seed) {
        long mixed = seed * 0x9E3779B97F4A7C15L; mixed ^= mixed >>> 31;
        return role.places.get((int) Math.floorMod(mixed, (long) role.places.size()));
    }
    /** A couple shares a complexion seed so their shared surname suits both (some name pools are complexion-bound). */
    public static int complexion(long seed) { long mixed = seed * 0xC2B2AE3D27D4EB4FL; mixed ^= mixed >>> 29; return (int) Math.floorMod(mixed, 6L); }
    /** The nameplate: "Edwin Hale of Cloverbrook Farm"; the pariah belongs nowhere, so "Corvin Vane, the Outcast". */
    public static String label(Role role, String name, String place) {
        return role == Role.PARIAH ? name + ", the Outcast" : name + " of " + place;
    }

    /**
     * Their day, out here: no tavern, no bell, no market square. Lunch and supper are eaten at home, the
     * evening spent by their own fire; the hours a villager would spend among neighbors go to the work of the
     * place (the farm, the flock) or their own pursuits. The veteran keeps the watch until midnight every night,
     * whatever the weather, and only guards keep night watches at all.
     */
    public static Block adjust(Role role, Block block, int time) {
        int t = Math.floorMod(time, 24000);
        if (role == Role.VETERAN && t >= Routine.at(20, 30) && t < Routine.at(23, 59)
                && (block == Block.EVENING || block == Block.SLEEP || block == Block.SUPPER || block == Block.SHELTER || block == Block.STORM
                || block == Block.TAVERN || block == Block.SUPPER_TAVERN || block == Block.SNOWED_IN)) return Block.NIGHT_WATCH;
        return switch (block) {
            case LUNCH, LUNCH_TAVERN -> Block.LUNCH_HOME;
            case SUPPER_TAVERN -> Block.SUPPER;
            case TAVERN, PERFORM -> Block.EVENING;
            case SOCIAL, MARKET, LESSONS, PARTY -> role == Role.HOMESTEADER || role == Role.SHEPHERD ? Block.WORK : Block.HOBBY;
            case NIGHT_WATCH -> role == Role.VETERAN ? Block.NIGHT_WATCH : Block.SLEEP;
            default -> block;
        };
    }
    /** What they're doing, as their conversation window shows it; null to use the usual words. */
    public static String doing(Role role, String job, Block block, boolean stormy) {
        return switch (role) {
            case PARIAH -> switch (block) {
                case WORK -> "Mending the old house"; case HOBBY -> "Keeping to themselves"; case EVENING -> "Brooding by the fire";
                case LUNCH_HOME, SUPPER, BREAKFAST -> "Eating alone"; default -> null; };
            case HOMESTEADER -> switch (block) {
                case WORK -> job.equals("cook") ? "Keeping house" : "Working the fields"; case EVENING -> "By the fire at home"; default -> null; };
            case SHEPHERD -> switch (block) { case WORK -> "Tending the flock"; case HOBBY -> "Up on the lookout rock"; default -> null; };
            case HERBALIST -> switch (block) { case WORK -> "Brewing remedies"; case HOBBY -> "Gathering herbs"; default -> null; };
            case VETERAN -> switch (block) {
                case WORK -> "Drilling with the bow"; case NIGHT_WATCH -> stormy ? "Keeping the watch in the storm" : "Keeping the watch"; default -> null; };
        };
    }
    /** The time-of-day group a homestead greeting is written for: "morning", "evening", "night", or null (midday). */
    public static String greetingTime(String period) {
        return switch (period) { case "dawn", "morning" -> "morning"; case "evening" -> "evening"; case "night", "late" -> "night"; default -> null; };
    }
    private Dwelling() {}
}
