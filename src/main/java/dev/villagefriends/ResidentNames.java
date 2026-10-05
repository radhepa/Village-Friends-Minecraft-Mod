package dev.villagefriends;

import com.google.gson.Gson;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.*;
import net.fabricmc.fabric.api.resource.v1.ResourceLoader;
import net.minecraft.resources.Identifier;
import net.minecraft.server.packs.PackType;
import net.minecraft.server.packs.resources.*;
import net.minecraft.util.profiling.ProfilerFiller;

/** Stable automatic names; pool eligibility uses the person's saved complexion. */
public final class ResidentNames {
    public record Pool(String id,int weight,List<Integer> complexions,List<String> names) {}
    public record Data(int version,List<Pool> pools,List<String> surnames,List<String> restrictedSurnames,List<Integer> restrictedSurnameComplexions) {}
    private static final Gson GSON=new Gson();
    private static volatile Data current=builtin();
    public static Data current(){return current;}
    private static Data builtin() {
        try(var stream=ResidentNames.class.getResourceAsStream("/data/villagefriends/villagefriends/names.json")) {
            if(stream==null)throw new IllegalStateException("Bundled name pools missing");
            return validate(GSON.fromJson(new InputStreamReader(stream,StandardCharsets.UTF_8),Data.class));
        }catch(Exception e){throw new IllegalStateException("Cannot read bundled names",e);}
    }
    public static Data validate(Data data) {
        if(data==null||data.version()!=1||data.pools()==null||data.pools().isEmpty()||data.surnames()==null||data.surnames().isEmpty()
            ||data.restrictedSurnames()==null||data.restrictedSurnameComplexions()==null)throw new IllegalArgumentException("Incomplete name pools");
        var ids=new HashSet<String>();var restricted=new HashSet<String>();
        for(var pool:data.pools()) {
            if(!ids.add(pool.id())||pool.weight()<1||pool.weight()>1000||pool.names()==null||pool.names().isEmpty()
                ||pool.complexions()==null||pool.complexions().isEmpty()||pool.complexions().stream().anyMatch(n->n<0||n>5))throw new IllegalArgumentException("Invalid name pool");
            for(String name:pool.names())validName(name);
            if(pool.id().equals("indian")) {
                if(pool.complexions().stream().anyMatch(n->n<2))throw new IllegalArgumentException("Indian names require brown/dark complexions");
                pool.names().forEach(n->restricted.add(n.toLowerCase(Locale.ROOT)));
            }
        }
        if(!ids.contains("indian"))throw new IllegalArgumentException("Indian name pool missing");
        for(var pool:data.pools())if(pool.complexions().stream().anyMatch(n->n<2)&&pool.names().stream().anyMatch(n->restricted.contains(n.toLowerCase(Locale.ROOT))))
            throw new IllegalArgumentException("Restricted Indian names leaked into another pool");
        for(String surname:data.surnames()){validName(surname);if(restricted.contains(surname.toLowerCase(Locale.ROOT)))throw new IllegalArgumentException("Restricted surname leaked");}
        data.restrictedSurnames().forEach(ResidentNames::validName);
        if(data.restrictedSurnameComplexions().stream().anyMatch(n->n<2||n>5))throw new IllegalArgumentException("Restricted surnames require brown/dark complexions");
        for(int skin=0;skin<6;skin++){int s=skin;if(data.pools().stream().noneMatch(p->p.complexions().contains(s)))throw new IllegalArgumentException("Missing complexion name pool");}
        return data;
    }
    private static void validName(String name){if(name==null||name.isBlank()||name.length()>64||name.codePoints().anyMatch(Character::isISOControl))throw new IllegalArgumentException("Invalid name");}
    private static SplittableRandom random(UUID id,long salt){return new SplittableRandom(id.getMostSignificantBits()^Long.rotateLeft(id.getLeastSignificantBits(),27)^salt);}
    public static Pool pool(UUID id,String look) {
        int skin=ResidentAppearance.complexion(look);var eligible=current.pools().stream().filter(p->p.complexions().contains(skin)).toList();
        int choice=random(id,0x71a8f031L).nextInt(eligible.stream().mapToInt(Pool::weight).sum());
        for(var pool:eligible){choice-=pool.weight();if(choice<0)return pool;}
        throw new IllegalStateException("No eligible name pool");
    }
    public static String name(UUID id,String look) {
        var pool=pool(id,look);var first=random(id,0x63179e12L);var last=random(id,0x586a0419L);
        int skin=ResidentAppearance.complexion(look),extra=current.restrictedSurnameComplexions().contains(skin)?current.restrictedSurnames().size():0;
        int index=last.nextInt(current.surnames().size()+extra);
        String surname=index<current.surnames().size()?current.surnames().get(index):current.restrictedSurnames().get(index-current.surnames().size());
        return pool.names().get(first.nextInt(pool.names().size()))+" "+surname;
    }
    public static void register() {
        ResourceLoader.get(PackType.SERVER_DATA).registerReloadListener(Identifier.fromNamespaceAndPath("villagefriends","resident_names"),new SimplePreparableReloadListener<Data>() {
            @Override protected Data prepare(ResourceManager resources,ProfilerFiller profiler) {
                try(var reader=resources.getResourceOrThrow(Identifier.fromNamespaceAndPath("villagefriends","villagefriends/names.json")).openAsReader()) {
                    return validate(GSON.fromJson(reader,Data.class));
                }catch(Exception e){VillageFriends.LOGGER.warn("Name pack invalid; retaining working names",e);return current;}
            }
            @Override protected void apply(Data loaded,ResourceManager resources,ProfilerFiller profiler){current=loaded;}
        });
    }
    private ResidentNames(){}
}
