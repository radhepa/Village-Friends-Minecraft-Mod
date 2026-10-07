package dev.villagefriends;

import static dev.villagefriends.VillageFriends.*;
import dev.villagefriends.animation.AnimationClip;
import dev.villagefriends.animation.AnimationLibrary;
import dev.villagefriends.client.*;
import java.util.*;
import java.util.function.Predicate;
import net.fabricmc.fabric.api.attachment.v1.AttachmentTarget;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.*;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.Identifier;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.Pose;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.phys.EntityHitResult;

/**
 * Village Life animation pack in the real client: posing rules (armor parity, planted feet, held
 * items, mirroring, eyes, children), the director (idles, chats, greetings, conversation reactions,
 * vanilla events, harm) and a still gallery of every clip for art review.
 * Run with {@code gradlew runClientGameTest -PanimationPack}.
 */
@SuppressWarnings("UnstableApiUsage")
public final class AnimationPackGameTest implements FabricClientGameTest {
    private static void check(boolean ok, String reason) { if (!ok) throw new AssertionError(reason); }
    private static void near(float a, float b, String reason) { check(Math.abs(a - b) < .0001F, reason + ": " + a + " / " + b); }
    private static AnimationClip clip(String id) {
        var clip = AnimationLibrary.current().clip("village_life:" + id); check(clip != null, "Missing clip " + id); return clip;
    }
    private static void same(ModelPart a, ModelPart b, String what) {
        near(a.x, b.x, what + " x"); near(a.y, b.y, what + " y"); near(a.z, b.z, what + " z");
        near(a.xRot, b.xRot, what + " xRot"); near(a.yRot, b.yRot, what + " yRot"); near(a.zRot, b.zRot, what + " zRot");
    }
    private static ResidentRenderState standing(int seed) {
        var s = new ResidentRenderState(); s.motionSeed = seed; s.onGround = true; s.pose = Pose.STANDING; s.ageInTicks = 40; return s;
    }
    private static Villager resident(TestSingleplayerContext w, UUID id) { return (Villager) w.getConnection().getServerLevel().getEntity(id); }
    private static int clientId(TestSingleplayerContext w, UUID id) { return w.getServer().computeOnServer(s -> resident(w, id).getId()); }
    private static void await(ClientGameTestContext c, int entity, Predicate<ResidentLife> condition, int ticks, String reason) {
        for (int i = 0; i < ticks; i++) {
            boolean ok = c.computeOnClient(client -> client.level.getEntity(entity) instanceof Villager v && condition.test(ResidentLife.of(v)));
            if (ok) return;
            c.waitTick();
        }
        throw new AssertionError(reason);
    }
    private static Predicate<ResidentLife> reacting(String trigger) { return life -> life.reaction() != null && life.reaction().trigger().equals(trigger); }

    @Override public void runTest(ClientGameTestContext c) {
        c.getInput().resizeWindow(1600, 1000);
        c.runOnClient(client -> { client.options.guiScale().set(2); client.resizeGui(); });
        posing(c);
        try (var w = c.worldBuilder().create()) {
            w.getConnection().waitForChunksRender();
            w.getServer().runCommand("time set 6000"); w.getServer().runCommand("weather clear");
            w.getServer().runCommand("gamerule advance_time false");
            director(c, w);
            gallery(c, w);
        }
        LOGGER.info("ANIMATION PACK PASSED: {} clips; armor parity, planted feet, held items, mirroring, eyes, children; idles, chats, greetings, conversation and event reactions; gallery captured.",
                AnimationLibrary.current().clips().size());
    }

