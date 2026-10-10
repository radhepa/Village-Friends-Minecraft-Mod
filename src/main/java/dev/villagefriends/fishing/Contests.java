package dev.villagefriends.fishing;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import dev.villagefriends.VillageFriends;
import dev.villagefriends.VillageProfessions;
import dev.villagefriends.VillageRecord;
import dev.villagefriends.VillageSettlements;
import dev.villagefriends.social.Calendar;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.UUID;
import net.fabricmc.fabric.api.attachment.v1.AttachmentRegistry;
import net.fabricmc.fabric.api.attachment.v1.AttachmentTarget;
import net.fabricmc.fabric.api.attachment.v1.AttachmentType;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.fabricmc.fabric.api.networking.v1.ServerPlayNetworking;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.entity.ai.village.poi.PoiManager;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.phys.AABB;

/**
 * The season's fishing contest in every village ({@link Contest} has the rules). While it's on, anything a player
 * catches in or near the village counts, and the village's fishermen and anglers enter too; players there see the
 * standings in the corner of the screen. At 17:00 the tavern keeper reads out the results, and winners collect
 * their prizes from the tavern (they're kept for them until they come by). State per village lives on the level
 * ({@code villagefriends:fishing_contests}).
 */
public final class Contests {
    /** One village's contest: the day it's for, the standings, what's been announced and the prizes not yet collected (UUID to place). */
    public record State(long day, List<Contest.Entry> standings, int announced, boolean awarded, Map<String, Integer> unclaimed) {
        static final Codec<State> CODEC = RecordCodecBuilder.create(i -> i.group(
                Codec.LONG.fieldOf("day").forGetter(State::day),
                Contest.Entry.CODEC.listOf().optionalFieldOf("standings", List.of()).forGetter(State::standings),
                Codec.INT.optionalFieldOf("announced", 0).forGetter(State::announced),
                Codec.BOOL.optionalFieldOf("awarded", false).forGetter(State::awarded),
                Codec.unboundedMap(Codec.STRING, Codec.INT).optionalFieldOf("unclaimed", Map.of()).forGetter(State::unclaimed)
        ).apply(i, State::new));
        static State fresh(long day, Map<String, Integer> unclaimed) { return new State(day, List.of(), 0, false, unclaimed); }
        State standings(List<Contest.Entry> s) { return new State(day, s, announced, awarded, unclaimed); }
        State announced(int a) { return new State(day, standings, a, awarded, unclaimed); }
        State awarded(Map<String, Integer> u) { return new State(day, standings, announced, true, u); }
        State claimed(String key) { var u = new HashMap<>(unclaimed); u.remove(key); return new State(day, standings, announced, awarded, Map.copyOf(u)); }
    }
    public static final AttachmentType<Map<String, State>> STATE = AttachmentRegistry.create(Fishing.id("fishing_contests"),
            b -> b.initializer(Map::of).persistent(Codec.unboundedMap(Codec.STRING, State.CODEC)));

    private static final Map<UUID, String> SHOWN = new HashMap<>();
    private static final Random RANDOM = new Random();
    /** Unless set, the contest follows the calendar; {@code /fishing contest start} runs one today. */
    private static final Map<String, Long> FORCED = new HashMap<>();

    static void register() {
        ServerTickEvents.END_SERVER_TICK.register(Contests::tick);
    }
    public static void clear() { SHOWN.clear(); FORCED.clear(); }

    private static Map<String, State> all(ServerLevel level) { return ((AttachmentTarget) level).getAttachedOrElse(STATE, Map.of()); }
    private static void put(ServerLevel level, String village, State state) {
        var next = new HashMap<>(all(level)); next.put(village, state);
        ((AttachmentTarget) level).setAttached(STATE, Map.copyOf(next));
    }
    public static State state(ServerLevel level, String village) { return all(level).get(village); }

