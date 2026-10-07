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
    private static void near(float actual,float expected,String message) { check(Math.abs(actual-expected)<.0001F,message+": "+actual+" vs "+expected); }
    private static Outfit outfit(int hair) {
        var t=Wardrobe.OUTFITS.getFirst();
        return new Outfit(hair%2==0?Gender.MALE:Gender.FEMALE,Profession.NONE,MasterPalettes.get(PaletteID.WASHED_INDIGO_AND_CREAM),Wardrobe.HAIR.get(hair),
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
                            int hair=outfit.hairColor().base(),face=base.getPixel(12,12),iris=base.getPixel(10,12);
                            check(baked.getPixel(FaceDetails.BROW_U,0)==FaceDetails.brow(hair),"Brows 20% darker than selected hair");
                            check(baked.getPixel(FaceDetails.LASH_U,0)==FaceDetails.lash(hair),"Dark lash swatch");
                            check(baked.getPixel(FaceDetails.SHADOW_U,0)==FaceDetails.shadow(face),"Neck 10% skin shade");
                            check(baked.getPixel(FaceDetails.TINT_U,0)==FaceDetails.tint(iris,base.getPixel(9,12)),"Starlit upper white tinted by the resident's iris");
                            check(baked.getPixel(FaceDetails.PUPIL_U,0)==FaceDetails.pupil(iris),"Pupil from the resident's iris");
                            check(baked.getPixel(FaceDetails.LIP_U,0)==FaceDetails.lip(face) && baked.getPixel(FaceDetails.ROSE_LIP_U,0)==FaceDetails.roseLip(face),"Lips from the complexion");
                            check(baked.getPixel(FaceDetails.BLUSH_U,0)==FaceDetails.blush(face),"Blush from the complexion");
                        } catch (Exception e) { throw new AssertionError(e); }
                    }
                    ResidentSkins.clear(); // six atlases per style; release them before the next of many styles
                    state.attention=1;state.eyeLookX=n%3==0?-.28F:.28F;state.eyeLookY=.12F;state.pose=Pose.STANDING;state.deathTime=0;state.motionSeed=n*7919;
                    for (var layer:state.layers) layer.clear(); // clips close eyes too; AnimationPackGameTest covers them
                    var style=FaceDetails.eyeStyle(state.motionSeed);boolean starlit=style==FaceDetails.EyeStyle.STARLIT;
                    boolean feminine=FaceDetails.feminine(outfit.gender(),state.motionSeed);float top=FaceDetails.eyeTop(style);
                    for (float age=0;age<200;age+=.25F) {
                        state.ageInTicks=age;model.setupAnim(state);float blink=ResidentMotion.blink(age,state.motionSeed);
                        for (int eye=0;eye<2;eye++) {
                            var root=model.head.getChild("eye"+eye);var lid=root.getChild("lid");var lash=root.getChild("lash");
                            float left=eye==0?-3:1,right=eye==0?-1:3;
                            for (var name:List.of("pupil","iris")) {
                                var part=root.getChild(name);if(!part.visible) continue;
                                check(part.x-part.xScale/2>=left-.0001F && part.x+part.xScale/2<=right+.0001F,"Gaze stays in eye width");
                                check(part.y-part.yScale/2>=top-.0001F && part.y+part.yScale/2<=FaceDetails.EYE_BOTTOM+.0001F,"Gaze stays in eye height");
                            }
                            check(root.getChild("iris").visible,"The iris always shows");
                            check(root.getChild("sclera").visible==starlit,"Only Starlit eyes have the tinted upper white");
                            check(root.getChild("wing").visible==feminine,"Feminine faces wear the lash wing");
                            near(lash.y+lash.yScale/2,FaceDetails.lashBottom(style,blink),"Lashes sweep down with the blink");
                            check(!lid.visible || Math.abs(lid.y-lid.yScale/2-(top-1))<.0001F,"The lid starts at the resting lash line");
                            near(model.head.getChild("brow"+eye).yScale,feminine?.45F:.55F,"Fine brows");
                            check(model.head.getChild("blush"+eye).visible==feminine,"Blush on feminine faces");
                        }
                        check(model.head.getChild("lips").visible==feminine && model.head.getChild("mouth").visible!=feminine,"One mouth per face");
                    }
                    state.pose=Pose.SLEEPING;model.setupAnim(state);
                    var shut=model.head.getChild("eye0").getChild("lash");near(shut.y+shut.yScale/2,FaceDetails.EYE_BOTTOM,"Sleeping eyes close");
                    check(model.head.getChild("eye0").getChild("lid").visible,"Sleeping lids cover the eyes");
                    state.pose=Pose.STANDING;state.deathTime=1;model.setupAnim(state);
                    shut=model.head.getChild("eye1").getChild("lash");near(shut.y+shut.yScale/2,FaceDetails.EYE_BOTTOM,"Death pose closes eyes");
                    state.deathTime=0;model.setupAnim(state);
                    long hairParts=WardrobeLayer.shown(state).stream().filter(s->s.garment()==outfit.hair()).count();
                    check(hairParts==outfit.hair().pieces().size(),"Every hair piece shows bareheaded");
                    state.headEquipment=new ItemStack(Items.IRON_HELMET);model.setupAnim(state);
                    check(WardrobeLayer.shown(state).stream().noneMatch(s->s.garment()==outfit.hair()),"Helmet hides every hair piece");
                    check(!model.hat.visible,"Helmet hides the hair layer");
                    state.headEquipment=ItemStack.EMPTY;state.isBaby=true;new ResidentModel(true).setupAnim(state);
                }
            });
            c.waitTicks(10);VillageFriends.LOGGER.info("HAIR CHECKS PASSED: {} styles, 6 complexions, protected eye UVs, Starlit and Soft Glint eyes, lashes/brows/lips/blush, blink/gaze/sleep/helmet/baby.",Wardrobe.HAIR.size());
        }
        VillageFriends.LOGGER.info("HAIR AND LIVING EYES GAMEPLAY PASSED.");
    }
}
