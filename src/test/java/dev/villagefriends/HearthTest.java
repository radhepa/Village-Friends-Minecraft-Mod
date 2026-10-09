package dev.villagefriends;

import static org.junit.jupiter.api.Assertions.*;

import com.google.gson.JsonParser;
import dev.villagefriends.hearth.CookingRecipe;
import dev.villagefriends.hearth.Cookbook;
import dev.villagefriends.hearth.Dish;
import dev.villagefriends.hearth.Dishes;
import dev.villagefriends.hearth.Station;
import dev.villagefriends.hearth.Tastes;
import dev.villagefriends.tavern.Patronage;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;
import java.util.UUID;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

class HearthTest {
    private static final String NS = "villagefriends:";
    private static final List<String> PERSONALITIES = List.of("warmhearted", "thoughtful", "playful", "adventurous", "meticulous", "steadfast",
            "reserved", "imaginative", "pragmatic", "curious", "protective", "gentle");
    private static Dishes.Table table;

    @BeforeAll static void load() throws Exception {
        try (var in = HearthTest.class.getResourceAsStream("/villagefriends/hearth/dishes.json")) {
            table = Dishes.parse(new InputStreamReader(in, StandardCharsets.UTF_8));
        }
        for (var d : table.dishes()) Dishes.put(d);
        var recipes = new ArrayList<CookingRecipe>();
        for (var d : table.dishes()) recipes.add(recipe(d.path()));
        Cookbook.load(recipes);
    }
    /** Reads a compiled recipe the way {@code HearthRecipes} does. */
    private static CookingRecipe recipe(String path) throws Exception {
        try (var in = HearthTest.class.getResourceAsStream("/data/villagefriends/hearth_recipe/" + path + ".json")) {
            assertNotNull(in, "every dish has a station recipe: " + path);
            var o = JsonParser.parseReader(new InputStreamReader(in, StandardCharsets.UTF_8)).getAsJsonObject();
            var ingredients = new ArrayList<String>();
            for (var e : o.getAsJsonArray("ingredients")) ingredients.add(e.getAsString());
            var result = o.getAsJsonObject("result");
            return new CookingRecipe(NS + path, Station.byId(o.get("station").getAsString()), ingredients, o.has("vessel") ? o.get("vessel").getAsString() : null,
                    result.get("id").getAsString(), result.get("count").getAsInt(), o.get("time").getAsInt(), o.has("secret") && o.get("secret").getAsBoolean());
        }
    }

    /** A slot as a station would show it to the cookbook. */
    private record Slot(String item, Set<String> tags) implements Cookbook.Slot {
        static Slot of(String item, String... tags) { return new Slot(item, Set.of(tags)); }
        static final Slot EMPTY = new Slot("", Set.of());
        @Override public boolean isEmpty() { return item.isEmpty(); }
        @Override public boolean is(String tag) { return tags.contains(tag); }
    }
    private static List<Slot> grid(Slot... filled) {
        var out = new ArrayList<Slot>(List.of(filled));
        while (out.size() < Station.GRID) out.add(Slot.EMPTY);
        return out;
    }

    @Test void theTableHasAboutSixtyDishesThatStayBalanced() {
        var meals = table.dishes().stream().filter(Dish::dish).toList();
        assertTrue(meals.size() >= 60, "about sixty dishes: " + meals.size());
        assertEquals(6, table.crops().size());
        for (var d : meals) {
            assertTrue(d.tier() >= 1 && d.tier() <= 3, d.id());
            assertTrue(d.buff() >= 60 && d.buff() <= 240, "Well Fed stays short: " + d.id() + " " + d.buff());
            assertTrue(d.food() >= 3 && d.food() <= 12, "no dish out-feeds a golden carrot by miles: " + d.id());
            assertFalse(d.likes().isEmpty(), "someone likes " + d.id());
        }
        for (var station : Station.values()) assertTrue(meals.stream().filter(d -> d.station() == station).count() >= 8, "plenty for the " + station);
        assertTrue(meals.stream().filter(Dish::secret).count() >= 10, "family recipes to collect");
        assertEquals(Set.of(1, 2, 3), new HashSet<>(meals.stream().map(Dish::tier).toList()));
    }

