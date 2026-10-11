package dev.villagefriends.rpg;

import java.util.List;
import java.util.Map;
import java.util.function.Predicate;

/**
 * The other mods of the Village Friends modpack that the RPG knows about. None of them is required:
 * their monsters, places, jobs and items only show up when the mod is installed. Pure; the server
 * and client set {@link #installed} from Fabric Loader at start-up (tests leave every mod "installed").
 */
public final class Modpack {
    private Modpack() {}

    /** Mod id to its display name, in the order the Atlas lists them. */
    public static final Map<String, String> MODS = orderedMap(
            "villagefriends", "Village Friends",
            "nsvmobs", "Not-So-Vanilla Mobs",
            "plataclan", "The Plata Clan",
            "caveexpansion", "Cave Expansion",
            "oceanexpansion", "Ocean Expansion",
            "seafriends", "Sea Friends",
            "skyfriends", "Sky Friends",
            "netherfriends", "Nether Friends",
            "endexpansion", "End Friends",
            "turningseasons", "Turning Seasons");

    private static Predicate<String> installed = id -> true;
    /** Called once at start-up with Fabric Loader's check. */
    public static void detect(Predicate<String> isLoaded) { installed = id -> id.isEmpty() || id.equals("minecraft") || isLoaded.test(id); }
    /** Whether a mod is installed; "" and "minecraft" always are. */
    public static boolean installed(String mod) { return installed.test(mod); }
    /** The mod an id belongs to: "nsvmobs:sporeling" to "nsvmobs", a bare path to "minecraft". */
    public static String modOf(String id) { int c = id.indexOf(':'); return c < 0 ? "minecraft" : id.substring(0, c); }
    public static String name(String mod) { return MODS.getOrDefault(mod, mod); }
    /** Installed modpack mods (Village Friends itself always is). */
    public static List<String> present() { return MODS.keySet().stream().filter(Modpack::installed).toList(); }

    private static Map<String, String> orderedMap(String... kv) {
        var m = new java.util.LinkedHashMap<String, String>();
        for (int i = 0; i < kv.length; i += 2) m.put(kv[i], kv[i + 1]);
        return java.util.Collections.unmodifiableMap(m);
    }
}
