package dev.villagefriends;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;

public final class NoticeBoardBlockEntity extends BlockEntity {
    public NoticeBoardBlockEntity(BlockPos pos, BlockState state) { super(VillageBlockEntities.NOTICE_BOARD, pos, state); }
    /** Integration hook for future settlement notices and recruitment contracts. */
    public void refreshNotices() {}
}
