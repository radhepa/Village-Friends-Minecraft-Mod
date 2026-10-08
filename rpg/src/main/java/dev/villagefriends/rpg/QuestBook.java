package dev.villagefriends.rpg;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

/**
 * Which villagers give which jobs, and how a day's offer is drawn. Pure. A template is
 * "kind target base minTier difficulty"; counts grow with how far the player's tier is above the
 * template's, and rewards scale with the player's level so a job is always worth taking.
 */
public final class QuestBook {
    private QuestBook() {}
    public record Template(String kind, String target, int base, int minTier, double diff) {}

    private static final Map<String, String> POOL_TEXT = Map.ofEntries(
            Map.entry("guard", "slay zombie 8 1 .2, slay skeleton 8 1 .2, slay spider 6 1 .2, slay creeper 5 1 .22, slay slime 6 2 .22, slay drowned 6 2 .22, slay enderman 4 2 .28, slay witch 2 3 .3, slay illager 5 3 .3, slay blaze 6 3 .32, slay piglin 8 3 .28, slay wither_skeleton 4 4 .4, slay ghast 2 4 .38, slay guardian 4 4 .38, slay breeze 3 4 .4, slay elder_guardian 1 4 .8, slay shulker 3 5 .45, slay warden 1 5 1, slay wither 1 5 1"),
            Map.entry("holy", "slay zombie 8 1 .2, slay skeleton 8 1 .2, slay drowned 6 2 .22, slay phantom 3 2 .3, gather rotten_flesh 16 1 .15, gather spider_eye 4 1 .18, gather bone 12 1 .15, gather gunpowder 5 2 .2, gather glowstone_dust 12 3 .25, gather blaze_rod 4 3 .32, gather nether_wart 8 3 .28, slay wither_skeleton 4 4 .4, gather ghast_tear 1 4 .4, gather dragon_breath 1 5 .5"),
            Map.entry("smith", "mine ores 12 1 .2, gather coal 16 1 .15, gather iron_ingot 8 1 .2, gather copper_ingot 12 1 .15, gather gold_ingot 6 2 .25, gather redstone 16 2 .2, gather lapis_lazuli 12 2 .22, gather diamond 2 3 .4, gather obsidian 8 3 .3, mine ores 24 3 .3, gather netherite_scrap 1 5 .7"),
            Map.entry("mason", "mine stone 64 1 .15, mine ores 8 1 .2, gather clay_ball 16 1 .18, gather brick 12 1 .2, gather cobbled_deepslate 32 2 .2, gather tuff 16 2 .2, gather calcite 8 2 .22, gather quartz 16 3 .28, gather amethyst_shard 8 3 .28, mine stone 160 3 .3, gather prismarine_shard 8 4 .35"),
            Map.entry("farm", "harvest crops 16 1 .15, gather wheat 16 1 .15, gather carrot 16 1 .15, gather potato 16 1 .15, gather beetroot 12 1 .15, gather pumpkin 6 1 .18, gather melon_slice 16 1 .15, gather sugar_cane 16 1 .15, breed animals 4 1 .18, gather sweet_berries 16 2 .18, gather cocoa_beans 8 2 .22, gather glow_berries 8 3 .26, harvest crops 48 3 .25"),
            Map.entry("kitchen", "gather bread 8 1 .18, gather baked_potato 8 1 .15, gather cooked_beef 6 1 .2, gather cooked_porkchop 6 1 .2, gather mushroom_stew 3 1 .18, harvest crops 16 1 .15, gather cookie 16 2 .2, gather pumpkin_pie 3 2 .22, gather cake 1 2 .25, gather honey_bottle 3 3 .28, gather rabbit_stew 2 3 .3"),
            Map.entry("fish", "fish fish 5 1 .2, gather cod 8 1 .15, gather salmon 6 1 .18, gather ink_sac 6 1 .18, gather tropical_fish 2 2 .25, gather pufferfish 2 2 .25, gather glow_ink_sac 3 3 .28, fish fish 15 3 .3, gather prismarine_crystals 6 4 .35, gather nautilus_shell 1 4 .4"),
            Map.entry("butcher", "breed animals 4 1 .18, gather beef 8 1 .18, gather porkchop 8 1 .18, gather mutton 8 1 .18, gather chicken 8 1 .18, gather leather 6 1 .18, gather rabbit 4 2 .22, breed animals 12 3 .28"),
            Map.entry("leather", "gather leather 8 1 .18, gather string 12 1 .15, gather white_wool 12 1 .15, slay spider 8 1 .2, gather rabbit_hide 4 2 .22, gather armadillo_scute 3 3 .28, gather phantom_membrane 4 3 .3, gather turtle_scute 2 4 .4"),
            Map.entry("shepherd", "gather white_wool 16 1 .15, gather string 12 1 .15, breed animals 4 1 .18, gather blue_dye 4 2 .2, gather black_dye 6 2 .2, gather lime_dye 4 2 .22, gather purple_dye 3 3 .25"),
            Map.entry("scholar", "enchant items 2 1 .22, gather paper 16 1 .15, gather book 4 1 .18, gather feather 8 1 .15, gather ink_sac 6 1 .18, trade villagers 3 1 .15, gather lapis_lazuli 12 2 .22, gather amethyst_shard 6 3 .28, gather ender_pearl 4 3 .3, gather blaze_powder 6 3 .3, enchant items 6 3 .32, gather echo_shard 1 5 .55"),
            Map.entry("explorer", "explore * 1 1 .25, explore * 1 2 .3, explore * 1 3 .35, explore * 1 4 .45, explore * 1 5 .55, gather paper 12 1 .15, trade villagers 3 1 .15, gather compass 1 2 .2"),
            Map.entry("fletcher", "gather flint 12 1 .15, gather feather 12 1 .15, gather stick 32 1 .12, gather string 8 1 .15, slay skeleton 8 1 .2, gather arrow 32 2 .2, slay phantom 3 2 .3, gather spectral_arrow 8 3 .28, slay ghast 2 4 .38"),
            Map.entry("carpenter", "mine logs 32 1 .15, gather oak_log 16 1 .15, gather spruce_log 16 1 .15, gather birch_log 16 1 .15, gather dark_oak_log 16 2 .2, gather jungle_log 16 2 .2, gather cherry_log 12 2 .22, gather bamboo 24 2 .18, gather mangrove_log 12 3 .25, mine logs 96 3 .28"),
            Map.entry("artist", "explore * 1 1 .25, explore * 1 2 .3, explore * 1 3 .35, gather poppy 6 1 .12, gather dandelion 6 1 .12, gather cornflower 4 1 .15, gather lily_of_the_valley 3 2 .2, gather sunflower 3 2 .2, gather note_block 2 2 .2, gather torchflower 1 3 .3, gather music_disc_cat 1 4 .45"));
    private static final Map<String, List<String>> JOBS = Map.ofEntries(
            Map.entry("armorer", List.of("smith", "guard")), Map.entry("weaponsmith", List.of("guard", "smith")), Map.entry("toolsmith", List.of("smith")),
            Map.entry("mason", List.of("mason")), Map.entry("farmer", List.of("farm")), Map.entry("cook", List.of("kitchen")),
            Map.entry("tavern_keeper", List.of("kitchen", "butcher")), Map.entry("fisherman", List.of("fish")), Map.entry("butcher", List.of("butcher")),
            Map.entry("leatherworker", List.of("leather")), Map.entry("tailor", List.of("leather", "shepherd")), Map.entry("shepherd", List.of("shepherd")),
            Map.entry("librarian", List.of("scholar")), Map.entry("scholar", List.of("scholar")), Map.entry("cartographer", List.of("explorer")),
            Map.entry("painter", List.of("artist")), Map.entry("bard", List.of("artist")), Map.entry("fletcher", List.of("fletcher")),
            Map.entry("archer", List.of("fletcher", "guard")), Map.entry("knight", List.of("guard")), Map.entry("cleric", List.of("holy")),
            Map.entry("apothecary", List.of("holy")), Map.entry("carpenter", List.of("carpenter")));
    private static final String[] DESTINATIONS = {
            "biome:birch_forest biome:savanna biome:taiga biome:swamp biome:flower_forest biome:sunflower_plains biome:stony_shore",
            "biome:desert biome:jungle biome:badlands biome:snowy_plains biome:dark_forest biome:mangrove_swamp biome:cherry_grove biome:meadow",
            "dim:the_nether biome:mushroom_fields biome:ice_spikes biome:lush_caves biome:dripstone_caves biome:bamboo_jungle biome:pale_garden",
            "biome:deep_dark biome:soul_sand_valley biome:warped_forest biome:basalt_deltas biome:crimson_forest",
            "dim:the_end biome:end_highlands biome:small_end_islands"};
    private static final Map<String, String[]> FLAVOR = Map.ofEntries(
            Map.entry("guard", new String[]{"The night watch can't keep up anymore.", "Something's been prowling past the walls. I'd sleep better if you dealt with it."}),
            Map.entry("holy", new String[]{"The sick need remedies, and remedies need ingredients.", "Restless dead walk too close to our homes. Help me put them to rest."}),
            Map.entry("smith", new String[]{"My forge is hungry and my stock is thin.", "A smith is only as good as the metal on the anvil."}),
            Map.entry("mason", new String[]{"Walls don't build themselves, you know.", "I've an order for stone and not enough hands to cut it."}),
            Map.entry("farm", new String[]{"Harvest's coming in faster than I can gather it.", "The market's tomorrow and my baskets are half empty."}),
            Map.entry("kitchen", new String[]{"We've hungry mouths at the tavern tonight.", "The pantry's looking bare and supper won't cook itself."}),
            Map.entry("fish", new String[]{"The fish are biting, but my back isn't.", "I promised the tavern a good catch."}),
            Map.entry("butcher", new String[]{"Orders are piling up at the counter.", "The village eats well, but only if somebody tends the herds."}),
            Map.entry("leather", new String[]{"I've more orders than hides to fill them.", "Good material is hard to come by these days."}),
            Map.entry("shepherd", new String[]{"The flock needs looking after, and I need supplies.", "Winter's coming, and everyone wants a warm blanket."}),
            Map.entry("scholar", new String[]{"My studies have stalled for want of materials.", "Knowledge isn't free, but I can make it worth your while."}),
            Map.entry("explorer", new String[]{"My maps have blank corners that keep me up at night.", "I need someone to see a place with their own eyes and tell me it's real."}),
            Map.entry("fletcher", new String[]{"The guards burn through arrows faster than I can fletch them.", "I need supplies for the archers."}),
            Map.entry("carpenter", new String[]{"There's a roof to raise and not enough timber.", "Wood, wood and more wood. That's carpentry."}),
            Map.entry("artist", new String[]{"I'm looking for inspiration, and a little color.", "Every song needs a story. Go and find me one."}));
    private static final Map<String, List<Template>> POOLS = new HashMap<>();
    static {
        POOL_TEXT.forEach((pool, text) -> {
            var list = new ArrayList<Template>();
            for (var entry : text.split(",")) {
                var f = entry.trim().split("\\s+");
                list.add(new Template(f[0], f[1], Integer.parseInt(f[2]), Integer.parseInt(f[3]), Double.parseDouble(f[4])));
            }
            POOLS.put(pool, List.copyOf(list));
        });
    }
    private static final double[] SCALE = {1, 1.5, 2.2, 3, 4};