    /** Today's phase in this village: the calendar's, or an open contest started by command. */
    public static Contest.Phase phase(ServerLevel level, String village) {
        long day = VillageFriends.day(level); int time = dev.villagefriends.ResidentRoutines.timeOfDay(level);
        var forced = FORCED.get(village);
        if (forced != null && forced == day) return Contest.Phase.OPEN;
        return Contest.phase(day, time);
    }
    /** Starts a contest today in the village at {@code pos} (for testing and for servers that want one now). */
    public static VillageRecord start(ServerLevel level, BlockPos pos) {
        var village = VillageSettlements.book(level).at(pos);
        if (village == null) return null;
        long day = VillageFriends.day(level);
        FORCED.put(village.id(), day);
        var old = state(level, village.id());
        put(level, village.id(), State.fresh(day, old == null ? Map.of() : old.unclaimed()));
        return village;
    }
    /** Ends today's contest now: results and prizes. */
    public static boolean finish(ServerLevel level, BlockPos pos) {
        var village = VillageSettlements.book(level).at(pos);
        if (village == null) return false;
        var s = state(level, village.id());
        if (s == null || s.awarded()) return false;
        award(level, village, s);
        FORCED.remove(village.id());
        return true;
    }

    /** A player's catch: if there's a contest on where they are, it's entered. */
    static void caught(ServerPlayer p, Fish fish, int size) {
        var level = (ServerLevel) p.level();
        var village = near(level, p.blockPosition());
        if (village == null || phase(level, village.id()) != Contest.Phase.OPEN || fish.legendary()) return;
        var s = current(level, village.id());
        var before = Contest.place(s.standings(), p.getUUID().toString());
        var standings = Contest.add(s.standings(), new Contest.Entry(p.getUUID().toString(), p.getName().getString(), true, fish.id(), size));
        put(level, village.id(), s.standings(standings));
        int place = Contest.place(standings, p.getUUID().toString());
        if (place != before) p.sendSystemMessage(Component.literal("Contest: your " + fish.name().toLowerCase(java.util.Locale.ROOT) + " puts you "
                + Contest.ordinal(place) + "!").withStyle(ChatFormatting.AQUA));
        board(p, level, village, true);
    }
    /** A resident's catch for the contest. */
    public static void residentCaught(ServerLevel level, Villager v, Fish fish, int size) {
        var village = VillageSettlements.home(v);
        if (village == null || phase(level, village.id()) != Contest.Phase.OPEN || fish.legendary()) return;
        var s = current(level, village.id());
        put(level, village.id(), s.standings(Contest.add(s.standings(), new Contest.Entry(VillageFriends.profile(v).id(), entrant(v), false, fish.id(), size))));
    }
    /** A resident's name on the board: "Aspen Peakrider", without "of Pondsend". */
    private static String entrant(Villager v) {
        String name = VillageFriends.name(v);
        int of = name.indexOf(" of ");
        return of > 0 ? name.substring(0, of) : name;
    }
    private static State current(ServerLevel level, String village) {
        long day = VillageFriends.day(level);
        var s = state(level, village);
        return s == null || s.day() != day ? State.fresh(day, s == null ? Map.of() : s.unclaimed()) : s;
    }
    /** The village whose contest a position counts for: inside it, or within 48 blocks of its edge. */
    private static VillageRecord near(ServerLevel level, BlockPos pos) {
        VillageRecord best = null; long bestD = Long.MAX_VALUE;
        for (var v : VillageSettlements.book(level).villages().values()) {
            long r = v.radius() + 48L;
            if (Math.abs((long) pos.getX() - v.x()) > r || Math.abs((long) pos.getZ() - v.z()) > r) continue;
            long d = v.distance(pos);
            if (d < bestD) { best = v; bestD = d; }
        }
        return best;
    }
    /** Who won this village's last contest, for three days after it. */
    public static Contest.Entry recentWinner(ServerLevel level, String village, long today) {
        var s = state(level, village);
        if (s == null || !s.awarded() || s.standings().isEmpty() || today - s.day() > 3) return null;
        return s.standings().getFirst();
    }

    // -- the day -----------------------------------------------------------------------------------------

