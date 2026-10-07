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

/** Every hairstyle on every complexion keeps the Living Eyes UVs intact and animates eyes correctly. */
@SuppressWarnings("UnstableApiUsage")
public final class HairFaceGameTest implements FabricClientGameTest {
    private static void check(boolean ok,String message) { if (!ok) throw new AssertionError(message); }
    private static void near(float actual,float expected,String message) { check(Math.abs(actual-expected)<.0001F,message); }
    private static Outfit outfit(int hair) {
        var t=Wardrobe.OUTFITS.getFirst();
        return new Outfit(Gender.MALE,Profession.NONE,MasterPalettes.get(PaletteID.WASHED_INDIGO_AND_CREAM),Wardrobe.HAIR.get(hair),
            Wardrobe.HAIR_COLORS.get(hair%Wardrobe.HAIR_COLORS.size()),t.top(),t.bottom(),t);
    }
    @Override public void runTest(ClientGameTestContext c) {
        c.getInput().resizeWindow(1800,1200);
        c.runOnClient(client->{client.options.pauseOnLostFocus=false;client.options.guiScale().set(2);client.resizeGui();});
        try (var world=c.worldBuilder().create()) {
            world.getConnection().waitForChunksRender();world.getServer().runCommand("time set day");
            int id=world.getServer().computeOnServer(server->{
                var player=world.getConnection().getServerPlayer();
                var resident=new Villager(EntityTypes.VILLAGER,player.level());resident.setNoAi(true);resident.setAge(0);
                resident.setPos(player.getX(),player.getY(),player.getZ()+5);resident.setYRot(180);resident.yBodyRot=resident.yHeadRot=180;
                world.getConnection().getServerLevel().addFreshEntity(resident);return resident.getId();
            });
            world.getConnection().waitForClientboundEntityUpdates(EntityTypes.VILLAGER);c.waitTicks(10);
            c.runOnClient(client->{
                var model=new ResidentModel(false);
                var resident=(Villager)client.level.getEntity(id);var renderer=(ResidentRenderer)client.getEntityRenderDispatcher().getRenderer(resident);
                for (int n=0;n<Wardrobe.HAIR.size();n++) {
                    var outfit=outfit(n);var state=renderer.createRenderState(resident,1);state.outfit=outfit;
                    for (int skin=0;skin<6;skin++) {
                        var baked=((DynamicTexture)client.getTextureManager().getTexture(ResidentSkins.texture(outfit,skin))).getPixels();
                        try (var stream=client.getResourceManager().getResourceOrThrow(Identifier.fromNamespaceAndPath("villagefriends","textures/body/"+skin+".png")).open();
                             var base=NativeImage.read(stream)) {
                            for (int x=8;x<16;x++) check(baked.getPixel(x,12)==base.getPixel(x,12),"Living Eyes row untouched, skin "+skin+" "+outfit.hair().id());
                            check(baked.getPixel(11,14)==base.getPixel(11,14),"Blink crease UV untouched");
                            int hair=outfit.hairColor().base();
                            check(baked.getPixel(FaceDetails.BROW_U,0)==FaceDetails.brow(hair),"Brows 20% darker than selected hair");
                            check(baked.getPixel(FaceDetails.LASH_U,0)==FaceDetails.lash(hair),"Dark lash swatch");
                            check(baked.getPixel(FaceDetails.SOCKET_U,0)==FaceDetails.shadow(base.getPixel(12,12)),"Eye socket 10% skin shade");
                            check(baked.getPixel(FaceDetails.CHIN_U,0)==FaceDetails.shadow(base.getPixel(12,15)),"Chin 10% skin shade");
                        } catch (Exception e) { throw new AssertionError(e); }
                    }
                    ResidentSkins.clear(); // six atlases per style; release them before the next of many styles
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
                    state.deathTime=0;model.setupAnim(state);
                    long hairParts=WardrobeLayer.shown(state).stream().filter(s->s.garment()==outfit.hair()).count();
                    check(hairParts==outfit.hair().pieces().size(),"Every hair piece shows bareheaded");
                    state.headEquipment=new ItemStack(Items.IRON_HELMET);model.setupAnim(state);
                    check(WardrobeLayer.shown(state).stream().noneMatch(s->s.garment()==outfit.hair()),"Helmet hides every hair piece");
                    check(!model.hat.visible,"Helmet hides the hair layer");
                    state.headEquipment=ItemStack.EMPTY;state.isBaby=true;new ResidentModel(true).setupAnim(state);
                }
            });
            c.waitTicks(10);VillageFriends.LOGGER.info("HAIR CHECKS PASSED: {} styles, 6 complexions, protected eye UVs, lashes/brows, blink/gaze/sleep/helmet/baby.",Wardrobe.HAIR.size());
        }
        VillageFriends.LOGGER.info("HAIR AND LIVING EYES GAMEPLAY PASSED.");
    }
}
