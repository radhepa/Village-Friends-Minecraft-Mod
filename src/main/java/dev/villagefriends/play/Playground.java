package dev.villagefriends.play;

import static dev.villagefriends.VillageFriends.*;

import dev.villagefriends.CompanionController;
import dev.villagefriends.Emote;
import dev.villagefriends.Knockouts;
import dev.villagefriends.VillageBlocks;
import dev.villagefriends.VillageSocieties;
import dev.villagefriends.play.Games.Game;
import dev.villagefriends.play.Games.Move;
import dev.villagefriends.routine.Routine;
import dev.villagefriends.routine.Routine.Block;
import java.util.ArrayList;
import java.util.Comparator;
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
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerEntityEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.GlobalPos;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.ai.memory.MemoryModuleType;
import net.minecraft.world.entity.ai.util.LandRandomPos;
import net.minecraft.world.entity.monster.Enemy;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.schedule.Activity;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;

/**
 * Children at play. Once a second {@code ResidentRoutines} asks about every resident; a child with free time
 * plays on their own (vanilla's play) until they get bored ({@link Games#boredAfter}), then rounds up the
 * children nearby for a game, joins one already going, or, now and then, tags along behind a player to see
 * what they're doing. While a child is in a game the playground drives them every tick (their brain rests,
 * see {@code VillagerCompanionMixin}) and shares their part through {@link #STATE} for animation and the ball.
 *
 * <p>Games end when their time is up, when a child's free time ends (lessons, supper, rain), or the moment
 * anything frightening happens nearby: a monster, a raid, a child getting hurt. Then vanilla takes over again.
 * Nothing here is saved; a game in progress simply stops when the world is closed.
 */
public final class Playground {
    /** A child's part in a game ({@code tag:it}, {@code catch:throw:42}, {@code curious:watch}...), shared with clients. */
    public static final AttachmentType<String> STATE = AttachmentRegistry.create(VillageBlocks.id("play"),
            b -> b.syncWith(ByteBufCodecs.STRING_UTF8, AttachmentSyncPredicate.all()));

    /** Ticks a thrown ball spends in the thrower's hand after the throw starts, and in the air. The clients use the same numbers. */
    public static final int RELEASE = 12, FLIGHT = 16;

    private static final class Kid { int bored; long restUntil; Game last; }
    private static final Map<UUID, Kid> kids = new HashMap<>();
    private static final Map<UUID, Session> sessionOf = new HashMap<>();
    private static final List<Session> sessions = new ArrayList<>();

    public static void register() {
        ServerTickEvents.END_SERVER_TICK.register(Playground::tick);
        ServerEntityEvents.ENTITY_UNLOAD.register((entity, level) -> { if (entity instanceof Villager v) unload(v); });
        ServerLifecycleEvents.SERVER_STOPPED.register(server -> clear());
    }
    public static void clear() { kids.clear(); sessionOf.clear(); sessions.clear(); }
    private static void unload(Villager v) {
        var s = sessionOf.remove(v.getUUID());
        if (s != null) { s.members.remove(v.getUUID()); s.left(v.getUUID()); }
        target(v).removeAttached(STATE);
        kids.remove(v.getUUID());
    }

    /** Called away mid-game (an alarm): they leave their game at once; it carries on without them, or ends. */
    public static void excuse(Villager v) {
        var s = sessionOf.get(v.getUUID());
        if (s != null) leave(s, v.getUUID(), v, s.level.getGameTime());
    }
    /** In a game or tagging along after a player: the playground moves them, not their brain. */
    public static boolean busy(Villager v) { return sessionOf.containsKey(v.getUUID()); }
    /** "Playing tag", "Hiding"... or null when not in a game. */
    public static String doing(Villager v) { return Games.doing(target(v).getAttached(STATE)); }

    /** Parts of a child's day when they're free to play. */
    static boolean free(Block block) {
        return block == Block.PLAY || block == Block.SNOW_PLAY || block == Block.RAIN_WALK || block == Block.MARKET;
    }

    // -- once a second, from ResidentRoutines ---------------------------------------------------------

