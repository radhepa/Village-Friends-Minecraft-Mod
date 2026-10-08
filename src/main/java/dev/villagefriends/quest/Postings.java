package dev.villagefriends.quest;

import dev.villagefriends.social.Calendar;
import dev.villagefriends.social.Society;
import dev.villagefriends.social.Townsfolk;
import java.util.*;

/**
 * What residents pin on their village's notice board, and what answering earns. Each morning a board
 * loses the notices nobody took and gains up to two new ones (at least three are up at any time, at most
 * five): monster hunts, things a resident needs for their trade, letters to carry to a neighbor, and
 * surprises for an upcoming birthday. Pure and unit-tested; {@code VillageQuests} applies it to the world.
 */
public final class Postings {
    /** Reads dialogue and item names from the world, so this stays pure. */
    public interface Writer {
        /** A line from a dialogue pool with these placeholders filled, or null when nothing fits. */
        String write(String pool, Map<String, String> fill, Random random);
        /** "iron ingot" for "minecraft:iron_ingot". */
        String itemName(String item);
        /** The item a resident loves most, or "". */
        String loved(String residentId);
    }
    public static final int MIN_OPEN = 3, MAX_OPEN = 5, NEW_PER_DAY = 2, MAX_NOTICES = 14, LIFETIME = 3, HOUSE_LIFETIME = 7;
    /**
     * A household short of room ({@code kind}: "homeless", "crowded" or "newborn"): {@code people} of them and
     * {@code beds} beds between them. {@code poster} is the grown-up who would ask on the board.
     */
    public record HouseNeed(String poster, String kind, int people, int beds) {}

    // -- monsters -----------------------------------------------------------------------------------

    /** A kind of monster to hunt: the entity types that count, how many, and what each is worth in emeralds. */
    public record Hunt(String group, String one, String title, List<String> types, int min, int max, double each, int weight) {}
    public static final List<Hunt> HUNTS = List.of(
            new Hunt("zombies", "zombie", "Zombie trouble", List.of("minecraft:zombie", "minecraft:husk", "minecraft:drowned", "minecraft:zombie_villager"), 4, 8, .8, 30),
            new Hunt("skeletons", "skeleton", "Skeletons about", List.of("minecraft:skeleton", "minecraft:stray", "minecraft:bogged", "minecraft:parched"), 3, 6, 1, 25),
            new Hunt("spiders", "spider", "Spiders in the barn", List.of("minecraft:spider", "minecraft:cave_spider"), 3, 6, .8, 20),
            new Hunt("creepers", "creeper", "Creeper watch", List.of("minecraft:creeper"), 2, 4, 1.5, 15),
            new Hunt("slimes", "slime", "A slimy problem", List.of("minecraft:slime"), 4, 8, .5, 5),
            new Hunt("witches", "witch", "A witch nearby", List.of("minecraft:witch"), 1, 2, 4, 6),
            new Hunt("phantoms", "phantom", "Phantoms at night", List.of("minecraft:phantom"), 1, 3, 3, 6),
            new Hunt("pillagers", "pillager", "Pillager patrols", List.of("minecraft:pillager", "minecraft:vindicator", "minecraft:evoker", "minecraft:illusioner"), 3, 5, 1.8, 6));
    public static Hunt hunt(String group) {
        for (var h : HUNTS) if (h.group().equals(group)) return h;
        return null;
    }
    /** The hunt group an entity type counts toward ("zombies" for a husk), or "". */
    public static String group(String entityType) {
        for (var h : HUNTS) if (h.types().contains(entityType)) return h.group();
        return "";
    }
    static String monster(String group) { var h = hunt(group); return h == null ? group : h.one(); }

    // -- wants and rewards ---------------------------------------------------------------------------

