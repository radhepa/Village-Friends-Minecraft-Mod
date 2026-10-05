package dev.villagefriends;

import com.mojang.blaze3d.platform.NativeImage;
import dev.villagefriends.client.*;
import dev.villagefriends.outfit.*;
import java.util.*;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.minecraft.client.renderer.texture.DynamicTexture;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.Pose;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;

@SuppressWarnings("UnstableApiUsage")
public final class HairFaceGameTest implements FabricClientGameTest {
    private static void check(boolean ok,String message) { if (!ok) throw new AssertionError(message); }
    private static void near(float actual,float expected,String message) { check(Math.abs(actual-expected)<.0001F,message); }
    private static long seed(int hair,int color) {
        for (long seed=0;seed<20000;seed++) {
            var outfit=OutfitFactory.assembleOutfit(Gender.MALE,Profession.NONE,PaletteID.WASHED_INDIGO_AND_CREAM,seed);
            if (outfit.hair().id().equals("m_hair_0"+hair) && outfit.hairRgb()==color) return seed;
        }
        throw new AssertionError("Head preview seed unavailable");
    }
    private static void gallery(ClientGameTestContext c,List<Integer> ids,int frame,String screenshot) {
        c.runOnClient(client->client.gui.setScreen(new HairFacePreviewScreen(ids.stream().map(id->(Villager)client.level.getEntity(id)).toList(),frame)));
        c.waitForScreen(HairFacePreviewScreen.class);c.waitTicks(2);c.takeScreenshot(screenshot);
    }
    @Override public void runTest(ClientGameTestContext c) {
        c.getInput().resizeWindow(1800,1200);
        c.runOnClient(client->{client.options.pauseOnLostFocus=false;client.options.guiScale().set(2);client.resizeGui();});
        try (var world=c.worldBuilder().create()) {
            world.getConnection().waitForChunksRender();world.getServer().runCommand("time set day");
            var colors=List.of(0x594134,0x8A8580,0x342A26,0x846344,0x3B3737);
            var seeds=new ArrayList<Long>();for (int i=0;i<5;i++) seeds.add(seed(i+1,colors.get(i)));
            var ids=world.getServer().computeOnServer(server->{
                var list=new ArrayList<Integer>();var player=world.getConnection().getServerPlayer();
                for (int i=0;i<5;i++) {
                    var resident=new Villager(EntityTypes.VILLAGER,player.level());resident.setNoAi(true);resident.setAge(0);
                    resident.setPos(player.getX()+(i-2)*2,player.getY(),player.getZ()+5);resident.setYRot(180);resident.yBodyRot=resident.yHeadRot=180;
                    String recipe=new ResidentLook(i,Gender.MALE,PaletteID.WASHED_INDIGO_AND_CREAM,seeds.get(i)).recipe();
                    VillageFriends.target(resident).setAttached(VillageFriends.PROFILE,ResidentProfile.generate(resident.getUUID(),recipe));
                    world.getConnection().getServerLevel().addFreshEntity(resident);list.add(resident.getId());
                }
                return list;
            });
            world.getConnection().waitForClientboundEntityUpdates(EntityTypes.VILLAGER);c.waitTicks(10);
            c.runOnClient(client->{
                var model=new ResidentModel(false);
                for (int n=0;n<5;n++) {
                    var resident=(Villager)client.level.getEntity(ids.get(n));var renderer=(ResidentRenderer)client.getEntityRenderDispatcher().getRenderer(resident);
                    var state=renderer.createRenderState(resident,1);check(state.outfit.hair().id().equals("m_hair_0"+(n+1)),"Each requested hair rendered");
                    for (int skin=0;skin<6;skin++) {
                        String recipe=new ResidentLook(skin,Gender.MALE,PaletteID.WASHED_INDIGO_AND_CREAM,seeds.get(n)).recipe();
                        var texture=ResidentSkins.texture(recipe,"none");var baked=((DynamicTexture)client.getTextureManager().getTexture(texture)).getPixels();
                        try (var stream=client.getResourceManager().getResourceOrThrow(Identifier.fromNamespaceAndPath("villagefriends","textures/body/"+skin+".png")).open();
                             var base=NativeImage.read(stream)) {
                            for (int x=8;x<16;x++) check(baked.getPixel(x,12)==base.getPixel(x,12),"Living Eyes row untouched, skin "+skin);
                            check(baked.getPixel(11,14)==base.getPixel(11,14),"Blink crease UV untouched");
                            check(baked.getPixel(FaceDetails.BROW_U,0)==FaceDetails.brow(state.outfit.hairRgb()),"Brows 20% darker than selected hair");
                            check(baked.getPixel(FaceDetails.LASH_U,0)==FaceDetails.lash(state.outfit.hairRgb()),"Dark lash swatch");
                            check(baked.getPixel(FaceDetails.SOCKET_U,0)==FaceDetails.shadow(base.getPixel(12,12)),"Eye socket 10% skin shade");
                            check(baked.getPixel(FaceDetails.CHIN_U,0)==FaceDetails.shadow(base.getPixel(12,15)),"Chin 10% skin shade");
                        } catch (Exception e) { throw new AssertionError(e); }
                    }
                    state.attention=1;state.eyeLookX=.28F;state.eyeLookY=.12F;state.pose=Pose.STANDING;state.deathTime=0;
                    for (float age=0;age<200;age+=.25F) {
                        state.ageInTicks=age;model.setupAnim(state);
                        for (int eye=0;eye<2;eye++) {
                            var root=model.head.getChild("eye"+eye);var iris=root.getChild("iris");var lid=root.getChild("lid");
                            float center=eye==0?-2:2;
                            check(iris.x-.45F>=center-1.0001F && iris.x+.45F<=center+1.0001F,"Gaze stays in eye width");
                            check(iris.y-.5F*iris.yScale>=-4.0001F && iris.y+.5F*iris.yScale<=-2.9999F,"Gaze stays in eye height");
                            check(lid.yScale>=0 && lid.yScale<=.5F,"Original blink closure retained");
                            near(root.getChild("lash").y,FaceDetails.LASH_Y+ResidentMotion.blink(age,state.motionSeed)*.5F,"Lashes follow upper lid");
                            near(model.head.getChild("brow"+eye).yScale,1,"One-pixel eyebrow thickness");
                        }
                    }
                    state.pose=Pose.SLEEPING;model.setupAnim(state);near(model.head.getChild("eye0").getChild("lid").yScale,.5F,"Sleeping eyes close");
                    state.pose=Pose.STANDING;state.deathTime=1;model.setupAnim(state);near(model.head.getChild("eye1").getChild("lowerLid").yScale,.5F,"Death pose closes eyes");
                    state.deathTime=0;model.setupAnim(state);long before=model.head.getAllParts().stream().filter(p->p.visible).count();
                    state.headEquipment=new ItemStack(Items.IRON_HELMET);model.setupAnim(state);
                    check(before-model.head.getAllParts().stream().filter(p->p.visible).count()==state.outfit.hair().voxels().size(),"Helmet hides all outer hair cubes");
                    state.headEquipment=ItemStack.EMPTY;state.isBaby=true;new ResidentModel(true).setupAnim(state);
                }
            });
            gallery(c,ids,-1,"village-friends-five-handcrafted-heads-eye-states");
            c.getInput().resizeWindow(1800,720);c.runOnClient(client->client.resizeGui());
            for (int frame=0;frame<12;frame++) gallery(c,ids,frame,"handcrafted-heads-frame-"+String.format(Locale.ROOT,"%02d",frame));
            c.runOnClient(client->client.gui.setScreen(null));
            var reload=c.computeOnClient(client->client.reloadResourcePacks());c.waitFor(client->reload.isDone(),600);reload.join();
            c.runOnClient(client->{var resident=(Villager)client.level.getEntity(ids.getFirst());var renderer=(ResidentRenderer)client.getEntityRenderDispatcher().getRenderer(resident);
                check(renderer.createRenderState(resident,1).texture.getPath().startsWith("generated/"),"Face details reload");});
            c.waitTicks(10);VillageFriends.LOGGER.info("HANDCRAFTED HEAD CHECKS PASSED: 5 styles, 6 complexions, protected eye UVs, lashes/brows, blink/gaze/sleep/helmet/baby/reload.");
        }
        VillageFriends.LOGGER.info("HANDCRAFTED HAIR AND LIVING EYES GAMEPLAY PASSED.");
    }
}
