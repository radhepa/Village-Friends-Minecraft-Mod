package dev.villagefriends.hearth;

import java.lang.reflect.Method;
import net.fabricmc.loader.api.FabricLoader;
import net.minecraft.world.level.Level;

/**
 * Optional seasons from Turning Seasons (mod id {@code turningseasons}), read through its public API by
 * reflection so Village Friends never needs it: in winter residents now and then eat preserved winter food
 * (sauerkraut, pickled onions, smoked fish, mulled cider, spice cake), and those dishes keep you Well Fed half
 * as long again. Without the mod there is no winter here and nothing changes.
 */
public final class HearthSeasons {
    public static final String MOD = "turningseasons";
    /** Winter dishes eaten in winter: this much longer Well Fed. */
    public static final double WINTER_FOOD = 1.5;
    private static boolean available = FabricLoader.getInstance().isModLoaded(MOD);
    private static Method getSeason, id;

    /** "spring", "summer", "autumn" or "winter", or null without Turning Seasons. */
    public static String season(Level level) {
        if (!available || level == null) return null;
        try {
            if (getSeason == null) getSeason = Class.forName("dev.turningseasons.api.TurningSeasonsApi").getMethod("getSeason", Level.class);
            Object season = getSeason.invoke(null, level);
            if (season == null) return null;
            if (id == null) id = season.getClass().getMethod("id");
            return (String) id.invoke(season);
        } catch (ReflectiveOperationException | LinkageError | ClassCastException e) {
            available = false;
            return null;
        }
    }
    public static boolean winter(Level level) { return "winter".equals(season(level)); }

    private HearthSeasons() {}
}
