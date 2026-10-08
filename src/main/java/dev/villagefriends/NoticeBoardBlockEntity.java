package dev.villagefriends;

import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;

/** Keeps a notice board's pinned notes in step with its village's notices ({@link VillageQuests}). */
public final class NoticeBoardBlockEntity extends BlockEntity {
    public NoticeBoardBlockEntity(BlockPos pos, BlockState state) { super(VillageBlockEntities.NOTICE_BOARD, pos, state); }

    /** Every five seconds or so: new notices go up in the morning, and taken ones come down. */
    void tick(Level level, BlockPos pos, BlockState state) {
        if (Math.floorMod(level.getGameTime() + pos.asLong(), 100L) == 0) refreshNotices();
    }
    /** Pins up today's notices and shows how many are up for grabs. */
    public void refreshNotices() {
        if (!(level instanceof ServerLevel server) || !getBlockState().hasProperty(NoticeBoardBlock.NOTES)) return;
        int notes = VillageQuests.pinned(server, worldPosition);
        var state = getBlockState();
        if (state.getValue(NoticeBoardBlock.NOTES) != notes) server.setBlock(worldPosition, state.setValue(NoticeBoardBlock.NOTES, notes), 3);
    }
}
