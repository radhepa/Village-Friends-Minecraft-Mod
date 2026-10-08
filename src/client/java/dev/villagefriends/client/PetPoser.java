package dev.villagefriends.client;

import dev.villagefriends.pet.PetKeeping;
import dev.villagefriends.pet.PetTrick;
import dev.villagefriends.pet.PetTrick.Bone;
import dev.villagefriends.pet.VillagerPets;
import java.util.Arrays;
import java.util.Map;
import java.util.Objects;
import java.util.WeakHashMap;
import net.fabricmc.fabric.api.attachment.v1.AttachmentTarget;
import net.fabricmc.fabric.api.client.rendering.v1.RenderStateDataKey;
import net.minecraft.client.Minecraft;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.renderer.entity.state.LivingEntityRenderState;
import net.minecraft.client.renderer.item.ItemStackRenderState;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.animal.feline.Cat;
import net.minecraft.world.entity.animal.wolf.Wolf;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import org.joml.Matrix3f;
import org.joml.Vector3f;

/**
 * Poses a resident's cat or dog for the trick it's doing (see {@link PetTrick}): the server names the
 * trick and when it began, this samples it each frame on top of the model's own pose, and fades the
 * last trick out underneath a new one. The root turns about the middle of the body so a dog can roll
 * onto its back or spin on the spot. Rendering is single threaded; scratch buffers are reused.
 */
public final class PetPoser {
    public static final RenderStateDataKey<Pose> POSE = RenderStateDataKey.create(() -> "villagefriends:pet_pose");
    /** A stick in a dog's mouth while it brings it back. */
    public static final RenderStateDataKey<ItemStackRenderState> CARRIED = RenderStateDataKey.create(() -> "villagefriends:pet_carried");
    public record Pose(PetTrick trick, float time, float weight, PetTrick fading, float fadingTime, float fadingWeight, boolean cat, boolean baby) {}

    private static final class State { String value; PetTrick trick, previous; double start, previousStart, switchedAt = -1000; }
    private static final Map<Entity, State> STATES = new WeakHashMap<>();
    private static final float FADE = 6;
    private static final ItemStack STICK = new ItemStack(Items.STICK);
    private static final int BONES = Bone.ALL.length;
    private static final float[] ROT = new float[BONES * 3], POS = new float[BONES * 3], SAMPLE = new float[3];
    private static final Matrix3f TURN = new Matrix3f();
    private static final Vector3f POINT = new Vector3f();
    /** The middle of the body in model pixels, which the root turns about (tools/pets/preview.py uses the same). */
    private static final float[] DOG = {0, 14, .5F}, PUPPY = {0, 19, 0}, CAT = {0, 17, 1}, KITTEN = {0, 20.5F, .5F};
    /** Tricks are written for grown pets; kittens and puppies stand about half as tall. */
    private static final float BABY_OFFSETS = .5F;

    public static void clear() { STATES.clear(); }

    /** Called as a cat's or wolf's render state is filled in. */
    public static void extract(LivingEntity entity, LivingEntityRenderState state, float partial) {
        boolean cat = entity instanceof Cat;
        if (!cat && !(entity instanceof Wolf)) return;
        // The pet card already shows their name; keep the floating label off the portrait.
        if (Minecraft.getInstance().gui.screen() instanceof PetScreen screen && screen.petId() == entity.getId()) state.nameTag = null;
        String value = ((AttachmentTarget) entity).getAttached(VillagerPets.TRICK);
        var s = STATES.get(entity);
        if (value == null && (s == null || s.trick == null && s.previous == null)) { state.setData(POSE, null); state.setData(CARRIED, null); return; }
        if (s == null) STATES.put(entity, s = new State());
        double now = entity.level().getGameTime() + partial;
        if (!Objects.equals(value, s.value)) {
            if (s.trick != null) { s.previous = s.trick; s.previousStart = s.start; s.switchedAt = now; }
            s.value = value; s.trick = null;
            if (value != null) {
                int at = value.lastIndexOf('@');
                double start = now;
                if (at >= 0) try { start = Long.parseLong(value.substring(at + 1)); } catch (NumberFormatException ignored) {}
                s.trick = PetTricks.get(cat ? PetKeeping.CAT : PetKeeping.DOG, at < 0 ? value : value.substring(0, at));
                s.start = Math.min(start, now);
            }
        }
        float t = (float) (now - s.start) / 20F, w = s.trick == null ? 0 : s.trick.envelope(t);
        PetTrick fading = null; float fadingTime = 0, fadingWeight = 0;
        if (s.previous != null) {
            float since = (float) (now - s.switchedAt);
            if (since >= FADE) s.previous = null;
            else {
                fading = s.previous;
                float ft = (float) (now - s.previousStart) / 20F;
                fadingTime = fading.time(ft);
                fadingWeight = fading.envelope(ft) * (1 - dev.villagefriends.animation.AnimationClip.smooth(since / FADE));
            }
        }
        state.setData(POSE, w > 0 || fadingWeight > 0 ? new Pose(s.trick, s.trick == null ? 0 : s.trick.time(t), w, fading, fadingTime, fadingWeight, cat, entity.isBaby()) : null);
        if (!cat && s.trick != null && s.trick.id().equals("carry")) {
            var item = new ItemStackRenderState();
            Minecraft.getInstance().getItemModelResolver().updateForLiving(item, STICK, ItemDisplayContext.GROUND, entity);
            state.setData(CARRIED, item);
        } else state.setData(CARRIED, null);
    }