    /** Pure posing rules on fresh models: what every frame relies on. */
    private static void posing(ClientGameTestContext c) {
        c.runOnClient(client -> {
            var library = AnimationLibrary.current();
            check(library.clips().size() >= 90 && library.packs().getFirst().name().equals("Village Life"), "Village Life loads from resources");
            var model = new ResidentModel(false); var armor = new ResidentArmorModel(ResidentModel.layer(false).bakeRoot());
            for (var clip : library.clips()) for (float f : new float[]{.3F, .55F, .8F}) {
                var s = standing(77); s.layers[0].set(clip, clip.length() * f, 1, false, 1);
                model.setupAnim(s); armor.setupAnim(s);
                same(model.head, armor.head, clip.id() + " head"); same(model.body, armor.body, clip.id() + " body");
                same(model.rightArm, armor.rightArm, clip.id() + " right arm"); same(model.leftArm, armor.leftArm, clip.id() + " left arm");
                same(model.rightLeg, armor.rightLeg, clip.id() + " right leg"); same(model.root(), armor.root(), clip.id() + " root");
                var root = model.root();
                var feet = new org.joml.Vector3f(0, 24, 0).rotate(new org.joml.Quaternionf().rotationZYX(root.zRot, root.yRot, root.xRot)).add(root.x, root.y, root.z);
                check(Math.abs(feet.x) < .6F && Math.abs(feet.z) < .9F && feet.y > 18 && feet.y < 31, clip.id() + " keeps the feet under the resident: " + feet);
            }
            var rest = standing(77); model.setupAnim(rest);
            float legBase = model.rightLeg.xRot, armBase = model.rightArm.zRot, leftBase = model.leftArm.zRot;
            var bow = standing(77); bow.layers[1].set(clip("bow_politely"), 1.1F, 1, false, 1); model.setupAnim(bow);
            near(model.rightLeg.xRot, legBase, "Bowing at the waist leaves the legs planted");
            check(model.body.xRot > .4F && model.head.z < -2, "The upper body bends forward from the hips");
            var wave = standing(77); wave.layers[1].set(clip("wave_hello"), 1, 1, false, 1); model.setupAnim(wave);
            check(model.rightArm.zRot - armBase > 1.8F && Math.abs(model.leftArm.zRot - leftBase) < .1F, "A right-handed wave raises the right arm");
            wave.layers[1].set(clip("wave_hello"), 1, 1, true, 1); model.setupAnim(wave);
            check(leftBase - model.leftArm.zRot > 1.8F && Math.abs(model.rightArm.zRot - armBase) < .1F, "A left-handed resident waves with the left arm");
            var holding = standing(77); holding.rightArmPose = HumanoidModel.ArmPose.ITEM; model.setupAnim(holding);
            float carried = model.rightArm.xRot;
            holding.layers[1].set(clip("wave_hello"), 1, 1, false, 1); model.setupAnim(holding);
            near(model.rightArm.xRot, carried, "A carried item keeps its pose during an ordinary gesture");
            holding.layers[1].clear(); holding.layers[0].set(clip("hammer_and_anvil"), .6F, 1, false, 1); model.setupAnim(holding);
            check(Math.abs(model.rightArm.xRot - carried) > .5F, "Work clips swing the tool in hand");
            var walking = standing(77); walking.walkAnimationSpeed = .6F; walking.walkAnimationPos = 3;
            model.setupAnim(walking); float stride = model.rightLeg.xRot;
            walking.layers[1].set(clip("cheer"), .5F, 1, false, 0); model.setupAnim(walking);
            near(model.rightLeg.xRot, stride, "Reactions while walking leave the stride alone");
            var pray = standing(77); pray.layers[0].set(clip("pray"), 2.5F, 1, false, 1); model.setupAnim(pray);
            near(model.head.getChild("eye0").getChild("lid").yScale, .5F, "Praying residents close their eyes");
            var read = standing(77); read.layers[0].set(clip("read_a_book"), 1.4F, 1, false, 1);
            for (float age = 0; age < 200; age += .5F) {
                read.ageInTicks = age; read.eyeLookX = .28F; read.eyeLookY = .12F; model.setupAnim(read);
                var iris = model.head.getChild("eye0").getChild("iris");
                check(iris.x - .45F >= -3.0001F && iris.x + .45F <= -.9999F && iris.y >= -4.0001F && iris.y <= -2.9999F, "Reading eyes stay in the eye whites");
            }
            var adult = standing(77); adult.layers[0].set(clip("cheer"), .5F, 1, false, 1); model.setupAnim(adult);
            float adultHop = model.root().y;
            var baby = new ResidentModel(true); var child = standing(77); child.isBaby = true;
            child.layers[0].set(clip("cheer"), .5F, 1, false, 1); baby.setupAnim(child);
            check(baby.root().y < 0 && baby.root().y > adultHop, "Children hop at their own scale: " + baby.root().y + " vs " + adultHop);
            for (var id : List.of("twirl", "watch_a_bug", "play_airplane", "peekaboo")) { child.layers[0].set(clip(id), 1, 1, false, 1); baby.setupAnim(child); }
            var spin = standing(77); spin.layers[0].set(clip("twirl"), 2.59F, 1, false, 1); model.setupAnim(spin);
            check(Math.abs(Math.sin(model.root().yRot)) < .02, "A twirl ends facing forward again");
            int before = ResidentSkins.cachedCount();
            for (int i = 0; i < 200; i++) { var s = standing(i); s.layers[0].set(clip("hum_a_tune"), i * .02F, 1, false, 1); model.setupAnim(s); }
            check(before == ResidentSkins.cachedCount(), "Posing never bakes textures");
        });
    }