    /** Lets a child get bored and start (or join) something; true while the playground is looking after them. */
    public static boolean update(Villager v, ServerLevel level, Routine.Plan plan) {
        if (busy(v)) return true;
        if (target(v).hasAttached(STATE)) target(v).removeAttached(STATE);
        if (!v.isBaby()) return false;
        var kid = kids.computeIfAbsent(v.getUUID(), id -> new Kid());
        long now = level.getGameTime();
        if (!free(plan.block()) || !calm(v) || v.isSleeping()) { kid.bored = 0; return false; }
        if (now < kid.restUntil) return false;
        String personality = profile(v).personality();
        if (++kid.bored < Games.boredAfter(personality)) return false;
        // Bored. Is there a game going they can join?
        for (var s : sessions) {
            if (s.game == null || s.level != level || s.members.size() >= s.game.max || s.center.distSqr(v.blockPosition()) > 18 * 18) continue;
            if (s.join(v, now)) { enlist(s, v); VillageSocieties.emote(v, Emote.EXCLAIM, 0); return true; }
        }
        var mates = playmates(v, level, now);
        var player = interesting(v, level);
        if (player != null && v.getRandom().nextInt(100) < Games.curiosity(personality, !mates.isEmpty())) {
            var s = new Curious(level, v, player, now);
            sessions.add(s); enlist(s, v); s.begin(now);
            VillageSocieties.emote(v, Emote.QUESTION, 0);
            return true;
        }
        if (!mates.isEmpty()) {
            var group = new ArrayList<Villager>(); group.add(v); group.addAll(mates);
            var personalities = new ArrayList<String>();
            for (var g : group) personalities.add(profile(g).personality());
            var game = Games.choose(group.size(), personalities, kid.last, new Random(v.getRandom().nextLong()));
            if (game != null) {
                while (group.size() > game.max) group.removeLast();
                start(game, level, group, now);
                return true;
            }
        }
        // Nobody to play with: try again in a little while.
        kid.bored = Games.boredAfter(personality) / 2;
        return false;
    }
    /** Starts a game straight away with these children, taking them out of whatever they were playing (for tests). */
    public static void play(Game game, List<Villager> group) {
        if (group.isEmpty() || !(group.getFirst().level() instanceof ServerLevel level)) return;
        long now = level.getGameTime();
        for (var v : group) { var old = sessionOf.get(v.getUUID()); if (old != null) end(old, now); }
        start(game, level, List.copyOf(group), now);
    }
    /** Sends a child off to follow a player around right away (for tests). */
    public static void follow(Villager v, Player player) {
        if (!(v.level() instanceof ServerLevel level)) return;
        long now = level.getGameTime();
        var old = sessionOf.get(v.getUUID());
        if (old != null) end(old, now);
        var s = new Curious(level, v, player, now);
        sessions.add(s); enlist(s, v); s.begin(now);
    }
    /** Other children nearby who are free to play, nearest first. */
    private static List<Villager> playmates(Villager v, ServerLevel level, long now) {
        var found = new ArrayList<Villager>();
        for (var other : CompanionController.loaded) {
            if (other == v || other.level() != level || !other.isBaby() || busy(other) || other.distanceToSqr(v) > 16 * 16) continue;
            if (!other.isAlive() || other.isSleeping() || !calm(other) || !fit(other)) continue;
            var kid = kids.get(other.getUUID());
            if (kid != null && now < kid.restUntil) continue;
            found.add(other);
        }
        found.sort(Comparator.comparingDouble(o -> o.distanceToSqr(v)));
        return found;
    }
    /** The nearest player a child can see who isn't already being followed by three other children. */
    private static Player interesting(Villager v, ServerLevel level) {
        Player best = null; double bestDistance = 12 * 12;
        for (var p : level.players()) {
            if (!p.isAlive() || p.isSpectator() || p.isPassenger()) continue;
            double d = p.distanceToSqr(v);
            if (d >= bestDistance || !v.hasLineOfSight(p)) continue;
            int following = 0;
            for (var s : sessions) if (s instanceof Curious c && c.player.equals(p.getUUID())) following++;
            if (following >= 3) continue;
            best = p; bestDistance = d;
        }
        return best;
    }
    private static void start(Game game, ServerLevel level, List<Villager> group, long now) {
        var center = middle(group);
        Session s = switch (game) {
            case TAG -> new Tag(level, center, now);
            case HIDE_AND_SEEK -> new HideAndSeek(level, center, now);
            case RING -> new Ring(level, center, now);
            case FOLLOW_THE_LEADER -> new FollowTheLeader(level, center, now);
            case CATCH -> new Catch(level, center, now);
        };
        sessions.add(s);
        for (var v : group) enlist(s, v);
        s.begin(now);
        // Whoever had the idea is excited about it.
        VillageSocieties.emote(group.getFirst(), Emote.IDEA, 0);
        for (int i = 1; i < group.size(); i++) VillageSocieties.emote(group.get(i), Emote.EXCLAIM, 6 + i * 4);
    }
    private static void enlist(Session s, Villager v) {
        if (!s.members.contains(v.getUUID())) s.members.add(v.getUUID());
        sessionOf.put(v.getUUID(), s);
        v.getBrain().eraseMemory(MemoryModuleType.WALK_TARGET);
        v.getBrain().eraseMemory(MemoryModuleType.LOOK_TARGET);
        v.getNavigation().stop();
    }
    /** Where the group stands, on average: the middle of the playground. */
    private static BlockPos middle(List<Villager> group) {
        double x = 0, y = 0, z = 0;
        for (var v : group) { x += v.getX(); y += v.getY(); z += v.getZ(); }
        return BlockPos.containing(x / group.size(), y / group.size(), z / group.size());
    }

    // -- every tick ---------------------------------------------------------------------------------

