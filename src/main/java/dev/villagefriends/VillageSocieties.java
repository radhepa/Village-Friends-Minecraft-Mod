package dev.villagefriends;

import dev.villagefriends.outfit.ResidentLook;
import dev.villagefriends.social.*;
import java.util.*;
import net.fabricmc.fabric.api.attachment.v1.AttachmentTarget;
import net.fabricmc.fabric.api.networking.v1.PlayerLookup;
import net.fabricmc.fabric.api.networking.v1.ServerPlayNetworking;
import net.minecraft.ChatFormatting;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.monster.zombie.ZombieVillager;
import net.minecraft.world.entity.npc.villager.Villager;
import static dev.villagefriends.VillageFriends.*;

/**
 * Keeps each village's {@link Society} in step with the world: registers residents as their hometown
 * is confirmed, settles newcomers into families, records births, deaths and curses, lives each day
 * while the village is loaded, notices who stands together, and has neighbors emote at each other.
 */
public final class VillageSocieties {
    /** Newcomers this close to each other may be one household. */
    private static final double HOUSEHOLD_RANGE = 20, TOGETHER_RANGE = 6, CHAT_RANGE = 3.5;
    private static final Set<String> ANNOUNCED = Set.of("sweethearts", "married", "born", "passed", "cursed", "cured", "grew_up");
    /** "player|resident" to the day that resident last waved a player over. */
    private static final Map<String, Long> nudged = new HashMap<>();
    /** Deaths settle a tick later: a villager killed by a zombie dies first and is converted right after. */
    private static final Map<String, Runnable> deaths = new LinkedHashMap<>();

    public static void clear() { nudged.clear(); deaths.clear(); }

    static SocietyBook book(ServerLevel level) { return ((AttachmentTarget) level).getAttachedOrCreate(SOCIETIES); }
    static void put(ServerLevel level, Society society) {
        var book = book(level); var next = book.put(society);
        if (next == book) return;
        ((AttachmentTarget) level).setAttached(SOCIETIES, next);
        announce(level, book.villages().get(society.village()), society);
    }
    /** The level that keeps an entity's hometown records, or null for residents without a hometown. */
    static ServerLevel origin(Entity e) {
        var home = target(e).getAttached(HOME);
        if (home == null || !(e.level() instanceof ServerLevel level)) return null;
        return level.getServer().getLevel(ResourceKey.create(Registries.DIMENSION, Identifier.parse(home.dimension())));
    }
    /** The society of an entity's hometown, or null. */
    public static Society of(Entity e) {
        var home = target(e).getAttached(HOME); var origin = origin(e);
        return home == null || origin == null ? null : book(origin).villages().get(home.village());
    }
    public static Society society(ServerLevel level, String village) { return book(level).villages().get(village); }
    static String id(Entity e) { var p = target(e).getAttached(PROFILE); return p == null ? "" : p.id(); }
    static String gender(Villager v) { var look = ResidentLook.parse(profile(v).look()); return look == null ? "NON_BINARY" : look.gender().name(); }
    static String baseName(Villager v) { var home = target(v).getAttached(HOME); return home == null ? name(v) : home.baseName(); }
    private static boolean visited(Villager v) {
        return !target(v).getAttachedOrCreate(BONDS).bonds().isEmpty() || !target(v).getAttachedOrCreate(FRIENDSHIPS).relationships().isEmpty();
    }

    // -- residents ---------------------------------------------------------------------------------