    /** Something a resident asks for: {@code min}-{@code max} of it, worth {@code each} emeralds apiece. */
    public record Want(String item, int min, int max, double each) {}
    /** A thank-you gift: {@code min}-{@code max} of an item. */
    public record Gift(String item, int min, int max) {}
    private static Want w(String item, int min, int max, double each) { return new Want(item.contains(":") ? item : "minecraft:" + item, min, max, each); }
    private static Gift g(String item, int min, int max) { return new Gift(item.contains(":") ? item : "minecraft:" + item, min, max); }
    public static final Map<String, List<Want>> WANTS = Map.ofEntries(
            Map.entry("farmer", List.of(w("wheat", 12, 24, .1), w("carrot", 8, 16, .15), w("potato", 8, 16, .15), w("pumpkin", 3, 6, .5), w("bone_meal", 8, 16, .15), w("beetroot", 8, 14, .15))),
            Map.entry("librarian", List.of(w("paper", 12, 24, .12), w("book", 2, 4, .8), w("ink_sac", 3, 6, .4), w("feather", 4, 8, .2), w("leather", 3, 5, .5))),
            Map.entry("fisherman", List.of(w("cod", 4, 8, .4), w("salmon", 3, 6, .5), w("string", 6, 12, .15), w("kelp", 8, 16, .08))),
            Map.entry("fletcher", List.of(w("stick", 16, 32, .05), w("flint", 6, 10, .25), w("feather", 6, 12, .2), w("string", 6, 12, .15))),
            Map.entry("cleric", List.of(w("rotten_flesh", 8, 16, .08), w("redstone", 8, 16, .15), w("gold_ingot", 2, 4, .9), w("glowstone_dust", 4, 8, .4), w("rabbit_foot", 1, 2, 2))),
            Map.entry("cartographer", List.of(w("paper", 12, 24, .12), w("glass_pane", 6, 12, .2), w("compass", 1, 1, 3), w("ink_sac", 3, 6, .4))),
            Map.entry("armorer", List.of(w("iron_ingot", 4, 8, .6), w("coal", 10, 20, .12), w("lava_bucket", 1, 1, 2), w("diamond", 1, 1, 6))),
            Map.entry("toolsmith", List.of(w("iron_ingot", 3, 6, .6), w("coal", 10, 20, .12), w("flint", 6, 10, .25), w("stick", 16, 32, .05))),
            Map.entry("weaponsmith", List.of(w("iron_ingot", 3, 6, .6), w("coal", 10, 20, .12), w("flint", 6, 10, .25))),
            Map.entry("leatherworker", List.of(w("leather", 4, 8, .5), w("rabbit_hide", 4, 8, .3), w("flint", 4, 8, .25))),
            Map.entry("mason", List.of(w("clay_ball", 8, 16, .15), w("stone", 24, 48, .04), w("andesite", 16, 32, .05), w("quartz", 6, 12, .3))),
            Map.entry("shepherd", List.of(w("white_wool", 6, 12, .25), w("string", 8, 16, .12), w("wheat", 12, 20, .1))),
            Map.entry("butcher", List.of(w("chicken", 4, 8, .3), w("porkchop", 4, 8, .3), w("mutton", 4, 8, .3), w("coal", 10, 16, .12), w("sweet_berries", 10, 20, .08))),
            Map.entry("knight", List.of(w("iron_ingot", 3, 6, .6), w("leather", 3, 6, .5), w("bread", 6, 12, .15), w("coal", 8, 16, .12))),
            Map.entry("archer", List.of(w("arrow", 16, 32, .06), w("string", 6, 12, .15), w("feather", 6, 12, .2), w("flint", 4, 8, .25))),
            Map.entry("cook", List.of(w("egg", 6, 12, .2), w("sugar", 6, 12, .15), w("milk_bucket", 1, 2, .8), w("cocoa_beans", 4, 8, .3), w("brown_mushroom", 4, 8, .2))),
            Map.entry("tavern_keeper", List.of(w("apple", 6, 12, .25), w("sweet_berries", 12, 24, .06), w("honey_bottle", 2, 4, .7), w("glass_bottle", 4, 8, .2), w("cocoa_beans", 4, 8, .3))),
            Map.entry("apothecary", List.of(w("poppy", 4, 8, .15), w("glow_berries", 6, 12, .15), w("honey_bottle", 2, 3, .7), w("glass_bottle", 4, 8, .2), w("spider_eye", 2, 4, .5))),
            Map.entry("painter", List.of(w("red_dye", 4, 8, .2), w("blue_dye", 4, 8, .25), w("yellow_dye", 4, 8, .2), w("paper", 8, 16, .12), w("ink_sac", 3, 6, .4))),
            Map.entry("bard", List.of(w("note_block", 1, 2, 1.5), w("amethyst_shard", 2, 4, .6), w("string", 6, 12, .15), w("bamboo", 8, 16, .08))),
            Map.entry("tailor", List.of(w("white_wool", 6, 12, .25), w("string", 8, 16, .12), w("leather", 3, 6, .5), w("blue_dye", 3, 6, .25))),
            Map.entry("carpenter", List.of(w("oak_log", 16, 32, .1), w("spruce_log", 16, 32, .1), w("stick", 24, 48, .04), w("iron_ingot", 2, 4, .6))),
            Map.entry("scholar", List.of(w("book", 2, 4, .8), w("candle", 2, 4, .5), w("paper", 12, 24, .12), w("glow_ink_sac", 2, 4, .6))),
            Map.entry("nitwit", List.of(w("cookie", 6, 12, .12), w("cake", 1, 1, 2), w("sweet_berries", 8, 16, .08), w("pumpkin_pie", 2, 3, .6))),
            Map.entry("none", List.of(w("bread", 4, 8, .15), w("torch", 12, 24, .05), w("apple", 4, 8, .25), w("coal", 8, 16, .12))));
    public static final List<Want> CHILD_WANTS = List.of(w("dandelion", 1, 3, .5), w("poppy", 1, 3, .5), w("cookie", 3, 6, .25), w("apple", 2, 4, .4),
            w("slime_ball", 1, 2, 1), w("feather", 2, 4, .3), w("cornflower", 1, 2, .6));
    public static final Map<String, List<Gift>> GIFTS = Map.ofEntries(
            Map.entry("farmer", List.of(g("bread", 3, 5), g("pumpkin_pie", 1, 2), g("golden_carrot", 2, 4))),
            Map.entry("librarian", List.of(g("book", 1, 2), g("bookshelf", 1, 1), g("experience_bottle", 2, 3))),
            Map.entry("fisherman", List.of(g("cooked_cod", 3, 5), g("cooked_salmon", 2, 4))),
            Map.entry("fletcher", List.of(g("arrow", 12, 24), g("spectral_arrow", 4, 8))),
            Map.entry("cleric", List.of(g("experience_bottle", 2, 4), g("glowstone_dust", 4, 8))),
            Map.entry("cartographer", List.of(g("map", 1, 1), g("compass", 1, 1))),
            Map.entry("armorer", List.of(g("iron_ingot", 2, 4))),
            Map.entry("toolsmith", List.of(g("iron_ingot", 2, 3), g("coal", 8, 12))),
            Map.entry("weaponsmith", List.of(g("iron_ingot", 2, 3))),
            Map.entry("leatherworker", List.of(g("leather", 3, 6))),
            Map.entry("mason", List.of(g("bricks", 8, 16), g("polished_andesite", 8, 16))),
            Map.entry("shepherd", List.of(g("white_wool", 4, 8), g("white_bed", 1, 1))),
            Map.entry("butcher", List.of(g("cooked_beef", 3, 5), g("cooked_porkchop", 3, 5))),
            Map.entry("knight", List.of(g("shield", 1, 1), g("bread", 3, 5))),
            Map.entry("archer", List.of(g("arrow", 16, 32))),
            Map.entry("cook", List.of(g("villagefriends:hearty_stew", 1, 1), g("villagefriends:fresh_village_bread", 2, 3))),
            Map.entry("tavern_keeper", List.of(g("villagefriends:mug_of_cider", 2, 3))),
            Map.entry("apothecary", List.of(g("villagefriends:bandage_wrap", 1, 2), g("villagefriends:smelling_salts", 1, 1))),
            Map.entry("painter", List.of(g("painting", 1, 2))),
            Map.entry("bard", List.of(g("note_block", 1, 1), g("amethyst_shard", 2, 3))),
            Map.entry("tailor", List.of(g("string", 6, 10), g("white_wool", 4, 6))),
            Map.entry("carpenter", List.of(g("oak_planks", 16, 24), g("chest", 1, 2))),
            Map.entry("scholar", List.of(g("experience_bottle", 2, 4), g("book", 1, 2))),
            Map.entry("nitwit", List.of(g("cookie", 3, 6), g("sweet_berries", 6, 10))),
            Map.entry("none", List.of(g("bread", 2, 3), g("torch", 8, 12))));
    public static final List<Gift> CHILD_GIFTS = List.of(g("cookie", 2, 4), g("apple", 1, 2), g("poppy", 1, 1), g("dandelion", 1, 1));
    /** Something special, now and then, for a notice worth eight emeralds or more. */
    public static final Map<String, Gift> RARE = Map.ofEntries(
            Map.entry("farmer", g("golden_carrot", 6, 8)), Map.entry("librarian", g("experience_bottle", 5, 6)),
            Map.entry("fisherman", g("nautilus_shell", 1, 1)), Map.entry("fletcher", g("spectral_arrow", 12, 16)),
            Map.entry("cleric", g("golden_apple", 1, 1)), Map.entry("cartographer", g("spyglass", 1, 1)),
            Map.entry("armorer", g("diamond", 1, 1)), Map.entry("toolsmith", g("diamond", 1, 1)), Map.entry("weaponsmith", g("diamond", 1, 1)),
            Map.entry("leatherworker", g("saddle", 1, 1)), Map.entry("mason", g("quartz_block", 8, 12)), Map.entry("shepherd", g("name_tag", 1, 1)),
            Map.entry("butcher", g("rabbit_stew", 1, 1)), Map.entry("knight", g("iron_sword", 1, 1)), Map.entry("archer", g("bow", 1, 1)),
            Map.entry("cook", g("cake", 1, 1)), Map.entry("tavern_keeper", g("cake", 1, 1)), Map.entry("apothecary", g("villagefriends:revival_tonic", 1, 1)),
            Map.entry("painter", g("glow_item_frame", 2, 3)), Map.entry("bard", g("music_disc_cat", 1, 1)), Map.entry("tailor", g("villagefriends:rain_cloak", 1, 1)),
            Map.entry("carpenter", g("villagefriends:village_bench", 1, 1)), Map.entry("scholar", g("experience_bottle", 6, 8)),
            Map.entry("nitwit", g("cake", 1, 1)), Map.entry("none", g("cake", 1, 1)));