    /** Quest pools a villager with this profession draws from; empty for none, nitwits and children. */
    public static List<String> pools(String profession, boolean guard) {
        if (guard) return List.of("guard");
        return JOBS.getOrDefault(profession, List.of());
    }
    public static List<Template> pool(String name) { return POOLS.getOrDefault(name, List.of()); }
    public static int tier(int level) { return 1 + (level >= 10 ? 1 : 0) + (level >= 25 ? 1 : 0) + (level >= 45 ? 1 : 0) + (level >= 70 ? 1 : 0); }

    /** The job a villager offers on a given day, or null if they have none to give. */
    public static Quest offer(List<String> pools, long seed, int level, String id, String giver, String giverName, String job) {
        if (pools.isEmpty()) return null;
        var rng = new Random(seed);
        String pool = pools.get(rng.nextInt(pools.size()));
        int tier = tier(level);
        var weighted = new ArrayList<Template>();
        for (var t : pool(pool)) {
            if (t.minTier() > tier) continue;
            int w = t.minTier() == tier ? 3 : tier - t.minTier() >= 2 ? 1 : 2;
            for (int i = 0; i < w; i++) weighted.add(t);
        }
        if (weighted.isEmpty()) return null;
        var t = weighted.get(rng.nextInt(weighted.size()));
        double scale = SCALE[Math.min(4, tier - t.minTier())];
        int need = t.base() <= 1 ? 1 : (int) Math.round(t.base() * scale);
        String target = t.kind().equals("explore") ? pick(DESTINATIONS[t.minTier() - 1], rng) : t.kind().equals("gather") ? "minecraft:" + t.target() : t.target();
        int xp = (int) Math.round(Balance.need(level) * t.diff() * 1.5 * (.75 + .25 * scale));
        int emeralds = 1 + tier + (int) Math.round(t.diff() * 10);
        int friendship = Math.min(25, 4 + (int) Math.round(t.diff() * 20));
        return new Quest(id, t.kind(), target, need, 0, giver, giverName, job, xp, emeralds, friendship, label(t.kind(), target, need));
    }
    private static String pick(String list, Random rng) {
        var all = list.split(" "); var d = all[rng.nextInt(all.length)];
        int colon = d.indexOf(':');
        return d.substring(0, colon + 1) + "minecraft:" + d.substring(colon + 1);
    }
    public static String flavor(String profession, boolean guard, long seed) {
        var pools = pools(profession, guard);
        if (pools.isEmpty()) return "";
        var lines = FLAVOR.get(pools.get(Math.floorMod(seed, pools.size())));
        return lines[(int) Math.floorMod(seed >> 8, lines.length)];
    }

