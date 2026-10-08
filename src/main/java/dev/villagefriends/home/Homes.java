package dev.villagefriends.home;

import static dev.villagefriends.VillageFriends.*;

import dev.villagefriends.CompanionController;
import dev.villagefriends.VillageProfessions;
import dev.villagefriends.VillageQuests;
import dev.villagefriends.VillageSettlements;
import dev.villagefriends.VillageSocieties;
import dev.villagefriends.home.HousingIndex.BedKey;
import dev.villagefriends.quest.Notice;
import dev.villagefriends.quest.Postings;
import dev.villagefriends.social.Society;
import dev.villagefriends.social.Townsfolk;
import java.util.*;
import net.fabricmc.fabric.api.attachment.v1.AttachmentTarget;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerEntityEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.GlobalPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.ai.memory.MemoryModuleType;
import net.minecraft.world.entity.ai.village.poi.PoiTypes;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.AbstractBedBlock;
import net.minecraft.world.level.block.state.BlockState;

/**
 * Every village's houses and who sleeps where, kept in step with the world.
 *
 * <p>A village's houses are read from its structure the first time one of its residents is loaded, then each
 * is checked against the real blocks once its chunks are loaded. After that a house is looked at again only
 * when a bed, door, plaque or job site in it changes ({@code HousingBlockChangeMixin}) or someone reads its
 * plaque: one house per tick at most, never a timer, never a chunk load. Beds are handed out by
 * {@link Assignments} whenever the houses or the village's families change (checked every five seconds).
 *
 * <p>Residents keep vanilla's sleeping AI: {@link #keep} points each resident's {@code HOME} memory at the
 * bed they were given and holds that bed's point-of-interest ticket, so vanilla never hands it to anyone
 * else, and takes an assigned bed back from anyone vanilla gave it to.
 *
 * <p>Extension points for later features: {@link #houseOf(ServerLevel, String, String)} and {@link #hearth} (a
 * resident inviting the player to dinner at home); {@link #vacate} and {@link #claim} (a resident moving to
 * another village); {@link HousingIndex#vacated()} (beds left by residents who passed away, for mourning).
 */
public final class Homes {
    /** How far from home a resident walks back for breakfast, supper or the evening. */
    private static final int HOME_REACH = 24;
    /** Knocked-out residents are carried to their own bed this close by. */
    public static final int CARRY_REACH = 48;
    private static final int ASSIGN_EVERY = 100, CHECK_EVERY = 100, MAX_READS = 4096;

    /** A queued look at one house (verify or re-flood), at a probe position for a survey, or at a loose bed. */
    private record Job(ResourceKey<Level> level, String village, String house, BlockPos pos, Kind kind) {
        enum Kind { SURVEY, VERIFY, FLOOD, FOUND }
        String key() { return level.identifier() + "|" + village + "|" + kind + "|" + (house.isEmpty() ? pos.asLong() : house); }
    }
    private static final ArrayDeque<Job> jobs = new ArrayDeque<>();
    private static final Set<String> queued = new HashSet<>();
    /** Villages ("dimension|village") whose beds need handing out again, and when they last were. */
    private static final Set<String> dirty = new HashSet<>();
    private static final Map<String, Integer> lastAssigned = new HashMap<>();
    /** Villages already surveyed this session (or asked to be). */
    private static final Set<String> surveying = new HashSet<>();
    /** Each homeless resident's vanilla home bed, by village: where they already sleep. */
    private static final Map<String, Map<String, BlockPos>> anchors = new HashMap<>();
    /** Per level: chunk to the houses touching it, rebuilt whenever that level's housing changes. */
    private record Spatial(HousingBook book, Map<Long, List<String[]>> chunks) {}
    private static final Map<ResourceKey<Level>, Spatial> spatial = new HashMap<>();
    /** A floor cell to walk to in each house, found once. */
    private static final Map<String, BlockPos> hearths = new HashMap<>();

    public static void register() {
        HouseBounds.install(bounds());
        ServerTickEvents.END_SERVER_TICK.register(Homes::tick);
        ServerLifecycleEvents.SERVER_STOPPED.register(server -> clear());
        ServerEntityEvents.ENTITY_LOAD.register((entity, level) -> { if (entity instanceof Villager v) keep(v, level); });
    }
    public static void clear() {
        jobs.clear(); queued.clear(); dirty.clear(); lastAssigned.clear(); surveying.clear(); anchors.clear(); spatial.clear(); hearths.clear();
    }

    // -- the index ---------------------------------------------------------------------------------

    public static HousingBook book(ServerLevel level) { return ((AttachmentTarget) level).getAttachedOrCreate(HOUSING); }
    public static HousingIndex index(ServerLevel level, String village) { return book(level).get(village); }
    static void put(ServerLevel level, HousingIndex index) {
        var book = book(level); var next = book.put(index);
        if (next != book) ((AttachmentTarget) level).setAttached(HOUSING, next);
    }
    private static String key(ServerLevel level, String village) { return level.dimension().identifier() + "|" + village; }
    /** Asks for a village's beds to be handed out again soon. */
    public static void changed(ServerLevel level, String village) { dirty.add(key(level, village)); }

