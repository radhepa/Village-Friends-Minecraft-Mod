package dev.villagefriends.client;

import dev.villagefriends.Emote;
import dev.villagefriends.ResidentMotion;
import dev.villagefriends.VillageFriends;
import dev.villagefriends.animation.AnimationClip;
import dev.villagefriends.animation.AnimationLibrary;
import dev.villagefriends.animation.ResidentBehavior;
import java.util.HashSet;
import java.util.Map;
import java.util.Random;
import java.util.Set;
import java.util.WeakHashMap;
import net.fabricmc.fabric.api.attachment.v1.AttachmentTarget;
import net.minecraft.client.Minecraft;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.Pose;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.level.biome.Biome;

/**
 * Client-side director for one resident: decides what they do from moment to moment. Standing
 * residents fidget, practice their trade or hobby, chat with a neighbor beside them, greet a player
 * who walks up, gesture while you talk with them, and react to gifts, jokes, hearts, anger and harm.
 * Decisions happen on client ticks; the renderer samples the chosen clips every frame.
 */
public final class ResidentLife {
    private static final Map<Villager, ResidentLife> LIVES = new WeakHashMap<>();
    private static final float FADE = 6;

    private static final class Playing {
        AnimationClip clip; float start, speed = 1, fadeFrom = -1; boolean mirror; String trigger;
        boolean active() { return clip != null; }
        float time(float age) { return (age - start) / 20F * speed; }
        boolean over(float age) {
            return clip == null || time(age) > clip.length() || fadeFrom >= 0 && age - fadeFrom > FADE;
        }
        void fade(float age) { if (clip != null && fadeFrom < 0) fadeFrom = age; }
        float weight(float age) {
            if (clip == null) return 0;
            float w = clip.envelope(time(age));
            if (fadeFrom >= 0) w *= 1 - AnimationClip.smooth((age - fadeFrom) / FADE);
            return w;
        }
        void clear() { clip = null; fadeFrom = -1; trigger = null; }
    }

    private final Random random;
    private final boolean leftHanded;
    private final Playing activity = new Playing(), reaction = new Playing();
    private int stillTicks, nextActivity, lastHurt, greetAt = -1, greetCooldown, partnerId = -1, partnerCheck, lastTick = -1;
    private boolean unhappy, greeted, talking, speaking;
    private String recent, previous;

    private ResidentLife(Villager villager) {
        int seed = ResidentMotion.seed(villager.getUUID());
        random = new Random(seed ^ villager.getId() * 0x9E3779B9L);
        leftHanded = ResidentBehavior.leftHanded(seed);
        // Neighbors loaded together shouldn't all start fidgeting on the same tick.
        nextActivity = villager.tickCount + 20 + random.nextInt(100);
    }
    public static ResidentLife of(Villager villager) { return LIVES.computeIfAbsent(villager, ResidentLife::new); }
    /** The clip a resident is doing now (idle, work, chat or talk), or null. */
    public AnimationClip activity() { return activity.clip; }
    /** The reaction playing now (greet, laugh, hurt...), or null. */
    public AnimationClip reaction() { return reaction.clip; }
    public static void clear() { LIVES.clear(); }

    // -- events ------------------------------------------------------------------------------------

    /** Vanilla villager entity events: hearts, angry clouds, happy sparkles, nervous sweat. */
    public static void entityEvent(Villager villager, byte id) {
        String trigger = switch (id) { case 12 -> "love"; case 13 -> "angry"; case 14 -> "happy"; case 42 -> "nervous"; default -> null; };
        if (trigger != null) of(villager).react(villager, trigger);
        var emote = switch (id) { case 12 -> Emote.HEART; case 13 -> Emote.ANGER; case 14 -> Emote.NOTE; case 42 -> Emote.SWEAT; default -> null; };
        if (emote != null) EmoteBubbles.ambient(villager, emote);
    }
    /** A conversation outcome for the resident with this entity id. */
    public static void cue(int entityId, String trigger) {
        var level = Minecraft.getInstance().level;
        if (level != null && level.getEntity(entityId) instanceof Villager villager) of(villager).react(villager, trigger);
    }

    void react(Villager villager, String trigger) {
        float now = villager.tickCount;
        var clip = AnimationLibrary.current().pick(trigger, tags(villager, -1), random, reaction.clip == null ? null : reaction.clip.id());
        if (clip == null) return;
        start(reaction, clip, now, trigger);
        activity.fade(now);
        nextActivity = Math.max(nextActivity, (int) (now + clip.length() * 20 + 6));
    }

    // -- per tick ----------------------------------------------------------------------------------

    public static void tickAll(Minecraft client) {
        if (client.level == null || client.isPaused()) return;
        var camera = client.getCameraEntity();
        for (var entity : client.level.entitiesForRendering()) {
            if (!(entity instanceof Villager villager)) continue;
            if (camera != null && villager.distanceToSqr(camera) > 64 * 64) continue;
            of(villager).tick(villager, client);
        }
    }

