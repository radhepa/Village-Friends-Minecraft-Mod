package dev.villagefriends;

import com.google.gson.Gson;
import dev.villagefriends.outfit.Gender;
import dev.villagefriends.outfit.ResidentLook;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.*;
import net.fabricmc.fabric.api.resource.v1.ResourceLoader;
import net.minecraft.resources.Identifier;
import net.minecraft.server.packs.PackType;
import net.minecraft.server.packs.resources.*;
import net.minecraft.util.profiling.ProfilerFiller;

/**
 * Stable automatic names. A resident's gender picks the male, female or unisex list (non-binary
 * residents get unisex names) and their saved complexion picks the eligible pools: Indian names and
 * surnames only go to brown and darker complexions (2-5). Residents whose version-1 name already
 * fits keep it, so only mismatched names change.
 */
public final class ResidentNames {
    public record Pool(String id,int weight,List<Integer> complexions,List<String> male,List<String> female,List<String> unisex,List<String> surnames) {
        public List<String> names(Gender gender) {
            return switch(gender) {
                case MALE -> concat(male,unisex);
                case FEMALE -> concat(female,unisex);
                case NON_BINARY -> unisex;
            };
        }
        public boolean has(Gender gender,String name) {
            return unisex.contains(name)||switch(gender){case MALE->male.contains(name);case FEMALE->female.contains(name);case NON_BINARY->false;};
        }
        public List<String> surnamesOr(List<String> fallback){return surnames==null||surnames.isEmpty()?fallback:surnames;}
    }
    public record Data(int version,List<Pool> pools,List<String> surnames,List<String> restrictedSurnames,List<Integer> restrictedSurnameComplexions) {}
    /** The ungendered version-1 pools, kept only to recognise names generated before 2.18.0. */
    private record LegacyPool(String id,int weight,List<Integer> complexions,List<String> names) {}
    private record Legacy(List<LegacyPool> pools,List<String> surnames,List<String> restrictedSurnames,List<Integer> restrictedSurnameComplexions) {}
    private static final Gson GSON=new Gson();
    private static final Legacy LEGACY=legacy();
    private static volatile Data current=builtin();
    public static Data current(){return current;}
    private static List<String> concat(List<String> a,List<String> b){var all=new ArrayList<String>(a.size()+b.size());all.addAll(a);all.addAll(b);return all;}
    private static Data builtin() {
        try(var stream=ResidentNames.class.getResourceAsStream("/data/villagefriends/villagefriends/names.json")) {
            if(stream==null)throw new IllegalStateException("Bundled name pools missing");
            return validate(GSON.fromJson(new InputStreamReader(stream,StandardCharsets.UTF_8),Data.class));
        }catch(Exception e){throw new IllegalStateException("Cannot read bundled names",e);}
    }
    private static Legacy legacy() {
        try(var stream=ResidentNames.class.getResourceAsStream("/villagefriends/legacy_names_v1.json")) {
            if(stream==null)throw new IllegalStateException("Legacy name pools missing");
            return GSON.fromJson(new InputStreamReader(stream,StandardCharsets.UTF_8),Legacy.class);
        }catch(Exception e){throw new IllegalStateException("Cannot read legacy names",e);}
    }
    public static Data validate(Data data) {
        if(data==null||data.version()!=2||data.pools()==null||data.pools().isEmpty()||data.surnames()==null||data.surnames().isEmpty()
            ||data.restrictedSurnames()==null||data.restrictedSurnameComplexions()==null)throw new IllegalArgumentException("Incomplete name pools");
        var ids=new HashSet<String>();var restricted=new HashSet<String>();
        for(var pool:data.pools()) {
            if(!ids.add(pool.id())||pool.weight()<1||pool.weight()>1000||pool.male()==null||pool.female()==null||pool.unisex()==null
                ||pool.male().isEmpty()&&pool.female().isEmpty()&&pool.unisex().isEmpty()
                ||pool.complexions()==null||pool.complexions().isEmpty()||pool.complexions().stream().anyMatch(n->n<0||n>5))throw new IllegalArgumentException("Invalid name pool");
            var seen=new HashSet<String>();
            for(var list:List.of(pool.male(),pool.female(),pool.unisex()))for(String name:list){validName(name);if(!seen.add(name))throw new IllegalArgumentException("Name listed under two genders: "+name);}
            if(pool.surnames()!=null)pool.surnames().forEach(ResidentNames::validName);
            if(pool.id().equals("indian")) {
                if(pool.complexions().stream().anyMatch(n->n<2))throw new IllegalArgumentException("Indian names require brown/dark complexions");
                seen.forEach(n->restricted.add(n.toLowerCase(Locale.ROOT)));
                if(pool.surnames()!=null)pool.surnames().forEach(n->restricted.add(n.toLowerCase(Locale.ROOT)));
            }
        }
        if(!ids.contains("indian"))throw new IllegalArgumentException("Indian name pool missing");
        for(var pool:data.pools())if(pool.complexions().stream().anyMatch(n->n<2)&&(concat(concat(pool.male(),pool.female()),concat(pool.unisex(),pool.surnamesOr(List.of())))).stream().anyMatch(n->restricted.contains(n.toLowerCase(Locale.ROOT))))
            throw new IllegalArgumentException("Restricted Indian names leaked into another pool");
        for(String surname:data.surnames()){validName(surname);if(restricted.contains(surname.toLowerCase(Locale.ROOT)))throw new IllegalArgumentException("Restricted surname leaked");}
        data.restrictedSurnames().forEach(ResidentNames::validName);
        if(data.restrictedSurnameComplexions().stream().anyMatch(n->n<2||n>5))throw new IllegalArgumentException("Restricted surnames require brown/dark complexions");
        for(int skin=0;skin<6;skin++)for(var gender:Gender.values()){int s=skin;
            if(data.pools().stream().noneMatch(p->p.complexions().contains(s)&&!p.names(gender).isEmpty()))throw new IllegalArgumentException("Missing name pool for complexion "+s+" "+gender);}
        return data;
    }
    private static void validName(String name){if(name==null||name.isBlank()||name.length()>64||name.indexOf(' ')>=0||name.codePoints().anyMatch(Character::isISOControl))throw new IllegalArgumentException("Invalid name");}
    private static SplittableRandom random(UUID id,long salt){return new SplittableRandom(id.getMostSignificantBits()^Long.rotateLeft(id.getLeastSignificantBits(),27)^salt);}
    private static ResidentLook look(String recipe){var look=ResidentLook.parse(recipe);return look==null?new ResidentLook(0,Gender.NON_BINARY,dev.villagefriends.outfit.PaletteID.values()[0],0):look;}
    public static Pool pool(UUID id,String recipe) {
        var look=look(recipe);int skin=look.complexion();
        var eligible=current.pools().stream().filter(p->p.complexions().contains(skin)&&!p.names(look.gender()).isEmpty()).toList();
        int choice=random(id,0x2b5e9d41L).nextInt(eligible.stream().mapToInt(Pool::weight).sum());
        for(var pool:eligible){choice-=pool.weight();if(choice<0)return pool;}
        throw new IllegalStateException("No eligible name pool");
    }
    /** True when a first name is one this resident's gender and complexion could be given today. */
    public static boolean fits(String first,String recipe) {
        var look=look(recipe);
        return current.pools().stream().anyMatch(p->p.complexions().contains(look.complexion())&&p.has(look.gender(),first));
    }
    public static String name(UUID id,String recipe) {
        String legacy=legacyName(id,recipe);
        if(legacy!=null&&fits(legacy.substring(0,legacy.indexOf(' ')),recipe))return legacy;
        var look=look(recipe);var pool=pool(id,recipe);var names=pool.names(look.gender());
        var surnames=pool.surnamesOr(current.surnames());
        return names.get(random(id,0x4c0f7a93L).nextInt(names.size()))+" "+surnames.get(random(id,0x1d93e6b5L).nextInt(surnames.size()));
    }
    /**
     * Saves from before 2.18.0 stored names drawn from mixed-gender pools. Returns the corrected
     * name for a stored one that is still the old automatic name (its surname may since have been
     * taken from family), or null when it fits, was chosen by a player or is already current.
     */
    public static String corrected(UUID id,String recipe,String stored) {
        if(stored==null)return null;
        String legacy=legacyName(id,recipe),fresh=name(id,recipe);
        if(legacy==null||legacy.equals(fresh))return null;
        String first=legacy.substring(0,legacy.indexOf(' '));
        if(!stored.startsWith(first+" "))return null;
        String surname=stored.substring(first.length()+1);
        if(surname.isEmpty()||surname.indexOf(' ')>=0)return null;
        if(stored.equals(legacy))return fresh;
        return fresh.substring(0,fresh.indexOf(' '))+" "+surname;
    }
    /** Version-1 generator, reproduced exactly. */
    static String legacyName(UUID id,String recipe) {
        var look=ResidentLook.parse(recipe);int skin=look==null?0:look.complexion();
        var eligible=LEGACY.pools().stream().filter(p->p.complexions().contains(skin)).toList();
        if(eligible.isEmpty())return null;
        int choice=random(id,0x71a8f031L).nextInt(eligible.stream().mapToInt(LegacyPool::weight).sum());
        LegacyPool pool=eligible.getLast();
        for(var p:eligible){choice-=p.weight();if(choice<0){pool=p;break;}}
        int extra=LEGACY.restrictedSurnameComplexions().contains(skin)?LEGACY.restrictedSurnames().size():0;
        int index=random(id,0x586a0419L).nextInt(LEGACY.surnames().size()+extra);
        String surname=index<LEGACY.surnames().size()?LEGACY.surnames().get(index):LEGACY.restrictedSurnames().get(index-LEGACY.surnames().size());
        return pool.names().get(random(id,0x63179e12L).nextInt(pool.names().size()))+" "+surname;
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
