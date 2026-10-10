package dev.villagefriends.stable.breed;

import dev.villagefriends.stable.yard.Stalls;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.animal.Animal;

/**
 * Called by the foundation's {@code AnimalBreedingMixin}. Owned by the breeds package; the signature is frozen.
 */
public final class BreedHooks {
    /**
     * Two animals just had a baby: runs at the end of {@code Animal.finalizeSpawnChildFromBreeding}, after vanilla
     * has mixed the parents' stats into the child and before the child is added to the world, so a foal never
     * reaches ENTITY_LOAD without its breed. Called for every animal; the breeds package acts on horses only. A foal
     * of a stalled horse also shares its parent's stall ({@link Stalls#foaled}), donkey and mule foals too.
     */
    public static void bred(Animal parent, ServerLevel level, Animal partner, AgeableMob child) {
        Breeds.bred(parent, level, partner, child);
        Stalls.foaled(parent, partner, child);
    }

    private BreedHooks() {}
}
