package dev.villagefriends.pet;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Random;
import java.util.UUID;

/**
 * Everything about keeping a pet that doesn't need a world: which residents long for a cat or a dog,
 * what pets are called, their personalities, favorite games and treats, how old they look and what
 * the pet card says about them. Pure and deterministic where it matters, so it is unit-tested.
 */
public final class PetKeeping {
    public static final String CAT = "cat", DOG = "dog";
    public static final int MAX_FONDNESS = 100;

    // -- who wants a pet ---------------------------------------------------------------------------

    /** The chance a resident of this personality wants a pet at all, and the share of those who'd pick a dog. */
    private record Longing(double wants, double dog) {}
    private static final Map<String, Longing> LONGING = Map.ofEntries(
            Map.entry("warmhearted", new Longing(.55, .5)), Map.entry("gentle", new Longing(.6, .3)),
            Map.entry("playful", new Longing(.55, .65)), Map.entry("adventurous", new Longing(.5, .8)),
            Map.entry("protective", new Longing(.5, .85)), Map.entry("steadfast", new Longing(.45, .7)),
            Map.entry("curious", new Longing(.45, .45)), Map.entry("imaginative", new Longing(.45, .3)),
            Map.entry("thoughtful", new Longing(.4, .2)), Map.entry("reserved", new Longing(.3, .25)),
            Map.entry("meticulous", new Longing(.25, .3)), Map.entry("pragmatic", new Longing(.3, .6)));

    /** "cat", "dog", or "" for residents who would rather not keep a pet. Fixed for each resident. */
    public static String wish(UUID resident, String personality, boolean child) {
        var longing = LONGING.getOrDefault(personality, new Longing(.4, .5));
        var random = new Random(resident.getMostSignificantBits() * 31 + resident.getLeastSignificantBits() ^ 0x9E7L);
        double roll = random.nextDouble(), pick = random.nextDouble();
        if (roll >= longing.wants() * (child ? .9 : 1)) return "";
        return pick < longing.dog() ? DOG : CAT;
    }

    // -- names -------------------------------------------------------------------------------------

    static final List<String> CAT_NAMES = List.of("Biscuit", "Mittens", "Thistle", "Clover", "Juniper", "Nutmeg", "Pip", "Sage",
            "Moss", "Fennel", "Tansy", "Wren", "Sorrel", "Hazel", "Saffron", "Marigold", "Puddle", "Soot", "Ember", "Cinder",
            "Muffin", "Crumpet", "Dumpling", "Quill", "Button", "Thimble", "Bobbin", "Socks", "Tuppence", "Farthing", "Penny",
            "Ginger", "Treacle", "Toffee", "Fudge", "Honey", "Turnip", "Acorn", "Pebble", "Magpie", "Nettle", "Fern", "Willow",
            "Rowan", "Basil", "Mouse", "Inkwell", "Smudge", "Whisker", "Velvet", "Plum", "Damson", "Tibbles", "Marmalade",
            "Duchess", "Sir Pounce", "Lady Fluff", "Mustard", "Bramble", "Snowdrop");
    static final List<String> DOG_NAMES = List.of("Rufus", "Bran", "Barnaby", "Duke", "Bear", "Bosun", "Captain", "Gruff", "Hob",
            "Jasper", "Kip", "Lark", "Mabel", "Ned", "Otto", "Patch", "Rascal", "Scout", "Tuck", "Barley", "Brandy", "Bruno",
            "Buckle", "Chester", "Conker", "Dash", "Fletcher", "Gus", "Hamish", "Hector", "Juno", "Maple", "Merry", "Moose",
            "Mungo", "Nell", "Oakley", "Pippin", "Pudding", "Quince", "Rolo", "Rosie", "Sable", "Samson", "Shadow", "Skipper",
            "Taffy", "Teasel", "Thatch", "Tilly", "Toby", "Trusty", "Winnie", "Biscuit", "Pepper", "Clover", "Boots", "Acorn",
            "Bramble", "Sorrel");

    public static String name(Random random, String species) {
        var names = species.equals(CAT) ? CAT_NAMES : DOG_NAMES;
        return names.get(random.nextInt(names.size()));
    }

    // -- personalities, games and treats -----------------------------------------------------------