    /** Adds the pose to the model. {@code parts} is indexed by {@link Bone} (root first), with null where the model has no such part. */
    public static void apply(Pose pose, ModelPart[] parts) {
        Arrays.fill(ROT, 0); Arrays.fill(POS, 0);
        accumulate(pose.trick(), pose.time(), pose.weight());
        accumulate(pose.fading(), pose.fadingTime(), pose.fadingWeight());
        float scale = pose.baby() ? BABY_OFFSETS : 1;
        for (Bone bone : Bone.ALL) {
            if (bone == Bone.ROOT) continue;
            var part = parts[bone.ordinal()];
            if (part == null) continue;
            int i = bone.ordinal() * 3;
            part.xRot += ROT[i] * Mth.DEG_TO_RAD; part.yRot += ROT[i + 1] * Mth.DEG_TO_RAD; part.zRot += ROT[i + 2] * Mth.DEG_TO_RAD;
            part.x += POS[i] * scale; part.y += POS[i + 1] * scale; part.z += POS[i + 2] * scale;
        }
        var root = parts[Bone.ROOT.ordinal()];
        if (ROT[0] == 0 && ROT[1] == 0 && ROT[2] == 0 && POS[0] == 0 && POS[1] == 0 && POS[2] == 0) return;
        float[] c = pose.cat() ? pose.baby() ? KITTEN : CAT : pose.baby() ? PUPPY : DOG;
        // Turn about the middle of the body: the root moves so that point stays put (inside any scale the model applies).
        TURN.rotationZYX(ROT[2] * Mth.DEG_TO_RAD, ROT[1] * Mth.DEG_TO_RAD, ROT[0] * Mth.DEG_TO_RAD);
        POINT.set(c[0], c[1], c[2]); TURN.transform(POINT);
        float s = root.xScale;
        root.x += s * (c[0] - POINT.x + POS[0] * scale);
        root.y += s * (c[1] - POINT.y + POS[1] * scale);
        root.z += s * (c[2] - POINT.z + POS[2] * scale);
        root.xRot += ROT[0] * Mth.DEG_TO_RAD; root.yRot += ROT[1] * Mth.DEG_TO_RAD; root.zRot += ROT[2] * Mth.DEG_TO_RAD;
    }
    private static void accumulate(PetTrick trick, float time, float weight) {
        if (trick == null || weight <= 0) return;
        for (Bone bone : Bone.ALL) {
            int i = bone.ordinal() * 3;
            var rotation = trick.rotations()[bone.ordinal()];
            if (rotation != null) { rotation.sample(time, SAMPLE, 0); ROT[i] += SAMPLE[0] * weight; ROT[i + 1] += SAMPLE[1] * weight; ROT[i + 2] += SAMPLE[2] * weight; }
            var position = trick.positions()[bone.ordinal()];
            if (position != null) { position.sample(time, SAMPLE, 0); POS[i] += SAMPLE[0] * weight; POS[i + 1] += SAMPLE[1] * weight; POS[i + 2] += SAMPLE[2] * weight; }
        }
    }
    private PetPoser() {}
}
