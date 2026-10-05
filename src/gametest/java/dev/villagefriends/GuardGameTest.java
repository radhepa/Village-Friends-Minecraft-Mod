package dev.villagefriends;

import static dev.villagefriends.VillageFriends.*;
import java.util.UUID;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.fabricmc.fabric.api.client.gametest.v1.world.TestWorldSave;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.ConversionParams;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.monster.zombie.Zombie;
import net.minecraft.world.entity.monster.Creeper;
import net.minecraft.world.entity.monster.skeleton.Skeleton;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.projectile.arrow.AbstractArrow;
import net.minecraft.world.entity.projectile.arrow.Arrow;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.enchantment.Enchantments;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.phys.Vec3;

/** Real Minecraft AI, damage, equipment and save fixtures; excluded from the release jar. */
@SuppressWarnings("UnstableApiUsage")
public final class GuardGameTest implements FabricClientGameTest {
    private static final EquipmentSlot[] ARMOR = {EquipmentSlot.HEAD,EquipmentSlot.CHEST,EquipmentSlot.LEGS,EquipmentSlot.FEET};
    private static void check(boolean ok, String why) { if (!ok) throw new AssertionError(why); }
    private static Villager villager(TestSingleplayerContext w, UUID id) { return (Villager)w.getConnection().getServerLevel().getEntity(id); }
    private static Villager spawn(ServerLevel level, Vec3 base, String job, double x, double z) {
        var v = new Villager(EntityTypes.VILLAGER, level);
        v.setPos(base.x + x, base.y, base.z + z); v.setNoAi(true);
        if (job != null) {
            v.setVillagerData(v.getVillagerData().withProfession(level.registryAccess(), VillageProfessions.key(job)));
            v.setVillagerXp(1);
        }
        level.addFreshEntity(v); return v;
    }
    private static Zombie zombie(ServerLevel level, Vec3 base, double x, double z) {
        var m = new Zombie(EntityTypes.ZOMBIE, level); m.setPos(base.x+x,base.y,base.z+z); m.setNoAi(true);
        m.getAttribute(Attributes.MAX_HEALTH).setBaseValue(100); m.setHealth(100);
        m.setItemSlot(EquipmentSlot.HEAD, new ItemStack(Items.IRON_HELMET));
        level.addFreshEntity(m); return m;
    }
    private static int count(net.minecraft.server.level.ServerPlayer p, net.minecraft.world.item.Item item) {
        int n = 0; for (int i=0;i<p.getInventory().getContainerSize();i++) { var s=p.getInventory().getItem(i); if(s.is(item)) n+=s.getCount(); } return n;
    }
    private static void reset(TestSingleplayerContext w, UUID k, UUID a, Vec3 base) {
        w.getServer().runOnServer(s -> {
            GuardController.clear();
            var knight=villager(w,k); var archer=villager(w,a);
            knight.setNoAi(true); archer.setNoAi(true); knight.stopUsingItem(); archer.stopUsingItem();
            knight.getNavigation().stop(); archer.getNavigation().stop();
            knight.setDeltaMovement(Vec3.ZERO); archer.setDeltaMovement(Vec3.ZERO);
            knight.setPos(base.x,base.y,base.z+2); archer.setPos(base.x+4,base.y,base.z+2);
            knight.setHealth(knight.getMaxHealth()); archer.setHealth(archer.getMaxHealth());
        });
    }
    @Override public void runTest(ClientGameTestContext c) {
        TestWorldSave saved;
        UUID knightId, archerId, babyId, naturalId, curedId;
        Vec3 base;
        try (var w=c.worldBuilder().create()) {
            w.getConnection().waitForChunksRender(); w.getServer().runCommand("gamemode creative @a");
            base=w.getServer().computeOnServer(s -> {
                var p=w.getConnection().getServerPlayer(); var level=w.getConnection().getServerLevel();
                var origin=p.blockPosition().above(4);
                for(int x=-36;x<=36;x++) for(int z=-36;z<=36;z++) {
                    level.setBlock(origin.offset(x,-1,z),Blocks.STONE.defaultBlockState(),3);
                    for(int y=0;y<4;y++) level.setBlock(origin.offset(x,y,z),Blocks.AIR.defaultBlockState(),3);
                }
                p.teleportTo(origin.getX()+.5,origin.getY(),origin.getZ()+.5);
                return p.position();
            });
            knightId=w.getServer().computeOnServer(s -> spawn(w.getConnection().getServerLevel(),base,"knight",0,2).getUUID());
            archerId=w.getServer().computeOnServer(s -> spawn(w.getConnection().getServerLevel(),base,"archer",4,2).getUUID());
            babyId=w.getServer().computeOnServer(s -> {
                var v=new Villager(EntityTypes.VILLAGER,w.getConnection().getServerLevel()); v.setPos(base.x+8,base.y,base.z+2); v.setNoAi(true); v.setAge(-24000);
                v.setVillagerData(v.getVillagerData().withProfession(s.registryAccess(),VillageProfessions.key("knight")));
                w.getConnection().getServerLevel().addFreshEntity(v);
                check(v.getMainHandItem().isEmpty(),"Children receive no combat gear");
                return v.getUUID();
            });
            w.getServer().runOnServer(s -> {
                var k=villager(w,knightId); var a=villager(w,archerId); var p=w.getConnection().getServerPlayer();
                check(k.getMainHandItem().is(Items.IRON_SWORD) && a.getMainHandItem().is(Items.BOW),"Default role weapons");
                for(var v:new Villager[]{k,a}) {
                    int iron=0,chain=0;
                    for(var slot:ARMOR) { String item=net.minecraft.core.registries.BuiltInRegistries.ITEM.getKey(v.getItemBySlot(slot).getItem()).getPath(); if(item.startsWith("iron_"))iron++;if(item.startsWith("chainmail_"))chain++; }
                    check(iron==2 && chain==2,"Exactly two iron and two chainmail armor pieces");
                    check(target(v).getAttachedOrElse(GUARD_EQUIPPED,false),"Initialization marker persists");
                }
                var upgraded=new ItemStack(Items.DIAMOND_SWORD); upgraded.setDamageValue(17);
                upgraded.enchant(s.registryAccess().lookupOrThrow(Registries.ENCHANTMENT).getOrThrow(Enchantments.SHARPNESS),2);
                p.setItemInHand(InteractionHand.MAIN_HAND,upgraded);
                int old=count(p,Items.IRON_SWORD);
                check(CompanionController.handle(p,k,"equip"),"Peaceful stranger can exchange without recruitment");
                check(k.getMainHandItem().is(Items.DIAMOND_SWORD) && k.getMainHandItem().getDamageValue()==17 && k.getMainHandItem().isEnchanted(),"Upgrade retains durability/enchantments");
                check(count(p,Items.DIAMOND_SWORD)==0 && count(p,Items.IRON_SWORD)==old+1,"Creative consumes exactly one item and returns old sword");
                p.setItemInHand(InteractionHand.MAIN_HAND,ItemStack.EMPTY); int returned=count(p,Items.IRON_SWORD);
                check(!CompanionController.handle(p,k,"equip") || count(p,Items.IRON_SWORD)==returned,"Replayed empty exchange cannot duplicate");
                p.setItemInHand(InteractionHand.MAIN_HAND,new ItemStack(Items.APPLE,3));
                CompanionController.handle(p,k,"equip"); check(p.getMainHandItem().getCount()==3 && k.getMainHandItem().is(Items.DIAMOND_SWORD),"Rejected item kept");
                p.setItemInHand(InteractionHand.MAIN_HAND,new ItemStack(Items.BOW)); CompanionController.handle(p,k,"equip"); check(!p.getMainHandItem().isEmpty(),"Knight rejects bows");
                p.setItemInHand(InteractionHand.MAIN_HAND,new ItemStack(Items.IRON_SWORD)); CompanionController.handle(p,a,"equip"); check(!p.getMainHandItem().isEmpty(),"Archer rejects swords");
                p.setItemInHand(InteractionHand.MAIN_HAND,new ItemStack(Items.NETHERITE_CHESTPLATE));
                CompanionController.handle(p,k,"equip"); check(k.getItemBySlot(EquipmentSlot.CHEST).is(Items.NETHERITE_CHESTPLATE),"Armor upgrade without recruitment");
                k.setItemSlot(EquipmentSlot.FEET,ItemStack.EMPTY); GuardController.initializeEquipment(k); check(k.getItemBySlot(EquipmentSlot.FEET).isEmpty(),"Missing/broken equipment never regenerates");
                target(k).setAttached(COMPANION,new CompanionState(UUID.randomUUID().toString(),"wait",base.x,base.y,base.z,0,true,0));
                check(!GuardController.canExchange(k,p),"Recruited guards refuse non-owner equipment exchanges");
                target(k).setAttached(COMPANION,new CompanionState(p.getUUID().toString(),"downed",base.x,base.y,base.z,levelTime(k)+100,true,0));
                check(!GuardController.canExchange(k,p),"Downed guard refuses exchanges");
                target(k).setAttached(COMPANION,new CompanionState(p.getUUID().toString(),"picnic",base.x,base.y,base.z,0,true,0));
                check(!GuardController.canExchange(k,p),"Activity participant refuses exchanges");
                target(k).setAttached(COMPANION,CompanionState.NONE);
                var baby=villager(w,babyId); baby.setAge(0); GuardController.initializeEquipment(baby); check(baby.getMainHandItem().is(Items.IRON_SWORD),"Grown guard initializes once");
            });
            // Natural job acquisition exercises initialization after entity load.
            naturalId=w.getServer().computeOnServer(s -> {
                var level=w.getConnection().getServerLevel(); var v=spawn(level,base,null,-12,0); v.setNoAi(false);
                level.setBlock(BlockPos.containing(base.add(-13,0,0)),VillageBlocks.get("training_dummy").defaultBlockState(),3);
                return v.getUUID();
            });
            w.getServer().runCommand("time set day");
            for (int t=0;t<900;t+=20) {
                c.waitTicks(20);
                if(w.getServer().computeOnServer(s -> GuardController.isGuard(villager(w,naturalId)))) break;
            }
            w.getServer().runOnServer(s -> {var v=villager(w,naturalId);check(GuardController.isGuard(v)&&v.getMainHandItem().is(Items.IRON_SWORD),"Naturally acquired guard job receives equipment");v.setNoAi(true);});
            // Knights use native damage and sword/armor durability.
            UUID foe=w.getServer().computeOnServer(s -> {
                var k=villager(w,knightId); k.setItemSlot(EquipmentSlot.MAINHAND,new ItemStack(Items.IRON_SWORD)); k.setNoAi(false);
                return zombie(w.getConnection().getServerLevel(),base,3,2).getUUID();
            });
            c.waitTicks(80);
            w.getServer().runOnServer(s -> {
                var level=w.getConnection().getServerLevel(); var k=villager(w,knightId); var m=(Zombie)level.getEntity(foe);
                check(m.getHealth()<100,"Knight deals real melee damage"); check(k.getMainHandItem().getDamageValue()>0,"Melee consumes native sword durability");
                m.discard(); k.setInvulnerableTime(0); float before=k.getHealth(); k.hurtServer(level,k.damageSources().mobAttack(zombie(level,base,24,24)),4);
                check(k.getHealth()>before-4,"Armor reduces damage");
                check(k.getItemBySlot(EquipmentSlot.CHEST).getDamageValue()>0,"Native armor wear applies to guards");
                level.getEntitiesOfClass(Zombie.class,k.getBoundingBox().inflate(50)).forEach(Zombie::discard);
            });
            reset(w,knightId,archerId,base);
            // Archers use real projectiles, with a native draw pose and enchanted weapon source.
            UUID rangedFoe=w.getServer().computeOnServer(s -> {
                var a=villager(w,archerId); a.setNoAi(false); a.setPos(base.x+4,base.y,base.z+2);
                w.getConnection().getServerPlayer().teleportTo(base.x+4,base.y,base.z-1);
                return zombie(w.getConnection().getServerLevel(),base,4,12).getUUID();
            });
            c.getInput().lookAt(0,0);
            int archerEntity=w.getServer().computeOnServer(s->villager(w,archerId).getId());
            c.waitFor(client -> client.level.getEntity(archerEntity) instanceof Villager v && v.isUsingItem(),100);
            c.runOnClient(client -> {
                var v=(Villager)client.level.getEntity(archerEntity);
                var renderer=(dev.villagefriends.client.ResidentRenderer)client.getEntityRenderDispatcher().getRenderer(v);
                var render=renderer.createRenderState(v,1);
                check(render.rightArmPose==net.minecraft.client.model.HumanoidModel.ArmPose.BOW_AND_ARROW
                        || render.leftArmPose==net.minecraft.client.model.HumanoidModel.ArmPose.BOW_AND_ARROW,"Actual archer has bow-drawing pose");
            });
            c.takeScreenshot("village-friends-guard-bow-draw");
            c.waitTicks(100);
            w.getServer().runOnServer(s -> {
                var level=w.getConnection().getServerLevel(); var a=villager(w,archerId); var m=(Zombie)level.getEntity(rangedFoe);
                check(m.getHealth()<100,"Archer arrows cause actual ranged damage"); check(a.getMainHandItem().getDamageValue()>0,"Bow consumes durability");
                for(var arrow:level.getEntitiesOfClass(AbstractArrow.class,a.getBoundingBox().inflate(40)))
                    if(target(arrow).hasAttached(GUARD_ARROW_TARGET)) check(arrow.pickup==AbstractArrow.Pickup.DISALLOWED,"Unlimited arrows cannot be collected");
                m.discard();
            });
            c.takeScreenshot("village-friends-guard-equipment");
            reset(w,knightId,archerId,base);
            // Creepers and idle skeletons never qualify, even while villagers are nearby.
            UUID[] excluded=w.getServer().computeOnServer(s -> {
                var level=w.getConnection().getServerLevel(); var k=villager(w,knightId); k.setNoAi(false);
                var creeper=new Creeper(EntityTypes.CREEPER,level); creeper.setPos(base.x+2,base.y,base.z+3); creeper.setNoAi(true); level.addFreshEntity(creeper);
                var skeleton=new Skeleton(EntityTypes.SKELETON,level); skeleton.setPos(base.x+3,base.y,base.z+3); skeleton.setNoAi(true); skeleton.setItemSlot(EquipmentSlot.HEAD,new ItemStack(Items.IRON_HELMET)); level.addFreshEntity(skeleton);
                return new UUID[]{creeper.getUUID(),skeleton.getUUID()};
            }); c.waitTicks(40);
            w.getServer().runOnServer(s -> {
                check(GuardController.combatTarget(villager(w,knightId))==null,"Idle player-hostile mobs ignored");
                var level=w.getConnection().getServerLevel(); var skeleton=(Skeleton)level.getEntity(excluded[1]); skeleton.setTarget(villager(w,babyId));
            }); c.waitTicks(12);
            w.getServer().runOnServer(s -> {
                check(GuardController.combatTarget(villager(w,knightId))==w.getConnection().getServerLevel().getEntity(excluded[1]),"Actual villager threat qualifies outside predator tag");
                for(UUID id:excluded)w.getConnection().getServerLevel().getEntity(id).discard();
            });
            reset(w,knightId,archerId,base);
            // Player attacks alert all nearby guards using the victim's friendship alone.
            w.getServer().runCommand("gamemode survival @a");
            w.getServer().runOnServer(s -> {
                var level=w.getConnection().getServerLevel(); var p=w.getConnection().getServerPlayer(); var victim=villager(w,babyId);
                var k=villager(w,knightId);var a=villager(w,archerId);k.setNoAi(false);a.setNoAi(false);
                saveBond(k,p,BondState.migrated(4)); saveBond(a,p,BondState.migrated(4));
                victim.damageCooldownTime=0; victim.hurtServer(level,victim.damageSources().playerAttack(p),1);
                check(GuardController.angryAt(k,p)&&GuardController.angryAt(a,p),"Friends of responding guards still provoke group when victim is not their friend");
                check(bond(victim,p).has("hurt"),"Attack still damages trust");
                check(!GuardController.canExchange(k,p),"Angry player cannot exchange");
                GuardController.clear(); save(victim,p,new FriendshipState(40,-1,-1,0,"")); saveBond(victim,p,BondState.NEW.flag("shared_experience"));
                victim.damageCooldownTime=0; victim.hurtServer(level,victim.damageSources().playerAttack(p),1);
                check(!GuardController.angryAt(k,p)&&!GuardController.angryAt(a,p),"Victim friendship suppresses the whole alert");
                saveBond(victim,p,BondState.NEW); save(victim,p,FriendshipState.NEW);
                var arrow=new Arrow(level,p,new ItemStack(Items.ARROW),null);
                victim.damageCooldownTime=0;check(victim.hurtServer(level,victim.damageSources().arrow(arrow,p),1),"Projectile damage is accepted by Minecraft");
                check(GuardController.angryAt(k,p)&&GuardController.angryAt(a,p),"Player projectile owner attributed correctly");
                var second=new net.minecraft.server.level.ServerPlayer(s,level,new com.mojang.authlib.GameProfile(UUID.randomUUID(),"SecondAggressor"),net.minecraft.server.level.ClientInformation.createDefault());
                second.setPos(p.getX(),p.getY(),p.getZ());victim.damageCooldownTime=0;victim.hurtServer(level,victim.damageSources().playerAttack(second),1);
                check(GuardController.angryAt(k,p)&&GuardController.angryAt(k,second),"Two aggressors have independent anger records");
                GuardController.clear();
                var guardArrow=new Arrow(level,a,new ItemStack(Items.ARROW),a.getMainHandItem());target(guardArrow).setAttached(GUARD_ARROW_TARGET,UUID.randomUUID().toString());
                float hp=victim.getHealth(); victim.setInvulnerableTime(0);victim.hurtServer(level,victim.damageSources().arrow(guardArrow,a),5);
                check(victim.getHealth()==hp,"Guard arrows cannot hurt villagers");
                hp=p.getHealth();p.setInvulnerableTime(0);p.hurtServer(level,p.damageSources().arrow(guardArrow,a),5);check(p.getHealth()==hp,"Guard arrows cannot hurt non-targeted players");
                // Full inventory returns previous gear through one dropped item.
                resetInventory(p);for(int i=0;i<p.getInventory().getContainerSize();i++)p.getInventory().setItem(i,new ItemStack(Items.COBBLESTONE,64));
                p.setItemInHand(InteractionHand.MAIN_HAND,new ItemStack(Items.DIAMOND_HELMET,2));
                var oldHelmet=k.getItemBySlot(EquipmentSlot.HEAD).getItem();k.setNoAi(true);a.setNoAi(true);
                check(GuardController.exchange(p,k),"Full-inventory exchange succeeds");
                check(p.getMainHandItem().getCount()==1,"Exactly one armor piece exchanged");
                check(level.getEntitiesOfClass(net.minecraft.world.entity.item.ItemEntity.class,p.getBoundingBox().inflate(2)).stream().anyMatch(e->e.getItem().is(oldHelmet)),"Previous armor drops when inventory is full");
                // Creative's native inventory insertion would delete overflow; guard exchanges must preserve it.
                p.getAbilities().instabuild=true;p.setItemInHand(InteractionHand.MAIN_HAND,new ItemStack(Items.NETHERITE_CHESTPLATE,2));
                check(GuardController.exchange(p,k)&&p.getMainHandItem().getCount()==1,"Creative full-inventory exchange consumes one physical item");
                check(level.getEntitiesOfClass(net.minecraft.world.entity.item.ItemEntity.class,p.getBoundingBox().inflate(2)).stream().anyMatch(e->e.getItem().is(Items.NETHERITE_CHESTPLATE)),"Creative overflow equipment drops instead of disappearing");
                p.getAbilities().instabuild=false;
                resetInventory(p);
            });
            // Target retention and pursuit boundaries run through the normal brain hook.
            reset(w,knightId,archerId,base);
            w.getServer().runOnServer(s -> {
                var p=w.getConnection().getServerPlayer();p.getAbilities().invulnerable=true;p.teleportTo(base.x,base.y,base.z);
                var k=villager(w,knightId);k.setNoAi(false);saveBond(k,p,BondState.NEW);save(k,p,FriendshipState.NEW);
                k.damageCooldownTime=0;k.hurtServer(w.getConnection().getServerLevel(),k.damageSources().playerAttack(p),1);
            });c.waitTicks(20);
            w.getServer().runOnServer(s -> {
                check(GuardController.combatTarget(villager(w,knightId))==w.getConnection().getServerPlayer(),"Attacked guard retains real player target between scans");
                w.getConnection().getServerPlayer().teleportTo(base.x+35,base.y,base.z);
            });c.waitTicks(12);
            w.getServer().runOnServer(s -> {
                var k=villager(w,knightId);check(GuardController.combatTarget(k)==null,"Player beyond pursuit limit is released");
                check(k.position().distanceToSqr(base.add(0,0,2))<1024,"Guard remains inside pursuit boundary");
                k.setNoAi(true);GuardController.clear();var p=w.getConnection().getServerPlayer();p.getAbilities().invulnerable=false;p.teleportTo(base.x,base.y,base.z);
            });
            // A bystander moving into a fired arrow is protected at the actual impact hook.
            UUID[] bystanderShot=w.getServer().computeOnServer(s -> {
                var level=w.getConnection().getServerLevel();var civilian=spawn(level,base,null,16,6);
                var arrow=new Arrow(level,villager(w,archerId),new ItemStack(Items.ARROW),new ItemStack(Items.BOW));
                arrow.setPos(civilian.getX(),civilian.getEyeY(),civilian.getZ()-3);
                target(arrow).setAttached(GUARD_ARROW_TARGET,UUID.randomUUID().toString());
                arrow.shoot(0,0,1,1.6F,0);level.addFreshEntity(arrow);
                return new UUID[]{civilian.getUUID(),arrow.getUUID()};
            });c.waitTicks(8);
            w.getServer().runOnServer(s -> {
                var level=w.getConnection().getServerLevel();var civilian=villager(w,bystanderShot[0]);
                check(civilian.getHealth()==civilian.getMaxHealth(),"Actual guard projectile impact leaves bystander unharmed");
                check(level.getEntity(bystanderShot[1])==null,"Protected impact discards the arrow");civilian.discard();
            });
            // Recruited guard Wait defends without pursuing, and downing/rescue/home remain intact.
            reset(w,knightId,archerId,base);
            UUID waitingFoe=w.getServer().computeOnServer(s -> {
                var p=w.getConnection().getServerPlayer();var k=villager(w,knightId);
                save(k,p,new FriendshipState(40,-1,-1,0,""));saveBond(k,p,BondState.migrated(2).chapter(2));
                check(CompanionController.handle(p,k,"recruit"),"Guard recruitment uses existing friendship gate");
                CompanionController.handle(p,k,"wait");
                return zombie(w.getConnection().getServerLevel(),base,1,2).getUUID();
            });c.waitTicks(45);
            w.getServer().runOnServer(s -> {
                var level=w.getConnection().getServerLevel();var k=villager(w,knightId);var p=w.getConnection().getServerPlayer();var waitingMob=(Zombie)level.getEntity(waitingFoe);
                check(waitingMob.getHealth()<100,"Wait-mode guard defends at melee reach");
                check(k.position().distanceToSqr(base.add(0,0,2))<1,"Wait-mode guard does not pursue");waitingMob.discard();
                k.damageCooldownTime=0;k.hurtServer(level,k.damageSources().generic(),100);
                check(CompanionController.state(k).downed()&&k.isAlive(),"Guard companion retains downed protection");
                check(CompanionController.handle(p,k,"rescue")&&!CompanionController.state(k).downed(),"Guard companion can be rescued");
                CompanionController.handle(p,k,"home");check(!CompanionController.state(k).active()&&k.isNoAi(),"Home restores original guard AI setting");
            });
            // Native conversion transfers the initialization marker; save/reload keeps upgraded/broken gear.
            curedId=w.getServer().computeOnServer(s -> {
                var k=villager(w,knightId);
                var z=k.convertTo(EntityTypes.ZOMBIE_VILLAGER,ConversionParams.single(k,true,true),e->{});
                check(target(z).getAttachedOrElse(GUARD_EQUIPPED,false),"Conversion transfers initialization marker");
                var cured=z.convertTo(EntityTypes.VILLAGER,ConversionParams.single(z,true,true),e->{});cured.setNoAi(true);
                check(target(cured).getAttachedOrElse(GUARD_EQUIPPED,false),"Cure transfers initialization marker");
                check(cured.getItemBySlot(EquipmentSlot.FEET).isEmpty(),"Cure never regenerates missing gear");
                return cured.getUUID();
            });
            saved=w.getWorldSave();
        }
        final UUID reloadedKnight=curedId;
        try(var w=saved.open()) {
            w.getConnection().waitForChunksDownload();
            w.getServer().runOnServer(s -> {
                var k=villager(w,reloadedKnight);check(k!=null,"Guard saves and reloads");
                check(target(k).getAttachedOrElse(GUARD_EQUIPPED,false),"Initialization marker saved");
                check(k.getItemBySlot(EquipmentSlot.FEET).isEmpty()&&k.getItemBySlot(EquipmentSlot.HEAD).is(Items.DIAMOND_HELMET),"Upgraded and missing equipment survives reload");
                check(!GuardController.fighting(k),"Combat state clears on restart");
            });
        }
        LOGGER.info("GUARD GAMEPLAY PASSED: native job acquisition, gear, upgrades, melee, ranged, armor, targeting, retaliation, forgiveness, projectiles, conversion and reload.");
    }
    private static void resetInventory(net.minecraft.server.level.ServerPlayer p) {p.getInventory().clearContent();}
    private static long levelTime(Villager v) {return v.level().getGameTime();}
}