    public static String label(String kind, String target, int need) {
        String name = words(target);
        return switch (kind) {
            case "slay" -> {
                var f = Bestiary.byId(target);
                yield f == null ? "Slay " + need + " " + name : f.boss() ? "Defeat " + f.label() + (need > 1 ? " " + need + " times" : "") : "Slay " + need + " " + f.label();
            }
            case "gather" -> "Bring " + need + " " + name;
            case "mine" -> "Mine " + need + " " + switch (target) { case "ores" -> "ore blocks"; case "stone" -> "stone blocks"; case "logs" -> "logs"; default -> "dirt, sand or gravel"; };
            case "harvest" -> "Harvest " + need + " ripe crops";
            case "fish" -> "Catch " + need + " fish";
            case "breed" -> "Breed " + need + " animals";
            case "enchant" -> "Enchant " + need + " items";
            case "trade" -> "Trade with villagers " + need + " times";
            case "explore" -> target.startsWith("dim:") ? "Set foot in " + (target.endsWith("the_nether") ? "the Nether" : "the End") : "Explore the " + title(name);
            default -> kind + " " + need;
        };
    }
    /** "minecraft:rotten_flesh" or "biome:minecraft:ice_spikes" to "rotten flesh" / "ice spikes". */
    public static String words(String id) { return id.substring(id.lastIndexOf(':') + 1).replace('_', ' '); }
    private static String title(String s) {
        var out = new StringBuilder();
        for (var w : s.split(" ")) out.append(out.isEmpty() ? "" : " ").append(Character.toUpperCase(w.charAt(0))).append(w.substring(1));
        return out.toString();
    }
}
