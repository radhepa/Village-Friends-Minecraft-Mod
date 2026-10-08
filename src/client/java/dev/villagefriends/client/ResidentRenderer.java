package dev.villagefriends.client;

import dev.villagefriends.ResidentAppearance;
import dev.villagefriends.ResidentMotion;
import dev.villagefriends.VillageFriends;
import net.fabricmc.fabric.api.attachment.v1.AttachmentTarget;
import net.minecraft.client.Minecraft;
import net.minecraft.client.model.geom.ModelLayers;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.HumanoidMobRenderer;
import net.minecraft.client.renderer.rendertype.RenderTypes;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.util.Mth;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.state.level.CameraRenderState;

/** Vanilla villagers retain their trades and AI, but use the actual player mesh and skin layout. */
public final class ResidentRenderer extends HumanoidMobRenderer<Villager, ResidentRenderState, HumanoidModel<ResidentRenderState>> {
    /** Set while a GUI portrait is extracted; the portrait follows the mouse, not the camera. */
    public static boolean portrait;
    public ResidentRenderer(EntityRendererProvider.Context context) {
        // Use the vanilla player's exact mesh, with a mob state: AvatarRenderState is
        // dispatched to the player renderer even when it originated from a villager.
        super(context, new ResidentModel(false), new ResidentModel(true), 0.45F);
        this.addLayer(new WardrobeLayer(this));
        this.addLayer(new PartyHatLayer(this));
        this.addLayer(new net.minecraft.client.renderer.entity.layers.HumanoidArmorLayer<>(this,
                ModelLayers.PLAYER_ARMOR.map(layer -> new ResidentArmorModel(context.bakeLayer(layer))),
                net.minecraft.client.model.player.PlayerModel.createArmorMeshSet(new net.minecraft.client.model.geom.builders.CubeDeformation(.5F),new net.minecraft.client.model.geom.builders.CubeDeformation(1F))
                    .map(mesh -> new ResidentArmorModel(net.minecraft.client.model.geom.builders.LayerDefinition.create(mesh,64,32).apply(HumanoidModel.BABY_TRANSFORMER).bakeRoot())),
                context.getEquipmentRenderer()));
    }

    @Override public ResidentRenderState createRenderState() { return new ResidentRenderState(); }
    @Override protected HumanoidModel.ArmPose getArmPose(Villager villager, net.minecraft.world.entity.HumanoidArm arm) {
        if (villager.isUsingItem() && villager.getUseItem().getItem() instanceof net.minecraft.world.item.BowItem)
            return arm == villager.getMainArm() ? HumanoidModel.ArmPose.BOW_AND_ARROW : HumanoidModel.ArmPose.EMPTY;
        return super.getArmPose(villager, arm);
    }
    @Override public Identifier getTextureLocation(ResidentRenderState state) { return state.texture; }
    /** Someone lying hurt: flat on their back, slumped a little to one side, centered over their hitbox. */
    @Override protected void setupRotations(ResidentRenderState state, PoseStack pose, float bodyRot, float scale) {
        if(!state.injured) { super.setupRotations(state, pose, bodyRot, scale); return; }
        float side=(state.motionSeed&1)==0?1:-1;
        pose.rotateDegrees(com.mojang.math.Axis.YP, 180-bodyRot);
        pose.translate(0, state.isBaby?.08F:.16F, state.isBaby?-.45F:-.9F);
        pose.rotateDegrees(com.mojang.math.Axis.XP, 90);
        pose.rotateDegrees(com.mojang.math.Axis.YP, 14*side);
    }
    @Override protected float getShadowRadius(ResidentRenderState state) { return super.getShadowRadius(state)*(state.isBaby?.6F:1F); }