    /** The level that keeps a resident's village records, or null. */
    static ServerLevel origin(Entity e) {
        var home = target(e).getAttached(HOME);
        if (home == null || !(e.level() instanceof ServerLevel level)) return null;
        return level.getServer().getLevel(ResourceKey.create(Registries.DIMENSION, Identifier.parse(home.dimension())));
    }
    static String id(Entity e) { var p = target(e).getAttached(PROFILE); return p == null ? "" : p.id(); }

    // -- residents ---------------------------------------------------------------------------------

    /**
     * Keeps a resident's vanilla home in step with the bed they were given (once a second, and when they load).
     * The only per-call cost when nothing changed is one memory comparison.
     */
    public static void keep(Villager v, ServerLevel level) {
        var home = target(v).getAttached(HOME); var origin = origin(v);
        if (home == null || origin == null || !v.isAlive()) return;
        String village = home.village(), id = id(v);
        if (id.isEmpty()) return;
        var index = index(origin, village);
        if (!index.surveyed() && surveying.add(key(origin, village))) enqueue(new Job(origin.dimension(), village, "", v.blockPosition().immutable(), Job.Kind.SURVEY));
        var brain = v.getBrain();
        var memory = brain.getMemory(MemoryModuleType.HOME).filter(g -> g.dimension() == level.dimension()).map(GlobalPos::pos).orElse(null);
        var mine = level == origin ? index.beds().get(id) : null;
        var poi = level.getPoiManager();
        if (mine != null && index.house(mine.house()) != null) {
            var head = mine.head();
            if (!head.equals(memory)) {
                if (memory != null) release(level, memory);
                if (level.isLoaded(head)) poi.take(h -> h.is(PoiTypes.HOME), (h, p) -> p.equals(head), head, 1);
                brain.setMemory(MemoryModuleType.HOME, GlobalPos.of(level.dimension(), head));
                var anchored = anchors.get(key(origin, village));
                if (anchored != null) anchored.remove(id);
            } else if (Math.floorMod(level.getGameTime() + v.getId(), 600) < 20 && level.isLoaded(head)) {
                // Now and then, make sure the bed's ticket is held (it may have been given back while they were away).
                poi.take(h -> h.is(PoiTypes.HOME), (h, p) -> p.equals(head), head, 1);
            }
            return;
        }
        if (memory == null) return;
        String owner = level == origin ? index.owner(memory) : null;
        if (owner != null && !owner.equals(id)) {
            // Vanilla gave them someone else's bed: give it back.
            brain.eraseMemory(MemoryModuleType.HOME);
            release(level, memory);
            return;
        }
        if (level != origin) return;
        anchors.computeIfAbsent(key(origin, village), k -> new HashMap<>()).put(id, memory.immutable());
        // A bed no house knows about, in a village that has no structure to read houses from.
        if (owner == null && index.surveyed() && houseWith(index, memory) == null && index.houses().stream().noneMatch(h -> h.kind() == House.Kind.GENERATED))
            enqueue(new Job(origin.dimension(), village, "", memory.immutable(), Job.Kind.FOUND));
    }
    /** Gives a bed's ticket back, if the bed is still there and its chunk is loaded. */
    private static void release(ServerLevel level, BlockPos head) {
        if (level.isLoaded(head) && level.getPoiManager().existsAtPosition(PoiTypes.HOME, head)) level.getPoiManager().release(head);
    }
    private static House houseWith(HousingIndex index, BlockPos pos) {
        for (var h : index.houses()) if (h.box().inflatedBy(1).isInside(pos)) return h;
        return null;
    }

    /** The house a resident sleeps in, or null. */
    public static House houseOf(Villager v) {
        var home = target(v).getAttached(HOME); var origin = origin(v);
        return home == null || origin == null ? null : houseOf(origin, home.village(), id(v));
    }
    /** The house a resident (by id) sleeps in, or null. For a dinner invitation, or anything else that needs their home. */
    public static House houseOf(ServerLevel origin, String village, String resident) { return index(origin, village).houseOf(resident); }
    /** A resident's own bed, if they have one. */
    public static Optional<House.Bed> bedOf(Villager v) {
        var home = target(v).getAttached(HOME); var origin = origin(v);
        if (home == null || origin == null || origin != v.level()) return Optional.empty();
        return index(origin, home.village()).bedOf(id(v));
    }
    /** The name of the house a resident sleeps in, or "". */
    public static String homeName(Villager v) {
        var home = target(v).getAttached(HOME); var origin = origin(v);
        if (home == null || origin == null) return "";
        var index = index(origin, home.village()); var h = index.houseOf(id(v));
        return h == null ? "" : name(origin, index, h);
    }
    public static String name(ServerLevel origin, HousingIndex index, House h) {
        var society = VillageSocieties.society(origin, index.village());
        return HouseNames.name(h, index.residents(h.id()), society == null ? x -> null : society::get);
    }