    /** Called whenever a resident's hometown is confirmed: joins them to its census and keeps it current. */
    public static void register(Villager v) {
        var home = target(v).getAttached(HOME); var origin = origin(v);
        if (home == null || origin == null || !v.isAlive()) return;
        long today = day(v.level());
        var society = book(origin).get(home.village(), today);
        String id = id(v);
        if (!society.has(id)) {
            society = society.register(Townsfolk.newcomer(id, baseName(v), gender(v), profession(v), profile(v).personality(), !v.isBaby(), today));
            String parents = target(v).getAttachedOrElse(PARENTS, "");
            if (!parents.isEmpty()) {
                var split = parents.split("\\|", -1);
                society = society.born(id, split[0], split.length > 1 ? split[1] : "", today);
                society = adoptSurname(v, society, split[0]);
            } else if (home.village().startsWith("natural:") && !visited(v)) {
                // Residents of a newly found village may have arrived as a family.
                var before = society;
                society = society.household(id, candidates(v, society, today), today);
                if (society != before) society = adoptSurname(v, society, society.news().getLast().b());
            }
        } else society = society.seen(id, baseName(v), profession(v), !v.isBaby(), today);
        put(origin, society);
    }
    /** Other new arrivals of the same village standing nearby, closest first. */
    private static List<String> candidates(Villager v, Society society, long today) {
        String village = target(v).getAttached(HOME).village();
        return CompanionController.loaded.stream()
                .filter(o -> o != v && o.isAlive() && o.level() == v.level() && o.distanceToSqr(v) < HOUSEHOLD_RANGE * HOUSEHOLD_RANGE)
                .filter(o -> target(o).getAttached(HOME) != null && target(o).getAttached(HOME).village().equals(village))
                .filter(o -> { var t = society.get(id(o)); return t != null && t.joined() >= today - 1; })
                .sorted(Comparator.comparingDouble(v::distanceToSqr)).map(VillageSocieties::id).toList();
    }
    /** A family member who still has their generated name takes the household's surname. */
    private static Society adoptSurname(Villager v, Society society, String relativeId) {
        var relative = society.get(relativeId);
        String base = baseName(v), look = profile(v).look();
        if (relative == null || !base.equals(Dialogue.name(v.getUUID(), look))) return society;
        int space = base.lastIndexOf(' '), theirs = relative.name().lastIndexOf(' ');
        if (space <= 0 || theirs <= 0) return society;
        String surname = relative.name().substring(theirs + 1);
        var names = ResidentNames.current();
        if (names.restrictedSurnames().contains(surname) && !names.restrictedSurnameComplexions().contains(ResidentAppearance.complexion(look))) return society;
        String renamed = base.substring(0, space) + " " + surname;
        if (renamed.equals(base)) return society;
        VillageSettlements.rename(v, renamed);
        return society.seen(id(v), renamed, profession(v), !v.isBaby(), day(v.level()));
    }
    /** A baby is about to be born: remember both parents for when they arrive. */
    public static void conceived(Villager parent, AgeableMob partner, Villager baby) {
        if (baby == null) return;
        String first = id(parent), second = partner instanceof Villager other ? id(other) : "";
        if (!first.isEmpty()) target(baby).setAttached(PARENTS, first + "|" + second);
        emote(parent, Emote.SPARKLE, 0);
        if (partner instanceof Villager other) emote(other, Emote.SPARKLE, 6);
    }
    /** Relatives never start a family together, and residents in love only with their own partner. */
    public static boolean mayBreed(Villager a, Villager b) {
        var society = of(a);
        String x = id(a), y = id(b);
        if (society == null || !society.has(x) || !society.has(y)) return true;
        String px = society.get(x).partner(), py = society.get(y).partner();
        return !society.blood(x, y) && (px.isEmpty() || px.equals(y)) && (py.isEmpty() || py.equals(x));
    }
    public static void died(Villager v) {
        var origin = origin(v); String id = id(v); var home = target(v).getAttached(HOME);
        if (origin == null || home == null || id.isEmpty()) return;
        deaths.put(id, () -> mourn(v, origin, home.village(), id));
    }
    private static void mourn(Villager v, ServerLevel origin, String village, String id) {
        var society = book(origin).villages().get(village);
        if (society == null || !society.has(id)) return;
        long today = day(v.level());
        put(origin, society.passed(id, today));
        for (var other : CompanionController.loaded) if (other != v && other.isAlive() && other.level() == v.level() && other.distanceToSqr(v) < 32 * 32
                && (society.blood(id, id(other)) || society.get(id).partner().equals(id(other)) || society.affinity(id, id(other), today) >= 40))
            emote(other, Emote.GLOOM, 10 + other.getRandom().nextInt(30));
    }
    /** Zombie conversion and curing keep the resident in their village's memory. */
    public static void converted(Entity before, Entity after) {
        var origin = origin(after); var society = of(after); String id = id(after);
        deaths.remove(id); // Converted, not gone.
        if (origin == null || society == null || !society.has(id)) return;
        long today = day(after.level());
        if (before instanceof Villager && !(after instanceof Villager)) put(origin, society.cursed(id, today));
        else if (before instanceof ZombieVillager && after instanceof Villager) put(origin, society.cured(id, today));
    }

    // -- daily life --------------------------------------------------------------------------------