    @Test void ingredientsGoInAnyOrderButMustBeExact() {
        Slot onion = Slot.of(NS + "onion"), barley = Slot.of(NS + "barley"), herbs = Slot.of(NS + "herbs"), bowl = Slot.of("minecraft:bowl");
        var r = Cookbook.find(Station.POT, grid(herbs, onion, barley, onion), bowl, x -> true);
        assertNotNull(r);
        assertEquals(NS + "onion_pottage", r.result());
        assertNull(Cookbook.find(Station.POT, grid(herbs, onion, barley), bowl, x -> true), "one onion short");
        assertNull(Cookbook.find(Station.POT, grid(herbs, onion, barley, onion, Slot.of("minecraft:dirt")), bowl, x -> true), "nothing extra");
        assertNull(Cookbook.find(Station.POT, grid(herbs, onion, barley, onion), Slot.EMPTY, x -> true), "pot dishes need their bowl");
        assertNull(Cookbook.find(Station.OVEN, grid(herbs, onion, barley, onion), null, x -> true), "and the right station");
        var spaced = new ArrayList<>(List.of(Slot.EMPTY, onion, Slot.EMPTY, barley, herbs, onion));
        assertNotNull(Cookbook.find(Station.POT, spaced, bowl, x -> true), "gaps in the grid don't matter");
    }

    @Test void anyFishGoesInTheFishDishes() {
        Slot cod = Slot.of("minecraft:cod", "villagefriends:cooking/fish"), modded = Slot.of("talltales:perch", "villagefriends:cooking/fish");
        Slot onion = Slot.of(NS + "onion"), potato = Slot.of("minecraft:potato"), bowl = Slot.of("minecraft:bowl");
        var r = Cookbook.find(Station.POT, grid(cod, modded, onion, potato), bowl, x -> true);
        assertNotNull(r, "a modded fish in the cooking/fish tag counts");
        assertEquals(NS + "fishermans_stew", r.result());
    }

    @Test void familyRecipesNeedToBeLearned() {
        var harvest = List.of("onion", "cabbage", "leek", "garlic").stream().map(i -> Slot.of(NS + i)).toList();
        var g = new ArrayList<Slot>(harvest); g.add(Slot.of("minecraft:carrot")); g.add(Slot.of("minecraft:potato"));
        var bowl = Slot.of("minecraft:bowl");
        assertNull(Cookbook.find(Station.POT, g, bowl, r -> !r.secret()), "a stranger can't make harvest stew");
        var r = Cookbook.find(Station.POT, g, bowl, x -> true);
        assertNotNull(r);
        assertTrue(r.secret());
        assertEquals(NS + "harvest_stew", r.id());
    }

    @Test void recipesNeverCollideAndEveryIngredientIsMadeSomewhere() {
        var seen = new HashSet<String>();
        for (var r : Cookbook.all()) {
            var key = new ArrayList<>(r.ingredients()); Collections.sort(key);
            assertTrue(seen.add(r.station() + "|" + r.vessel() + "|" + key), "two recipes share one grid: " + r.id());
        }
        // Flour, butter, pastry, cheese and trenchers all have recipes, so every recipe can be cooked from scratch.
        for (var r : Cookbook.all())
            for (var i : r.ingredients()) if (i.startsWith(NS) && Dishes.has(i)) assertNotNull(Cookbook.making(i), "nothing makes " + i);
    }

    @Test void everyoneHasAFavoriteThatSuitsThem() {
        var random = new Random(7);
        int childSweets = 0, children = 400, adultsMatched = 0, adults = 600;
        var favorites = new HashSet<String>();
        for (int n = 0; n < children; n++) {
            var e = new Tastes.Eater(new UUID(random.nextLong(), random.nextLong()).toString(), PERSONALITIES.get(n % 12), "none", true);
            if (Tastes.favorite(e, Dishes.all()).likes().contains("child")) childSweets++;
        }
        for (int n = 0; n < adults; n++) {
            String personality = PERSONALITIES.get(n % 12);
            var e = new Tastes.Eater(new UUID(random.nextLong(), random.nextLong()).toString(), personality, n % 3 == 0 ? "farmer" : "none", false);
            var fav = Tastes.favorite(e, Dishes.all());
            assertSame(fav, Tastes.favorite(e, Dishes.all()), "a favorite never changes");
            assertNull(fav.needs(), "favorites never need another mod");
            if (fav.likes().contains(personality) || fav.likes().contains(e.job())) adultsMatched++;
            favorites.add(fav.id());
            var family = Tastes.familyRecipe(e, Dishes.all());
            assertTrue(family.secret(), "a family recipe is a secret one");
        }
        assertTrue(childSweets > children * 0.6, "children mostly love sweet things: " + childSweets);
        assertTrue(adultsMatched > adults * 0.6, "adults mostly love what their personality or job likes: " + adultsMatched);
        assertTrue(favorites.size() > 30, "lots of different favorites across a village: " + favorites.size());
    }

