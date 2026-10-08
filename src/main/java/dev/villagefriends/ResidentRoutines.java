package dev.villagefriends;

import dev.villagefriends.routine.Routine;
import dev.villagefriends.routine.Routine.Block;
import dev.villagefriends.routine.Routine.Weather;
import dev.villagefriends.routine.RoutineBrain;
import dev.villagefriends.play.Playground;
import dev.villagefriends.tavern.Seat;
import dev.villagefriends.tavern.Taverns;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import net.minecraft.core.BlockPos;
import net.minecraft.core.GlobalPos;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.BlockTags;
import net.minecraft.tags.FluidTags;
import net.minecraft.world.entity.ai.memory.MemoryModuleType;
import net.minecraft.world.entity.ai.memory.WalkTarget;
import net.minecraft.world.entity.ai.village.poi.PoiManager;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.schedule.Activity;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.levelgen.Heightmap;
import static dev.villagefriends.VillageFriends.*;

/**
 * Applies each resident's {@link Routine} to the world once a second: it picks the vanilla activity
 * that carries out the current part of their day (work, the bell, home, bed, play), walks them to the
 * tavern or their hobby spot, hurries them indoors when rain or a storm starts, keeps them awake at
 * home until bedtime, and shares what they are doing with clients for animation and conversation.
 * Guards on night watch walk in squads and guards in a raid muster to fight ({@link GuardPatrols}); at the
 * tavern {@link Taverns} seats, serves and stands residents up;
 * bored children play games together or tag along after a player ({@link Playground});
 * the apothecary leaves whatever they were doing to dress a knocked-out neighbor's wounds ({@link Knockouts}).
 */
public final class ResidentRoutines {
    /** Rain counts as "just stopped" for this long. */
    private static final int CLEARING = 1200;
    private static final Map<ResourceKey<Level>, Long> lastRain = new HashMap<>();
    private record Spot(long day, BlockPos pos) {}
    private static final Map<UUID, Spot> hobbySpots = new HashMap<>();

    public static void clear() { lastRain.clear(); hobbySpots.clear(); }
    public static void unload(Villager v) { hobbySpots.remove(v.getUUID()); }

    public static void tick(MinecraftServer server) {
        for (var level : server.getAllLevels()) if (level.isRaining()) lastRain.put(level.dimension(), level.getGameTime());
        int tick = server.getTickCount();
        for (var v : List.copyOf(CompanionController.loaded)) if (Math.floorMod(tick + v.getId(), 20) == 0) update(v);
    }

    // -- the plan ----------------------------------------------------------------------------------

    public static int seed(Villager v) { return ResidentMotion.seed(UUID.fromString(profile(v).id())); }
    public static int seed(String residentId) {
        try { return ResidentMotion.seed(UUID.fromString(residentId)); } catch (IllegalArgumentException e) { return residentId.hashCode(); }
    }
    public static int timeOfDay(Level level) { return (int) Math.floorMod(level.getOverworldClockTime(), 24000L); }
    public static Routine.Day day(Villager v) {
        return Routine.day(seed(v), profession(v), profile(v).personality(), v.isBaby(), VillageFriends.day(v.level()));
    }
    /** The weather a resident is living through: rain, a storm, snow in cold places, or none at all in deserts. */
    public static Weather weather(Level level, BlockPos pos) {
        if (!level.dimensionType().hasSkyLight() || level.dimensionType().hasCeiling()) return Weather.CLEAR;
        var precipitation = level.getBiome(pos).value().getPrecipitationAt(pos, level.getSeaLevel());
        if (level.isRaining() && precipitation != Biome.Precipitation.NONE) {
            if (level.isThundering()) return Weather.THUNDER;
            return precipitation == Biome.Precipitation.SNOW ? Weather.SNOW : Weather.RAIN;
        }
        Long rained = lastRain.get(level.dimension());
        return rained != null && level.getGameTime() - rained < CLEARING && precipitation == Biome.Precipitation.RAIN ? Weather.CLEARING : Weather.CLEAR;
    }
    public static Routine.Plan plan(Villager v) {
        var level = v.level();
        var brain = v.getBrain();
        var job = brain.getMemory(MemoryModuleType.JOB_SITE).map(GlobalPos::pos).orElse(null);
        boolean indoors = job == null || !level.canSeeSky(job.above());
        var plan = Routine.plan(day(v), timeOfDay(level), weather(level, v.blockPosition()), seed(v), profession(v), profile(v).personality(), v.isBaby(), indoors);
        // Guard duty outranks the schedule: a raid calls every guard out, and a short-handed watch calls up the next guard.
        if (GuardPatrols.defending(v)) return new Routine.Plan(Block.DEFEND, plan.scheduled(), plan.weather(), plan.day());
        if (GuardPatrols.drafted(v, timeOfDay(level)) && plan.block() != Block.NIGHT_WATCH) return new Routine.Plan(Block.NIGHT_WATCH, plan.scheduled(), plan.weather(), plan.day());
        return plan;
    }
    /** What a resident is doing, as shown to players: "At work", "Sheltering from the rain"... */
    public static String doing(Villager v) {
        if (Knockouts.knockedOut(v)) return Knockouts.status(v);
        if (v.isSleeping()) return "Asleep";
        String playing = Playground.doing(v);
        return playing != null ? playing : Taverns.doing(v, plan(v).label());
    }

