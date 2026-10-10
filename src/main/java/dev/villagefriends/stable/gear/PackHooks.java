package dev.villagefriends.stable.gear;

import dev.villagefriends.stable.mixin.AbstractHorseAccessor;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.ItemStackWithSlot;
import net.minecraft.world.SimpleContainer;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.animal.equine.AbstractChestedHorse;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;
import org.jspecify.annotations.Nullable;

/**
 * Pack slots from tack (saddlebags on a horse, a pack saddle on a donkey or mule), called by the foundation's
 * {@code HorsePackMixin}, {@code ChestedHorsePackMixin} and {@code HorseEquipMixin}. Owned by the gear package;
 * the signatures are frozen.
 *
 * <p>The pack always matches the tack at once: {@link #equipped} resizes it in the same call that changed the saddle
 * (so a horse saddled and loaded in one server task works), and {@link #refresh} runs again just before the horse
 * menu is built. A tick where {@code getInventoryColumns()} counted more slots than the container held would let the
 * menu build phantom slots, and putting an item in one throws on the server thread. Shrinking drops what no longer
 * fits at the animal's feet. Vanilla saves a chested animal's container; {@link #save} and {@link #load} save the
 * rest under {@value #PACK}. An open horse menu closes when its container is swapped (vanilla's
 * {@code hasInventoryChanged}); the player opens it again to see the new slots.
 */
public final class PackHooks {
    /** Where a pack without a chest is saved on the animal. */
    public static final String PACK = "villagefriends:pack";

    /**
     * The inventory columns an animal has (3 slots each), given what vanilla says. Also called from the
     * {@code AbstractHorse} constructor (vanilla builds the inventory there), before attachments or the gear
     * table may be ready: anything missing means {@code vanilla}.
     */
    public static int columns(AbstractHorse horse, int vanilla) {
        String animal = Tack.animal(horse);
        if (animal == null) return vanilla;
        int tack = Tack.saddle(horse).map(g -> PackCapacity.tackColumns(g, animal)).orElse(0);
        int columns = PackCapacity.columns(animal, horse instanceof AbstractChestedHorse c && c.hasChest(), tack);
        return columns == PackCapacity.KEEP ? vanilla : columns;
    }

    /** End of {@code AbstractHorse.addAdditionalSaveData}: saves a pack that vanilla would not (no chest). */
    public static void save(AbstractHorse horse, ValueOutput out) {
        if (horse instanceof AbstractChestedHorse c && c.hasChest()) return; // vanilla saves the whole container under "Items"
        var pack = inventory(horse);
        if (pack == null || pack.isEmpty()) return;
        var list = out.list(PACK, ItemStackWithSlot.CODEC);
        for (int i = 0; i < pack.getContainerSize(); i++) {
            var stack = pack.getItem(i);
            if (!stack.isEmpty()) list.add(new ItemStackWithSlot(i, stack));
        }
    }

    /** End of {@code AbstractHorse.readAdditionalSaveData}: equipment is loaded by now, so the pack can be sized and refilled. */
    public static void load(AbstractHorse horse, ValueInput in) {
        if (Tack.animal(horse) == null) return;
        // Equipment is already read (it loads in LivingEntity's part of the chain); a chested donkey's own
        // setChest + createInventory run after this and copy these slots over, then read vanilla's "Items".
        ((AbstractHorseAccessor) horse).villagefriends$createInventory();
        var pack = inventory(horse);
        if (pack == null) return;
        for (var item : in.listOrEmpty(PACK, ItemStackWithSlot.CODEC))
            if (item.isValidInContainer(pack.getContainerSize())) pack.setItem(item.slot(), item.stack());
    }

    /**
     * Start of {@code LivingEntity.onEquipItem}, for every living entity: the new item is already in the slot (so
     * {@code getInventoryColumns()} already counts it), and this runs even on an entity's first tick, when vanilla
     * returns early.
     */
    public static void equipped(LivingEntity entity, EquipmentSlot slot, ItemStack old, ItemStack now) {
        if (slot == EquipmentSlot.SADDLE && entity instanceof AbstractHorse horse) refresh(horse);
    }

    /** Resizes the pack to match the gear right now (server side), dropping what no longer fits. A no-op when it already matches. */
    public static void refresh(AbstractHorse horse) {
        if (!(horse.level() instanceof ServerLevel level)) return;
        var pack = inventory(horse);
        int size = horse.getInventorySize();
        if (pack == null || pack.getContainerSize() == size) return;
        for (int i = Math.max(0, size); i < pack.getContainerSize(); i++) {
            var spilled = pack.removeItemNoUpdate(i);
            if (!spilled.isEmpty()) horse.spawnAtLocation(level, spilled);
        }
        // Vanilla's createInventory copies every slot that still fits into the new container and drops nothing itself.
        ((AbstractHorseAccessor) horse).villagefriends$createInventory();
    }

    /** The animal's container (saddle-free in 26.3: only pack slots), or null while it is being built. */
    public static @Nullable SimpleContainer inventory(AbstractHorse horse) { return ((AbstractHorseAccessor) horse).villagefriends$inventory(); }

    private PackHooks() {}
}