    /** A pet personality: how often they want to play and which games they like best (by weight). */
    public record Nature(String id, String label, double playfulness, Map<String, Integer> games) {}
    private static final List<Nature> DOG_NATURES = List.of(
            new Nature("playful", "Playful", 1.4, Map.of("fetch", 2, "chase", 2, "spin", 2, "belly_rub", 1, "beg", 1, "shake_paw", 1)),
            new Nature("lazy", "Lazy", .6, Map.of("belly_rub", 4, "beg", 2, "shake_paw", 1, "fetch", 1)),
            new Nature("curious", "Curious", 1.0, Map.of("fetch", 3, "spin", 2, "beg", 1, "chase", 1)),
            new Nature("cuddly", "Cuddly", 1.2, Map.of("belly_rub", 4, "shake_paw", 2, "beg", 1, "fetch", 1)),
            new Nature("proud", "Proud", .8, Map.of("shake_paw", 3, "spin", 3, "fetch", 1)),
            new Nature("shy", "Shy", .7, Map.of("beg", 2, "shake_paw", 2, "belly_rub", 2)),
            new Nature("zoomy", "Zoomy", 1.6, Map.of("fetch", 3, "chase", 3, "spin", 1)),
            new Nature("foodie", "Food-loving", 1.0, Map.of("beg", 4, "shake_paw", 2, "fetch", 1)),
            new Nature("loyal", "Loyal", 1.2, Map.of("fetch", 2, "shake_paw", 2, "belly_rub", 2, "chase", 1)),
            new Nature("brave", "Brave", 1.1, Map.of("chase", 3, "fetch", 2, "spin", 1)));
    private static final List<Nature> CAT_NATURES = List.of(
            new Nature("playful", "Playful", 1.4, Map.of("string", 2, "feather", 2, "weave", 1, "treat", 1, "chin_scratch", 1)),
            new Nature("lazy", "Lazy", .6, Map.of("stroke", 4, "chin_scratch", 2, "treat", 1)),
            new Nature("curious", "Curious", 1.0, Map.of("string", 3, "feather", 2, "treat", 1)),
            new Nature("cuddly", "Cuddly", 1.2, Map.of("stroke", 3, "chin_scratch", 3, "weave", 2)),
            new Nature("proud", "Proud", .8, Map.of("weave", 2, "treat", 2, "chin_scratch", 1)),
            new Nature("shy", "Shy", .7, Map.of("chin_scratch", 3, "treat", 2, "stroke", 1)),
            new Nature("zoomy", "Zoomy", 1.6, Map.of("feather", 3, "string", 2, "weave", 1)),
            new Nature("foodie", "Food-loving", 1.0, Map.of("treat", 4, "weave", 2, "chin_scratch", 1)),
            new Nature("aloof", "Aloof", .5, Map.of("weave", 2, "chin_scratch", 1, "treat", 1)),
            new Nature("mischievous", "Mischievous", 1.3, Map.of("string", 3, "feather", 3, "weave", 1)));
    public static final List<String> DOG_GAMES = List.of("fetch", "belly_rub", "beg", "shake_paw", "spin", "chase");
    public static final List<String> CAT_GAMES = List.of("string", "stroke", "chin_scratch", "feather", "treat", "weave");

    public static List<Nature> natures(String species) { return species.equals(CAT) ? CAT_NATURES : DOG_NATURES; }
    public static Nature nature(String species, String id) {
        for (var n : natures(species)) if (n.id().equals(id)) return n;
        return natures(species).getFirst();
    }
    public static List<String> games(String species) { return species.equals(CAT) ? CAT_GAMES : DOG_GAMES; }
    public static String gameLabel(String game) {
        return switch (game) {
            case "fetch" -> "Fetch"; case "belly_rub" -> "Belly rubs"; case "beg" -> "Begging for treats";
            case "shake_paw" -> "Shaking paws"; case "spin" -> "Spinning in circles"; case "chase" -> "A good chase";
            case "string" -> "Batting at string"; case "stroke" -> "Long strokes"; case "chin_scratch" -> "Chin scratches";
            case "feather" -> "Chasing a feather"; case "treat" -> "Treat time"; case "weave" -> "Weaving round ankles";
            default -> game.replace('_', ' ');
        };
    }
    static final List<String> DOG_TREATS = List.of("minecraft:cooked_beef", "minecraft:cooked_porkchop", "minecraft:cooked_chicken",
            "minecraft:cooked_mutton", "minecraft:cooked_rabbit", "minecraft:beef");
    static final List<String> CAT_TREATS = List.of("minecraft:cod", "minecraft:salmon");
    public static String treatLabel(String item) {
        return switch (item) {
            case "minecraft:cooked_beef" -> "Steak"; case "minecraft:cooked_porkchop" -> "Pork chops";
            case "minecraft:cooked_chicken" -> "Roast chicken"; case "minecraft:cooked_mutton" -> "Mutton";
            case "minecraft:cooked_rabbit" -> "Rabbit stew meat"; case "minecraft:beef" -> "Raw beef";
            case "minecraft:cod" -> "Fresh cod"; case "minecraft:salmon" -> "Fresh salmon";
            default -> item.substring(item.indexOf(':') + 1).replace('_', ' ');
        };
    }
    /** What a resident lures a stray with: a bone for a dog, a fish for a cat. */
    public static String lure(String species) { return species.equals(CAT) ? "minecraft:cod" : "minecraft:bone"; }

