package dev.villagefriends;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.EntityBlock;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityTicker;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.IntegerProperty;

/**
 * A village notice board. {@code notes} (0-3) is how many notices are pinned up for grabs, so players can
 * see from across the square when there's work posted; the board entity keeps it current.
 */
public final class NoticeBoardBlock extends FoundationBlock implements EntityBlock {
    public static final IntegerProperty NOTES = IntegerProperty.create("notes", 0, 3);

    public NoticeBoardBlock(BlockBehaviour.Properties properties, double[][] boxes) {
        super(properties, boxes);
        registerDefaultState(defaultBlockState().setValue(NOTES, 0));
    }
    @Override protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) { super.createBlockStateDefinition(builder); builder.add(NOTES); }
    @Override public BlockEntity newBlockEntity(BlockPos pos, BlockState state) { return new NoticeBoardBlockEntity(pos, state); }
    @Override @SuppressWarnings("unchecked")
    public <T extends BlockEntity> BlockEntityTicker<T> getTicker(Level level, BlockState state, BlockEntityType<T> type) {
        return level.isClientSide() || type != VillageBlockEntities.NOTICE_BOARD ? null
                : (BlockEntityTicker<T>) (BlockEntityTicker<NoticeBoardBlockEntity>) (l, pos, s, board) -> board.tick(l, pos, s);
    }
}