    // -- applying it -------------------------------------------------------------------------------

    static void update(Villager v) {
        if (!(v.level() instanceof ServerLevel level) || !v.isAlive() || v.isRemoved() || Knockouts.knockedOut(v)) return;
        var plan = plan(v);
        String id = plan.block().id(), old = target(v).getAttached(ROUTINE);
        if (!id.equals(old)) { target(v).setAttached(ROUTINE, id); changed(v, Block.byId(old), plan); }
        var brain = v.getBrain();
        if (!(brain instanceof RoutineBrain routine)) return;
        boolean duty = plan.block() == Block.DEFEND;
        routine.villagefriends$duty(duty);
        // Companions on an outing, guards in a fight and trading residents follow other rules.
        if (v.isNoAi() || v.isPassenger() && !Seat.seated(v) || CompanionController.state(v).active() || CompanionController.hasActivity(v)
                || GuardController.fighting(v) || v.isTrading()) { routine.villagefriends$routine(null, true); return; }
        var activity = Taverns.activity(v, activity(v, level, plan.block()));
        routine.villagefriends$routine(activity, plan.block().sleep);
        var current = brain.getActiveNonCoreActivity().orElse(Activity.IDLE);
        if (duty) {
            // Guards called out by a raid ignore the alarm bell and the urge to hide.
            brain.eraseMemory(MemoryModuleType.HEARD_BELL_TIME); brain.eraseMemory(MemoryModuleType.HIDING_PLACE);
            if (current == Activity.RAID || current == Activity.PRE_RAID || current == Activity.HIDE || current == Activity.PANIC) current = null;
        }
        if (current != activity && (current == null || current == Activity.IDLE || current == Activity.WORK || current == Activity.MEET || current == Activity.REST || current == Activity.PLAY))
            brain.setActiveActivityIfPossible(activity);
        if (v.isSleeping() && !plan.block().sleep) v.stopSleeping();
        if (Knockouts.tend(v, level)) return;
        // Bored children start games with each other, or follow a player around to see what they're up to.
        if (Playground.update(v, level, plan)) return;
        // At the tavern they find a seat with their friends, order, eat and talk; Taverns stands them up afterwards.
        if (Taverns.update(v, level, plan)) return;
        steer(v, level, plan);
    }
    private static Activity activity(Villager v, ServerLevel level, Block block) {
        var brain = v.getBrain();
        boolean bell = brain.hasMemoryValue(MemoryModuleType.MEETING_POINT);
        return switch (block) {
            case SLEEP, NAP, WAKE, BREAKFAST, LUNCH_HOME, SUPPER, EVENING, SHELTER, STORM, SNOWED_IN -> Activity.REST;
            case WORK, PRAYER -> !v.isBaby() && brain.hasMemoryValue(MemoryModuleType.JOB_SITE) ? Activity.WORK : Activity.IDLE;
            case LUNCH, SOCIAL, MARKET, LESSONS -> bell ? Activity.MEET : Activity.IDLE;
            case TAVERN, PERFORM, LUNCH_TAVERN, SUPPER_TAVERN -> tavern(v, level) != null || !bell ? Activity.IDLE : Activity.MEET;
            case PLAY, SNOW_PLAY -> v.isBaby() ? Activity.PLAY : Activity.IDLE;
            case RAIN_WALK -> v.isBaby() ? Activity.PLAY : Activity.IDLE;
            case HOBBY, NIGHT_WATCH, DEFEND -> Activity.IDLE;
        };
    }
    /** Walks a resident to places vanilla activities don't know about: the tavern, a hobby spot, shelter, a patrol route. */
    private static void steer(Villager v, ServerLevel level, Routine.Plan plan) {
        var brain = v.getBrain();
        switch (plan.block()) {
            case TAVERN, PERFORM, LUNCH_TAVERN, SUPPER_TAVERN -> {
                var tavern = tavern(v, level);
                if (tavern != null && !tavern.closerToCenterThan(v.position(), 5)) walk(v, tavern, .55F, 3);
            }
            case HOBBY -> {
                var spot = hobbySpot(v, level);
                if (spot != null && !spot.closerToCenterThan(v.position(), 10)) walk(v, spot, .5F, 2);
            }
            case SHELTER, STORM, SNOWED_IN -> {
                if (!level.canSeeSky(v.blockPosition().above())) break;
                var home = brain.getMemory(MemoryModuleType.HOME).filter(h -> h.dimension() == level.dimension()).map(GlobalPos::pos)
                        .filter(h -> h.closerToCenterThan(v.position(), 48)).orElseGet(() -> cover(v, level));
                if (home != null) walk(v, home, .7F, 1);
            }
            case NIGHT_WATCH -> GuardPatrols.patrol(v, level);
            case DEFEND -> GuardPatrols.muster(v, level);
            default -> {}
        }
    }
    public static void walk(Villager v, BlockPos pos, float speed, int closeEnough) {
        var brain = v.getBrain();
        var existing = brain.getMemory(MemoryModuleType.WALK_TARGET);
        if (existing.isPresent() && existing.get().getTarget().currentBlockPosition().closerThan(pos, closeEnough + 1)) return;
        brain.setMemory(MemoryModuleType.WALK_TARGET, new WalkTarget(pos, speed, closeEnough));
    }
    /** What a change of plan looks like: a dash for cover, a cheer for snow, a sigh of relief when the rain stops. */
    private static void changed(Villager v, Block old, Routine.Plan plan) {
        if (old == null || v.isSleeping()) return;
        switch (plan.block()) {
            case SHELTER, SNOWED_IN -> { if (!old.outdoors() && old != Block.WORK) return; VillageSocieties.emote(v, Emote.SWEAT, v.getRandom().nextInt(20)); }
            case STORM -> VillageSocieties.emote(v, v.isBaby() ? Emote.SWEAT : Emote.EXCLAIM, v.getRandom().nextInt(20));
            case DEFEND -> VillageSocieties.emote(v, Emote.EXCLAIM, v.getRandom().nextInt(10));
            case RAIN_WALK -> VillageSocieties.emote(v, Emote.NOTE, v.getRandom().nextInt(30));
            case SNOW_PLAY -> VillageSocieties.emote(v, Emote.SPARKLE, v.getRandom().nextInt(30));
            default -> {
                if ((old == Block.SHELTER || old == Block.STORM) && plan.weather() == Weather.CLEARING && v.getRandom().nextInt(3) == 0)
                    VillageSocieties.emote(v, Emote.SPARKLE, v.getRandom().nextInt(40));
                else if (plan.block() == Block.WAKE && v.getRandom().nextInt(4) == 0) VillageSocieties.emote(v, Emote.DOTS, 20);
            }
        }
    }

