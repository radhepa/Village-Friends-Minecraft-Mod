package dev.villagefriends.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.math.Axis;
import dev.villagefriends.fishing.TrophyMount;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.blockentity.BlockEntityRenderer;
import net.minecraft.client.renderer.blockentity.BlockEntityRendererProvider;
import net.minecraft.client.renderer.blockentity.state.BlockEntityRenderState;
import net.minecraft.client.renderer.feature.ModelFeatureRenderer;
import net.minecraft.client.renderer.item.ItemModelResolver;
import net.minecraft.client.renderer.item.ItemStackRenderState;
import net.minecraft.client.renderer.state.level.CameraRenderState;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.core.Direction;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.level.block.HorizontalDirectionalBlock;
import net.minecraft.world.phys.Vec3;
import org.jspecify.annotations.Nullable;

/** Draws the mounted fish on a Trophy Mount, flat against the plaque like a fish in an item frame, a little larger. */
public final class TrophyMountRenderer implements BlockEntityRenderer<TrophyMount.Entity, TrophyMountRenderer.State> {
    public static final class State extends BlockEntityRenderState {
        final ItemStackRenderState item = new ItemStackRenderState();
        boolean shown;
        Direction facing = Direction.NORTH;
    }
    private final ItemModelResolver items;

    public TrophyMountRenderer(BlockEntityRendererProvider.Context context) { this.items = context.itemModelResolver(); }

    @Override public State createRenderState() { return new State(); }

    @Override public void extractRenderState(TrophyMount.Entity mount, State state, float partialTicks, Vec3 camera, ModelFeatureRenderer.@Nullable CrumblingOverlay breaking) {
        BlockEntityRenderer.super.extractRenderState(mount, state, partialTicks, camera, breaking);
        state.facing = mount.getBlockState().getValue(HorizontalDirectionalBlock.FACING);
        state.shown = !mount.fish().isEmpty();
        if (state.shown) items.updateForTopItem(state.item, mount.fish(), ItemDisplayContext.FIXED, mount.getLevel(), null, (int) mount.getBlockPos().asLong());
    }

    @Override public void submit(State state, PoseStack pose, SubmitNodeCollector collector, CameraRenderState camera) {
        if (!state.shown) return;
        pose.pushPose();
        pose.translate(.5F, .53F, .5F);
        pose.rotateDegrees(Axis.YP, 180 - state.facing.toYRot());
        pose.translate(0, 0, .41F);
        pose.scale(.72F, .72F, .72F);
        state.item.submit(pose, collector, state.lightCoords, OverlayTexture.NO_OVERLAY, 0);
        pose.popPose();
    }
}