    /** A brand-new pet's identity, adopted today by the resident with this id. Strays are guessed to be a few weeks old or more. */
    public static PetProfile newProfile(Random random, String species, String residentId, String residentName, long today, boolean baby) {
        var nature = natures(species).get(random.nextInt(natures(species).size()));
        String game = weighted(random, nature.games(), games(species));
        var treats = species.equals(CAT) ? CAT_TREATS : DOG_TREATS;
        long born = baby ? today : today - (20 + random.nextInt(180));
        return new PetProfile(residentId, residentName, name(random, species), species, nature.id(), game,
                treats.get(random.nextInt(treats.size())), born, today, "", Map.of());
    }

    /** Which game a resident and their pet play now: the pet's favorite comes up most, then what their nature enjoys. */
    public static String pickGame(Random random, PetProfile pet, List<String> possible) {
        var weights = new java.util.LinkedHashMap<String, Integer>();
        var nature = nature(pet.species(), pet.personality());
        for (String game : possible) {
            int w = 1 + nature.games().getOrDefault(game, 0);
            if (game.equals(pet.game())) w += 4;
            weights.put(game, w);
        }
        return weighted(random, weights, possible);
    }
    private static String weighted(Random random, Map<String, Integer> weights, List<String> fallback) {
        int total = 0;
        for (String game : fallback) total += weights.getOrDefault(game, 0);
        if (total <= 0) return fallback.get(random.nextInt(fallback.size()));
        int roll = random.nextInt(total);
        for (String game : fallback) { roll -= weights.getOrDefault(game, 0); if (roll < 0) return game; }
        return fallback.getLast();
    }

    /** Ticks until a resident and their pet play again: lively pets and playful residents play more often. */
    public static int playPause(Random random, PetProfile pet, String residentPersonality) {
        double rate = nature(pet.species(), pet.personality()).playfulness();
        if (residentPersonality.equals("playful") || residentPersonality.equals("warmhearted")) rate *= 1.25;
        if (residentPersonality.equals("reserved") || residentPersonality.equals("meticulous")) rate *= .8;
        return (int) ((1400 + random.nextInt(2200)) / rate);
    }

    // -- age ---------------------------------------------------------------------------------------

    public static String stage(String species, boolean baby, long ageDays) {
        if (baby) return species.equals(CAT) ? "Kitten" : "Puppy";
        if (ageDays < 20) return "Young " + species;
        if (ageDays < 200) return "Grown " + species;
        return "Old-timer";
    }
    public static String age(long ageDays) {
        if (ageDays <= 0) return "born today";
        return ageDays == 1 ? "1 day old" : ageDays + " days old";
    }

    // -- fondness ----------------------------------------------------------------------------------

    public static String fondnessLabel(int points) {
        if (points >= 90) return "Adores you";
        if (points >= 60) return "Fond of you";
        if (points >= 30) return "Friendly with you";
        if (points >= 10) return "Curious about you";
        return "Wary of you";
    }

    // -- what the pet card says --------------------------------------------------------------------

    private static final Map<String, String> NATURE_LINES = Map.ofEntries(
            Map.entry("lazy", "{name} opens one eye, sees it's only you, and goes back to resting."),
            Map.entry("zoomy", "{name} can't keep still. They've done three laps around you already."),
            Map.entry("shy", "{name} peeks out from behind {owner}, curious but careful."),
            Map.entry("foodie", "{name} stares at your hands. Then at your bag. Then at your hands again."),
            Map.entry("proud", "{name} sits up very straight and lets you admire them."),
            Map.entry("cuddly", "{name} presses their head into your palm before you've even offered it."),
            Map.entry("curious", "{name} is very interested in your boots. Where have they been?"),
            Map.entry("playful", "{name} bounces on the spot, ready for any game you can think of."),
            Map.entry("loyal", "{name} keeps one eye on you and one on {owner}, always."),
            Map.entry("brave", "{name} stands tall beside {owner}, ears up, keeping watch."),
            Map.entry("aloof", "{name} allows you to look at them. Briefly."),
            Map.entry("mischievous", "{name} has the look of a cat who has just knocked something off a shelf."));
    private static final List<String> CAT_LINES = List.of(
            "{name} blinks slowly at you. In cat, that's a compliment.",
            "{name} sniffs your fingers, decides you'll do, and sits on your boot.",
            "{name} watches you through half-closed eyes, tail flicking now and then.",
            "{name} winds once around your ankles and pretends it was an accident.",
            "{name} meows at you, then looks over at {owner} as if to ask who let you in.",
            "{name} is pretending not to care that you're here. The tail says otherwise.");
    private static final List<String> DOG_LINES = List.of(
            "{name} wags so hard that the whole back half of them wags too.",
            "{name} drops into a play bow, then looks up at you hopefully.",
            "{name} sniffs your pockets very thoroughly. Strictly business.",
            "{name} leans their whole weight against your legs and sighs happily.",
            "{name} barks once, then glances back at {owner} to check that was allowed.",
            "{name} tilts their head at you, ears up, waiting to see what you'll do.");

