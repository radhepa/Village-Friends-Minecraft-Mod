package dev.villagefriends.hearth;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Supplier;
import net.fabricmc.fabric.api.registry.VillagerInteractionRegistries;
import net.fabricmc.loader.api.FabricLoader;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.food.FoodProperties;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.ItemUseAnimation;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.component.Consumable;
import net.minecraft.world.item.component.Consumables;
import net.minecraft.world.item.consume_effects.ApplyStatusEffectsConsumeEffect;
import net.minecraft.world.level.ItemLike;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.CropBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;
import net.minecraft.world.level.material.PushReaction;

/**
 * Registers the crops (blocks, seeds and produce), the mob ingredients, every dish from the dish table and
 * the recipe card. Dishes the mod already had (Hearty Stew, Shepherd's Pie...) keep their items and only gain
 * Well Fed ({@link Hearth}).
 */
public final class HearthItems {
    private static final Map<String, Item> ITEMS = new LinkedHashMap<>();
    private static final List<Block> CROPS = new ArrayList<>();
    private static final List<Item> FOOD = new ArrayList<>(), INGREDIENTS = new ArrayList<>(), FARMING = new ArrayList<>();
    public static Item RECIPE_CARD;

    public static Item get(String path) { return ITEMS.get(path); }
    public static Map<String, Item> all() { return java.util.Collections.unmodifiableMap(ITEMS); }
    public static List<Block> crops() { return List.copyOf(CROPS); }
    /** Dishes for the Food and Drinks tab, ingredients for Ingredients, seeds and produce for Natural Blocks. */
    public static List<Item> food() { return List.copyOf(FOOD); }
    public static List<Item> ingredients() { return List.copyOf(INGREDIENTS); }
    public static List<Item> farming() { return List.copyOf(FARMING); }

    /** A crop that grows like wheat (eight ages) and drops its own seed. */
    public static final class HearthCrop extends CropBlock {
        private final Supplier<Item> seed;
        public HearthCrop(Properties properties, Supplier<Item> seed) { super(properties); this.seed = seed; }
        @Override protected ItemLike getBaseSeedId() { return seed.get(); }
    }

    /** A cooked dish: "Fine Onion Pottage" when it was made well. */
    public static final class DishItem extends Item {
        public DishItem(Properties properties) { super(properties); }
        @Override public Component getName(ItemStack stack) {
            var name = super.getName(stack);
            return HearthApi.isFine(stack) ? Component.translatable("item.villagefriends.fine_dish", name) : name;
        }
    }

    private static Item item(String path, Item.Properties properties, java.util.function.Function<Item.Properties, Item> factory) {
        var id = Hearth.id(path);
        var item = Registry.register(BuiltInRegistries.ITEM, id, factory.apply(properties.setId(ResourceKey.create(Registries.ITEM, id))));
        ITEMS.put(path, item);
        return item;
    }

    static void register(Dishes.Table table) {
        for (var c : table.crops()) {
            var blockId = Hearth.id(c.id() + "_crop");
            Item[] seed = new Item[1];
            var block = Registry.register(BuiltInRegistries.BLOCK, blockId, new HearthCrop(BlockBehaviour.Properties.of()
                    .setId(ResourceKey.create(Registries.BLOCK, blockId)).mapColor(MapColor.PLANT).noCollision().randomTicks().instabreak()
                    .sound(SoundType.CROP).pushReaction(PushReaction.POPPED), () -> seed[0]));
            CROPS.add(block);
            seed[0] = item(c.seed(), new Item.Properties(), p -> new BlockItem(block, p));
            var produce = c.food() > 0
                    ? item(c.id(), new Item.Properties().food(new FoodProperties.Builder().nutrition(c.food()).saturationModifier(c.saturation()).build()), Item::new)
                    : item(c.id(), new Item.Properties(), Item::new);
            FARMING.add(seed[0]); FARMING.add(produce);
            VillagerInteractionRegistries.registerCompostable(seed[0]);
            VillagerInteractionRegistries.registerCompostable(produce);
        }
        for (var i : table.ingredients()) {
            var food = new FoodProperties.Builder().nutrition(i.food()).saturationModifier(i.saturation()).build();
            var properties = new Item.Properties();
            if (i.effect() != null) {
                var effect = BuiltInRegistries.MOB_EFFECT.get(Identifier.parse(i.effect())).orElseThrow();
                properties.food(food, Consumables.defaultFood().onConsume(new ApplyStatusEffectsConsumeEffect(new MobEffectInstance(effect, i.effectSeconds() * 20, 0))).build());
            } else properties.food(food);
            var item = item(i.id(), properties, Item::new);
            if (i.needs() == null || FabricLoader.getInstance().isModLoaded(i.needs())) INGREDIENTS.add(item);
        }
        for (var d : table.dishes()) if (!d.existing()) dish(d);
        RECIPE_CARD = item("recipe_card", new Item.Properties().stacksTo(16), RecipeCardItem::new);
    }

    /** Registers one dish or kitchen ingredient from its table row. */
    static Item dish(Dish d) {
        var properties = new Item.Properties().stacksTo(d.dish() ? 16 : 64);
        var vessel = d.vesselItem() == null ? null : BuiltInRegistries.ITEM.getValue(Identifier.parse(d.vesselItem()));
        if (vessel != null) properties.craftRemainder(vessel);
        if (d.food() > 0) {
            var food = new FoodProperties.Builder().nutrition(d.food()).saturationModifier(d.saturation()).build();
            var consumable = d.serve().equals("cider") ? Consumables.defaultDrink() : Consumables.defaultFood();
            if (d.serve().equals("cider")) consumable.animation(ItemUseAnimation.DRINK).sound(SoundEvents.GENERIC_DRINK);
            if (d.dish()) consumable.onConsume(new WellFed.OnEat(d.tier(), d.buff()));
            properties.food(food, consumable.build());
            if (vessel != null) properties.usingConvertsTo(vessel);
        }
        var item = item(d.path(), properties, d.dish() ? DishItem::new : Item::new);
        if (d.needs() == null || FabricLoader.getInstance().isModLoaded(d.needs())) (d.dish() ? FOOD : INGREDIENTS).add(item);
        return item;
    }

    /** The consumable a dish the mod already had gets: its old eating, plus Well Fed. */
    static Consumable consumableFor(Dish d, Item item) {
        var builder = Consumables.defaultFood();
        return builder.onConsume(new WellFed.OnEat(d.tier(), d.buff())).build();
    }

    static ItemStack stack(String id, int count) {
        var item = BuiltInRegistries.ITEM.getValue(Identifier.parse(id));
        return item == null || item == Items.AIR ? ItemStack.EMPTY : new ItemStack(item, count);
    }

    private HearthItems() {}
}
