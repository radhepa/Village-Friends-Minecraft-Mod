package dev.villagefriends.homestead;

import static dev.villagefriends.VillageFriends.*;

import dev.villagefriends.ResidentNames;
import dev.villagefriends.ResidentProfile;
import dev.villagefriends.ResidentRoutines;
import dev.villagefriends.VillageBlocks;
import dev.villagefriends.VillageFriends;
import dev.villagefriends.VillageRecord;
import dev.villagefriends.VillageSettlements;
import dev.villagefriends.homestead.Dwelling.Dweller;
import dev.villagefriends.homestead.Dwelling.Role;
import dev.villagefriends.outfit.Gender;
import dev.villagefriends.outfit.ResidentLook;
import dev.villagefriends.routine.Routine;
import dev.villagefriends.routine.Routine.Block;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import net.fabricmc.fabric.api.attachment.v1.AttachmentRegistry;
import net.fabricmc.fabric.api.attachment.v1.AttachmentType;
import net.minecraft.core.BlockPos;
import net.minecraft.core.GlobalPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.TagKey;
import net.minecraft.world.entity.ai.memory.MemoryModuleType;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.npc.villager.VillagerType;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.structure.Structure;
import net.minecraft.world.level.levelgen.structure.StructureStart;

/**
 * The people who live out in the wild ({@link Dwelling}): the farmstead couple, the pariah, the shepherd, the
 * herbalist and the veteran. When one first loads, the role their homestead tagged them with becomes who they
 * are: the gender the place asks for, a personality that fits the life, one surname for a married couple, the
 * homestead's name on their nameplate and their biome's villager type. They never join a village. Afterwards
 * this keeps them near home, walks the veteran's watch round the tower, and tells conversations where they live.
 *
 * <p>Hooks: {@code VillageFriends} calls {@link #settle} on load, {@code VillageSettlements.identify} skips
 * dwellers, {@code ResidentRoutines} calls {@link #plan}, {@link #steer} and {@link #doing}, {@code TalkWorld}
 * calls {@link #talk}, and {@code NarrativeEngine} sends their talk to their own dialogue pools.
 */
public final class Homesteads {
    public static final AttachmentType<Dweller> DWELLER = AttachmentRegistry.create(VillageBlocks.id("dweller"), b -> b.persistent(Dweller.CODEC));
    private static final TagKey<Structure> HOMESTEADS = TagKey.create(Registries.STRUCTURE, VillageBlocks.id("homesteads"));
    /** The veteran's watch: which corner of the tower they're making for, since when, and when they got there. */
    private record Watch(int leg, long since, long arrived) {}
    private static final Map<UUID, Watch> watches = new HashMap<>();
    private static final int[][] POSTS = {{-6, -6}, {6, -6}, {6, 6}, {-6, 6}};

    /** Registers the attachment (attachments must exist before any entity loads). */
    public static void register() { java.util.Objects.requireNonNull(DWELLER); }
    public static void clear() { watches.clear(); }
    public static void unload(Villager v) { watches.remove(v.getUUID()); }

    public static Dweller dweller(Villager v) { return target(v).getAttached(DWELLER); }
    public static boolean dwells(Villager v) { return target(v).hasAttached(DWELLER); }

    // -- settling in -------------------------------------------------------------------------------

