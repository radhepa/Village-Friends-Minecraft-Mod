package dev.villagefriends;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.*;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.world.TestWorldSave;
import net.minecraft.core.*;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.StructureTags;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.level.ChunkPos;
import net.minecraft.world.level.block.*;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.densityfunction.SamplerContext;
import net.minecraft.world.level.levelgen.structure.*;
import net.minecraft.world.level.levelgen.structure.pools.JigsawPlacement;
import net.minecraft.world.level.levelgen.structure.pools.SinglePoolElement;
import net.minecraft.world.level.levelgen.structure.pools.alias.PoolAliasLookup;
import net.minecraft.world.level.levelgen.structure.structures.JigsawStructure;
import net.minecraft.world.level.levelgen.structure.templatesystem.*;
import net.minecraft.world.phys.AABB;

/** Native template loading, rotation, rooms, assembly, worldgen and persistence. */
@SuppressWarnings("UnstableApiUsage")
public final class StructuresGameTest implements FabricClientGameTest {
    private static void check(boolean ok, String reason) { if (!ok) throw new AssertionError(reason); }
    private static JsonObject catalog() {
        try (var stream=StructuresGameTest.class.getResourceAsStream("/data/villagefriends/villagefriends/structure-catalog.json")) {
            check(stream!=null,"Structure catalog packaged");
            return JsonParser.parseReader(new InputStreamReader(stream, StandardCharsets.UTF_8)).getAsJsonObject();
        } catch (java.io.IOException e) { throw new AssertionError(e); }
    }
    private static BlockPos pos(JsonArray v) { return new BlockPos(v.get(0).getAsInt(),v.get(1).getAsInt(),v.get(2).getAsInt()); }
    private static BlockPos at(BlockPos local, BlockPos origin, Rotation rotation) {
        return StructureTemplate.transform(local,Mirror.NONE,rotation,BlockPos.ZERO).offset(origin);
    }
    private static boolean passable(ServerLevel level, BlockPos pos) {
        var state=level.getBlockState(pos);
        if (state.getBlock() instanceof DoorBlock) return false; // Doors divide scan regions even when open.
        return state.isAir() || state.is(Blocks.LANTERN) || state.is(Blocks.LADDER) || state.is(Blocks.TORCH)
                || state.is(Blocks.WALL_TORCH) || state.getCollisionShape(level,pos).isEmpty();
    }
    private static void rooms(ServerLevel level, JsonObject definition, BlockPos origin, Rotation rotation) {
        var regions=new ArrayList<Set<BlockPos>>();
        for (var json:definition.getAsJsonArray("rooms")) {
            var room=json.getAsJsonObject();var lo=pos(room.getAsJsonArray("min"));var hi=pos(room.getAsJsonArray("max"));
            var a=at(lo,origin,rotation);var b=at(hi,origin,rotation);
            var probe=at(pos(room.getAsJsonArray("probe")).above(),origin,rotation);
            var seen=new HashSet<BlockPos>();var queue=new ArrayDeque<BlockPos>();seen.add(probe);queue.add(probe);
            while(!queue.isEmpty()) {
                var p=queue.removeFirst();
                check(p.getX()>=Math.min(a.getX(),b.getX())&&p.getX()<=Math.max(a.getX(),b.getX())
                    &&p.getZ()>=Math.min(a.getZ(),b.getZ())&&p.getZ()<=Math.max(a.getZ(),b.getZ())
                    &&p.getY()>=a.getY()&&p.getY()<=b.getY(),"Room sealed after rotation: "+definition.get("id")+"/"+room.get("name")+" at "+p);
                for(var direction:Direction.values()) {
                    var adjacent=p.relative(direction);
                    if(!seen.contains(adjacent)&&passable(level,adjacent)){seen.add(adjacent);queue.add(adjacent);}
                }
            }
            for(var other:regions)check(Collections.disjoint(seen,other),"Distinct bedrooms stay separate");
            int beds=0;
            for(var bed:definition.getAsJsonArray("bed_feet")) {
                var foot=at(pos(bed.getAsJsonArray()),origin,rotation);
                if(seen.contains(foot.above()))beds++;
            }
            check(beds==room.get("beds").getAsInt(),"Enclosed room includes exactly its authored beds");regions.add(seen);
        }
        for(var json:definition.getAsJsonArray("doors")) {
            var p=at(pos(json.getAsJsonArray()),origin,rotation);var state=level.getBlockState(p);
            check(state.getBlock() instanceof DoorBlock,"Both halves of real doors survive template placement");
            var facing=state.getValue(DoorBlock.FACING);
            for(var side:List.of(facing,facing.getOpposite()))for(int height=0;height<2;height++)
                check(passable(level,p.relative(side).above(height)),"Door has a clear two-block walking route on both sides: "+p);
        }
        for(var json:definition.getAsJsonArray("anchors")) {
            var anchor=json.getAsJsonObject();var p=at(pos(anchor.getAsJsonArray("pos")),origin,rotation);
            String name=Identifier.parse(anchor.get("id").getAsString()).getPath();
            check(level.getBlockState(p).is(net.minecraft.core.registries.BuiltInRegistries.BLOCK.getValue(Identifier.parse(anchor.get("id").getAsString()))),"Registered workstation/fixture survives rotation: "+name);
            if(List.of("house_plaque","notice_board","command_desk","apothecary_cot").contains(name))
                check(level.getBlockEntity(p)!=null&&level.getBlockEntity(p).getType().isValid(level.getBlockState(p)),"Template creates the correct block entity: "+name);
        }
    }
    private static List<PoolElementStructurePiece> assembly(ServerLevel level,JsonObject village,long seed,BlockPos start) {
        var generator=level.getChunkSource().getGenerator();var random=level.getChunkSource().randomState();
        var context=new Structure.GenerationContext(level.registryAccess(),generator,generator.getBiomeSource(),
            random.createClimateSampler(SamplerContext.EMPTY_UNCACHED),random,level.getStructureTemplateManager(),seed,ChunkPos.containing(start),level,b->true);
        var pool=level.registryAccess().lookupOrThrow(Registries.TEMPLATE_POOL).getOrThrow(ResourceKey.create(Registries.TEMPLATE_POOL,Identifier.parse(village.get("start_pool").getAsString())));
        var stub=JigsawPlacement.addPieces(context,pool,Optional.of(Identifier.parse(village.get("start_jigsaw").getAsString())),village.get("depth").getAsInt(),start,false,Optional.of(net.minecraft.world.level.levelgen.Heightmap.Types.WORLD_SURFACE_WG),
            new JigsawStructure.MaxDistance(village.get("max_distance").getAsInt()),PoolAliasLookup.EMPTY,JigsawStructure.DEFAULT_DIMENSION_PADDING,JigsawStructure.DEFAULT_LIQUID_SETTINGS).orElseThrow();
        var pieces=stub.getPiecesBuilder().build().pieces().stream().map(p->(PoolElementStructurePiece)p).toList();
        String type=village.get("type").getAsString();
        check(pieces.size()>=village.get("min_pieces").getAsInt(),"A full procedural "+type+" village assembles for seed "+seed+": "+pieces.size()+" pieces");
        var names=new HashSet<String>();
        for(var piece:pieces)names.add(((SinglePoolElement)piece.getElement()).getTemplateLocation().toString());
        for(var json:village.getAsJsonArray("required_modules")) {
            var module=json.getAsJsonObject();boolean found=false;
            for(var id:module.getAsJsonArray("templates"))if(names.contains(id.getAsString()))found=true;
            check(found,"Guaranteed "+type+" layout contains a template from "+module.get("pool"));
        }
        for(int i=0;i<pieces.size();i++)for(int j=i+1;j<pieces.size();j++)
            check(!pieces.get(i).getBoundingBox().intersects(pieces.get(j).getBoundingBox()),"Assembled lots do not overlap");
        return pieces;
    }
    private static JsonObject definition(JsonObject catalog,String id) {
        for(var value:catalog.getAsJsonArray("templates"))if(value.getAsJsonObject().get("id").getAsString().equals(id))return value.getAsJsonObject();
        throw new AssertionError("Missing catalog definition "+id);
    }
    private record View(BlockPos position,float yaw,String name) {}
    @Override public void runTest(ClientGameTestContext c) {
        var catalog=catalog();c.getInput().resizeWindow(1400,900);int[] originalDistance={2};
        c.runOnClient(client->{originalDistance[0]=client.options.renderDistance().get();client.options.guiScale().set(2);client.resizeGui();});
        try(var w=c.worldBuilder().create()) {
            w.getConnection().waitForChunksRender();w.getServer().runCommand("gamemode spectator @a");w.getServer().runCommand("time set 2000");
            w.getServer().runOnServer(server->{
                var level=w.getConnection().getServerLevel();var manager=level.getStructureTemplateManager();
                for(var json:catalog.getAsJsonArray("templates")) {
                    var info=json.getAsJsonObject();var id=Identifier.parse(info.get("id").getAsString());var template=manager.get(id).orElseThrow();
                    check(template.getSize().equals(pos(info.getAsJsonArray("size"))),"Every NBT template loads with correct dimensions: "+id);
                    check(template.getJigsaws(BlockPos.ZERO,Rotation.NONE).size()==info.getAsJsonArray("connectors").size(),"Template connectors parse correctly: "+id);
                    for(var rotation:Rotation.values()) {
                        if(info.getAsJsonArray("rooms").isEmpty()&&rotation!=Rotation.NONE)continue;
                        var origin=new BlockPos(180+rotation.ordinal()*48,80,180);
                        check(template.placeInWorld(level,origin,origin,new StructurePlaceSettings().setRotation(rotation).setIgnoreEntities(true)
                            .setKnownShape(true).addProcessor(JigsawReplacementProcessor.INSTANCE),level.getRandom(),18),"Template places in Minecraft: "+id);
                        rooms(level,info,origin,rotation);
                    }
                }
                // Like the structure itself, start at the surface so terrain-matching streets stay in range.
                for(var village:catalog.getAsJsonArray("villages"))for(int seed=0;seed<12;seed++)assembly(level,village.getAsJsonObject(),seed,new BlockPos(0,0,0));
                VillageFriends.LOGGER.info("STRUCTURE FIXTURES PASSED: {} templates, four bedroom rotations, clear doors, block entities and 12 procedural jigsaw assemblies per village type.",catalog.getAsJsonArray("templates").size());
            });
        }
        // A real normal world exercises biome selection, placement, terrain and entities.
        var residents=new HashMap<UUID,BlockPos>();var fixtures=new ArrayList<BlockPos>();TestWorldSave saved;
        try(var w=c.worldBuilder().adjustSettings(ui->{
            var normal=ui.getSettings().worldgenLoadContext().lookupOrThrow(Registries.WORLD_PRESET).getOrThrow(net.minecraft.world.level.levelgen.presets.WorldPresets.NORMAL);
            ui.setWorldType(new net.minecraft.client.gui.screens.worldselection.WorldCreationUiState.WorldTypeEntry(normal));ui.setGenerateStructures(true);ui.setSeed("1");
        }).create()) {
            w.getConnection().waitForChunksDownload();w.getServer().runCommand("gamemode spectator @a");w.getServer().runCommand("time set 2000");w.getServer().runCommand("weather clear");
            c.runOnClient(client->{client.options.renderDistance().set(8);client.options.broadcastOptions();});
            for(var entry:catalog.getAsJsonArray("villages")) {
            var village=entry.getAsJsonObject();String type=village.get("type").getAsString();var views=new ArrayList<View>();
            BlockPos center=w.getServer().computeOnServer(server->{
                server.getPlayerList().setViewDistance(8);
                var level=w.getConnection().getServerLevel();var registry=level.registryAccess().lookupOrThrow(Registries.STRUCTURE);
                var holder=registry.getOrThrow(ResourceKey.create(Registries.STRUCTURE,Identifier.parse(village.get("structure").getAsString())));
                check(holder.is(StructureTags.VILLAGE),"New "+type+" village participates in settlement discovery");
                var located=level.getChunkSource().getGenerator().findNearestMapStructure(level,HolderSet.direct(holder),BlockPos.ZERO,80,false);
                check(located!=null,"Normal world naturally locates the custom "+type+" village");var entrance=located.getFirst();level.getChunkAt(entrance);
                StructureStart start=StructureStart.INVALID_START;
                for(int y=32;y<256&&!start.isValid();y+=4)start=level.structureManager().getStructureAt(new BlockPos(entrance.getX(),y,entrance.getZ()),holder.value());
                check(start.isValid()&&start.getPieces().size()>=village.get("min_pieces").getAsInt(),"Natural structure generates a full procedural "+type+" village");
                var bounds=start.getBoundingBox();
                for(int x=bounds.minX()>>4;x<=bounds.maxX()>>4;x++)for(int z=bounds.minZ()>>4;z<=bounds.maxZ()>>4;z++)level.getChunk(x,z);
                for(var piece:start.getPieces()) {
                    var poolPiece=(PoolElementStructurePiece)piece;var id=((SinglePoolElement)poolPiece.getElement()).getTemplateLocation();var info=definition(catalog,id.toString());
                    // Terrain-matching streets follow the ground column by column, so their decor has no fixed template height.
                    if(poolPiece.getElement().getProjection()!=net.minecraft.world.level.levelgen.structure.pools.StructureTemplatePool.Projection.TERRAIN_MATCHING)
                        rooms(level,info,poolPiece.getPosition(),poolPiece.getRotation());
                    if(id.getPath().endsWith("/tavern"))views.add(new View(at(new BlockPos(8,2,7),poolPiece.getPosition(),poolPiece.getRotation()),poolPiece.getRotation().rotate(Direction.SOUTH).toYRot(),type+"-tavern"));
                    if(id.getPath().equals("village/family_house"))views.add(new View(at(new BlockPos(6,6,6),poolPiece.getPosition(),poolPiece.getRotation()),poolPiece.getRotation().rotate(Direction.SOUTH).toYRot(),"bedroom"));
                    for(var anchor:info.getAsJsonArray("anchors"))if(anchor.getAsJsonObject().get("id").getAsString().equals("villagefriends:house_plaque"))
                        fixtures.add(at(pos(anchor.getAsJsonObject().getAsJsonArray("pos")),poolPiece.getPosition(),poolPiece.getRotation()));
                }
                var centerPos=bounds.getCenter();var town=VillageSettlements.discover(level,centerPos);check(town!=null,"Natural custom "+type+" village receives its town name");
                var locals=level.getEntitiesOfClass(Villager.class,AABB.of(bounds).inflate(4));
                check(locals.size()>=village.get("resident_minimum").getAsInt(),"Natural "+type+" templates spawn the authored starter residents: "+locals.size());var jobs=new HashSet<String>();
                for(var v:locals) {
                    v.setNoAi(true);VillageSettlements.identify(v,true);residents.put(v.getUUID(),v.blockPosition());jobs.add(VillageFriends.profession(v));
                    check(VillageFriends.name(v).endsWith(" of "+town.name()),"Generated residents join their hometown");
                    if(VillageProfessions.JOBS.contains(VillageFriends.profession(v)))check(v.getOffers().size()==2,"Generated profession has its native trades");
                }
                check(jobs.containsAll(VillageProfessions.JOBS),"Every new profession appears in the generated "+type+" village");
                var player=w.getConnection().getServerPlayer();player.teleportTo(centerPos.getX(),bounds.maxY()+28,centerPos.getZ()+65);
                VillageFriends.LOGGER.info("NATURAL {} VILLAGE GENERATED at {}: {} pieces, {} residents, all ten professions, town {}.",type.toUpperCase(Locale.ROOT),centerPos,start.getPieces().size(),locals.size(),town.name());
                return centerPos;
            });
            // The fast-test all-sections predicate assumes its original tiny view
            // distance. Wait for the actual destination chunk with our wider view.
            c.waitFor(client->client.level!=null&&client.level.getChunkSource().hasChunk(center.getX()>>4,center.getZ()>>4));
            w.getServer().runCommand("tp @a "+center.getX()+" "+(center.getY()+45)+" "+(center.getZ()+65)+" 180 35");
            c.waitTicks(80);c.runOnClient(client->client.gui.toastManager().clear());c.takeScreenshot("village-friends-phase2-"+type+"-village");
            for(var view:views) {
                var p=view.position();w.getServer().runCommand("tp @a "+(p.getX()+.5)+" "+p.getY()+" "+(p.getZ()+.5)+" "+view.yaw()+" 0");
                c.waitTicks(60);c.runOnClient(client->client.gui.toastManager().clear());c.takeScreenshot("village-friends-phase2-"+view.name());
            }
            }
            c.runOnClient(client->{client.options.renderDistance().set(originalDistance[0]);client.options.broadcastOptions();});
            c.waitTicks(5);
            saved=w.getWorldSave();
        }
        try(var w=saved.open()) {
            w.getConnection().waitForChunksDownload();
            w.getServer().runOnServer(server->{
                server.getPlayerList().setViewDistance(8);
                for(var p:residents.values())w.getConnection().getServerLevel().getChunkAt(p);
            });
            c.waitTicks(20);
            w.getServer().runOnServer(server->{
                var level=w.getConnection().getServerLevel();
                for(var pos:fixtures){level.getChunkAt(pos);check(level.getBlockEntity(pos) instanceof HousePlaqueBlockEntity,"Generated house plaque survives world reload");}
                for(var id:residents.keySet()){var v=(Villager)level.getEntity(id);check(v!=null&&VillageSettlements.home(v)!=null,"Generated resident and hometown survive world reload: "+id);}
            });
        }
        c.runOnClient(client->client.options.renderDistance().set(originalDistance[0]));
        VillageFriends.LOGGER.info("PHASE 2 GAMEPLAY PASSED: native templates/rotations, enclosed rooms, reachable doors, 12 procedural jigsaw seeds, natural village worldgen, all professions/trades, named residents, block entities and save/reload.");
    }
}