    /** The director with real residents, a real player and the real conversation window. */
    private static void director(ClientGameTestContext c, TestSingleplayerContext w) {
        var random = new Random(9012);
        UUID loner = AnimationCast.identity(random, "playful"), left = AnimationCast.identity(random, null), right = AnimationCast.identity(random, null);
        UUID host = AnimationCast.identity(random, "warmhearted");
        w.getServer().runOnServer(s -> {
            var level = s.overworld(); var p = w.getConnection().getServerPlayer();
            double x = p.getX(), y = p.getY(), z = p.getZ();
            AnimationCast.spawn(level, loner, new AnimationCast.Role("farmer", null, false), x - 6, y, z + 6, 180, false);
            AnimationCast.spawn(level, left, new AnimationCast.Role("librarian", null, false), x + 6, y, z + 6, -90, false);
            AnimationCast.spawn(level, right, new AnimationCast.Role("cleric", null, false), x + 8, y, z + 6, 90, false);
            AnimationCast.spawn(level, host, new AnimationCast.Role("cook", null, false), x, y, z + 18, 180, false);
        });
        w.getConnection().waitForClientboundEntityUpdates(EntityTypes.VILLAGER);
        c.waitTicks(5);
        int lonerId = clientId(w, loner), leftId = clientId(w, left), hostId = clientId(w, host);
        String personality = w.getServer().computeOnServer(s -> target(resident(w, host)).getAttached(PROFILE).personality());
        c.runOnClient(client -> check(personality.equals(((AttachmentTarget) client.level.getEntity(hostId)).getAttached(TEMPERAMENT)),
                "The resident's personality reaches the client for body language"));
        await(c, lonerId, life -> life.activity() != null && life.activity().trigger().equals("idle"), 400, "A resident standing around starts an idle");
        var seen = new HashSet<String>();
        for (int i = 0; i < 2400 && seen.size() < 4; i++) {
            String id = c.computeOnClient(client -> { var a = ResidentLife.of((Villager) client.level.getEntity(lonerId)).activity(); return a == null ? null : a.id(); });
            if (id != null) seen.add(id);
            c.waitTick();
        }
        check(seen.size() >= 4, "One resident moves through several different idles: " + seen);
        await(c, leftId, life -> life.activity() != null && life.activity().trigger().startsWith("chat"), 900, "Neighbors standing face to face chat");
        // Walking up to a resident earns a greeting.
        w.getServer().runCommand("tp @a ~ ~ ~-30");
        c.waitTicks(30);
        w.getServer().runOnServer(s -> { var v = resident(w, host); w.getConnection().getServerPlayer().teleportTo(v.getX(), v.getY(), v.getZ() - 3); });
        c.waitTicks(2);
        c.runOnClient(client -> { var v = client.level.getEntity(hostId); client.player.lookAt(net.minecraft.commands.arguments.EntityAnchorArgument.Anchor.EYES, v.getEyePosition()); });
        await(c, hostId, reacting("greet"), 60, "A resident greets the player who walks up");
        c.waitTicks(60);
        // Conversation: gestures while talking, a laugh at a joke, delight at a loved gift, a polite refusal.
        c.runOnClient(client -> { var v = client.level.getEntity(hostId); client.gameMode.interact(client.player, v, new EntityHitResult(v), InteractionHand.MAIN_HAND); });
        c.waitForScreen(FriendshipScreen.class);
        await(c, hostId, reacting("greet"), 20, "Opening a conversation greets the player");
        await(c, hostId, life -> life.activity() != null && life.activity().trigger().equals("chat_listen"), 240, "Residents listen once their line has typed out");
        c.clickScreenButton("Tell me about work");
        await(c, hostId, life -> life.activity() != null && life.activity().trigger().equals("talk"), 140, "Residents gesture while their reply types out");
        c.waitTicks(40);
        c.clickScreenButton("Share a joke");
        await(c, hostId, reacting("laugh"), 60, "A joke gets a laugh");
        c.takeScreenshot("village-friends-animation-portrait-laugh");
        String love = w.getServer().computeOnServer(s -> target(resident(w, host)).getAttached(PROFILE).love());
        String dislike = w.getServer().computeOnServer(s -> target(resident(w, host)).getAttached(PROFILE).dislike());
        w.getServer().runOnServer(s -> w.getConnection().getServerPlayer().setItemInHand(InteractionHand.MAIN_HAND,
                new ItemStack(BuiltInRegistries.ITEM.getValue(Identifier.parse(love)))));
        c.waitTicks(5);
        c.clickScreenButton("Give gift");
        await(c, hostId, reacting("delighted"), 60, "A loved gift delights the resident");
        c.waitTicks(10);
        c.takeScreenshot("village-friends-animation-portrait-delighted");
        w.getServer().runOnServer(s -> w.getConnection().getServerPlayer().setItemInHand(InteractionHand.MAIN_HAND,
                new ItemStack(BuiltInRegistries.ITEM.getValue(Identifier.parse(dislike)))));
        c.waitTicks(60);
        c.clickScreenButton("Give gift");
        await(c, hostId, reacting("decline"), 60, "A disliked gift is politely refused");
        c.clickScreenButton("Goodbye");
        c.waitForScreen(null);
        // Vanilla villager events and harm.
        var events = Map.of((byte) 14, "happy", (byte) 12, "love", (byte) 13, "angry", (byte) 42, "nervous");
        for (var e : events.entrySet()) {
            c.waitTicks(70);
            w.getServer().runOnServer(s -> s.overworld().broadcastEntityEvent(resident(w, loner), e.getKey()));
            await(c, lonerId, reacting(e.getValue()), 20, "Villager event " + e.getKey() + " plays " + e.getValue());
        }
        c.waitTicks(70);
        w.getServer().runOnServer(s -> resident(w, loner).hurtServer(s.overworld(), s.overworld().damageSources().magic(), .5F));
        await(c, lonerId, reacting("hurt"), 20, "Getting hurt makes a resident flinch");
        w.getServer().runOnServer(s -> resident(w, loner).setUnhappyCounter(40));
        c.waitTicks(70);
        w.getServer().runOnServer(s -> resident(w, loner).setUnhappyCounter(40));
        await(c, lonerId, reacting("decline"), 30, "A refused trade shakes the head");
        w.getServer().runCommand("tick freeze");
        c.waitTicks(5);
        int frozenAt = c.computeOnClient(client -> client.level.getEntity(lonerId).tickCount);
        var frozenClip = c.computeOnClient(client -> String.valueOf(ResidentLife.of((Villager) client.level.getEntity(lonerId)).activity()));
        c.waitTicks(80);
        int later = c.computeOnClient(client -> client.level.getEntity(lonerId).tickCount);
        String laterClip = c.computeOnClient(client -> String.valueOf(ResidentLife.of((Villager) client.level.getEntity(lonerId)).activity()));
        check(later == frozenAt && frozenClip.equals(laterClip), "A frozen world holds residents mid-motion: " + frozenAt + "/" + later + " " + frozenClip + "/" + laterClip);
        w.getServer().runCommand("tick step 3");
        c.waitTicks(5);
        int stepped = c.computeOnClient(client -> client.level.getEntity(lonerId).tickCount);
        check(stepped == frozenAt + 3, "Stepping a frozen world advances residents tick by tick: " + frozenAt + " -> " + stepped);
        w.getServer().runCommand("tick unfreeze");
    }

