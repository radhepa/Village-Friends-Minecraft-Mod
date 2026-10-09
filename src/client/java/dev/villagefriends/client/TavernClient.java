package dev.villagefriends.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.math.Axis;
import dev.villagefriends.ResidentMotion;
import dev.villagefriends.animation.AnimationClip;
import dev.villagefriends.animation.ResidentBehavior;
import dev.villagefriends.tavern.Patronage;
import dev.villagefriends.tavern.Patronage.Phase;
import dev.villagefriends.tavern.Seat;
import dev.villagefriends.tavern.TavernSurvey;
import dev.villagefriends.tavern.Taverns;
import java.util.Map;
import java.util.Set;
import java.util.WeakHashMap;
import net.fabricmc.fabric.api.attachment.v1.AttachmentTarget;
import net.fabricmc.fabric.api.client.rendering.v1.EntityRendererRegistry;
import net.minecraft.client.Minecraft;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.entity.NoopRenderer;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.Identifier;
import net.minecraft.tags.BlockTags;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.CampfireBlock;

/**
 * The tavern on the client: the invisible seat, the dish set on the table in front of a diner (or in their
 * hand while they take a bite or a sip, while they stand at the bar, and while the keeper carries it out),
 * and the tags that pick tavern animations: seated, what they're eating, music and the hearth nearby.
 */
public final class TavernClient {
    private record Nearby(int until, boolean music, boolean hearth) {}
    private static final Map<Villager, Nearby> NEARBY = new WeakHashMap<>();

    public static void register() {
        EntityRendererRegistry.register(Taverns.SEAT, NoopRenderer::new);
    }

    // -- props -------------------------------------------------------------------------------------

    /** Puts the dish in the resident's hand or on the table for this frame. Called after vanilla fills in their held items. */
    public static void extract(Villager v, ResidentRenderState s, boolean portrait) {
        s.seated = Seat.seated(v);
        s.tableItemShown = false;
        if (portrait) return;
        String state = state(v);
        var phase = Patronage.phase(state);
        if (phase == null || phase == Phase.WAIT) return;
        var item = stack(Patronage.item(state));
        if (item.isEmpty()) return;
        var resolver = Minecraft.getInstance().getItemModelResolver();
        boolean hand = phase == Phase.CARRY || !s.seated || phase != Phase.DONE && holding(ResidentLife.of(v));
        if (!hand && !table(v, s)) hand = phase != Phase.DONE;
        if (hand) {
            boolean left = ResidentBehavior.leftHanded(ResidentMotion.seed(v.getUUID()));
            if (left) {
                resolver.updateForLiving(s.leftHandItemState, item, ItemDisplayContext.THIRD_PERSON_LEFT_HAND, v);
                s.leftHandItemStack = item; s.leftArmPose = HumanoidModel.ArmPose.ITEM;
            } else {
                resolver.updateForLiving(s.rightHandItemState, item, ItemDisplayContext.THIRD_PERSON_RIGHT_HAND, v);
                s.rightHandItemStack = item; s.rightArmPose = HumanoidModel.ArmPose.ITEM;
            }
        } else if (s.tableItemShown) {
            resolver.updateForTopItem(s.tableItem, item, ItemDisplayContext.FIXED, v.level(), v, v.getId());
        }
    }
    /** At the tavern, or eating a meal at home (Hearth & Harvest), in the same "eat:<item>" form. */
    private static String state(Villager v) {
        String state = ((AttachmentTarget) v).getAttached(Taverns.STATE);
        return state != null ? state : ((AttachmentTarget) v).getAttached(dev.villagefriends.hearth.HomeMeals.STATE);
    }
    /** Finds the table in front of a seated diner and where on it their dish goes; false if there's nothing to set it on. */
    private static boolean table(Villager v, ResidentRenderState s) {
        if (!(v.getVehicle() instanceof Seat seat)) return false;
        float yaw = seat.getYRot();
        var front = Direction.fromYRot(yaw);
        BlockPos at = seat.seatPos().relative(front);
        double top = TavernSurvey.tableTop(v.level(), at);
        if (top < .3 || top > 1.6) return false;
        // Near the diner's edge of the table, a little to their right.
        double fx = front.getStepX(), fz = front.getStepZ(), rx = -fz, rz = fx;
        s.tableX = at.getX() + .5 - fx * .28 - rx * .12 - s.x;
        s.tableY = at.getY() + top + .005 - s.y;
        s.tableZ = at.getZ() + .5 - fz * .28 - rz * .12 - s.z;
        s.tableYaw = yaw;
        s.tableItemShown = true;
        return true;
    }
    /** Whether the clip playing now takes a bite or a sip, so the dish is in hand. */
    private static boolean holding(ResidentLife life) {
        return uses(life.activity()) || uses(life.reaction());
    }
    private static boolean uses(AnimationClip clip) {
        if (clip == null) return false;
        for (var group : clip.require()) if (group.contains("dining:eat") || group.contains("dining:drink") || group.contains("dining:done")) return true;
        return false;
    }
    private static ItemStack stack(String id) {
        if (id == null) return ItemStack.EMPTY;
        var parsed = Identifier.tryParse(id);
        if (parsed == null) return ItemStack.EMPTY;
        return BuiltInRegistries.ITEM.getOptional(parsed).map(ItemStack::new).orElse(ItemStack.EMPTY);
    }

