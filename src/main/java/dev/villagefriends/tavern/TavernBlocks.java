package dev.villagefriends.tavern;

import dev.villagefriends.FoundationBlock;
import dev.villagefriends.VillageBlocks;
import java.util.ArrayList;
import java.util.List;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;

/**
 * Tavern furniture. Boxes are written facing north, the way the sitter faces; models come from
 * {@code tools/tavern/furniture.py} ({@code --boxes} prints these).
 */
public final class TavernBlocks {
    public static Block TABLE, CHAIR, STOOL, ARMCHAIR;
    /** Where a dish sits on a Tavern Table, and how high a Bar Stool's seat is. */
    public static final double TABLE_TOP = 14 / 16.0, STOOL_SURFACE = 11 / 16.0;
    private static final List<Block> ALL = new ArrayList<>();
    public static List<Block> all() { return List.copyOf(ALL); }

    private static Block add(String name, double[][] boxes, SoundType sound) {
        var id = VillageBlocks.id(name);
        var properties = BlockBehaviour.Properties.of().setId(ResourceKey.create(Registries.BLOCK, id)).strength(2.0F).sound(sound).noOcclusion().ignitedByLava();
        Block block = Registry.register(BuiltInRegistries.BLOCK, id, new FoundationBlock(properties, boxes));
        Registry.register(BuiltInRegistries.ITEM, id, new BlockItem(block, new Item.Properties().setId(ResourceKey.create(Registries.ITEM, id)).useBlockDescriptionPrefix()));
        ALL.add(block);
        return block;
    }

    static void register() {
        TABLE = add("tavern_table", new double[][]{{0,12,0,16,14,16},{6,0,6,10,12,10},{2,0,6,14,2,10},{6,0,2,10,2,14}}, SoundType.WOOD);
        CHAIR = add("tavern_chair", new double[][]{{2,6,2,14,8,14},{2,0,2,4,6,4},{12,0,2,14,6,4},{2,0,12,4,6,14},{12,0,12,14,6,14},{2,8,12,14,16,14}}, SoundType.WOOD);
        STOOL = add("bar_stool", new double[][]{{3,9,3,13,11,13},{5,0,5,11,9,11}}, SoundType.WOOD);
        ARMCHAIR = add("fireside_armchair", new double[][]{{1,0,1,15,8,15},{0,0,1,2,12,16},{14,0,1,16,12,16},{2,8,13,14,16,16}}, SoundType.WOOL);
    }

    private TavernBlocks() {}
}
