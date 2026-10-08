package dev.villagefriends.tavern;

import dev.villagefriends.VillageBlocks;
import dev.villagefriends.VillageMealItem;
import java.util.ArrayList;
import java.util.List;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.food.FoodProperties;
import net.minecraft.world.item.Item;

/** The tavern's dishes: they join the cook's dish of the day, and residents eat them at the tavern. */
public final class TavernItems {
    private static final List<Item> MEALS = new ArrayList<>();
    public static List<Item> meals() { return List.copyOf(MEALS); }

    private static void meal(String name, int nutrition, float saturation, int stack, float healing) {
        var id = VillageBlocks.id(name);
        var properties = new Item.Properties().setId(ResourceKey.create(Registries.ITEM, id)).stacksTo(stack)
                .food(new FoodProperties.Builder().nutrition(nutrition).saturationModifier(saturation).build());
        MEALS.add(Registry.register(BuiltInRegistries.ITEM, id, new VillageMealItem(properties, healing)));
    }

    static void register() {
        // Bread, a wedge of cheese, an apple and a pickle on a board: the tavern's lunch.
        meal("ploughmans_lunch", 7, .7F, 16, 2);
        // Lamb and gravy under mashed potato, baked in a dish: a supper that sees you through the night.
        meal("shepherds_pie", 9, .8F, 16, 4);
        // A little apple tart with a lattice top, for afters.
        meal("apple_tart", 5, .5F, 16, 1);
    }

    private TavernItems() {}
}
