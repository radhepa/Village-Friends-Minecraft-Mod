package dev.villagefriends.quest;

import java.util.Locale;
import java.util.Set;

/** Counts and plurals for notices: "12 wheat", "3 iron ingots", "a cake", "5 zombies", "a witch". */
public final class Words {
    /** Things you count by the heap, not one by one. */
    private static final Set<String> UNCOUNTED = Set.of("wheat", "wool", "string", "leather", "coal", "flint", "paper", "sugar", "glowstone dust",
            "redstone dust", "redstone", "kelp", "dried kelp", "bone meal", "bread", "cod", "salmon", "raw cod", "raw salmon", "cooked cod", "cooked salmon",
            "gunpowder", "clay", "honeycomb", "sweet berries", "glow berries", "cocoa beans", "wheat seeds", "beetroot seeds", "pumpkin seeds",
            "melon seeds", "raw beef", "raw porkchop", "raw mutton", "raw chicken", "raw rabbit", "cooked beef", "cooked mutton", "cooked chicken",
            "steak", "rabbit stew", "mushroom stew", "beetroot soup", "cobblestone", "stone", "dirt", "sand", "gravel", "glass", "white wool",
            "bamboo", "sugar cane", "cactus", "moss", "amethyst", "prismarine", "lapis lazuli", "quartz", "nether quartz", "hay");

    /** "12 wheat", "3 iron ingots", "a cake", "an apple". */
    public static String count(int n, String name) {
        String lower = name.toLowerCase(Locale.ROOT);
        if (n == 1) return (UNCOUNTED.contains(lower) ? "some " : article(lower) + " ") + lower;
        return n + " " + plural(lower);
    }
    public static String article(String word) { return word.isEmpty() || "aeiou".indexOf(word.charAt(0)) < 0 ? "a" : "an"; }
    public static String plural(String name) {
        if (UNCOUNTED.contains(name) || name.endsWith("s") && !name.endsWith("ss")) return name;
        int of = name.indexOf(" of ");
        if (of > 0) return plural(name.substring(0, of)) + name.substring(of);
        if (name.endsWith("y") && name.length() > 1 && "aeiou".indexOf(name.charAt(name.length() - 2)) < 0) return name.substring(0, name.length() - 1) + "ies";
        if (name.endsWith("ch") || name.endsWith("sh") || name.endsWith("x") || name.endsWith("ss")) return name + "es";
        if (name.endsWith("leaf")) return name.substring(0, name.length() - 4) + "leaves";
        if (name.endsWith("foot")) return name.substring(0, name.length() - 4) + "feet";
        return name + "s";
    }
    /** "5 zombies", "a witch", "2 witches". */
    public static String mobs(int n, String group) {
        String one = Postings.monster(group);
        return n == 1 ? article(one) + " " + one : n + " " + plural(one);
    }
    private Words() {}
}
