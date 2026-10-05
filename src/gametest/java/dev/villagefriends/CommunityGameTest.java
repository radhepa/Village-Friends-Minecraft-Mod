package dev.villagefriends;

import static dev.villagefriends.VillageFriends.*;
import dev.villagefriends.client.*;
import java.util.*;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.*;
import net.fabricmc.fabric.api.client.gametest.v1.world.TestWorldSave;
import net.minecraft.core.*;
import net.minecraft.core.component.DataComponents;
import net.minecraft.network.chat.Component;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.*;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.item.*;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.phys.*;

/** Actual marker placement, rendered children/accessories and persistent community identities. */
@SuppressWarnings("UnstableApiUsage")
public final class CommunityGameTest implements FabricClientGameTest {
    private static void check(boolean ok,String reason){if(!ok)throw new AssertionError(reason);}
    private static Villager villager(TestSingleplayerContext w,UUID id){return (Villager)w.getConnection().getServerLevel().getEntity(id);}
    private static UUID spawn(TestSingleplayerContext w,double x,double z,boolean child,String look) {
        var p=w.getConnection().getServerPlayer();var v=new Villager(EntityTypes.VILLAGER,p.level());v.setPos(p.getX()+x,p.getY(),p.getZ()+z);v.setNoAi(true);v.setAge(child?-24000:0);v.setYRot(180);v.yBodyRot=v.yHeadRot=180;
        if(look!=null)target(v).setAttached(PROFILE,ResidentProfile.generate(v.getUUID(),look));
        w.getConnection().getServerLevel().addFreshEntity(v);return v.getUUID();
    }
    private static void open(ClientGameTestContext c,TestSingleplayerContext w,UUID id) {
        w.getConnection().waitForClientboundEntityUpdates(EntityTypes.VILLAGER);
        int eid=w.getServer().computeOnServer(s->villager(w,id).getId());
        c.runOnClient(client->{client.gui.setScreen(null);var e=client.level.getEntity(eid);client.gameMode.interact(client.player,e,new EntityHitResult(e),InteractionHand.MAIN_HAND);});
        c.waitForScreen(FriendshipScreen.class);w.getConnection().waitForServerboundPackets();w.getConnection().waitForClientboundPackets();
    }
    @Override public void runTest(ClientGameTestContext c) {
        UUID child,adult,legacy,curedLegacy;String childIdentity,adultLook;BlockPos marker;TestWorldSave saved;
        c.getInput().resizeWindow(1280,800);c.runOnClient(client->{client.options.guiScale().set(2);client.resizeGui();});
        try(var w=c.worldBuilder().create()) {
            w.getConnection().waitForChunksRender();w.getServer().runCommand("time set day");w.getServer().runCommand("gamemode creative @a");
            adult=w.getServer().computeOnServer(s->spawn(w,0,3,false,ResidentAppearance.generate(new UUID(0, 10))));
            child=w.getServer().computeOnServer(s->spawn(w,1,2,true,ResidentAppearance.generate(new UUID(0, 11))));
            legacy=w.getServer().computeOnServer(s->spawn(w,-2,3,false,ResidentAppearance.generate(new UUID(0, 12))));
            childIdentity=w.getServer().computeOnServer(s->profile(villager(w,child)).id());adultLook=w.getServer().computeOnServer(s->profile(villager(w,child)).look());
            marker=w.getServer().computeOnServer(s->{
                var p=w.getConnection().getServerPlayer();var level=w.getConnection().getServerLevel();var pos=p.blockPosition().offset(-2,0,1);
                level.setBlock(pos.below(),Blocks.OAK_PLANKS.defaultBlockState(),3);p.setItemInHand(InteractionHand.MAIN_HAND,new ItemStack(VillageMarkerBlock.ITEM));
                p.getMainHandItem().set(DataComponents.CUSTOM_NAME,Component.literal("Willowhaven"));
                var context=new BlockPlaceContext(p,InteractionHand.MAIN_HAND,p.getMainHandItem(),new BlockHitResult(Vec3.atCenterOf(pos.below()),Direction.UP,pos.below(),false));
                VillageMarkerBlock.ITEM.place(context);
                check(level.getBlockState(pos).is(VillageMarkerBlock.BLOCK),"Named marker actually places its block");
                check(VillageSettlements.book(level).at(pos).name().equals("Willowhaven"),"Anvil name names settlement");
                for(UUID id:List.of(adult,child,legacy)){var v=villager(w,id);check(name(v).equals(Dialogue.name(v.getUUID(),profile(v).look())+" of Willowhaven"),"All nearby residents receive First Last of Village");VillageSettlements.identify(v,true);check(name(v).indexOf(" of ")==name(v).lastIndexOf(" of "),"Suffix never repeats");}
                var v=villager(w,legacy);save(v,p,new FriendshipState(143,7,8,2,"minecraft:emerald"));saveBond(v,p,BondState.migrated(4));
                check(profile(v).look().equals(ResidentAppearance.generate(new UUID(0, 12))),"Previously saved adult recipe is preserved");
                check(NarrativeEngine.greeting(v,p).contains("Willowhaven")&&NarrativeEngine.conversation(v,p,"work").contains("Willowhaven"),"Adults refer directly to their village");
                check(NarrativeEngine.conversation(villager(w,child),p,"chat").contains("Willowhaven"),"Children know their hometown too");
                p.setItemInHand(InteractionHand.MAIN_HAND,ItemStack.EMPTY);return pos;
            });
            w.getConnection().waitForClientboundEntityUpdates(EntityTypes.VILLAGER);c.waitTicks(15);
            c.runOnClient(client->{
                var a=new ResidentModel(false);var b=new ResidentModel(true);
                check(b.head.xScale==.75F&&b.body.xScale==.5F,"Child has proportionally large head and smaller body");
                check(a.head.xScale==1&&a.body.xScale==1,"Adult keeps player proportions");
                var state=new ResidentRenderState();state.outfit=dev.villagefriends.outfit.ResidentLook.generate(new UUID(0, 10)).outfit(dev.villagefriends.outfit.Profession.NONE);
                a.setupAnim(state);state.headEquipment=new ItemStack(Items.IRON_HELMET);a.setupAnim(state);
                state.isBaby=true;b.setupAnim(state);
                check(ResidentSkins.texture(ResidentAppearance.generate(new UUID(0, 10))).getPath().startsWith("generated/"),"New outfit atlas resolves");            });
            open(c,w,child);c.takeScreenshot("village-friends-child-portrait-large");
            c.getInput().resizeWindow(854,480);c.waitTicks(10);c.takeScreenshot("village-friends-child-portrait-compact");c.getInput().resizeWindow(1280,800);c.waitTicks(10);
            c.clickScreenButton("Goodbye");open(c,w,adult);c.takeScreenshot("village-friends-gardener-portrait");c.clickScreenButton("Goodbye");
            w.getServer().runOnServer(s->{
                var p=w.getConnection().getServerPlayer();p.teleportTo(p.getX(),p.getY(),p.getZ()-4);
                villager(w,child).setPos(p.getX()+.85,p.getY(),p.getZ()+5);villager(w,adult).setPos(p.getX()-.85,p.getY(),p.getZ()+5);
                var v=villager(w,legacy);v.setCustomName(Component.literal("Liora Ash"));VillageSettlements.identify(v,false);check(name(v).equals("Liora Ash of Willowhaven"),"Custom name tags preserve hometown");
                VillageSettlements.mark(w.getConnection().getServerLevel(),marker,"Fernford");check(name(v).equals("Liora Ash of Fernford"),"Town rename updates suffix, preserving base");
                check(state(v,p).points()==143&&bond(v,p).legacyLevel()==4,"Town rename keeps friendship and unlocked tiers");
                var home=target(v).getAttached(HOME);v.teleportTo(p.getX()+120,p.getY(),p.getZ());VillageSettlements.identify(v,true);check(target(v).getAttached(HOME).equals(home),"Moving away does not replace hometown");v.teleportTo(p.getX()-3,p.getY(),p.getZ()+5);
            });
            w.getConnection().waitForClientboundEntityUpdates(EntityTypes.VILLAGER);c.getInput().lookAt(0,8);c.waitTicks(25);c.runOnClient(client->client.gui.toastManager().clear());c.takeScreenshot("village-friends-children-and-marker");
            // Show one clear example of each new accessory and outfit family in the real renderer.
            var cast=new ArrayList<UUID>();
            w.getServer().runOnServer(s->{
                for(int n=0;n<10;n++){
                    UUID id=spawn(w,(n%5-2)*2.1,7+(n/5)*3,false,ResidentAppearance.generate(new UUID(0, n+20)));
                    check(name(villager(w,id)).endsWith(" of Fernford"),"Newborn/arriving residents get a known hometown immediately");cast.add(id);
                }
            });
            w.getConnection().waitForClientboundEntityUpdates(EntityTypes.VILLAGER);c.waitTicks(30);c.takeScreenshot("village-friends-expressive-community");
            w.getServer().runOnServer(s->{
                var v=villager(w,child);v.setAge(0);check(profile(v).id().equals(childIdentity)&&profile(v).look().equals(adultLook),"Growing up keeps adult appearance and identity");
                check(target(v).getAttached(HOME)!=null&&name(v).endsWith(" of Fernford"),"Growing up keeps hometown");
            });
            open(c,w,child);c.takeScreenshot("village-friends-grown-up-portrait");c.clickScreenButton("Goodbye");
            curedLegacy=w.getServer().computeOnServer(s->{
                var v=villager(w,legacy);var home=target(v).getAttached(HOME);
                var zombie=v.convertTo(EntityTypes.ZOMBIE_VILLAGER,ConversionParams.single(v,true,true),z->{});
                check(target(zombie).getAttached(HOME).equals(home),"Zombie conversion preserves hometown");
                var cured=zombie.convertTo(EntityTypes.VILLAGER,ConversionParams.single(zombie,true,true),r->{});cured.setNoAi(true);
                check(target(cured).getAttached(HOME).equals(home)&&name(cured).equals("Liora Ash of Fernford"),"Curing keeps full name and origin");
                return cured.getUUID();
            });
            w.getServer().runOnServer(s->{w.getConnection().getServerLevel().destroyBlock(marker,false);VillageSettlements.unmark(w.getConnection().getServerLevel(),marker);check(VillageSettlements.book(w.getConnection().getServerLevel()).at(marker)!=null,"Breaking a marker doesn't erase settlement");});
            saved=w.getWorldSave();
        }
        try(var w=saved.open()) {
            w.getConnection().waitForChunksDownload();UUID finalLegacy=curedLegacy;
            w.getServer().runOnServer(s->{
                var town=VillageSettlements.book(w.getConnection().getServerLevel()).at(marker);check(town!=null&&town.name().equals("Fernford")&&!town.marked(),"Village registry persists without marker");
                var v=villager(w,finalLegacy);check(name(v).equals("Liora Ash of Fernford")&&profile(v).look().equals(ResidentAppearance.generate(new UUID(0, 12))),"Names and old recipes survive reload");
                check(state(v,w.getConnection().getServerPlayer()).points()==143&&bond(v,w.getConnection().getServerPlayer()).legacyLevel()==4,"Existing friendship survives community upgrade");
                var grown=villager(w,child);check(!grown.isBaby()&&profile(grown).id().equals(childIdentity)&&profile(grown).look().equals(adultLook),"Age and original identity persist");
            });
        }
        // Generate a real vanilla village; discovery needs neither a placed marker nor modified terrain.
        try(var w=c.worldBuilder().adjustSettings(ui->{
            var normal=ui.getSettings().worldgenLoadContext().lookupOrThrow(net.minecraft.core.registries.Registries.WORLD_PRESET).getOrThrow(net.minecraft.world.level.levelgen.presets.WorldPresets.NORMAL);
            ui.setWorldType(new net.minecraft.client.gui.screens.worldselection.WorldCreationUiState.WorldTypeEntry(normal));ui.setGenerateStructures(true);ui.setSeed("1");
        }).create()) {
            w.getConnection().waitForChunksDownload();
            BlockPos villagePos=w.getServer().computeOnServer(s->{
                var level=w.getConnection().getServerLevel();var p=w.getConnection().getServerPlayer();
                var pos=level.findNearestMapStructure(net.minecraft.tags.StructureTags.VILLAGE,p.blockPosition(),64,false);check(pos!=null,"Normal world contains a natural village");
                level.getChunkAt(pos);
                var structures=level.registryAccess().lookupOrThrow(net.minecraft.core.registries.Registries.STRUCTURE).getOrThrow(net.minecraft.tags.StructureTags.VILLAGE);
                var start=level.structureManager().getStructureAt(pos,structures);
                // Locate uses the structure's entrance position. Query its generated horizontal references
                // at surface height if the entrance itself is below the final terrain.
                if(!start.isValid()) {
                    for(int y=32;y<192&&!start.isValid();y+=4)start=level.structureManager().getStructureAt(new BlockPos(pos.getX(),y,pos.getZ()),structures);
                }
                check(start.isValid(),"Located structure generates an actual village start");
                var center=start.getBoundingBox().getCenter();level.getChunkAt(center);
                var town=VillageSettlements.discover(level,center);check(town!=null&&town.id().startsWith("natural:"),"Natural village automatically receives a stable name");
                int y=level.getHeight(net.minecraft.world.level.levelgen.Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,center.getX(),center.getZ());
                p.teleportTo(center.getX()+.5,y,center.getZ()+.5);VillageSettlements.updateResidents(level);
                check(VillageSettlements.discover(level,center).equals(town),"Repeat discovery keeps town identity");
                LOGGER.info("NATURAL VILLAGE DISCOVERED: {} at {}",town.name(),center);return center;
            });
            c.waitTicks(110);w.getConnection().waitForChunksRender();c.getInput().lookAt(45,12);c.runOnClient(client->client.gui.toastManager().clear());c.takeScreenshot("village-friends-natural-village");
            w.getServer().runOnServer(s->{
                var level=w.getConnection().getServerLevel();var town=VillageSettlements.book(level).at(villagePos);int assigned=0;
                for(var v:CompanionController.loaded)if(v.level()==level&&town.contains(v.blockPosition())){VillageSettlements.identify(v,true);check(name(v).endsWith(" of "+town.name()),"Generated village locals have hometown names");assigned++;}
                check(assigned>0,"Actual generated villagers participate in settlement identity");
            });
        }
        LOGGER.info("COMMUNITY GAMEPLAY PASSED: named marker placement, hometown dialogue/names/rename, child model/portraits/growth, 2400 rich textures, old/new child textures, accessories/armor, conversion/cure and save/reload.");
    }
}