    // -- the board ----------------------------------------------------------------------------------

    /** The board for {@code today}: stale notices come down and new ones go up, once a day. */
    public static Board refresh(Board board, Society society, long today, Writer writer) { return refresh(board, society, today, writer, List.of()); }
    /**
     * The board for {@code today}, given the households short of room: one of them may ask for a bigger house
     * (at most one such notice is up at a time), and one nobody took comes down once that household has room.
     */
    public static Board refresh(Board board, Society society, long today, Writer writer, List<HouseNeed> needs) {
        if (board.day() >= today) return board;
        var notices = new ArrayList<Notice>();
        for (var n : board.notices()) {
            var poster = society == null ? null : society.get(n.poster());
            boolean gone = poster == null || !poster.home();
            if (n.kind().equals(Notice.HOUSE) && !n.taken() && needs.stream().noneMatch(x -> x.poster().equals(n.poster()))) gone = true;
            if (n.taken() || today < n.expires() && !gone) notices.add(n);
        }
        int open = (int) notices.stream().filter(n -> n.open(today)).count();
        int wanted = board.day() < 0 ? MAX_OPEN - 1 : Math.max(MIN_OPEN - open, Math.min(NEW_PER_DAY, MAX_OPEN - open));
        var random = new Random(seed(board.village(), today));
        int serial = board.serial();
        for (int i = 0, tries = 0; i < wanted && tries < wanted * 4 && notices.size() < MAX_NOTICES && society != null; tries++) {
            var notice = post(society, today, "n" + serial, random, writer, notices);
            if (notice == null) continue;
            notices.add(notice); serial++; i++;
        }
        // A household short of room asks for a bigger house, after the day's other notices so those stay the same.
        if (society != null && notices.size() < MAX_NOTICES && notices.stream().noneMatch(n -> n.kind().equals(Notice.HOUSE))) {
            var notice = house(society, today, "n" + serial, random, writer, needs);
            if (notice != null) { notices.add(notice); serial++; }
        }
        return new Board(board.village(), notices, today, serial, board.favors());
    }
    static long seed(String village, long day) { return village.hashCode() * 0x9E3779B97F4A7C15L + day * 0x632BE59BD9B4E019L; }

