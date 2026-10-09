package dev.villagefriends.hearth;

import java.util.EnumMap;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.RandomSource;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.EntityBlock;
import net.minecraft.world.level.block.HorizontalDirectionalBlock;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityTicker;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.block.state.properties.BooleanProperty;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.Shapes;
import net.minecraft.world.phys.shapes.VoxelShape;

/**
 * A kitchen station block: right-click to open it. The pot steams and bubbles while it cooks, the oven
 * glows and smokes while it burns, and the prep table is plain wood.
 */
public abstract class StationBlock extends HorizontalDirectionalBlock implements EntityBlock {
    public static final BooleanProperty LIT = BlockStateProperties.LIT;
    public static final BooleanProperty FILLED = BooleanProperty.create("filled");
    public final Station station;
    private final EnumMap<Direction, VoxelShape> shapes = new EnumMap<>(Direction.class);

    protected StationBlock(Properties properties, Station station, double[][] boxes) {
        super(properties);
        this.station = station;
        for (Direction d : Direction.Plane.HORIZONTAL) {
            VoxelShape shape = Shapes.empty();
            for (double[] b : boxes) {
                double[] r = switch (d) {
                    case EAST -> new double[]{16 - b[5], b[1], b[0], 16 - b[2], b[4], b[3]};
                    case SOUTH -> new double[]{16 - b[3], b[1], 16 - b[5], 16 - b[0], b[4], 16 - b[2]};
                    case WEST -> new double[]{b[2], b[1], 16 - b[3], b[5], b[4], 16 - b[0]};
                    default -> b;
                };
                shape = Shapes.or(shape, box(r[0], r[1], r[2], r[3], r[4], r[5]));
            }
            shapes.put(d, shape.optimize());
        }
    }

    @Override public BlockState getStateForPlacement(BlockPlaceContext context) {
        return defaultBlockState().setValue(FACING, context.getHorizontalDirection().getOpposite());
    }
    @Override protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
        return shapes.get(state.getValue(FACING));
    }
    @Override public BlockEntity newBlockEntity(BlockPos pos, BlockState state) { return new StationBlockEntity(pos, state); }
    @SuppressWarnings("unchecked")
    @Override public <T extends BlockEntity> BlockEntityTicker<T> getTicker(Level level, BlockState state, BlockEntityType<T> type) {
        if (level.isClientSide() || type != HearthBlocks.STATION) return null;
        return (BlockEntityTicker<T>) (BlockEntityTicker<StationBlockEntity>) StationBlockEntity::serverTick;
    }
    @Override protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
        if (level.isClientSide()) return InteractionResult.SUCCESS;
        if (level.getBlockEntity(pos) instanceof StationBlockEntity station && player instanceof ServerPlayer p) {
            station.cook(p);
            p.openMenu(station);
        }
        return InteractionResult.SUCCESS_SERVER;
    }
    @Override protected boolean hasAnalogOutputSignal(BlockState state) { return true; }
    @Override protected int getAnalogOutputSignal(BlockState state, Level level, BlockPos pos, Direction direction) {
        return level.getBlockEntity(pos) instanceof StationBlockEntity s ? s.signal() : 0;
    }

    /** The cooking pot: sits on a lit campfire or fire, takes a bowl or bottle, steams and bubbles while it cooks. */
    public static final class Pot extends StationBlock {
        public Pot(Properties properties) {
            super(properties, Station.POT, new double[][]{{2, 0, 2, 14, 10, 14}});
            registerDefaultState(stateDefinition.any().setValue(FACING, Direction.NORTH).setValue(LIT, false).setValue(FILLED, false));
        }
        @Override protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) { builder.add(FACING, LIT, FILLED); }
        @Override public void animateTick(BlockState state, Level level, BlockPos pos, RandomSource random) {
            if (!state.getValue(LIT)) return;
            double x = pos.getX() + .5, y = pos.getY() + .62, z = pos.getZ() + .5;
            // Steam curling up off the pot, and bubbles breaking on the surface.
            if (random.nextInt(3) == 0) level.addParticle(ParticleTypes.WHITE_SMOKE, x + random.nextGaussian() * .12, y + .2, z + random.nextGaussian() * .12, 0, .035, 0);
            if (random.nextInt(2) == 0) level.addParticle(ParticleTypes.BUBBLE_POP, x + (random.nextDouble() - .5) * .55, y, z + (random.nextDouble() - .5) * .55, 0, .01, 0);
            if (random.nextInt(9) == 0) level.playLocalSound(x, y, z, SoundEvents.BUBBLE_COLUMN_BUBBLE_POP, SoundSource.BLOCKS, .35F, .8F + random.nextFloat() * .3F, false);
        }
    }

    /** The clay oven: burns fuel like a furnace; fire glows in its mouth and smoke leaves the vent. */
    public static final class Oven extends StationBlock {
        public Oven(Properties properties) {
            super(properties.lightLevel(s -> s.getValue(LIT) ? 12 : 0), Station.OVEN, new double[][]{{0, 0, 0, 16, 16, 16}});
            registerDefaultState(stateDefinition.any().setValue(FACING, Direction.NORTH).setValue(LIT, false));
        }
        @Override protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) { builder.add(FACING, LIT); }
        @Override public void animateTick(BlockState state, Level level, BlockPos pos, RandomSource random) {
            if (!state.getValue(LIT)) return;
            double x = pos.getX() + .5, y = pos.getY(), z = pos.getZ() + .5;
            var front = state.getValue(FACING);
            double fx = x + front.getStepX() * .52, fz = z + front.getStepZ() * .52;
            if (random.nextInt(2) == 0) level.addParticle(ParticleTypes.SMOKE, x + random.nextGaussian() * .1, y + 1.05, z + random.nextGaussian() * .1, 0, .04, 0);
            if (random.nextInt(4) == 0) level.addParticle(ParticleTypes.FLAME, fx + (random.nextDouble() - .5) * .3, y + .25, fz, 0, 0, 0);
            if (random.nextInt(12) == 0) level.playLocalSound(x, y, z, SoundEvents.FURNACE_FIRE_CRACKLE, SoundSource.BLOCKS, .8F, 1F, false);
        }
    }

    /** The prep table: chopping, kneading and assembling; no heat needed. */
    public static final class Prep extends StationBlock {
        public Prep(Properties properties) {
            super(properties, Station.PREP, new double[][]{{0, 0, 0, 16, 15, 16}});
            registerDefaultState(stateDefinition.any().setValue(FACING, Direction.NORTH));
        }
        @Override protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) { builder.add(FACING); }
    }
}
