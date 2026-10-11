package dev.villagefriends.rpg;

import net.fabricmc.loader.api.FabricLoader;
import net.minecraft.world.level.Level;

import java.lang.reflect.Method;

/**
 * Turning Seasons, if it's installed, read through its public API by reflection (the way Village Friends'
 * Hearth reads it), so the add-on never needs the mod. Jobs follow the season, and autumn's harvest
 * teaches Farming faster. Without the mod there are no seasons and nothing changes.
 */
public final class Seasons {
    private Seasons() {}
    /** Farming experience from ripe crops in autumn, harvest season. */
    public static final double AUTUMN_FARMING = 1.25;

    private static boolean tried, broken;
    private static Method hasSeasons, getSeason, seasonId;

    /** "spring", "summer", "autumn" or "winter" where this level has seasons, else "". */
    public static String season(Level level) {
        if (!load()) return "";
        try {
            if (!(boolean) hasSeasons.invoke(null, level)) return "";
            Object s = getSeason.invoke(null, level);
            return s == null ? "" : (String) seasonId.invoke(s);
        } catch (ReflectiveOperationException | RuntimeException e) {
            broken = true;
            Rpg.LOGGER.warn("Couldn't read the season from Turning Seasons, ignoring seasons: {}", e.toString());
            return "";
        }
    }
    /** The Farming experience multiplier for a ripe crop in this level's season. */
    public static double farming(Level level) { return season(level).equals("autumn") ? AUTUMN_FARMING : 1; }

    private static boolean load() {
        if (broken) return false;
        if (tried) return hasSeasons != null;
        tried = true;
        if (!FabricLoader.getInstance().isModLoaded("turningseasons")) return false;
        try {
            var api = Class.forName("dev.turningseasons.api.TurningSeasonsApi");
            hasSeasons = api.getMethod("hasSeasons", Level.class);
            getSeason = api.getMethod("getSeason", Level.class);
            seasonId = Class.forName("dev.turningseasons.api.Season").getMethod("id");
            return true;
        } catch (ReflectiveOperationException | RuntimeException e) {
            broken = true; hasSeasons = null;
            Rpg.LOGGER.warn("Turning Seasons is installed but its API didn't load, ignoring seasons: {}", e.toString());
            return false;
        }
    }
}
