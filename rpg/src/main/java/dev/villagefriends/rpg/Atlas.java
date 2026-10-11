package dev.villagefriends.rpg;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * The Atlas: every kind of place the modpack's mods build into the world. Standing inside one for the first
 * time is a discovery (character experience and a line on the Atlas page), and explorers, cartographers and
 * bards can send you to find one as a job. Pure data; {@link Discoveries} does the looking.
 *
 * <p>{@code tier} (1-5) is how far and how dangerous the place is: it sets the discovery's experience and
 * the earliest quest tier that asks for it. Places of mods that aren't installed never show up.
 */
public final class Atlas {
    private Atlas() {}

    /**
     * One kind of place. {@code id} is "mod:key"; {@code structures} are the structure ids that count as it
     * (Plata dens, for example, come in six regional styles). {@code quest} is false for places too common
     * to send anyone looking for.
     */
    public record Place(String id, String name, String mod, int tier, boolean quest, List<String> structures) {
        /** The article-led name a job uses: "Find the Sunken Forge", "Find a Plata Clan Scale Den". */
        public String findLabel() { return "Find " + name; }
    }

    private static Place p(String mod, String key, String name, int tier, String... structures) {
        return new Place(mod + ":" + key, name, mod, tier, true, List.of(structures.length == 0 ? new String[]{mod + ":" + key} : structures));
    }
    private static Place common(String mod, String key, String name, String... structures) {
        return new Place(mod + ":" + key, name, mod, 1, false, List.of(structures));
    }
    private static String[] styles(String mod, String kind, String... regions) {
        var out = new String[regions.length];
        for (int i = 0; i < regions.length; i++) out[i] = mod + ":" + kind + "_" + regions[i];
        return out;
    }

    public static final List<Place> PLACES = List.of(
            // Village Friends: villages for every biome, and the homesteads between them.
            common("villagefriends", "village", "a plains village", "villagefriends:village"),
            common("villagefriends", "village_desert", "a desert village", "villagefriends:village_desert"),
            common("villagefriends", "village_savanna", "a savanna village", "villagefriends:village_savanna"),
            common("villagefriends", "village_snowy", "a snowy village", "villagefriends:village_snowy"),
            common("villagefriends", "village_taiga", "a taiga village", "villagefriends:village_taiga"),
            p("villagefriends", "homestead_farmstead", "a farmstead in the wild", 1),
            p("villagefriends", "homestead_shepherd_fold", "a shepherd's fold", 1),
            p("villagefriends", "homestead_herbalist_cottage", "the herbalist's cottage", 1),
            p("villagefriends", "homestead_watchtower", "an old watchtower", 1),
            p("villagefriends", "homestead_pariah_house", "the pariah's house", 2),
            // The Plata Clan's hideouts.
            p("plataclan", "den", "a Plata Clan Scale Den", 2, styles("plataclan", "den", "green", "cold", "sand", "mesa", "dry", "stone")),
            p("plataclan", "warren", "a Silver Warren", 4, styles("plataclan", "warren", "green", "cold", "sand", "mesa", "dry", "stone")),
            // Cave Expansion's delves.
            p("caveexpansion", "camp", "a Delvers' Camp", 2),
            p("caveexpansion", "hermit", "Hermit's Hollow", 2),
            p("caveexpansion", "seam", "the Buried Seam", 2),
            p("caveexpansion", "cistern", "the Drowned Cistern", 3),
            p("caveexpansion", "post", "a Deepwatch Post", 3),
            p("caveexpansion", "grotto", "the Glimmering", 3),
            p("caveexpansion", "ossuary", "the Ossuary", 3),
            p("caveexpansion", "forge", "the Sunken Forge", 4),
            // Ocean Expansion's sites.
            p("oceanexpansion", "lighthouse", "Lighthouse Isle", 2),
            p("oceanexpansion", "whale", "the Whalefall", 2),
            p("oceanexpansion", "fort", "Tidewatch Fort", 3),
            p("oceanexpansion", "smugglers", "Smugglers' Rock", 3),
            p("oceanexpansion", "galleon", "the Sunken Galleon", 3),
            p("oceanexpansion", "grotto", "the Pearl Grotto", 3),
            p("oceanexpansion", "bell", "Wexley's Diving Bell", 3),
            p("oceanexpansion", "iceberg", "the Frozen Hold", 3),
            p("oceanexpansion", "temple", "the Drowned Sanctum", 4),
            p("oceanexpansion", "vents", "the Ember Vents", 4),
            // Sea Friends' towns.
            p("seafriends", "reef_town", "a merfolk Reef Town", 2),
            p("seafriends", "prism_court", "a Prismari Prism Court", 3),
            // Sky Friends' sky.
            p("skyfriends", "sky_islet", "a sky islet", 2),
            p("skyfriends", "wind_shrine", "a Wind Shrine", 2),
            p("skyfriends", "sky_village", "a Cirri sky village", 3),
            p("skyfriends", "ruined_belltower", "a ruined belltower in the sky", 3),
            // Nether Friends' villages.
            p("netherfriends", "hold", "a Piglin Hold", 4),
            p("netherfriends", "vigil", "a Withren Vigil", 4),
            p("netherfriends", "mooring", "a Magmari Mooring", 4),
            p("netherfriends", "loom", "a Weft Loom", 4),
            p("netherfriends", "eave", "a Ghastkin Eave", 4),
            // End Friends' villages and the Court.
            p("endexpansion", "spire_village", "a Shulkin Spire", 5),
            p("endexpansion", "stead_village", "a Chorrin Stead", 5),
            p("endexpansion", "crossing", "an End Crossing", 5),
            p("endexpansion", "citadel", "an Endarch Citadel", 5));

    private static final Map<String, Place> BY_ID = new HashMap<>(), BY_STRUCTURE = new HashMap<>();
    static { for (var pl : PLACES) { BY_ID.put(pl.id(), pl); for (var st : pl.structures()) BY_STRUCTURE.put(st, pl); } }

    public static Place byId(String id) { return BY_ID.get(id); }
    /** The place a structure id belongs to, or null if it isn't one the Atlas lists. */
    public static Place ofStructure(String structure) { return BY_STRUCTURE.get(structure); }
    /** Places of installed mods, in Atlas order. */
    public static List<Place> shown() { return PLACES.stream().filter(pl -> Modpack.installed(pl.mod())).toList(); }
    /** Places a job can send you to at exactly this quest tier, of installed mods. */
    public static List<Place> questsAt(int tier) { return PLACES.stream().filter(pl -> pl.quest() && pl.tier() == tier && Modpack.installed(pl.mod())).toList(); }
    /** The sheet mark that remembers a discovery (its value is the day it was found, plus one). */
    public static String mark(Place pl) { return "found:" + pl.id(); }
}
