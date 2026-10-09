package dev.villagefriends.hearth;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Predicate;

/**
 * Every station recipe, and how a grid of ingredients matches one. Pure: the world hands it {@link Slot}
 * views of the station's items. Data-pack recipes are replaced on every reload; recipes added from code
 * with {@link #register} stay.
 */
public final class Cookbook {
    /** What a station slot holds, as the cookbook sees it. */
    public interface Slot {
        boolean isEmpty();
        String item();
        /** Whether the item is in this tag ({@code namespace:path}, without the #). */
        boolean is(String tag);
    }

    private static final Map<String, CookingRecipe> DATA = new LinkedHashMap<>(), CODE = new LinkedHashMap<>();

    /** Replaces the data-pack recipes (called on every data pack reload). */
    public static synchronized void load(Collection<CookingRecipe> recipes) {
        DATA.clear();
        for (var r : recipes) DATA.put(r.id(), r);
    }
    /** Adds a recipe from code; it survives data pack reloads and wins over a data-pack recipe with the same id. */
    public static synchronized void register(CookingRecipe recipe) { CODE.put(recipe.id(), recipe); }

    public static synchronized List<CookingRecipe> all() {
        var all = new LinkedHashMap<>(DATA); all.putAll(CODE);
        return List.copyOf(all.values());
    }
    public static List<CookingRecipe> forStation(Station station) {
        return all().stream().filter(r -> r.station() == station).sorted(Comparator.comparing(CookingRecipe::result)).toList();
    }
    public static synchronized CookingRecipe get(String id) { return CODE.containsKey(id) ? CODE.get(id) : DATA.get(id); }
    /** The recipe that makes this item, if any. */
    public static CookingRecipe making(String item) {
        for (var r : all()) if (r.result().equals(item)) return r;
        return null;
    }

    public static boolean accepts(String ingredient, Slot slot) {
        if (slot.isEmpty()) return false;
        return ingredient.startsWith("#") ? slot.is(ingredient.substring(1)) : slot.item().equals(ingredient);
    }

    /**
     * The recipe these slots make: every filled slot is used by exactly one ingredient, in any order.
     *
     * @param vessel  the pot's vessel slot, or null for stations without one
     * @param allowed which recipes may be cooked here (family recipes need the cook to know them)
     */
    public static CookingRecipe find(Station station, List<? extends Slot> grid, Slot vessel, Predicate<CookingRecipe> allowed) {
        int filled = (int) grid.stream().filter(s -> !s.isEmpty()).count();
        if (filled == 0) return null;
        for (var r : all()) {
            if (r.station() != station || r.ingredients().size() != filled || !allowed.test(r)) continue;
            if (r.vessel() != null && (vessel == null || vessel.isEmpty() || !vessel.item().equals(r.vessel()))) continue;
            if (assign(r, grid) != null) return r;
        }
        return null;
    }

    /** Which grid slot each of the recipe's ingredients comes from, or null if the grid doesn't make it. */
    public static int[] assign(CookingRecipe recipe, List<? extends Slot> grid) {
        var ingredients = recipe.ingredients();
        var slots = new ArrayList<Integer>();
        for (int i = 0; i < grid.size(); i++) if (!grid.get(i).isEmpty()) slots.add(i);
        if (slots.size() != ingredients.size()) return null;
        int[] chosen = new int[ingredients.size()];
        boolean[] used = new boolean[grid.size()];
        return place(ingredients, grid, slots, 0, chosen, used) ? chosen : null;
    }
    private static boolean place(List<String> ingredients, List<? extends Slot> grid, List<Integer> slots, int n, int[] chosen, boolean[] used) {
        if (n == ingredients.size()) return true;
        for (int slot : slots) {
            if (used[slot] || !accepts(ingredients.get(n), grid.get(slot))) continue;
            used[slot] = true; chosen[n] = slot;
            if (place(ingredients, grid, slots, n + 1, chosen, used)) return true;
            used[slot] = false;
        }
        return false;
    }

    private Cookbook() {}
}
