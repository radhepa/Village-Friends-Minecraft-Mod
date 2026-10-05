package dev.villagefriends;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;

public final class HousePlaqueBlockEntity extends BlockEntity {
    public HousePlaqueBlockEntity(BlockPos pos, BlockState state) { super(VillageBlockEntities.HOUSE_PLAQUE, pos, state); }
    /** Integration hook. Housing flood-fill and bed assignment are implemented in a later phase. */
    public void scanForBeds() {}
    public void scanForWorkstations() {}
}
