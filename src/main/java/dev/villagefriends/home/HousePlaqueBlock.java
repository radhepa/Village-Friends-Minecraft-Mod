package dev.villagefriends.home;

import dev.villagefriends.FoundationBlock;
import dev.villagefriends.HousePlaqueBlockEntity;
import java.util.EnumMap;
import java.util.Locale;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.component.DataComponents;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.util.StringRepresentable;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.EntityBlock;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.EnumProperty;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.Shapes;
import net.minecraft.world.phys.shapes.VoxelShape;

/**
 * A House Plaque: hung on a wall (the way village houses have them) or standing on a post. Using it reads the
 * house out: its name, who lives there, its beds and workstation. Sneak and use it to make a house you built
 * private (nobody moves in) or open again. Put up in a house a player built, it finds the house's rooms and
 * beds ({@link Homes#scanPlaque}); renamed on an anvil first, it names the house.
 */
public final class HousePlaqueBlock extends FoundationBlock implements EntityBlock {
    public enum Mount implements StringRepresentable {
        WALL, STANDING;
        @Override public String getSerializedName() { return name().toLowerCase(Locale.ROOT); }
    }
    /** Hung on a wall (the default, which every plaque in a village structure has) or standing on a post. */
    public static final EnumProperty<Mount> MOUNT = EnumProperty.create("mount", Mount.class);
    /** The plaque on its post, facing north; {@code tools/create_foundation_assets.py} builds the model from these. */
    public static final double[][] STANDING = new double[][]{{7,0,7,9,8,9},{2,7,7,14,16,9}};
    private final EnumMap<Direction, VoxelShape> post = new EnumMap<>(Direction.class);

    public HousePlaqueBlock(BlockBehaviour.Properties properties, double[][] boxes) {
        super(properties, boxes);
        registerDefaultState(defaultBlockState().setValue(MOUNT, Mount.WALL));
        for (var direction : Direction.Plane.HORIZONTAL) {
            VoxelShape shape = Shapes.empty();
            for (var b : STANDING) {
                double[] r = switch (direction) {
                    case EAST -> new double[]{16-b[5], b[1], b[0], 16-b[2], b[4], b[3]};
                    case SOUTH -> new double[]{16-b[3], b[1], 16-b[5], 16-b[0], b[4], 16-b[2]};
                    case WEST -> new double[]{b[2], b[1], 16-b[3], b[5], b[4], 16-b[0]};
                    default -> b;
                };
                shape = Shapes.or(shape, box(r[0], r[1], r[2], r[3], r[4], r[5]));
            }
            post.put(direction, shape.optimize());
        }
    }
    public static boolean standing(BlockState state) { return state.hasProperty(MOUNT) && state.getValue(MOUNT) == Mount.STANDING; }

    @Override protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) { super.createBlockStateDefinition(builder); builder.add(MOUNT); }
    /** On the side of a block it hangs there, facing out; on top of one it stands on a post, facing the player. */
    @Override public BlockState getStateForPlacement(BlockPlaceContext context) {
        var face = context.getClickedFace();
        if (face.getAxis().isHorizontal()) return defaultBlockState().setValue(FACING, face).setValue(MOUNT, Mount.WALL);
        return defaultBlockState().setValue(FACING, context.getHorizontalDirection().getOpposite()).setValue(MOUNT, Mount.STANDING);
    }
    @Override protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
        return standing(state) ? post.get(state.getValue(FACING)) : super.getShape(state, level, pos, context);
    }
    @Override public BlockEntity newBlockEntity(BlockPos pos, BlockState state) { return new HousePlaqueBlockEntity(pos, state); }

    @Override public void setPlacedBy(Level level, BlockPos pos, BlockState state, LivingEntity placer, ItemStack stack) {
        super.setPlacedBy(level, pos, state, placer, stack);
        if (!(level instanceof ServerLevel server) || !(placer instanceof ServerPlayer player)) return;
        var custom = stack.get(DataComponents.CUSTOM_NAME);
        if (custom != null && server.getBlockEntity(pos) instanceof HousePlaqueBlockEntity plaque) plaque.name(custom.getString());
        String message = server.getBlockEntity(pos) instanceof HousePlaqueBlockEntity plaque ? plaque.scanForBeds() : Homes.scanPlaque(server, pos, "");
        // Failures go to chat too, so the reason stays readable.
        player.sendSystemMessage(Component.literal(message), true);
        if (!message.startsWith("★")) player.sendSystemMessage(Component.literal(message), false);
    }
    @Override protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
        if (!(player instanceof ServerPlayer sp)) return InteractionResult.SUCCESS;
        if (player.isSecondaryUseActive()) Homes.togglePrivate(sp, pos); else Homes.readout(sp, pos);
        return InteractionResult.SUCCESS_SERVER;
    }
}
