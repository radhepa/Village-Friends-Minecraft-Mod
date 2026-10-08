package dev.villagefriends;

import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
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
        Block block = kind == null ? new FoundationBlock(properties, boxes) : switch (kind) {
            case NOTICE_BOARD -> new NoticeBoardBlock(properties, boxes);
            case HOUSE_PLAQUE -> new dev.villagefriends.home.HousePlaqueBlock(properties, boxes);
            default -> new FoundationEntityBlock(properties, boxes, kind);
        };
        BLOCKS.put(name, Registry.register(BuiltInRegistries.BLOCK, identifier, block));
        Registry.register(BuiltInRegistries.ITEM, identifier, new BlockItem(block,
                new Item.Properties().setId(ResourceKey.create(Registries.ITEM, identifier)).useBlockDescriptionPrefix()));
    }
    private static void add(String name, boolean stone, double[][] boxes) { add(name, stone, boxes, null); }
    /** A profession's workstation: it does something for players and for the resident who works there. */
    private static void station(String name, boolean stone, double[][] boxes) {
        var identifier = id(name);
        var station = WorkstationBlock.Station.of(name);
        var properties = BlockBehaviour.Properties.of().setId(ResourceKey.create(Registries.BLOCK, identifier))
                .strength(stone ? 3.0F : 2.0F).sound(stone ? SoundType.STONE : SoundType.WOOD).noOcclusion()
                .lightLevel(state -> state.hasProperty(WorkstationBlock.LIT) && state.getValue(WorkstationBlock.LIT) ? 13 : 0);
        Block block = switch (station) {
            case KITCHEN_STOVE -> new WorkstationBlock.Lit(properties, boxes, station);
            case EASEL_CANVAS -> new WorkstationBlock.Canvas(properties, boxes, station);
            default -> new WorkstationBlock(properties, boxes, station);
        };
        BLOCKS.put(name, Registry.register(BuiltInRegistries.BLOCK, identifier, block));
        Registry.register(BuiltInRegistries.ITEM, identifier, new BlockItem(block,
                new Item.Properties().setId(ResourceKey.create(Registries.ITEM, identifier)).useBlockDescriptionPrefix()));
    }
    public static List<String> stations() { return java.util.Arrays.stream(WorkstationBlock.Station.values()).map(s -> s.block).toList(); }

    public static void register() {
        station("training_dummy", false, new double[][]{{1,0,1,15,3,15},{6,3,6,10,16,10},{4,10,5,12,16,11}});
        station("archery_target", false, new double[][]{{1,0,6,15,16,9},{2,0,9,14,3,11}});
        station("kitchen_stove", true, new double[][]{{0,0,1,16,13,16},{2,13,4,8,16,10},{11,13,11,14,16,14}});
        station("drinks_barrel", false, new double[][]{{1,0,1,15,15,15}});
        station("tap_stand", false, new double[][]{{1,0,2,15,10,14},{4,10,5,12,16,13}});
        station("alchemical_press", true, new double[][]{{0.5,0,0.5,15.5,2,15.5},{1.5,2,6,3.5,16,10},{12.5,2,6,14.5,16,10},{3.5,2,3.5,12.5,9,12.5}});
        station("easel_canvas", false, new double[][]{{2,0,4,14,16,8.5},{7,0,9,9,3,13}});
        station("music_stand", false, new double[][]{{6.5,0,6.5,9.5,16,9.5},{2,11,6,14,16,9}});
        station("sewing_table", false, new double[][]{{0,11,0,16,13,16},{1,0,1,3,11,3},{13,0,1,15,11,3},{1,0,13,3,11,15},{13,0,13,15,11,15},{1,3,1,15,4,15}});
        station("sawmill", false, new double[][]{{0,10,2,16,12,14},{1,0,3,3,10,5},{13,0,3,15,10,5},{1,0,11,3,10,13},{13,0,11,15,10,13}});
        station("archives", false, new double[][]{{0,0,0,16,16,16}});
        double[][] bench = {{0,6,3,16,9,13},{1,0,4,4,6,12},{12,0,4,15,6,12},{0,9,11,16,16,13}};
        add("village_bench", false, bench);
        add("campfire_bench", false, bench);
        add("apothecary_cot", false, new double[][]{{0,5,1,16,9,15},{1,0,2,3,5,4},{13,0,2,15,5,4},{1,0,12,3,5,14},{13,0,12,15,5,14}}, FoundationEntityBlock.Kind.APOTHECARY_COT);
        add("house_plaque", false, new double[][]{{2,5,12,14,15,16}}, FoundationEntityBlock.Kind.HOUSE_PLAQUE);
        add("notice_board", false, new double[][]{{1,0,7,3,16,9},{13,0,7,15,16,9},{3,2,6,13,14,9},{0,14,5,16,16,11}}, FoundationEntityBlock.Kind.NOTICE_BOARD);
        add("command_desk", false, new double[][]{{0,10,0,16,13,16},{1,0,1,4,10,15},{12,0,1,15,10,15},{4,13,7,12,14,14}}, FoundationEntityBlock.Kind.COMMAND_DESK);
    }

    private VillageBlocks() {}
}
