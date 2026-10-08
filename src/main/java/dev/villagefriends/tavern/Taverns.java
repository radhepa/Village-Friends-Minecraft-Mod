package dev.villagefriends.tavern;

import static dev.villagefriends.VillageFriends.*;

import dev.villagefriends.CompanionController;
import dev.villagefriends.Emote;
import dev.villagefriends.Knockouts;
import dev.villagefriends.ResidentRoutines;
import dev.villagefriends.VillageBlocks;
import dev.villagefriends.VillageSocieties;
import dev.villagefriends.Workstations;
import dev.villagefriends.routine.Routine;
import dev.villagefriends.routine.Routine.Block;
import dev.villagefriends.routine.Routine.Weather;
import dev.villagefriends.social.Society;
import dev.villagefriends.tavern.Patronage.Choice;
import dev.villagefriends.tavern.Patronage.Mood;
import dev.villagefriends.tavern.Patronage.Neighbor;
import dev.villagefriends.tavern.Patronage.Phase;
import dev.villagefriends.tavern.TavernSurvey.Spot;
import dev.villagefriends.tavern.TavernSurvey.Tavern;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;
import java.util.UUID;
import net.fabricmc.fabric.api.attachment.v1.AttachmentRegistry;
import net.fabricmc.fabric.api.attachment.v1.AttachmentSyncPredicate;
import net.fabricmc.fabric.api.attachment.v1.AttachmentType;
import net.fabricmc.fabric.api.creativetab.v1.CreativeModeTabEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerEntityEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.fabricmc.fabric.api.event.player.UseBlockCallback;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.GlobalPos;
import net.minecraft.core.Registry;
import net.minecraft.core.particles.ItemParticleOption;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.entity.ai.memory.MemoryModuleType;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.schedule.Activity;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.HorizontalDirectionalBlock;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.Vec3;

/**
 * The tavern at work. When a resident's day takes them to the tavern ({@link Routine#atTavern}), they look
 * for a seat with their people ({@link Patronage#score}), walk to it and sit down, order, are served by the
 * tavern keeper (who fetches the dish or pours the drink at the bar and carries it to the table) or help
 * themselves when nobody is behind the bar, eat and drink course by course, talk, and get up when their hour
 * is over. With every seat taken they stand at the bar, or mingle. The bard plays on the tavern's stage.
 *
 * <p>What each patron is doing is shared with clients through {@link #STATE} for animation and the dish on
 * the table. Everything else is kept in memory; a resident who was seated when the world was saved keeps
 * their seat and simply orders again.
 */
public final class Taverns {
    public static final EntityType<Seat> SEAT = Registry.register(BuiltInRegistries.ENTITY_TYPE, VillageBlocks.id("seat"),
            EntityType.Builder.<Seat>of(Seat::new, MobCategory.MISC).sized(.25F, .25F).noSummon().fireImmune().noLootTable()
                    .clientTrackingRange(10).updateInterval(20).build(ResourceKey.create(Registries.ENTITY_TYPE, VillageBlocks.id("seat"))));
    /** What a resident is doing at the tavern ("wait", "eat:villagefriends:hearty_stew", "carry:..."), for animation and props. */
    public static final AttachmentType<String> STATE = AttachmentRegistry.create(VillageBlocks.id("tavern"),
            b -> b.syncWith(ByteBufCodecs.STRING_UTF8, AttachmentSyncPredicate.all()));

    /** One visit by one resident. */
    private static final class Patron {
        final UUID id; final String tavern; Block block;
        BlockPos seat, stand; float standYaw;
        Phase phase; String item; long until; int course;
        long progressAt; double bestDistance = Double.MAX_VALUE;
        final Set<BlockPos> unreachable = new HashSet<>();
        Patron(UUID id, String tavern, Block block) { this.id = id; this.tavern = tavern; this.block = block; }
    }
    private record Order(UUID patron, String item, long placed, int roll) {}
    /** One of the staff on the floor: what's on their tray, and the table they're wiping. */
    private static final class Runner {
        final UUID id; final boolean cook; final List<Order> tray = new ArrayList<>();
        boolean carrying; long since; BlockPos wiping; long wipedAt;
        Runner(UUID id, boolean cook) { this.id = id; this.cook = cook; }
    }
    /** One tavern: its survey, who has which seat, the orders waiting at the bar and the one being carried out. */
    private static final class House {
        final ResourceKey<Level> dimension; Tavern tavern; long surveyed, used;
        final Map<BlockPos, UUID> claims = new HashMap<>();
        final ArrayDeque<Order> orders = new ArrayDeque<>();
        final Map<UUID, Runner> runners = new HashMap<>();
        /** Seats whose diners have just left, waiting for the keeper's cloth. */
        final ArrayDeque<BlockPos> dirty = new ArrayDeque<>();
        House(ResourceKey<Level> dimension) { this.dimension = dimension; }
    }
    private static final Map<String, House> houses = new HashMap<>();
    private static final Map<GlobalPos, String> stationKeys = new HashMap<>();
    private static final Map<UUID, Patron> patrons = new HashMap<>();

    private static final int RESURVEY = 1200, FORGET = 12000, GIVE_UP_WALKING = 300, CARRY_TIMEOUT = 600, LONG_WAIT = 900, TRAY = 3;