    /** One new notice from someone in the village, or null if nobody has anything to ask right now. */
    static Notice post(Society society, long today, String id, Random random, Writer writer, List<Notice> pinned) {
        var busy = new HashSet<String>();
        for (var n : pinned) if (n.open(today)) busy.add(n.poster());
        var people = society.living().stream().filter(t -> t.home() && !busy.contains(t.id())).toList();
        if (people.isEmpty()) return null;
        var birthday = birthdaySurprise(society, today, pinned);
        int roll = random.nextInt(100);
        if (birthday != null && roll < 45) return birthday(society, today, id, random, writer, birthday, busy);
        if (roll < 75) {
            var adults = people.stream().filter(Townsfolk::adult).toList();
            if (!adults.isEmpty() && random.nextInt(100) < 42) return hunt(today, id, random, writer, pick(adults, random, Postings::huntWeight), pinned);
            if (!adults.isEmpty() && random.nextInt(100) < 25) { var letter = letter(society, today, id, random, writer, adults, pinned); if (letter != null) return letter; }
        }
        return fetch(today, id, random, writer, people.get(random.nextInt(people.size())), pinned);
    }
    private static int huntWeight(Townsfolk t) {
        int w = switch (t.job()) { case "knight", "archer" -> 5; case "farmer", "shepherd", "butcher", "fletcher", "cleric" -> 2; default -> 1; };
        return t.personality().equals("protective") || t.personality().equals("steadfast") ? w * 2 : w;
    }
    private static <T> T pick(List<T> list, Random random, java.util.function.ToIntFunction<T> weight) {
        int total = 0;
        for (var t : list) total += Math.max(1, weight.applyAsInt(t));
        int roll = random.nextInt(total);
        for (var t : list) { roll -= Math.max(1, weight.applyAsInt(t)); if (roll < 0) return t; }
        return list.getLast();
    }
    private static String first(String name) { int space = name.indexOf(' '); return space > 0 ? name.substring(0, space) : name; }
    private static String job(String job) { return job.equals("none") ? "neighbor" : job.equals("nitwit") ? "free spirit" : job.replace('_', ' '); }
    private static Map<String, String> fill(Townsfolk poster) {
        var fill = new HashMap<String, String>();
        fill.put("name", first(poster.name())); fill.put("job", job(poster.job()));
        return fill;
    }
    private static String write(Writer writer, Random random, String pool, String fallbackPool, Map<String, String> fill, String fallback) {
        String text = writer.write(pool, fill, random);
        if (text == null && fallbackPool != null) text = writer.write(fallbackPool, fill, random);
        return text == null ? fallback : text;
    }
    private static Notice.Reward reward(int emeralds, String job, boolean child, Random random) {
        var gifts = child ? CHILD_GIFTS : GIFTS.getOrDefault(job, GIFTS.get("none"));
        var gift = gifts.get(random.nextInt(gifts.size()));
        if (!child && emeralds >= 8 && random.nextInt(100) < 35) gift = RARE.getOrDefault(job, gift);
        return new Notice.Reward(emeralds, gift.item(), gift.min() + random.nextInt(gift.max() - gift.min() + 1));
    }