    /** Draws the dish lying on the table. */
    public static void submit(ResidentRenderState s, PoseStack pose, SubmitNodeCollector collector) {
        if (!s.tableItemShown || s.tableItem.isEmpty()) return;
        pose.pushPose();
        pose.translate(s.tableX, s.tableY, s.tableZ);
        pose.rotateDegrees(Axis.YP, -s.tableYaw);
        pose.rotateDegrees(Axis.XP, 90);
        pose.scale(.42F, .42F, .42F);
        s.tableItem.submit(pose, collector, s.lightCoords, OverlayTexture.NO_OVERLAY, 0);
        pose.popPose();
    }

    // -- animation tags ----------------------------------------------------------------------------

    /** Adds the tavern's tags to a resident's situation. */
    public static void tags(Villager v, Set<String> tags) {
        if (Seat.seated(v)) tags.add("seated");
        String routine = ((AttachmentTarget) v).getAttached(dev.villagefriends.VillageFriends.ROUTINE);
        if (routine != null && dev.villagefriends.routine.Routine.atTavern(dev.villagefriends.routine.Routine.Block.byId(routine))) tags.add("tavern");
        String state = state(v);
        var phase = Patronage.phase(state);
        if (phase != null) {
            tags.add("dining:" + phase.id());
            String item = Patronage.item(state);
            if (item != null && (phase == Phase.EAT || phase == Phase.DRINK)) tags.add((phase == Phase.DRINK ? "drink:" : "food:") + Patronage.kind(item));
            if (item != null && phase != Phase.WAIT && !Seat.seated(v)) tags.add("holding");
        }
        var near = nearby(v);
        if (near.music()) tags.add("music");
        if (near.hearth()) tags.add("hearth");
    }
    /** A bard playing within twelve blocks, a fire within four: looked up a couple of times a minute. */
    private static Nearby nearby(Villager v) {
        var known = NEARBY.get(v);
        if (known != null && v.tickCount < known.until() && v.tickCount > known.until() - 200) return known;
        boolean music = false, hearth = false;
        for (var other : v.level().getEntitiesOfClass(Villager.class, v.getBoundingBox().inflate(12, 4, 12))) {
            if ("perform".equals(((AttachmentTarget) other).getAttached(dev.villagefriends.VillageFriends.ROUTINE))) { music = true; break; }
        }
        var origin = v.blockPosition();
        for (var p : BlockPos.betweenClosed(origin.offset(-4, -1, -4), origin.offset(4, 2, 4))) {
            var state = v.level().getBlockState(p);
            if (state.is(Blocks.CAMPFIRE) && state.getValue(CampfireBlock.LIT) || state.is(BlockTags.FIRE)) { hearth = true; break; }
        }
        var found = new Nearby(v.tickCount + 100 + v.getRandom().nextInt(60), music, hearth);
        NEARBY.put(v, found);
        return found;
    }
    public static void clear() { NEARBY.clear(); }

    private TavernClient() {}
}
