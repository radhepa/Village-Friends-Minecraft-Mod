package dev.villagefriends.fishing;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Random;
import java.util.Set;

/**
 * Tall tales: the words residents use for where and when a legendary fish bites ("the rivers and lakes of the
 * plains", "on rainy nights"), read straight from its row in the fish table so the rumours are always true,
 * and which legend a resident is likeliest to talk about (the one in their own part of the world).
 */
public final class Tales {
    /** "the rivers and lakes of the plains", "the deep sea", "the black water below the world". */
    public static String where(Fish f) {
        var w = f.water();
        if (w.contains("deepcave")) return "the black water below the world";
        if (w.contains("cave")) return "the underground pools";
        if (w.contains("deep")) return f.region().isEmpty() ? "the deep sea" : "the deep sea off " + regions(f);
        if (w.contains("ocean") || w.contains("warm") || w.contains("cold"))
            return f.region().isEmpty() ? (w.contains("warm") ? "the warm seas" : w.contains("cold") ? "the cold seas" : "the open sea") : "the sea off " + regions(f);
        if (w.equals(Set.of("swamp"))) return "the black water of " + (f.region().isEmpty() ? "the swamps" : regions(f));
        boolean desert = f.region().contains("desert") || f.region().contains("badlands");
        var kinds = new ArrayList<String>();
        if (w.contains("river")) kinds.add("rivers");
        if (w.contains("lake")) kinds.add(desert ? "pools" : "lakes");
        if (w.contains("swamp")) kinds.add("marshes");
        if (desert && kinds.size() == 2 && kinds.get(0).equals("rivers")) kinds = new ArrayList<>(List.of("pools", "rivers"));
        String water = kinds.isEmpty() ? "waters" : and(kinds);
        return "the " + water + (f.region().isEmpty() ? " of the world" : " of " + regions(f));
    }
    private static String regions(Fish f) {
        var words = new ArrayList<String>();
        for (var r : f.region()) words.add(FishTable.regionWords(r));
        words.sort(null);
        return or(words);
    }

    /** "on rainy nights", "at noon under a clear sky in summer", "at dawn in the autumn rains", "whenever thunder rolls". */
    public static String when(Fish f) {
        var t = f.time(); String weather = f.weather();
        var seasons = new ArrayList<>(f.season());
        seasons.sort(java.util.Comparator.comparingInt(s -> List.of("spring", "summer", "autumn", "winter").indexOf(s)));
        boolean rain = weather.equals("rain"), clear = weather.equals("clear");
        String moment;
        if (weather.equals("thunder")) moment = t.isEmpty() ? "whenever thunder rolls" : times(t) + " when thunder rolls";
        else if (t.equals(Set.of("night")) && rain) moment = "on rainy nights";
        else if (t.equals(Set.of("night")) && clear) moment = "on clear, starry nights";
        else if (t.equals(Set.of("day")) && rain) moment = "on rainy days";
        else if (t.equals(Set.of("day")) && clear) moment = "on bright, clear days";
        else if (t.isEmpty() && rain) moment = "whenever it rains";
        else if (t.isEmpty() && clear) moment = "under clear skies";
        else if (t.isEmpty()) moment = seasons.isEmpty() ? "at any hour of the day or night" : "";
        else moment = times(t) + (clear ? " under a clear sky" : rain && !(seasons.size() == 1 && seasons.getFirst().equals("autumn")) ? " in the rain" : "");
        if (seasons.isEmpty()) return moment;
        String in = rain && seasons.size() == 1 && seasons.getFirst().equals("autumn") && !moment.contains("rain") ? "in the autumn rains" : "in " + or(seasons);
        return moment.isEmpty() ? in : moment + " " + in;
    }
    private static String times(Set<String> t) {
        var out = new ArrayList<String>();
        for (var k : List.of("dawn", "day", "noon", "dusk", "night")) {
            if (!t.contains(k)) continue;
            out.add(switch (k) { case "dawn" -> "at dawn"; case "day" -> "by day"; case "noon" -> "at noon"; case "dusk" -> "at dusk"; default -> "at night"; });
        }
        if (out.size() == 2 && out.get(0).startsWith("at ") && out.get(1).startsWith("at ")) return out.get(0) + " or " + out.get(1).substring(3);
        return or(out);
    }
    static String and(List<String> words) { return join(words, "and"); }
    static String or(List<String> words) { return join(words, "or"); }
    private static String join(List<String> words, String last) {
        if (words.isEmpty()) return "";
        if (words.size() == 1) return words.getFirst();
        return String.join(", ", words.subList(0, words.size() - 1)) + " " + last + " " + words.getLast();
    }

    /**
     * The legend a resident tells of: usually one from their own region (a desert villager talks of Sunscale),
     * now and then any other; and rather one {@code known} doesn't already include.
     */
    public static Fish legend(Collection<Fish> table, String region, Set<String> known, Random random) {
        var legends = table.stream().filter(Fish::legendary).toList();
        if (legends.isEmpty()) return null;
        var local = legends.stream().filter(f -> region != null && f.region().contains(region)).toList();
        var fresh = legends.stream().filter(f -> !known.contains(f.id())).toList();
        List<Fish> from = !local.isEmpty() && random.nextInt(3) > 0 ? local : !fresh.isEmpty() && random.nextBoolean() ? fresh : legends;
        return from.get(random.nextInt(from.size()));
    }

    private Tales() {}
}