    private static void tick(MinecraftServer server) {
        for (var s : List.copyOf(sessions)) {
            long now = s.level.getGameTime();
            boolean check = now % 20 == 0;
            if (check && danger(s)) { end(s, now); continue; }
            var present = new ArrayList<Villager>();
            for (var id : List.copyOf(s.members)) {
                var e = s.level.getEntity(id);
                if (e instanceof Villager v && fit(v) && v.position().distanceToSqr(Vec3.atBottomCenterOf(s.center)) < 40 * 40 && (!check || calm(v))) present.add(v);
                else leave(s, id, e instanceof Villager v ? v : null, now);
            }
            if (s.done || now >= s.until || present.size() < s.minimum()) { end(s, now); continue; }
            s.step(now, present);
        }
    }
    /** Still able to play: awake, unhurt, free and not off on some other business. */
    private static boolean fit(Villager v) {
        if (!v.isAlive() || v.isRemoved() || !v.isBaby() || v.isSleeping() || v.isPassenger() || v.hurtTime > 0 || v.isNoAi()) return false;
        if (Knockouts.knockedOut(v) || CompanionController.state(v).active()) return false;
        var block = Block.byId(target(v).getAttached(ROUTINE));
        return block == null || free(block);
    }
    /** Not panicking, caught up in a raid or hiding from one, and not just hurt. */
    private static boolean calm(Villager v) {
        var activity = v.getBrain().getActiveNonCoreActivity().orElse(null);
        return activity != Activity.PANIC && activity != Activity.RAID && activity != Activity.PRE_RAID && activity != Activity.HIDE
                && !v.getBrain().hasMemoryValue(MemoryModuleType.HURT_BY);
    }
    /** A monster close by or a raid on the village: games stop and everyone runs home. */
    private static boolean danger(Session s) {
        if (s.level.isRaided(s.center) || dev.villagefriends.VillageAlarm.raised(s.level, s.center)) return true;
        var box = new net.minecraft.world.phys.AABB(s.center).inflate(16, 6, 16);
        return !s.level.getEntitiesOfClass(Mob.class, box, m -> m instanceof Enemy && m.isAlive()).isEmpty();
    }
    private static void leave(Session s, UUID id, Villager v, long now) {
        s.members.remove(id);
        sessionOf.remove(id);
        s.left(id);
        if (v != null) release(v, s, now);
    }
    private static void end(Session s, long now) {
        sessions.remove(s);
        for (var id : List.copyOf(s.members)) {
            sessionOf.remove(id);
            if (s.level.getEntity(id) instanceof Villager v) release(v, s, now);
        }
        s.members.clear();
    }
    /** Back to their own devices: a breather before they can get bored again. */
    private static void release(Villager v, Session s, long now) {
        target(v).removeAttached(STATE);
        v.getNavigation().stop();
        v.getBrain().eraseMemory(MemoryModuleType.WALK_TARGET);
        v.getBrain().eraseMemory(MemoryModuleType.LOOK_TARGET);
        var kid = kids.computeIfAbsent(v.getUUID(), id -> new Kid());
        kid.bored = 0; kid.restUntil = now + Games.restAfter(s.random);
        if (s.game != null) kid.last = s.game;
    }

    // -- sessions -----------------------------------------------------------------------------------

    /** One game (or one child following a player), with the children taking part. */
    private abstract static class Session {
        final ServerLevel level; final Game game; final List<UUID> members = new ArrayList<>(); final Random random;
        BlockPos center; final long started; long until; boolean done;
        Session(ServerLevel level, Game game, BlockPos center, long now) {
            this.level = level; this.game = game; this.center = center; this.started = now;
            this.random = new Random(now * 31 + center.asLong());
            this.until = now + (game == null ? 1200 : game.length + random.nextInt(game.length / 2));
        }
        int minimum() { return game == null ? 1 : game.min; }
        /** Sets the game up once the first children are enlisted. */
        abstract void begin(long now);
        abstract void step(long now, List<Villager> kids);
        /** A bored child asks to join in; true if they're let in (and given a part). */
        boolean join(Villager v, long now) { return false; }
        /** A child dropped out (tired, hurt, called home). */
        void left(UUID id) {}

        Villager kid(UUID id) { return id != null && level.getEntity(id) instanceof Villager v && members.contains(id) ? v : null; }
        Vec3 middle() { return Vec3.atBottomCenterOf(center); }
        void set(Villager v, String role) {
            String state = game == null ? Games.curious(role) : Games.state(game, role);
            if (!state.equals(target(v).getAttached(STATE))) target(v).setAttached(STATE, state);
        }
        String role(Villager v) { return Games.role(target(v).getAttached(STATE)); }
    }

    // -- moving children about ----------------------------------------------------------------------

    /** Walks toward a spot: pathfinding when it's far, a straight little step when it's close. */
    private static void go(Villager v, Vec3 to, double speed) {
        double dx = to.x - v.getX(), dz = to.z - v.getZ(), flat = dx * dx + dz * dz;
        if (flat < .3 * .3) { halt(v); return; }
        if (flat < 2.2 * 2.2 && Math.abs(to.y - v.getY()) < .8) {
            v.getNavigation().stop();
            v.getMoveControl().setWantedPosition(to.x, v.getY(), to.z, speed);
            return;
        }
        if (v.getNavigation().isDone() || (v.tickCount & 7) == 0) v.getNavigation().moveTo(to.x, to.y, to.z, speed);
    }
    private static void chase(Villager v, Entity target, double speed) {
        if (v.getNavigation().isDone() || (v.tickCount & 3) == 0) v.getNavigation().moveTo(target, speed);
    }
    private static void halt(Villager v) { v.getNavigation().stop(); v.getMoveControl().setWait(); }
    private static void face(Villager v, Entity e) { v.getLookControl().setLookAt(e, 30, 30); }
    private static void face(Villager v, Vec3 at) { v.getLookControl().setLookAt(at.x, v.getEyeY(), at.z, 30, 30); }
    private static boolean near(Villager v, Vec3 to, double within) {
        double dx = to.x - v.getX(), dz = to.z - v.getZ();
        return dx * dx + dz * dz < within * within && Math.abs(to.y - v.getY()) < 1.5;
    }
    /** A spot a child can stand on: solid ground, room for them, no water. */
    private static boolean standable(ServerLevel level, BlockPos pos) {
        if (!level.isLoaded(pos)) return false;
        var below = pos.below();
        return level.getBlockState(below).isFaceSturdy(level, below, Direction.UP)
                && level.getBlockState(pos).getCollisionShape(level, pos).isEmpty() && level.getFluidState(pos).isEmpty()
                && level.getBlockState(pos.above()).getCollisionShape(level, pos.above()).isEmpty();
    }
    /** The standable spot nearest this height in the column at x, z, or null. */
    private static BlockPos ground(ServerLevel level, int x, int y, int z) {
        for (int dy : new int[]{0, 1, -1, 2, -2, 3, -3}) {
            var pos = new BlockPos(x, y + dy, z);
            if (standable(level, pos)) return pos;
        }
        return null;
    }
    /** An open patch near the playground where a ring (or a game of catch) of this radius fits. */
    private static BlockPos open(ServerLevel level, BlockPos around, double radius, Random random) {
        BlockPos best = around; int bestScore = -1;
        for (int i = 0; i < 18; i++) {
            var c = i == 0 ? ground(level, around.getX(), around.getY(), around.getZ())
                    : ground(level, around.getX() + random.nextInt(13) - 6, around.getY(), around.getZ() + random.nextInt(13) - 6);
            if (c == null) continue;
            int score = 0;
            for (int k = 0; k < 10; k++) {
                double a = k * Math.PI / 5;
                var p = ground(level, (int) Math.floor(c.getX() + .5 + Math.cos(a) * radius), c.getY(), (int) Math.floor(c.getZ() + .5 + Math.sin(a) * radius));
                if (p != null && Math.abs(p.getY() - c.getY()) <= 1) score++;
            }
            if (score > bestScore) { best = c; bestScore = score; }
            if (score == 10) break;
        }
        return best;
    }

