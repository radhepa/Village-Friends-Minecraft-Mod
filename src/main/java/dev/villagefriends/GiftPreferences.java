package dev.villagefriends;

import java.util.Map;
import java.util.Set;

public final class GiftPreferences {
    private static final Set<String> FLOWERS = Set.of("dandelion", "poppy", "blue_orchid", "allium",
            "azure_bluet", "red_tulip", "orange_tulip", "white_tulip", "pink_tulip", "oxeye_daisy",
            "cornflower", "lily_of_the_valley", "sunflower", "lilac", "rose_bush", "peony",
            "torchflower", "pitcher_plant", "pink_petals", "wildflowers", "cactus_flower");
    private static final Set<String> TREATS = Set.of("bread", "apple", "cookie", "pumpkin_pie",
            "cake", "sweet_berries", "glow_berries", "honey_bottle", "golden_carrot");
    private static final Map<String, Set<String>> FAVORITES = Map.ofEntries(
            Map.entry("farmer", Set.of("wheat", "carrot", "potato", "beetroot", "pumpkin", "melon")),
            Map.entry("librarian", Set.of("book", "paper", "writable_book", "enchanted_book")),
            Map.entry("fisherman", Set.of("cod", "salmon", "tropical_fish", "cooked_cod", "cooked_salmon")),
            Map.entry("fletcher", Set.of("flint", "feather", "arrow", "bow")),
            Map.entry("cleric", Set.of("amethyst_shard", "glowstone_dust", "ender_pearl", "blaze_powder")),
            Map.entry("cartographer", Set.of("paper", "map", "compass")),
            Map.entry("armorer", Set.of("iron_ingot", "diamond", "iron_chestplate")),
            Map.entry("toolsmith", Set.of("iron_ingot", "diamond", "iron_pickaxe")),
            Map.entry("weaponsmith", Set.of("iron_ingot", "diamond", "iron_sword")),
            Map.entry("leatherworker", Set.of("leather", "rabbit_hide")),
            Map.entry("mason", Set.of("clay_ball", "brick", "quartz", "terracotta")),
            Map.entry("shepherd", Set.of("white_wool", "pink_wool", "blue_wool", "shears")),
            Map.entry("butcher", Set.of("cooked_beef", "cooked_porkchop", "cooked_chicken")));

    public static int value(String profession, boolean baby, String identifier) {
        // Modded items must not receive vanilla preferences merely by sharing a path.
        if (!identifier.startsWith("minecraft:")) return 0;
        String item = identifier.substring("minecraft:".length());
        if (baby && (item.equals("cookie") || item.equals("apple"))) return 12;
        if (item.equals("emerald")) return 12;
        if (!baby && FAVORITES.getOrDefault(profession, Set.of()).contains(item)) return 10;
        if (FLOWERS.contains(item)) return 8;
        if (TREATS.contains(item)) return 6;
        return 0;
    }

    public static String hint(String profession, boolean baby) {
        if (baby) return "Favorite gifts: cookies and apples. Flowers are lovely too!";
        String favorite = switch (profession) {
            case "farmer" -> "fresh crops";
            case "librarian" -> "books and paper";
            case "fisherman" -> "fish";
            case "fletcher" -> "flint, feathers, and arrows";
            case "cleric" -> "amethyst, glowstone, and ender pearls";
            case "cartographer" -> "paper, maps, and compasses";
            case "armorer", "toolsmith", "weaponsmith" -> "iron and diamonds";
            case "leatherworker" -> "leather and rabbit hides";
            case "mason" -> "clay, bricks, and quartz";
            case "shepherd" -> "wool and shears";
            case "butcher" -> "cooked meat";
            default -> "flowers and tasty treats";
        };
        return "Favorite gifts: " + favorite + ". Everyone enjoys emeralds and flowers.";
    }

    private GiftPreferences() {}
}