    private static void tick(MinecraftServer server) {
        if (server.getTickCount() % 20 != 7) return;
        for (var level : server.getAllLevels()) {
            var book = VillageSettlements.book(level);
            if (book.villages().isEmpty()) continue;
            long day = VillageFriends.day(level);
            for (var village : book.villages().values()) {
                var phase = phase(level, village.id());
                var saved = state(level, village.id());
                if (saved != null && !saved.unclaimed().isEmpty()) prizes(level, village, saved);
                if (phase == Contest.Phase.NONE) { tomorrow(level, village, day); continue; }
                var s = current(level, village.id());
                if (phase == Contest.Phase.OPEN && s.announced() < 2) {
                    announce(level, village, Component.literal("Today is the " + village.name() + " fishing contest! Fish until 16:30; the biggest fish wins. Weigh-in at the tavern at 17:00.")
                            .withStyle(ChatFormatting.AQUA));
                    s = s.announced(2); put(level, village.id(), s);
                }
                if (phase == Contest.Phase.OPEN && server.getTickCount() % 1200 == 7) entrants(level, village);
                if (phase == Contest.Phase.OVER && !s.awarded()) award(level, village, s);
            }
            for (var p : level.players()) {
                var village = near(level, p.blockPosition());
                var phase = village == null ? Contest.Phase.NONE : phase(level, village.id());
                boolean show = phase == Contest.Phase.OPEN || phase == Contest.Phase.WEIGH_IN;
                if (show) board(p, level, village, server.getTickCount() % 100 == 7);
                else if (SHOWN.remove(p.getUUID()) != null) ServerPlayNetworking.send(p, FishingNet.ContestBoard.HIDDEN);
            }
        }
    }
    /** The evening before, players in the village hear about tomorrow's contest. */
    private static void tomorrow(ServerLevel level, VillageRecord village, long day) {
        if (Contest.daysUntil(day) != 1 || Math.floorMod(dev.villagefriends.ResidentRoutines.timeOfDay(level), 24000) < 11000) return;
        var s = state(level, village.id());
        if (s != null && s.day() == day + 1 && s.announced() >= 1) return;
        announce(level, village, Component.literal("Tomorrow is the " + village.name() + " fishing contest. Bring your best rod!").withStyle(ChatFormatting.AQUA));
        put(level, village.id(), State.fresh(day + 1, s == null ? Map.of() : s.unclaimed()).announced(1));
    }
    private static void announce(ServerLevel level, VillageRecord village, Component message) {
        for (var p : level.players()) if (village.contains(p.blockPosition())) p.sendSystemMessage(message);
    }
    /** The village's fishermen and anglers (and a couple of hopefuls) cast for the contest about once a minute. */
    private static void entrants(ServerLevel level, VillageRecord village) {
        var box = new AABB(village.x() - village.radius(), village.y() - 40, village.z() - village.radius(), village.x() + village.radius(), village.y() + 40, village.z() + village.radius());
        var spot = DockAnglers.villageSpot(level, village);
        if (spot == null) return;
        for (var v : level.getEntitiesOfClass(Villager.class, box, Villager::isAlive)) {
            if (v.isBaby() || VillageSettlements.home(v) == null || !village.id().equals(VillageSettlements.home(v).id())) continue;
            boolean angler = VillageFriends.profession(v).equals("fisherman") || "fishing".equals(VillageFriends.profile(v).hobby());
            if (!angler && Math.floorMod(v.getUUID().hashCode() + VillageFriends.day(level), 6) != 0) continue;
            if (RANDOM.nextInt(angler ? 3 : 6) != 0) continue;
            var entry = Contest.residentCatch(VillageFriends.profile(v).id(), entrant(v), FishTable.all(), spot, angler ? 2 : 0, RANDOM);
            if (entry == null) continue;
            var s = current(level, village.id());
            put(level, village.id(), s.standings(Contest.add(s.standings(), entry)));
        }
    }
    /** 17:00: the results, read out at the tavern; the winners' prizes wait for them there. */
    private static void award(ServerLevel level, VillageRecord village, State s) {
        var top = s.standings().subList(0, Math.min(3, s.standings().size()));
        var unclaimed = new HashMap<>(s.unclaimed());
        if (top.isEmpty()) announce(level, village, Component.literal("Nobody caught a thing in the " + village.name() + " fishing contest. There's always next season.").withStyle(ChatFormatting.GRAY));
        else {
            var line = Component.literal("The tavern keeper reads out the " + village.name() + " fishing contest results: ").withStyle(ChatFormatting.GOLD);
            for (int i = 0; i < top.size(); i++) {
                var e = top.get(i); var f = FishTable.get(e.fish());
                line.append(Component.literal((i > 0 ? ", " : "") + Contest.ordinal(i + 1) + " " + e.name() + " (" + (f == null ? e.fish() : f.name()) + ", "
                        + Catches.cm(e.size()) + ")").withStyle(i == 0 ? ChatFormatting.YELLOW : ChatFormatting.WHITE));
                if (e.player()) unclaimed.put(e.key(), i + 1);
            }
            announce(level, village, line);
            if (!unclaimed.isEmpty()) announce(level, village, Component.literal("Winners: collect your prizes at the tavern.").withStyle(ChatFormatting.GRAY));
        }
        put(level, village.id(), s.awarded(Map.copyOf(unclaimed)));
    }
    /** Winners who come by the tavern (within 10 blocks of the keeper's station) get their prize. */
    private static void prizes(ServerLevel level, VillageRecord village, State s) {
        var tavern = tavern(level, village);
        for (var e : Map.copyOf(s.unclaimed()).entrySet()) {
            var p = level.getServer().getPlayerList().getPlayer(UUID.fromString(e.getKey()));
            if (p == null || p.level() != level) continue;
            if (tavern != null ? !tavern.closerToCenterThan(p.position(), 10) : !village.contains(p.blockPosition())) continue;
            for (var prize : Contest.prizes(e.getValue())) {
                var stack = FishingItems.stack(prize.item(), prize.count());
                if (!p.getInventory().add(stack)) dev.villagefriends.VillageFriends.drop(p, stack);
            }
            p.sendSystemMessage(Component.literal("\"Here's your prize for " + Contest.ordinal(e.getValue()) + " place. Well fished!\"").withStyle(ChatFormatting.GOLD));
            level.playSound(null, p.blockPosition(), SoundEvents.PLAYER_LEVELUP, SoundSource.PLAYERS, .7F, 1.2F);
            s = s.claimed(e.getKey());
            put(level, village.id(), s);
        }
    }
    /** The tavern keeper's station nearest the village centre, or null. */
    public static BlockPos tavern(ServerLevel level, VillageRecord village) {
        var poi = VillageProfessions.poiKey("tavern_keeper");
        return level.getPoiManager().findClosest(holder -> holder.is(poi), new BlockPos(village.x(), village.y(), village.z()), Math.min(village.radius(), 128), PoiManager.Occupancy.ANY).orElse(null);
    }

