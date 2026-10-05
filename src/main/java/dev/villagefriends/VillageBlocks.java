package dev.villagefriends;

import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;

public final class VillageBlocks {
    private static final Map<String, Block> BLOCKS = new LinkedHashMap<>();
    public static final int BENCH_CAPACITY = 2;

    public static Identifier id(String path) { return Identifier.fromNamespaceAndPath("villagefriends", path); }
    public static Map<String, Block> all() { return Collections.unmodifiableMap(BLOCKS); }
    public static Block get(String path) {
        Block block = BLOCKS.get(path);
        if (block == null) throw new IllegalArgumentException("Unknown Village Friends block: " + path);
        return block;
    }
    private static void add(String name, boolean stone, double[][] boxes, FoundationEntityBlock.Kind kind) {
        var identifier = id(name);
        var properties = BlockBehaviour.Properties.of().setId(ResourceKey.create(Registries.BLOCK, identifier))
                .strength(stone ? 3.0F : 2.0F).sound(stone ? SoundType.STONE : SoundType.WOOD).noOcclusion();
        Block block = kind == null ? new FoundationBlock(properties, boxes) : new FoundationEntityBlock(properties, boxes, kind);
        BLOCKS.put(name, Registry.register(BuiltInRegistries.BLOCK, identifier, block));
        Registry.register(BuiltInRegistries.ITEM, identifier, new BlockItem(block,
                new Item.Properties().setId(ResourceKey.create(Registries.ITEM, identifier)).useBlockDescriptionPrefix()));
    }
    private static void add(String name, boolean stone, double[][] boxes) { add(name, stone, boxes, null); }

    public static void register() {
        add("training_dummy", false, new double[][]{{2,0,2,14,2,14},{7,2,7,9,16,9},{3,8,6,13,14,10},{5,14,5,11,16,11}});
        add("archery_target", false, new double[][]{{2,0,3,14,2,13},{3,2,7,5,8,9},{11,2,7,13,8,9},{2,7,6,14,16,10}});
        add("kitchen_stove", true, new double[][]{{0,0,0,16,12,16},{3,12,3,13,16,13}});
        add("drinks_barrel", false, new double[][]{{1,0,1,15,16,15}});
        add("tap_stand", false, new double[][]{{1,0,2,15,3,14},{3,3,5,13,12,13},{5,12,6,11,16,10},{7,10,2,9,12,6}});
        add("alchemical_press", true, new double[][]{{1,0,1,15,3,15},{3,3,3,5,16,13},{11,3,3,13,16,13},{3,14,3,13,16,13},{5,4,5,11,8,11}});
        add("easel_canvas", false, new double[][]{{2,0,3,4,14,5},{12,0,3,14,14,5},{7,0,11,9,14,13},{2,7,4,14,16,6}});
        add("music_stand", false, new double[][]{{2,0,2,14,2,14},{7,2,7,9,11,9},{2,11,4,14,13,12}});
        add("sewing_table", false, new double[][]{{1,10,1,15,12,15},{2,0,2,4,10,4},{12,0,2,14,10,4},{2,0,12,4,10,14},{12,0,12,14,10,14},{5,12,5,11,16,11}});
        add("sawmill", false, new double[][]{{0,8,0,16,12,16},{1,0,1,4,8,15},{12,0,1,15,8,15},{7,12,4,9,16,12}});
        add("archives", false, new double[][]{{0,0,0,16,16,16}});
        double[][] bench = {{0,6,3,16,9,13},{1,0,4,4,6,12},{12,0,4,15,6,12},{0,9,11,16,16,13}};
        add("village_bench", false, bench);
        add("campfire_bench", false, bench);
        add("apothecary_cot", false, new double[][]{{0,5,1,16,9,15},{1,0,2,3,5,4},{13,0,2,15,5,4},{1,0,12,3,5,14},{13,0,12,15,5,14}}, FoundationEntityBlock.Kind.APOTHECARY_COT);
        add("house_plaque", false, new double[][]{{2,5,12,14,15,16}}, FoundationEntityBlock.Kind.HOUSE_PLAQUE);
        add("notice_board", false, new double[][]{{2,0,7,4,14,9},{12,0,7,14,14,9},{1,6,6,15,16,10}}, FoundationEntityBlock.Kind.NOTICE_BOARD);
        add("command_desk", false, new double[][]{{0,10,0,16,13,16},{1,0,1,4,10,15},{12,0,1,15,10,15},{4,13,7,12,14,14}}, FoundationEntityBlock.Kind.COMMAND_DESK);
    }

    private VillageBlocks() {}
}
