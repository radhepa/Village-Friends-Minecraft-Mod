package dev.villagefriends;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.block.EntityBlock;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;

public final class FoundationEntityBlock extends FoundationBlock implements EntityBlock {
    public enum Kind { HOUSE_PLAQUE, NOTICE_BOARD, COMMAND_DESK, APOTHECARY_COT }
    private final Kind kind;

    public FoundationEntityBlock(BlockBehaviour.Properties properties, double[][] boxes, Kind kind) {
        super(properties, boxes);
        this.kind = kind;
    }

    @Override public BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
        return switch (kind) {
            case HOUSE_PLAQUE -> new HousePlaqueBlockEntity(pos, state);
            case NOTICE_BOARD -> new NoticeBoardBlockEntity(pos, state);
            case COMMAND_DESK -> new CommandDeskBlockEntity(pos, state);
            case APOTHECARY_COT -> new ApothecaryCotBlockEntity(pos, state);
        };
    }
}
