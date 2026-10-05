package dev.villagefriends;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;

public final class CommandDeskBlockEntity extends BlockEntity {
    public CommandDeskBlockEntity(BlockPos pos, BlockState state) { super(VillageBlockEntities.COMMAND_DESK, pos, state); }
    /** Integration hooks for future patrol and formation controllers. */
    public void updatePatrolAssignments() {}
    public void refreshGuardRoster() {}
}
