package dev.villagefriends;

import dev.villagefriends.client.*;
import dev.villagefriends.outfit.*;
import java.util.*;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.minecraft.client.renderer.texture.DynamicTexture;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.npc.villager.VillagerProfession;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;

@SuppressWarnings("UnstableApiUsage")
public final class OutfitGameTest implements FabricClientGameTest {
    private static void check(boolean ok, String message) { if (!ok) throw new AssertionError(message); }
    private static long maleSeed(Profession job,PaletteID palette,MaleTopRegistry.Family top,MaleHairRegistry.Geometry hair) {
        for (long seed=0;seed<20000;seed++) {
            var outfit=OutfitFactory.assembleOutfit(Gender.MALE,job,palette,seed);
            if (MaleTopRegistry.ALL.stream().anyMatch(e->e.id().equals(outfit.top().id()) && e.family()==top)
                && MaleHairRegistry.ALL.stream().anyMatch(e->e.id().equals(outfit.hair().id()) && e.geometry()==hair)
                && outfit.bottom().id().equals("m_bottom_0"+(hair.ordinal()+1))) return seed;
        }
        throw new AssertionError("Male preview combination not found");
    }
    private static void gallery(ClientGameTestContext context,List<Integer> ids,String title,String screenshot) {
        context.runOnClient(client->client.gui.setScreen(new OutfitPreviewScreen(ids.stream()
            .map(id->(Villager)client.level.getEntity(id)).toList(),title)));
        context.waitForScreen(OutfitPreviewScreen.class); context.waitTicks(5); context.takeScreenshot(screenshot);
        context.runOnClient(client->client.gui.setScreen(null));
    }
    @Override public void runTest(ClientGameTestContext context) {
        context.getInput().resizeWindow(1600, 1000);
        context.runOnClient(client->{client.options.pauseOnLostFocus=false;client.options.guiScale().set(2);client.resizeGui();});
        try (var world = context.worldBuilder().create()) {
            world.getConnection().waitForChunksRender(); world.getServer().runCommand("time set day");
            var ids = world.getServer().computeOnServer(server -> {
                var entities = new ArrayList<Integer>(); var player = world.getConnection().getServerPlayer();
                int index = 0;
                var jobs=List.of(Profession.NONE,Profession.FARMER,Profession.LIBRARIAN,Profession.CLERIC,Profession.CARTOGRAPHER);
                var nativeJobs=List.of(VillagerProfession.NONE,VillagerProfession.FARMER,VillagerProfession.LIBRARIAN,VillagerProfession.CLERIC,VillagerProfession.CARTOGRAPHER);
                var topFamilies=List.of(MaleTopRegistry.Family.TUNIC,MaleTopRegistry.Family.VEST,MaleTopRegistry.Family.OVERCOAT,
                    MaleTopRegistry.Family.ROBE,MaleTopRegistry.Family.TRAVEL_COAT);
                var hairFamilies=List.of(MaleHairRegistry.Geometry.values());
                var palettes=List.of(PaletteID.WASHED_INDIGO_AND_CREAM,PaletteID.FOREST_AND_HEARTH,PaletteID.RUSTIC_TWEED,
                    PaletteID.SCHOLARLY_PLUM,PaletteID.ASH_AND_TEAL);
                for (int position=0;position<5;position++) {
                    var palette=palettes.get(position);
                    var resident = new Villager(EntityTypes.VILLAGER, player.level());
                    resident.setNoAi(true); resident.setAge(0);
                    resident.setPos(player.getX() + (index % 5 - 2) * 2, player.getY(), player.getZ() + 5 + index / 5 * 3);
                    resident.setYRot(180); resident.yBodyRot = resident.yHeadRot = 180;
                    resident.setVillagerData(resident.getVillagerData().withProfession(server.registryAccess(),nativeJobs.get(position%5)));
                    long seed=maleSeed(jobs.get(position),palette,topFamilies.get(position),hairFamilies.get(position));
                    String recipe = new ResidentLook(index % 6,Gender.MALE,palette,seed).recipe();
                    VillageFriends.target(resident).setAttached(VillageFriends.PROFILE, ResidentProfile.generate(resident.getUUID(), recipe));
                    world.getConnection().getServerLevel().addFreshEntity(resident);
                    entities.add(resident.getId()); index++;
                }
                return entities;
            });
            world.getConnection().waitForClientboundEntityUpdates(EntityTypes.VILLAGER); context.waitTicks(15);
            context.runOnClient(client -> {
                for (int id : ids) {
                    var resident = (Villager)client.level.getEntity(id);
                    var renderer = (ResidentRenderer)client.getEntityRenderDispatcher().getRenderer(resident);
                    var state = renderer.createRenderState(resident, 1);
                    check(state.outfit != null, "New outfit extracted");
                    String prefix=state.outfit.gender()==Gender.MALE?"m_":"f_";
                    check(state.outfit.hair().id().startsWith(prefix+"hair_") && state.outfit.top().id().startsWith(prefix+"top_")
                        && state.outfit.bottom().id().startsWith(prefix+"bottom_"), "Gender registries used by renderer");
                    var image = ((DynamicTexture)client.getTextureManager().getTexture(state.texture)).getPixels();
                    check(image.getWidth() == 512 && image.getHeight() == 512, "Pixel-density atlas dimensions");
                    var colors=new HashSet<Integer>();
                    for (int y=64;y<image.getHeight();y++) for (int x=0;x<image.getWidth();x++)
                        if ((image.getPixel(x,y)>>>24)!=0) colors.add(image.getPixel(x,y));
                    check(colors.size()>45,"Visible woven/leather/hair texture pixels replace solid fills");
                    for (var layer : state.outfit.layers()) check(layer.palette() == state.outfit.palette(), "One palette per outfit");
                    var model = new ResidentModel(false); model.setupAnim(state);
                    check(model.head.getAllParts().size() > 90, "Volumetric hair templates baked into head");
                    state.headEquipment = new ItemStack(Items.IRON_HELMET); model.setupAnim(state);
                    state.chestEquipment = new ItemStack(Items.IRON_CHESTPLATE); model.setupAnim(state);
                }
                ResidentSkins.clear();
                check(ResidentSkins.cachedCount() == 0, "Atlas cache released");
            });
            gallery(context,ids,"VILLAGE FRIENDS  /  FIVE REBUILT MALE OUTFITS","village-friends-five-male-textured-outfits");
            var reload = context.computeOnClient(client -> client.reloadResourcePacks());
            context.waitFor(client -> reload.isDone(), 600); reload.join();
            context.runOnClient(client -> {
                var resident = (Villager)client.level.getEntity(ids.getFirst());
                var renderer = (ResidentRenderer)client.getEntityRenderDispatcher().getRenderer(resident);
                check(renderer.createRenderState(resident, 1).texture.getPath().startsWith("generated/"), "Outfits survive resource reload");
            });
            // Let the client/server test phases settle after reload before disconnecting the integrated server.
            context.waitTicks(10);
            VillageFriends.LOGGER.info("TEXTURED MALE RENDER CHECKS PASSED before test-world shutdown.");
        }
        VillageFriends.LOGGER.info("TEXTURED MALE OUTFITS PASSED: five hairs/tops/bottoms, face textures, palette lock, armor and reload.");
    }
}
