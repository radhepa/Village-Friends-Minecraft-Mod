package dev.villagefriends;

import static dev.villagefriends.VillageFriends.*;
import java.util.UUID;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.fabricmc.fabric.api.client.gametest.v1.world.TestWorldSave;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.ConversionParams;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.animal.cow.Cow;
import net.minecraft.world.entity.monster.Creeper;
import net.minecraft.world.entity.monster.skeleton.Skeleton;
import net.minecraft.world.entity.monster.zombie.Zombie;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.projectile.arrow.AbstractArrow;
import net.minecraft.world.entity.projectile.arrow.Arrow;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.phys.Vec3;

/** Native damage/death events and NBT; all fixtures are excluded from the released mod. */
@SuppressWarnings("UnstableApiUsage")
public final class GuardProgressGameTest implements FabricClientGameTest {
    private static void check(boolean ok, String message) { if (!ok) throw new AssertionError(message); }
    private static void near(double expected, double actual, String message) { check(Math.abs(expected - actual) < .0001, message + " (expected " + expected + ", got " + actual + ")"); }
    private static Villager get(TestSingleplayerContext w, UUID id) { return (Villager)w.getConnection().getServerLevel().getEntity(id); }
    private static void profession(Villager v, String job) { v.setVillagerData(v.getVillagerData().withProfession(v.level().registryAccess(), VillageProfessions.key(job))); }
    private static Villager guard(ServerLevel level, Vec3 base, String job, boolean trained, double x) {
        var v = new Villager(EntityTypes.VILLAGER, level); v.setNoAi(true); v.setPos(base.x + x, base.y, base.z + 2);
        if (!trained) profession(v, job);
        level.addFreshEntity(v);
        if (trained) profession(v, job);
        return v;
    }
    private static void stats(Villager v, int level, double xp) {
        target(v).setAttached(GUARD_PROGRESS, new GuardProgress(level, xp, "trained", "")); GuardProgression.refresh(v);
    }
    private static Zombie zombie(ServerLevel level, Vec3 base, float health) {
        var m = new Zombie(EntityTypes.ZOMBIE, level); m.setNoAi(true); m.setPos(base.x + 20, base.y, base.z + 12);
        m.getAttribute(Attributes.ARMOR).setBaseValue(0); // Isolate health contribution arithmetic from innate zombie armor.
        m.getAttribute(Attributes.MAX_HEALTH).setBaseValue(health); m.setHealth(health); level.addFreshEntity(m); return m;
    }
    private static void hit(LivingEntity victim, LivingEntity attacker, float amount) {
        victim.damageCooldownTime = 0;
        victim.hurtServer((ServerLevel)victim.level(), victim.damageSources().mobAttack(attacker), amount);
    }
    private static UUID shot(ServerLevel level, Villager archer, Zombie victim) {
        var arrow = new Arrow(level, archer, new ItemStack(Items.ARROW), archer.getMainHandItem().copy());
        arrow.setPos(victim.getX(), victim.getEyeY(), victim.getZ() - 3); arrow.setNoGravity(true);
        arrow.pickup = AbstractArrow.Pickup.DISALLOWED;
        target(arrow).setAttached(GUARD_ARROW_TARGET, victim.getUUID().toString()); GuardProgression.captureArrow(archer, arrow);
        arrow.shoot(0, 0, 1, 1.6F, 0); level.addFreshEntity(arrow); return arrow.getUUID();
    }
    @Override public void runTest(ClientGameTestContext c) {
        TestWorldSave saved;
        UUID keeper, savedCivilian, savedMob, savedContributor;
        double savedContributorXp;
        GuardProgress keeperProgress;
        try (var w = c.worldBuilder().create()) {
            w.getConnection().waitForChunksRender(); w.getServer().runCommand("gamemode creative @a"); w.getServer().runCommand("time set midnight");
            Vec3 base = w.getServer().computeOnServer(s -> {
                var p = w.getConnection().getServerPlayer(); var level = w.getConnection().getServerLevel(); var origin = p.blockPosition().above(4);
                for (int x = -28; x <= 28; x++) for (int z = -28; z <= 28; z++) {
                    level.setBlock(origin.offset(x, -1, z), Blocks.STONE.defaultBlockState(), 3);
                    for (int y = 0; y < 4; y++) level.setBlock(origin.offset(x, y, z), Blocks.AIR.defaultBlockState(), 3);
                }
                p.teleportTo(origin.getX() + .5, origin.getY(), origin.getZ() + .5); return p.position();
            });
            UUID[] guards = w.getServer().computeOnServer(s -> {
                var level = w.getConnection().getServerLevel();
                var veteran = guard(level, base, "knight", false, -12);
                var generated = GuardProgression.progress(veteran);
                check(generated.level() >= 15 && generated.level() <= 30 && generated.origin().equals("generated"), "World guards start at a saved veteran level");
                near(20 + .2 * generated.level(), veteran.getHealth(), "Generated guards start at full maximum health");
                var old = new Villager(EntityTypes.VILLAGER, level); old.setNoAi(true); old.setPos(base.x - 16, base.y, base.z + 2); profession(old, "archer");
                old.setHealth(10); target(old).setAttached(PROFILE, ResidentProfile.generate(old.getUUID(), "")); level.addFreshEntity(old);
                var migrated = GuardProgression.progress(old);
                check(migrated.origin().equals("migrated") && migrated.level() >= 15, "Existing guard migrates once");
                near(.5, old.getHealth() / old.getMaxHealth(), "Migration preserves existing injury percentage");
                var first = guard(level, base, "knight", true, 0); var second = guard(level, base, "knight", true, 4); var archer = guard(level, base, "archer", true, 8);
                check(GuardProgression.progress(first).level() == 0 && GuardProgression.progress(archer).level() == 0, "Post-load profession acquisition starts at zero");
                target(first).setAttached(GUARD_PROGRESS, new GuardProgress(20, 2.375, "trained", "")); GuardProgression.refresh(first);
                first.setHealth(7.5F);
                for (int i = 0; i < 20; i++) GuardProgression.refresh(first);
                near(24, first.getMaxHealth(), "Repeated refresh never stacks maximum health"); near(7.5, first.getHealth(), "Refresh never heals an injured guard");
                check(first.getAttribute(Attributes.MAX_HEALTH).getModifiers().stream().filter(m -> m.id().equals(GuardProgression.HEALTH_BONUS)).count() == 1, "One stable health modifier");
                profession(first, "archer"); near(24, first.getMaxHealth(), "Switching guard role retains progress before a kill");
                first.setVillagerData(first.getVillagerData().withProfession(level.registryAccess(), net.minecraft.world.entity.npc.villager.VillagerProfession.NONE));
                near(20, first.getMaxHealth(), "Leaving guard jobs removes the bonus");
                profession(first, "knight"); near(24, first.getMaxHealth(), "Returning restores the saved bonus once");
                near(2.375, GuardProgression.progress(first).xp(), "Changing jobs never rerolls XP");
                stats(first, 0, 0); first.setHealth(20); return new UUID[]{first.getUUID(), second.getUUID(), archer.getUUID()};
            });
            c.waitTicks(3); // Native equipment attributes are updated by living ticks.
            double[] meleeDamage = new double[2];
            w.getServer().runOnServer(s -> {
                var level = w.getConnection().getServerLevel(); var first = get(w, guards[0]);
                var low = zombie(level, base, 100); first.doHurtTarget(level, low); double baseline = 100 - low.getHealth(); meleeDamage[0] = baseline; low.discard();
                stats(first, 50, 0); var high = zombie(level, base, 100); first.doHurtTarget(level, high);
                meleeDamage[1] = 100 - high.getHealth(); near(baseline * 1.25, meleeDamage[1], "Native melee scales by 25% at the cap"); high.discard();
                near(30, first.getMaxHealth(), "Capped maximum health is 30");
                first.setItemSlot(EquipmentSlot.MAINHAND, new ItemStack(Items.DIAMOND_SWORD));
            }); c.waitTicks(3);
            w.getServer().runOnServer(s -> {
                var level = w.getConnection().getServerLevel(); var first = get(w, guards[0]); var mob = zombie(level, base, 100);
                first.doHurtTarget(level, mob); check(100 - mob.getHealth() > meleeDamage[1], "Upgraded weapons remain stronger at the same level"); mob.discard();
                first.getMainHandItem().enchant(s.registryAccess().lookupOrThrow(net.minecraft.core.registries.Registries.ENCHANTMENT).getOrThrow(net.minecraft.world.item.enchantment.Enchantments.SHARPNESS), 2);
                stats(first, 0, 0); var enchantedLow = zombie(level, base, 100); first.doHurtTarget(level, enchantedLow); double enchantedDamage = 100 - enchantedLow.getHealth(); enchantedLow.discard();
                stats(first, 50, 0); var enchantedHigh = zombie(level, base, 100); first.doHurtTarget(level, enchantedHigh);
                near(enchantedDamage * 1.25, 100 - enchantedHigh.getHealth(), "Native enchantment damage is scaled once before mitigation"); enchantedHigh.discard();
                stats(first, 0, 0); first.setItemSlot(EquipmentSlot.MAINHAND, new ItemStack(Items.IRON_SWORD));
                var second = get(w, guards[1]); var p = w.getConnection().getServerPlayer(); var split = zombie(level, base, 20);
                split.hurtServer(level, split.damageSources().playerAttack(p), 5); hit(split, first, 5); hit(split, second, 10);
                near(2.5, GuardProgression.progress(first).xp(), "Assisting knight gets its damage share"); near(5, GuardProgression.progress(second).xp(), "Killing knight excludes the player's share");
                check(GuardProgression.progress(first).lockedProfession().isEmpty(), "Assists do not combat-lock a job");
                check(GuardProgression.progress(second).lockedProfession().equals("villagefriends:knight"), "First qualifying killing blow locks the full profession key");
                var deathSource = split.damageSources().mobAttack(second); GuardProgression.afterDeath(split, deathSource);
                near(5, GuardProgression.progress(second).xp(), "Duplicate death callback cannot award twice");
                profession(second, "archer"); check(VillageFriends.profession(second).equals("knight"), "Combat-locked knight rejects another profession");
                second.setVillagerData(second.getVillagerData().withLevel(3)); check(second.getVillagerData().level() == 3, "Trade level remains independent and editable");
                var playerFinish = zombie(level, base, 20); hit(playerFinish, first, 10); playerFinish.damageCooldownTime = 0;
                playerFinish.hurtServer(level, playerFinish.damageSources().playerAttack(p), 10);
                near(7.5, GuardProgression.progress(first).xp(), "Player killing blow still awards the guard's contribution");
                check(GuardProgression.progress(first).lockedProfession().isEmpty(), "A player's kill does not lock an assisting guard");
                var protectedMob = zombie(level, base, 20); protectedMob.setPermanentlyInvulnerable(true); hit(protectedMob, first, 100); protectedMob.setPermanentlyInvulnerable(false);
                protectedMob.damageCooldownTime = 0; protectedMob.hurtServer(level, protectedMob.damageSources().playerAttack(p), 100);
                near(7.5, GuardProgression.progress(first).xp(), "Blocked damage does not receive a death share");
                for (LivingEntity excluded : new LivingEntity[]{new Creeper(EntityTypes.CREEPER, level), new Skeleton(EntityTypes.SKELETON, level), new Cow(EntityTypes.COW, level)}) {
                    excluded.setPos(base.x + 22, base.y, base.z + 16); ((net.minecraft.world.entity.Mob)excluded).setNoAi(true); level.addFreshEntity(excluded); hit(excluded, first, 100);
                }
                near(7.5, GuardProgression.progress(first).xp(), "Creepers, unrelated skeletons and passive animals yield no XP");
                stats(first, 0, 19.5); first.setHealth(1);
                target(first).setAttached(COMPANION, new CompanionState(p.getUUID().toString(), "downed", first.getX(), first.getY(), first.getZ(), level.getGameTime() + 1200, true, 0));
                hit(zombie(level, base, 20), first, 100);
                check(GuardProgression.progress(first).level() == 1, "A downed guard can receive credit from an already-attributed attack");
                near(1, first.getHealth(), "Leveling never revives or heals a downed guard"); target(first).setAttached(COMPANION, CompanionState.NONE);
            });
            UUID[] arrows = w.getServer().computeOnServer(s -> {
                var level = w.getConnection().getServerLevel(); var archer = get(w, guards[2]);
                archer.getMainHandItem().enchant(s.registryAccess().lookupOrThrow(net.minecraft.core.registries.Registries.ENCHANTMENT).getOrThrow(net.minecraft.world.item.enchantment.Enchantments.POWER), 2);
                var low = zombie(level, base, 100); low.setPos(base.x + 16, base.y, base.z + 12);
                var high = zombie(level, base, 100); high.setPos(base.x + 24, base.y, base.z + 12);
                stats(archer, 0, 0); UUID lowShot = shot(level, archer, low);
                stats(archer, 50, 0); UUID highShot = shot(level, archer, high); stats(archer, 0, 0);
                check(target(level.getEntity(highShot)).getAttached(GUARD_ARROW_LEVEL) == 50, "Arrow stores its firing-time level");
                return new UUID[]{low.getUUID(), high.getUUID(), lowShot, highShot};
            }); c.waitTicks(8);
            w.getServer().runOnServer(s -> {
                var level = w.getConnection().getServerLevel(); var low = (Zombie)level.getEntity(arrows[0]); var high = (Zombie)level.getEntity(arrows[1]);
                check(low.getHealth() < 100, "Real ordinary arrow hits the target"); near((100 - low.getHealth()) * 1.25, 100 - high.getHealth(), "Arrow uses firing-time level after owner changes level"); low.discard(); high.discard();
            });
            w.getServer().runOnServer(s -> {
                var level = w.getConnection().getServerLevel(); var mob = zombie(level, base, 1); mob.setPos(base.x + 24, base.y, base.z + 12);
                shot(level, get(w, guards[2]), mob);
            }); c.waitTicks(8);
            w.getServer().runOnServer(s -> {
                var archer = get(w, guards[2]); near(10, GuardProgression.progress(archer).xp(), "Native arrow kill is attributed once to its archer");
                check(GuardProgression.progress(archer).lockedProfession().equals("villagefriends:archer"), "Arrow killing blow locks Archer");
                check(!GuardController.angryAt(get(w, guards[1]), w.getConnection().getServerPlayer()), "Guard projectiles never provoke player retaliation");
            });
            UUID expiredVictim = w.getServer().computeOnServer(s -> {
                var mob = zombie(w.getConnection().getServerLevel(), base, 20); hit(mob, get(w, guards[1]), 10); return mob.getUUID();
            }); c.waitTicks(601);
            w.getServer().runOnServer(s -> {
                var level = w.getConnection().getServerLevel(); var second = get(w, guards[1]); double before = GuardProgression.progress(second).xp();
                var mob = (Zombie)level.getEntity(expiredVictim); mob.damageCooldownTime = 0; mob.hurtServer(level, mob.damageSources().generic(), 100);
                near(before, GuardProgression.progress(second).xp(), "Expired contribution receives no XP");
                var skeleton = new Skeleton(EntityTypes.SKELETON, level); skeleton.setNoAi(true); skeleton.setPos(base.x + 22, base.y, base.z + 16); level.addFreshEntity(skeleton);
                skeleton.setTarget(get(w, guards[0])); hit(skeleton, second, 100);
                near(before + 10, GuardProgression.progress(second).xp(), "An actual villager attacker outside the predator list grants XP");
            });
            keeper = w.getServer().computeOnServer(s -> {
                var first = get(w, guards[0]); target(first).setAttached(GUARD_PROGRESS, new GuardProgress(25, 12.375, "trained", "villagefriends:knight"));
                GuardProgression.refresh(first); first.setHealth(7.5F);
                first.setItemSlot(EquipmentSlot.MAINHAND, ItemStack.EMPTY); first.setItemSlot(EquipmentSlot.FEET, ItemStack.EMPTY);
                var infected = first.convertTo(EntityTypes.ZOMBIE_VILLAGER, ConversionParams.single(first, true, true), z -> z.setVillagerData(first.getVillagerData()));
                check(target(infected).getAttached(GUARD_PROGRESS).level() == 25, "Conversion preserves combat progress");
                var cured = infected.convertTo(EntityTypes.VILLAGER, ConversionParams.single(infected, true, true), v -> v.setVillagerData(infected.getVillagerData())); cured.setNoAi(true);
                var progress = GuardProgression.progress(cured);
                check(progress.level() == 25 && progress.lockedProfession().equals("villagefriends:knight"), "Cure preserves level and profession lock");
                near(25, cured.getMaxHealth(), "Cured guard restores one health bonus");
                check(cured.getMainHandItem().isEmpty() && cured.getItemBySlot(EquipmentSlot.FEET).isEmpty(), "Level/cure never regenerates broken equipment");
                cured.setHealth(7.5F); return cured.getUUID();
            });
            keeperProgress = w.getServer().computeOnServer(s -> GuardProgression.progress(get(w, keeper)));
            UUID[] last = w.getServer().computeOnServer(s -> {
                var level = w.getConnection().getServerLevel(); var civilian = new Villager(EntityTypes.VILLAGER, level); civilian.setNoAi(true); civilian.setPos(base.x - 8, base.y, base.z + 2); level.addFreshEntity(civilian);
                var mob = zombie(level, base, 20); hit(mob, get(w, guards[1]), 5); return new UUID[]{civilian.getUUID(), mob.getUUID()};
            }); savedCivilian = last[0]; savedMob = last[1]; savedContributor = guards[1];
            savedContributorXp = w.getServer().computeOnServer(s -> GuardProgression.progress(get(w, savedContributor)).xp());
            saved = w.getWorldSave();
        }
        try (var w = saved.open()) {
            w.getConnection().waitForChunksDownload();
            w.getServer().runOnServer(s -> {
                var cured = get(w, keeper); check(keeperProgress.equals(GuardProgression.progress(cured)), "NBT keeps fractional XP, origin and lock");
                near(25, cured.getMaxHealth(), "Reload never stacks health"); near(7.5, cured.getHealth(), "Native NBT retains wounded health without clamping or healing");
                check(cured.getMainHandItem().isEmpty() && cured.getItemBySlot(EquipmentSlot.FEET).isEmpty(), "Reload keeps broken equipment empty");
                profession(cured, "archer"); check(VillageFriends.profession(cured).equals("knight"), "Lock survives reload");
                var civilian = get(w, savedCivilian); profession(civilian, "archer"); check(GuardProgression.progress(civilian).level() == 0, "Saved ordinary resident becomes a level-zero trainee");
                var level = w.getConnection().getServerLevel(); var mob = (Zombie)level.getEntity(savedMob); var p = w.getConnection().getServerPlayer();
                mob.damageCooldownTime = 0; mob.hurtServer(level, mob.damageSources().playerAttack(p), 100);
                near(savedContributorXp, GuardProgression.progress(get(w, savedContributor)).xp(), "Restart clears damage contributions instead of awarding stale XP");
                check(GuardProgression.journal(cured).contains("25 / 50") && GuardProgression.journal(cured).contains("12.38 / 95"), "Existing journal displays level, fractional XP and lock");
            });
        }
        LOGGER.info("GUARD PROGRESSION PASSED: generated/trained/migrated levels, native melee/arrows, fractional assists, player credit, excluded mobs, expiry, locking, downing, equipment, conversion/cure and NBT.");
    }
}