    /** One still per clip, held at a telling moment, grouped by situation for art review. */
    private static void gallery(ClientGameTestContext c, TestSingleplayerContext w) {
        var clips = new ArrayList<>(AnimationLibrary.current().clips());
        var random = new Random(5150);
        var ids = new ArrayList<UUID>();
        w.getServer().runOnServer(s -> {
            var p = w.getConnection().getServerPlayer();
            for (int i = 0; i < clips.size(); i++) {
                var role = AnimationCast.role(clips.get(i), i);
                var id = AnimationCast.identity(random, role.personality());
                ids.add(id);
                AnimationCast.spawn(s.overworld(), id, role, p.getX() - 12 + i % 12 * 2, p.getY(), p.getZ() - 10 - i / 12 * 2, 0, false);
            }
        });
        w.getConnection().waitForClientboundEntityUpdates(EntityTypes.VILLAGER);
        c.waitTicks(10);
        var entityIds = w.getServer().computeOnServer(s -> ids.stream().map(id -> resident(w, id).getId()).toList());
        int perPage = 20;
        for (int page = 0; page * perPage < clips.size(); page++) {
            int from = page * perPage, to = Math.min(clips.size(), from + perPage), number = page + 1;
            c.runOnClient(client -> {
                var cells = new ArrayList<AnimationShowcaseScreen.Cell>();
                for (int i = from; i < to; i++)
                    cells.add(new AnimationShowcaseScreen.Cell((Villager) client.level.getEntity(entityIds.get(i)), clips.get(i), false, clips.get(i).trigger()));
                var screen = new AnimationShowcaseScreen("VILLAGE LIFE  /  ANIMATION PACK 1  /  " + number,
                        "Every clip held at 45% of its length", cells, 5);
                screen.freeze = .45F;
                client.gui.setScreen(screen);
            });
            c.waitForScreen(AnimationShowcaseScreen.class);
            c.waitTicks(3);
            c.takeScreenshot("village-friends-animation-pack-" + number);
        }
        c.runOnClient(client -> client.gui.setScreen(null));
    }
}