    /**
     * Somewhere to stand in a house: an open floor cell in its first room, found once. Null when it can't be
     * found (its chunks aren't loaded, or the room is full of furniture). For walking residents home, and for a
     * dinner invitation later.
     */
    public static BlockPos hearth(ServerLevel level, House h) {
        var cached = hearths.get(h.id());
        if (cached != null || h.rooms().isEmpty() || !HouseSurvey.loaded(level, h.box())) return cached;
        var room = h.rooms().getFirst().box(); var center = room.getCenter();
        BlockPos best = null; double distance = Double.MAX_VALUE;
        for (var p : BlockPos.betweenClosed(room.minX(), room.minY(), room.minZ(), room.maxX(), room.maxY(), room.maxZ())) {
            if (!floor(level, p)) continue;
            double d = p.distSqr(center);
            if (d < distance) { distance = d; best = p.immutable(); }
        }
        if (best != null) hearths.put(h.id(), best);
        return best;
    }
    /** Where a resident far from home should walk back to for breakfast, supper or the evening; null when they're close enough already. */
    public static BlockPos homeward(Villager v, ServerLevel level) {
        var h = houseOf(v);
        if (h == null || origin(v) != level || !far(v, h)) return null;
        return hearth(level, h);
    }
    /** More than {@value #HOME_REACH} blocks (across the ground) from their house. */
    private static boolean far(Villager v, House h) {
        var box = h.box();
        double dx = Math.max(0, Math.max(box.minX() - v.getX(), v.getX() - box.maxX() - 1)), dz = Math.max(0, Math.max(box.minZ() - v.getZ(), v.getZ() - box.maxZ() - 1));
        return dx * dx + dz * dz > HOME_REACH * HOME_REACH;
    }
    /** Where a pet curls up while its resident sleeps: the open floor beside their bed's foot. */
    public static Optional<BlockPos> bedside(Villager owner) {
        if (!owner.isSleeping() || !(owner.level() instanceof ServerLevel level)) return Optional.empty();
        var sleeping = owner.getSleepingPos().orElse(null);
        var mine = bedOf(owner).orElse(null);
        var bed = mine != null && (sleeping == null || mine.head().equals(sleeping)) ? mine : sleeping == null ? null : HouseSurvey.bedAt(level, sleeping);
        if (bed == null) return Optional.empty();
        var side = bed.facing().getClockWise();
        for (var p : List.of(bed.foot().relative(side), bed.foot().relative(side.getOpposite()), bed.foot().relative(bed.facing().getOpposite()),
                bed.head().relative(side), bed.head().relative(side.getOpposite())))
            if (level.isLoaded(p) && floor(level, p)) return Optional.of(p);
        return Optional.empty();
    }
    /** Open at feet and head with a solid floor, and not a doorway. */
    static boolean floor(ServerLevel level, BlockPos p) {
        var at = level.getBlockState(p);
        if (!at.getCollisionShape(level, p).isEmpty() || HouseSurvey.door(at) || !at.getFluidState().isEmpty()) return false;
        if (!level.getBlockState(p.above()).getCollisionShape(level, p.above()).isEmpty()) return false;
        return level.getBlockState(p.below()).isFaceSturdy(level, p.below(), Direction.UP);
    }

    /** A resident leaves their bed for good ("moved" to another village, say): it is freed and remembered. */
    public static void vacate(ServerLevel origin, String village, String resident, String name, String why) {
        var index = index(origin, village);
        var next = index.vacate(resident, name, day(origin), why);
        if (next == index) return;
        var key = index.beds().get(resident);
        if (key != null) release(origin, key.head());
        put(origin, next); changed(origin, village);
    }
    /** A resident has settled in another village: their old bed is freed and the new village finds them one. */
    public static void claim(ServerLevel fromLevel, String fromVillage, ServerLevel toLevel, String toVillage, String resident, String name) {
        vacate(fromLevel, fromVillage, resident, name, "moved");
        changed(toLevel, toVillage);
    }

    // -- what villagers say and what the ledger shows ----------------------------------------------

    /** Puts {@code house} (their house's name) and {@code home_talk} (which "home." pool fits their situation) into a dialogue fill. */
    public static void talk(Villager v, Map<String, String> fill) {
        var home = target(v).getAttached(HOME); var origin = origin(v);
        if (home == null || origin == null) return;
        var index = index(origin, home.village()); String id = id(v);
        if (!index.surveyed()) return;
        var h = index.houseOf(id); long today = day(origin);
        var need = index.needOf(id);
        if (h == null) { fill.put("home_talk", "homeless"); return; }
        boolean fresh = today - index.moved().getOrDefault(id, -100L) <= 2;
        // Children notice when the house is too small, and talk about their own bed (a new one most of all).
        if (v.isBaby()) { fill.put("home_talk", need != null ? "crowded" : fresh ? "new" : "mine"); return; }
        fill.put("house", name(origin, index, h));
        // Out late, far from home: "I'm off home" (home.bedtime).
        if (v.level() == origin && far(v, h)) fill.put("home_far", "true");
        var housemates = index.residents(h.id());
        String talk;
        if (need != null && !need.kind().equals(HousingIndex.NEWBORN)) talk = "crowded";
        else if (fresh) talk = h.player() ? "new.player" : "new";
        else if (housemates.stream().anyMatch(o -> !o.equals(id) && today - index.moved().getOrDefault(o, -100L) <= 2 && partnerOf(origin, home.village(), id).equals(o))) talk = "partner_moved";
        else if (housemates.stream().anyMatch(o -> !o.equals(id) && today - index.moved().getOrDefault(o, -100L) <= 3 && isBaby(origin, home.village(), o))) talk = "newborn_bed";
        else if (index.vacated().stream().anyMatch(x -> x.house().equals(h.id()) && x.why().equals("passed") && today - x.day() <= 7)) talk = "vacant";
        else talk = housemates.size() > 1 ? "shared" : "mine";
        fill.put("home_talk", talk);
    }
    private static String partnerOf(ServerLevel origin, String village, String id) {
        var society = VillageSocieties.society(origin, village); var t = society == null ? null : society.get(id);
        return t == null ? "" : t.partner();
    }
    private static boolean isBaby(ServerLevel origin, String village, String id) {
        var society = VillageSocieties.society(origin, village); var t = society == null ? null : society.get(id);
        return t != null && Assignments.newborn(t);
    }