    void tick(Villager v, Minecraft client) {
        int now = v.tickCount;
        // A frozen or stepped world (/tick freeze) holds residents mid-motion, exactly like everything else.
        if (now == lastTick) return;
        lastTick = now;
        boolean able = canAct(v);
        boolean moving = v.walkAnimation.speed() > .06F;
        stillTicks = able && !moving ? stillTicks + 1 : 0;
        if (reaction.over(now)) reaction.clear();
        if (activity.over(now)) {
            if (activity.active()) nextActivity = now + pause(v, activity.trigger);
            activity.clear();
        }
        if (!able) { activity.fade(now); return; }

        if (v.hurtTime > lastHurt) { react(v, "hurt"); EmoteBubbles.show(v.getId(), Emote.ANGER, 0); }
        lastHurt = v.hurtTime;
        boolean sad = v.getUnhappyCounter() > 0;
        if (sad && !unhappy) react(v, "decline");
        unhappy = sad;

        var screen = client.gui.screen() instanceof FriendshipScreen open && open.residentId() == v.getId() ? open : null;
        talking = screen != null;
        boolean wasSpeaking = speaking;
        speaking = talking && screen.speaking();
        // A new line starts: stop listening and start talking right away.
        if (speaking && !wasSpeaking && activity.active() && !"talk".equals(activity.trigger)) { activity.fade(now); nextActivity = now + 2; }
        noticePlayer(v, client, now);
        if (activity.active() && moving && !talking) activity.fade(now);
        if (activity.active() || reaction.active() || now < nextActivity) return;

        String trigger = null;
        // In conversation they gesture while their line types out, then listen while you choose a reply.
        if (talking) trigger = speaking ? "talk" : "chat_listen";
        else if (stillTicks > 20) {
            int partner = partner(v, now);
            // Diners mostly eat while the food is in front of them, and talk between courses.
            float chatty = dining(v) ? .35F : .8F;
            trigger = partner >= 0 && random.nextFloat() < chatty ? (speaker(v, partner) ? "chat_speak" : "chat_listen") : "idle";
        }
        if (trigger == null) return;
        var library = AnimationLibrary.current();
        var tags = tags(v, trigger.startsWith("chat") ? partnerId : -1);
        var clip = library.pick(trigger, tags, random, recent, previous);
        if (clip == null && trigger.startsWith("chat")) { trigger = "idle"; clip = library.pick(trigger, tags, random, recent, previous); }
        if (clip == null) { nextActivity = now + 40; return; }
        start(activity, clip, now, trigger);
        previous = recent; recent = clip.id();
        // Neighbors chatting now and then show what they're on about.
        if (trigger.equals("chat_speak") && random.nextFloat() < .3F) EmoteBubbles.ambient(v, random.nextFloat() < .7F ? Emote.DOTS : Emote.NOTE);
    }

    private void noticePlayer(Villager v, Minecraft client, int now) {
        var player = client.player;
        if (player == null || talking) { greetAt = -1; return; }
        double distance = v.distanceToSqr(player);
        if (distance > 11 * 11) greeted = false;
        if (!greeted && now >= greetCooldown && distance < 5.5 * 5.5 && facing(v, player.getX(), player.getZ(), 80)) {
            greeted = true; greetCooldown = now + 1200;
            greetAt = now + 3 + random.nextInt(14);
        }
        if (greetAt >= 0 && now >= greetAt) { greetAt = -1; if (!reaction.active()) { react(v, "greet"); EmoteBubbles.ambient(v, Emote.EXCLAIM); } }
    }

    /** Another resident standing close by and roughly in front of this one: a conversation partner. */
    private int partner(Villager v, int now) {
        if (now < partnerCheck) return partnerId;
        partnerCheck = now + 10;
        partnerId = -1;
        double best = Double.MAX_VALUE;
        // Around a table people talk to whoever sits beside them as well as across from them.
        boolean seated = dev.villagefriends.tavern.Seat.seated(v);
        for (var other : v.level().getEntitiesOfClass(Villager.class, v.getBoundingBox().inflate(3.2, 1, 3.2))) {
            if (other == v || !other.isAlive() || other.isSleeping() || other.walkAnimation.speed() > .06F) continue;
            if (!facing(v, other.getX(), other.getZ(), seated ? 115 : 70)) continue;
            double d = v.distanceToSqr(other);
            if (d < best) { best = d; partnerId = other.getId(); }
        }
        return partnerId;
    }
    /** Two neighbors take turns: one speaks while the other listens, swapping every few seconds. */
    private static boolean speaker(Villager v, int partner) {
        long slot = v.level().getGameTime() / 70;
        return (slot + (v.getId() < partner ? 0 : 1)) % 2 == 0;
    }
    private static boolean facing(Villager v, double x, double z, float within) {
        float yaw = (float) Math.toDegrees(Math.atan2(-(x - v.getX()), z - v.getZ()));
        return Math.abs(Mth.wrapDegrees(yaw - v.getYHeadRot())) < within;
    }