    // -- tag ----------------------------------------------------------------------------------------

    private static final class Tag extends Session {
        static final double FIELD = 12;
        UUID it; long frozenUntil; final Map<UUID, Long> immune = new HashMap<>(); final Map<UUID, Long> repath = new HashMap<>();
        Tag(ServerLevel level, BlockPos center, long now) { super(level, Game.TAG, center, now); }
        @Override void begin(long now) {
            it = members.get(random.nextInt(members.size()));
            frozenUntil = now + 60;
        }
        @Override boolean join(Villager v, long now) { set(v, "run"); return true; }
        @Override void left(UUID id) { if (id.equals(it)) it = null; }
        @Override void step(long now, List<Villager> kids) {
            var chaser = kid(it);
            if (chaser == null) { chaser = kids.get(random.nextInt(kids.size())); it = chaser.getUUID(); frozenUntil = now + 40; set(chaser, "count"); }
            for (var v : kids) if (v != chaser) run(v, chaser, now);
            if (now < frozenUntil) {
                // Counting to three before giving chase.
                halt(chaser);
                if (!"tagged".equals(role(chaser))) set(chaser, "count");
                return;
            }
            set(chaser, "it");
            Villager prey = null; double best = Double.MAX_VALUE;
            for (var v : kids) {
                if (v == chaser || now < immune.getOrDefault(v.getUUID(), 0L)) continue;
                double d = v.distanceToSqr(chaser);
                if (d < best) { best = d; prey = v; }
            }
            if (prey == null) { halt(chaser); return; }
            face(chaser, prey);
            chase(chaser, prey, .82);
            if (best < 1.6 && Math.abs(prey.getY() - chaser.getY()) < 1) {
                chaser.swingForAttack(InteractionHand.MAIN_HAND);
                VillageSocieties.emote(prey, Emote.EXCLAIM, 0);
                VillageSocieties.emote(chaser, Emote.NOTE, 4);
                // No tagging straight back.
                immune.put(chaser.getUUID(), now + 80);
                set(chaser, "run"); repath.put(chaser.getUUID(), 0L);
                it = prey.getUUID(); frozenUntil = now + 40;
                halt(prey); set(prey, "tagged");
            }
        }
        private void run(Villager v, Villager chaser, long now) {
            set(v, "run");
            var middle = middle();
            boolean strayed = v.position().distanceToSqr(middle) > FIELD * FIELD;
            boolean close = v.distanceToSqr(chaser) < 7 * 7 && now >= frozenUntil;
            if (!strayed && !close) {
                // Safe for now: stop and taunt.
                if (v.getNavigation().isDone()) { halt(v); face(v, chaser); }
                return;
            }
            if (now < repath.getOrDefault(v.getUUID(), 0L) && !v.getNavigation().isDone()) return;
            Vec3 to = strayed ? LandRandomPos.getPosTowards(v, 8, 4, middle) : LandRandomPos.getPosAway(v, 8, 4, chaser.position());
            if (to != null && to.distanceToSqr(middle) > (FIELD + 2) * (FIELD + 2)) to = LandRandomPos.getPosTowards(v, 8, 4, middle);
            if (to != null) v.getNavigation().moveTo(to.x, to.y, to.z, .74);
            repath.put(v.getUUID(), now + 12 + random.nextInt(10));
        }
    }

    // -- hide-and-seek ------------------------------------------------------------------------------