    /** The Ledger's line about where a resident lives: "Home: The Ashford House (with Tobin, Pip)". Null when the village's houses aren't known yet. */
    public static String ledgerLine(ServerLevel origin, String village, Society society, String id) {
        var index = index(origin, village);
        if (!index.surveyed()) return null;
        var t = society.get(id);
        if (t == null || !t.home()) return null;
        var h = index.houseOf(id);
        if (h == null) return "No bed of their own yet";
        if (h.use() == House.Use.BARRACKS && !h.jobs().contains(t.job())) return "Sleeping at the garrison";
        if (h.use() == House.Use.INN && !h.jobs().contains(t.job())) return "Lodging in the tavern's guest rooms";
        var with = index.residents(h.id()).stream().filter(o -> !o.equals(id)).map(o -> first(society.nameOf(o))).toList();
        return "Home: " + name(origin, index, h) + (with.isEmpty() ? "" : " (with " + String.join(", ", with) + ")");
    }
    /** Residents with no bed of their own. */
    public static Set<String> homeless(ServerLevel origin, String village) { return Set.copyOf(index(origin, village).homeless()); }
    /** Ledger news for households short of room: "The Reed family needs a bigger house (4 people, 2 beds)." */
    public static List<String> needLines(ServerLevel origin, String village, Society society) {
        var out = new ArrayList<String>();
        for (var need : index(origin, village).needs().values()) {
            if (out.size() >= 3) break;
            String family = family(society, need.members());
            out.add(switch (need.kind()) {
                case HousingIndex.HOMELESS -> family + " " + (need.members().size() == 1 ? "has" : "have") + " no home of " + (need.members().size() == 1 ? "their own" : "their own yet") + ".";
                case HousingIndex.NEWBORN -> family + " need a bed for the new baby.";
                default -> family + " needs a bigger house (" + need.members().size() + " people, " + need.beds() + (need.beds() == 1 ? " bed" : " beds") + ").";
            });
        }
        return out;
    }
    private static String family(Society society, List<String> members) {
        if (members.size() == 1) return society.nameOf(members.getFirst());
        String surname = HouseNames.surname(members, society::get);
        return surname.isEmpty() ? first(society.nameOf(members.getFirst())) + "'s family" : "The " + surname + " family";
    }
    private static String first(String name) { int space = name.indexOf(' '); return space > 0 ? name.substring(0, space) : name; }

    /** Households that could use a notice for a bigger house, for the village's notice board. */
    public static List<Postings.HouseNeed> needs(ServerLevel origin, String village) {
        var society = VillageSocieties.society(origin, village);
        if (society == null) return List.of();
        var out = new ArrayList<Postings.HouseNeed>();
        for (var need : index(origin, village).needs().values()) {
            String poster = need.members().stream().filter(m -> { var t = society.get(m); return t != null && t.adult() && t.home(); }).findFirst().orElse(null);
            if (poster != null) out.add(new Postings.HouseNeed(poster, need.kind(), need.members().size(), need.beds()));
        }
        return out;
    }
    /** Whether a resident who asked for a bigger house now lives in a house a player built, with room for their whole household. */
    public static boolean housed(ServerLevel origin, String village, String resident) {
        var index = index(origin, village); var h = index.houseOf(resident);
        return h != null && h.kind() == House.Kind.PLAYER && index.needOf(resident) == null;
    }

    // -- ticking -----------------------------------------------------------------------------------

