package dev.villagefriends;

import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.projectile.Projectile;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.EntityBlock;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityTicker;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.block.state.properties.BooleanProperty;
import net.minecraft.world.level.block.state.properties.IntegerProperty;
import net.minecraft.world.phys.BlockHitResult;

/**
 * A profession's workstation that does something: players use it (cook on the stove, saw logs, press
 * herbs, play the music stand...) and its resident works at it during working hours (see {@link Workstations}).
 */
public class WorkstationBlock extends FoundationBlock implements EntityBlock {
    public static final BooleanProperty LIT = BlockStateProperties.LIT;
    /** The easel's canvas: 0 blank, 1 a sketch, 2-8 a finished painting. */
    public static final IntegerProperty ART = IntegerProperty.create("art", 0, 8);
    public static final int SKETCH = 1, FIRST_PAINTING = 2, PAINTINGS = 7;

    public enum Station {
        TRAINING_DUMMY("training_dummy", "knight"), ARCHERY_TARGET("archery_target", "archer"), KITCHEN_STOVE("kitchen_stove", "cook"),
        DRINKS_BARREL("drinks_barrel", "tavern_keeper"), TAP_STAND("tap_stand", "tavern_keeper"), ALCHEMICAL_PRESS("alchemical_press", "apothecary"),
        EASEL_CANVAS("easel_canvas", "painter"), MUSIC_STAND("music_stand", "bard"), SEWING_TABLE("sewing_table", "tailor"),
        SAWMILL("sawmill", "carpenter"), ARCHIVES("archives", "scholar");
        public final String block, job;
        Station(String block, String job) { this.block = block; this.job = job; }
        public static Station of(String block) {
            for (var s : values()) if (s.block.equals(block)) return s;
            return null;
        }
    }
    private final Station station;

    public WorkstationBlock(BlockBehaviour.Properties properties, double[][] boxes, Station station) {
        super(properties, boxes);
        this.station = station;
    }
    public Station station() { return station; }

    @Override public BlockEntity newBlockEntity(BlockPos pos, BlockState state) { return new WorkstationBlockEntity(pos, state); }
    @Override public <T extends BlockEntity> BlockEntityTicker<T> getTicker(Level level, BlockState state, BlockEntityType<T> type) {
        if (level.isClientSide() || station != Station.KITCHEN_STOVE || type != VillageBlockEntities.WORKSTATION) return null;
        return (l, pos, s, entity) -> WorkstationBlockEntity.stoveTick((ServerLevel) l, pos, s, (WorkstationBlockEntity) entity);
    }

    @Override protected InteractionResult useItemOn(ItemStack stack, BlockState state, Level level, BlockPos pos, Player player, InteractionHand hand, BlockHitResult hit) {
        if (stack.isEmpty()) return InteractionResult.TRY_WITH_EMPTY_HAND;
        return Workstations.use(station, state, level, pos, player, hand, stack);
    }
    @Override protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
        return Workstations.use(station, state, level, pos, player, InteractionHand.MAIN_HAND, ItemStack.EMPTY);
    }
    @Override protected void onProjectileHit(Level level, BlockState state, BlockHitResult hit, Projectile projectile) {
        if (station == Station.ARCHERY_TARGET) Workstations.targetHit(level, state, hit, projectile);
    }
    @Override public void animateTick(BlockState state, Level level, BlockPos pos, RandomSource random) {
        if (station != Station.KITCHEN_STOVE || !state.getValue(LIT)) return;
        var facing = state.getValue(FACING);
        if (random.nextInt(3) == 0) {
            // Smoke curls from the chimney pipe at the back.
            double x = pos.getX() + .5 - facing.getStepX() * .25 + facing.getClockWise().getStepX() * .22, z = pos.getZ() + .5 - facing.getStepZ() * .25 + facing.getClockWise().getStepZ() * .22;
            level.addParticle(ParticleTypes.SMOKE, x, pos.getY() + 1.3, z, 0, .03, 0);
        }
        if (random.nextInt(5) == 0) {
            double x = pos.getX() + .5 + facing.getStepX() * .52, z = pos.getZ() + .5 + facing.getStepZ() * .52;
            level.addParticle(ParticleTypes.FLAME, x + (random.nextDouble() - .5) * .3, pos.getY() + .28, z + (random.nextDouble() - .5) * .3, 0, 0, 0);
        }
        if (random.nextInt(60) == 0) level.playLocalSound(pos, net.minecraft.sounds.SoundEvents.FURNACE_FIRE_CRACKLE, net.minecraft.sounds.SoundSource.BLOCKS, .6F, 1, false);
    }

    /** The stove can be lit. */
    public static final class Lit extends WorkstationBlock {
        public Lit(BlockBehaviour.Properties properties, double[][] boxes, Station station) {
            super(properties, boxes, station);
            registerDefaultState(defaultBlockState().setValue(LIT, false));
        }
        @Override protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) { super.createBlockStateDefinition(builder); builder.add(LIT); }
    }
    /** The easel holds a canvas: blank, sketched or painted. */
    public static final class Canvas extends WorkstationBlock {
        public Canvas(BlockBehaviour.Properties properties, double[][] boxes, Station station) {
            super(properties, boxes, station);
            registerDefaultState(defaultBlockState().setValue(ART, 0));
        }
        @Override protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) { super.createBlockStateDefinition(builder); builder.add(ART); }
    }
}