    static Notice hunt(long today, String id, Random random, Writer writer, Townsfolk poster, List<Notice> pinned) {
        var taken = new HashSet<String>();
        for (var n : pinned) if (n.kind().equals(Notice.HUNT) && n.open(today)) taken.add(n.target());
        var choices = HUNTS.stream().filter(h -> !taken.contains(h.group())).toList();
        if (choices.isEmpty()) return null;
        var h = pick(choices, random, x -> x.weight() * (switch (poster.job()) {
            case "knight", "archer" -> x.group().equals("pillagers") || x.group().equals("witches") ? 3 : 1;
            case "fletcher" -> x.group().equals("skeletons") ? 3 : 1;
            case "shepherd" -> x.group().equals("spiders") ? 3 : 1;
            case "cleric" -> x.group().equals("zombies") ? 2 : 1;
            default -> 1;
        }));
        int count = h.min() + random.nextInt(h.max() - h.min() + 1);
        int emeralds = (int) Math.clamp(Math.round(count * h.each()) + 1, 2, 16);
        var fill = fill(poster); fill.put("mobs", Words.mobs(count, h.group()));
        String text = write(writer, random, "notice.hunt." + h.group(), null, fill, "Could someone deal with " + fill.get("mobs") + "? They've been bothering the village at night.");
        return new Notice(id, Notice.HUNT, poster.id(), poster.name(), poster.job(), h.group(), count, "", "", reward(emeralds, poster.job(), false, random),
                h.title(), text, today, today + LIFETIME, "");
    }
    static Notice fetch(long today, String id, Random random, Writer writer, Townsfolk poster, List<Notice> pinned) {
        var wants = poster.adult() ? WANTS.getOrDefault(poster.job(), WANTS.get("none")) : CHILD_WANTS;
        var taken = new HashSet<String>();
        for (var n : pinned) if (n.open(today)) taken.add(n.target());
        var choices = wants.stream().filter(x -> !taken.contains(x.item())).toList();
        if (choices.isEmpty()) return null;
        var want = choices.get(random.nextInt(choices.size()));
        int count = want.min() + random.nextInt(want.max() - want.min() + 1);
        int emeralds = (int) Math.clamp(Math.round(count * want.each()) + 1, poster.adult() ? 2 : 1, 12);
        String name = writer.itemName(want.item());
        var fill = fill(poster); fill.put("wanted", Words.count(count, name));
        String pool = poster.adult() ? "notice.fetch." + poster.job() : "notice.fetch.child";
        String text = write(writer, random, pool, "notice.fetch.general", fill, "Looking for " + fill.get("wanted") + ". I'll make it worth your while.");
        String title = "Wanted: " + Words.count(count, name);
        return new Notice(id, Notice.FETCH, poster.id(), poster.name(), poster.job(), want.item(), count, "", "", reward(emeralds, poster.job(), !poster.adult(), random),
                title, text, today, today + LIFETIME, "");
    }
    /** Someone to write to: a sweetheart, family, a best friend, a secret crush, or a neighbor they quarreled with. */
    static Notice letter(Society society, long today, String id, Random random, Writer writer, List<Townsfolk> adults, List<Notice> pinned) {
        var order = new ArrayList<>(adults);
        Collections.shuffle(order, random);
        for (var poster : order) {
            var options = new ArrayList<String[]>();
            if (!poster.partner().isEmpty()) options.add(new String[]{poster.partner(), "partner"});
            for (String relative : society.family(poster.id())) if (!relative.equals(poster.partner())) { options.add(new String[]{relative, "family"}); break; }
            String friend = society.bestFriend(poster.id(), today);
            if (!friend.isEmpty()) options.add(new String[]{friend, "friend"});
            String crush = society.crush(poster.id(), today);
            if (!crush.isEmpty()) options.add(new String[]{crush, "crush"});
            for (var other : society.living()) {
                var tie = society.tie(poster.id(), other.id());
                if (!other.id().equals(poster.id()) && tie.quarrel() >= 0 && today - tie.quarrel() <= 20) { options.add(new String[]{other.id(), "apology"}); break; }
            }
            options.removeIf(o -> { var t = society.get(o[0]); return t == null || !t.home() || pinned.stream().anyMatch(n -> n.kind().equals(Notice.LETTER) && n.target().equals(o[0]) && n.poster().equals(poster.id())); });
            if (options.isEmpty()) continue;
            var choice = options.get(random.nextInt(options.size()));
            String recipient = society.nameOf(choice[0]);
            var fill = fill(poster); fill.put("recipient", first(recipient));
            String text = write(writer, random, "notice.letter." + choice[1], null, fill, "Could you carry a letter to " + first(recipient) + " for me? It's sealed, so no peeking.");
            return new Notice(id, Notice.LETTER, poster.id(), poster.name(), poster.job(), choice[0], 1, choice[1], recipient,
                    reward(2 + random.nextInt(3), poster.job(), false, random), "A letter for " + first(recipient), text, today, today + LIFETIME, "");
        }
        return null;
    }
    /** A resident whose birthday is one to four days away and nobody is planning a surprise for yet. */
    static Townsfolk birthdaySurprise(Society society, long today, List<Notice> pinned) {
        for (var t : society.birthdays(today, 64)) {
            int until = Calendar.daysUntil(t.birthday(), today);
            if (until < 1) continue;
            if (until > 4) break;
            if (pinned.stream().noneMatch(n -> n.kind().equals(Notice.BIRTHDAY) && n.about().equals(t.id()))) return t;
        }
        return null;
    }
    static Notice birthday(Society society, long today, String id, Random random, Writer writer, Townsfolk celebrant, Set<String> busy) {
        // Their sweetheart plans it if they have one, then family, then their closest friend.
        Townsfolk poster = null;
        var planners = new ArrayList<String>();
        if (!celebrant.partner().isEmpty()) planners.add(celebrant.partner());
        planners.addAll(society.family(celebrant.id()));
        String friend = society.bestFriend(celebrant.id(), today);
        if (!friend.isEmpty()) planners.add(friend);
        for (String p : planners) { var t = society.get(p); if (t != null && t.home() && t.adult() && !busy.contains(p)) { poster = t; break; } }
        if (poster == null) return null;
        String loved = writer.loved(celebrant.id());
        boolean cake = loved.isEmpty() || random.nextBoolean();
        String item = cake ? "minecraft:cake" : loved;
        int count = cake ? 1 : 1 + random.nextInt(3);
        int until = Calendar.daysUntil(celebrant.birthday(), today);
        var fill = fill(poster);
        fill.put("celebrant", first(celebrant.name())); fill.put("wanted", Words.count(count, writer.itemName(item)));
        fill.put("when", Calendar.when(until)); fill.put("birthday", Calendar.birthdayDate(celebrant.birthday()));
        String text = write(writer, random, "notice.birthday", null, fill, first(celebrant.name()) + "'s birthday is " + fill.get("when") + ". Could you help me surprise them with " + fill.get("wanted") + "?");
        return new Notice(id, Notice.BIRTHDAY, poster.id(), poster.name(), poster.job(), item, count, celebrant.id(), celebrant.name(),
                reward(3 + random.nextInt(3), poster.job(), false, random), "Surprise for " + first(celebrant.name()), text, today, today + Math.min(LIFETIME, until + 1), "");
    }

