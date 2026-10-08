package dev.villagefriends;

import com.google.common.collect.ImmutableSet;
import it.unimi.dsi.fastutil.ints.Int2ObjectOpenHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Set;
import java.util.stream.Collectors;
import net.fabricmc.fabric.api.object.builder.v1.world.poi.PoiHelper;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.entity.ai.village.poi.PoiType;
import net.minecraft.world.entity.npc.villager.VillagerProfession;
import net.minecraft.world.item.trading.TradeSet;
import net.minecraft.world.level.block.state.BlockState;

public final class VillageProfessions {
    public static final List<String> JOBS = List.of("knight", "archer", "cook", "tavern_keeper", "apothecary", "painter", "bard", "tailor", "carpenter", "scholar");
    public static ResourceKey<VillagerProfession> key(String job) { return ResourceKey.create(Registries.VILLAGER_PROFESSION, VillageBlocks.id(job)); }
    public static ResourceKey<PoiType> poiKey(String job) { return ResourceKey.create(Registries.POINT_OF_INTEREST_TYPE, VillageBlocks.id(job)); }
    public static String label(String job) {
        return java.util.Arrays.stream(job.split("_")).map(part -> part.substring(0,1).toUpperCase(Locale.ROOT) + part.substring(1)).collect(Collectors.joining(" "));
    }
    public static List<String> workstations(String job) {
        return switch (job) {
            case "knight" -> List.of("training_dummy");
            case "archer" -> List.of("archery_target");
            case "cook" -> List.of("kitchen_stove");
            case "tavern_keeper" -> List.of("drinks_barrel", "tap_stand");
            case "apothecary" -> List.of("alchemical_press");
            case "painter" -> List.of("easel_canvas");
            case "bard" -> List.of("music_stand");
            case "tailor" -> List.of("sewing_table");
            case "carpenter" -> List.of("sawmill");
            case "scholar" -> List.of("archives");
            default -> throw new IllegalArgumentException("Unknown Village Friends profession: " + job);
        };
    }
    /** The sound a resident makes working at their station. */
    static net.minecraft.sounds.SoundEvent workSound(String job) {
        return switch (job) {
            case "knight" -> SoundEvents.VILLAGER_WORK_WEAPONSMITH;
            case "archer" -> SoundEvents.VILLAGER_WORK_FLETCHER;
            case "cook" -> SoundEvents.VILLAGER_WORK_BUTCHER;
            case "tavern_keeper" -> SoundEvents.BOTTLE_FILL;
            case "apothecary" -> SoundEvents.VILLAGER_WORK_CLERIC;
            case "painter" -> SoundEvents.VILLAGER_WORK_CARTOGRAPHER;
            case "tailor" -> SoundEvents.VILLAGER_WORK_SHEPHERD;
            case "carpenter" -> SoundEvents.VILLAGER_WORK_TOOLSMITH;
            default -> SoundEvents.VILLAGER_WORK_LIBRARIAN;
        };
    }
    public static void register() {
        for (String job : JOBS) {
            Set<BlockState> states = workstations(job).stream().flatMap(name -> VillageBlocks.get(name).getStateDefinition().getPossibleStates().stream()).collect(Collectors.toSet());
            PoiHelper.register(VillageBlocks.id(job), 1, 1, states);
            var trades = new Int2ObjectOpenHashMap<ResourceKey<TradeSet>>();
            for (int level = 1; level <= 5; level++) trades.put(level, ResourceKey.create(Registries.TRADE_SET, VillageBlocks.id(job + "/level_" + level)));
            Registry.register(BuiltInRegistries.VILLAGER_PROFESSION, key(job), new VillagerProfession(
                    Component.translatable("entity.villagefriends.villager." + job), holder -> holder.is(poiKey(job)), holder -> holder.is(poiKey(job)),
                    ImmutableSet.of(), ImmutableSet.of(), workSound(job), trades));
        }
    }
    private VillageProfessions() {}
}
