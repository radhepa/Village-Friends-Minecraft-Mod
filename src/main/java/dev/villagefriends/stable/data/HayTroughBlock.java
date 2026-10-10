package dev.villagefriends.stable.data;

import dev.villagefriends.FoundationBlock;
import dev.villagefriends.stable.yard.StallRules;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.IntegerProperty;
import net.minecraft.world.phys.BlockHitResult;

/**
 * A wooden trough holding up to four servings of hay. Stalled horses that are hurt, or foals, eat from the
 * nearest one; the stablehand tops it up. Owned by the stables package (the yard fills and reads {@link #HAY}).
 *
 * <p>Fill it with wheat (one serving) or a hay bale (all four); use it with an empty hand to see how full it is.
 * A comparator reads it too (empty 0, full 15).
 */
public class HayTroughBlock extends FoundationBlock {
    public static final IntegerProperty HAY = IntegerProperty.create("hay", 0, 4);

    public HayTroughBlock(BlockBehaviour.Properties properties, double[][] boxes) {
        super(properties, boxes);
        registerDefaultState(defaultBlockState().setValue(HAY, 0));
    }

    @Override protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) { super.createBlockStateDefinition(builder); builder.add(HAY); }

    @Override protected InteractionResult useItemOn(ItemStack stack, BlockState state, Level level, BlockPos pos, Player player, InteractionHand hand, BlockHitResult hit) {
        int add = stack.is(Items.WHEAT) ? 1 : stack.is(Items.HAY_BLOCK) ? StallRules.MAX_HAY : 0;
        if (add == 0) return InteractionResult.TRY_WITH_EMPTY_HAND;
        int hay = state.getValue(HAY), next = StallRules.fill(hay, add);
        if (!level.isClientSide()) {
            if (next != hay) {
                level.setBlock(pos, state.setValue(HAY, next), Block.UPDATE_ALL);
                stack.consume(1, player);
                level.playSound(null, pos, SoundEvents.GRASS_PLACE, SoundSource.BLOCKS, 1F, .9F);
            }
            player.sendOverlayMessage(Component.literal(fullness(next)));
        }
        return InteractionResult.SUCCESS;
    }
    @Override protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
        if (!player.getMainHandItem().isEmpty()) return InteractionResult.PASS;
        if (!level.isClientSide()) player.sendOverlayMessage(Component.literal(fullness(state.getValue(HAY))));
        return InteractionResult.SUCCESS;
    }
    @Override protected boolean hasAnalogOutputSignal(BlockState state) { return true; }
    @Override protected int getAnalogOutputSignal(BlockState state, Level level, BlockPos pos, Direction direction) {
        int hay = state.getValue(HAY);
        return hay >= StallRules.MAX_HAY ? 15 : hay * 3;
    }

    /** "The trough is empty..." / "Hay in the trough: 2 of 4." / "The trough is full of hay." */
    public static String fullness(int hay) {
        if (hay <= 0) return "The trough is empty. Fill it with wheat or a hay bale.";
        return hay >= StallRules.MAX_HAY ? "The trough is full of hay." : "Hay in the trough: " + hay + " of " + StallRules.MAX_HAY + ".";
    }
}
