package dev.villagefriends;

import net.fabricmc.fabric.api.creativetab.v1.CreativeModeTabEvents;
import net.minecraft.world.item.CreativeModeTabs;

/** Phase 1 content registration, ordered before any world or content-pack loading. */
public final class VillageFoundation {
    public static void register() {
        VillageBlocks.register();
        VillageItems.register();
        VillageBlockEntities.register();
        VillageProfessions.register();
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.FUNCTIONAL_BLOCKS)
                .register(entries -> VillageBlocks.all().values().forEach(entries::accept));
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.FOOD_AND_DRINKS)
                .register(entries -> VillageItems.meals().forEach(entries::accept));
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.TOOLS_AND_UTILITIES)
                .register(entries -> VillageItems.suppliesAndTools().forEach(entries::accept));
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.COMBAT)
                .register(entries -> VillageItems.wearables().forEach(entries::accept));
    }

    private VillageFoundation() {}
}