    static void tick(MinecraftServer server) {
        int now = server.getTickCount();
        if (now % CHECK_EVERY == 17) check(server);
        // One house (or survey, or loose bed) per tick, within a budget of block reads.
        int reads = 0;
        while (!jobs.isEmpty() && reads < MAX_READS) {
            var job = jobs.poll(); queued.remove(job.key());
            var level = server.getLevel(job.level());
            if (level == null) continue;
            reads += run(level, job);
            if (job.kind() != Job.Kind.VERIFY) break;
        }
        for (var key : List.copyOf(dirty)) {
            if (now - lastAssigned.getOrDefault(key, -ASSIGN_EVERY) < ASSIGN_EVERY) continue;
            int bar = key.indexOf('|');
            var level = server.getLevel(ResourceKey.create(Registries.DIMENSION, Identifier.parse(key.substring(0, bar))));
            dirty.remove(key);
            if (level == null) continue;
            lastAssigned.put(key, now);
            assign(level, key.substring(bar + 1));
        }
    }
    /** Every five seconds: villages whose families changed get their beds handed out again; newly loaded houses get checked. */
    private static void check(MinecraftServer server) {
        var villages = new HashMap<String, ServerLevel>();
        for (var v : List.copyOf(CompanionController.loaded)) {
            var home = target(v).getAttached(HOME); var origin = origin(v);
            if (home == null || origin == null || !v.isAlive()) continue;
            villages.putIfAbsent(home.village(), origin);
        }
        for (var e : villages.entrySet()) {
            var level = e.getValue(); String village = e.getKey();
            var index = index(level, village);
            if (!index.surveyed()) continue;
            var society = VillageSocieties.society(level, village);
            if (society != null && stamp(society, day(level)) != index.stamp()) changed(level, village);
            for (var h : index.houses()) if (!h.verified() && HouseSurvey.loaded(level, h.box())) enqueue(new Job(level.dimension(), village, h.id(), BlockPos.ZERO, h.player() ? Job.Kind.FLOOD : Job.Kind.VERIFY));
        }
    }
    /** A fingerprint of everything bed assignment depends on in a village's society. */
    static long stamp(Society society, long today) {
        long hash = today * 31;
        for (var t : new TreeMap<>(society.folk()).values()) {
            hash = hash * 1_000_003L + Objects.hash(t.id(), t.status(), t.partner(), t.adult(), t.household(), t.born() >= 0, t.job());
            for (var k : new TreeMap<>(t.kin()).entrySet()) if (k.getValue().equals("parent")) hash = hash * 31 + k.getKey().hashCode();
        }
        return hash == 0 ? 1 : hash;
    }
    private static void enqueue(Job job) { if (queued.add(job.key())) jobs.add(job); }

    private static int run(ServerLevel level, Job job) {
        var index = index(level, job.village());
        switch (job.kind()) {
            case SURVEY -> {
                var start = HouseSurvey.structureAt(level, job.pos());
                var found = start == null ? List.<House>of() : HouseSurvey.fromStructure(start);
                put(level, index.surveyed(found));
                if (start == null) {
                    // No structure: look for loose beds around the resident who led us here.
                    level.getPoiManager().findAll(h -> h.is(PoiTypes.HOME), p -> level.isLoaded(p), job.pos(), HouseSurvey.FOUND_REACH,
                            net.minecraft.world.entity.ai.village.poi.PoiManager.Occupancy.ANY).sorted()
                            .forEach(p -> enqueue(new Job(level.dimension(), job.village(), "", p.immutable(), Job.Kind.FOUND)));
                }
                for (var h : found) if (HouseSurvey.loaded(level, h.box())) enqueue(new Job(level.dimension(), job.village(), h.id(), BlockPos.ZERO, Job.Kind.VERIFY));
                changed(level, job.village());
                return 64;
            }
            case VERIFY -> {
                var h = index.house(job.house());
                if (h == null || !HouseSurvey.loaded(level, h.box())) return 0;
                var next = HouseSurvey.verify(level, h, level.getGameTime());
                put(level, index.withHouse(next));
                hearths.remove(h.id());
                if (!next.verified() || !h.verified() || !next.beds().equals(h.beds()) || !next.workstations().equals(h.workstations())) changed(level, job.village());
                return 16 + h.beds().size();
            }
            case FLOOD -> {
                var h = index.house(job.house());
                if (h == null || h.plaque().isEmpty() || !HouseSurvey.loaded(level, h.box().inflatedBy(4))) return 0;
                var pos = h.plaque().get(); var state = level.getBlockState(pos);
                if (!(state.getBlock() instanceof HousePlaqueBlock)) {
                    put(level, index.withoutHouse(h.id())); changed(level, job.village()); return 1;
                }
                rescan(level, index, h, pos, state);
                return MAX_READS;
            }
            case FOUND -> {
                if (index.owner(job.pos()) != null || houseWith(index, job.pos()) != null || !level.isLoaded(job.pos())) return 0;
                var h = HouseSurvey.found(level, job.pos(), level.getGameTime());
                if (h == null || index.house(h.id()) != null) return 0;
                put(level, index.withHouse(h)); changed(level, job.village());
                return MAX_READS;
            }
        }
        return 0;
    }
    /** Re-floods a player's house from its plaque; when it no longer closes, its beds are given up until it is fixed. */
    private static String rescan(ServerLevel level, HousingIndex index, House h, BlockPos pos, BlockState state) {
        var flood = FloodFill.fromPlaque(HouseSurvey.grid(level), pos, state.getValue(HousePlaqueBlock.FACING), HousePlaqueBlock.standing(state));
        if (!flood.ok()) {
            if (flood.status() != FloodFill.Status.UNLOADED && !h.beds().isEmpty()) {
                put(level, index.withHouse(new House(h.id(), h.kind(), h.template(), h.use(), h.box(), h.rooms(), List.of(), h.doors(), h.workstations(),
                        h.plaque(), h.customName(), h.privateHome(), true, level.getGameTime())));
                changed(level, index.village());
            }
            return failure(flood, h.customName());
        }
        var next = HouseSurvey.fromFlood(level, h.id(), House.Kind.PLAYER, flood, pos, h.customName(), h.privateHome(), level.getGameTime());
        if (!next.equals(h)) { put(level, index.withHouse(next)); changed(level, index.village()); hearths.remove(h.id()); }
        return null;
    }

