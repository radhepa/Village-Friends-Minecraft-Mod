package dev.villagefriends.stable.api;

import dev.villagefriends.stable.data.StableItems;
import dev.villagefriends.stable.data.StableTable;
import dev.villagefriends.stable.gear.PackHooks;
import dev.villagefriends.stable.gear.Tack;
import java.util.ArrayList;
import java.util.List;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.animal.equine.AbstractChestedHorse;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.entity.animal.equine.Donkey;
import net.minecraft.world.entity.animal.equine.Horse;
import net.minecraft.world.entity.animal.equine.Mule;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import org.jspecify.annotations.Nullable;

/**
 * Pack animals for other mods (Kingsroads &amp; Caravans): carrying goods, and seating guards on horses. All static,
 * server side, safe to call whether or not Stablehand's other features are in use.
 * Owned by the gear package; the signatures are frozen.
 *
 * <p><b>Pack slots.</b> An animal's pack comes from what it wears, never from its breed or bond: saddlebags give a
 * horse 6 slots, a pack saddle gives a donkey or mule 15 (no chest needed), and a chest gives a donkey or mule
 * vanilla's 15. The pack resizes in the same call that changes the tack, so fitting a pack saddle and loading goods
 * in one server task works. Goods are saved with the animal, chest or no chest. Taking the tack off spills what no
 * longer fits at the animal's feet, and an open horse menu closes when the pack resizes (open it again).
 *
 * <p><b>Guards.</b> {@link #mountGuard} seats a resident for a caravan: while mounted, Village Friends switches off
 * their daily routine and their villager brain, and the caller steers with
 * {@code guard.getNavigation().moveTo(x, y, z, speed)}, which drives the horse. A knight or archer attacked on the
 * road still fights first. {@link #dismountGuard} hands them back to their routine.
 *
 * <pre>{@code
 * var mule = PackAnimals.spawnPackAnimal(level, pos, "mule");          // tamed adult mule with a pack saddle
 * var left = PackAnimals.load(mule, List.of(new ItemStack(Items.WHEAT, 64), new ItemStack(Items.IRON_INGOT, 20)));
 * var horse = PackAnimals.spawnHorse(level, pos.east(2), "destrier");
 * if (PackAnimals.mountGuard(knight, horse)) knight.getNavigation().moveTo(x, y, z, 1.2);
 * List<ItemStack> goods = PackAnimals.unload(mule);                     // at the market
 * }</pre>
 */
public final class PackAnimals {
    /** True for an adult, tamed horse/donkey/mule whose gear gives it pack slots (saddlebags, pack saddle or chest). */
    public static boolean canCarry(AbstractHorse animal) {
        return Tack.animal(animal) != null && animal.isTamed() && !animal.isBaby() && animal.isAlive() && capacity(animal) > 0;
    }

    /** Pack slots it has now (columns x 3), 0 if none. */
    public static int capacity(AbstractHorse animal) { return Math.max(0, animal.getInventorySize()); }

    /** Tames (no owner) and fits a pack saddle on a donkey or mule, dropping any saddle it wore. False for other animals or babies. */
    public static boolean fitPackSaddle(AbstractHorse animal) {
        var packSaddle = StableItems.gear("pack_saddle");
        if (!(animal instanceof Donkey || animal instanceof Mule) || animal.isBaby() || packSaddle == null || !(animal.level() instanceof ServerLevel level)) return false;
        if (!animal.isTamed()) animal.setTamed(true);
        var worn = animal.getItemBySlot(EquipmentSlot.SADDLE);
        if (worn.is(packSaddle)) return true;
        if (!worn.isEmpty()) animal.spawnAtLocation(level, worn.copy());
        animal.setItemSlot(EquipmentSlot.SADDLE, new ItemStack(packSaddle)); // resizes the pack at once (PackHooks.equipped)
        animal.setGuaranteedDrop(EquipmentSlot.SADDLE);
        return true;
    }

    /** Puts copies of the goods into the pack, merging stacks; returns what did not fit (never null). */
    public static List<ItemStack> load(AbstractHorse animal, List<ItemStack> goods) {
        PackHooks.refresh(animal);
        var pack = PackHooks.inventory(animal);
        var left = new ArrayList<ItemStack>();
        for (var stack : goods) {
            if (stack == null || stack.isEmpty()) continue;
            var rest = pack == null || pack.getContainerSize() == 0 ? stack.copy() : pack.addItem(stack.copy());
            if (!rest.isEmpty()) left.add(rest);
        }
        return left;
    }

