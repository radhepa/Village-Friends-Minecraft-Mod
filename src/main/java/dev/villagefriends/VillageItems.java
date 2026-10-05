package dev.villagefriends;

import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import net.minecraft.core.Registry;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.food.FoodProperties;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.ItemUseAnimation;
import net.minecraft.world.item.component.Consumable;
import net.minecraft.world.item.consume_effects.ApplyStatusEffectsConsumeEffect;
import net.minecraft.world.item.equipment.EquipmentAssets;
import net.minecraft.world.item.equipment.Equippable;

public final class VillageItems {
    private static final Map<String, Item> ITEMS = new LinkedHashMap<>();
    private static final List<Item> MEALS = new ArrayList<>(), SUPPLIES = new ArrayList<>(), WEARABLES = new ArrayList<>();
    public static Map<String, Item> all() { return Collections.unmodifiableMap(ITEMS); }
    public static List<Item> meals() { return List.copyOf(MEALS); }
    public static List<Item> suppliesAndTools() { return List.copyOf(SUPPLIES); }
    public static List<Item> wearables() { return List.copyOf(WEARABLES); }
    public static Item get(String name) {
        Item item = ITEMS.get(name);
        if (item == null) throw new IllegalArgumentException("Unknown Village Friends item: " + name);
        return item;
    }
    private static Item add(String name, Function<Item.Properties, Item> factory, List<Item> group) {
        var id = VillageBlocks.id(name);
        Item item = Registry.register(BuiltInRegistries.ITEM, id, factory.apply(new Item.Properties().setId(ResourceKey.create(Registries.ITEM, id))));
        ITEMS.put(name, item); group.add(item); return item;
    }
    private static void wearable(String name) {
        add(name, p -> new Item(p.stacksTo(1).component(DataComponents.EQUIPPABLE,
                Equippable.builder(EquipmentSlot.CHEST).setAsset(ResourceKey.create(EquipmentAssets.ROOT_ID, VillageBlocks.id(name)))
                        .setDamageOnHurt(false).build())), WEARABLES);
    }
    public static void register() {
        add("smelling_salts", p -> new MedicalSupplyItem(p.stacksTo(16), MedicalSupplyItem.Treatment.SMELLING_SALTS), SUPPLIES);
        add("revival_tonic", p -> new MedicalSupplyItem(p.stacksTo(16), MedicalSupplyItem.Treatment.REVIVAL_TONIC), SUPPLIES);
        add("bandage_wrap", p -> new MedicalSupplyItem(p, MedicalSupplyItem.Treatment.BANDAGE_WRAP), SUPPLIES);
        Item mug = add("empty_coffee_mug", Item::new, SUPPLIES);
        add("steaming_coffee_mug", p -> new Item(p.stacksTo(16).food(new FoodProperties.Builder().nutrition(1).saturationModifier(0.1F).alwaysEdible().build(),
                Consumable.builder().animation(ItemUseAnimation.DRINK).sound(SoundEvents.GENERIC_DRINK).hasConsumeParticles(false)
                        .onConsume(new ApplyStatusEffectsConsumeEffect(new MobEffectInstance(MobEffects.SPEED, 600, 0))).build()).usingConvertsTo(mug)), MEALS);
        add("fresh_village_bread", p -> new VillageMealItem(p.food(new FoodProperties.Builder().nutrition(6).saturationModifier(0.6F).build()).villagerFood(6), 2.0F), MEALS);
        add("hearty_stew", p -> new VillageMealItem(p.stacksTo(1).food(new FoodProperties.Builder().nutrition(8).saturationModifier(0.8F).build()).usingConvertsTo(Items.BOWL), 6.0F), MEALS);
        wearable("rain_cloak"); wearable("hooded_poncho");
        for (String profession : VillageProfessions.JOBS) wearable(profession + "_uniform");
        for (String tool : List.of("broom", "paintbrush", "lute", "carpenter_hammer", "field_journal"))
            add(tool, p -> new Item(p.stacksTo(1)), SUPPLIES);
    }
    private VillageItems() {}
}
