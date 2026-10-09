package dev.villagefriends.hearth;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;

/**
 * What residents like to eat, pure and unit-tested: each resident's favorite dish and the family recipe
 * they hand a good friend, what they eat at home today, the cake at their birthday party, the tavern's
 * menu, what a dish is worth as a gift, and how long Well Fed lasts. Everything is decided from a resident's
 * id, personality and job, so it never needs saving and never changes.
 */
public final class Tastes {
    /** Friendship level at which a resident hands over their family recipe (Friend). */
    public static final int RECIPE_LEVEL = 4;

    /** Who someone is, as far as their tastes go. */
    public record Eater(String id, String personality, String job, boolean child) {}

    /** How much a resident's personality, job and age pull towards a dish. */
    static double appetite(Eater e, Dish d) {
        // Anything can be a favorite, but what suits their personality, job or age is far likelier.
        double w = .2;
        if (d.likes().contains(e.personality())) w += 4;
        if (d.likes().contains(e.job())) w += 4;
        if (d.likes().contains("child")) w += e.child() ? 6 : 0;
        else if (e.child()) w *= .25;
        return w;
    }
    /** A dish every installation has: nothing that needs another mod. */
    private static boolean everywhere(Dish d) { return d.needs() == null; }

    /** Their favorite dish: one of the dishes their personality, job or age likes most, the same every time. */
    public static Dish favorite(Eater e, Collection<Dish> dishes) {
        var pool = dishes.stream().filter(Dish::dish).filter(Tastes::everywhere).sorted(Comparator.comparing(Dish::id)).toList();
        return weighted(pool, d -> appetite(e, d), seed(e.id(), 0x0F00D));
    }
    /** The family recipe they share at {@link #RECIPE_LEVEL}: a secret dish that suits them. */
    public static Dish familyRecipe(Eater e, Collection<Dish> dishes) {
        var pool = dishes.stream().filter(Dish::dish).filter(Dish::secret).filter(Tastes::everywhere).sorted(Comparator.comparing(Dish::id)).toList();
        return weighted(pool, d -> appetite(e, d), seed(e.id(), 0xFA417));
    }
    /** What they eat at home for this meal ("breakfast", "lunch" or "supper") today: now and then their favorite. */
    public static Dish homeMeal(Eater e, String meal, long day, Collection<Dish> dishes) {
        var pool = dishes.stream().filter(Dish::dish).filter(Tastes::everywhere).filter(d -> d.meal(meal))
                .sorted(Comparator.comparing(Dish::id)).toList();
        if (pool.isEmpty()) return null;
        long s = seed(e.id(), meal.hashCode() * 31L + day);
        var favorite = favorite(e, dishes);
        if (favorite != null && favorite.meal(meal) && Math.floorMod(s, 5) == 0) return favorite;
        return weighted(pool, d -> appetite(e, d), s >>> 3);
    }
    /** The cake at their birthday party: their favorite if it's a cake, otherwise one that suits them. */
    public static Dish partyCake(Eater e, Collection<Dish> dishes) {
        var favorite = favorite(e, dishes);
        if (favorite != null && favorite.cake()) return favorite;
        var cakes = dishes.stream().filter(Dish::cake).filter(Tastes::everywhere).sorted(Comparator.comparing(Dish::id)).toList();
        return weighted(cakes, d -> appetite(e, d) + (d.secret() ? 2 : 0), seed(e.id(), 0xCA4E));
    }
    /** The cook's dishes for the tavern, in the order they come round (see {@code Patronage}). */
    public static List<String> tavernMenu(Collection<Dish> dishes) {
        var menu = new ArrayList<String>();
        var pool = dishes.stream().filter(Dish::dish).filter(Tastes::everywhere).filter(d -> d.meal("tavern"))
                .sorted(Comparator.comparing(Dish::id)).toList();
        // Spread the kinds out so stews, pies and breads take turns instead of running in alphabetical clumps.
        var kinds = pool.stream().map(Dish::serve).distinct().sorted().toList();
        int longest = kinds.stream().mapToInt(k -> (int) pool.stream().filter(d -> d.serve().equals(k)).count()).max().orElse(0);
        for (int i = 0; i < longest; i++)
            for (var k : kinds) {
                var ofKind = pool.stream().filter(d -> d.serve().equals(k)).toList();
                if (i < ofKind.size()) menu.add(ofKind.get(i).id());
            }
        return menu;
    }

    /** Friendship points for a dish as a gift. A favorite beats everything; a fine dish is worth a little more. */
    public static int giftValue(Dish dish, boolean favorite, boolean fine, boolean child) {
        if (dish == null || !dish.dish()) return 0;
        int value = favorite ? 18 : 6 + 2 * dish.tier() + (child && dish.likes().contains("child") ? 4 : 0);
        return value + (fine ? 2 : 0);
    }

    // -- Well Fed ----------------------------------------------------------------------------------

    /** A fine dish's Well Fed lasts this much longer. */
    public static final double FINE_DURATION = 1.5;
    /** Well Fed I-III: hunger drains this much slower. */
    public static final double[] HUNGER = {.15, .25, .35};
    /** Well Fed II and III mend half a heart this often (ticks); I doesn't. */
    public static final int[] MEND_EVERY = {0, 240, 160};

    /** Seconds of Well Fed from eating a dish: its table time, longer if fine, times any bonus (the RPG Cooking skill). */
    public static int wellFedSeconds(Dish dish, boolean fine, double bonus) {
        if (dish == null || !dish.dish()) return 0;
        return (int) Math.round(dish.buff() * (fine ? FINE_DURATION : 1) * Math.max(0, bonus));
    }
    public static double hungerFactor(int amplifier) { return 1 - HUNGER[Math.clamp(amplifier, 0, 2)]; }

    // -- helpers -----------------------------------------------------------------------------------

    private interface Weight<T> { double of(T t); }
    private static <T> T weighted(List<T> pool, Weight<T> weight, long seed) {
        if (pool.isEmpty()) return null;
        double total = 0;
        for (var t : pool) total += weight.of(t);
        double roll = (Math.floorMod(seed, 1_000_003L) / 1_000_003.0) * total;
        for (var t : pool) { roll -= weight.of(t); if (roll < 0) return t; }
        return pool.getLast();
    }
    static long seed(String id, long salt) {
        long h = 1125899906842597L ^ salt;
        for (char c : id.toLowerCase(Locale.ROOT).toCharArray()) h = 31 * h + c;
        h ^= h >>> 33; h *= 0xff51afd7ed558ccdL; h ^= h >>> 33; h *= 0xc4ceb9fe1a85ec53L; h ^= h >>> 33;
        return h;
    }

    private Tastes() {}
}
