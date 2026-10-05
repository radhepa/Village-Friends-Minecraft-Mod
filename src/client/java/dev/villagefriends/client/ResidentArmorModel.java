package dev.villagefriends.client;

import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.geom.ModelPart;

/** Armor follows each resident's actual gait instead of the default player walk. */
public final class ResidentArmorModel extends HumanoidModel<ResidentRenderState> {
    public ResidentArmorModel(ModelPart root) { super(root); }
    @Override public void setupAnim(ResidentRenderState state) {
        super.setupAnim(state);
        ResidentAnimation.apply(this, state);
    }
}
