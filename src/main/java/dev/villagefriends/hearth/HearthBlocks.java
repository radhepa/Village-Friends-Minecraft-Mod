package dev.villagefriends.hearth;

import java.util.List;
import net.fabricmc.fabric.api.menu.v1.ExtendedMenuType;
import net.fabricmc.fabric.api.object.builder.v1.block.entity.FabricBlockEntityTypeBuilder;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;

/** The three kitchen stations, their shared block entity and their screen. */
public final class HearthBlocks {
    public static Block COOKING_POT, CLAY_OVEN, PREP_TABLE;
    public static BlockEntityType<StationBlockEntity> STATION;
    public static ExtendedMenuType<StationMenu, StationMenu.Opening> MENU;

    public static List<Block> blocks() { return List.of(COOKING_POT, CLAY_OVEN, PREP_TABLE); }
    public static Block of(Station station) {
        return switch (station) { case POT -> COOKING_POT; case OVEN -> CLAY_OVEN; case PREP -> PREP_TABLE; };
    }

    private static Block add(String name, java.util.function.Function<BlockBehaviour.Properties, Block> factory, BlockBehaviour.Properties properties) {
        var id = Hearth.id(name);
        Block block = Registry.register(BuiltInRegistries.BLOCK, id, factory.apply(properties.setId(ResourceKey.create(Registries.BLOCK, id))));
        Registry.register(BuiltInRegistries.ITEM, id, new BlockItem(block, new Item.Properties().setId(ResourceKey.create(Registries.ITEM, id)).useBlockDescriptionPrefix()));
        return block;
    }

    static void register() {
        COOKING_POT = add("cooking_pot", StationBlock.Pot::new, BlockBehaviour.Properties.of().mapColor(MapColor.METAL).strength(2.0F, 6.0F)
                .requiresCorrectToolForDrops().sound(SoundType.LANTERN).noOcclusion());
        CLAY_OVEN = add("clay_oven", StationBlock.Oven::new, BlockBehaviour.Properties.of().mapColor(MapColor.TERRACOTTA_ORANGE).strength(2.5F, 6.0F)
                .requiresCorrectToolForDrops().sound(SoundType.DECORATED_POT).noOcclusion());
        PREP_TABLE = add("prep_table", StationBlock.Prep::new, BlockBehaviour.Properties.of().mapColor(MapColor.WOOD).strength(2.0F)
                .sound(SoundType.WOOD).noOcclusion().ignitedByLava());
        STATION = Registry.register(BuiltInRegistries.BLOCK_ENTITY_TYPE, Hearth.id("kitchen_station"),
                FabricBlockEntityTypeBuilder.create(StationBlockEntity::new, COOKING_POT, CLAY_OVEN, PREP_TABLE).build());
        MENU = Registry.register(BuiltInRegistries.MENU, Hearth.id("kitchen_station"), new ExtendedMenuType<>(StationMenu::new, StationMenu.Opening.STREAM_CODEC));
    }

    private HearthBlocks() {}
}
