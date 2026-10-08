package dev.villagefriends.client;

import net.minecraft.client.renderer.entity.state.HumanoidRenderState;
import net.minecraft.resources.Identifier;

public final class ResidentRenderState extends HumanoidRenderState {
    public Identifier texture;
    public dev.villagefriends.outfit.Outfit outfit;
    public int motionSeed;
    public boolean onGround;
    public float eyeLookX, eyeLookY, attention;
    /** Animation pack clips: [0] activity (idle, work, chat, talk, pet play), [1] reaction (greet, laugh, hurt...),
     *  [2] the activity being replaced, fading out underneath the new one. */
    public final AnimationLayer[] layers = {new AnimationLayer(), new AnimationLayer(), new AnimationLayer()};
    /** Degrees to turn the head toward the player while greeting or talking, and how strongly. */
    public float turnYaw, turnPitch, turnWeight;
    /** The emote bubble above their head this frame, or null. */
    public EmoteBubbles.Bubble bubble;
    public float bubbleAge;
    /** Lying hurt on the ground: knocked out, or a downed companion. */
    public boolean injured;
}
