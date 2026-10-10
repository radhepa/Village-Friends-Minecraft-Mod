package dev.villagefriends.stable.data;

import com.google.common.collect.ImmutableSet;
import dev.villagefriends.FoundationBlock;
import dev.villagefriends.VillageBlocks;
import dev.villagefriends.VillageProfessions;
import it.unimi.dsi.fastutil.ints.Int2ObjectOpenHashMap;
import java.util.ArrayList;
import java.util.List;
import java.util.function.BiFunction;
import net.fabricmc.fabric.api.creativetab.v1.CreativeModeTabEvents;
import net.fabricmc.fabric.api.object.builder.v1.world.poi.PoiHelper;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.entity.ai.village.poi.PoiType;
import net.minecraft.world.entity.npc.villager.VillagerProfession;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.trading.TradeSet;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;

/**
 * The stable's blocks, their points of interest and the stablehand's job. Collision boxes are written facing north
 * in sixteenths and match the models drawn by {@code tools/stablehand/yard.py} (print them with {@code --boxes};
 * the tool refuses to write the art while they differ).
 *
 * <p>The Horse Stall is a point of interest (not a job site) so stables can be found by a POI search. The
 * Saddle Rack is the stablehand's job site. The stablehand is a normal villager profession but is deliberately
 * <b>not</b> in {@link VillageProfessions#JOBS}: that list also drives guard uniforms, the foundation block and
 * item counts and the "every job in every village type" checks, which a stable-only job doesn't fit.
 * {@code VillageProfessions.key("stablehand")} and {@code VillageFriends.profession(v)} still work for it.
 */
public final class StableBlocks {
    public static Block HORSE_STALL, HAY_TROUGH, SADDLE_RACK;
    public static final ResourceKey<PoiType> STALL_POI = VillageProfessions.poiKey("horse_stall");
    public static final ResourceKey<PoiType> STABLEHAND_POI = VillageProfessions.poiKey("stablehand");
    public static final ResourceKey<VillagerProfession> STABLEHAND = VillageProfessions.key("stablehand");
    private static final List<Block> ALL = new ArrayList<>();
    public static List<Block> all() { return List.copyOf(ALL); }

    private static Block add(String name, double[][] boxes, BiFunction<BlockBehaviour.Properties, double[][], Block> factory) {
        var id = VillageBlocks.id(name);
        var properties = BlockBehaviour.Properties.of().setId(ResourceKey.create(Registries.BLOCK, id)).strength(2.0F).sound(SoundType.WOOD).noOcclusion().ignitedByLava();
        Block block = Registry.register(BuiltInRegistries.BLOCK, id, factory.apply(properties, boxes));
        Registry.register(BuiltInRegistries.ITEM, id, new BlockItem(block, new Item.Properties().setId(ResourceKey.create(Registries.ITEM, id)).useBlockDescriptionPrefix()));
        ALL.add(block);
        return block;
    }

    public static void register() {
        HORSE_STALL = add("horse_stall", new double[][]{{0,0,0,16,2,16},{0,2,12,16,16,16},{3,6,9,13,10.5,12}}, FoundationBlock::new);
        HAY_TROUGH = add("hay_trough", new double[][]{{0,0,2,16,8,14}}, HayTroughBlock::new);
        SADDLE_RACK = add("saddle_rack", new double[][]{{2,0,2,14,2,14},{6,2,6,10,10,10},{3,7,2,13,15,14}}, FoundationBlock::new);
        PoiHelper.register(STALL_POI.identifier(), 1, 1, HORSE_STALL.getStateDefinition().getPossibleStates());
        PoiHelper.register(STABLEHAND_POI.identifier(), 1, 1, SADDLE_RACK.getStateDefinition().getPossibleStates());
        var trades = new Int2ObjectOpenHashMap<ResourceKey<TradeSet>>();
        for (int level = 1; level <= 5; level++) trades.put(level, ResourceKey.create(Registries.TRADE_SET, VillageBlocks.id("stablehand/level_" + level)));
        Registry.register(BuiltInRegistries.VILLAGER_PROFESSION, STABLEHAND, new VillagerProfession(
                Component.translatable("entity.villagefriends.villager.stablehand"), holder -> holder.is(STABLEHAND_POI), holder -> holder.is(STABLEHAND_POI),
                ImmutableSet.of(), ImmutableSet.of(), SoundEvents.VILLAGER_WORK_LEATHERWORKER, trades));
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.FUNCTIONAL_BLOCKS).register(entries -> ALL.forEach(entries::accept));
    }

    private StableBlocks() {}
}
