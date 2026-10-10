package dev.villagefriends.fishing;

import java.util.LinkedHashSet;
import java.util.Set;

/**
 * Where and when a line is in the water: what kind of water ({@code river}, {@code lake}, {@code swamp},
 * {@code ocean} plus {@code warm}/{@code cold}/{@code deep}, {@code cave} plus {@code deepcave}), the land region
 * around it, the time of day as fish see it, the weather, the season (null without Turning Seasons) and
 * whether it is open water (treasure only comes from open water, as in vanilla).
 */
public record Spot(Set<String> waters, String region, Set<String> times, boolean raining, boolean thundering, String season, boolean openWater) {

    /**
     * The fish's names for the time ({@code ticks} of the day, 0 = 6:00): dawn 5:00–7:00, day 7:00–18:00 (noon
     * 11:00–13:00 within it), dusk 18:00–19:30, night after that.
     */
    public static Set<String> times(int ticks) {
        int t = Math.floorMod(ticks, 24000);
        var out = new LinkedHashSet<String>();
        if (t >= 23000 || t < 1000) out.add("dawn");
        else if (t < 12000) { out.add("day"); if (t >= 5000 && t < 7000) out.add("noon"); }
        else if (t < 13500) out.add("dusk");
        else out.add("night");
        return out;
    }

    /**
     * The water at the bobber from what is known about it: underground (no sky, well below sea level) is cave
     * water; otherwise the biome's kind of water decides (an ocean, a river, a swamp), and anything else is a lake.
     */
    public static Set<String> waters(boolean underground, int y, String biomeWater, boolean warmOcean, boolean coldOcean, boolean deepOcean) {
        var out = new LinkedHashSet<String>();
        if (underground) {
            out.add("cave");
            if (y < 0) out.add("deepcave");
            return out;
        }
        switch (biomeWater) {
            case "ocean" -> {
                out.add("ocean");
                if (warmOcean) out.add("warm");
                if (coldOcean) out.add("cold");
                if (deepOcean) out.add("deep");
            }
            case "river" -> out.add("river");
            case "swamp" -> out.add("swamp");
            default -> out.add("lake");
        }
        return out;
    }
}