    private static final class HideAndSeek extends Session {
        static final int COUNT = 220, SEEK = 1500, CHEER = 70;
        enum Phase { COUNT, SEEK, CHEER }
        Phase phase; long phaseAt, countFrom; UUID seeker, firstFound; Vec3 waypoint, facing;
        final Map<UUID, BlockPos> spots = new HashMap<>(); final Set<UUID> found = new HashSet<>();
        final Map<UUID, Long> busyUntil = new HashMap<>();
        HideAndSeek(ServerLevel level, BlockPos center, long now) { super(level, Game.HIDE_AND_SEEK, center, now); }
        @Override void begin(long now) { round(members.get(random.nextInt(members.size())), now); }
        private void round(UUID nextSeeker, long now) {
            seeker = nextSeeker; firstFound = null; found.clear(); spots.clear(); busyUntil.clear(); waypoint = null;
            phase = Phase.COUNT; phaseAt = now; countFrom = -1;
            var hiders = new ArrayList<Villager>();
            for (var id : members) { var v = kid(id); if (v != null && !id.equals(seeker)) hiders.add(v); }
            var places = hidingPlaces(hiders.isEmpty() ? null : hiders.getFirst(), hiders.size());
            for (int i = 0; i < hiders.size(); i++) spots.put(hiders.get(i).getUUID(), places.get(i));
            // The seeker counts facing away from where everyone goes.
            double fx = 0, fz = 0;
            for (var p : places) { fx += p.getX() - center.getX(); fz += p.getZ() - center.getZ(); }
            double len = Math.max(1e-3, Math.sqrt(fx * fx + fz * fz));
            facing = middle().add(-fx / len * 3, 1, -fz / len * 3);
        }
        @Override boolean join(Villager v, long now) {
            if (phase != Phase.COUNT) return false;
            var places = hidingPlaces(v, 1);
            spots.put(v.getUUID(), places.getFirst());
            return true;
        }
        @Override void left(UUID id) { if (id.equals(seeker)) seeker = null; spots.remove(id); found.remove(id); }
        @Override int minimum() { return 2; }
        @Override void step(long now, List<Villager> kids) {
            var seek = kid(seeker);
            if (seek == null) { round(kids.get(random.nextInt(kids.size())).getUUID(), now); return; }
            switch (phase) {
                case COUNT -> {
                    var base = middle();
                    if (countFrom < 0 && (near(seek, base, 1.5) || now - phaseAt > 120)) countFrom = now;
                    if (countFrom < 0) { go(seek, base, .6); set(seek, "seek"); }
                    else { halt(seek); face(seek, facing); set(seek, "count"); }
                    for (var v : kids) if (v != seek) hide(v, base);
                    if (countFrom >= 0 && now - countFrom >= COUNT) {
                        phase = Phase.SEEK; phaseAt = now;
                        VillageSocieties.emote(seek, Emote.EXCLAIM, 0);
                    }
                }
                case SEEK -> {
                    for (var v : kids) if (v != seek) {
                        if (found.contains(v.getUUID())) home(v, seek, now); else hide(v, middle());
                    }
                    if (now < busyUntil.getOrDefault(seeker, 0L)) { halt(seek); return; }
                    set(seek, "seek");
                    Villager spotted = null;
                    for (var v : kids) {
                        if (v == seek || found.contains(v.getUUID())) continue;
                        double d = v.distanceToSqr(seek);
                        if (d < 3.5 * 3.5 && seek.hasLineOfSight(v) || d < 6 * 6 && seek.hasLineOfSight(v) && random.nextInt(14) == 0) { spotted = v; break; }
                    }
                    if (spotted != null) {
                        found.add(spotted.getUUID());
                        if (firstFound == null) firstFound = spotted.getUUID();
                        halt(seek); face(seek, spotted); set(seek, "point");
                        busyUntil.put(seeker, now + 30);
                        VillageSocieties.emote(seek, Emote.EXCLAIM, 0);
                        VillageSocieties.emote(spotted, random.nextBoolean() ? Emote.SWEAT : Emote.NOTE, 8);
                        set(spotted, "found"); halt(spotted); face(spotted, seek);
                        busyUntil.put(spotted.getUUID(), now + 40);
                        waypoint = null;
                        return;
                    }
                    if (found.containsAll(spots.keySet()) || now - phaseAt > SEEK) {
                        for (var v : kids) if (v != seek && !found.contains(v.getUUID())) { set(v, "won"); VillageSocieties.emote(v, Emote.SPARKLE, random.nextInt(10)); }
                        phase = Phase.CHEER; phaseAt = now;
                        return;
                    }
                    search(seek, kids);
                }
                case CHEER -> {
                    for (var v : kids) {
                        if (v == seek) { go(seek, middle(), .55); if (near(seek, middle(), 2)) { halt(seek); set(seek, "home"); } continue; }
                        if (!"won".equals(role(v)) || now - phaseAt > 40) home(v, seek, now);
                    }
                    if (now - phaseAt > CHEER) {
                        if (until - now < 900) { done = true; return; }
                        // Whoever was found first counts next.
                        var next = firstFound != null && members.contains(firstFound) ? firstFound : members.get(random.nextInt(members.size()));
                        round(next, now);
                    }
                }
            }
        }
        /** Off to their hiding place, then keep still. */
        private void hide(Villager v, Vec3 base) {
            var spot = spots.get(v.getUUID());
            if (spot == null) { set(v, "hidden"); halt(v); return; }
            var to = Vec3.atBottomCenterOf(spot);
            if (near(v, to, .7)) { halt(v); face(v, base); set(v, "hidden"); }
            else { go(v, to, .72); set(v, "hide"); }
        }
        /** Found children go back to home base and watch the search. */
        private void home(Villager v, Villager seek, long now) {
            if (now < busyUntil.getOrDefault(v.getUUID(), 0L)) { halt(v); return; }
            var base = middle().add((v.getId() % 5 - 2) * .7, 0, (v.getId() % 3 - 1) * .7);
            if (near(v, base, 1.2)) { halt(v); face(v, seek); }
            else go(v, base, .6);
            if (!"won".equals(role(v))) set(v, "home");
        }
        /** The seeker wanders toward hiding places (and now and then somewhere nobody is), peering about. */
        private void search(Villager seek, List<Villager> kids) {
            if (waypoint == null || near(seek, waypoint, 1.2) || seek.getNavigation().isDone() && seek.tickCount % 40 == 0) {
                var hidden = new ArrayList<BlockPos>();
                for (var e : spots.entrySet()) if (!found.contains(e.getKey())) hidden.add(e.getValue());
                if (hidden.isEmpty() || random.nextInt(100) < 30) {
                    var p = LandRandomPos.getPosTowards(seek, 10, 4, middle());
                    waypoint = p != null ? p : middle();
                } else {
                    hidden.sort(Comparator.comparingDouble(p -> p.distToCenterSqr(seek.position())));
                    var spot = hidden.getFirst();
                    waypoint = Vec3.atBottomCenterOf(spot).add(random.nextInt(5) - 2, 0, random.nextInt(5) - 2);
                }
            }
            go(seek, waypoint, .56);
        }
        /** Hiding places around home base, behind something where possible, that a child can actually reach. */
        private List<BlockPos> hidingPlaces(Villager sample, int count) {
            record Candidate(BlockPos pos, double score) {}
            var eye = middle().add(0, 1.4, 0);
            var candidates = new ArrayList<Candidate>();
            for (int i = 0; i < 90; i++) {
                double a = random.nextDouble() * Math.PI * 2, d = 6 + random.nextDouble() * 10;
                var pos = ground(level, (int) Math.floor(center.getX() + .5 + Math.cos(a) * d), center.getY(), (int) Math.floor(center.getZ() + .5 + Math.sin(a) * d));
                if (pos == null) continue;
                var at = Vec3.atBottomCenterOf(pos).add(0, .8, 0);
                boolean behind = level.clip(new ClipContext(eye, at, ClipContext.Block.COLLIDER, ClipContext.Fluid.NONE, net.minecraft.world.phys.shapes.CollisionContext.empty())).getType() != HitResult.Type.MISS;
                boolean roofed = !level.canSeeSky(pos.above());
                int walls = 0;
                for (var dir : Direction.Plane.HORIZONTAL) if (!level.getBlockState(pos.relative(dir)).getCollisionShape(level, pos.relative(dir)).isEmpty()) walls++;
                candidates.add(new Candidate(pos, (behind ? 4 : 0) + (roofed ? 1.5 : 0) + Math.min(walls, 2) * .7 + d / 16 + random.nextDouble()));
            }
            candidates.sort(Comparator.comparingDouble(Candidate::score).reversed());
            var chosen = new ArrayList<BlockPos>();
            int tested = 0;
            for (var c : candidates) {
                if (chosen.size() >= count || tested > 16) break;
                if (chosen.stream().anyMatch(p -> p.distSqr(c.pos()) < 9)) continue;
                if (sample != null) {
                    tested++;
                    var path = sample.getNavigation().createPath(c.pos(), 0);
                    if (path == null || !path.canReach()) continue;
                }
                chosen.add(c.pos());
            }
            // Not enough good places: hide wherever.
            while (chosen.size() < count) {
                var p = ground(level, center.getX() + random.nextInt(15) - 7, center.getY(), center.getZ() + random.nextInt(15) - 7);
                chosen.add(p != null ? p : center);
            }
            return chosen;
        }
    }