    public static void register() {
        TavernBlocks.register();
        TavernItems.register();
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.FUNCTIONAL_BLOCKS).register(entries -> TavernBlocks.all().forEach(entries::accept));
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.FOOD_AND_DRINKS).register(entries -> TavernItems.meals().forEach(entries::accept));
        ServerTickEvents.END_SERVER_TICK.register(Taverns::tick);
        ServerEntityEvents.ENTITY_UNLOAD.register((entity, level) -> { if (entity instanceof Villager v) forget(v); });
        ServerLifecycleEvents.SERVER_STOPPED.register(server -> clear());
        UseBlockCallback.EVENT.register(Taverns::use);
    }
    public static void clear() { houses.clear(); stationKeys.clear(); patrons.clear(); }

    // -- residents, once a second ------------------------------------------------------------------

    /**
     * Seats and serves a resident while their day has them at the tavern, and stands them up when it doesn't.
     * Called once a second for every resident by {@link ResidentRoutines}; true if the tavern took care of them.
     */
    public static boolean update(Villager v, ServerLevel level, Routine.Plan plan) {
        var p = patrons.get(v.getUUID());
        if (!Routine.atTavern(plan.block()) || v.isBaby()) {
            if (p != null || Seat.seated(v) || target(v).hasAttached(STATE) && !serving(v)) leave(v);
            return false;
        }
        // Frightened residents (panic, a raid, hiding) leave the tavern to vanilla until they calm down.
        if (!calm(v)) { if (p != null || Seat.seated(v)) leave(v); return true; }
        var house = house(level, v, p);
        if (house == null) { if (p != null) leave(v); return false; }
        long now = level.getGameTime();
        if (p == null || !p.tavern.equals(house.tavern.key())) {
            if (p != null) leave(v);
            p = new Patron(v.getUUID(), house.tavern.key(), plan.block());
            patrons.put(v.getUUID(), p);
        } else if (p.block != plan.block()) carryOn(p, plan.block(), now);
        house.used = now;
        if (p.block == Block.PERFORM) perform(v, level, house, p, now);
        else visit(v, level, house, p, plan, now);
        return true;
    }
    /** Supper turns into an evening out: they keep their seat and order a drink. */
    private static void carryOn(Patron p, Block block, long now) {
        p.block = block;
        p.course = Math.min(p.course, 1);
        if (p.phase == Phase.DONE) p.until = Math.min(p.until, now + 40);
    }

    private static void visit(Villager v, ServerLevel level, House house, Patron p, Routine.Plan plan, long now) {
        var tavern = house.tavern;
        if (Seat.seated(v)) {
            var seat = ((Seat) v.getVehicle()).seatPos();
            if (!seat.equals(p.seat)) { release(house, p); p.seat = seat; house.claims.put(seat, v.getUUID()); }
            dine(v, level, house, p, now);
            return;
        }
        if (p.seat != null) {
            var spot = tavern.seat(p.seat);
            if (spot == null || !v.getUUID().equals(house.claims.get(p.seat)) || Seat.occupied(level, p.seat)) { giveUp(house, p); }
            else {
                var center = Vec3.atBottomCenterOf(p.seat);
                double dx = v.getX() - center.x, dz = v.getZ() - center.z, d = Math.sqrt(dx * dx + dz * dz), dy = v.getY() - p.seat.getY();
                if (d < 1.6 && dy > -1.2 && dy < 1.4) {
                    if (Seat.sit(v, p.seat, spot.surface(), spot.yaw())) {
                        v.getBrain().eraseMemory(MemoryModuleType.WALK_TARGET); v.getNavigation().stop();
                        if (p.phase == null) p.until = now + 20 + v.getRandom().nextInt(40);
                    } else giveUp(house, p);
                    return;
                }
                if (progress(p, d, now)) { ResidentRoutines.walk(v, p.seat, .55F, 1); return; }
                giveUp(house, p);
            }
        }
        if (p.stand != null) {
            var center = Vec3.atBottomCenterOf(p.stand);
            double dx = v.getX() - center.x, dz = v.getZ() - center.z, d = Math.sqrt(dx * dx + dz * dz);
            if (d > 1.2) {
                if (progress(p, d, now)) ResidentRoutines.walk(v, p.stand, .55F, 0);
                else { p.unreachable.add(p.stand); release(house, p); p.stand = null; }
                return;
            }
            var facing = Vec3.directionFromRotation(0, p.standYaw);
            v.getLookControl().setLookAt(center.x + facing.x * 2, v.getEyeY() - .3, center.z + facing.z * 2);
            dine(v, level, house, p, now);
            return;
        }
        choose(v, level, house, p, plan, now);
    }
    /** Still getting closer? Residents who can't find a way to their chair pick another. */
    private static boolean progress(Patron p, double distance, long now) {
        if (p.progressAt == 0 || distance < p.bestDistance - .5) { p.bestDistance = distance; p.progressAt = now; }
        return now - p.progressAt < GIVE_UP_WALKING;
    }
    private static void giveUp(House house, Patron p) {
        if (p.seat != null) p.unreachable.add(p.seat);
        release(house, p); p.seat = null; p.progressAt = 0; p.bestDistance = Double.MAX_VALUE;
    }

    /** A seat with their people, a place at the bar, or failing that a spot in the room. */
    private static void choose(Villager v, ServerLevel level, House house, Patron p, Routine.Plan plan, long now) {
        var tavern = house.tavern;
        int time = ResidentRoutines.timeOfDay(level);
        boolean dark = time >= Routine.at(18, 30) || time < Routine.at(6, 0);
        var mood = new Mood(profile(v).personality(), plan.block(), plan.weather() == Weather.RAIN || plan.weather() == Weather.THUNDER,
                plan.weather() == Weather.SNOW, dark);
        var society = VillageSocieties.of(v);
        String me = profile(v).id(); long today = day(level);
        var sitting = new HashMap<Integer, List<UUID>>();
        for (var claim : house.claims.entrySet()) {
            var spot = tavern.seat(claim.getKey());
            if (spot != null) sitting.computeIfAbsent(spot.table(), k -> new ArrayList<>()).add(claim.getValue());
        }
        var random = new Random(ResidentRoutines.seed(v) * 31L + now / 200);
        var known = new HashMap<UUID, Neighbor>();
        Spot chosen = null; double best = Patronage.CLOSED;
        for (var s : tavern.seats()) {
            if (house.claims.containsKey(s.pos()) || p.unreachable.contains(s.pos()) || Seat.occupied(level, s.pos())) continue;
            var table = new ArrayList<Neighbor>();
            for (var id : sitting.getOrDefault(s.table(), List.of())) table.add(known.computeIfAbsent(id, k -> neighbor(level, society, me, k, today)));
            int free = tavern.tableSeats().getOrDefault(s.table(), 1) - table.size() - 1;
            double distance = Math.sqrt(s.pos().distSqr(v.blockPosition()));
            double score = Patronage.score(mood, new Choice(s.kind(), s.hearth(), s.outdoor(), free, table, distance), random.nextDouble());
            if (score > best) { best = score; chosen = s; }
        }
        if (chosen != null) {
            p.seat = chosen.pos(); house.claims.put(chosen.pos(), v.getUUID());
            p.progressAt = now; p.bestDistance = Double.MAX_VALUE;
            ResidentRoutines.walk(v, p.seat, .55F, 1);
            return;
        }
        for (var stand : tavern.standing()) {
            if (house.claims.containsKey(stand.pos()) || p.unreachable.contains(stand.pos())) continue;
            p.stand = stand.pos(); p.standYaw = stand.yaw(); house.claims.put(stand.pos(), v.getUUID());
            p.progressAt = now; p.bestDistance = Double.MAX_VALUE;
            return;
        }
        // A packed house: find a bit of floor in the room.
        var origin = tavern.stations().getFirst();
        for (int i = 0; i < 24; i++) {
            var cell = origin.offset(random.nextInt(13) - 6, random.nextInt(3) - 1, random.nextInt(13) - 6);
            if (!tavern.box().isInside(cell) || house.claims.containsKey(cell) || p.unreachable.contains(cell) || !TavernSurvey.floor(level, cell) || level.canSeeSky(cell)) continue;
            p.stand = cell; p.standYaw = random.nextFloat() * 360; house.claims.put(cell, v.getUUID());
            p.progressAt = now; p.bestDistance = Double.MAX_VALUE;
            return;
        }
    }
    private static Neighbor neighbor(ServerLevel level, Society society, String me, UUID other, long today) {
        if (society == null || !(level.getEntity(other) instanceof Villager o)) return Neighbor.STRANGER;
        String them = profile(o).id();
        String romance = society.romance(me, them, today);
        return new Neighbor(society.affinity(me, them, today), !society.relation(me, them).isEmpty(),
                romance.equals("married") || romance.equals("sweethearts"), them.equals(society.bestFriend(me, today)),
                them.equals(society.rival(me, today)), them.equals(society.crush(me, today)));
    }

    // -- the meal ----------------------------------------------------------------------------------

    private static void dine(Villager v, ServerLevel level, House house, Patron p, long now) {
        if (p.phase == null) { if (now >= p.until) order(v, level, house, p, now); return; }
        switch (p.phase) {
            case WAIT, CARRY, WIPE -> {}
            case EAT, DRINK -> { if (now >= p.until) finish(v, p, now); else savor(v, level, p); }
            case DONE -> { if (now >= p.until && p.course < Patronage.maxCourses(p.block)) order(v, level, house, p, now); }
        }
    }
    private static void order(Villager v, ServerLevel level, House house, Patron p, long now) {
        int roll = v.getRandom().nextInt(1000);
        String item = Patronage.order(p.block, p.course, day(level), ResidentRoutines.seed(v), cooking(level, house), roll);
        p.course++;
        if (item == null) { p.phase = Phase.DONE; p.until = Long.MAX_VALUE; return; }
        p.phase = Phase.WAIT; p.item = null;
        target(v).setAttached(STATE, Patronage.state(Phase.WAIT, null));
        house.orders.add(new Order(v.getUUID(), item, now, roll));
    }
    private static void finish(Villager v, Patron p, long now) {
        String leftover = Patronage.leftover(p.item);
        p.phase = Phase.DONE;
        p.until = now + Patronage.pause(p.block, v.getRandom().nextInt(1000));
        target(v).setAttached(STATE, Patronage.state(Phase.DONE, leftover));
        if (v.getRandom().nextInt(4) == 0) VillageSocieties.emote(v, p.block == Block.TAVERN ? Emote.NOTE : Emote.SPARKLE, 10);
    }
    /** The sounds of a full tavern: a bite here, a sip there. */
    private static void savor(Villager v, ServerLevel level, Patron p) {
        boolean drink = p.phase == Phase.DRINK;
        if (v.getRandom().nextInt(drink ? 14 : 8) != 0) return;
        level.playSound(null, v.getX(), v.getY(), v.getZ(), (drink ? SoundEvents.GENERIC_DRINK : SoundEvents.GENERIC_EAT).value(), SoundSource.NEUTRAL, .25F, .9F + v.getRandom().nextFloat() * .2F);
        var item = item(p.item);
        if (!drink && item != null) {
            var look = v.getLookAngle();
            level.sendParticles(new ItemParticleOption(ParticleTypes.ITEM, item), v.getX() + look.x * .3, v.getEyeY() - .25, v.getZ() + look.z * .3, 3, .05, .05, .05, .02);
        }
    }
    private static boolean cooking(ServerLevel level, House house) {
        for (var stove : house.tavern.stoves()) {
            var state = level.getBlockState(stove);
            if (state.hasProperty(dev.villagefriends.WorkstationBlock.LIT) && state.getValue(dev.villagefriends.WorkstationBlock.LIT)) return true;
        }
        return false;
    }
    static Item item(String id) {
        if (id == null) return null;
        var parsed = Identifier.tryParse(id);
        return parsed == null ? null : BuiltInRegistries.ITEM.getOptional(parsed).orElse(null);
    }

    // -- the bar -----------------------------------------------------------------------------------

    private static void tick(MinecraftServer server) {
        if (server.getTickCount() % 20 != 7) return;
        for (var it = houses.entrySet().iterator(); it.hasNext(); ) {
            var house = it.next().getValue();
            var level = server.getLevel(house.dimension);
            if (level == null) { it.remove(); continue; }
            long now = level.getGameTime();
            if (house.claims.isEmpty() && house.orders.isEmpty() && house.runners.values().stream().allMatch(r -> r.tray.isEmpty()) && now - house.used > FORGET) {
                stationKeys.values().removeIf(k -> k.equals(house.tavern.key())); it.remove(); continue;
            }
            if (now - house.surveyed > RESURVEY) resurvey(level, house, now);
            serve(level, house, now);
        }
        // Residents who wandered off, were unloaded or changed worlds give their seats back.
        var leaving = new ArrayList<Villager>();
        for (var it = patrons.values().iterator(); it.hasNext(); ) {
            var p = it.next(); var house = houses.get(p.tavern);
            var level = house == null ? null : server.getLevel(house.dimension);
            if (level != null && level.getEntity(p.id) instanceof Villager v && v.isAlive()) {
                // Recruited for an adventure or knocked out: their routine stops running, so give the seat back here.
                if (CompanionController.state(v).active() || Knockouts.injured(v)) leaving.add(v);
                continue;
            }
            if (house != null) { release(house, p); house.orders.removeIf(o -> o.patron().equals(p.id)); }
            it.remove();
        }
        leaving.forEach(Taverns::leave);
    }
    private static void resurvey(ServerLevel level, House house, long now) {
        var fresh = TavernSurvey.survey(level, house.tavern.stations().getFirst());
        house.surveyed = now;
        if (!fresh.key().equals(house.tavern.key())) return;
        house.tavern = fresh;
        for (var s : fresh.stations()) stationKeys.put(GlobalPos.of(level.dimension(), s), fresh.key());
    }
    /**
     * The staff work through the orders. The keeper goes to the bar, serves anyone waiting at the counter
     * straight away, then carries a tray of up to three orders out to tables close together, nearest first,
     * and wipes down tables people have left when nobody is waiting. The cook, while the stove is going,
     * brings dishes out from the kitchen the same way. Anyone kept waiting too long helps themselves.
     */
    private static void serve(ServerLevel level, House house, long now) {
        house.orders.removeIf(o -> !waiting(o.patron()));
        var staff = staff(level, house);
        // Staff who went off duty put their trays back on the order book.
        for (var it = house.runners.values().iterator(); it.hasNext(); ) {
            var r = it.next();
            if (staff.stream().noneMatch(v -> v.getUUID().equals(r.id))) { stopCarrying(level, house, r); stopWiping(level, r); it.remove(); }
        }
        Villager keeper = null;
        for (var v : staff) if (!cook(v)) { keeper = v; break; }
        for (var it = house.orders.iterator(); it.hasNext(); ) {
            var o = it.next();
            if (now - o.placed() >= (staff.isEmpty() ? Patronage.selfService(o.roll()) : patience(o))) { it.remove(); served(level, house, o, keeper, now); }
        }
        for (var v : staff) run(level, house, house.runners.computeIfAbsent(v.getUUID(), id -> new Runner(id, cook(v))), v, now);
    }
    /** How long someone waits for a busy keeper before fetching it themselves: not long in the lunch hour. */
    private static int patience(Order o) {
        var p = patrons.get(o.patron());
        return p == null ? LONG_WAIT : p.block == Block.LUNCH_TAVERN ? LONG_WAIT / 2 : p.block == Block.SUPPER_TAVERN ? LONG_WAIT * 2 / 3 : LONG_WAIT;
    }
    private static void run(ServerLevel level, House house, Runner r, Villager v, long now) {
        r.tray.removeIf(o -> !waiting(o.patron()));
        if (r.tray.isEmpty()) {
            if (r.carrying) stopCarrying(level, house, r);
            Order first = null;
            for (var o : house.orders) if (!r.cook || !Patronage.drink(o.item())) { first = o; break; }
            if (first == null) {
                if (r.cook) return;
                tidy(level, house, r, v, now);
                // A keeper with nothing to do minds the bar instead of wandering the house.
                var bar = house.tavern.stations().getFirst();
                if (r.wiping == null && !v.position().closerThan(Vec3.atCenterOf(bar), 5)) ResidentRoutines.walk(v, bar, .5F, 1);
                return;
            }
            stopWiping(level, r);
            house.orders.remove(first);
            r.tray.add(first); r.carrying = false; r.since = now;
        }
        if (now - r.since > CARRY_TIMEOUT) {
            for (var o : List.copyOf(r.tray)) served(level, house, o, v, now);
            r.tray.clear(); stopCarrying(level, house, r);
            return;
        }
        if (!r.carrying) {
            var pickup = r.cook ? stove(house, v) : station(level, house, r.tray.getFirst().item());
            if (!v.position().closerThan(Vec3.atCenterOf(pickup), 2.4)) { ResidentRoutines.walk(v, pickup, .6F, 1); return; }
            // Over the counter to whoever is waiting right there.
            if (!r.cook) for (var it = house.orders.iterator(); it.hasNext(); ) {
                var o = it.next();
                if (level.getEntity(o.patron()) instanceof Villager w && !Seat.seated(w) && w.distanceTo(v) < 3.5) { it.remove(); served(level, house, o, v, now); }
            }
            var first = r.tray.getFirst();
            if (level.getEntity(first.patron()) instanceof Villager w && w.distanceTo(v) < 3.5) { served(level, house, first, v, now); r.tray.clear(); stopCarrying(level, house, r); return; }
            // Load the tray with orders for tables near the first one.
            var near = level.getEntity(first.patron());
            for (var it = house.orders.iterator(); it.hasNext() && r.tray.size() < TRAY; ) {
                var o = it.next();
                if (r.cook && Patronage.drink(o.item())) continue;
                if (near != null && level.getEntity(o.patron()) instanceof Villager w && w.distanceTo(near) < 6) { it.remove(); r.tray.add(o); }
            }
            r.carrying = true;
            target(v).setAttached(STATE, Patronage.state(Phase.CARRY, first.item()));
            level.playSound(null, pickup, Patronage.drink(first.item()) ? SoundEvents.BOTTLE_FILL : SoundEvents.BUNDLE_INSERT, SoundSource.BLOCKS, .6F, 1.1F);
            return;
        }
        // Out to the tables, nearest first.
        Order next = null; Villager patron = null; double best = Double.MAX_VALUE;
        for (var o : r.tray) if (level.getEntity(o.patron()) instanceof Villager w && w.distanceToSqr(v) < best) { best = w.distanceToSqr(v); next = o; patron = w; }
        if (next == null) { r.tray.clear(); stopCarrying(level, house, r); return; }
        if (v.distanceTo(patron) < 2.3) {
            v.getLookControl().setLookAt(patron);
            served(level, house, next, v, now);
            r.tray.remove(next);
            if (r.tray.isEmpty()) stopCarrying(level, house, r);
            else target(v).setAttached(STATE, Patronage.state(Phase.CARRY, r.tray.getFirst().item()));
        } else ResidentRoutines.walk(v, patron.blockPosition(), .6F, 1);
    }
    /** With nobody waiting, the keeper wipes down the places people have just left. */
    private static void tidy(ServerLevel level, House house, Runner r, Villager keeper, long now) {
        if (r.wiping == null) {
            while (!house.dirty.isEmpty() && house.claims.containsKey(house.dirty.peekFirst())) house.dirty.pollFirst();
            r.wiping = house.dirty.pollFirst();
            if (r.wiping == null) return;
            r.wipedAt = 0;
        }
        if (r.wipedAt == 0) {
            if (keeper.position().closerThan(Vec3.atCenterOf(r.wiping), 2.2)) {
                r.wipedAt = now + 100;
                keeper.getLookControl().setLookAt(Vec3.atCenterOf(r.wiping.relative(Direction.fromYRot(seatYaw(house, r.wiping)))));
                target(keeper).setAttached(STATE, Patronage.state(Phase.WIPE, null));
            } else ResidentRoutines.walk(keeper, r.wiping, .5F, 1);
        } else if (now >= r.wipedAt) stopWiping(level, r);
    }
    private static float seatYaw(House house, BlockPos seat) { var s = house.tavern.seat(seat); return s == null ? 0 : s.yaw(); }
    private static void stopWiping(ServerLevel level, Runner r) {
        if (r.wiping == null) return;
        if (level.getEntity(r.id) instanceof Villager keeper && Patronage.phase(target(keeper).getAttached(STATE)) == Phase.WIPE) target(keeper).removeAttached(STATE);
        r.wiping = null; r.wipedAt = 0;
    }
    private static void stopCarrying(ServerLevel level, House house, Runner r) {
        if (level.getEntity(r.id) instanceof Villager v && Patronage.phase(target(v).getAttached(STATE)) == Phase.CARRY) target(v).removeAttached(STATE);
        // Anything still on the tray goes back on the order book.
        for (var o : r.tray) if (waiting(o.patron())) house.orders.addFirst(o);
        r.tray.clear(); r.carrying = false;
    }
    /** The order arrives: a dish set down in front of them, or a mug of cider or coffee drawn from the bar's own stock. */
    private static void served(ServerLevel level, House house, Order order, Villager keeper, long now) {
        var p = patrons.get(order.patron());
        if (p == null || p.phase != Phase.WAIT || !(level.getEntity(order.patron()) instanceof Villager v)) return;
        String item = order.item();
        if (Patronage.drink(item)) {
            var tap = drinkStation(level, house, item);
            if (tap != null && !Workstations.pour(level, tap)) {
                // Run dry: the keeper taps a fresh barrel; without one there's nothing to pour.
                if (keeper != null) { Workstations.restock(level, tap, 4); Workstations.pour(level, tap); }
                else {
                    // Nothing to pour until the keeper is back: they'll try again in a little while.
                    p.course--; p.phase = Phase.DONE; p.until = now + 400;
                    target(v).setAttached(STATE, Patronage.state(Phase.DONE, null)); VillageSocieties.emote(v, Emote.SWEAT, 0);
                    return;
                }
            }
        }
        p.phase = Patronage.drink(item) ? Phase.DRINK : Phase.EAT; p.item = item;
        p.until = now + Patronage.duration(item, order.roll());
        target(v).setAttached(STATE, Patronage.state(p.phase, item));
        level.playSound(null, v.getX(), v.getY(), v.getZ(), Patronage.drink(item) ? SoundEvents.DECORATED_POT_INSERT : SoundEvents.WOOD_PLACE, SoundSource.NEUTRAL, .45F, 1.2F);
        if (keeper != null && v.getRandom().nextInt(3) == 0) VillageSocieties.emote(v, v.getRandom().nextBoolean() ? Emote.NOTE : Emote.SPARKLE, 6);
    }
    private static boolean waiting(UUID id) { var p = patrons.get(id); return p != null && p.phase == Phase.WAIT; }
    /**
     * The staff on duty here: tavern keepers keeping one of this tavern's stations (or between job sites, inside
     * it), then the cook while the kitchen stove is going. At work, awake and not sitting down.
     */
    private static List<Villager> staff(ServerLevel level, House house) {
        var box = house.tavern.box();
        var area = new AABB(box.minX(), box.minY(), box.minZ(), box.maxX() + 1, box.maxY() + 1, box.maxZ() + 1).inflate(8);
        var keepers = new ArrayList<Villager>(); Villager cook = null;
        boolean kitchen = cooking(level, house);
        for (var v : level.getEntitiesOfClass(Villager.class, area, Taverns::onDuty)) {
            var site = v.getBrain().getMemory(MemoryModuleType.JOB_SITE).filter(g -> g.dimension() == level.dimension()).map(GlobalPos::pos).orElse(null);
            boolean here = site == null ? house.tavern.contains(v.blockPosition()) : cook(v) ? house.tavern.stoves().contains(site) : house.tavern.stations().contains(site);
            if (!here) continue;
            if (!cook(v)) keepers.add(v);
            else if (kitchen && cook == null) cook = v;
        }
        if (cook != null) keepers.add(cook);
        return keepers;
    }
    private static boolean cook(Villager v) { return profession(v).equals("cook"); }
    private static boolean onDuty(Villager v) {
        String job = profession(v);
        return (job.equals("tavern_keeper") || job.equals("cook")) && v.isAlive() && !v.isSleeping() && !Seat.seated(v) && !Knockouts.injured(v)
                && Block.WORK.id().equals(target(v).getAttached(ROUTINE)) && !CompanionController.state(v).active();
    }
    /** The kitchen stove nearest the cook. */
    private static BlockPos stove(House house, Villager cook) {
        BlockPos best = house.tavern.stations().getFirst(); double distance = Double.MAX_VALUE;
        for (var s : house.tavern.stoves()) if (s.distSqr(cook.blockPosition()) < distance) { distance = s.distSqr(cook.blockPosition()); best = s; }
        return best;
    }
    /** Where the keeper fetches an order: the drinks barrel for cider, the tap stand for coffee, the nearest station for food. */
    private static BlockPos station(ServerLevel level, House house, String item) {
        var tap = Patronage.drink(item) ? drinkStation(level, house, item) : null;
        return tap != null ? tap : house.tavern.stations().getFirst();
    }
    private static BlockPos drinkStation(ServerLevel level, House house, String item) {
        var block = VillageBlocks.get(item.equals(Patronage.COFFEE) ? "tap_stand" : "drinks_barrel");
        for (var s : house.tavern.stations()) if (level.getBlockState(s).is(block)) return s;
        return null;
    }
    /** Whether this resident is one of the staff carrying an order out or wiping a table right now. */
    public static boolean serving(Villager v) {
        for (var house : houses.values()) { var r = house.runners.get(v.getUUID()); if (r != null && (!r.tray.isEmpty() || r.wiping != null)) return true; }
        return false;
    }
    /** The vanilla activity a resident should be in: staff carrying an order walk freely instead of working at their station. */
    public static Activity activity(Villager v, Activity planned) { return serving(v) ? Activity.IDLE : planned; }

    // -- the stage ---------------------------------------------------------------------------------

    /** The bard plays the tavern from the stage, one song after another. */
    private static void perform(Villager v, ServerLevel level, House house, Patron p, long now) {
        if (Seat.seated(v)) v.stopRiding();
        var stage = house.tavern.stage();
        if (p.stand == null) {
            var near = stage != null ? beside(level, stage) : null;
            if (near == null && !house.tavern.standing().isEmpty()) near = house.tavern.standing().getLast().pos();
            if (near == null) near = house.tavern.stations().getFirst();
            p.stand = near; p.progressAt = now;
        }
        var center = Vec3.atBottomCenterOf(p.stand);
        if (v.position().distanceToSqr(center.x, v.getY(), center.z) > 1.5 * 1.5) { ResidentRoutines.walk(v, p.stand, .55F, 0); return; }
        var box = house.tavern.box();
        v.getLookControl().setLookAt(box.getCenter().getX() + .5, v.getEyeY(), box.getCenter().getZ() + .5);
        if (now >= p.until) p.until = now + Workstations.serenade(level, stage != null ? stage : v.blockPosition(), v.getRandom()) + 120 + v.getRandom().nextInt(200);
    }
    private static BlockPos beside(ServerLevel level, BlockPos pos) {
        for (var d : Direction.Plane.HORIZONTAL) for (int dy = -1; dy <= 1; dy++) {
            var cell = pos.relative(d).above(dy);
            if (TavernSurvey.floor(level, cell)) return cell;
        }
        return null;
    }

    // -- seats -------------------------------------------------------------------------------------

    /** Not panicking, caught up in a raid or hiding from one. */
    private static boolean calm(Villager v) {
        var activity = v.getBrain().getActiveNonCoreActivity().orElse(null);
        return activity != Activity.PANIC && activity != Activity.RAID && activity != Activity.PRE_RAID && activity != Activity.HIDE;
    }
    /** Whether a resident sitting at the tavern should stay seated: not hurt, frightened, knocked out, recruited or off somewhere else. */
    public static boolean mayStaySeated(Villager v) {
        if (!v.isAlive() || v.isSleeping() || Knockouts.injured(v) || v.hurtTime > 0 || CompanionController.state(v).active() || !calm(v)) return false;
        String routine = target(v).getAttached(ROUTINE);
        // Right after loading, before their day is worked out again, keep them where they are.
        return routine == null || Routine.atTavern(Block.byId(routine));
    }
    /** Whether a seat entity at this block still has something to sit on. */
    static boolean seat(ServerLevel level, BlockPos pos) { return TavernSurvey.seat(level, pos); }

    /** Players sit on tavern furniture and benches (and stair chairs at a table) with an empty hand. */
    private static InteractionResult use(Player player, Level level, InteractionHand hand, BlockHitResult hit) {
        if (hand != InteractionHand.MAIN_HAND || player.isShiftKeyDown() || player.isSpectator() || player.isPassenger() || !player.getMainHandItem().isEmpty())
            return InteractionResult.PASS;
        var pos = hit.getBlockPos(); var state = level.getBlockState(pos);
        var spot = TavernSurvey.seatAt(level, pos, state);
        if (spot == null) {
            if (!TavernSurvey.sittable(state)) return InteractionResult.PASS;
            spot = new Spot(pos, state.getValue(HorizontalDirectionalBlock.FACING).toYRot(), TavernSurvey.surface(state), null, -1, false, false);
        }
        if (!level.getBlockState(pos.above()).getCollisionShape(level, pos.above()).isEmpty()) return InteractionResult.PASS;
        if (level.isClientSide()) return InteractionResult.SUCCESS;
        if (player.distanceToSqr(Vec3.atCenterOf(pos)) > 9 || Seat.occupied(level, pos)) return InteractionResult.PASS;
        return Seat.sit(player, pos, spot.surface(), spot.yaw()) ? InteractionResult.SUCCESS_SERVER : InteractionResult.PASS;
    }

    // -- leaving -----------------------------------------------------------------------------------

    /** Their time at the tavern is up: they get up, give their seat back and cancel anything still on order. */
    public static void leave(Villager v) {
        var p = patrons.remove(v.getUUID());
        if (Seat.seated(v)) v.stopRiding();
        if (!serving(v)) target(v).removeAttached(STATE);
        if (p == null) return;
        var house = houses.get(p.tavern);
        if (house == null) return;
        if (p.seat != null && p.course > 0 && house.dirty.size() < 12) house.dirty.add(p.seat);
        release(house, p);
        house.orders.removeIf(o -> o.patron().equals(v.getUUID()));
    }
    private static void forget(Villager v) {
        var p = patrons.remove(v.getUUID());
        if (p == null) return;
        var house = houses.get(p.tavern);
        if (house != null) { release(house, p); house.orders.removeIf(o -> o.patron().equals(v.getUUID())); }
    }
    private static void release(House house, Patron p) {
        house.claims.values().removeIf(id -> id.equals(p.id));
        p.stand = null;
    }

    // -- finding taverns ---------------------------------------------------------------------------

    private static House house(ServerLevel level, Villager v, Patron p) {
        if (p != null) { var known = houses.get(p.tavern); if (known != null) return known; }
        var station = ResidentRoutines.tavern(v, level);
        if (station == null) return null;
        var key = stationKeys.get(GlobalPos.of(level.dimension(), station));
        if (key != null && houses.containsKey(key)) return houses.get(key);
        var survey = TavernSurvey.survey(level, station);
        var house = houses.computeIfAbsent(survey.key(), k -> new House(level.dimension()));
        house.tavern = survey; house.surveyed = level.getGameTime();
        for (var s : survey.stations()) stationKeys.put(GlobalPos.of(level.dimension(), s), survey.key());
        stationKeys.put(GlobalPos.of(level.dimension(), station.immutable()), survey.key());
        return house;
    }
    /** The tavern a block belongs to, for tests and the conversation window; null if it isn't in one we know. */
    public static Tavern tavernAt(ServerLevel level, BlockPos pos) {
        for (var house : houses.values()) if (house.dimension == level.dimension() && house.tavern.contains(pos)) return house.tavern;
        return null;
    }
    /** How many residents are sitting, standing and waiting at a tavern, for tests and the ledger. */
    public static int[] census(Tavern tavern) {
        var house = houses.get(tavern.key());
        if (house == null) return new int[]{0, 0, 0};
        int seated = 0, standing = 0, waiting = 0;
        for (var p : patrons.values()) {
            if (!p.tavern.equals(tavern.key())) continue;
            if (p.seat != null) seated++; else if (p.stand != null) standing++;
            if (p.phase == Phase.WAIT) waiting++;
        }
        return new int[]{seated, standing, waiting};
    }

    /** Everything the tavern knows right now, one line per tavern and patron, for tests and debugging. */
    public static String describe(ServerLevel level) {
        var out = new StringBuilder();
        for (var house : houses.values()) {
            if (house.dimension != level.dimension()) continue;
            var t = house.tavern;
            out.append("tavern ").append(t.key()).append(": ").append(t.seats().size()).append(" seats, ").append(t.standing().size()).append(" standing, stations ")
                    .append(t.stations()).append(", stoves ").append(t.stoves()).append(", ").append(house.orders.size()).append(" orders, serving ")
                    .append(house.runners.values().stream().map(r -> r.tray.size() + (r.cook ? " (cook" : " (keeper") + (r.carrying ? ", carrying)" : ")")).toList()).append(System.lineSeparator());
            var box = t.box();
            for (var v : level.getEntitiesOfClass(Villager.class, new AABB(box.minX(), box.minY(), box.minZ(), box.maxX() + 1, box.maxY() + 1, box.maxZ() + 1).inflate(8),
                    v -> profession(v).equals("tavern_keeper") || cook(v)))
                out.append("  keeper ").append(name(v)).append(" routine=").append(target(v).getAttached(ROUTINE)).append(" site=")
                        .append(v.getBrain().getMemory(MemoryModuleType.JOB_SITE).map(g -> g.pos().toShortString()).orElse("none"))
                        .append(" activity=").append(v.getBrain().getActiveNonCoreActivity().map(Object::toString).orElse("-"))
                        .append(" onDuty=").append(onDuty(v)).append(" at ").append(v.blockPosition().toShortString()).append(System.lineSeparator());
        }
        for (var p : patrons.values()) {
            if (!(level.getEntity(p.id) instanceof Villager v)) continue;
            out.append("  patron ").append(name(v)).append(' ').append(p.block).append(" phase=").append(p.phase).append(" item=").append(p.item)
                    .append(" course=").append(p.course).append(" seat=").append(p.seat == null ? "-" : p.seat.toShortString())
                    .append(" stand=").append(p.stand == null ? "-" : p.stand.toShortString()).append(" seated=").append(Seat.seated(v))
                    .append(" state=").append(target(v).getAttached(STATE)).append(System.lineSeparator());
        }
        return out.toString();
    }

    /** "Lunch at the tavern · eating shepherds pie" for the conversation window. */
    public static String doing(Villager v, String label) {
        String state = target(v).getAttached(STATE);
        var phase = Patronage.phase(state);
        if (phase == null) return label;
        String item = Patronage.item(state), name = item == null ? null : itemName(item);
        return switch (phase) {
            case WAIT -> label + " · waiting to be served";
            case EAT -> label + " · eating " + name;
            case DRINK -> label + " · drinking " + name.replace("mug of ", "").replace("steaming ", "").replace(" mug", "");
            case CARRY -> label + " · serving " + name;
            case WIPE -> label + " · wiping a table";
            case DONE -> label;
        };
    }

    private Taverns() {}
}
