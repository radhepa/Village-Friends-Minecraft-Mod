package dev.villagefriends.stable.data;

import dev.villagefriends.FoundationBlock;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.IntegerProperty;

/**
 * A wooden trough holding up to four servings of hay. Stalled horses that are hurt, or foals, eat from the
 * nearest one; the stablehand tops it up. Owned by the stables package (the yard fills and reads {@link #HAY}).
 */
public class HayTroughBlock extends FoundationBlock {
    public static final IntegerProperty HAY = IntegerProperty.create("hay", 0, 4);

    public HayTroughBlock(BlockBehaviour.Properties properties, double[][] boxes) {
        super(properties, boxes);
        registerDefaultState(defaultBlockState().setValue(HAY, 0));
    }

    @Override protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) { super.createBlockStateDefinition(builder); builder.add(HAY); }
}
