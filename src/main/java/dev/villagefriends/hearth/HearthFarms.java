package dev.villagefriends.hearth;

import dev.villagefriends.CompanionController;
import dev.villagefriends.VillageFriends;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.item.ItemStack;

/**
 * Farmers sow Hearth crops: once a day every farmer keeps a few seeds of the crops their village grows
 * (onions and garlic in the desert, cabbages and leeks in the snow...), and vanilla's farming plants them
 * in the village fields alongside the wheat, since the seeds are tagged {@code minecraft:villager_plantable_seeds}.
 * Fields are also sown with Hearth crops when a village is built (the {@code <type>_..._fields} processors
 * from {@code tools/hearth/hearth.py}).
 */
public final class HearthFarms {
    private static final Map<UUID, Long> stocked = new HashMap<>();
    private static final Map<String, String> TYPES = Map.of("plains", "plains", "desert", "desert", "savanna", "savanna", "snow", "snowy", "taiga", "taiga");

    static void register() {
        ServerTickEvents.END_SERVER_TICK.register(HearthFarms::tick);
        ServerLifecycleEvents.SERVER_STOPPED.register(server -> stocked.clear());
    }
    private static void tick(MinecraftServer server) {
        if (server.getTickCount() % 600 != 0) return;
        for (var v : List.copyOf(CompanionController.loaded)) stock(v);
    }
    /** Hands a farmer the day's seeds, if they're running low. */
    public static void stock(Villager v) {
        if (v.isBaby() || !v.isAlive() || !VillageFriends.profession(v).equals("farmer")) return;
        long today = VillageFriends.day(v.level());
        if (stocked.getOrDefault(v.getUUID(), -1L) == today) return;
        stocked.put(v.getUUID(), today);
        var crops = cropsFor(v);
        if (crops.isEmpty()) return;
        int have = 0;
        var inventory = v.getInventory();
        for (int i = 0; i < inventory.getContainerSize(); i++) {
            var s = inventory.getItem(i);
            for (var c : crops) if (s.is(HearthItems.get(c.seed()))) have += s.getCount();
        }
        if (have >= 4) return;
        var crop = crops.get((int) Math.floorMod(Tastes.seed(VillageFriends.profile(v).id(), today), crops.size()));
        inventory.addItem(new ItemStack(HearthItems.get(crop.seed()), 4 + v.getRandom().nextInt(3)));
    }
    /** The crops a resident's village grows; homestead folk grow the homestead crops. */
    static List<Dishes.Crop> cropsFor(Villager v) {
        String kind = dev.villagefriends.homestead.Homesteads.dwells(v) ? "homestead"
                : TYPES.getOrDefault(v.getVillagerData().type().unwrapKey().map(k -> k.identifier().getPath()).orElse("plains"), "plains");
        return Dishes.table().crops().stream().filter(c -> c.biomes().contains(kind)).toList();
    }

    private HearthFarms() {}
}