    /** First load of a tagged homestead resident: who they are and where they live. Does nothing for anyone else. */
    public static void settle(Villager v) {
        if (!(v.level() instanceof ServerLevel level) || dwells(v)) return;
        var role = Dwelling.role(v.entityTags());
        if (role == null) return;
        var pos = v.blockPosition();
        var start = homestead(level, pos);
        BlockPos middle = pos;
        String dwelling = "homestead:" + (pos.getX() >> 4) + ":" + (pos.getZ() >> 4);
        if (start != null) {
            var center = start.getBoundingBox().getCenter();
            middle = new BlockPos(center.getX(), pos.getY(), center.getZ());
            dwelling = "homestead:" + start.getChunkPos().x() + ":" + start.getChunkPos().z();
        }
        long seed = level.getSeed() ^ (long) dwelling.hashCode() * 0x9E3779B97F4A7C15L;
        var profile = profile(v);
        var look = ResidentLook.parse(profile.look());
        var gender = Dwelling.gender(v.entityTags());
        if (look != null) {
            // A couple shares a complexion so the family surname suits them both.
            int complexion = role == Role.HOMESTEADER ? Dwelling.complexion(seed) : look.complexion();
            look = new ResidentLook(complexion, gender != null ? gender : look.gender(), look.palette(), look.seed());
        }
        String recipe = look != null ? look.recipe() : profile.look();
        target(v).setAttached(PROFILE, ResidentProfile.withPersonality(profile, role.personality(look == null ? null : look.gender()), recipe));
        String name = ResidentNames.name(v.getUUID(), recipe);
        if (role == Role.HOMESTEADER && look != null) {
            var family = new ResidentLook(look.complexion(), Gender.MALE, look.palette(), seed).recipe();
            String surname = ResidentNames.name(UUID.nameUUIDFromBytes(dwelling.getBytes(StandardCharsets.UTF_8)), family);
            name = first(name) + surname.substring(surname.indexOf(' '));
        }
        String place = Dwelling.placeName(role, seed);
        target(v).setAttached(DWELLER, new Dweller(role.id(), name, place, dwelling, middle.getX(), middle.getY(), middle.getZ()));
        v.setVillagerData(v.getVillagerData().withType(level.registryAccess(), VillagerType.byBiome(level.getBiome(pos))));
        v.setCustomName(Component.literal(Dwelling.label(role, name, place)));
        v.setCustomNameVisible(true);
        // Share the new look and temperament with clients.
        VillageFriends.ensureIdentity(v);
    }
    private static StructureStart homestead(ServerLevel level, BlockPos pos) {
        var structures = level.registryAccess().lookupOrThrow(Registries.STRUCTURE).get(HOMESTEADS);
        if (structures.isEmpty()) return null;
        var start = level.structureManager().getStructureAt(pos, structures.get());
        return start.isValid() ? start : null;
    }
    private static String first(String name) { int space = name.indexOf(' '); return space > 0 ? name.substring(0, space) : name; }

    // -- their day ---------------------------------------------------------------------------------