    /** Hands out a village's beds again and moves points-of-interest tickets to match. */
    static void assign(ServerLevel level, String village) {
        var society = VillageSocieties.society(level, village);
        var index = index(level, village);
        if (society == null || !index.surveyed()) return;
        long today = day(level);
        var asking = new HashSet<String>();
        var board = ((AttachmentTarget) level).getAttachedOrCreate(VillageQuests.BOARDS).get(village);
        if (board != null) for (var n : board.notices()) if (n.kind().equals(Notice.HOUSE)) asking.add(n.poster());
        var next = Assignments.assign(index, society.folk().values(), anchors.getOrDefault(key(level, village), Map.of()), asking, today);
        next = new HousingIndex(next.village(), next.houses(), next.beds(), next.homeless(), next.needs(), next.vacated(), next.moved(), next.cursed(), stamp(society, today), true);
        // Assigned beds hold their ticket; freed ones give it back (only where the chunk is loaded; keep() mends the rest).
        var poi = level.getPoiManager();
        var before = new HashMap<BlockPos, String>(); var after = new HashMap<BlockPos, String>();
        for (var e : index.beds().entrySet()) before.put(e.getValue().head(), e.getKey());
        for (var e : next.beds().entrySet()) after.put(e.getValue().head(), e.getKey());
        for (var e : before.entrySet()) if (!after.containsKey(e.getKey())) release(level, e.getKey());
        for (var e : after.entrySet()) if (!e.getValue().equals(before.get(e.getKey())) && level.isLoaded(e.getKey())) {
            var head = e.getKey();
            poi.take(h -> h.is(PoiTypes.HOME), (h, p) -> p.equals(head), head, 1);
        }
        put(level, next);
        anchors.remove(key(level, village));
    }

    // -- block changes -----------------------------------------------------------------------------

    /** A block changed (main thread only): houses around it are looked at again; a new bed outside any house may be a new one. O(1). */
    public static void changed(ServerLevel level, BlockPos pos, BlockState old, BlockState now) {
        if (old == now || !HouseSurvey.relevant(old) && !HouseSurvey.relevant(now)) return;
        var hits = spatial(level).get(net.minecraft.world.level.ChunkPos.pack(pos.getX() >> 4, pos.getZ() >> 4));
        boolean inHouse = false;
        if (hits != null) for (var hit : hits) {
            var index = index(level, hit[0]); var h = index.house(hit[1]);
            if (h == null || !h.box().inflatedBy(1).isInside(pos)) continue;
            inHouse = true;
            enqueue(new Job(level.dimension(), hit[0], h.id(), BlockPos.ZERO, h.player() ? Job.Kind.FLOOD : Job.Kind.VERIFY));
        }
        if (!inHouse && now.getBlock() instanceof AbstractBedBlock && now.getValue(AbstractBedBlock.PART) == net.minecraft.world.level.block.state.properties.BedPart.HEAD) {
            var record = VillageSettlements.book(level).at(pos);
            if (record == null) return;
            var index = index(level, record.id());
            if (index.surveyed() && index.houses().stream().noneMatch(h -> h.kind() == House.Kind.GENERATED))
                enqueue(new Job(level.dimension(), record.id(), "", pos.immutable(), Job.Kind.FOUND));
        }
    }
    private static Map<Long, List<String[]>> spatial(ServerLevel level) {
        var book = book(level); var cached = spatial.get(level.dimension());
        if (cached != null && cached.book() == book) return cached.chunks();
        var chunks = new HashMap<Long, List<String[]>>();
        for (var index : book.villages().values()) for (var h : index.houses()) {
            var box = h.box().inflatedBy(1);
            for (int cx = box.minX() >> 4; cx <= box.maxX() >> 4; cx++) for (int cz = box.minZ() >> 4; cz <= box.maxZ() >> 4; cz++)
                chunks.computeIfAbsent(net.minecraft.world.level.ChunkPos.pack(cx, cz), k -> new ArrayList<>()).add(new String[]{index.village(), h.id()});
        }
        spatial.put(level.dimension(), new Spatial(book, chunks));
        return chunks;
    }
    /** The village and house around a position, from the index only. */
    static House houseAt(ServerLevel level, BlockPos pos, String[] village) {
        var hits = spatial(level).get(net.minecraft.world.level.ChunkPos.pack(pos.getX() >> 4, pos.getZ() >> 4));
        if (hits == null) return null;
        House best = null;
        for (var hit : hits) {
            var h = index(level, hit[0]).house(hit[1]);
            if (h == null || !h.box().inflatedBy(1).isInside(pos)) continue;
            // The smaller of two overlapping houses is the one you're in.
            if (best == null || h.box().getXSpan() * h.box().getZSpan() < best.box().getXSpan() * best.box().getZSpan()) { best = h; village[0] = hit[0]; }
        }
        return best;
    }