    // -- places ------------------------------------------------------------------------------------

    /** The tavern nearest this resident: a tavern keeper's barrel or tap within reach of the village. */
    public static BlockPos tavern(Villager v, ServerLevel level) {
        var poi = VillageProfessions.poiKey("tavern_keeper");
        return level.getPoiManager().findClosest(holder -> holder.is(poi), v.blockPosition(), 64, PoiManager.Occupancy.ANY).orElse(null);
    }
    /** Somewhere to enjoy their hobby today: water for anglers, flowers for gardeners, a bench for readers... */
    private static BlockPos hobbySpot(Villager v, ServerLevel level) {
        long today = VillageFriends.day(level);
        var cached = hobbySpots.get(v.getUUID());
        if (cached != null && cached.day() == today) return cached.pos();
        String hobby = profile(v).hobby();
        var brain = v.getBrain();
        var home = brain.getMemory(MemoryModuleType.HOME).filter(h -> h.dimension() == level.dimension()).map(GlobalPos::pos).orElse(null);
        var bell = brain.getMemory(MemoryModuleType.MEETING_POINT).filter(h -> h.dimension() == level.dimension()).map(GlobalPos::pos).orElse(null);
        var anchor = bell != null ? bell : home != null ? home : v.blockPosition();
        var random = new java.util.Random(seed(v) * 31L + today);
        BlockPos found = switch (hobby) {
            case "baking", "reading" -> home;
            case "music" -> bell;
            default -> {
                BlockPos best = null;
                for (int i = 0; i < 48 && best == null; i++) {
                    int x = anchor.getX() + random.nextInt(49) - 24, z = anchor.getZ() + random.nextInt(49) - 24;
                    var pos = new BlockPos(x, level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, x, z), z);
                    if (!level.isLoaded(pos) || !level.getFluidState(pos.below()).isEmpty()) continue;
                    if (suits(level, pos, hobby)) best = pos;
                }
                yield best;
            }
        };
        if (found == null) found = home != null && (hobby.equals("carving") || hobby.equals("woodworking") || hobby.equals("collecting")) ? home : null;
        hobbySpots.put(v.getUUID(), new Spot(today, found));
        return found;
    }
    private static boolean suits(ServerLevel level, BlockPos pos, String hobby) {
        return switch (hobby) {
            case "fishing" -> near(level, pos, 2, p -> level.getFluidState(p).is(FluidTags.WATER));
            case "gardening" -> near(level, pos, 2, p -> level.getBlockState(p).is(Blocks.FARMLAND) || level.getBlockState(p).is(BlockTags.FLOWERS));
            case "flowers" -> near(level, pos, 2, p -> level.getBlockState(p).is(BlockTags.FLOWERS));
            case "carving", "woodworking", "painting" -> near(level, pos, 2, p -> level.getBlockState(p).is(VillageBlocks.get("village_bench")) || level.getBlockState(p).is(VillageBlocks.get("campfire_bench")))
                    || hobby.equals("painting") && level.canSeeSky(pos);
            // Stargazers, explorers and collectors are happy anywhere with open sky.
            default -> level.canSeeSky(pos);
        };
    }
    private static boolean near(ServerLevel level, BlockPos center, int r, java.util.function.Predicate<BlockPos> test) {
        for (var p : BlockPos.betweenClosed(center.offset(-r, -1, -r), center.offset(r, 1, r))) if (test.test(p)) return true;
        return false;
    }
    /** The nearest roofed place to stand: under a porch, in a doorway, beneath a tree. */
    private static BlockPos cover(Villager v, ServerLevel level) {
        var random = v.getRandom(); var origin = v.blockPosition();
        BlockPos best = null; double bestDistance = Double.MAX_VALUE;
        for (int i = 0; i < 40; i++) {
            var pos = origin.offset(random.nextInt(25) - 12, random.nextInt(5) - 2, random.nextInt(25) - 12);
            if (!level.isLoaded(pos) || level.canSeeSky(pos.above()) || !level.getBlockState(pos).isAir() || !level.getBlockState(pos.above()).isAir()
                    || !level.getBlockState(pos.below()).isFaceSturdy(level, pos.below(), net.minecraft.core.Direction.UP)) continue;
            double d = pos.distSqr(origin);
            if (d < bestDistance) { best = pos; bestDistance = d; }
        }
        return best;
    }
    private ResidentRoutines() {}
}
