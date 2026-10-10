package dev.villagefriends.stable.gear;

import dev.villagefriends.VillageBlocks;
import dev.villagefriends.stable.data.StableTable;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.entity.animal.equine.Donkey;
import net.minecraft.world.entity.animal.equine.Horse;
import net.minecraft.world.entity.animal.equine.Mule;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import org.jspecify.annotations.Nullable;

/**
 * Which gear an animal wears, by the item's id and the gear table. Read from both sides and from the horse
 * constructor (vanilla sizes the pack there), so it touches nothing that might not exist yet: an item that is not
 * Stablehand gear is simply no row. Rows are cached per item (the client and server threads both read it).
 */
public final class Tack {
    private static final String NAMESPACE = VillageBlocks.id("gear").getNamespace();
    private static final Map<Item, Optional<StableTable.Gear>> ROWS = new ConcurrentHashMap<>();

    /** The gear row of an item stack, if it is Stablehand gear. */
    public static Optional<StableTable.Gear> row(ItemStack stack) {
        if (stack == null || stack.isEmpty()) return Optional.empty();
        return ROWS.computeIfAbsent(stack.getItem(), item -> {
            var id = BuiltInRegistries.ITEM.getKey(item);
            return id != null && id.getNamespace().equals(NAMESPACE) ? StableTable.gear(id.getPath()) : Optional.empty();
        });
    }

    /** The tack row an animal wears in its SADDLE slot, if any. */
    public static Optional<StableTable.Gear> saddle(AbstractHorse animal) {
        return row(animal.getItemBySlot(EquipmentSlot.SADDLE)).filter(StableTable.Gear::tack);
    }

    /** Whether an animal wears this gear id in its SADDLE slot. */
    public static boolean wears(AbstractHorse animal, String gearId) { return saddle(animal).map(g -> g.id().equals(gearId)).orElse(false); }

    /** The gear table's name for the animal ("horse", "donkey" or "mule"), or null for any other (llamas, camels, undead horses). */
    public static @Nullable String animal(AbstractHorse animal) {
        if (animal instanceof Horse) return "horse";
        if (animal instanceof Donkey) return "donkey";
        if (animal instanceof Mule) return "mule";
        return null;
    }

    private Tack() {}
}
