package dev.villagefriends.hearth;

import java.util.List;

/**
 * One row of the dish table ({@code tools/hearth/dishes.tsv}, compiled to {@code villagefriends/hearth/dishes.json}):
 * a dish or kitchen ingredient, how filling it is, its Well Fed tier and how long that lasts, what residents
 * call it in their animations ({@code serve}), the bowl or bottle it comes in, when residents eat it, and who
 * tends to love it. Pure data; {@link Dishes} registers the items.
 *
 * @param id       full item id, {@code villagefriends:onion_pottage}
 * @param existing an item Village Friends registered before Hearth & Harvest (it only gains a recipe and Well Fed)
 * @param needs    a mod id the dish depends on (its recipe only loads with that mod), or null
 * @param tier     Well Fed I-III; 0 for kitchen ingredients
 * @param buff     Well Fed seconds
 * @param vessel   "bowl", "bottle" or "-"
 */
public record Dish(String id, Station station, boolean existing, boolean ingredient, boolean secret, String needs,
                   int food, float saturation, int tier, int buff, String serve, String vessel, List<String> meals, List<String> likes) {
    public Dish {
        meals = List.copyOf(meals); likes = List.copyOf(likes);
    }
    /** The id without its namespace: {@code onion_pottage}. */
    public String path() { return id.substring(id.indexOf(':') + 1); }
    public boolean meal(String meal) { return meals.contains(meal); }
    /** A real dish (not flour or butter): it gives Well Fed and can be a favorite. */
    public boolean dish() { return !ingredient && tier > 0; }
    public boolean cake() { return meal("party") && serve.equals("tart"); }
    /** Its vessel's item id, or null. */
    public String vesselItem() {
        return switch (vessel) { case "bowl" -> "minecraft:bowl"; case "bottle" -> "minecraft:glass_bottle"; default -> null; };
    }
    /** How a resident would say it: "onion pottage". */
    public String spoken() { return path().replace('_', ' ').replace("fishermans", "fisherman's").replace("shepherds", "shepherd's").replace("ploughmans", "ploughman's"); }
}
