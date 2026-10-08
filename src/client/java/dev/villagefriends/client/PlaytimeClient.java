package dev.villagefriends.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.math.Axis;
import dev.villagefriends.VillageItems;
import dev.villagefriends.play.Games;
import dev.villagefriends.play.Playground;
import java.util.Map;
import java.util.Set;
import java.util.WeakHashMap;
import net.fabricmc.fabric.api.attachment.v1.AttachmentTarget;
import net.minecraft.client.Minecraft;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.phys.Vec3;

/**
 * Children's games on the client: the tags that pick game animations ({@code play:tag:it}, {@code moving}), which
 * parts of a game play their clip once and which keep repeating it, and the leather ball in a game of catch, held
 * in the hand and then flying in an arc from thrower to catcher (or past them, when they fumble it).
 */
public final class PlaytimeClient {
    /** Parts of a game whose clip plays once; every other part repeats its clips for as long as it lasts. */
    private static final Set<String> ONCE = Set.of("throw", "fall", "found", "point", "tagged", "bye", "won", "fumble", "do");
    /** When a child's part changed, and where a fumbled ball came to rest (so it stays put while they fetch it). */
    private static final class Since {
        final String state; final float start; Vec3 rest;
        Since(String state, float start) { this.state = state; this.start = start; }
    }
    private static final Map<Villager, Since> SINCE = new WeakHashMap<>();
    private static ItemStack ball;

    public static String state(Villager v) { return ((AttachmentTarget) v).getAttached(Playground.STATE); }
    public static boolean once(String state) { return ONCE.contains(Games.role(state)); }

    /** Adds a child's part in a game to their situation for picking clips. */
    public static void tags(Villager v, Set<String> tags) {
        String state = state(v);
        if (state == null) return;
        String game = Games.game(state), role = Games.role(state);
        tags.add("play:" + game);
        if (role != null) tags.add("play:" + game + ":" + role);
        if ("do".equals(role)) tags.add("play:" + state);
        if (v.walkAnimation.speed() > .08F) tags.add("moving");
    }

    // -- the ball -----------------------------------------------------------------------------------

    /** Puts the ball in a child's hand, or in the air, for this frame. Called after vanilla fills in their held items. */
    public static void extract(Villager v, ResidentRenderState s, boolean portrait) {
        s.ballShown = false;
        String state = state(v);
        if (portrait || state == null || !Games.Game.CATCH.id().equals(Games.game(state))) { SINCE.remove(v); return; }
        var since = SINCE.get(v);
        if (since == null || !since.state.equals(state)) { since = new Since(state, s.ageInTicks); SINCE.put(v, since); }
        float age = s.ageInTicks - since.start;
        String role = Games.role(state);
        if ("hold".equals(role) || "throw".equals(role) && age < Playground.RELEASE) { hold(v, s); return; }
        if (!"throw".equals(role)) return;
        if (Games.detail(state) == null) return;
        String[] detail = Games.detail(state).split(":");
        Entity catcher;
        try { catcher = v.level().getEntity(Integer.parseInt(detail[0])); } catch (NumberFormatException e) { return; }
        if (catcher == null) return;
        boolean miss = detail.length > 1 && detail[1].equals("miss");
        float partial = s.ageInTicks - v.tickCount;
        var me = v.getPosition(partial); var them = catcher.getPosition(partial);
        var from = hand(me, them, v.getBbHeight() * .62);
        var to = miss ? Playground.landing(me, them).add(0, .12, 0) : hand(them, me, catcher.getBbHeight() * .58);
        float t = (age - Playground.RELEASE) / Playground.FLIGHT;
        Vec3 at;
        if (t < 1) {
            double lift = (miss ? .8 : 1.1) * 4 * t * (1 - t);
            at = from.lerp(to, t).add(0, lift, 0);
        } else if (miss) {
            if (since.rest == null) since.rest = to;
            at = since.rest;
        } else return;
        s.ballX = at.x - s.x; s.ballY = at.y - s.y; s.ballZ = at.z - s.z;
        s.ballSpin = t < 1 ? age * 38 : 0;
        Minecraft.getInstance().getItemModelResolver().updateForTopItem(s.ball, ball(), ItemDisplayContext.FIXED, v.level(), v, v.getId());
        s.ballShown = true;
    }
    /** About where a child's hands are, a little toward whoever they're facing. */
    private static Vec3 hand(Vec3 self, Vec3 toward, double height) {
        double dx = toward.x - self.x, dz = toward.z - self.z, len = Math.max(1e-3, Math.sqrt(dx * dx + dz * dz));
        return self.add(dx / len * .28, height, dz / len * .28);
    }
    private static void hold(Villager v, ResidentRenderState s) {
        var resolver = Minecraft.getInstance().getItemModelResolver();
        resolver.updateForLiving(s.rightHandItemState, ball(), ItemDisplayContext.THIRD_PERSON_RIGHT_HAND, v);
        s.rightHandItemStack = ball(); s.rightArmPose = HumanoidModel.ArmPose.ITEM;
    }
    private static ItemStack ball() {
        if (ball == null) ball = new ItemStack(VillageItems.get("leather_ball"));
        return ball;
    }

    /** Draws the ball in flight, or lying on the grass after a fumble. */
    public static void submit(ResidentRenderState s, PoseStack pose, SubmitNodeCollector collector) {
        if (!s.ballShown || s.ball.isEmpty()) return;
        pose.pushPose();
        pose.translate(s.ballX, s.ballY, s.ballZ);
        pose.rotateDegrees(Axis.YP, s.ballSpin);
        pose.rotateDegrees(Axis.XP, s.ballSpin * .6F);
        pose.scale(.32F, .32F, .32F);
        s.ball.submit(pose, collector, s.lightCoords, OverlayTexture.NO_OVERLAY, 0);
        pose.popPose();
    }

    public static void clear() { SINCE.clear(); }
    private PlaytimeClient() {}
}
