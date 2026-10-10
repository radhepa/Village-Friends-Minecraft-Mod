package dev.villagefriends.fishing;

import dev.villagefriends.social.Calendar;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Consumer;
import java.util.function.Function;
import net.minecraft.ChatFormatting;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.food.FoodProperties;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.component.Consumables;
import net.minecraft.world.item.component.TooltipDisplay;
import net.minecraft.world.item.consume_effects.ApplyStatusEffectsConsumeEffect;
import net.minecraft.world.level.Level;

/**
 * Every fish in the fish table that isn't a vanilla item, the three rods' new two, bait, tackle, the Angler's
 * Journal, Message in a Bottle and Grilled Fish. Fish are food (lionfish stings), legends don't stack and
 * aren't food, and a record catch or a legend carries a {@link Fishing#TROPHY} with its size.
 */
public final class FishingItems {
    private static final Map<String, Item> ITEMS = new LinkedHashMap<>();
    private static final List<Item> FISH = new ArrayList<>(), GEAR = new ArrayList<>();
    public static Item REINFORCED_ROD, ANGLERS_ROD, JOURNAL, BOTTLE, GRILLED_FISH;

    public static Item get(String path) { return ITEMS.get(path); }
    public static List<Item> fish() { return List.copyOf(FISH); }
    public static List<Item> gear() { return List.copyOf(GEAR); }

    private static Item item(String path, Item.Properties properties, Function<Item.Properties, Item> factory) {
        var id = Fishing.id(path);
        var item = Registry.register(BuiltInRegistries.ITEM, id, factory.apply(properties.setId(ResourceKey.create(Registries.ITEM, id))));
        ITEMS.put(path, item);
        return item;
    }

    /** A caught fish: "Pike (54.3 cm)" when it's a trophy, with its rarity and the catch in the tooltip. */
    public static final class FishItem extends Item {
        public FishItem(Properties properties) { super(properties); }
        @Override public Component getName(ItemStack stack) {
            var name = super.getName(stack);
            var trophy = stack.get(Fishing.TROPHY);
            return trophy == null ? name : Component.translatable("item.villagefriends.trophy_fish", name, Catches.cm(trophy.size()).replace(" cm", ""));
        }
        @Override public void appendHoverText(ItemStack stack, TooltipContext context, TooltipDisplay display, Consumer<Component> out, TooltipFlag flag) {
            tooltip(stack, out);
        }
    }
    /** Tooltip lines for any fish (vanilla ones get them through {@link Fishing}'s tooltip event). */
    static void tooltip(ItemStack stack, Consumer<Component> out) {
        var fish = FishTable.byItem(BuiltInRegistries.ITEM.getKey(stack.getItem()).toString());
        if (fish == null) return;
        out.accept(Component.literal("★".repeat(fish.rarity().stars()) + " " + fish.rarity().label).withStyle(rarityColor(fish.rarity())));
        var trophy = stack.get(Fishing.TROPHY);
        if (trophy != null) out.accept(Component.literal(Catches.cm(trophy.size()) + ", caught by " + trophy.catcher() + " on " + Calendar.date(trophy.day()))
                .withStyle(ChatFormatting.GRAY));
    }
    public static ChatFormatting rarityColor(Fish.Rarity r) {
        return switch (r) { case COMMON -> ChatFormatting.GRAY; case UNCOMMON -> ChatFormatting.GREEN; case RARE -> ChatFormatting.AQUA;
            case EPIC -> ChatFormatting.LIGHT_PURPLE; case LEGENDARY -> ChatFormatting.GOLD; };
    }

    /** Bait and tackle: what they do, and how to load them. */
    public static final class GearItem extends Item {
        private final String effect;
        public GearItem(Properties properties, String effect) { super(properties); this.effect = effect; }
        @Override public void appendHoverText(ItemStack stack, TooltipContext context, TooltipDisplay display, Consumer<Component> out, TooltipFlag flag) {
            out.accept(Component.literal(effect).withStyle(ChatFormatting.GRAY));
            out.accept(Component.literal("Click onto a Reinforced or Angler's Rod to load it.").withStyle(ChatFormatting.DARK_GRAY));
        }
    }

    /** Opens the angler's journal. */
    public static final class JournalItem extends Item {
        public JournalItem(Properties properties) { super(properties); }
        @Override public InteractionResult use(Level level, Player player, InteractionHand hand) {
            if (player instanceof ServerPlayer p) FishingNet.openJournal(p);
            return InteractionResult.SUCCESS;
        }
        @Override public void appendHoverText(ItemStack stack, TooltipContext context, TooltipDisplay display, Consumer<Component> out, TooltipFlag flag) {
            out.accept(Component.literal("Every fish you catch, and the tall tales you hear.").withStyle(ChatFormatting.GRAY));
        }
    }

