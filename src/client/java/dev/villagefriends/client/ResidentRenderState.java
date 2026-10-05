package dev.villagefriends.client;

import net.minecraft.client.renderer.entity.state.HumanoidRenderState;
import net.minecraft.resources.Identifier;

public final class ResidentRenderState extends HumanoidRenderState {
    public Identifier texture;
    public dev.villagefriends.outfit.Outfit outfit;
    public int motionSeed;
    public boolean onGround;
    public float eyeLookX, eyeLookY, attention;
}
