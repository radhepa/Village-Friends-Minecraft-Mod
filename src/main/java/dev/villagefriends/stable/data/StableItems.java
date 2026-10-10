package dev.villagefriends.stable.data;

import dev.villagefriends.VillageBlocks;
import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.function.UnaryOperator;
import net.fabricmc.fabric.api.creativetab.v1.CreativeModeTabEvents;
import net.minecraft.core.Registry;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.TagKey;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.ToolMaterial;
import net.minecraft.world.item.component.AttackRange;
import net.minecraft.world.item.equipment.ArmorMaterial;
import net.minecraft.world.item.equipment.ArmorType;
import net.minecraft.world.item.equipment.EquipmentAssets;
import net.minecraft.world.item.equipment.Equippable;

/**
 * Every Stablehand item. There are no custom item classes: the brush, whistle, papers and lance get their
 * behaviour from Fabric callbacks in their feature packages. Gear comes from {@code gear.json}: barding is
 * vanilla horse armor with our own {@link ArmorMaterial} (rendered by vanilla's {@code horse_body} layer),
 * and tack is any item whose {@link Equippable} slot is SADDLE, which is all a horse needs to count as saddled
 * (steerable, worn through the horse menu, put on with a right click, taken off with shears).
 */
public final class StableItems {
    private static final Map<String, Item> ITEMS = new LinkedHashMap<>();
    private static final List<Item> TOOLS = new ArrayList<>(), COMBAT = new ArrayList<>();
    public static Item GROOMING_BRUSH, HORSE_WHISTLE, HORSE_PAPERS, JOUSTING_LANCE;

    public static Map<String, Item> all() { return Collections.unmodifiableMap(ITEMS); }
    public static Item get(String name) {
        Item item = ITEMS.get(name);
        if (item == null) throw new IllegalArgumentException("Unknown Stablehand item: " + name);
        return item;
    }
    /** The item of a gear row, or null when the id is not Stablehand gear. */
    public static Item gear(String id) { return StableTable.gear(id).isPresent() ? ITEMS.get(id) : null; }

    private static Item add(String name, UnaryOperator<Item.Properties> properties, List<Item> tab) {
        var id = VillageBlocks.id(name);
        Item item = Registry.register(BuiltInRegistries.ITEM, id, new Item(properties.apply(new Item.Properties().setId(ResourceKey.create(Registries.ITEM, id)))));
        ITEMS.put(name, item); tab.add(item);
        return item;
    }

    public static void register() {
        GROOMING_BRUSH = add("grooming_brush", p -> p.stacksTo(1).durability(128), TOOLS);
        HORSE_WHISTLE = add("horse_whistle", p -> p.stacksTo(1), TOOLS);
        HORSE_PAPERS = add("horse_papers", p -> p.stacksTo(1), TOOLS);
        for (var g : StableTable.gear()) {
            if (g.tack()) add(g.id(), p -> p.stacksTo(1).component(DataComponents.EQUIPPABLE, Equippable.builder(EquipmentSlot.SADDLE)
                    .setEquipSound(SoundEvents.HORSE_SADDLE).setAsset(ResourceKey.create(EquipmentAssets.ROOT_ID, VillageBlocks.id(g.id())))
                    .setAllowedEntities(animals(g.animals())).setEquipOnInteract(true).setCanBeSheared(true)
                    .setShearingSound(SoundEvents.SADDLE_UNEQUIP).build()), TOOLS);
            else if (g.barding()) add(g.id(), p -> p.stacksTo(1).horseArmor(material(g)), COMBAT);
        }
        var l = StableTable.lance();
        JOUSTING_LANCE = add(l.id(), p -> p.spear(toolMaterial(l.material()), l.attackDuration(), l.damageMultiplier(), l.delay(), l.dismountTime(),
                l.dismountThreshold(), l.knockbackTime(), l.knockbackThreshold(), l.damageTime(), l.damageThreshold())
                .component(DataComponents.ATTACK_RANGE, new AttackRange(l.reach()[0], l.reach()[1], l.reach()[2], l.reach()[3], l.reach()[4], l.reach()[5])), COMBAT);
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.TOOLS_AND_UTILITIES).register(entries -> {
            for (var item : TOOLS) {
                if (item != HORSE_PAPERS) { entries.accept(item); continue; }
                for (var breed : papersBreeds()) entries.accept(papers(breed));
            }
        });
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.COMBAT).register(entries -> COMBAT.forEach(entries::accept));
    }

    /** Every animal papers can be for: each breed in table order, then donkey and mule. */
    public static List<String> papersBreeds() {
        var out = new ArrayList<String>();
        for (var b : StableTable.breeds()) out.add(b.id());
        out.add("donkey"); out.add("mule");
        return out;
    }
    /** Horse Papers for a breed id, "donkey" or "mule". */
    public static ItemStack papers(String breed) {
        var stack = new ItemStack(HORSE_PAPERS);
        stack.set(StableComponents.HORSE_PAPERS, new HorsePapers(breed));
        return stack;
    }

    private static EntityType<?>[] animals(List<String> names) {
        return names.stream().map(n -> switch (n) {
            case "horse" -> EntityTypes.HORSE;
            case "donkey" -> EntityTypes.DONKEY;
            case "mule" -> EntityTypes.MULE;
            default -> throw new IllegalArgumentException("Gear can't be worn by " + n);
        }).toArray(EntityType<?>[]::new);
    }
    private static ArmorMaterial material(StableTable.Gear g) {
        return new ArmorMaterial(0, Map.of(ArmorType.BODY, g.defense()), g.enchantability(), SoundEvents.HORSE_ARMOR, g.toughness(), g.knockback(),
                TagKey.create(Registries.ITEM, Identifier.parse(g.repair())), ResourceKey.create(EquipmentAssets.ROOT_ID, VillageBlocks.id(g.id())));
    }
    private static ToolMaterial toolMaterial(String name) {
        return switch (name) {
            case "wood" -> ToolMaterial.WOOD;
            case "stone" -> ToolMaterial.STONE;
            case "copper" -> ToolMaterial.COPPER;
            case "gold" -> ToolMaterial.GOLD;
            case "diamond" -> ToolMaterial.DIAMOND;
            case "netherite" -> ToolMaterial.NETHERITE;
            default -> ToolMaterial.IRON;
        };
    }

    private StableItems() {}
}
