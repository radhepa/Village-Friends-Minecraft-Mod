package dev.villagefriends.stable.client.breed;

import static dev.villagefriends.VillageFriends.target;

import dev.villagefriends.stable.data.HorseBreed;
import dev.villagefriends.stable.data.StableData;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;
import net.fabricmc.fabric.api.client.rendering.v1.RenderStateDataKey;
import net.minecraft.client.renderer.entity.state.EquineRenderState;
import net.minecraft.client.renderer.entity.state.HorseRenderState;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.entity.animal.equine.Horse;
import org.jspecify.annotations.Nullable;

/**
 * Painted breed coats. The foundation's {@code HorseRenderStateMixin} calls {@link #extract} as a horse's render
 * state is filled (it carries the synced breed into the state), and {@code HorseCoatMixin} asks {@link #texture}
 * before vanilla picks a coat; null keeps vanilla's. Owned by the breeds package; the signatures are frozen.
 *
 * <p>Coats live at {@code villagefriends:textures/entity/horse/<breed>[_<coat>][_baby].png} (painted by
 * {@code tools/stablehand/breeds.py} on the vanilla horse's UV layout, so vanilla's markings still fit on top). A
 * breed without painted art (an add-on's breed, or a coat number past the art) keeps vanilla's coat rather than
 * showing a missing texture: {@link BreedClient} lists the loaded coat textures after every resource reload.
 */
public final class HorseCoats {
    public static final RenderStateDataKey<HorseBreed> COAT = RenderStateDataKey.create(() -> "villagefriends:horse_coat");
    /** The folder the coats are in, inside the {@code villagefriends} namespace. */
    public static final String FOLDER = "textures/entity/horse";
    /** Every coat texture the loaded resources have (replaced on each resource reload). */
    private static volatile Set<Identifier> loaded = Set.of();
    /** Texture path -> its id, so a frame builds no new ids. Render thread only. */
    private static final Map<String, Identifier> IDS = new HashMap<>();

    public static void extract(AbstractHorse horse, EquineRenderState state) {
        // Render states are reused between horses, so a horse without a breed must clear what the last one left.
        state.setData(COAT, horse instanceof Horse ? target(horse).getAttached(StableData.BREED) : null);
    }

    public static @Nullable Identifier texture(HorseRenderState state) {
        var breed = state.getData(COAT);
        if (breed == null) return null;
        var id = IDS.computeIfAbsent(path(breed.breed(), breed.coat(), state.isBaby), p -> Identifier.tryBuild("villagefriends", p));
        return id != null && loaded.contains(id) ? id : null;
    }

    /** The texture path of a coat: {@code textures/entity/horse/<breed>[_<coat>][_baby].png}. */
    public static String path(String breed, int coat, boolean baby) {
        return FOLDER + "/" + breed + (coat > 0 ? "_" + coat : "") + (baby ? "_baby" : "") + ".png";
    }

    /** The coat textures the resources have now (called after each resource reload). */
    static void loaded(Set<Identifier> textures) { loaded = Set.copyOf(textures); }

    /** Whether a coat texture is loaded (for tests). */
    public static boolean has(Identifier texture) { return loaded.contains(texture); }

    private HorseCoats() {}
}
