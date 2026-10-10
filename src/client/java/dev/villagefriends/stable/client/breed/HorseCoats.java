package dev.villagefriends.stable.client.breed;

import dev.villagefriends.stable.data.HorseBreed;
import net.fabricmc.fabric.api.client.rendering.v1.RenderStateDataKey;
import net.minecraft.client.renderer.entity.state.EquineRenderState;
import net.minecraft.client.renderer.entity.state.HorseRenderState;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import org.jspecify.annotations.Nullable;

/**
 * Painted breed coats. The foundation's {@code HorseRenderStateMixin} calls {@link #extract} as a horse's render
 * state is filled (it carries the synced breed into the state), and {@code HorseCoatMixin} asks {@link #texture}
 * before vanilla picks a coat; null keeps vanilla's. Owned by the breeds package; the signatures are frozen.
 */
public final class HorseCoats {
    public static final RenderStateDataKey<HorseBreed> COAT = RenderStateDataKey.create(() -> "villagefriends:horse_coat");

    public static void extract(AbstractHorse horse, EquineRenderState state) {}
    public static @Nullable Identifier texture(HorseRenderState state) { return null; }

    private HorseCoats() {}
}
