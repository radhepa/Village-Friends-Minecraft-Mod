package dev.villagefriends.fishing;

import com.mojang.logging.LogUtils;
import java.util.EnumMap;
import net.fabricmc.fabric.api.object.builder.v1.block.entity.FabricBlockEntityTypeBuilder;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.network.protocol.game.ClientboundBlockEntityDataPacket;
import net.minecraft.resources.ResourceKey;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.ProblemReporter;
import net.minecraft.world.Containers;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.EntityBlock;
import net.minecraft.world.level.block.HorizontalDirectionalBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.material.MapColor;
import net.minecraft.world.level.storage.TagValueOutput;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

/**
 * The Trophy Mount: a wooden plaque for the wall. Right-click it with a fish to mount it (a record catch or a
 * legend shows its size, who caught it and when); right-click it empty-handed to read the plate, and sneak and
 * right-click to take the fish down. The fish is drawn on the plaque by the client's trophy renderer.
 */
public final class TrophyMount extends HorizontalDirectionalBlock implements EntityBlock {
    public static Block BLOCK;
    public static BlockEntityType<Entity> TYPE;
    private final EnumMap<Direction, VoxelShape> shapes = new EnumMap<>(Direction.class);

    TrophyMount(BlockBehaviour.Properties properties) {
        super(properties);
        shapes.put(Direction.NORTH, box(2, 3, 15, 14, 13, 16));
        shapes.put(Direction.SOUTH, box(2, 3, 0, 14, 13, 1));
        shapes.put(Direction.EAST, box(0, 3, 2, 1, 13, 14));
        shapes.put(Direction.WEST, box(15, 3, 2, 16, 13, 14));
    }

    static void register() {
        var id = Fishing.id("trophy_mount");
        BLOCK = Registry.register(BuiltInRegistries.BLOCK, id, new TrophyMount(BlockBehaviour.Properties.of().setId(ResourceKey.create(Registries.BLOCK, id))
                .mapColor(MapColor.WOOD).strength(1.0F).sound(SoundType.WOOD).noCollision().noOcclusion().ignitedByLava()));
        Registry.register(BuiltInRegistries.ITEM, id, new BlockItem(BLOCK, new Item.Properties().setId(ResourceKey.create(Registries.ITEM, id)).useBlockDescriptionPrefix()));
        TYPE = Registry.register(BuiltInRegistries.BLOCK_ENTITY_TYPE, id, FabricBlockEntityTypeBuilder.create(Entity::new, BLOCK).build());
    }

    @Override protected void createBlockStateDefinition(net.minecraft.world.level.block.state.StateDefinition.Builder<Block, BlockState> builder) { builder.add(FACING); }
    @Override public BlockState getStateForPlacement(BlockPlaceContext context) {
        var face = context.getClickedFace();
        return defaultBlockState().setValue(FACING, face.getAxis().isHorizontal() ? face : context.getHorizontalDirection().getOpposite());
    }
    @Override protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) { return shapes.get(state.getValue(FACING)); }
    @Override public BlockEntity newBlockEntity(BlockPos pos, BlockState state) { return new Entity(pos, state); }

    @Override protected InteractionResult useItemOn(ItemStack held, BlockState state, Level level, BlockPos pos, Player player, InteractionHand hand, BlockHitResult hit) {
        if (!held.is(FishingApi.FISH) || !(level.getBlockEntity(pos) instanceof Entity mount) || !mount.fish.isEmpty()) return InteractionResult.TRY_WITH_EMPTY_HAND;
        if (!level.isClientSide()) {
            mount.set(held.copyWithCount(1));
            if (!player.getAbilities().instabuild) held.shrink(1);
            level.playSound(null, pos, SoundEvents.ITEM_FRAME_ADD_ITEM, SoundSource.BLOCKS, 1, 1);
            player.sendOverlayMessage(plate(mount.fish));
        }
        return InteractionResult.SUCCESS;
    }
    @Override protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
        if (!(level.getBlockEntity(pos) instanceof Entity mount) || mount.fish.isEmpty()) return InteractionResult.PASS;
        if (!level.isClientSide()) {
            if (player.isSecondaryUseActive()) {
                var fish = mount.fish.copy();
                mount.set(ItemStack.EMPTY);
                if (!player.getInventory().add(fish) && player.level() instanceof net.minecraft.server.level.ServerLevel sl) player.spawnAtLocation(sl, fish);
                level.playSound(null, pos, SoundEvents.ITEM_FRAME_REMOVE_ITEM, SoundSource.BLOCKS, 1, 1);
            } else player.sendOverlayMessage(plate(mount.fish));
        }
        return InteractionResult.SUCCESS;
    }
    /** What the brass plate says. */
    static Component plate(ItemStack fish) {
        var trophy = fish.get(Fishing.TROPHY);
        var name = Component.translatable(fish.getItem().getDescriptionId()).withStyle(ChatFormatting.GOLD);
        if (trophy == null) return name;
        return name.append(Component.literal(" · " + Catches.cm(trophy.size()) + " · caught by " + trophy.catcher() + ", "
                + dev.villagefriends.social.Calendar.date(trophy.day()) + ", Year " + dev.villagefriends.social.Calendar.year(trophy.day())).withStyle(ChatFormatting.YELLOW));
    }

    /** Holds the mounted fish. */
    public static final class Entity extends BlockEntity {
        private ItemStack fish = ItemStack.EMPTY;
        public Entity(BlockPos pos, BlockState state) { super(TYPE, pos, state); }
        public ItemStack fish() { return fish; }
        void set(ItemStack stack) {
            fish = stack;
            setChanged();
            if (level != null) level.sendBlockUpdated(worldPosition, getBlockState(), getBlockState(), Block.UPDATE_ALL);
        }
        @Override protected void loadAdditional(ValueInput input) {
            super.loadAdditional(input);
            fish = input.read("Fish", ItemStack.CODEC).orElse(ItemStack.EMPTY);
        }
        @Override protected void saveAdditional(ValueOutput output) {
            super.saveAdditional(output);
            if (!fish.isEmpty()) output.store("Fish", ItemStack.CODEC, fish);
        }
        @Override public ClientboundBlockEntityDataPacket getUpdatePacket() { return ClientboundBlockEntityDataPacket.create(this); }
        @Override public CompoundTag getUpdateTag(HolderLookup.Provider registries) {
            try (var reporter = new ProblemReporter.ScopedCollector(problemPath(), LogUtils.getLogger())) {
                var output = TagValueOutput.createWithContext(reporter, registries);
                if (!fish.isEmpty()) output.store("Fish", ItemStack.CODEC, fish);
                return output.buildResult();
            }
        }
        @Override public void preRemoveSideEffects(BlockPos pos, BlockState state) {
            if (level != null && !fish.isEmpty()) Containers.dropItemStack(level, pos.getX() + .5, pos.getY() + .5, pos.getZ() + .5, fish);
        }
    }
}