    /** A corked bottle from the sea: a note inside tells a tall tale and goes in your journal. */
    public static final class BottleItem extends Item {
        public BottleItem(Properties properties) { super(properties); }
        @Override public InteractionResult use(Level level, Player player, InteractionHand hand) {
            if (player instanceof ServerPlayer p) {
                var stack = player.getItemInHand(hand);
                FishingVillage.readBottle(p);
                level.playSound(null, p.blockPosition(), SoundEvents.BOTTLE_EMPTY, SoundSource.PLAYERS, 1, 1.1F);
                if (!p.getAbilities().instabuild) stack.shrink(1);
                if (!p.getInventory().add(new ItemStack(Items.GLASS_BOTTLE))) dev.villagefriends.VillageFriends.drop(p, new ItemStack(Items.GLASS_BOTTLE));
            }
            return InteractionResult.SUCCESS;
        }
        @Override public void appendHoverText(ItemStack stack, TooltipContext context, TooltipDisplay display, Consumer<Component> out, TooltipFlag flag) {
            out.accept(Component.literal("There's a rolled-up note inside.").withStyle(ChatFormatting.GRAY));
        }
    }

    static void register() {
        for (var f : FishTable.all()) {
            if (f.existing()) continue;
            var properties = new Item.Properties().rarity(switch (f.rarity()) {
                case LEGENDARY -> Rarity.EPIC; case EPIC -> Rarity.RARE; case RARE -> Rarity.UNCOMMON; default -> Rarity.COMMON; });
            if (f.legendary()) properties.stacksTo(1);
            if (f.edible()) {
                var food = new FoodProperties.Builder().nutrition(f.food()).saturationModifier(f.saturation()).build();
                if (f.flags().contains("poison"))
                    properties.food(food, Consumables.defaultFood().onConsume(new ApplyStatusEffectsConsumeEffect(new MobEffectInstance(MobEffects.POISON, 200, 0))).build());
                else properties.food(food);
            }
            FISH.add(item(f.id(), properties, FishItem::new));
        }
        REINFORCED_ROD = item("reinforced_rod", new Item.Properties().durability(128).enchantable(1), p -> new RodItem(p, Gear.Rod.REINFORCED));
        ANGLERS_ROD = item("anglers_rod", new Item.Properties().durability(256).enchantable(1).rarity(Rarity.UNCOMMON), p -> new RodItem(p, Gear.Rod.ANGLERS));
        GEAR.add(REINFORCED_ROD); GEAR.add(ANGLERS_ROD);
        for (var b : Gear.Bait.values())
            GEAR.add(item(b.id(), new Item.Properties().rarity(b == Gear.Bait.LEGEND_LURE ? Rarity.RARE : Rarity.COMMON), p -> new GearItem(p, Gear.baitEffect(b))));
        for (var t : Gear.Tackle.values())
            GEAR.add(item(t.id(), new Item.Properties().stacksTo(16), p -> new GearItem(p, t.effect() + " (" + Gear.TACKLE_USES + " fish)")));
        JOURNAL = item("anglers_journal", new Item.Properties().stacksTo(1), JournalItem::new);
        BOTTLE = item("message_in_a_bottle", new Item.Properties().stacksTo(16).rarity(Rarity.UNCOMMON), BottleItem::new);
        GRILLED_FISH = item("grilled_fish", new Item.Properties().food(new FoodProperties.Builder().nutrition(5).saturationModifier(.6F).build()), Item::new);
        GEAR.add(JOURNAL); GEAR.add(BOTTLE);
    }

    /** The bait or tackle kind an item is, or null. */
    public static Gear.Bait bait(ItemStack stack) {
        return stack.isEmpty() ? null : Gear.Bait.byId(path(stack));
    }
    public static Gear.Tackle tackle(ItemStack stack) {
        return stack.isEmpty() ? null : Gear.Tackle.byId(path(stack));
    }
    private static String path(ItemStack stack) {
        Identifier key = BuiltInRegistries.ITEM.getKey(stack.getItem());
        return key.getNamespace().equals(Fishing.NS) ? key.getPath() : "";
    }
    public static ItemStack stack(String id, int count) {
        var item = BuiltInRegistries.ITEM.getValue(Identifier.parse(id));
        return item == null || item == Items.AIR ? ItemStack.EMPTY : new ItemStack(item, count);
    }

    private FishingItems() {}
}
