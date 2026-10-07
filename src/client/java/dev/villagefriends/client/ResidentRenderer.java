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

/** Vanilla villagers retain their trades and AI, but use the actual player mesh and skin layout. */
public final class ResidentRenderer extends HumanoidMobRenderer<Villager, ResidentRenderState, HumanoidModel<ResidentRenderState>> {
    /** Set while a GUI portrait is extracted; the portrait follows the mouse, not the camera. */
    public static boolean portrait;
    public ResidentRenderer(EntityRendererProvider.Context context) {
        // Use the vanilla player's exact mesh, with a mob state: AvatarRenderState is
        // dispatched to the player renderer even when it originated from a villager.
        super(context, new ResidentModel(false), new ResidentModel(true), 0.45F);
        this.addLayer(new WardrobeLayer(this));
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
    @Override protected float getShadowRadius(ResidentRenderState state) { return super.getShadowRadius(state)*(state.isBaby?.6F:1F); }

    @Override public void extractRenderState(Villager villager, ResidentRenderState state, float delta) {
        super.extractRenderState(villager, state, delta);
        state.motionSeed=ResidentMotion.seed(villager.getUUID());
        state.onGround=villager.onGround();
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
    }
}