    @Override public void extractRenderState(Villager villager, ResidentRenderState state, float delta) {
        super.extractRenderState(villager, state, delta);
        state.motionSeed=ResidentMotion.seed(villager.getUUID());
        state.injured=villager.hasPose(net.minecraft.world.entity.Pose.SLEEPING) && dev.villagefriends.Knockouts.injured(villager);
        // The pose and the injured flag arrive separately; the lying hitbox needs both, so refit it once both are here.
        if(state.injured && villager.getBbWidth()<.5F && !villager.isBaby()) villager.refreshDimensions();
        state.onGround=villager.onGround();
        state.partyHat=!state.injured && dev.villagefriends.Birthdays.wearingHat(villager);
        state.eyeLookX=state.eyeLookY=state.attention=0;
        var camera=Minecraft.getInstance().getCameraEntity();
        if(camera!=null && villager.isAlive() && !villager.isSleeping()) {
            var offset=camera.getEyePosition(delta).subtract(villager.getEyePosition(delta));
            double horizontal=Math.sqrt(offset.x*offset.x+offset.z*offset.z);
            float yaw=(float)Math.toDegrees(Math.atan2(-offset.x, offset.z));
            float relative=Mth.wrapDegrees(yaw-Mth.rotLerp(delta,villager.yHeadRotO,villager.yHeadRot));
            // Eye contact only with someone nearby and already in front of the face.
            float proximity=ResidentMotion.smooth((float)((6-offset.length())/2));
            float facing=ResidentMotion.smooth((65-Math.abs(relative))/25);
            state.attention=proximity*facing;
            state.eyeLookX=Mth.clamp(relative/65, -.28F, .28F)*state.attention;
            float pitch=(float)-Math.toDegrees(Math.atan2(offset.y, horizontal));
            state.eyeLookY=Mth.clamp((pitch-state.xRot)/90, -.12F, .12F)*state.attention;
        }
        // Names remain visible during play; the conversation card already shows
        // the resident's name, so avoid a large floating label behind its portrait.
        if (Minecraft.getInstance().gui.screen() instanceof FriendshipScreen) state.nameTag = null;
        String look = ((AttachmentTarget)villager).getAttached(VillageFriends.LOOK);
        if (look == null) look = ResidentAppearance.generate(villager.getUUID());
        String job = villager.isBaby() ? "none" : VillageFriends.profession(villager);
        state.outfit = ResidentSkins.outfit(look, job);
        state.texture = ResidentSkins.texture(look, job);
        ResidentLife.of(villager).extract(villager, state, portrait);
        TavernClient.extract(villager, state, portrait);
        PlaytimeClient.extract(villager, state, portrait);
        var bubble = portrait ? null : EmoteBubbles.get(villager.getId());
        state.bubble = bubble;
        state.bubbleAge = bubble == null ? 0 : bubble.age(delta);
    }

    @Override public void submit(ResidentRenderState state, PoseStack pose, SubmitNodeCollector collector, CameraRenderState camera) {
        super.submit(state, pose, collector, camera);
        TavernClient.submit(state, pose, collector);
        PlaytimeClient.submit(state, pose, collector);
        if (state.bubble != null && state.distanceToCameraSq < 40 * 40) submitBubble(state, pose, collector, camera);
    }
    /** Draws the emote bubble as a camera-facing card above the head (and above the name, when shown). */
    private static void submitBubble(ResidentRenderState state, PoseStack pose, SubmitNodeCollector collector, CameraRenderState camera) {
        var bubble = state.bubble; float age = state.bubbleAge;
        float scale = EmoteBubbles.scale(bubble, age);
        if (scale <= .01F) return;
        var anchor = state.nameTagAttachment;
        double y = state.nameTag != null && anchor != null ? anchor.y + .78 : state.boundingBoxHeight + .32;
        pose.pushPose();
        pose.translate(anchor == null ? 0 : anchor.x, y, anchor == null ? 0 : anchor.z);
        pose.rotate(camera.orientation);
        float pixel = .019F * scale;
        pose.scale(pixel, -pixel, pixel);
        float bob = EmoteBubbles.bob(age);
        int shape = EmoteBubbles.shape(bubble.emote()), symbol = EmoteBubbles.symbol(bubble.emote(), age);
        float[] motion = EmoteBubbles.symbolMotion(bubble.emote(), age);
        collector.submitCustomGeometry(pose, RenderTypes.text(EmoteBubbles.SHEET), (p, vc) -> {
            quad(p, vc, -16, -32 + bob, 32, 32, 0, shape * 32, 0, 0, 1, 0);
            // The symbol sits in the middle of the bubble's body, a hair closer to the camera (+z faces the viewer here).
            float cx = motion[0], cy = -19 + bob + motion[1], half = 7.5F * motion[2];
            quad(p, vc, cx - half, cy - half, half * 2, half * 2, 32 + symbol / 8 * 16, symbol % 8 * 16, 16, .3F, 1, motion[3]);
        });
        pose.popPose();
    }
    /** One textured square in sheet pixels (u = row y, v = column x, as cells are laid out), optionally rotated. */
    private static void quad(PoseStack.Pose p, VertexConsumer vc, float x, float y, float w, float h, int row, int column, int size, float z, float alpha, float degrees) {
        int cell = size == 0 ? 32 : size;
        float u0 = column / 128F, v0 = row / 128F, u1 = (column + cell) / 128F, v1 = (row + cell) / 128F;
        float cx = x + w / 2, cy = y + h / 2, cos = Mth.cos(degrees * Mth.DEG_TO_RAD), sin = Mth.sin(degrees * Mth.DEG_TO_RAD);
        float[][] corners = {{x, y, u0, v0}, {x, y + h, u0, v1}, {x + w, y + h, u1, v1}, {x + w, y, u1, v0}};
        int color = ((int) (alpha * 255) << 24) | 0xFFFFFF;
        for (var c : corners) {
            float dx = c[0] - cx, dy = c[1] - cy;
            vc.addVertex(p, cx + dx * cos - dy * sin, cy + dx * sin + dy * cos, z).setColor(color).setUv(c[2], c[3]).setLight(0xF000F0);
        }
    }
}