    /** House bounds for other features (deeds: theft and breaking things in someone's home). */
    public static HouseBounds bounds() {
        return new HouseBounds() {
            @Override public Optional<HouseRef> houseAt(ServerLevel level, BlockPos pos) {
                var village = new String[1]; var h = Homes.houseAt(level, pos, village);
                if (h == null) return Optional.empty();
                var index = index(level, village[0]);
                return Optional.of(new HouseRef(village[0], h.id(), name(level, index, h), index.residents(h.id())));
            }
            @Override public List<String> owners(ServerLevel level, BlockPos pos) {
                var village = new String[1]; var h = Homes.houseAt(level, pos, village);
                if (h == null) return List.of();
                var index = index(level, village[0]);
                var bed = h.bedAt(pos);
                if (bed != null) { String owner = index.owner(bed.head()); return owner == null ? List.of() : List.of(owner); }
                // Either half of a door (the index may list only one), or a door the index hasn't seen yet.
                boolean door = h.doors().contains(pos) || h.doors().contains(pos.below()) || h.doors().contains(pos.above()) || HouseSurvey.door(level.getBlockState(pos));
                boolean station = h.workstations().stream().anyMatch(w -> w.pos().equals(pos));
                return door || station ? index.residents(h.id()) : List.of();
            }
        };
    }

    // -- plaques -----------------------------------------------------------------------------------

    /**
     * A plaque was put up or read: binds it to the village house it hangs in, or floods the house a player built
     * around it. Returns the message to show (success or why not), never null.
     */
    public static String scanPlaque(ServerLevel level, BlockPos pos, String customName) {
        var state = level.getBlockState(pos);
        if (!(state.getBlock() instanceof HousePlaqueBlock)) return "There's no plaque here.";
        var record = VillageSettlements.book(level).at(pos);
        if (record == null) return "This house is outside any village. The plaque still names it, but nobody will move in.";
        var index = index(level, record.id());
        String id = "p:" + pos.getX() + "," + pos.getY() + "," + pos.getZ();
        var mine = index.house(id);
        if (mine == null) {
            // A plaque inside one of the village's own houses names that house.
            for (var h : index.houses()) if (h.kind() != House.Kind.PLAYER && h.box().inflatedBy(1).isInside(pos)) {
                var next = h.plaque().isPresent() && h.plaque().get().equals(pos) && (customName.isBlank() || customName.equals(h.customName())) ? h
                        : h.withPlaque(pos).named(customName.isBlank() ? h.customName() : customName);
                if (next != h) put(level, index.withHouse(next));
                return summary(level, index(level, record.id()), next);
            }
        }
        var flood = FloodFill.fromPlaque(HouseSurvey.grid(level), pos, state.getValue(HousePlaqueBlock.FACING), HousePlaqueBlock.standing(state));
        String name = customName.isBlank() && mine != null ? mine.customName() : customName;
        if (!flood.ok()) {
            if (flood.leak() != null) level.sendParticles(ParticleTypes.HAPPY_VILLAGER, flood.leak().getX() + .5, flood.leak().getY() + .5, flood.leak().getZ() + .5, 12, .3, .3, .3, 0);
            if (mine != null) rescan(level, index, mine, pos, state);
            return failure(flood, name);
        }
        var house = HouseSurvey.fromFlood(level, id, House.Kind.PLAYER, flood, pos, name, mine != null && mine.privateHome(), level.getGameTime());
        put(level, index.withHouse(house)); changed(level, record.id()); hearths.remove(id);
        return summary(level, index(level, record.id()), house);
    }
    private static String failure(FloodFill.Result flood, String name) {
        String house = name == null || name.isBlank() ? "This house" : name;
        return switch (flood.status()) {
            case OPEN_TO_SKY -> flood.leak() == null ? house + " is open to the sky." : house + " is open to the sky above " + flood.leak().getX() + " " + flood.leak().getY() + " " + flood.leak().getZ() + ".";
            case TOO_BIG -> house + " is too big or not closed in (over " + FloodFill.MAX_CELLS + " blocks of room). Put the plaque in a smaller, closed house.";
            case UNLOADED -> "Part of " + (name == null || name.isBlank() ? "this house" : name) + " isn't loaded yet. Try again up close.";
            default -> "The plaque needs to be on a wall of a closed room.";
        };
    }
    private static String summary(ServerLevel level, HousingIndex index, House h) {
        int beds = h.presentBeds().size(), stations = h.workstations().size();
        String head = "★ " + name(level, index, h) + ": " + h.rooms().size() + (h.rooms().size() == 1 ? " room, " : " rooms, ");
        if (beds == 0) return head + "no beds yet; residents can move in once it has one.";
        return head + beds + (beds == 1 ? " bed, " : " beds, ") + stations + (stations == 1 ? " workstation." : " workstations.");
    }

