package dev.villagefriends;

import static dev.villagefriends.VillageFriends.*;

import dev.villagefriends.play.Games;
import dev.villagefriends.play.Games.Game;
import dev.villagefriends.play.Playground;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.function.Predicate;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.phys.Vec3;

/**
 * Children at play: each game with real children on a little playground with walls to hide behind, a child
 * following the player and freezing when looked at, games stopping for a monster and at the end of free time,
 * and bored children starting a game on their own. Screenshots: playground-*.
 * Run with {@code gradlew runClientGameTest -Ptests=PlaygroundGameTest}.
 */
@SuppressWarnings("UnstableApiUsage")
public final class PlaygroundGameTest implements FabricClientGameTest {
    private static void check(boolean ok, String why) { if (!ok) throw new AssertionError(why); }
    private static Villager kid(TestSingleplayerContext w, UUID id) { return (Villager) w.getConnection().getServerLevel().getEntity(id); }
    private static String state(TestSingleplayerContext w, UUID id) { return w.getServer().computeOnServer(s -> target(kid(w, id)).getAttached(Playground.STATE)); }
    private static List<String> states(TestSingleplayerContext w, List<UUID> ids) {
        return w.getServer().computeOnServer(s -> { var out = new ArrayList<String>(); for (var id : ids) out.add(target(kid(w, id)).getAttached(Playground.STATE)); return out; });
    }
    private static long count(List<String> states, String role) { return states.stream().filter(st -> role.equals(Games.role(st))).count(); }
    /** Waits (up to {@code ticks}) until the children's states pass the test. */
    private static List<String> await(ClientGameTestContext c, TestSingleplayerContext w, List<UUID> ids, Predicate<List<String>> test, int ticks, String why) {
        for (int t = 0; t < ticks; t += 5) {
            var now = states(w, ids);
            if (test.test(now)) return now;
            c.waitTicks(5);
        }
        throw new AssertionError(why + " (states " + states(w, ids) + ")");
    }
    private static UUID spawn(ServerLevel level, Vec3 base, double x, double z) {
        var v = new Villager(EntityTypes.VILLAGER, level);
        v.setPos(base.x + x, base.y, base.z + z);
        v.setAge(-200000);
        level.addFreshEntity(v);
        return v.getUUID();
    }
    private static void play(TestSingleplayerContext w, Game game, List<UUID> ids) {
        w.getServer().runOnServer(s -> { var group = new ArrayList<Villager>(); for (var id : ids) group.add(kid(w, id)); Playground.play(game, group); });
    }
    private static void stopAll(ClientGameTestContext c, TestSingleplayerContext w, List<UUID> ids) {
        // Lessons time ends any game; back to free play afterwards.
        w.getServer().runCommand("time set 4500");
        await(c, w, ids, st -> st.stream().allMatch(x -> x == null), 120, "Games end when free time does");
        w.getServer().runCommand("time set 8000");
        c.waitTicks(30);
    }
    private static void overhead(ClientGameTestContext c, TestSingleplayerContext w, Vec3 base, String shot) {
        w.getServer().runOnServer(s -> w.getConnection().getServerPlayer().teleportTo(base.x, base.y + 9, base.z - 9));
        c.getInput().lookAt(0, 42); c.waitTicks(4); c.takeScreenshot(shot);
    }

