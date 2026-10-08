package dev.villagefriends;

import static dev.villagefriends.VillageFriends.*;
import java.util.UUID;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.monster.zombie.Zombie;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.phys.Vec3;

/** A player striking a resident down sends the neighbors running home and every guard straight at them; mobs leave the downed alone; the downed say nothing. */
@SuppressWarnings("UnstableApiUsage")
public final class VillageAlarmGameTest implements FabricClientGameTest {
    private static void check(boolean ok, String why) { if (!ok) throw new AssertionError(why); }
    private static Villager villager(TestSingleplayerContext w, UUID id) { return (Villager) w.getConnection().getServerLevel().getEntity(id); }
    private static Villager spawn(ServerLevel level, Vec3 base, String job, double x, double z) {
        var v = new Villager(EntityTypes.VILLAGER, level);
        v.setPos(base.x + x, base.y, base.z + z);
        if (job != null) {
            v.setVillagerData(v.getVillagerData().withProfession(level.registryAccess(), VillageProfessions.key(job)));
            v.setVillagerXp(1);
        }
        level.addFreshEntity(v); return v;
    }
    private static Zombie zombie(ServerLevel level, Vec3 base, double x, double z) {
        var m = new Zombie(EntityTypes.ZOMBIE, level); m.setPos(base.x + x, base.y, base.z + z);
        level.addFreshEntity(m); return m;
    }
    private static Zombie zombie(TestSingleplayerContext w, UUID id) { return (Zombie) w.getConnection().getServerLevel().getEntity(id); }
    private static void interact(ClientGameTestContext c, TestSingleplayerContext w, UUID id) {
        w.getConnection().waitForClientboundEntityUpdates(EntityTypes.VILLAGER);
        int eid = w.getServer().computeOnServer(s -> villager(w, id).getId());
        c.runOnClient(client -> { var e = client.level.getEntity(eid); client.gameMode.interact(client.player, e, new net.minecraft.world.phys.EntityHitResult(e), InteractionHand.MAIN_HAND); });
        c.waitTicks(5);
    }