    /** Right-click on a plaque: the house's name, who lives there, its beds and workstation, and what it needs. */
    public static void readout(ServerPlayer player, BlockPos pos) {
        var level = (ServerLevel) player.level();
        var record = VillageSettlements.book(level).at(pos);
        String custom = level.getBlockEntity(pos) instanceof dev.villagefriends.HousePlaqueBlockEntity be ? be.name() : "";
        if (record == null) {
            player.sendSystemMessage(Component.literal("✦ " + (custom.isBlank() ? "A house" : custom)).withStyle(ChatFormatting.GOLD), true);
            player.sendSystemMessage(Component.literal("This house is outside any village. The plaque still names it, but nobody will move in."), false);
            return;
        }
        var index = index(level, record.id());
        var h = plaqueHouse(index, pos);
        // Reading a player's plaque looks the house over again.
        if (h == null || h.player()) {
            String message = scanPlaque(level, pos, custom);
            index = index(level, record.id()); h = plaqueHouse(index, pos);
            if (!message.startsWith("★")) player.sendSystemMessage(Component.literal(message), false);
            if (h == null) return;
        }
        for (var line : readout(level, index, h)) player.sendSystemMessage(line, false);
        String flavor = flavor(index, h, level.getRandom().nextInt(64));
        if (flavor != null) player.sendSystemMessage(Component.literal(flavor).withStyle(ChatFormatting.ITALIC, ChatFormatting.DARK_GRAY), false);
        player.sendSystemMessage(Component.literal("✦ " + name(level, index, h)).withStyle(ChatFormatting.GOLD), true);
    }
    /** A line of how the house looks from the door ({@code home.plaque.lived}, {@code .empty} or {@code .private}), or null. */
    private static String flavor(HousingIndex index, House h, int roll) {
        var lines = dev.villagefriends.talk.DialogueBank.current().pool("home.plaque." + (h.privateHome() ? "private" : index.residents(h.id()).isEmpty() ? "empty" : "lived"));
        for (int n = 0; n < lines.size(); n++) {
            String text = dev.villagefriends.talk.Talk.fill(lines.get((roll + n) % lines.size()), Map.of());
            if (text != null) return text;
        }
        return null;
    }
    private static House plaqueHouse(HousingIndex index, BlockPos pos) {
        for (var h : index.houses()) if (h.plaque().isPresent() && h.plaque().get().equals(pos)) return h;
        for (var h : index.houses()) if (h.box().inflatedBy(1).isInside(pos)) return h;
        return null;
    }
    /** The readout's lines, also used by tests. */
    public static List<Component> readout(ServerLevel level, HousingIndex index, House h) {
        var society = VillageSocieties.society(level, index.village());
        var lines = new ArrayList<Component>();
        lines.add(Component.literal("✦ " + name(level, index, h)).withStyle(ChatFormatting.GOLD));
        var residents = index.residents(h.id());
        var names = new ArrayList<String>();
        for (var r : residents) {
            var t = society == null ? null : society.get(r);
            if (t == null) continue;
            String job = !t.adult() ? "child" : t.job().equals("none") || t.job().equals("nitwit") ? "" : VillageProfessions.label(t.job());
            names.add(t.name() + (job.isEmpty() ? "" : " (" + job + ")"));
        }
        lines.add(Component.literal("Lives here: " + (names.isEmpty() ? (h.privateHome() ? "nobody (private)" : "nobody yet") : String.join(", ", names))));
        int beds = h.presentBeds().size();
        long used = h.presentBeds().stream().filter(b -> index.owner(b.head()) != null).count();
        var station = h.workstations().isEmpty() ? null : h.workstations().getFirst();
        String stationText = "";
        if (station != null) {
            String block = level.isLoaded(station.pos()) ? level.getBlockState(station.pos()).getBlock().getName().getString() : station.job();
            String worker = residents.stream().map(r -> society == null ? null : society.get(r)).filter(t -> t != null && t.job().equals(station.job()))
                    .map(t -> first(t.name())).findFirst().orElse("");
            stationText = " · Workstation: " + block + (worker.isEmpty() ? "" : " (" + worker + ")");
        }
        lines.add(Component.literal("Beds: " + used + " of " + beds + " used" + stationText).withStyle(ChatFormatting.GRAY));
        for (var r : residents) {
            var need = index.needOf(r);
            if (need == null) continue;
            lines.add(Component.literal("Needs: " + switch (need.kind()) {
                case HousingIndex.NEWBORN -> "a bed for the new baby";
                case HousingIndex.CROWDED -> "more room (" + need.members().size() + " people, " + need.beds() + " beds)";
                default -> "a home";
            }).withStyle(ChatFormatting.YELLOW));
            break;
        }
        if (h.privateHome()) lines.add(Component.literal("Private: residents won't move in. Sneak and use the plaque to open it.").withStyle(ChatFormatting.GRAY));
        return lines;
    }
    /** Sneak + use on a plaque: a player's house (or an empty village house) becomes private, or open again. */
    public static void togglePrivate(ServerPlayer player, BlockPos pos) {
        var level = (ServerLevel) player.level();
        var record = VillageSettlements.book(level).at(pos);
        if (record == null) { player.sendSystemMessage(Component.literal("This house is outside any village, so nobody moves in anyway."), true); return; }
        var index = index(level, record.id());
        var h = plaqueHouse(index, pos);
        if (h == null) {
            scanPlaque(level, pos, level.getBlockEntity(pos) instanceof dev.villagefriends.HousePlaqueBlockEntity be ? be.name() : "");
            index = index(level, record.id()); h = plaqueHouse(index, pos);
            if (h == null) { player.sendSystemMessage(Component.literal("This plaque isn't on a house yet."), true); return; }
        }
        if (!h.player() && !h.privateHome() && !index.residents(h.id()).isEmpty()) {
            player.sendSystemMessage(Component.literal("Someone lives here. They won't be turned out of their home."), true); return;
        }
        var next = h.privateHome(!h.privateHome());
        put(level, index.withHouse(next)); changed(level, record.id());
        player.sendSystemMessage(Component.literal(next.privateHome() ? "✦ " + name(level, index, next) + " is private now. Residents won't move in."
                : "✦ " + name(level, index, next) + " is open. Residents who need a home may move in."), true);
    }

    private Homes() {}
}
