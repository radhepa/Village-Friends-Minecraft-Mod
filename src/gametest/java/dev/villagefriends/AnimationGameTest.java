package dev.villagefriends;

import static dev.villagefriends.VillageFriends.*;
import dev.villagefriends.client.*;
import java.util.*;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.*;
import net.fabricmc.fabric.api.client.gametest.v1.world.TestWorldSave;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.world.entity.*;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.item.*;
import net.minecraft.world.phys.EntityHitResult;
import net.minecraft.world.InteractionHand;

@SuppressWarnings("UnstableApiUsage")
public final class AnimationGameTest implements FabricClientGameTest {
    private static void check(boolean ok,String reason){if(!ok)throw new AssertionError(reason);}
    private static void near(float a,float b,String reason){check(Math.abs(a-b)<.00001F,reason+": "+a+" / "+b);}
    private static UUID spawn(TestSingleplayerContext w,UUID id,String look,boolean baby,int index) {
        var p=w.getConnection().getServerPlayer();var v=new Villager(EntityTypes.VILLAGER,p.level());
        v.setUUID(id);v.setPos(p.getX()+(index%4-1.5)*2,p.getY(),p.getZ()+4+index/4*2);
        v.setNoAi(true);v.setAge(baby?-24000:0);v.setYRot(180);v.yBodyRot=v.yHeadRot=180;
        target(v).setAttached(PROFILE,ResidentProfile.generate(id,look));w.getConnection().getServerLevel().addFreshEntity(v);return id;
    }
    private static Villager resident(TestSingleplayerContext w,UUID id){return (Villager)w.getConnection().getServerLevel().getEntity(id);}
    private static List<Integer> entityIds(TestSingleplayerContext w,List<UUID> ids){return w.getServer().computeOnServer(s->ids.stream().map(id->resident(w,id).getId()).toList());}
    private static void gallery(ClientGameTestContext c,List<Integer> ids,boolean faces,float sample,String screenshot) {
        c.runOnClient(client->client.gui.setScreen(new AnimationPreviewScreen(ids.stream().map(id->(Villager)client.level.getEntity(id)).toList(),faces,sample)));
        c.waitForScreen(AnimationPreviewScreen.class);c.waitTicks(5);c.takeScreenshot(screenshot);
        c.runOnClient(client->client.gui.setScreen(null));
    }
    @Override public void runTest(ClientGameTestContext c) {
        c.getInput().resizeWindow(1600,1120);c.runOnClient(client->{client.options.guiScale().set(2);client.resizeGui();});
        var walkers=new ArrayList<UUID>();var faces=new ArrayList<UUID>();var random=new Random(218671);TestWorldSave saved;
        try(var w=c.worldBuilder().create()) {
            w.getConnection().waitForChunksRender();w.getServer().runCommand("time set day");w.getServer().runCommand("gamemode creative @a");
            for(var gait:ResidentMotion.Gait.values()) {
                UUID id;do{id=new UUID(random.nextLong(),random.nextLong());}while(ResidentMotion.gait(ResidentMotion.seed(id))!=gait);
                final UUID chosen=id;int index=walkers.size();
                String look=ResidentAppearance.generate(chosen);
                walkers.add(w.getServer().computeOnServer(s->spawn(w,chosen,look,false,index)));
            }
            for(int n=0;n<8;n++) {
                final int index=n;UUID id=new UUID(random.nextLong(),random.nextLong());
                String look=ResidentAppearance.generate(id);
                faces.add(w.getServer().computeOnServer(s->spawn(w,id,look,index==5,index+8)));
            }
            w.getConnection().waitForClientboundEntityUpdates(EntityTypes.VILLAGER);c.waitTicks(10);
            var walkerIds=entityIds(w,walkers);var faceIds=entityIds(w,faces);
            c.runOnClient(client->{
                var poses=new HashSet<String>();
                for(int entity:walkerIds) {
                    var v=(Villager)client.level.getEntity(entity);var renderer=(ResidentRenderer)client.getEntityRenderDispatcher().getRenderer(v);
                    var s=renderer.createRenderState(v,1);check(s.motionSeed==ResidentMotion.seed(v.getUUID()),"Actual entity supplies a stable motion seed");
                    var model=new ResidentModel(false);var armor=new ResidentArmorModel(ResidentModel.layer(false).bakeRoot());
                    s.onGround=true;s.pose=Pose.STANDING;s.walkAnimationPos=2.7F;s.walkAnimationSpeed=.55F;s.ageInTicks=38;
                    model.setupAnim(s);armor.setupAnim(s);
                    poses.add(model.leftLeg.xRot+":"+model.rightArm.xRot+":"+model.root().y);
                    near(model.leftLeg.xRot,armor.leftLeg.xRot,"Armor follows stride");near(model.root().y,armor.root().y,"Armor follows bob");near(model.root().zRot,armor.root().zRot,"Armor follows balance");
                    float first=model.head.zRot;model.setupAnim(s);near(first,model.head.zRot,"Repeated samples never accumulate motion");
                    s.walkAnimationSpeed=0;s.walkAnimationPos=0;model.setupAnim(s);near(model.leftLeg.xRot,0,"Feet settle when idle");near(model.root().y,0,"Idle doesn't hop in place");
                    s.walkAnimationSpeed=.6F;s.rightArmPose=HumanoidModel.ArmPose.ITEM;model.setupAnim(s);
                    var vanilla=new HumanoidModel<ResidentRenderState>(ResidentModel.layer(false).bakeRoot());vanilla.setupAnim(s);near(model.rightArm.xRot,vanilla.rightArm.xRot,"Carried-item pose stays intact");
                    s.rightArmPose=HumanoidModel.ArmPose.EMPTY;
                    for(int mode=0;mode<7;mode++) {
                        s.onGround=mode!=0;s.isPassenger=mode==1;s.isInWater=mode==2;s.isCrouching=mode==3;s.isUsingItem=mode==4;s.pose=mode==5?Pose.SLEEPING:Pose.STANDING;s.deathTime=mode==6?1:0;
                        model.setupAnim(s);vanilla.setupAnim(s);near(model.rightLeg.xRot,vanilla.rightLeg.xRot,"Special poses retain vanilla legs");near(model.root().y,vanilla.root().y,"Special poses don't bob");
                    }
                }
                check(poses.size()==6,"Six actual residents have visibly different walking poses");
                var model=new ResidentModel(false);var s=new ResidentRenderState();s.motionSeed=5131;s.onGround=true;s.pose=Pose.STANDING;
                for(float age=0;age<300;age+=.2F) {
                    s.ageInTicks=age;s.eyeLookX=.28F;s.eyeLookY=.12F;model.setupAnim(s);
                    for(int i=0;i<2;i++) {
                        var eye=model.head.getChild("eye"+i);var iris=eye.getChild("iris");var lid=eye.getChild("lid");
                        float center=i==0?-2:2;
                        check(iris.x-.45F>=center-1.0001F && iris.x+.45F<=center+1.0001F,"Pupils stay inside the eye white");
                        check(iris.y-.5F*iris.yScale>=-4.0001F && iris.y+.5F*iris.yScale<=-2.9999F,"Eyes remain within the pixel-art eye line");
                        check(lid.yScale>=0 && lid.yScale<=1,"Blink stays within face");
                    }
                }
                s.pose=Pose.SLEEPING;model.setupAnim(s);near(model.head.getChild("eye0").getChild("lid").yScale,.5F,"Sleeping upper eyelid closes");near(model.head.getChild("eye0").getChild("lowerLid").yScale,.5F,"Sleeping lower eyelid closes");
                s.pose=Pose.STANDING;s.headEquipment=new ItemStack(Items.IRON_HELMET);model.setupAnim(s);
                s.isBaby=true;s.headEquipment=ItemStack.EMPTY;new ResidentModel(true).setupAnim(s);
                var before=ResidentSkins.cachedCount();for(int n=0;n<100;n++){s.ageInTicks=n;model.setupAnim(s);}check(before==ResidentSkins.cachedCount(),"No per-frame skin allocation");
            });
            gallery(c,walkerIds,false,18,"village-friends-walking-contact");
            gallery(c,walkerIds,false,22,"village-friends-walking-passing");
            gallery(c,faceIds,true,38,"village-friends-living-eyes");
            // A live walk uses real server movement and the synced vanilla walk cycle.
            UUID moving=walkers.getFirst();
            w.getServer().runOnServer(s->{var v=resident(w,moving);var p=w.getConnection().getServerPlayer();v.setPos(p.getX()+2,p.getY(),p.getZ()+3);v.setNoAi(false);v.getNavigation().moveTo(p.getX()-3,p.getY(),p.getZ()+3,.7);});
            c.waitTicks(12);w.getConnection().waitForClientboundEntityUpdates(EntityTypes.VILLAGER);
            c.runOnClient(client->{var v=(Villager)client.level.getEntity(walkerIds.getFirst());var renderer=(ResidentRenderer)client.getEntityRenderDispatcher().getRenderer(v);var s=renderer.createRenderState(v,1);check(s.walkAnimationSpeed>0 && s.walkAnimationPos>0,"Actual pathfinding drives the expressive walk");});
            c.getInput().lookAt(0,8);c.takeScreenshot("village-friends-living-village");
            w.getServer().runOnServer(s->{var v=resident(w,moving);var p=w.getConnection().getServerPlayer();v.setNoAi(true);v.setPos(p.getX(),p.getY(),p.getZ()+2);v.setYRot(180);v.yBodyRot=v.yHeadRot=180;});
            c.waitTicks(5);w.getConnection().waitForClientboundEntityUpdates(EntityTypes.VILLAGER);
            int entity=walkerIds.getFirst();
            c.runOnClient(client->{var v=(Villager)client.level.getEntity(entity);client.gameMode.interact(client.player,v,new EntityHitResult(v),InteractionHand.MAIN_HAND);});
            c.waitForScreen(FriendshipScreen.class);c.waitTicks(5);c.takeScreenshot("village-friends-expressive-portrait");c.clickScreenButton("Goodbye");
            saved=w.getWorldSave();
        }
        try(var w=saved.open()) {
            w.getConnection().waitForChunksDownload();
            for(UUID id:walkers)w.getServer().runOnServer(s->check(resident(w,id)!=null && ResidentMotion.seed(resident(w,id).getUUID())==ResidentMotion.seed(id),"Resident gait identity survives reload"));
            w.getConnection().waitForClientboundEntityUpdates(EntityTypes.VILLAGER);
            var reload=c.computeOnClient(client->client.reloadResourcePacks());c.waitFor(client->reload.isDone(),600);reload.join();c.waitTicks(5);
            var ids=entityIds(w,walkers);gallery(c,ids,false,18,"village-friends-walks-after-reload");
        }
        LOGGER.info("ANIMATION GAMEPLAY PASSED: six stable walks, natural blinking/glances, bounded pixel-art eyes, child/helmet compatibility, matching armor poses, real navigation, live portrait, deterministic samples, resource and world reload.");
    }
}