    private Set<String> tags(Villager v, int partner) {
        var tags = new HashSet<String>();
        tags.add(v.isBaby() ? "child" : "adult");
        if (!v.isBaby()) ResidentBehavior.jobTags(VillageFriends.profession(v), tags);
        String personality = personality(v);
        if (personality != null) tags.add("personality:" + personality);
        // What they're doing in their day: at work they practice their trade, on their hobby time their hobby.
        String routine = ((AttachmentTarget) v).getAttached(VillageFriends.ROUTINE);
        if (routine != null) tags.add("routine:" + routine);
        var level = v.level();
        tags.add(ResidentBehavior.timeTag(level.getOverworldClockTime()));
        var pos = v.blockPosition();
        if (level.isRaining() && level.isRainingAt(pos.above())) tags.add("rain");
        if (level.isThundering()) tags.add("thunder");
        if (level.getBiome(pos).value().getPrecipitationAt(pos, level.getSeaLevel()) == Biome.Precipitation.SNOW) tags.add("cold");
        if (!v.getMainHandItem().isEmpty()) tags.add("holding");
        if (partner >= 0) tags.add("social");
        TavernClient.tags(v, tags);
        return tags;
    }
    private static String personality(Villager v) { return ((AttachmentTarget) v).getAttached(VillageFriends.TEMPERAMENT); }
    private static boolean dining(Villager v) {
        String state = ((AttachmentTarget) v).getAttached(dev.villagefriends.tavern.Taverns.STATE);
        return state != null && state.startsWith("eat");
    }

    private void start(Playing slot, AnimationClip clip, float now, String trigger) {
        slot.clip = clip; slot.start = now; slot.fadeFrom = -1; slot.trigger = trigger;
        slot.speed = .94F + random.nextFloat() * .12F;
        slot.mirror = switch (clip.mirror()) {
            case HAND -> leftHanded;
            case FREE -> leftHanded ^ random.nextFloat() < .4F;
            case NEVER -> false;
        };
    }
    private int pause(Villager v, String trigger) {
        if ("talk".equals(trigger) || talking) return 4 + random.nextInt(14);
        if (trigger != null && trigger.startsWith("chat")) return 6 + random.nextInt(22);
        return ResidentBehavior.pause(ResidentBehavior.energy(personality(v), v.isBaby()), random.nextFloat());
    }
    private static boolean canAct(Villager v) {
        return v.isAlive() && !v.isSleeping() && v.getPose() == Pose.STANDING && (!v.isPassenger() || dev.villagefriends.tavern.Seat.seated(v))
                && !v.isInWater() && !v.isUsingItem() && !v.isSwinging();
    }

    // -- per frame ---------------------------------------------------------------------------------

    /** Fills the render state's clip layers and head turn for this frame. */
    public void extract(Villager v, ResidentRenderState s, boolean portrait) {
        float age = s.ageInTicks;
        float walk = ResidentMotion.smooth(Mth.clamp(s.walkAnimationSpeed, 0, 1) / .28F);
        float react = reaction.weight(age);
        if (react > 0) s.layers[1].set(reaction.clip, reaction.time(age), react, reaction.mirror, 1 - walk);
        else s.layers[1].clear();
        float act = activity.weight(age) * (1 - walk) * (1 - react);
        if (act > 0) s.layers[0].set(activity.clip, activity.time(age), act, activity.mirror, 1);
        else s.layers[0].clear();
        s.turnWeight = 0;
        // Seated neighbors turn their heads to each other while they talk.
        if (!portrait && v.isPassenger() && partnerId >= 0 && activity.active() && activity.trigger != null && activity.trigger.startsWith("chat")
                && v.level().getEntity(partnerId) instanceof Villager other) {
            float yaw = (float) Math.toDegrees(Math.atan2(-(other.getX() - v.getX()), other.getZ() - v.getZ()));
            float relative = Mth.wrapDegrees(yaw - v.getYHeadRot());
            if (Math.abs(relative) < 120) { s.turnYaw = Mth.clamp(relative, -60, 60); s.turnPitch = 0; s.turnWeight = act * .85F; }
        }
        boolean attentive = talking || reaction.active() && "greet".equals(reaction.trigger);
        var camera = Minecraft.getInstance().getCameraEntity();
        if (!portrait && attentive && camera != null) {
            var offset = camera.getEyePosition(1).subtract(v.getEyePosition(1));
            float yaw = (float) Math.toDegrees(Math.atan2(-offset.x, offset.z));
            float relative = Mth.wrapDegrees(yaw - v.getYHeadRot());
            if (Math.abs(relative) < 100) {
                s.turnYaw = Mth.clamp(relative, -55, 55);
                double flat = Math.sqrt(offset.x * offset.x + offset.z * offset.z);
                s.turnPitch = Mth.clamp((float) -Math.toDegrees(Math.atan2(offset.y, flat)) - s.xRot, -25, 25);
                s.turnWeight = talking ? 1 : reaction.weight(age);
            }
        }
    }
}
