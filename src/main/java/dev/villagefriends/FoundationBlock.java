package dev.villagefriends;

import java.util.EnumMap;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.HorizontalDirectionalBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.Shapes;
import net.minecraft.world.phys.shapes.VoxelShape;

/** Simple directional geometry; detailed animated models can replace its JSON later. */
public class FoundationBlock extends HorizontalDirectionalBlock {
    private final EnumMap<Direction, VoxelShape> shapes = new EnumMap<>(Direction.class);

    public FoundationBlock(BlockBehaviour.Properties properties, double[][] boxes) {
        super(properties);
        registerDefaultState(stateDefinition.any().setValue(FACING, Direction.NORTH));
        for (Direction direction : Direction.Plane.HORIZONTAL) {
            VoxelShape shape = Shapes.empty();
            for (double[] b : boxes) {
                double[] rotated = switch (direction) {
                    case EAST -> new double[]{16-b[5], b[1], b[0], 16-b[2], b[4], b[3]};
                    case SOUTH -> new double[]{16-b[3], b[1], 16-b[5], 16-b[0], b[4], 16-b[2]};
                    case WEST -> new double[]{b[2], b[1], 16-b[3], b[5], b[4], 16-b[0]};
                    default -> b;
                };
                shape = Shapes.or(shape, box(rotated[0], rotated[1], rotated[2], rotated[3], rotated[4], rotated[5]));
            }
            shapes.put(direction, shape.optimize());
        }
    }

    @Override protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) { builder.add(FACING); }
    @Override public BlockState getStateForPlacement(BlockPlaceContext context) {
        return defaultBlockState().setValue(FACING, context.getHorizontalDirection().getOpposite());
    }
    @Override protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
        return shapes.get(state.getValue(FACING));
    }
}
