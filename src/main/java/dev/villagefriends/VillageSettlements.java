package dev.villagefriends;

import java.util.*;
import net.fabricmc.fabric.api.attachment.v1.AttachmentTarget;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.tags.StructureTags;
import net.minecraft.world.entity.npc.villager.Villager;
import static dev.villagefriends.VillageFriends.*;

public final class VillageSettlements {
    private static final Map<UUID,String> visiting=new HashMap<>();
    public static VillageBook book(ServerLevel level) { return ((AttachmentTarget)level).getAttachedOrCreate(VILLAGES); }
    private static void put(ServerLevel level,VillageRecord village) { ((AttachmentTarget)level).setAttached(VILLAGES,book(level).put(village)); }
    public static void clear() { visiting.clear(); arrived.clear(); }
    public static VillageRecord discover(ServerLevel level,BlockPos pos) {
        var known=book(level).at(pos); if(known!=null)return known;
        var structures=level.registryAccess().lookupOrThrow(Registries.STRUCTURE).getOrThrow(StructureTags.VILLAGE);
        var start=level.structureManager().getStructureAt(pos,structures);
        if(!start.isValid()) {
            // Walking on a roof or a raised path still counts as entering the village.
            var candidates=level.structureManager().startsForStructure(net.minecraft.core.SectionPos.blockToSectionCoord(pos.getX()),net.minecraft.core.SectionPos.blockToSectionCoord(pos.getZ()),
                structure->structures.stream().anyMatch(holder->holder.value()==structure));
            for(var candidate:candidates) {
                var box=candidate.getBoundingBox();
                if(candidate.isValid()&&pos.getX()>=box.minX()&&pos.getX()<=box.maxX()&&pos.getZ()>=box.minZ()&&pos.getZ()<=box.maxZ()&&Math.abs(pos.getY()-box.getCenter().getY())<=80){start=candidate;break;}
            }
        }
        if(!start.isValid())return null;
        var chunk=start.getChunkPos(); String id="natural:"+chunk.x()+":"+chunk.z();
        var existing=book(level).villages().get(id); if(existing!=null)return existing;
        var bounds=start.getBoundingBox(); var center=bounds.getCenter();
        int radius=Math.clamp(Math.max(bounds.getXSpan(),bounds.getZSpan())/2+24,64,512);
        var village=new VillageRecord(id,VillageNames.generate(level.getSeed(),chunk.x()*16,chunk.z()*16),center.getX(),center.getY(),center.getZ(),radius,false,0,0,0);
        put(level,village); return village;
    }
    public static VillageRecord mark(ServerLevel level,BlockPos pos,String chosenName) {
        var village=discover(level,pos);
        if(village==null) village=new VillageRecord("marker:"+pos.getX()+":"+pos.getY()+":"+pos.getZ(),VillageNames.generate(level.getSeed(),pos.getX(),pos.getZ()),pos.getX(),pos.getY(),pos.getZ(),96,false,0,0,0);
        String name=chosenName==null?"":VillageNames.clean(chosenName);
        if(name.isBlank() || name.length()>48)name=village.name();
        village=village.marker(pos,name); put(level,village); updateResidents(level); return village;
    }
    public static void unmark(ServerLevel level,BlockPos pos) {
        for(var village:book(level).villages().values()) if(village.marked() && new BlockPos(village.mx(),village.my(),village.mz()).equals(pos))put(level,village.unmarked());
    }
    public static VillageRecord home(Villager v) {
        var membership=target(v).getAttached(HOME); if(membership==null || !(v.level() instanceof ServerLevel level))return null;
        var origin=level.getServer().getLevel(net.minecraft.resources.ResourceKey.create(Registries.DIMENSION,net.minecraft.resources.Identifier.parse(membership.dimension())));
        return origin==null?null:book(origin).villages().get(membership.village());
    }
    public static void identify(Villager v,boolean discover) {
        if(!(v.level() instanceof ServerLevel level))return;
        if(dev.villagefriends.homestead.Homesteads.dwells(v))return; // Homestead folk live out in the wild and belong to no village.
        var membership=target(v).getAttached(HOME);
        if(membership==null) {
            if(CompanionController.state(v).active())return; // An outing does not change someone's hometown.
            var village=discover?discover(level,v.blockPosition()):book(level).at(v.blockPosition());
            if(village==null)return;
            membership=new ResidentHome(village.id(),VillageFriends.name(v),level.dimension().identifier().toString());
            target(v).setAttached(HOME,membership);
        }
        String fixed=ResidentNames.corrected(v.getUUID(),profile(v).look(),membership.baseName());
        if(fixed!=null){membership=new ResidentHome(membership.village(),fixed,membership.dimension());target(v).setAttached(HOME,membership);}
        var village=home(v); if(village==null)return;
        String previous=target(v).getAttachedOrElse(HOME_LABEL,"");
        String actual=v.hasCustomName()?v.getCustomName().getString():"";
        // Respect custom name tags without accumulating repeated 'of ...' suffixes.
        if(!previous.isEmpty() && !actual.equals(previous)) {
            membership=new ResidentHome(membership.village(),actual.isBlank()?membership.baseName():actual,membership.dimension());
            target(v).setAttached(HOME,membership);
        }
        String label=VillageNames.label(membership.baseName(),village.name());
        if(!actual.equals(label))v.setCustomName(Component.literal(label));
        if(!previous.equals(label))target(v).setAttached(HOME_LABEL,label);
        v.setCustomNameVisible(true);
        VillageSocieties.register(v);
    }
    /** Gives a resident a new personal name (such as their family's surname), keeping their hometown suffix. */
    public static void rename(Villager v,String base) {
        var membership=target(v).getAttached(HOME); if(membership==null)return;
        target(v).setAttached(HOME,new ResidentHome(membership.village(),base,membership.dimension()));
        var village=home(v); String label=village==null?base:VillageNames.label(base,village.name());
        v.setCustomName(Component.literal(label)); target(v).setAttached(HOME_LABEL,label);
    }
    public static void updateResidents(ServerLevel level) {
        for(var v:List.copyOf(CompanionController.loaded))if(v.isAlive()&&v.level()==level)identify(v,false);
    }
    public static String reference(Villager v,String topic,long variation) {
        var town=home(v); if(town==null)return ""; String name=town.name();
        if(v.isBaby())return switch((int)Math.floorMod(variation,3)) {
            case 0 -> "I live in "+name+"! Do you know any games we can play here?";
            case 1 -> "When I'm bigger, I want to explore beyond "+name+". For now, I'm learning all the little paths.";
            default -> "The other children in "+name+" are my friends. You can be our friend too!";
        };
        if(topic.equals("work"))return "My work is part of life in "+name+". I like knowing the people I do it for.";
        if(topic.equals("adventure"))return "I'd like to see more of the world, but "+name+" will always feel like home.";
        return switch((int)Math.floorMod(variation,3)) {
            case 0 -> "I call "+name+" home. People here notice when you take the time to know them.";
            case 1 -> "There's more to "+name+" than its houses and trades. It's the people who make me want to stay.";
            default -> "If you're staying in "+name+", come visit when you have a quiet moment. You don't have to bring anything.";
        };
    }
    /** Re-crossing the same village edge within a minute does not replay the arrival card. */
    private static final int ARRIVAL_COOLDOWN=1200;
    private record Arrival(String key,int tick,int variant) {}
    private static final Map<UUID,Arrival> arrived=new HashMap<>();
    public static void tick(MinecraftServer server) {
        int now=server.getTickCount();
        if(now%20==0)for(var p:server.getPlayerList().getPlayers()) {
            var level=(ServerLevel)p.level();var village=discover(level,p.blockPosition()); String key=village==null?"":level.dimension().identifier()+"/"+village.id();
            String before=visiting.put(p.getUUID(),key);
            if(village==null||key.equals(before))continue;
            var last=arrived.get(p.getUUID());
            if(last!=null&&last.key().equals(key)&&now-last.tick()<ARRIVAL_COOLDOWN)continue;
            int variant=VillageArrival.next(last==null?-1:last.variant(),p.getRandom().nextInt(VillageArrival.VARIANTS));
            arrived.put(p.getUUID(),new Arrival(key,now,variant));
            if(net.fabricmc.fabric.api.networking.v1.ServerPlayNetworking.canSend(p,VillageArrivalPayload.TYPE))
                net.fabricmc.fabric.api.networking.v1.ServerPlayNetworking.send(p,new VillageArrivalPayload(village.name(),variant));
            else p.sendSystemMessage(Component.literal(VillageArrival.line(variant).sentence(village.name())),true);
        }
        if(now%100==0)for(var level:server.getAllLevels())updateResidents(level);
    }
    private VillageSettlements() {}
}