    public static void tick(MinecraftServer server) {
        if (!deaths.isEmpty()) { var settled = List.copyOf(deaths.values()); deaths.clear(); settled.forEach(Runnable::run); }
        if (server.getTickCount() % 200 != 50) return;
        var groups = new HashMap<String, List<Villager>>();
        for (var v : List.copyOf(CompanionController.loaded)) {
            var home = target(v).getAttached(HOME);
            if (home == null || !v.isAlive() || v.isRemoved()) continue;
            groups.computeIfAbsent(home.dimension() + "|" + home.village(), k -> new ArrayList<>()).add(v);
        }
        for (var group : groups.values()) live(group);
        for (var player : server.getPlayerList().getPlayers()) nudge(player);
    }
    private static void live(List<Villager> residents) {
        var first = residents.getFirst(); var origin = origin(first);
        if (origin == null) return;
        long today = day(first.level());
        String village = target(first).getAttached(HOME).village();
        var society = book(origin).villages().get(village);
        if (society == null) return;
        society = society.advance(today);
        var chats = new ArrayList<Villager[]>();
        for (int i = 0; i < residents.size(); i++) for (int j = i + 1; j < residents.size(); j++) {
            var a = residents.get(i); var b = residents.get(j);
            if (a.level() != b.level()) continue;
            double distance = a.distanceToSqr(b);
            if (distance < TOGETHER_RANGE * TOGETHER_RANGE) society = society.together(id(a), id(b), today);
            if (distance < CHAT_RANGE * CHAT_RANGE && chatty(a) && chatty(b)) chats.add(new Villager[]{a, b});
        }
        put(origin, society);
        // Neighbors who stand together sometimes strike up a conversation you can see from afar.
        var random = first.getRandom();
        Collections.shuffle(chats, new Random(random.nextLong()));
        int shown = 0;
        for (var pair : chats) {
            if (shown >= 2 || random.nextFloat() > .55F) continue;
            var speaker = random.nextBoolean() ? pair[0] : pair[1]; var listener = speaker == pair[0] ? pair[1] : pair[0];
            var pairEmotes = chat(society, id(speaker), id(listener), today, random.nextInt(100));
            emote(speaker, pairEmotes[0], 0);
            emote(listener, pairEmotes[1], 26 + random.nextInt(14));
            shown++;
        }
    }
    private static boolean chatty(Villager v) {
        return !v.isSleeping() && !v.isTrading() && !CompanionController.state(v).active() && v.getDeltaMovement().horizontalDistanceSqr() < .002;
    }
    /** What two neighbors' bubbles say about how they feel: hearts for sweethearts, sparks for rivals. */
    static Emote[] chat(Society society, String a, String b, long day, int roll) {
        String romance = society.romance(a, b, day);
        int affinity = society.affinity(a, b, day);
        var tie = society.tie(a, b);
        boolean sore = tie.quarrel() >= 0 && day - tie.quarrel() < 10;
        if (romance.equals("married") || romance.equals("sweethearts")) return new Emote[]{Emote.HEART, roll < 50 ? Emote.HEART : Emote.BLUSH};
        if (society.crush(a, day).equals(b)) return new Emote[]{Emote.BLUSH, roll < 50 ? Emote.QUESTION : Emote.NOTE};
        if (sore || affinity < -10) return new Emote[]{Emote.ANGER, roll < 50 ? Emote.ANGER : Emote.SWEAT};
        if (!society.relation(a, b).isEmpty()) return new Emote[]{roll < 50 ? Emote.NOTE : Emote.EXCLAIM, Emote.NOTE};
        if (affinity >= 65) return new Emote[]{roll < 35 ? Emote.NOTE : roll < 70 ? Emote.IDEA : Emote.EXCLAIM, roll % 2 == 0 ? Emote.NOTE : Emote.SPARKLE};
        if (affinity >= 15) return new Emote[]{roll < 50 ? Emote.DOTS : Emote.IDEA, roll < 33 ? Emote.EXCLAIM : roll < 66 ? Emote.QUESTION : Emote.NOTE};
        return new Emote[]{Emote.DOTS, roll < 50 ? Emote.DOTS : Emote.QUESTION};
    }
    /** Close friends wave a player over with a heart; anyone with fresh news gets an idea bubble. */
    private static void nudge(ServerPlayer player) {
        if (player.isSpectator()) return;
        var acquaintances = target(player).getAttachedOrCreate(ACQUAINTANCES);
        for (var v : CompanionController.loaded) {
            if (v.level() != player.level() || v.isSleeping() || v.distanceToSqr(player) > 36 || !v.isAlive()) continue;
            String key = player.getUUID() + "|" + id(v); long today = day(v.level());
            if (nudged.getOrDefault(key, -1L) == today) continue;
            int level = acquaintances.getOrDefault(id(v), -1);
            var society = of(v);
            boolean news = level >= FriendshipLevels.NEWS && society != null && !society.recent(today, 1).isEmpty();
            if (level < FriendshipLevels.HEART_GREETING && !news) continue;
            nudged.put(key, today);
            if (ServerPlayNetworking.canSend(player, EmotePayload.TYPE))
                ServerPlayNetworking.send(player, new EmotePayload(v.getId(), (level >= FriendshipLevels.HEART_GREETING ? Emote.HEART : Emote.IDEA).name(), 4));
        }
    }
    /** Shows an emote above a resident to everyone nearby. */
    public static void emote(Villager v, Emote emote, int delay) {
        if (!(v.level() instanceof ServerLevel)) return;
        var payload = new EmotePayload(v.getId(), emote.name(), delay);
        for (var player : PlayerLookup.tracking(v))
            if (player.distanceToSqr(v) < 48 * 48 && ServerPlayNetworking.canSend(player, EmotePayload.TYPE)) ServerPlayNetworking.send(player, payload);
    }
    /** Big village events reach everyone currently in that village. */
    private static void announce(ServerLevel level, Society before, Society after) {
        var record = VillageSettlements.book(level).villages().get(after.village());
        if (record == null) return;
        var fresh = new ArrayList<>(after.news());
        if (before != null) fresh.removeAll(before.news());
        for (var news : fresh) {
            if (!ANNOUNCED.contains(news.kind()) || news.day() < day(level) - 1) continue;
            var message = Component.literal("✉ " + record.name() + ": ").withStyle(ChatFormatting.GOLD)
                    .append(Component.literal(news.headline(after)).withStyle(ChatFormatting.YELLOW));
            for (var player : level.players()) if (record.contains(player.blockPosition())) player.sendSystemMessage(message, false);
        }
    }
    private VillageSocieties() {}
}
