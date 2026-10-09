package dev.villagefriends.hearth;

import java.util.List;

/**
 * A station recipe: one ingredient per grid slot, in any order. Ingredients are item ids or item tags
 * written {@code #namespace:path}. The pot also wants {@code vessel} (a bowl or bottle) in its vessel slot.
 * Recipes come from data packs ({@code data/<namespace>/hearth_recipe/*.json}, loaded by {@link HearthRecipes})
 * or from code ({@link Cookbook#register}).
 *
 * @param id     the recipe's id, usually the dish's
 * @param time   ticks to cook one batch
 * @param secret a family recipe: it only cooks for someone who has learned it from a recipe card
 */
public record CookingRecipe(String id, Station station, List<String> ingredients, String vessel, String result, int count, int time, boolean secret) {
    public CookingRecipe {
        ingredients = List.copyOf(ingredients);
        if (ingredients.isEmpty() || ingredients.size() > Station.GRID) throw new IllegalArgumentException(id + ": 1 to " + Station.GRID + " ingredients");
        if (vessel != null && vessel.isEmpty()) vessel = null;
        if (count < 1 || time < 1) throw new IllegalArgumentException(id + ": count and time must be positive");
    }
}
