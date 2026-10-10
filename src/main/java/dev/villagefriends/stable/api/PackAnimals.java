package dev.villagefriends.stable.api;

import java.util.ArrayList;
import java.util.List;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.animal.equine.AbstractChestedHorse;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.entity.animal.equine.Horse;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.item.ItemStack;
import org.jspecify.annotations.Nullable;

/**
 * Pack animals for other mods (Kingsroads &amp; Caravans): carrying goods, and seating guards on horses. All static,
 * server side, safe to call whether or not Stablehand's other features are in use.
 * Owned by the gear package; the signatures are frozen.
 */
public final class PackAnimals {
    /** True for an adult, tamed horse/donkey/mule whose gear gives it pack slots (saddlebags, pack saddle or chest). */
    public static boolean canCarry(AbstractHorse animal) { return false; }
    /** Pack slots it has now (columns x 3), 0 if none. */
    public static int capacity(AbstractHorse animal) { return 0; }
    /** Tames (no owner) and fits a pack saddle on a donkey or mule, dropping any saddle it wore. False for other animals or babies. */
    public static boolean fitPackSaddle(AbstractHorse animal) { return false; }
    /** Puts copies of the goods into the pack, merging stacks; returns what did not fit (never null). */
    public static List<ItemStack> load(AbstractHorse animal, List<ItemStack> goods) {
        var left = new ArrayList<ItemStack>();
        for (var stack : goods) if (!stack.isEmpty()) left.add(stack.copy());
        return left;
    }
    /** Empties the pack and returns everything that was in it. */
    public static List<ItemStack> unload(AbstractHorse animal) { return List.of(); }
    /** A copy of what is in the pack, in slot order, without empties. */
    public static List<ItemStack> contents(AbstractHorse animal) { return List.of(); }
    /** Spawns a tamed adult donkey or mule ("donkey" / "mule") wearing a pack saddle at pos. */
    public static @Nullable AbstractChestedHorse spawnPackAnimal(ServerLevel level, BlockPos pos, String kind) { return null; }
    /** Spawns a tamed, saddled adult horse of a breed (null = the biome's pick) at pos, with no owner. */
    public static @Nullable Horse spawnHorse(ServerLevel level, BlockPos pos, @Nullable String breed) { return null; }
    /**
     * Seats a resident on a horse (order "caravan") until {@link #dismountGuard}. While mounted, Village Friends stops
     * steering them: their daily routine and their villager brain are switched off (as for companions), so they stay
     * where the caller puts them. The caller steers with {@code guard.getNavigation().moveTo(x, y, z, speed)} (or
     * {@code moveTo(entity, speed)}), which drives the horse at the horse's own speed times the modifier (1.0 to 1.6
     * is a walk to a canter). A guard (knight/archer) attacked on the road still fights through GuardController first.
     * Returns false if the horse is not a tame adult AbstractHorse, already has a rider, or the villager is a baby.
     */
    public static boolean mountGuard(Villager guard, AbstractHorse horse) { return false; }
    /** Takes a resident off their horse and clears the caravan order; their routine resumes on its next update. */
    public static void dismountGuard(Villager guard) { Riders.dismount(guard); }

    private PackAnimals() {}
}