    // -- ring-around-the-rosie ----------------------------------------------------------------------

    private static final class Ring extends Session {
        static final int WALK = 260, FALL = 70, ROUNDS = 3;
        enum Phase { GATHER, WALK, FALL }
        Phase phase = Phase.GATHER; long phaseAt; double angle, turn = .03; int rounds;
        Ring(ServerLevel level, BlockPos center, long now) { super(level, Game.RING, center, now); }
        double radius() { return 1.2 + .32 * members.size(); }
        @Override void begin(long now) { center = open(level, center, radius(), random); phaseAt = now; angle = random.nextDouble() * Math.PI * 2; }
        @Override boolean join(Villager v, long now) { return phase != Phase.WALK; }
        Vec3 slot(int i, int n, double extra) {
            double a = angle + extra + i * Math.PI * 2 / n, r = radius();
            return middle().add(Math.cos(a) * r, 0, Math.sin(a) * r);
        }
        @Override void step(long now, List<Villager> kids) {
            int n = members.size();
            switch (phase) {
                case GATHER -> {
                    boolean ready = true;
                    for (var v : kids) {
                        var to = slot(members.indexOf(v.getUUID()), n, 0);
                        if (near(v, to, .8)) { halt(v); face(v, middle()); } else { go(v, to, .6); ready = false; }
                        set(v, "join");
                    }
                    if (ready || now - phaseAt > 220) { phase = Phase.WALK; phaseAt = now; }
                }
                case WALK -> {
                    angle += turn;
                    for (var v : kids) {
                        int i = members.indexOf(v.getUUID());
                        var to = slot(i, n, turn * 6);
                        double dx = to.x - v.getX(), dz = to.z - v.getZ();
                        if (dx * dx + dz * dz > 2.6 * 2.6) go(v, to, .7);
                        else { v.getNavigation().stop(); v.getMoveControl().setWantedPosition(to.x, v.getY(), to.z, .45 + Math.min(.3, Math.sqrt(dx * dx + dz * dz) * .2)); }
                        face(v, slot(i, n, turn * 22));
                        set(v, "walk");
                    }
                    if (now - phaseAt > WALK) {
                        phase = Phase.FALL; phaseAt = now;
                        for (var v : kids) { halt(v); set(v, "fall"); VillageSocieties.emote(v, random.nextBoolean() ? Emote.NOTE : Emote.SPARKLE, 10 + random.nextInt(20)); }
                    }
                }
                case FALL -> {
                    for (var v : kids) { halt(v); face(v, middle()); }
                    if (now - phaseAt > FALL) {
                        if (++rounds >= ROUNDS) { done = true; return; }
                        if (random.nextBoolean()) turn = -turn;
                        phase = Phase.GATHER; phaseAt = now;
                    }
                }
            }
        }
    }

    // -- follow the leader --------------------------------------------------------------------------

