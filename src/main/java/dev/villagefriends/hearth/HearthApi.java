package dev.villagefriends.hearth;

import java.util.Set;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.tags.TagKey;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;

/**
 * The public face of Hearth & Harvest, for later features and add-ons.
 *
 * <ul>
 * <li>Dishes: add rows to {@code tools/hearth/dishes.tsv} and run {@code tools/hearth/hearth.py}, or call
 * {@link #registerDish} during mod initialization (it registers the item, with Well Fed, and the dish row).</li>
 * <li>Recipes: data packs ({@code data/<ns>/hearth_recipe/*.json}, see {@link HearthRecipes}) or {@link #registerRecipe}.</li>
 * <li>Fish: anything in the item tag {@code villagefriends:cooking/fish} ({@link #FISH}) goes into the fish dishes.</li>
 * <li>Hooks: {@link HearthEvents} (cooked, taken out, eaten).</li>
 * </ul>
 */
public final class HearthApi {
    /** Fish for the pot and the oven: add your fish to {@code data/villagefriends/tags/item/cooking/fish.json}. */
    public static final TagKey<Item> FISH = TagKey.create(Registries.ITEM, Hearth.id("cooking/fish"));
    /** Every Hearth & Harvest dish (and the dishes Village Friends had before). */
    public static final TagKey<Item> DISHES = TagKey.create(Registries.ITEM, Hearth.id("hearth/dishes"));

    /** Registers a dish item from a table row (call during mod initialization; {@code dish.existing()} rows only add the row). */
    public static Item registerDish(Dish dish) {
        Dishes.put(dish);
        return dish.existing() ? BuiltInRegistries.ITEM.getValue(net.minecraft.resources.Identifier.parse(dish.id())) : HearthItems.dish(dish);
    }
    /** Adds a station recipe from code; it survives data pack reloads. */
    public static void registerRecipe(CookingRecipe recipe) { Cookbook.register(recipe); }

    /** The dish row for an item stack, or null if it isn't a dish. */
    public static Dish dish(ItemStack stack) { return stack.isEmpty() ? null : Dishes.get(BuiltInRegistries.ITEM.getKey(stack.getItem()).toString()); }
    public static boolean isFine(ItemStack stack) { return Hearth.FINE != null && Boolean.TRUE.equals(stack.get(Hearth.FINE)); }
    /** Marks a dish as fine (a longer Well Fed, worth more as a gift, glinting, "Fine ..." in its name). */
    public static ItemStack makeFine(ItemStack stack) {
        var dish = dish(stack);
        if (dish == null || !dish.dish()) return stack;
        stack.set(Hearth.FINE, true);
        stack.set(DataComponents.ENCHANTMENT_GLINT_OVERRIDE, true);
        return stack;
    }

    /** Family recipes the player has learned. */
    public static Set<String> known(ServerPlayer player) { return Hearth.known(player); }
    public static boolean learn(ServerPlayer player, String recipe) { return Hearth.learn(player, recipe); }

    /** A resident's favorite dish (never null while the table has dishes). */
    public static Dish favorite(Villager resident) { return HearthVillage.favorite(resident); }

    private HearthApi() {}
}