    /** Empties the pack and returns everything that was in it. */
    public static List<ItemStack> unload(AbstractHorse animal) {
        PackHooks.refresh(animal);
        var pack = PackHooks.inventory(animal);
        var out = new ArrayList<ItemStack>();
        if (pack == null) return out;
        for (int i = 0; i < pack.getContainerSize(); i++) {
            var stack = pack.removeItemNoUpdate(i);
            if (!stack.isEmpty()) out.add(stack);
        }
        pack.setChanged();
        return out;
    }

    /** A copy of what is in the pack, in slot order, without empties. */
    public static List<ItemStack> contents(AbstractHorse animal) {
        PackHooks.refresh(animal);
        var pack = PackHooks.inventory(animal);
        var out = new ArrayList<ItemStack>();
        if (pack != null) for (int i = 0; i < pack.getContainerSize(); i++) if (!pack.getItem(i).isEmpty()) out.add(pack.getItem(i).copy());
        return out;
    }

    /** Spawns a tamed adult donkey or mule ("donkey" / "mule") wearing a pack saddle at pos; null for any other kind. */
    public static @Nullable AbstractChestedHorse spawnPackAnimal(ServerLevel level, BlockPos pos, String kind) {
        EntityType<? extends AbstractChestedHorse> type = switch (kind == null ? "" : kind) {
            case "donkey" -> EntityTypes.DONKEY;
            case "mule" -> EntityTypes.MULE;
            default -> null;
        };
        if (type == null) return null;
        var animal = adult(level, pos, type);
        if (animal == null) return null;
        fitPackSaddle(animal);
        level.addFreshEntity(animal);
        return animal;
    }

    /** Spawns a tamed, saddled adult horse of a breed (null or unknown = the biome's pick) at pos, with no owner. */
    public static @Nullable Horse spawnHorse(ServerLevel level, BlockPos pos, @Nullable String breed) {
        var horse = adult(level, pos, EntityTypes.HORSE);
        if (horse == null) return null;
        horse.setTamed(true);
        // The breed goes on before the horse joins the world, so the breed feature's first-load pick leaves it alone.
        String pick = breed != null && StableTable.breed(breed).isPresent() ? breed : Horses.pickBreed(level, pos, level.getRandom());
        Horses.assignBreed(horse, pick, level.getRandom());
        horse.setItemSlot(EquipmentSlot.SADDLE, new ItemStack(Items.SADDLE));
        horse.setGuaranteedDrop(EquipmentSlot.SADDLE);
        level.addFreshEntity(horse);
        return horse;
    }

    /**
     * Seats a resident on a horse (order "caravan") until {@link #dismountGuard}. While mounted, Village Friends stops
     * steering them: their daily routine and their villager brain are switched off (as for companions), so they stay
     * where the caller puts them. The caller steers with {@code guard.getNavigation().moveTo(x, y, z, speed)} (or
     * {@code moveTo(entity, speed)}), which drives the horse at the horse's own speed times the modifier (1.0 to 1.6
     * is a walk to a canter). A guard (knight/archer) attacked on the road still fights through GuardController first.
     * Returns false if the horse is not a tame adult AbstractHorse, already has a rider, or the villager is a baby.
     */
    public static boolean mountGuard(Villager guard, AbstractHorse horse) {
        if (guard.isBaby() || !guard.isAlive() || !horse.isAlive() || !horse.isTamed() || horse.isBaby() || horse.isVehicle()) return false;
        return Riders.mount(guard, horse, "caravan");
    }

    /** Takes a resident off their horse and clears the caravan order; their routine resumes on its next update. */
    public static void dismountGuard(Villager guard) { Riders.dismount(guard); }

    /** A fresh adult of a type at the middle of {@code pos}, with vanilla's random stats, not yet in the world. */
    private static <T extends AbstractHorse> @Nullable T adult(ServerLevel level, BlockPos pos, EntityType<T> type) {
        T animal = type.create(level, EntitySpawnReason.MOB_SUMMONED);
        if (animal == null) return null;
        animal.snapTo(pos.getX() + .5, pos.getY(), pos.getZ() + .5, level.getRandom().nextFloat() * 360, 0);
        animal.finalizeSpawn(level, level.getCurrentDifficultyAt(pos), EntitySpawnReason.MOB_SUMMONED, null);
        animal.setAge(0);
        return animal;
    }

    private PackAnimals() {}
}