    /** Sends a player the board for this village's contest (only when it changed, unless {@code force}). */
    private static void board(ServerPlayer p, ServerLevel level, VillageRecord village, boolean force) {
        var s = current(level, village.id());
        var phase = phase(level, village.id());
        String status = phase == Contest.Phase.OPEN ? "Fishing until 16:30" : "Weigh-in at the tavern at 17:00";
        String key = p.getUUID().toString();
        int place = Contest.place(s.standings(), key);
        String best = "";
        if (place > 0) { var e = s.standings().get(place - 1); var f = FishTable.get(e.fish()); best = (f == null ? e.fish() : f.name()) + ", " + Catches.cm(e.size()); }
        var top = s.standings().subList(0, Math.min(5, s.standings().size()));
        String signature = village.id() + "|" + status + "|" + top + "|" + place;
        if (!force && signature.equals(SHOWN.get(p.getUUID()))) return;
        SHOWN.put(p.getUUID(), signature);
        ServerPlayNetworking.send(p, new FishingNet.ContestBoard(true, village.name() + " Fishing Contest", status, top, place, best));
    }

    /** "Summer 12 (in 5 days)", for the notice board and the ledger. */
    public static String next(long day) {
        int until = Contest.daysUntil(day);
        return Contest.nextDate(day) + " (" + Calendar.when(until) + ")";
    }

    private Contests() {}
}
