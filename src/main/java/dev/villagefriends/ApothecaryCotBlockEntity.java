package dev.villagefriends;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;

public final class ApothecaryCotBlockEntity extends BlockEntity {
    public ApothecaryCotBlockEntity(BlockPos pos, BlockState state) { super(VillageBlockEntities.APOTHECARY_COT, pos, state); }
    /** Integration hook. No patient transfer, revival timer or ticking runs in Phase 1. */
    public void updatePatient() {}
}