    private static final class FollowTheLeader extends Session {
        static final double FIELD = 13;
        Vec3 waypoint; long showAt = -1, lastShow, leaderSince; Move move;
        FollowTheLeader(ServerLevel level, BlockPos center, long now) { super(level, Game.FOLLOW_THE_LEADER, center, now); }
        @Override void begin(long now) { leaderSince = now; lastShow = now; }
        @Override boolean join(Villager v, long now) { return showAt < 0; }
        @Override void step(long now, List<Villager> kids) {
            // Everyone gets a turn at the front: the leader drops to the back of the line now and then.
            if (showAt < 0 && now - leaderSince > 600 && members.size() > 1) {
                members.add(members.removeFirst());
                leaderSince = now; waypoint = null;
                var lead = kid(members.getFirst());
                if (lead != null) VillageSocieties.emote(lead, Emote.SPARKLE, 0);
            }
            var line = new ArrayList<Villager>();
            for (var id : members) { var v = kid(id); if (v != null) line.add(v); }
            if (line.isEmpty()) return;
            var leader = line.getFirst();
            if (showAt >= 0) { show(now, line); return; }
            set(leader, "lead");
            if (waypoint == null || near(leader, waypoint, 1.2) || leader.getNavigation().isDone() && leader.tickCount % 20 == 0) {
                if (waypoint != null && now - lastShow > 80 && random.nextInt(100) < 45) {
                    move = Move.values()[random.nextInt(Move.values().length)];
                    showAt = now; halt(leader); show(now, line); return;
                }
                var middle = middle();
                Vec3 to = leader.position().distanceToSqr(middle) > FIELD * FIELD ? LandRandomPos.getPosTowards(leader, 9, 3, middle) : LandRandomPos.getPos(leader, 9, 3);
                if (to != null && to.distanceToSqr(middle) > (FIELD + 2) * (FIELD + 2)) to = null;
                waypoint = to != null ? to : middle;
            }
            go(leader, waypoint, .5);
            for (int i = 1; i < line.size(); i++) {
                var v = line.get(i); var ahead = line.get(i - 1);
                if (v.distanceToSqr(ahead) > 2.1 * 2.1) chase(v, ahead, .58); else halt(v);
                face(v, ahead);
                set(v, "follow");
            }
        }
        /** The leader does a move, and one by one down the line, everyone copies it. */
        private void show(long now, List<Villager> line) {
            long last = 0;
            for (int i = 0; i < line.size(); i++) {
                var v = line.get(i);
                long from = showAt + (i == 0 ? 0 : 14 + 8L * i), to = from + move.ticks;
                last = Math.max(last, to);
                halt(v);
                if (i > 0) face(v, line.getFirst());
                if (now >= from && now < to) set(v, "do:" + move.id);
                else if (now >= to) set(v, i == 0 ? "lead" : "follow");
                else set(v, "follow");
            }
            if (now >= last) { showAt = -1; lastShow = now; waypoint = null; }
        }
    }

    // -- catch --------------------------------------------------------------------------------------

    private static final class Catch extends Session {
        static final double SPREAD = 2.4;
        enum Phase { GATHER, HOLD, THROW, FUMBLE }
        Phase phase = Phase.GATHER; long phaseAt, holdFor; UUID holder, receiver; boolean miss; Vec3 dropped;
        Catch(ServerLevel level, BlockPos center, long now) { super(level, Game.CATCH, center, now); }
        @Override void begin(long now) { center = open(level, center, SPREAD, random); phaseAt = now; holder = members.getFirst(); }
        @Override boolean join(Villager v, long now) {
            if (phase != Phase.HOLD || members.size() >= game.max) return false;
            phase = Phase.GATHER; phaseAt = now;
            return true;
        }
        @Override void left(UUID id) {
            if (id.equals(holder) || id.equals(receiver)) { holder = null; receiver = null; phase = Phase.GATHER; }
        }
        Vec3 spot(int i, int n) {
            double a = i * Math.PI * 2 / n + (center.asLong() & 7) * .4;
            return middle().add(Math.cos(a) * SPREAD, 0, Math.sin(a) * SPREAD);
        }
        @Override void step(long now, List<Villager> kids) {
            int n = members.size();
            var hold = kid(holder);
            if (hold == null) { hold = kids.getFirst(); holder = hold.getUUID(); }
            switch (phase) {
                case GATHER -> {
                    boolean ready = true;
                    for (var v : kids) {
                        var to = spot(members.indexOf(v.getUUID()), n);
                        if (near(v, to, .7)) { halt(v); face(v, middle()); } else { go(v, to, .6); ready = false; }
                        set(v, v == hold ? "hold" : "ready");
                    }
                    if (ready || now - phaseAt > 200) { phase = Phase.HOLD; phaseAt = now; holdFor = 25 + random.nextInt(45); }
                }
                case HOLD -> {
                    // The ball is passed round in turn; with three, now and then to whoever isn't expecting it.
                    int next = (members.indexOf(holder) + 1 + (n > 2 && random.nextInt(4) == 0 ? 1 : 0)) % n;
                    var catcher = kid(members.get(next));
                    for (var v : kids) { halt(v); face(v, v == hold ? (catcher != null ? catcher : v) : hold); set(v, v == hold ? "hold" : "ready"); }
                    if (now - phaseAt > holdFor && catcher != null && catcher != hold) {
                        receiver = catcher.getUUID();
                        miss = random.nextInt(100) < 15;
                        phase = Phase.THROW; phaseAt = now;
                        set(hold, "throw:" + catcher.getId() + (miss ? ":miss" : ""));
                        set(catcher, "catch");
                    }
                }
                case THROW -> {
                    var catcher = kid(receiver);
                    if (catcher == null) { phase = Phase.GATHER; phaseAt = now; return; }
                    for (var v : kids) { halt(v); face(v, v == hold ? catcher : hold); if (v != hold && v != catcher) set(v, "ready"); }
                    if (now - phaseAt >= RELEASE + FLIGHT) {
                        if (!miss) {
                            holder = receiver; set(catcher, "hold"); set(hold, "ready");
                            phase = Phase.HOLD; phaseAt = now; holdFor = 25 + random.nextInt(45);
                        } else {
                            // Whoops: it bounces past them and they go and get it.
                            dropped = landing(hold.position(), catcher.position());
                            set(catcher, "fumble");
                            VillageSocieties.emote(catcher, random.nextBoolean() ? Emote.SWEAT : Emote.DOTS, 0);
                            phase = Phase.FUMBLE; phaseAt = now;
                        }
                    }
                }
                case FUMBLE -> {
                    var catcher = kid(receiver);
                    if (catcher == null) { phase = Phase.GATHER; phaseAt = now; return; }
                    for (var v : kids) if (v != catcher) { halt(v); face(v, catcher); }
                    if (now - phaseAt < 30) { halt(catcher); return; }
                    if (!near(catcher, dropped, .8) && now - phaseAt < 120) { go(catcher, dropped, .55); face(catcher, dropped); return; }
                    // Picked it up: back to their place and carry on.
                    holder = receiver; set(catcher, "hold"); set(hold, "ready");
                    phase = Phase.GATHER; phaseAt = now;
                }
            }
        }
    }
    /** Where a missed ball ends up: a little past the child who should have caught it. Clients work it out the same way. */
    public static Vec3 landing(Vec3 thrower, Vec3 catcher) {
        double dx = catcher.x - thrower.x, dz = catcher.z - thrower.z, len = Math.max(1e-3, Math.sqrt(dx * dx + dz * dz));
        return new Vec3(catcher.x + dx / len * 1.4 + dz / len * .5, catcher.y, catcher.z + dz / len * 1.4 - dx / len * .5);
    }

