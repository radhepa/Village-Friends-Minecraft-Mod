package dev.villagefriends;

import net.fabricmc.fabric.api.creativetab.v1.CreativeModeTabEvents;
import net.minecraft.core.*;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.*;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.*;
import net.minecraft.server.level.*;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.*;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.*;
import net.minecraft.world.level.block.*;
import net.minecraft.world.level.block.state.*;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.shapes.*;

public final class VillageMarkerBlock extends HorizontalDirectionalBlock {
    public static VillageMarkerBlock BLOCK;
    public static BlockItem ITEM;
    public VillageMarkerBlock(BlockBehaviour.Properties properties) { super(properties); registerDefaultState(stateDefinition.any().setValue(FACING,Direction.NORTH)); }
    public static void register() {
        var id=Identifier.fromNamespaceAndPath("villagefriends","village_marker");
        BLOCK=Registry.register(BuiltInRegistries.BLOCK,id,new VillageMarkerBlock(BlockBehaviour.Properties.of().setId(ResourceKey.create(Registries.BLOCK,id)).strength(2.0F).sound(SoundType.WOOD).noOcclusion()));
        ITEM=Registry.register(BuiltInRegistries.ITEM,id,new BlockItem(BLOCK,new Item.Properties().setId(ResourceKey.create(Registries.ITEM,id)).useBlockDescriptionPrefix()));
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.FUNCTIONAL_BLOCKS).register(entries -> entries.accept(ITEM));
        net.fabricmc.fabric.api.event.player.PlayerBlockBreakEvents.AFTER.register((level,player,pos,state,entity) -> {
            if(state.is(BLOCK) && level instanceof ServerLevel server) VillageSettlements.unmark(server,pos);
        });
    }
    @Override protected void createBlockStateDefinition(StateDefinition.Builder<Block,BlockState> builder) { builder.add(FACING); }
    @Override public BlockState getStateForPlacement(BlockPlaceContext context) { return defaultBlockState().setValue(FACING,context.getHorizontalDirection().getOpposite()); }
    @Override protected VoxelShape getShape(BlockState state,BlockGetter level,BlockPos pos,CollisionContext context) {
        return state.getValue(FACING).getAxis()==Direction.Axis.Z ? Shapes.or(box(3,0,3,13,3,13),box(7,3,7,9,10,9),box(2,8,6,14,16,10))
                : Shapes.or(box(3,0,3,13,3,13),box(7,3,7,9,10,9),box(6,8,2,10,16,14));
    }
    @Override public void setPlacedBy(Level level,BlockPos pos,BlockState state,LivingEntity placer,ItemStack stack) {
        if(!(level instanceof ServerLevel server))return;
        var chosen=stack.get(DataComponents.CUSTOM_NAME);
        var village=VillageSettlements.mark(server,pos,chosen==null?null:chosen.getString());
        if(placer instanceof ServerPlayer p)p.sendSystemMessage(Component.literal("Village marker: "+village.name()+". Nearby residents now belong to this settlement."),false);
    }
    @Override protected InteractionResult useWithoutItem(BlockState state,Level level,BlockPos pos,Player player,BlockHitResult hit) {
        if(level instanceof ServerLevel server && player instanceof ServerPlayer p) {
            var village=VillageSettlements.discover(server,pos);
            if(village==null)village=VillageSettlements.mark(server,pos,null);
            String id=village.id();
            long count=CompanionController.loaded.stream().filter(v->v.level()==level && VillageFriends.target(v).getAttached(VillageFriends.HOME)!=null && VillageFriends.target(v).getAttached(VillageFriends.HOME).village().equals(id)).count();
            p.sendSystemMessage(Component.literal(village.name()+" · "+count+" residents nearby. Name a Village Marker in an anvil before placing it to rename the village."),false);
        }
        return level.isClientSide()?InteractionResult.SUCCESS:InteractionResult.SUCCESS_SERVER;
    }
}