    @Test void homeMealsFitTheMeal() {
        var e = new Tastes.Eater(UUID.randomUUID().toString(), "steadfast", "farmer", false);
        for (long day = 0; day < 40; day++)
            for (var meal : List.of("breakfast", "lunch", "supper")) {
                var d = Tastes.homeMeal(e, meal, day, Dishes.all());
                assertNotNull(d, meal);
                assertTrue(d.meal(meal), d.id() + " for " + meal);
            }
        int larder = 0, summerLarder = 0;
        for (long day = 0; day < 90; day++) {
            if (Tastes.homeMeal(e, "supper", day, Dishes.all(), true).meal("winter")) larder++;
            if (Tastes.homeMeal(e, "supper", day, Dishes.all(), false).meal("winter")) summerLarder++;
        }
        assertTrue(larder > 15 && larder > summerLarder + 10, "in winter (Turning Seasons) suppers often come from the larder: " + larder + " vs " + summerLarder);
        var cake = Tastes.partyCake(e, Dishes.all());
        assertTrue(cake.cake(), "the party cake is a cake: " + cake.id());
    }

    @Test void theTavernMenuRotatesRealDishes() {
        var menu = Tastes.tavernMenu(Dishes.all());
        assertTrue(menu.size() >= 8, "a proper menu: " + menu);
        for (var id : menu) assertTrue(Dishes.get(id).meal("tavern"), id);
        Map<String, String> kinds = new java.util.HashMap<>();
        for (var d : Dishes.all()) kinds.put(d.id(), d.serve());
        Patronage.menu(menu, kinds);
        for (long day = 0; day < 30; day++) assertNotEquals(Patronage.dishOfTheDay(day), Patronage.supperDish(day), "lunch and supper differ");
        int repeats = 0;
        for (int i = 1; i < menu.size(); i++) if (kinds.get(menu.get(i)).equals(kinds.get(menu.get(i - 1)))) repeats++;
        assertTrue(repeats < menu.size() / 2, "stews, pies and breads take turns");
        assertEquals("stew", Patronage.kind(NS + "onion_pottage"));
        assertEquals("pie", Patronage.kind(NS + "mutton_pie"));
        assertEquals("minecraft:bowl", Patronage.leftover(NS + "beef_stew"));
    }

    @Test void giftsAndWellFed() {
        Dish stew = Dishes.get(NS + "beef_stew"), pottage = Dishes.get(NS + "onion_pottage"), flour = Dishes.get(NS + "flour");
        assertEquals(0, Tastes.giftValue(flour, false, false, false), "flour isn't a present");
        for (var d : Dishes.meals()) assertTrue(Tastes.giftValue(d, true, false, false) > Tastes.giftValue(d, false, true, false), "a favorite beats a fine dish");
        assertTrue(Tastes.giftValue(stew, false, false, false) > Tastes.giftValue(pottage, false, false, false), "a better dish is a better gift");
        assertTrue(Tastes.giftValue(stew, true, false, false) > 14, "a favorite dish beats their favorite thing (14)");
        assertEquals(Math.round(stew.buff() * 1.5), Tastes.wellFedSeconds(stew, true, 1));
        assertEquals(stew.buff() * 2, Tastes.wellFedSeconds(stew, false, 2));
        assertTrue(Tastes.hungerFactor(0) > Tastes.hungerFactor(1) && Tastes.hungerFactor(1) > Tastes.hungerFactor(2));
        assertTrue(Tastes.hungerFactor(2) >= .6, "even Well Fed III only slows hunger");
    }
}
