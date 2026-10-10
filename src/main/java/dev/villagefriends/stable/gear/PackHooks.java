package dev.villagefriends.stable.gear;

import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;

/**
 * Pack slots from tack (saddlebags on a horse, a pack saddle on a donkey or mule), called by the foundation's
 * {@code HorsePackMixin}, {@code ChestedHorsePackMixin} and {@code HorseEquipMixin}. Owned by the gear package;
 * the signatures are frozen.
 */
public final class PackHooks {
    /**
     * The inventory columns an animal has (3 slots each), given what vanilla says. Also called from the
     * {@code AbstractHorse} constructor (vanilla builds the inventory there), before attachments or the gear
     * table may be ready: anything missing means {@code vanilla}.
     */
    public static int columns(AbstractHorse horse, int vanilla) { return vanilla; }
    /** End of {@code AbstractHorse.addAdditionalSaveData}: saves a pack that vanilla would not (no chest). */
    public static void save(AbstractHorse horse, ValueOutput out) {}
    /** End of {@code AbstractHorse.readAdditionalSaveData}: equipment is loaded by now, so the pack can be sized and refilled. */
    public static void load(AbstractHorse horse, ValueInput in) {}
    /**
     * Start of {@code LivingEntity.onEquipItem}, for every living entity: the new item is already in the slot (so
     * {@code getInventoryColumns()} already counts it), and this runs even on an entity's first tick, when vanilla
     * returns early.
     */
    public static void equipped(LivingEntity entity, EquipmentSlot slot, ItemStack old, ItemStack now) {}
    /** Resizes the pack to match the gear right now (server side), dropping what no longer fits. A no-op when it already matches. */
    public static void refresh(AbstractHorse horse) {}

    private PackHooks() {}
}