    /** "We need a bigger house": build one with enough beds and put up a House Plaque. Null when nobody needs one. */
    static Notice house(Society society, long today, String id, Random random, Writer writer, List<HouseNeed> needs) {
        for (var need : needs) {
            var poster = society.get(need.poster());
            if (poster == null || !poster.home() || !poster.adult()) continue;
            int beds = Math.max(2, need.people());
            var fill = fill(poster);
            fill.put("count", Integer.toString(beds)); fill.put("people", Integer.toString(need.people()));
            String fallback = switch (need.kind()) {
                case "newborn" -> "Our family has grown, and there's no bed for the baby. Could someone build us a house with " + beds + " beds?";
                case "homeless" -> "I have no home of my own here. If someone could build a little house with a bed, I'd be so grateful.";
                default -> "We need a bigger house! There are " + need.people() + " of us and only " + need.beds() + (need.beds() == 1 ? " bed" : " beds") + ". Could someone build us one?";
            };
            String text = write(writer, random, "notice.house." + need.kind(), "notice.house", fill, fallback);
            int emeralds = 6 + Math.min(6, beds);
            var gifts = GIFTS.get("carpenter");
            var gift = gifts.get(random.nextInt(gifts.size()));
            var reward = new Notice.Reward(emeralds, gift.item(), gift.min() + random.nextInt(gift.max() - gift.min() + 1));
            return new Notice(id, Notice.HOUSE, poster.id(), poster.name(), poster.job(), poster.id(), beds, need.kind(), poster.name(), reward,
                    "We need a bigger house", text, today, today + HOUSE_LIFETIME, "");
        }
        return null;
    }

    private Postings() {}
}