    @Override public void runTest(ClientGameTestContext c) {
        try (var w = c.worldBuilder().create()) {
            w.getConnection().waitForChunksRender();
            w.getServer().runCommand("gamemode survival @a"); w.getServer().runCommand("difficulty easy");
            w.getServer().runCommand("gamerule advance_time false"); w.getServer().runCommand("gamerule spawn_mobs false");
            w.getServer().runCommand("time set 4000");
            Vec3 base = w.getServer().computeOnServer(s -> {
                var p = w.getConnection().getServerPlayer(); var level = w.getConnection().getServerLevel();
                var origin = p.blockPosition().above(4);
                for (int x = -44; x <= 44; x++) for (int z = -44; z <= 44; z++) {
                    level.setBlock(origin.offset(x, -1, z), Blocks.STONE.defaultBlockState(), 3);
                    for (int y = 0; y < 5; y++) level.setBlock(origin.offset(x, y, z), Blocks.AIR.defaultBlockState(), 3);
                }
                p.teleportTo(origin.getX() + .5, origin.getY(), origin.getZ() + .5);
                p.addEffect(new MobEffectInstance(MobEffects.RESISTANCE, 100000, 4, false, false));
                // These are village grounds.
                VillageSettlements.mark(level, origin, "Testford");
                return p.position();
            });

            // --- Mobs leave someone lying hurt on the ground alone, even one they were already after.
            UUID downed = w.getServer().computeOnServer(s -> spawn(w.getConnection().getServerLevel(), base, null, -10, -10).getUUID());
            c.waitTicks(5);
            UUID chaser = w.getServer().computeOnServer(s -> {
                var level = w.getConnection().getServerLevel(); var v = villager(w, downed);
                var z = zombie(level, base, -12, -10);
                z.setTarget(v);
                check(z.getTarget() == v, "The zombie is after the resident");
                Knockouts.knockOut(v, level);
                check(z.getTargetUnchecked() != v && z.getTarget() != v, "Knocking them out shakes the zombie off");
                return z.getUUID();
            });
            for (int i = 0; i < 5; i++) {
                c.waitTicks(20);
                w.getServer().runOnServer(s -> {
                    var v = villager(w, downed); var z = zombie(w, chaser);
                    check(z.getTargetUnchecked() != v, "The zombie doesn't go back for the downed resident");
                    check(Knockouts.knockedOut(v) && v.getHealth() == 1, "The downed resident is left untouched");
                });
            }
            w.getServer().runOnServer(s -> zombie(w, chaser).discard());

            // --- The village guards (and the neighbors) come into it.
            record Cast(UUID knight, UUID archer, UUID victim, UUID left, UUID right) {}
            var cast = w.getServer().computeOnServer(s -> {
                var level = w.getConnection().getServerLevel();
                return new Cast(spawn(level, base, "knight", 26, 0).getUUID(), spawn(level, base, "archer", -26, 4).getUUID(),
                        spawn(level, base, null, 2, 2).getUUID(), spawn(level, base, null, 7, 7).getUUID(), spawn(level, base, null, -6, 8).getUUID());
            });
            c.waitTicks(40);

            // --- A mob hurting a resident on village grounds: every guard goes straight for it, however far.
            UUID biter = w.getServer().computeOnServer(s -> {
                var level = w.getConnection().getServerLevel(); var victim = villager(w, cast.right());
                var z = zombie(level, base, -8, 10);
                victim.hurtServer(level, level.damageSources().mobAttack(z), 1);
                for (var id : new UUID[]{cast.knight(), cast.archer()})
                    check(GuardController.combatTarget(villager(w, id)) == z, "A guard " + (int) villager(w, id).distanceTo(z) + " blocks away goes straight for the zombie");
                return z.getUUID();
            });
            w.getServer().runOnServer(s -> { zombie(w, biter).discard(); GuardController.clear(); });
            c.waitTicks(40);

            // --- A player knocking a resident out: the neighbors run, the guards come at the player at once.
            record Spot(Vec3 knight, double left, double right) {}
            var before = w.getServer().computeOnServer(s -> {
                var level = w.getConnection().getServerLevel(); var p = w.getConnection().getServerPlayer(); var victim = villager(w, cast.victim());
                victim.hurtServer(level, level.damageSources().playerAttack(p), 100);
                check(Knockouts.knockedOut(victim), "The resident is knocked out");
                check(VillageAlarm.fleeing(villager(w, cast.left())) && VillageAlarm.fleeing(villager(w, cast.right())), "The neighbors panic");
                check(!VillageAlarm.fleeing(villager(w, cast.knight())), "Guards don't run away");
                for (var id : new UUID[]{cast.knight(), cast.archer()})
                    check(GuardController.combatTarget(villager(w, id)) == p, "A guard " + (int) villager(w, id).distanceTo(p) + " blocks away turns on the player at once");
                return new Spot(villager(w, cast.knight()).position(), villager(w, cast.left()).distanceTo(p), villager(w, cast.right()).distanceTo(p));
            });
            c.waitTicks(60);
            w.getServer().runOnServer(s -> {
                var p = w.getConnection().getServerPlayer();
                check(villager(w, cast.knight()).distanceTo(p) < before.knight().distanceTo(p.position()) - 6, "The knight charges the player");
                for (var neighbor : new Object[][]{{cast.left(), before.left()}, {cast.right(), before.right()}}) {
                    var v = villager(w, (UUID) neighbor[0]); double was = (Double) neighbor[1];
                    check(VillageAlarm.fleeing(v) && (v.distanceTo(p) > was + 2 || VillageAlarm.describe(v).contains("arrived=true")),
                            "A neighbor runs from the player to safety: " + was + " -> " + v.distanceTo(p) + " " + VillageAlarm.describe(v));
                }
            });
            w.getServer().runOnServer(s -> w.getConnection().getServerPlayer().teleportTo(base.x, base.y + 6, base.z - 10));
            c.getInput().lookAt(0, 30); c.waitTicks(10); c.takeScreenshot("village-alarm");
            w.getServer().runOnServer(s -> {
                GuardController.clear(); VillageAlarm.clear();
                for (var id : new UUID[]{cast.knight(), cast.archer()}) villager(w, id).discard();
                w.getConnection().getServerPlayer().teleportTo(base.x, base.y, base.z);
            });

            // --- A downed companion doesn't talk: the window narrates, silently.
            UUID friend = w.getServer().computeOnServer(s -> spawn(w.getConnection().getServerLevel(), base, null, 0, 3).getUUID());
            c.waitTicks(5);
            w.getServer().runOnServer(s -> {
                var level = w.getConnection().getServerLevel(); var p = w.getConnection().getServerPlayer(); var v = villager(w, friend);
                target(v).setAttached(COMPANION, new CompanionState(p.getUUID().toString(), "follow", v.getX(), v.getY(), v.getZ(), 0, false, level.getGameTime()));
                target(p).setAttached(PARTY, profile(v).id());
                v.hurtServer(level, v.damageSources().generic(), 100);
                check(CompanionController.state(v).downed() && Knockouts.injured(v), "The companion is downed");
            });
            c.waitTicks(5);
            interact(c, w, friend);
            for (int i = 0; i < 20 && c.computeOnClient(client -> client.gui.screen() == null); i++) c.waitTicks(10);
            if (c.computeOnClient(client -> client.gui.screen() == null)) {
                String server = w.getServer().computeOnServer(s -> {
                    var p = w.getConnection().getServerPlayer(); var v = villager(w, friend);
                    return "valid=" + validTarget(p, v) + " dist=" + p.distanceTo(v) + " los=" + p.hasLineOfSight(v) + " downed=" + CompanionController.state(v).downed()
                            + " injured=" + Knockouts.injured(v) + " alive=" + v.isAlive() + " sleeping=" + v.isSleeping();
                });
                int eid = w.getServer().computeOnServer(s -> villager(w, friend).getId());
                String client = c.computeOnClient(cl -> { var e = cl.level.getEntity(eid); return "client: " + (e == null ? "missing" : "injured=" + Knockouts.injured(e) + " downed=" + CompanionController.state((Villager) e).downed()); });
                throw new AssertionError("No window for the downed companion: " + server + " " + client);
            }
            c.runOnClient(client -> {
                check(client.gui.screen() instanceof dev.villagefriends.client.FriendshipScreen, "Right-clicking a downed companion still offers help");
                check(!((dev.villagefriends.client.FriendshipScreen) client.gui.screen()).speaking(), "A downed companion doesn't speak");
            });
            c.takeScreenshot("downed-companion-silent");
            c.runOnClient(client -> client.gui.setScreen(null));
        }
    }
}
