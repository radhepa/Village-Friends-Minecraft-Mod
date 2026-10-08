package dev.villagefriends;

import static dev.villagefriends.VillageFriends.*;
import dev.villagefriends.routine.Routine;
import java.util.ArrayList;
import java.util.List;
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
import net.minecraft.world.entity.Pose;
import net.minecraft.world.entity.ai.village.poi.PoiTypes;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.schedule.Activity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.phys.Vec3;

/** Knockouts, treatment and permanent death; downed companions lying down; night patrol squads; raid muster. */
@SuppressWarnings("UnstableApiUsage")
public final class KnockoutGameTest implements FabricClientGameTest {
    private static final long HOUR = 60L * 60 * 20;
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
    private static void interact(ClientGameTestContext c, TestSingleplayerContext w, UUID id) {
        w.getConnection().waitForClientboundEntityUpdates(EntityTypes.VILLAGER);
        int eid = w.getServer().computeOnServer(s -> villager(w, id).getId());
        c.runOnClient(client -> { var e = client.level.getEntity(eid); client.gameMode.interact(client.player, e, new net.minecraft.world.phys.EntityHitResult(e), InteractionHand.MAIN_HAND); });
        c.waitTicks(5);
    }
    private static void hold(TestSingleplayerContext w, String item, int n) {
        w.getServer().runOnServer(s -> w.getConnection().getServerPlayer().setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(VillageItems.get(item), n)));
        w.getConnection().waitForClientboundPackets();
    }
    private static int held(TestSingleplayerContext w) { return w.getServer().computeOnServer(s -> w.getConnection().getServerPlayer().getMainHandItem().getCount()); }
    private static void knockOut(TestSingleplayerContext w, UUID id) {
        w.getServer().runOnServer(s -> { var v = villager(w, id); v.hurtServer(w.getConnection().getServerLevel(), v.damageSources().generic(), 100); });
    }
    private static UUID firstLeader(List<UUID> guards) {
        for (var id : guards) { var squad = GuardPatrols.squad(id); if (!squad.isEmpty()) return squad.getFirst(); }
        throw new AssertionError("No patrol squad formed");
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
                for (int x = -40; x <= 40; x++) for (int z = -40; z <= 40; z++) {
                    level.setBlock(origin.offset(x, -1, z), Blocks.STONE.defaultBlockState(), 3);
                    for (int y = 0; y < 5; y++) level.setBlock(origin.offset(x, y, z), Blocks.AIR.defaultBlockState(), 3);
                }
                p.teleportTo(origin.getX() + .5, origin.getY(), origin.getZ() + .5);
                p.addEffect(new MobEffectInstance(MobEffects.RESISTANCE, 100000, 4, false, false));
                return p.position();
            });

            // --- A fatal blow knocks a resident out instead of killing them.
            UUID patient = w.getServer().computeOnServer(s -> spawn(w.getConnection().getServerLevel(), base, null, 0, 3).getUUID());
            c.waitTicks(5);
            knockOut(w, patient);
            w.getServer().runOnServer(s -> {
                var level = w.getConnection().getServerLevel(); var v = villager(w, patient);
                check(v.isAlive() && Knockouts.knockedOut(v), "A fatal blow knocks the resident out");
                check(v.getPose() == Pose.SLEEPING && Knockouts.injured(v), "The knocked-out resident lies on the ground");
                check(Math.abs(v.getBbWidth() - 1F) < .01F && v.getBbHeight() < .6F, "Lying residents have a low, body-sized hitbox: " + v.getBbWidth() + "x" + v.getBbHeight());
                var st = Knockouts.state(v);
                check(st.until() - st.since() == 24 * HOUR, "The clock is a full day of play in ticks");
                check(!v.hurtServer(level, v.damageSources().generic(), 100), "Nobody can hurt a knocked-out resident");
                check(!v.canBeSeenAsEnemy(), "Mobs don't target a knocked-out resident");
                check(ResidentRoutines.doing(v).startsWith("Unconscious"), "The status line says they're unconscious");
            });
            int patientEntity = w.getServer().computeOnServer(s -> villager(w, patient).getId());
            c.waitFor(client -> client.level.getEntity(patientEntity) instanceof Villager v && Knockouts.injured(v) && v.hasPose(Pose.SLEEPING), 100);
            c.waitTicks(5);
            c.runOnClient(client -> {
                var v = (Villager) client.level.getEntity(patientEntity);
                var renderer = (dev.villagefriends.client.ResidentRenderer) client.getEntityRenderDispatcher().getRenderer(v);
                check(renderer.createRenderState(v, 1).injured, "The client draws the resident lying injured");
                check(v.getBbWidth() > .9F, "The client gets the clickable lying hitbox too");
            });
            c.getInput().lookAt(0, 35); c.waitTicks(10); c.takeScreenshot("knockout-lying");
            w.getServer().runOnServer(s -> w.getConnection().getServerPlayer().teleportTo(base.x + 2.5, base.y, base.z + 3));
            c.getInput().lookAt(90, 40); c.waitTicks(10); c.takeScreenshot("knockout-lying-side");
            w.getServer().runOnServer(s -> w.getConnection().getServerPlayer().teleportTo(base.x, base.y, base.z));

            // --- Checking on them opens no conversation; a bandage buys twelve hours; salts wake them.
            interact(c, w, patient);
            c.runOnClient(client -> check(client.gui.screen() == null, "No conversation with someone unconscious"));
            long before = w.getServer().computeOnServer(s -> Knockouts.state(villager(w, patient)).until());
            hold(w, "bandage_wrap", 2); interact(c, w, patient);
            w.getServer().runOnServer(s -> check(Knockouts.state(villager(w, patient)).until() - before == 12 * HOUR, "A Bandage Wrap adds twelve hours"));
            check(held(w) == 1, "The bandage is used up");
            hold(w, "smelling_salts", 1); interact(c, w, patient);
            w.getServer().runOnServer(s -> {
                var v = villager(w, patient);
                check(!Knockouts.knockedOut(v) && !Knockouts.injured(v) && v.getPose() == Pose.STANDING, "Smelling Salts wake them up");
                check(Math.abs(v.getHealth() - v.getMaxHealth() * .2F) < .01F, "Smelling Salts restore a fifth of their health: " + v.getHealth());
                check(v.getBbHeight() > 1.5F, "They stand up with a normal hitbox");
            });
            check(held(w) == 0, "The salts are used up");

            // --- A Revival Tonic restores everything.
            knockOut(w, patient);
            hold(w, "revival_tonic", 1); interact(c, w, patient);
            w.getServer().runOnServer(s -> { var v = villager(w, patient); check(!Knockouts.knockedOut(v) && v.getHealth() == v.getMaxHealth(), "A Revival Tonic restores full health"); });

            // --- The village apothecary comes over and dresses a patient's wounds once.
            UUID hurt = w.getServer().computeOnServer(s -> spawn(w.getConnection().getServerLevel(), base, null, -8, 8).getUUID());
            UUID doctor = w.getServer().computeOnServer(s -> spawn(w.getConnection().getServerLevel(), base, "apothecary", 8, 8).getUUID());
            c.waitTicks(5);
            knockOut(w, hurt);
            long untreated = w.getServer().computeOnServer(s -> Knockouts.state(villager(w, hurt)).until());
            for (int i = 0; i < 30 && !w.getServer().computeOnServer(s -> Knockouts.state(villager(w, hurt)).tended()); i++) c.waitTicks(20);
            w.getServer().runOnServer(s -> check(Knockouts.state(villager(w, hurt)).until() - untreated == 12 * HOUR, "The apothecary's dressing adds twelve hours"));

            // --- The clock running out is permanent; /kill still kills outright.
            w.getServer().runOnServer(s -> {
                var v = villager(w, hurt); var st = Knockouts.state(v);
                target(v).setAttached(KNOCKOUT, new KnockoutState(st.since(), w.getConnection().getServerLevel().getGameTime() + 5, st.bandages(), true));
            });
            c.waitTicks(20);
            w.getServer().runOnServer(s -> check(villager(w, hurt) == null || !villager(w, hurt).isAlive(), "Unrevived residents die when the day runs out"));
            w.getServer().runOnServer(s -> { var v = villager(w, doctor); v.kill(w.getConnection().getServerLevel()); check(!v.isAlive(), "/kill still kills"); });

            // --- A downed companion lies on the ground the same way, and gets up when helped.
            UUID friend = w.getServer().computeOnServer(s -> spawn(w.getConnection().getServerLevel(), base, null, 0, 3).getUUID());
            c.waitTicks(5);
            w.getServer().runOnServer(s -> {
                var level = w.getConnection().getServerLevel(); var p = w.getConnection().getServerPlayer(); var v = villager(w, friend);
                target(v).setAttached(COMPANION, new CompanionState(p.getUUID().toString(), "follow", v.getX(), v.getY(), v.getZ(), 0, false, level.getGameTime()));
                target(p).setAttached(PARTY, profile(v).id());
                v.hurtServer(level, v.damageSources().generic(), 100);
                check(CompanionController.state(v).downed() && !Knockouts.knockedOut(v), "A companion is downed, not knocked out");
                check(v.getPose() == Pose.SLEEPING && Knockouts.injured(v), "A downed companion lies on the ground");
            });
            w.getServer().runOnServer(s -> w.getConnection().getServerPlayer().teleportTo(base.x + 2.5, base.y, base.z + 3));
            c.getInput().lookAt(90, 40); c.waitTicks(20); c.takeScreenshot("downed-companion");
            w.getServer().runOnServer(s -> {
                var v = villager(w, friend);
                check(v.getPose() == Pose.SLEEPING, "A downed companion stays down");
                check(CompanionController.handle(w.getConnection().getServerPlayer(), v, "rescue"), "Helping a downed companion up works");
                check(v.getPose() == Pose.STANDING && !Knockouts.injured(v), "A rescued companion stands up");
                CompanionController.returnHome(v, w.getConnection().getServerPlayer(), false);
            });

            // --- At night the guards walk the village in squads of two or more.
            List<UUID> guards = w.getServer().computeOnServer(s -> {
                var level = w.getConnection().getServerLevel(); var ids = new ArrayList<UUID>();
                for (int i = 0; i < 4; i++) ids.add(spawn(level, base, i % 2 == 0 ? "knight" : "archer", -6 + i * 4, -6).getUUID());
                return ids;
            });
            w.getServer().runCommand("time set 17000");
            c.waitTicks(260);
            w.getServer().runOnServer(s -> {
                int onWatch = 0;
                for (var id : guards) {
                    if (!Routine.Block.NIGHT_WATCH.id().equals(target(villager(w, id)).getAttached(ROUTINE))) continue;
                    onWatch++;
                    check(GuardPatrols.squad(id).size() >= 2, "Every guard on watch has a squad of two or more");
                }
                check(onWatch >= 2, "At least two guards keep the watch: " + onWatch);
            });
            UUID leaderId = w.getServer().computeOnServer(s -> firstLeader(guards));
            Vec3 start = w.getServer().computeOnServer(s -> villager(w, leaderId).position());
            c.waitTicks(300);
            w.getServer().runOnServer(s -> {
                var leader = villager(w, leaderId);
                check(leader.position().distanceTo(start) > 3, "The squad leader walks the patrol route");
                for (var id : GuardPatrols.squad(leaderId)) check(villager(w, id).distanceTo(leader) < 12, "The squad sticks together");
            });
            w.getServer().runOnServer(s -> {
                var p = w.getConnection().getServerPlayer(); var leader = villager(w, leaderId);
                p.addEffect(new MobEffectInstance(MobEffects.NIGHT_VISION, 2000, 0, false, false));
                p.teleportTo(leader.getX(), leader.getY() + 6, leader.getZ() - 7);
            });
            c.getInput().lookAt(0, 22); c.waitTicks(15); c.takeScreenshot("night-patrol");

            // --- A raid calls the guards out instead of sending them into hiding.
            w.getServer().runCommand("time set 4000");
            w.getServer().runOnServer(s -> {
                var level = w.getConnection().getServerLevel(); var p = w.getConnection().getServerPlayer();
                var bell = BlockPos.containing(base).offset(0, 0, -14);
                level.setBlock(bell, Blocks.BELL.defaultBlockState(), 3);
                level.getPoiManager().take(h -> h.is(PoiTypes.MEETING), (h, pos) -> true, bell, 4);
                p.addEffect(new MobEffectInstance(MobEffects.RAID_OMEN, 600, 0));
                check(level.getRaids().createOrExtendRaid(p, bell) != null, "Test raid starts");
            });
            c.waitTicks(120);
            w.getServer().runOnServer(s -> w.getConnection().getServerPlayer().teleportTo(base.x, base.y + 5, base.z - 5));
            c.getInput().lookAt(180, 30); c.waitTicks(10); c.takeScreenshot("raid-muster");
            w.getServer().runOnServer(s -> {
                for (var id : guards) {
                    var g = villager(w, id);
                    check(GuardPatrols.defending(g) && Routine.Block.DEFEND.id().equals(target(g).getAttached(ROUTINE)), "Guards are called out to defend the village");
                    var activity = g.getBrain().getActiveNonCoreActivity().orElse(Activity.IDLE);
                    check(activity != Activity.HIDE && activity != Activity.RAID && activity != Activity.PRE_RAID && !g.isSleeping(), "Guards don't hide from the raid: " + activity);
                }
                var raid = w.getConnection().getServerLevel().getRaidAt(BlockPos.containing(base).offset(0, 0, -14));
                if (raid != null) raid.stop();
            });
            c.waitTicks(40);
            w.getServer().runOnServer(s -> { for (var id : guards) check(!GuardPatrols.defending(villager(w, id)), "Guards stand down when the raid is over"); });
        }
    }
}
