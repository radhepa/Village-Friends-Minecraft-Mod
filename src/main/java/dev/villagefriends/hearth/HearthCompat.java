package dev.villagefriends.hearth;

import net.fabricmc.fabric.api.loot.v3.LootTableEvents;
import net.fabricmc.loader.api.FabricLoader;
import net.minecraft.world.item.ItemStack;

/**
 * Optional ties to other mods. With Not-So-Vanilla Mobs installed, a few of its creatures drop kitchen
 * ingredients (its own loot tables drop only vanilla items): Wild Boars a haunch of boar, the Brineclaw
 * crab its claw meat, Sporelings a sporecap. Their dishes' recipes load only with the mod
 * ({@code fabric:load_conditions}). No mixins into other mods; nothing here runs without them.
 */
public final class HearthCompat {
    public static final String NSV = "nsvmobs";

    static void register() {
        if (!FabricLoader.getInstance().isModLoaded(NSV)) return;
        LootTableEvents.MODIFY_DROPS.register((table, context, drops) -> {
            var key = table.unwrapKey().orElse(null);
            if (key == null || !key.identifier().getNamespace().equals(NSV)) return;
            String path = key.identifier().getPath();
            for (var i : Dishes.table().ingredients()) {
                if (i.source() == null || !i.source().equals(NSV + ":" + path.substring(path.lastIndexOf('/') + 1)) || !path.startsWith("entities/")) continue;
                int n = i.min() + context.getRandom().nextInt(i.max() - i.min() + 1);
                if (n > 0) drops.add(new ItemStack(HearthItems.get(i.id()), n));
            }
        });
    }

    private HearthCompat() {}
}