    /** A homestead resident's day has no tavern, bell or market in it ({@link Dwelling#adjust}). */
    public static Routine.Plan plan(Villager v, Routine.Plan plan, int time) {
        var d = dweller(v);
        if (d == null || d.kind() == null) return plan;
        var block = Dwelling.adjust(d.kind(), plan.block(), time);
        return block == plan.block() ? plan : new Routine.Plan(block, plan.scheduled(), plan.weather(), plan.day());
    }
    /** What they're doing in words that fit their life, or null for the usual ones. */
    public static String doing(Villager v, Routine.Plan plan) {
        var d = dweller(v);
        if (d == null || d.kind() == null) return null;
        boolean stormy = plan.weather() == Routine.Weather.RAIN || plan.weather() == Routine.Weather.THUNDER;
        return Dwelling.doing(d.kind(), profession(v), plan.block(), stormy);
    }
    /**
     * Keeps a homestead resident near home (wandering off past {@link Dwelling#TETHER} blocks, they turn back for
     * their own bed) and walks the veteran's watch. True when it told them where to go.
     */
    public static boolean steer(Villager v, ServerLevel level, Routine.Plan plan) {
        var d = dweller(v);
        if (d == null || d.kind() == null) return false;
        var middle = new BlockPos(d.x(), d.y(), d.z());
        if (plan.block() == Block.NIGHT_WATCH && d.kind() == Role.VETERAN) { watch(v, level, middle); return true; }
        if (plan.block().sleep || d.away(v.getX(), v.getZ()) <= (long) Dwelling.TETHER * Dwelling.TETHER) return false;
        var bed = v.getBrain().getMemory(MemoryModuleType.HOME).filter(h -> h.dimension() == level.dimension()).map(GlobalPos::pos)
                .filter(h -> h.distSqr(middle) < 40 * 40).orElse(middle);
        ResidentRoutines.walk(v, bed, .55F, 3);
        return true;
    }
    /** The veteran walks slowly from corner to corner round the tower, stopping at each to look out. */
    private static void watch(Villager v, ServerLevel level, BlockPos middle) {
        long now = level.getGameTime();
        var w = watches.getOrDefault(v.getUUID(), new Watch(Math.floorMod(v.getId(), POSTS.length), now, -1));
        var post = post(level, middle, w.leg());
        if (post != null && w.arrived() < 0 && horizontal(v, post) < 2.5 * 2.5) w = new Watch(w.leg(), w.since(), now);
        if (post == null || (w.arrived() >= 0 && now - w.arrived() > 240) || now - w.since() > 900) {
            w = new Watch((w.leg() + 1) % POSTS.length, now, -1);
            post = post(level, middle, w.leg());
        }
        watches.put(v.getUUID(), w);
        if (post == null) return;
        if (w.arrived() < 0) ResidentRoutines.walk(v, post, .42F, 1);
        else v.getLookControl().setLookAt(post.getX() * 2.0 - middle.getX(), post.getY() + 1.5, post.getZ() * 2.0 - middle.getZ());
    }
    private static BlockPos post(ServerLevel level, BlockPos middle, int leg) {
        int x = middle.getX() + POSTS[leg][0], z = middle.getZ() + POSTS[leg][1];
        var probe = new BlockPos(x, middle.getY(), z);
        if (!level.hasChunkAt(probe)) return null;
        var pos = new BlockPos(x, level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, x, z), z);
        if (Math.abs(pos.getY() - middle.getY()) > 6 || !level.getFluidState(pos.below()).isEmpty()) return null;
        return pos;
    }
    private static double horizontal(Villager v, BlockPos p) { double dx = v.getX() - (p.getX() + .5), dz = v.getZ() - (p.getZ() + .5); return dx * dx + dz * dz; }

    // -- talking -----------------------------------------------------------------------------------

    /**
     * What a conversation with a homestead resident knows: their role ({@code dweller}, which sends their talk to
     * their own pools), {@code place}, the nearest village they could know of ({@code village}, or "the village"),
     * and for the farmstead couple their spouse ({@code partner}, {@code spouse}).
     */
    public static void talk(Villager v, Map<String, String> fill) {
        var d = dweller(v);
        if (d == null || !(v.level() instanceof ServerLevel level)) return;
        fill.put("dweller", d.role());
        fill.put("place", d.place());
        var town = nearestVillage(level, v.blockPosition());
        fill.put("village", town == null ? "the village" : town.name());
        fill.remove("partner");
        var partner = partner(v, d, level);
        if (partner != null) {
            fill.put("partner", first(dweller(partner).name()));
            var look = ResidentLook.parse(profile(partner).look());
            fill.put("spouse", look != null && look.gender() == Gender.FEMALE ? "wife" : "husband");
        }
    }
    /** The other half of a homestead couple, while they're alive and nearby. */
    public static Villager partner(Villager v, Dweller d, ServerLevel level) {
        if (d.kind() != Role.HOMESTEADER) return null;
        var found = level.getEntitiesOfClass(Villager.class, v.getBoundingBox().inflate(48),
                o -> o != v && o.isAlive() && dwells(o) && dweller(o).dwelling().equals(d.dwelling()));
        return found.isEmpty() ? null : found.getFirst();
    }
    private static VillageRecord nearestVillage(ServerLevel level, BlockPos pos) {
        VillageRecord best = null;
        for (var village : VillageSettlements.book(level).villages().values())
            if (village.distance(pos) < 2000L * 2000L && (best == null || village.distance(pos) < best.distance(pos))) best = village;
        return best;
    }
    /** The "About" lines that replace a hometown for someone who lives out here. */
    public static String about(Villager v) {
        var d = dweller(v);
        if (d == null) return null;
        return "\nLives at: " + d.place() + (d.kind() == Role.PARIAH ? " (cast out of their village)" : " (out in the wild)");
    }
    private Homesteads() {}
}
