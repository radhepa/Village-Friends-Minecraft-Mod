package dev.villagefriends;

import net.fabricmc.fabric.api.object.builder.v1.block.entity.FabricBlockEntityTypeBuilder;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.world.level.block.entity.BlockEntityType;

public final class VillageBlockEntities {
    public static BlockEntityType<HousePlaqueBlockEntity> HOUSE_PLAQUE;
    public static BlockEntityType<NoticeBoardBlockEntity> NOTICE_BOARD;
    public static BlockEntityType<CommandDeskBlockEntity> COMMAND_DESK;
    public static BlockEntityType<ApothecaryCotBlockEntity> APOTHECARY_COT;

    public static void register() {
        HOUSE_PLAQUE = Registry.register(BuiltInRegistries.BLOCK_ENTITY_TYPE, VillageBlocks.id("house_plaque"),
                FabricBlockEntityTypeBuilder.create(HousePlaqueBlockEntity::new, VillageBlocks.get("house_plaque")).build());
        NOTICE_BOARD = Registry.register(BuiltInRegistries.BLOCK_ENTITY_TYPE, VillageBlocks.id("notice_board"),
                FabricBlockEntityTypeBuilder.create(NoticeBoardBlockEntity::new, VillageBlocks.get("notice_board")).build());
        COMMAND_DESK = Registry.register(BuiltInRegistries.BLOCK_ENTITY_TYPE, VillageBlocks.id("command_desk"),
                FabricBlockEntityTypeBuilder.create(CommandDeskBlockEntity::new, VillageBlocks.get("command_desk")).build());
        APOTHECARY_COT = Registry.register(BuiltInRegistries.BLOCK_ENTITY_TYPE, VillageBlocks.id("apothecary_cot"),
                FabricBlockEntityTypeBuilder.create(ApothecaryCotBlockEntity::new, VillageBlocks.get("apothecary_cot")).build());
    }

    private VillageBlockEntities() {}
}