    /** The opening line on a pet's card. */
    public static String greeting(Random random, PetProfile pet) {
        String line;
        if (!pet.owned()) line = pet.former().isEmpty()
                ? "{name} has no home yet. They look at you, then at the village, hopefully."
                : "{name} still waits by " + pet.former() + "'s door sometimes, hoping.";
        else if (random.nextInt(3) == 0 && NATURE_LINES.containsKey(pet.personality())) line = NATURE_LINES.get(pet.personality());
        else { var lines = pet.cat() ? CAT_LINES : DOG_LINES; line = lines.get(random.nextInt(lines.size())); }
        return fill(line, pet);
    }
    public static String patLine(Random random, PetProfile pet, boolean first) {
        if (!first) return fill(pet.cat() ? "{name} purrs again. It's still a very good scratch." : "{name} is always happy for more pats.", pet);
        var lines = pet.cat()
                ? List.of("{name} pushes up into your hand and starts to purr.", "{name} purrs like a little kettle.", "{name} leans into the scratch, eyes closed.")
                : List.of("{name}'s tail goes wild. Best. Pat. Ever.", "{name} rolls over for a belly rub, just in case.", "{name} licks your hand and grins.");
        return fill(lines.get(random.nextInt(lines.size())), pet);
    }
    public static String treatLine(PetProfile pet, String item, boolean first) { return treatLine(pet, item, first, null); }
    /** {@code fish} is the fish's name when the treat is a fish: cats and dogs love fish. */
    public static String treatLine(PetProfile pet, String item, boolean first, String fish) {
        if (!first) return fill("{name} happily eats it, though they've already had a treat from you today.", pet);
        if (item.equals(pet.treat())) return fill(treatLabel(item) + "! {name}'s favorite. Gone in three bites, and they look up for more.", pet);
        String a = fish == null || fish.isEmpty() || "aeiou".indexOf(fish.charAt(0)) < 0 ? "A " : "An ";
        if (fish != null) return fill(pet.cat() ? a + fish + "! {name} purrs so loudly the whole street can hear, and eats every scrap."
                : a + fish + "! {name} wolfs it down, tail going like a windmill, and licks your fingers clean.", pet);
        return fill("{name} gobbles it up and gives you a grateful look.", pet);
    }
    public static String refusedLine(PetProfile pet, boolean emptyHand) {
        if (emptyHand) return "Hold a treat in your main hand first: fish for cats, meat or fish for dogs.";
        return fill(pet.cat() ? "{name} sniffs it and turns away. Cats would rather have fish." : "{name} sniffs it politely. Dogs would rather have meat or fish.", pet);
    }
    static String fill(String line, PetProfile pet) {
        return line.replace("{name}", pet.name()).replace("{owner}", pet.ownerName().isEmpty() ? "the village" : pet.ownerName());
    }

    /** A collar color that suits the resident: warm reds for the warmhearted, blues for the thoughtful... */
    public static String collar(Random random, String residentPersonality) {
        var colors = switch (residentPersonality) {
            case "warmhearted", "protective" -> List.of("red", "orange");
            case "gentle", "imaginative" -> List.of("pink", "magenta", "light_blue");
            case "playful" -> List.of("yellow", "lime", "orange");
            case "adventurous", "steadfast" -> List.of("green", "brown");
            case "thoughtful", "reserved" -> List.of("blue", "purple", "cyan");
            default -> List.of("red", "blue", "green", "yellow", "purple", "cyan");
        };
        return colors.get(random.nextInt(colors.size()));
    }

    /** Lower-case display of a vanilla variant id, "minecraft:british_shorthair" to "British shorthair". */
    public static String breed(String variantId) {
        String path = variantId.substring(variantId.indexOf(':') + 1).replace('_', ' ');
        if (path.equals("all black")) path = "black";
        if (path.equals("jellie")) path = "Jellie";
        return path.isEmpty() ? "" : path.substring(0, 1).toUpperCase(Locale.ROOT) + path.substring(1);
    }

    static List<String> allNames() { var all = new ArrayList<>(CAT_NAMES); all.addAll(DOG_NAMES); return all; }
    private PetKeeping() {}
}