    // -- curious ------------------------------------------------------------------------------------

    /** A bored child tags along behind a player to see what they're doing, and freezes, all innocence, when the player looks round. */
    private static final class Curious extends Session {
        final UUID player; long byeAt = -1, caughtSince = -1, stillSince; Vec3 lastSeen, lookAway; BlockPos anchor;
        Curious(ServerLevel level, Villager v, Player player, long now) {
            super(level, null, v.blockPosition(), now);
            this.player = player.getUUID();
            this.until = now + Games.curiousFor(random);
            var brain = v.getBrain();
            anchor = brain.getMemory(MemoryModuleType.MEETING_POINT).or(() -> brain.getMemory(MemoryModuleType.HOME))
                    .filter(g -> g.dimension() == level.dimension()).map(GlobalPos::pos).orElse(v.blockPosition());
        }
        @Override void begin(long now) { stillSince = now; }
        @Override void step(long now, List<Villager> kids) {
            var v = kids.getFirst();
            var p = level.getPlayerByUUID(player);
            if (byeAt >= 0) {
                halt(v); if (p != null) face(v, p); set(v, "bye");
                if (now - byeAt > 50) done = true;
                return;
            }
            // Keep the playground's middle with the child, so wandering after a player doesn't count as leaving it.
            center = v.blockPosition();
            if (p == null || !p.isAlive() || p.isSpectator() || p.level() != level || p.distanceToSqr(v) > 22 * 22 || now >= until
                    || v.blockPosition().distSqr(anchor) > 44 * 44) { bye(v, now, p != null && p.distanceToSqr(v) > 22 * 22 ? Emote.GLOOM : null); return; }
            double distance = Math.sqrt(p.distanceToSqr(v));
            if (distance > 13 && p.isSprinting()) { bye(v, now, Emote.GLOOM); return; }
            // Caught! The player turned round to look: freeze and act as if nothing is going on.
            var toKid = v.getEyePosition().subtract(p.getEyePosition());
            boolean watched = distance < 14 && toKid.normalize().dot(p.getViewVector(1)) > .965 && p.hasLineOfSight(v);
            if (watched) {
                if (caughtSince < 0) {
                    caughtSince = now;
                    var side = new Vec3(-toKid.z, 0, toKid.x).normalize().scale(random.nextBoolean() ? 3 : -3);
                    lookAway = v.position().add(side).add(0, 2.5, 0);
                    VillageSocieties.emote(v, random.nextInt(3) == 0 ? Emote.SWEAT : Emote.BLUSH, 2);
                }
                halt(v); v.getLookControl().setLookAt(lookAway.x, lookAway.y, lookAway.z, 20, 20); set(v, "caught");
                return;
            }
            if (caughtSince >= 0 && now - caughtSince < 25) { halt(v); set(v, "caught"); return; }
            caughtSince = -1;
            face(v, p);
            boolean moving = lastSeen != null && lastSeen.distanceToSqr(p.position()) > .002;
            lastSeen = p.position();
            if (moving) stillSince = now;
            // Several curious children spread out behind the same player.
            int index = 0;
            for (var s : sessions) { if (s == this) break; if (s instanceof Curious c && c.player.equals(player)) index++; }
            double keep = 2.6 + index * .9;
            if (distance > keep + 1.2) {
                var away = v.position().subtract(p.position()); away = new Vec3(away.x, 0, away.z);
                var to = p.position().add(away.lengthSqr() < 1e-4 ? Vec3.ZERO : away.normalize().scale(keep));
                go(v, to, p.isSprinting() ? .8 : .62);
                set(v, "follow");
            } else {
                halt(v);
                set(v, "watch");
                if (now - stillSince == 30 && random.nextInt(100) < 40) VillageSocieties.emote(v, random.nextInt(4) == 0 ? Emote.IDEA : Emote.QUESTION, 0);
            }
        }
        private void bye(Villager v, long now, Emote emote) {
            byeAt = now;
            if (emote != null) VillageSocieties.emote(v, emote, 0);
        }
    }

    private Playground() {}
}
