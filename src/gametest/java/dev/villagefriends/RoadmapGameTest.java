package dev.villagefriends;

import static dev.villagefriends.VillageFriends.*;
import com.mojang.authlib.GameProfile;
import dev.villagefriends.client.*;
import java.util.*;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.*;
import net.fabricmc.fabric.api.client.gametest.v1.world.TestWorldSave;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.*;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.*;
import net.minecraft.world.entity.npc.villager.*;
import net.minecraft.world.item.*;
import net.minecraft.world.level.Level;

/** Real client/server packets and rendered screens, with a second server-player fixture for co-op credit. */
@SuppressWarnings("UnstableApiUsage")
public final class RoadmapGameTest implements FabricClientGameTest {
    private static void check(boolean ok, String why) { if (!ok) throw new AssertionError(why); }
    private static Villager resident(TestSingleplayerContext w, UUID id) { return (Villager)w.getConnection().getServerLevel().getEntity(id); }
    private static void flush(TestSingleplayerContext w) { w.getConnection().waitForServerboundPackets(); w.getConnection().waitForClientboundPackets(); }
    private static void click(ClientGameTestContext c, TestSingleplayerContext w, String label) { c.clickScreenButton(label); flush(w); }
    private static void action(ClientGameTestContext c, TestSingleplayerContext w, UUID id, String action) {
        int eid = w.getServer().computeOnServer(s -> resident(w,id).getId());
        c.runOnClient(client -> ClientPlayNetworking.send(new ActionPayload(eid,id,action))); flush(w);
    }
    private static void open(ClientGameTestContext c, TestSingleplayerContext w, UUID id) {
        w.getConnection().waitForClientboundEntityUpdates(EntityTypes.VILLAGER);
        int eid = w.getServer().computeOnServer(s -> resident(w,id).getId());
        c.runOnClient(client -> { client.gui.setScreen(null); var e=client.level.getEntity(eid); client.gameMode.interact(client.player,e,new net.minecraft.world.phys.EntityHitResult(e),InteractionHand.MAIN_HAND); });
        c.waitForScreen(FriendshipScreen.class); flush(w);
    }
    private static void held(TestSingleplayerContext w, Item item, int n) { w.getServer().runOnServer(s -> w.getConnection().getServerPlayer().setItemInHand(InteractionHand.MAIN_HAND,new ItemStack(item,n))); w.getConnection().waitForClientboundPackets(); }
    @Override public void runTest(ClientGameTestContext c) {
        TestWorldSave saved; UUID id, legacyId, playerId; String stableId, look;
        var peers = new ArrayList<UUID>();
        try (var w = c.worldBuilder().create()) {
            w.getConnection().waitForChunksRender(); w.getServer().runCommand("gamemode survival @a");
            playerId = w.getServer().computeOnServer(s -> w.getConnection().getServerPlayer().getUUID());
            legacyId = w.getServer().computeOnServer(s -> {
                var p=w.getConnection().getServerPlayer(); var v=new Villager(EntityTypes.VILLAGER,p.level()); v.setPos(p.getX()+4,p.getY(),p.getZ()+2); v.setNoAi(true);
                v.setCustomName(Component.literal("Old Friend")); v.setVillagerData(v.getVillagerData().withProfession(s.registryAccess(),VillagerProfession.FARMER));
                target(v).setAttached(FRIENDSHIPS,FriendshipBook.empty().with(p.getUUID(),new FriendshipState(143,7,8,2,"minecraft:emerald")));
                w.getConnection().getServerLevel().addFreshEntity(v);
                check(dev.villagefriends.outfit.ResidentLook.parse(profile(v).look())!=null,"Resident uses the new outfit recipe");
                check(state(v,p).points()==143 && state(v,p).giftsToday()==2 && bond(v,p).level(state(v,p))==4,"Migration must keep exact progress, daily count, and unlocked tier");
                check(name(v).equals("Old Friend") && profession(v).equals("farmer"),"Migration keeps names and professions/trades"); return v.getUUID();
            });
            id = w.getServer().computeOnServer(s -> {
                var p=w.getConnection().getServerPlayer(); var v=new Villager(EntityTypes.VILLAGER,p.level()); v.setPos(p.getX(),p.getY(),p.getZ()+2); v.setNoAi(true);
                w.getConnection().getServerLevel().addFreshEntity(v); var r=profile(v);
                target(v).setAttached(PROFILE,new ResidentProfile(r.id(),"thoughtful","growing flowers","keeping promises","minecraft:poppy","minecraft:rotten_flesh","garden",r.look()));
                v.setCustomName(Component.literal("Liora Ash"));
                check(bond(v,p).level(state(v,p))==0,"Fresh residents begin without friendship points"); return v.getUUID();
            });
            stableId=w.getServer().computeOnServer(s -> profile(resident(w,id)).id()); look=w.getServer().computeOnServer(s -> profile(resident(w,id)).look());
            open(c,w,id); click(c,w,"Story"); c.takeScreenshot("village-friends-story-introduction"); click(c,w,"You can count on me");
            held(w,Items.WHEAT_SEEDS,6); click(c,w,"Help with your request");
            w.getServer().runOnServer(s -> {
                var v=resident(w,id); var p=w.getConnection().getServerPlayer(); check(p.getMainHandItem().getCount()==3,"Story consumes exactly three seeds");
                check(bond(v,p).chapter()==2 && bond(v,p).has("shared_experience"),"Helping creates trust and experience");
                check(shared(v).outcomes().values().contains(p.getName().getString()),"Physical task keeps contributor credit");
                int points=state(v,p).points(); check(!NarrativeEngine.handle(p,v,"deliver"),"Repeated quest completion rejected"); check(state(v,p).points()==points,"Quest replay cannot reward");
                var friend=new ServerPlayer(s,w.getConnection().getServerLevel(),new GameProfile(UUID.randomUUID(),"CoopFriend"),ClientInformation.createDefault()); friend.setPos(p.getX(),p.getY(),p.getZ());
                friend.setItemInHand(InteractionHand.MAIN_HAND,new ItemStack(Items.WHEAT_SEEDS,3));
                NarrativeEngine.handle(friend,v,"pledge"); NarrativeEngine.handle(friend,v,"deliver");
                check(friend.getMainHandItem().getCount()==3,"Co-op does not demand duplicate world supplies"); check(state(v,friend).points()==0,"Co-op recap cannot steal reward credit");
                check(bond(v,friend).chapter()==2 && !bond(v,friend).has("shared_experience"),"Co-op player needs their own shared experience");
                check(bond(v,p).chapter()==2 && state(v,p).points()==points,"Private relationship stays independent");
                check(!NarrativeEngine.handle(p,v,"encourage"),"Out-of-order story choice rejected");
            });
            // Real visits on separate days, rather than gift grinding.
            for (int day=1;day<=4;day++) {
                w.getServer().runCommand("time set "+(day*24000)); open(c,w,id); action(c,w,id,"chat");
                if(day==2) { action(c,w,id,"share"); w.getServer().runOnServer(s -> check(bond(resident(w,id),w.getConnection().getServerPlayer()).chapter()==3,"Third visit unlocks a personal confession")); }
            }
            action(c,w,id,"story"); click(c,w,"Your hopes matter to me");
            w.getServer().runOnServer(s -> {
                var v=resident(w,id); var p=w.getConnection().getServerPlayer(); var b=bond(v,p);
                check(b.chapter()==4 && b.has("ending:encourage") && b.has("story_gift"),"Ending and reciprocal gift remembered permanently");
                int points=state(v,p).points(); check(!NarrativeEngine.handle(p,v,"encourage"),"Ending cannot issue a second gift"); check(state(v,p).points()==points,"Ending reward cannot replay");
            });
            c.takeScreenshot("village-friends-story-complete"); click(c,w,"Journal"); c.takeScreenshot("village-friends-journal-large");
            c.getInput().resizeWindow(854,480); c.runOnClient(client -> { client.options.guiScale().set(2); client.resizeGui(); }); c.waitTicks(10); c.takeScreenshot("village-friends-journal-compact");
            c.getInput().resizeWindow(1280,800); c.waitTicks(10);
            held(w,Items.ROTTEN_FLESH,3); action(c,w,id,"gift"); w.getServer().runOnServer(s -> check(w.getConnection().getServerPlayer().getMainHandItem().getCount()==3,"Personal disliked gifts remain in inventory"));
            click(c,w,"Travel"); click(c,w,"Travel with me");
            w.getServer().runOnServer(s -> {
                var v=resident(w,id); var p=w.getConnection().getServerPlayer(); check(CompanionController.state(v).owner().equals(p.getUUID().toString()),"Recruitment assigns sole owner");
                check(!v.canTeleport(v.level(),s.getLevel(Level.NETHER)),"Active companions cannot leave Overworld through portals");
                var other=resident(w,legacyId); saveBond(other,p,BondState.migrated(4).chapter(2)); check(!CompanionController.handle(p,other,"recruit"),"One recruited resident per player");
            });
            held(w,Items.IRON_SWORD,1); click(c,w,"Equip held item"); held(w,Items.IRON_HELMET,1); click(c,w,"Equip held item");
            w.getServer().runOnServer(s -> { var v=resident(w,id); check(v.getMainHandItem().is(Items.IRON_SWORD) && v.getItemBySlot(EquipmentSlot.HEAD).is(Items.IRON_HELMET),"Vanilla sword and helmet equipped"); });
            c.takeScreenshot("village-friends-companion-equipment"); click(c,w,"Goodbye");
            double initial=w.getServer().computeOnServer(s -> {var p=w.getConnection().getServerPlayer(); p.teleportTo(p.getX()+10,p.getY(),p.getZ()); return resident(w,id).distanceToSqr(p);});
            c.waitTicks(100); w.getServer().runOnServer(s -> check(resident(w,id).distanceToSqr(w.getConnection().getServerPlayer()) < initial/2,"Companion follows with actual pathfinding"));
            w.getServer().runOnServer(s -> {
                var v=resident(w,id); var p=w.getConnection().getServerPlayer(); v.teleportTo(p.getX(),p.getY(),p.getZ()+1);
                var foe=new net.minecraft.world.entity.monster.zombie.Husk(EntityTypes.HUSK,p.level()); foe.setPos(v.getX()+1,v.getY(),v.getZ()); foe.setNoAi(true); foe.setTarget(p); w.getConnection().getServerLevel().addFreshEntity(foe); peers.add(foe.getUUID());
            });
            c.waitTicks(65); w.getServer().runOnServer(s -> {
                var foe=(LivingEntity)w.getConnection().getServerLevel().getEntity(peers.removeFirst()); check(foe.getHealth()<foe.getMaxHealth(),"Companion attacks hostile attackers"); foe.discard();
                var v=resident(w,id); v.hurtServer(w.getConnection().getServerLevel(),v.damageSources().generic(),100);
                check(v.isAlive() && CompanionController.state(v).downed(),"Lethal hit downs recruited companion without killing");
                check(v.getMainHandItem().is(Items.IRON_SWORD),"Downed companion keeps equipment");
                check(!v.hurtServer(w.getConnection().getServerLevel(),v.damageSources().generic(),100),"Downed resident protected from further harm");
            });
            open(c,w,id); click(c,w,"Travel"); click(c,w,"Help them up"); w.getServer().runOnServer(s -> check(!CompanionController.state(resident(w,id)).downed(),"Rescue restores companion"));
            click(c,w,"Wait here"); w.getServer().runOnServer(s -> check(CompanionController.state(resident(w,id)).mode().equals("wait"),"Wait command persisted"));
            click(c,w,"Return home"); c.waitForScreen(null);
            w.getServer().runOnServer(s -> { var v=resident(w,id); var p=w.getConnection().getServerPlayer(); check(!CompanionController.state(v).active() && v.isNoAi(),"Home command restores original work behavior"); p.teleportTo(v.getX(),v.getY(),v.getZ()-2); });
            open(c,w,id); held(w,Items.BREAD,4); click(c,w,"Time"); click(c,w,"Share a picnic"); click(c,w,"Goodbye"); c.waitTicks(310); open(c,w,id); click(c,w,"Time"); click(c,w,"Finish our outing");
            w.getServer().runOnServer(s -> check(bond(resident(w,id),w.getConnection().getServerPlayer()).has("activity:picnic"),"Picnic remembered after actual time together"));
            int trustBefore=w.getServer().computeOnServer(s -> bond(resident(w,id),w.getConnection().getServerPlayer()).trust());
            for(String kind:List.of("walk","explore")) {
                action(c,w,id,kind); click(c,w,"Goodbye");
                int distance=kind.equals("walk")?12:36;
                w.getServer().runOnServer(s -> {var p=w.getConnection().getServerPlayer();p.teleportTo(p.getX()+distance,p.getY(),p.getZ());});
                c.waitTicks(kind.equals("walk")?310:610); open(c,w,id); action(c,w,id,"finish_activity");
                w.getServer().runOnServer(s -> check(bond(resident(w,id),w.getConnection().getServerPlayer()).has("activity:"+kind),"Completed "+kind+" records its own experience"));
            }
            w.getServer().runOnServer(s -> {
                var p=w.getConnection().getServerPlayer();
                for(int n=0;n<2;n++){var guest=new Villager(EntityTypes.VILLAGER,p.level());guest.setPos(p.getX()+n+1,p.getY(),p.getZ()+2);guest.setNoAi(true);w.getConnection().getServerLevel().addFreshEntity(guest);peers.add(guest.getUUID());}
            });
            held(w,Items.BREAD,2); action(c,w,id,"gathering"); click(c,w,"Goodbye"); c.waitTicks(410); open(c,w,id); action(c,w,id,"finish_activity");
            w.getServer().runOnServer(s -> {var p=w.getConnection().getServerPlayer();check(bond(resident(w,id),p).has("activity:gathering"),"Host remembers village gathering");for(var guestId:peers){var guest=resident(w,guestId);check(bond(guest,p).has("activity:gathering")&&!CompanionController.state(guest).active(),"Guests remember gathering and restore ordinary behavior");}check(bond(resident(w,id),p).trust()==trustBefore,"Repeated same-day activities cannot grind trust");});
            peers.clear();
            action(c,w,id,"request"); held(w,Items.BONE_MEAL,3); click(c,w,"Deliver supplies");
            action(c,w,id,"request"); held(w,Items.POPPY,1); click(c,w,"Deliver supplies");
            w.getServer().runOnServer(s -> check(shared(resident(w,id)).outcomes().size()==3,"All three physical story requests complete exactly once"));
            click(c,w,"Travel"); click(c,w,"Travel with me");
            w.getServer().runOnServer(s -> { var v=resident(w,id); var p=w.getConnection().getServerPlayer(); v.hurtServer(w.getConnection().getServerLevel(),v.damageSources().generic(),100); CompanionController.resetParty(p); check(!CompanionController.state(v).active() && target(p).getAttachedOrElse(PARTY,"").isEmpty(),"Logout/death cleanup clears downed party and restores home"); check(bond(v,p).memories().stream().anyMatch(m -> m.contains("recovered at home")),"Abandoned downing is remembered"); p.teleportTo(v.getX(),v.getY(),v.getZ()-2); });
            open(c,w,id); action(c,w,id,"recruit");
            w.getServer().runOnServer(s -> {var v=resident(w,id);v.setInvulnerableTime(0);v.hurtServer(w.getConnection().getServerLevel(),v.damageSources().generic(),100);});
            click(c,w,"Goodbye"); c.waitTicks(1220);
            w.getServer().runOnServer(s -> {var v=resident(w,id);var p=w.getConnection().getServerPlayer();check(!CompanionController.state(v).active() && v.getHealth()>=10,"Abandoned companion automatically recovers at home after one minute");p.teleportTo(v.getX(),v.getY(),v.getZ()-2);});
            // Conversion and curing use Minecraft's actual conversion mechanism.
            UUID converted=w.getServer().computeOnServer(s -> {
                var v=resident(w,id); var zombie=v.convertTo(EntityTypes.ZOMBIE_VILLAGER,ConversionParams.single(v,true,true),z -> {});
                check(target(zombie).getAttached(PROFILE).id().equals(stableId),"Zombie conversion keeps stable identity");
                var cured=zombie.convertTo(EntityTypes.VILLAGER,ConversionParams.single(zombie,true,true),r -> {}); cured.setNoAi(true);
                check(profile(cured).id().equals(stableId) && profile(cured).look().equals(look),"Cure keeps identity and modular recipe");
                check(name(cured).equals("Liora Ash") && bond(cured,w.getConnection().getServerPlayer()).chapter()==4 && !shared(cured).outcomes().isEmpty(),"Cure keeps name, history, and physical quest outcomes");
                check(cured.getMainHandItem().is(Items.IRON_SWORD),"Equipment transfers through conversion"); return cured.getUUID();
            });
            // Dynamic texture churn, reload, fallback, and a crowded rendered village.
            c.runOnClient(client -> check(ResidentSkins.texture(look).getPath().startsWith("generated/"),"New outfit atlas resolves"));
            c.waitTicks(10); c.runOnClient(client -> check(ResidentSkins.cachedCount()<=256,"Idle skin cache trims to 256"));
            var reload=c.computeOnClient(client -> client.reloadResourcePacks()); c.waitFor(client -> reload.isDone(),600); reload.join();
            c.runOnClient(client -> check(ResidentSkins.texture(look).getPath().startsWith("generated/"),"Skin parts work after resource reload"));
            w.getServer().runCommand("reload");
            w.getServer().runOnServer(s -> {
                var p=w.getConnection().getServerPlayer();
                for(int n=0;n<100;n++) { var v=new Villager(EntityTypes.VILLAGER,p.level()); v.setPos(p.getX()+(n%10-5)*2,p.getY(),p.getZ()+5+(n/10)*2); v.setNoAi(true); v.setYRot(180); v.yBodyRot=v.yHeadRot=180; w.getConnection().getServerLevel().addFreshEntity(v); peers.add(v.getUUID()); }
            });
            c.runOnClient(client -> client.gui.setScreen(null)); w.getConnection().waitForClientboundEntityUpdates(EntityTypes.VILLAGER); c.getInput().lookAt(0,8); c.waitTicks(50); c.takeScreenshot("village-friends-modular-community");
            saved=w.getWorldSave();
            // Track the new entity UUID after curing, while identity itself remains stable.
            peers.addFirst(converted);
        }
        try(var w=saved.open()) {
            w.getConnection().waitForChunksDownload(); w.getServer().runOnServer(s -> {
                var v=resident(w,peers.getFirst()); check(v!=null,"Cured resident saves and reloads");
                check(profile(v).id().equals(stableId) && profile(v).look().equals(look),"Recipe and stable identity survive reload");
                check(target(v).getAttachedOrCreate(BONDS).get(playerId).chapter()==4,"Completed private story survives reload");
                check(v.getMainHandItem().is(Items.IRON_SWORD) && v.getItemBySlot(EquipmentSlot.HEAD).is(Items.IRON_HELMET),"Equipment survives save/reload");
                var old=resident(w,legacyId); check(name(old).equals("Old Friend") && target(old).getAttached(FRIENDSHIPS).get(playerId).points()==143 && target(old).getAttachedOrCreate(BONDS).get(playerId).legacyLevel()==4,"Legacy save still has exact names/progress/tier");
                check(CompanionController.loaded.size()>=100,"Crowded village residents reload");
            });
        }
        LOGGER.info("ROADMAP GAMEPLAY PASSED: migration, authored story, private co-op bonds/shared credit, gifts, companion follow/defense/equipment/rescue/home/logout, conversion/cure, 2000 textures/cache/reload, 100 residents, save/reload.");
    }
}