    @Override public void runTest(ClientGameTestContext c) {
        try (var w = c.worldBuilder().create()) {
            w.getConnection().waitForChunksRender();
            w.getServer().runCommand("gamemode creative @a");
            w.getServer().runCommand("gamerule advance_time false"); w.getServer().runCommand("gamerule spawn_mobs false"); w.getServer().runCommand("gamerule advance_weather false");
            w.getServer().runCommand("weather clear");
            // 14:00: the children's afternoon free time.
            w.getServer().runCommand("time set 8000");
            Vec3 base = w.getServer().computeOnServer(s -> {
                var p = w.getConnection().getServerPlayer(); var level = w.getConnection().getServerLevel();
                var origin = p.blockPosition().above(3);
                for (int x = -30; x <= 30; x++) for (int z = -30; z <= 30; z++) {
                    level.setBlock(origin.offset(x, -1, z), Blocks.GRASS_BLOCK.defaultBlockState(), 3);
                    for (int y = 0; y < 6; y++) level.setBlock(origin.offset(x, y, z), Blocks.AIR.defaultBlockState(), 3);
                }
                // Somewhere to hide: a few walls and a hut round the playground.
                for (int[] wall : new int[][]{{9, -3, 9, 3}, {-9, -4, -9, 2}, {-3, 10, 3, 10}, {-2, -11, 4, -11}}) {
                    for (int x = wall[0]; x <= wall[2]; x++) for (int z = wall[1]; z <= wall[3]; z++) for (int y = 0; y < 2; y++)
                        level.setBlock(origin.offset(x, y, z), Blocks.OAK_PLANKS.defaultBlockState(), 3);
                }
                p.teleportTo(origin.getX() + .5, origin.getY(), origin.getZ() + .5);
                p.addEffect(new MobEffectInstance(MobEffects.RESISTANCE, 100000, 4, false, false));
                p.getAbilities().flying = true; p.onUpdateAbilities();
                return p.position();
            });
            var kids = w.getServer().computeOnServer(s -> {
                var level = w.getConnection().getServerLevel();
                return List.of(spawn(level, base, 2, 2), spawn(level, base, -2, 2), spawn(level, base, 2, -2), spawn(level, base, -2, -2));
            });
            c.waitTicks(60);
            w.getServer().runOnServer(s -> { for (var id : kids) check(kid(w, id).isBaby() && "play".equals(target(kid(w, id)).getAttached(ROUTINE)), "The children are out playing at two in the afternoon"); });
            // Keep the player out of the way while games run.
            w.getServer().runOnServer(s -> w.getConnection().getServerPlayer().teleportTo(base.x, base.y + 9, base.z - 9));

            // --- Tag: one child is it, the rest run; someone gets tagged.
            play(w, Game.TAG, kids);
            var st = await(c, w, kids, x -> x.stream().allMatch(y -> y != null && y.startsWith("tag:")), 20, "Everyone joins the game of tag");
            check(count(st, "it") + count(st, "count") + count(st, "tagged") == 1 && count(st, "run") == 3, "One child is it, the others run: " + st);
            var firstIt = kids.get(st.indexOf(st.stream().filter(x -> !x.equals("tag:run")).findFirst().orElseThrow()));
            c.waitTicks(80);
            overhead(c, w, base, "playground-tag");
            await(c, w, kids, x -> "run".equals(Games.role(x.get(kids.indexOf(firstIt)))), 1200, "Whoever was it tags someone and runs off");
            w.getServer().runOnServer(s -> check(ResidentRoutines.doing(kid(w, kids.getFirst())).contains("tag") || ResidentRoutines.doing(kid(w, kids.getFirst())).contains("It"), "The status line says they're playing tag"));
            stopAll(c, w, kids);

            // --- Hide-and-seek: the seeker counts with eyes covered, the others hide behind the walls, and get found.
            play(w, Game.HIDE_AND_SEEK, kids);
            st = await(c, w, kids, x -> count(x, "count") == 1, 200, "The seeker gets to home base and counts");
            st = await(c, w, kids, x -> count(x, "hidden") >= 2, 260, "The others reach their hiding places");
            var hidden = new ArrayList<UUID>();
            for (int i = 0; i < kids.size(); i++) if ("hidden".equals(Games.role(st.get(i)))) hidden.add(kids.get(i));
            w.getServer().runOnServer(s -> {
                for (var id : hidden) check(kid(w, id).position().distanceTo(base) > 4, "Hiders go off to hide, not stand at home base");
            });
            overhead(c, w, base, "playground-hide-count");
            await(c, w, kids, x -> count(x, "seek") == 1, 260, "Ready or not: the seeker goes looking");
            await(c, w, kids, x -> count(x, "found") + count(x, "home") + count(x, "point") >= 1, 1600, "The seeker finds someone");
            overhead(c, w, base, "playground-hide-found");
            stopAll(c, w, kids);

            // --- Ring-around-the-rosie: hands joined in a ring, round and round, and all fall down.
            play(w, Game.RING, kids);
            await(c, w, kids, x -> count(x, "walk") == 4, 300, "The children join hands in a ring and go round");
            c.waitTicks(40);
            w.getServer().runOnServer(s -> {
                double cx = 0, cz = 0; for (var id : kids) { cx += kid(w, id).getX() / 4; cz += kid(w, id).getZ() / 4; }
                for (var id : kids) {
                    double r = Math.hypot(kid(w, id).getX() - cx, kid(w, id).getZ() - cz);
                    check(r > 1.2 && r < 4, "Each child stands on the ring: " + r);
                }
            });
            c.getInput().lookAt(0, 50); c.waitTicks(4); c.takeScreenshot("playground-ring");
            await(c, w, kids, x -> count(x, "fall") == 4, 320, "They all fall down together");
            c.waitTicks(14); c.takeScreenshot("playground-ring-fall");
            stopAll(c, w, kids);

            // --- Follow the leader: a line behind the leader, copying every move down the line.
            play(w, Game.FOLLOW_THE_LEADER, kids);
            st = await(c, w, kids, x -> x.stream().anyMatch(y -> y != null && y.contains(":do:")), 900, "The leader shows a move");
            String move = st.stream().filter(y -> y != null && y.contains(":do:")).findFirst().orElseThrow();
            await(c, w, kids, x -> x.stream().filter(move::equals).count() >= 2, 120, "The line copies the leader's move (" + move + ")");
            overhead(c, w, base, "playground-leader");
            stopAll(c, w, kids);

            // --- Catch: two children toss the leather ball; it flies between them.
            var pair = kids.subList(0, 2);
            play(w, Game.CATCH, pair);
            await(c, w, pair, x -> x.stream().anyMatch(y -> y != null && "throw".equals(Games.role(y))), 500, "A throw comes");
            int thrower = w.getServer().computeOnServer(s -> {
                for (var id : pair) if ("throw".equals(Games.role(target(kid(w, id)).getAttached(Playground.STATE)))) return kid(w, id).getId();
                return -1;
            });
            w.getServer().runOnServer(s -> w.getConnection().getServerPlayer().teleportTo(base.x + 6, base.y + 2, base.z + 6));
            c.getInput().lookAt(135, 18);
            c.waitTicks(Playground.RELEASE + 4);
            c.runOnClient(client -> {
                var v = (Villager) client.level.getEntity(thrower);
                var renderer = (dev.villagefriends.client.ResidentRenderer) client.getEntityRenderDispatcher().getRenderer(v);
                check(renderer.createRenderState(v, 1).ballShown, "The client draws the ball in the air");
            });
            c.takeScreenshot("playground-catch");
            await(c, w, pair, x -> x.stream().anyMatch(y -> y != null && ("hold".equals(Games.role(y)) || "fumble".equals(Games.role(y)))), 80, "The ball is caught (or fumbled)");
            stopAll(c, w, kids);

            // --- A curious child follows the player, and freezes all innocent when the player turns round.
            UUID curious = kids.getFirst();
            w.getServer().runOnServer(s -> { var p = w.getConnection().getServerPlayer(); p.teleportTo(base.x + 6, base.y, base.z); Playground.follow(kid(w, curious), p); });
            c.getInput().lookAt(-90, 0);
            c.waitTicks(20);
            w.getServer().runOnServer(s -> w.getConnection().getServerPlayer().teleportTo(base.x + 12, base.y, base.z + 2));
            c.getInput().lookAt(-90, 0);
            await(c, w, List.of(curious), x -> "curious:follow".equals(x.getFirst()) || "curious:watch".equals(x.getFirst()), 60, "The curious child tags along");
            c.waitTicks(120);
            w.getServer().runOnServer(s -> check(kid(w, curious).distanceTo(w.getConnection().getServerPlayer()) < 6, "They keep close behind: " + kid(w, curious).distanceTo(w.getConnection().getServerPlayer())));
            check(w.getServer().computeOnServer(s -> ResidentRoutines.doing(kid(w, curious))).equals("Following you around"), "The status line says they're following you");
            // Turn round and look straight at them.
            w.getServer().runOnServer(s -> {
                var p = w.getConnection().getServerPlayer(); var k = kid(w, curious);
                double dx = k.getX() - p.getX(), dz = k.getZ() - p.getZ();
                p.setYRot((float) Math.toDegrees(Math.atan2(-dx, dz))); p.setXRot(20);
            });
            int curiousId = w.getServer().computeOnServer(s -> kid(w, curious).getId());
            c.runOnClient(client -> client.player.lookAt(net.minecraft.commands.arguments.EntityAnchorArgument.Anchor.EYES, client.level.getEntity(curiousId).getEyePosition()));
            await(c, w, List.of(curious), x -> "curious:caught".equals(x.getFirst()), 40, "Looked at, they freeze and act innocent");
            c.waitTicks(10); c.takeScreenshot("playground-curious-caught");
            stopAll(c, w, kids);

            // --- A monster nearby stops every game at once.
            play(w, Game.TAG, kids);
            await(c, w, kids, x -> x.stream().allMatch(y -> y != null), 20, "A new game of tag starts");
            w.getServer().runOnServer(s -> EntityTypes.ZOMBIE.spawn(w.getConnection().getServerLevel(), BlockPos.containing(base.x + 10, base.y, base.z + 10), EntitySpawnReason.COMMAND));
            await(c, w, kids, x -> x.stream().allMatch(y -> y == null), 40, "Everyone stops playing when a monster comes");
            w.getServer().runCommand("kill @e[type=zombie]");
            c.waitTicks(10);

            // --- Left to themselves, bored children start a game (or follow you) on their own.
            w.getServer().runOnServer(s -> w.getConnection().getServerPlayer().teleportTo(base.x, base.y + 9, base.z - 9));
            await(c, w, kids, x -> x.stream().anyMatch(y -> y != null), 3200, "Bored children start something on their own");
            overhead(c, w, base, "playground-own-game");
        }
    }
}
