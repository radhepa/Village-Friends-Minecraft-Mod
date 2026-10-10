package dev.villagefriends.stable.data;

import dev.villagefriends.VillageBlocks;
import net.minecraft.core.Registry;
import net.minecraft.core.component.DataComponentType;
import net.minecraft.core.registries.BuiltInRegistries;

/**
 * Stablehand's item component. {@link #HORSE_PAPERS} says which animal a Horse Papers item is for; trades set it
 * in their JSON ({@code "components": {"villagefriends:horse_papers": {"breed": "destrier"}}}).
 */
public final class StableComponents {
    public static DataComponentType<HorsePapers> HORSE_PAPERS;

    public static void register() {
        HORSE_PAPERS = Registry.register(BuiltInRegistries.DATA_COMPONENT_TYPE, VillageBlocks.id("horse_papers"),
                DataComponentType.<HorsePapers>builder().persistent(HorsePapers.CODEC).networkSynchronized(HorsePapers.STREAM_CODEC).build());
    }

    private StableComponents() {}
}
