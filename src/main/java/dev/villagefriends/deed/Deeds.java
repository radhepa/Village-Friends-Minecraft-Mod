package dev.villagefriends.deed;

import static dev.villagefriends.VillageFriends.*;
import dev.villagefriends.*;
import dev.villagefriends.home.HouseBounds;
import dev.villagefriends.pet.VillagerPets;
import dev.villagefriends.social.News;
import dev.villagefriends.social.Relations;
import dev.villagefriends.social.Society;
import dev.villagefriends.talk.Talk;
import java.util.*;
import net.fabricmc.fabric.api.attachment.v1.AttachmentRegistry;
import net.fabricmc.fabric.api.attachment.v1.AttachmentTarget;
import net.fabricmc.fabric.api.attachment.v1.AttachmentType;
import net.fabricmc.fabric.api.entity.event.v1.ServerLivingEntityEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.fabricmc.fabric.api.event.player.PlayerBlockBreakEvents;
import net.fabricmc.fabric.api.event.player.UseBlockCallback;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.tags.BlockTags;
import net.minecraft.world.Container;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.ai.behavior.EntityTracker;
import net.minecraft.world.entity.ai.gossip.GossipType;
import net.minecraft.world.entity.ai.memory.MemoryModuleType;
import net.minecraft.world.entity.ai.village.poi.PoiTypes;
import net.minecraft.world.entity.animal.golem.IronGolem;
import net.minecraft.world.entity.monster.Enemy;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.raid.Raid;
import net.minecraft.world.entity.raid.Raider;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.ChestBlock;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;

/**
 * Residents react to what players do in their village. Every deed (good or bad, {@link DeedKind}) is kept
 * in the village's {@link DeedBook} with who it happened to, who saw it and who has since heard; witnesses
 * show a bubble and turn to look; word spreads through the village's daily life ({@link Rumors}); the first
 * conversation afterwards brings it up ({@link Reactions}); and it moves the player's {@link Standing} and
 * prices. One {@link #register()} call installs the event hooks; the rest are single calls from the
 * existing systems (knockouts, companions, guards, pets, birthdays, notices, conversations).
 */
public final class Deeds {
    private static Identifier id(String path) { return Identifier.fromNamespaceAndPath("villagefriends", path); }
    /** Every player's deeds in every village recorded on a level. */
    public static final AttachmentType<DeedBook> DEEDS = AttachmentRegistry.create(id("deeds"),
            b -> b.initializer(() -> DeedBook.EMPTY).persistent(DeedBook.CODEC));
    /** How far a witness can be from the player or the victim, and how many there can be. */
    public static final int RANGE = 16, MAX_WITNESSES = 16, RAYCASTS = 6;
    /** How long one resident's price term for one player is reused. */
    private static final int PRICE_TICKS = 100;

    /** Where a deed belongs: the village and the level that keeps its records. */
    public record Place(ServerLevel origin, String village) {}
    private record Tally(Place place, String key, Set<UUID> players) {}
    private record Snapshot(ServerLevel level, BlockPos pos, HouseBounds.HouseRef house, Map<String, Integer> counts, long tick) {}

    /** "villager|player" to {price term, game time it was worked out}. */
    private static final Map<String, long[]> prices = new HashMap<>();
    /** "villager|player" to the bubble the next greeting opens with, after a reaction line. */
    private static final Map<String, Emote> moods = new HashMap<>();
    /** Raids players have fought in, until they end. */
    private static final Map<Raid, Tally> raids = new HashMap<>();
    /** Containers in residents' houses a player opened: what was in them. */
    private static final Map<UUID, Snapshot> opened = new HashMap<>();
    /** "player|pos" to how many items were in a resident's container the player is breaking. */
    private static final Map<String, Integer> breaking = new HashMap<>();

    public static void register() {
        ServerLivingEntityEvents.AFTER_DEATH.register(Deeds::died);
        ServerLivingEntityEvents.AFTER_DAMAGE.register((entity, source, base, taken, blocked) -> { if (taken > 0 && !blocked) hurt(entity, source); });
        ServerTickEvents.END_SERVER_TICK.register(Deeds::tick);
        PlayerBlockBreakEvents.BEFORE.register(Deeds::breaking);
        PlayerBlockBreakEvents.AFTER.register(Deeds::broke);
        UseBlockCallback.EVENT.register(Deeds::use);
    }
    public static void clear() { prices.clear(); moods.clear(); raids.clear(); opened.clear(); breaking.clear(); }

    // -- the book ------------------------------------------------------------------------------------

    public static DeedBook book(ServerLevel origin) { return ((AttachmentTarget) origin).getAttachedOrCreate(DEEDS); }
    private static void save(ServerLevel origin, DeedBook book) { ((AttachmentTarget) origin).setAttached(DEEDS, book); prices.clear(); }
    public static DeedLog log(Place place, UUID player) { return place == null ? null : book(place.origin()).log(place.village(), player.toString()); }
    /** A resident's hometown, or null. */
    public static Place place(Villager v) {
        var home = target(v).getAttached(HOME); var origin = VillageSocieties.origin(v);
        return home == null || origin == null ? null : new Place(origin, home.village());
    }
    /** The village around a spot on a level, or null. */
    public static Place place(ServerLevel level, BlockPos pos) {
        var record = VillageSettlements.book(level).at(pos);
        return record == null ? null : new Place(level, record.id());
    }
    private static String villageName(Place place) {
        var record = VillageSettlements.book(place.origin()).villages().get(place.village());
        return record == null ? "the village" : record.name();
    }

    // -- recording -----------------------------------------------------------------------------------

    /** A player did something. Creative and spectator players never do deeds. Returns the deed as it stands, or null. */
    public static Deed record(ServerPlayer p, DeedKind kind, Place place, String key, String label, List<String> involved, int count, boolean child, Entity victim) {
        if (p == null || place == null || p.isCreative() || p.isSpectator()) return null;
        return record(place, p.getUUID(), p.getName().getString(), p, kind, key, label, involved, count, child, victim);
    }
    /**
     * Records a deed by a player who may be offline ({@code actor} null): the involved residents and their
     * families know at once, witnesses see it, a big deed becomes village news, and standing is updated.
     */
    public static Deed record(Place place, UUID player, String playerName, LivingEntity actor, DeedKind kind, String key, String label,
            List<String> involved, int count, boolean child, Entity victim) {
        var origin = place.origin(); long today = day(origin), tick = origin.getGameTime();
        var society = VillageSocieties.society(origin, place.village());
        var book = book(origin);
        var log = book.log(place.village(), player.toString());
        if (log == null) log = DeedLog.create(player.toString(), playerName);
        if (!playerName.isEmpty()) log = log.named(playerName);
        int before = score10(origin, place.village(), player.toString());
        var recorded = log.record(kind, key, label, today, tick, involved, count, child);
        var deed = recorded.deed();
        for (var id : involved) deed = deed.learn(id, Know.of(Know.INVOLVED, today, ""));
        if (society != null) for (var id : involved) for (var kin : family(society, id)) deed = deed.learn(kin, Know.of(Know.FAMILY, today, id));
        var level = actor != null && actor.level() instanceof ServerLevel l ? l : victim != null && victim.level() instanceof ServerLevel l ? l : origin;
        var seen = witnesses(level, place.village(), actor, victim);
        for (var w : seen) deed = deed.learn(VillageSocieties.id(w), Know.of(Know.SEEN, today, ""));
        save(origin, book.put(place.village(), recorded.log().with(deed)));
        if (kind.big() && !recorded.merged() && society != null) {
            boolean pet = kind == DeedKind.KILLED_PET;
            VillageSocieties.put(origin, society.report(new News(today, "deed:" + kind.id(), deed.victim(), pet ? label : "", log.playerName())));
        }
        react(seen, actor != null ? actor : victim, kind);
        changed(place, player, before);
        return deed;
    }
    /** A resident's living partner and family. */
    private static Set<String> family(Society s, String id) {
        var out = new LinkedHashSet<String>();
        var self = s.get(id);
        if (self == null) return out;
        if (!self.partner().isEmpty()) out.add(self.partner());
        out.addAll(s.family(id));
        out.removeIf(other -> !Rumors.present(s, other));
        return out;
    }

    /**
     * Residents who saw it: awake, not lying hurt, within {@value #RANGE} blocks, and with the player or
     * the victim in sight. Vanilla's own line-of-sight sensor memory answers first; a few raycasts cover
     * residents whose senses haven't caught up yet.
     */
    static List<Villager> witnesses(ServerLevel level, String village, LivingEntity actor, Entity victim) {
        Entity center = actor != null ? actor : victim;
        if (center == null) return List.of();
        var near = new ArrayList<Villager>();
        for (var v : CompanionController.loaded) {
            if (v == victim || !v.isAlive() || v.level() != level || v.isSleeping() || Knockouts.injured(v)) continue;
            var home = target(v).getAttached(HOME);
            if (home == null || !home.village().equals(village)) continue;
            if ((actor == null || v.distanceTo(actor) > RANGE) && (victim == null || v.distanceTo(victim) > RANGE)) continue;
            near.add(v);
        }
        near.sort(Comparator.comparingDouble(v -> v.distanceToSqr(center)));
        var out = new ArrayList<Villager>(); int raycasts = 0;
        for (var v : near) {
            if (out.size() >= MAX_WITNESSES) break;
            var memory = v.getBrain().getMemory(MemoryModuleType.NEAREST_VISIBLE_LIVING_ENTITIES);
            boolean saw = memory.isPresent() && (actor != null && memory.get().contains(actor) || victim instanceof LivingEntity l && memory.get().contains(l));
            if (!saw && raycasts < RAYCASTS) {
                raycasts++;
                saw = actor != null && v.distanceTo(actor) <= RANGE && v.hasLineOfSight(actor) || victim != null && v.distanceTo(victim) <= RANGE && v.hasLineOfSight(victim);
            }
            if (saw) out.add(v);
        }
        return out;
    }
    /** Witnesses pop a heart (a sparkle for something big), anger at violence or gloom at breaking and taking, and turn to look. */
    private static void react(List<Villager> witnesses, Entity at, DeedKind kind) {
        var emote = kind.good ? kind.big() ? Emote.SPARKLE : Emote.HEART : kind.violent() ? Emote.ANGER : Emote.GLOOM;
        for (var w : witnesses) {
            VillageSocieties.emote(w, emote, w.getRandom().nextInt(16));
            if (at != null) {
                w.getBrain().setMemoryWithExpiry(MemoryModuleType.LOOK_TARGET, new EntityTracker(at, true), 60);
                w.getLookControl().setLookAt(at, 30, 30);
            }
        }
    }

    // -- standing ------------------------------------------------------------------------------------

    /** A player's standing score in a village, in tenths of a notice. */
    public static int score10(ServerLevel origin, String village, String player) {
        return Standing.score10(VillageQuests.favors(origin, village, player), book(origin).log(village, player), day(origin));
    }
    public static int tier(ServerLevel origin, String village, String player) { return Standing.tier(score10(origin, village, player)); }
    public static boolean unwelcome(ServerLevel origin, String village, UUID player) { return tier(origin, village, player.toString()) == Standing.UNWELCOME; }
    /** The board's standing line: "Good Neighbor · 4 notices answered", plus a note when deeds weigh on it. */
    public static String boardLine(ServerLevel origin, String village, String villageName, String player) {
        int favors = VillageQuests.favors(origin, village, player), score = score10(origin, village, player), tier = Standing.tier(score);
        var log = book(origin).log(village, player);
        boolean remembered = log != null && log.deeds().stream().anyMatch(d -> !d.good() && Standing.decay(d, day(origin)) > .1);
        return Standing.title(tier, villageName) + " · " + favors + (favors == 1 ? " notice" : " notices") + " answered"
                + (remembered && score < favors * 10 ? " (they remember what you did)" : "");
    }
    public static String boardHint(ServerLevel origin, String village, String villageName, String player) {
        return Standing.hint(score10(origin, village, player), villageName);
    }
    /** "Your standing: Good Neighbor", for the Village Ledger's news page; "" before anything happened. */
    public static String ledgerLine(ServerPlayer p, ServerLevel origin, String village, String villageName) {
        String me = p.getUUID().toString();
        if (VillageQuests.favors(origin, village, me) == 0 && book(origin).log(village, me) == null) return "";
        int tier = tier(origin, village, me);
        return "Your standing: " + Standing.title(tier, villageName) + (tier == Standing.UNWELCOME ? " (they remember what you did)" : "");
    }

    /**
     * After any deed or notice: a new tier is announced. Reaching a tier never reached before brings its
     * rewards (better prices all over the village, emeralds, Hero of the Village); falling only tells you so.
     */
    public static void changed(Place place, UUID player, int before) {
        var origin = place.origin(); String me = player.toString();
        int after = score10(origin, place.village(), me), was = Standing.tier(before), now = Standing.tier(after);
        if (was == now) return;
        var book = book(origin); var log = book.log(place.village(), me);
        if (log == null) log = DeedLog.create(me, "");
        var change = Standing.change(was, now, log.peakTier());
        if (change.reward()) save(origin, book.put(place.village(), log.peak(now)));
        var p = origin.getServer().getPlayerList().getPlayer(player);
        String name = villageName(place);
        if (change.reward()) {
            if (p != null) p.sendSystemMessage(Component.literal("★ " + name + ": you are now " + (now == 4 ? "the " : "a ") + Standing.title(now, name) + "!").withStyle(ChatFormatting.GOLD), false);
            int gossip = switch (now) { case 2 -> 5; case 3 -> 10; case 4 -> 20; default -> 0; };
            if (gossip > 0) for (var v : CompanionController.loaded) {
                var home = target(v).getAttached(HOME);
                if (home != null && home.village().equals(place.village()) && v.isAlive()) v.getGossips().add(player, GossipType.MAJOR_POSITIVE, gossip);
            }
            if (p != null && now == 3) giveItem(p, "minecraft:emerald", 8);
            if (p != null && now == 4) p.addEffect(new MobEffectInstance(MobEffects.HERO_OF_THE_VILLAGE, 48000, 0));
            return;
        }
        if (p == null) return;
        if (now == Standing.UNWELCOME) p.sendSystemMessage(Component.literal("✖ " + name + ": you are now Unwelcome. Nobody here will offer you work, and they remember what you did.").withStyle(ChatFormatting.RED), false);
        else if (change.fell()) p.sendSystemMessage(Component.literal("✖ " + name + ": folk are wary of you. You are " + (now == 0 ? "a Newcomer" : "a " + Standing.title(now, name)) + " here now.").withStyle(ChatFormatting.RED), false);
        else p.sendSystemMessage(Component.literal("★ " + name + ": you are " + (now == 4 ? "the " : "a ") + Standing.title(now, name) + " here again.").withStyle(ChatFormatting.GOLD), false);
    }

    // -- prices --------------------------------------------------------------------------------------

    /** What this resident's knowledge of the player's deeds adds to their vanilla reputation (prices, golems). */
    public static int reputation(Villager v, Player player) {
        if (!(v.level() instanceof ServerLevel level) || player == null) return 0;
        String key = v.getUUID() + "|" + player.getUUID();
        long now = level.getGameTime();
        var cached = prices.get(key);
        if (cached != null && now - cached[1] < PRICE_TICKS && now >= cached[1]) return (int) cached[0];
        var place = place(v); var log = log(place, player.getUUID());
        int value = log == null ? 0 : Standing.reputation(log.deeds(), VillageSocieties.id(v), day(place.origin()));
        if (prices.size() > 4096) prices.clear();
        prices.put(key, new long[]{value, now});
        return value;
    }

    // -- rumors --------------------------------------------------------------------------------------

    /** Two residents who stood together during a pass of {@code VillageSocieties.live}, and what they were doing. */
    public record Pair(String a, String routineA, String b, String routineB) {}
    /**
     * Once per pass of the village's daily life: catches up each deed's daily gossip, and lets neighbors
     * standing together pass on what they know.
     */
    public static void gossip(ServerLevel origin, Society society, List<Pair> pairs, long today) {
        var book = book(origin); var logs = book.logs(society.village());
        if (logs.isEmpty()) return;
        Rumors.Circles circles = null; var next = book; long check = origin.getGameTime() / 200;
        for (var log : logs.values()) {
            var updated = log; boolean day = false;
            for (var d : log.deeds()) {
                if (!d.fresh(today)) continue;
                var spread = d;
                if (spread.spread() < today) { if (circles == null) circles = Rumors.Circles.of(society); spread = Rumors.daily(spread, circles, today); day = true; }
                for (var pair : pairs) spread = Rumors.together(spread, society, pair.a(), pair.routineA(), pair.b(), pair.routineB(), today, check);
                if (spread != d) updated = updated.with(spread);
            }
            if (day) updated = updated.pruned(today);
            if (updated != log) next = next.put(society.village(), updated);
        }
        if (next != book) save(origin, next);
    }

    // -- residents bring it up -----------------------------------------------------------------------

    private static String key(Villager v, Player p) { return v.getUUID() + "|" + p.getUUID(); }
    private static int salt(Villager v, ServerPlayer p, long day) { return Math.floorMod(Objects.hash(v.getUUID(), p.getUUID(), day), 100); }
    private static String first(String name) { return TalkWorld.firstName(name); }

    /**
     * The first conversation after a resident learns of something the player did opens with it: "You're the
     * one who carried Liora to the cot!" Marks it told. Family of someone the player saved keep it in their
     * Journal for good. Null when there is nothing to bring up.
     */
    public static String reaction(Villager v, ServerPlayer p) {
        var place = place(v); var log = log(place, p.getUUID());
        if (log == null) return null;
        String me = VillageSocieties.id(v); long today = day(place.origin());
        var deed = Reactions.pick(log.deeds(), me, today);
        if (deed == null) return null;
        var know = deed.know(me); var society = VillageSocieties.of(v);
        var fill = new HashMap<String, String>();
        String victim = deed.victim();
        if (society != null && !victim.isEmpty() && society.has(victim)) {
            fill.put("victim", first(society.nameOf(victim)));
            String relation = society.relation(me, victim);
            if (society.get(me) != null && society.get(me).partner().equals(victim)) relation = "spouse";
            if (!relation.isEmpty()) fill.put("kin", Relations.kin(relation, society.get(victim).gender()).toLowerCase(Locale.ROOT));
        }
        if (society != null && !know.from().isEmpty() && society.has(know.from())) fill.put("teller", first(society.nameOf(know.from())));
        if (!deed.label().isEmpty()) fill.put(deed.kind() == DeedKind.HURT_PET || deed.kind() == DeedKind.KILLED_PET || deed.kind() == DeedKind.PET_KINDNESS ? "pet" : "house", deed.label());
        String line = null;
        if (deed.apologized() && !deed.good()) line = TalkWorld.say(v, p, "deed.apology.remembered", fill);
        for (var pool : Reactions.pools(deed.kind(), know, profile(v).personality(), v.isBaby(), salt(v, p, today)))
            if (line == null) line = TalkWorld.say(v, p, pool, fill);
        if (line == null) line = fallback(deed, know, fill);
        var told = know.markTold();
        if (know.how() == Know.FAMILY && !know.kept() && saved(deed.kind()) && fill.containsKey("victim")) {
            String memory = TalkWorld.say(v, p, Reactions.kept(deed.kind(), true), fill);
            if (memory == null) memory = p.getName().getString() + (deed.kind() == DeedKind.REVIVED ? " brought back" : " saved") + " my " + fill.getOrDefault("kin", "family") + " " + fill.get("victim") + ".";
            saveBond(v, p, bond(v, p).keep(today, memory));
            told = told.markKept();
        }
        var latest = book(place.origin()).log(place.village(), p.getUUID().toString());
        save(place.origin(), book(place.origin()).put(place.village(), latest.with(latest.find(deed.serial()).replace(me, told))));
        moods.put(key(v, p), deed.good() ? deed.kind().big() || know.how() <= Know.FAMILY ? Emote.SPARKLE : Emote.HEART : deed.kind().violent() ? Emote.ANGER : Emote.GLOOM);
        return line;
    }
    /** Whether a deed saved someone (brought them back, fought off a monster, carried them home), remembered by them and their family for good. */
    static boolean saved(DeedKind kind) { return kind == DeedKind.REVIVED || kind == DeedKind.SAVED_FROM_MONSTER || kind == DeedKind.RESCUED_COMPANION; }
    private static String fallback(Deed deed, Know know, Map<String, String> fill) {
        String victim = fill.getOrDefault("victim", "");
        if (deed.good()) return switch (know.how()) {
            case Know.INVOLVED -> "I haven't forgotten what you did for me. Thank you, truly.";
            case Know.FAMILY -> victim.isEmpty() ? "You helped my family. I won't forget it." : "You helped my " + fill.getOrDefault("kin", "family") + " " + victim + ". I won't forget it.";
            case Know.SEEN -> "I saw what you did. That was good of you.";
            default -> "Folk are saying good things about you. Keep it up!";
        };
        return switch (know.how()) {
            case Know.INVOLVED -> "I haven't forgotten what you did to me.";
            case Know.FAMILY -> "I know what you did to my family. Don't expect a warm welcome.";
            case Know.SEEN -> "I saw what you did. I'm watching you.";
            default -> "I've heard what you did. Word gets around, you know.";
        };
    }
    /** Whether the player is Unwelcome in this resident's village. */
    public static boolean unwelcome(Villager v, ServerPlayer p) {
        var place = place(v);
        return place != null && unwelcome(place.origin(), place.village(), p.getUUID());
    }
    /** A cold hello from someone in a village where the player is Unwelcome; null otherwise. */
    public static String cold(Villager v, ServerPlayer p) {
        if (!unwelcome(v, p)) return null;
        String line = null;
        for (var pool : Reactions.unwelcome(profile(v).personality(), v.isBaby(), salt(v, p, day(v.level())))) if (line == null) line = TalkWorld.say(v, p, pool, Map.of());
        moods.put(key(v, p), Emote.GLOOM);
        if (line != null) return line;
        return v.isBaby() ? "My mother says I shouldn't talk to you." : "Oh. It's you. Say what you need and move along.";
    }
    /** "How's your day?" from someone who'd rather not chat with an Unwelcome player; null otherwise. */
    public static String coldChat(Villager v, ServerPlayer p) {
        if (v.isBaby() || !unwelcome(v, p)) return null;
        String line = TalkWorld.say(v, p, "chat.unwelcome", Map.of());
        return line != null ? line : "I've nothing to share with you. Not today.";
    }
    /** What the notice board says to an Unwelcome player: a note pinned over the others. */
    public static String boardRefusal(ServerPlayer p, String villageName) {
        var lines = dev.villagefriends.talk.DialogueBank.current().pool("notice.unwelcome");
        if (!lines.isEmpty()) {
            var fill = Map.of("player", p.getName().getString(), "village", villageName);
            int start = p.getRandom().nextInt(lines.size());
            for (int n = 0; n < lines.size(); n++) {
                String text = Talk.fill(lines.get((start + n) % lines.size()), fill);
                if (text != null) return "A note is pinned over the others: \"" + text + "\"";
            }
        }
        return "Nobody here will give you work until they trust you again.";
    }
    /** The bubble a greeting opens with after a reaction or a cold hello, used once; null otherwise. */
    public static Emote mood(Villager v, ServerPlayer p) { return moods.remove(key(v, p)); }

    /** The saved resident keeps it in their Journal for good ({@code deed.kept.<kind>.self}, or {@code fallback}). */
    private static void keep(Villager v, ServerPlayer p, DeedKind kind, String fallback) {
        var place = place(v); var log = log(place, p.getUUID());
        if (log == null) return;
        String me = VillageSocieties.id(v); var before = log;
        // Once per deed: a second rescue the same day folds into the first and is already remembered.
        for (var d : log.deeds()) if (d.kind() == kind && d.involved().contains(me) && d.knows(me) && !d.know(me).kept())
            log = log.with(d.replace(me, d.know(me).markKept()));
        if (log == before) return;
        String memory = TalkWorld.say(v, p, Reactions.kept(kind, false), Map.of());
        saveBond(v, p, bond(v, p).keep(day(v.level()), memory != null ? memory : fallback));
        save(place.origin(), book(place.origin()).put(place.village(), log));
    }

    // -- apologies -----------------------------------------------------------------------------------

    /** The bad deed this resident could forgive: it happened to them, or it killed their family. */
    private static Deed grievance(Villager v, ServerPlayer p) {
        var place = place(v); var log = log(place, p.getUUID());
        if (log == null) return null;
        String me = VillageSocieties.id(v);
        for (int i = log.deeds().size() - 1; i >= 0; i--) {
            var d = log.deeds().get(i); var know = d.know(me);
            if (d.good() || d.apologized() || know == null || Standing.decay(d, day(place.origin())) < .1) continue;
            if (know.how() == Know.INVOLVED || know.how() == Know.FAMILY && d.kind() == DeedKind.KILLED_RESIDENT) return d;
        }
        return null;
    }
    /** "I'm sorry about what happened", for residents who have something to forgive. */
    public static List<FriendshipPayload.Choice> choices(Villager v, ServerPlayer p) {
        var b = bond(v, p);
        if (b.has("hurt")) return List.of(); // The existing "I'm sorry" covers a fresh hurt.
        var d = grievance(v, p);
        if (d == null || b.has("apology_tried:" + d.serial() + ":" + day(v.level()))) return List.of();
        return List.of(new FriendshipPayload.Choice("deed_apology", "I'm sorry about what happened", true));
    }
    public static boolean handle(ServerPlayer p, Villager v, String action) {
        if (!action.equals("deed_apology")) return false;
        var d = grievance(v, p);
        if (d == null) return false;
        long today = day(v.level()); var b = bond(v, p); var profile = profile(v);
        String held = BuiltInRegistries.ITEM.getKey(p.getMainHandItem().getItem()).toString();
        boolean gift = !p.getMainHandItem().isEmpty() && (held.equals(profile.love()) || GiftPreferences.value(profession(v), v.isBaby(), held) > 0) && !held.equals(profile.dislike());
        if (b.trust() >= 40 || gift || today - d.day() >= 3) {
            forgive(v, p, d);
            saveBond(v, p, bond(v, p).trust(3).remember(today, "You apologized for what happened, and I accepted."));
            String line = TalkWorld.say(v, p, v.isBaby() ? "deed.apology.accept.child" : "deed.apology.accept", Map.of());
            show(p, v, "talk", line != null ? line : "Thank you for saying it. I won't pretend it didn't happen, but I can let it go a little.",
                    "Apology accepted. What you did will fade faster.", false, Emote.SPARKLE);
        } else {
            saveBond(v, p, b.flag("apology_tried:" + d.serial() + ":" + today));
            String line = TalkWorld.say(v, p, "deed.apology.cool", Map.of());
            show(p, v, "talk", line != null ? line : "Words are easy. Give it some time.", "Not yet. Try again tomorrow, or with a gift they like.", false, Emote.DOTS);
        }
        return true;
    }
    private static void forgive(Villager v, ServerPlayer p, Deed d) {
        var place = place(v); var log = log(place, p.getUUID());
        if (log == null || log.find(d.serial()) == null) return;
        int before = score10(place.origin(), place.village(), p.getUUID().toString());
        save(place.origin(), book(place.origin()).put(place.village(), log.with(log.find(d.serial()).apologize())));
        changed(place, p.getUUID(), before);
    }
    /** The existing "I'm sorry" after a fresh hurt also apologizes for the deed that hurt them. */
    public static void apologized(Villager v, ServerPlayer p) {
        var d = grievance(v, p);
        if (d != null) forgive(v, p, d);
    }

    // -- hooks from existing systems -----------------------------------------------------------------

    private static List<String> resident(Villager v) { String id = VillageSocieties.id(v); return id.isEmpty() ? List.of() : List.of(id); }
    /** A player hit a resident (at most once a second). */
    public static void hit(ServerPlayer p, Villager v) { record(p, DeedKind.HIT_RESIDENT, place(v), "r:" + VillageSocieties.id(v), "", resident(v), 1, false, v); }
    public static void knockedOut(ServerPlayer p, Villager v) { record(p, DeedKind.KNOCKED_OUT_RESIDENT, place(v), "", "", resident(v), 1, false, v); }
    /** A knocked-out resident died: the player who knocked them out is blamed, even if they are offline. */
    public static void died(Villager v, String by) {
        if (by.isEmpty() || !(v.level() instanceof ServerLevel level)) return;
        var place = place(v);
        if (place == null) return;
        UUID player;
        try { player = UUID.fromString(by); } catch (IllegalArgumentException e) { return; }
        var online = level.getServer().getPlayerList().getPlayer(player);
        var log = log(place, player);
        String name = online != null ? online.getName().getString() : log == null ? "" : log.playerName();
        record(place, player, name, online != null && online.level() == level ? online : null, DeedKind.KILLED_RESIDENT, "", "", resident(v), 1, false, v);
    }
    public static void revived(ServerPlayer p, Villager v) {
        if (record(p, DeedKind.REVIVED, place(v), "", "", resident(v), 1, false, v) != null) keep(v, p, DeedKind.REVIVED, p.getName().getString() + " brought me back when I was knocked out.");
    }
    public static void bandaged(ServerPlayer p, Villager v) { record(p, DeedKind.BANDAGED, place(v), "r:" + VillageSocieties.id(v), "", resident(v), 1, false, v); }
    public static void rescued(ServerPlayer p, Villager v) {
        if (record(p, DeedKind.RESCUED_COMPANION, place(v), "r:" + VillageSocieties.id(v), "", resident(v), 1, false, v) != null)
            keep(v, p, DeedKind.RESCUED_COMPANION, p.getName().getString() + " came back for me when I fell on the road.");
    }
    /** A notice answered: folded into standing through the board's favors; recorded so residents talk about it. */
    public static void answered(ServerPlayer p, ServerLevel origin, String village, String poster, Villager posterEntity) {
        record(p, DeedKind.NOTICE_ANSWERED, new Place(origin, village), "", "", poster.isEmpty() ? List.of() : List.of(poster), 1, false, posterEntity);
    }
    public static void birthdayGift(ServerPlayer p, Villager v) { record(p, DeedKind.BIRTHDAY_GIFT, place(v), "r:" + VillageSocieties.id(v), "", resident(v), 1, false, v); }
    /** The first pat or treat of the day for a resident's pet. */
    public static void petKindness(ServerPlayer p, Entity pet) {
        var profile = VillagerPets.profile(pet);
        if (profile == null || !profile.owned() || !(pet.level() instanceof ServerLevel level)) return;
        record(p, DeedKind.PET_KINDNESS, petPlace(level, pet, profile.owner()), "pet:" + pet.getUUID(), profile.name(), List.of(profile.owner()), 1, false, pet);
    }

    /** A pet's village: where it is, or else its owner's hometown when the owner is about. */
    private static Place petPlace(ServerLevel level, Entity pet, String owner) {
        var here = place(level, pet.blockPosition());
        if (here != null) return here;
        for (var v : CompanionController.loaded) if (v.isAlive() && VillageSocieties.id(v).equals(owner)) return place(v);
        return null;
    }

    // -- hooks from events ---------------------------------------------------------------------------

    private static ServerPlayer player(DamageSource source) { return GuardController.attacker(source) instanceof ServerPlayer p ? p : null; }
    private static void hurt(LivingEntity entity, DamageSource source) {
        var p = player(source);
        if (p == null || !(entity.level() instanceof ServerLevel level)) return;
        if (entity instanceof IronGolem g && !g.isPlayerCreated() && g.isAlive())
            record(p, DeedKind.HIT_GOLEM, place(level, g.blockPosition()), "golem:" + g.getUUID(), "", List.of(), 1, false, g);
        else if (VillagerPets.residentPet(entity) && VillagerPets.profile(entity).owned() && entity.isAlive()) {
            var profile = VillagerPets.profile(entity);
            record(p, DeedKind.HURT_PET, petPlace(level, entity, profile.owner()), "pet:" + entity.getUUID(), profile.name(), List.of(profile.owner()), 1, false, entity);
        }
    }
    private static void died(LivingEntity entity, DamageSource source) {
        if (!(entity.level() instanceof ServerLevel level)) return;
        var p = player(source);
        if (p == null) return;
        if (entity instanceof IronGolem g && !g.isPlayerCreated()) { record(p, DeedKind.KILLED_GOLEM, place(level, g.blockPosition()), "", "", List.of(), 1, false, g); return; }
        if (VillagerPets.residentPet(entity) && VillagerPets.profile(entity).owned()) {
            var profile = VillagerPets.profile(entity);
            record(p, DeedKind.KILLED_PET, petPlace(level, entity, profile.owner()), "", profile.name(), List.of(profile.owner()), 1, false, entity);
            return;
        }
        if (entity instanceof Raider raider) {
            // Raiders have already left their raid by now: find it by where they fell.
            var raid = level.getRaids().getNearbyRaid(raider.blockPosition(), Raid.VALID_RAID_RADIUS_SQR);
            var at = raid == null ? null : place(level, raid.getCenter()) != null ? place(level, raid.getCenter()) : place(level, raider.blockPosition());
            if (at != null) {
                String key = "raid:" + level.dimension().identifier() + ":" + level.getRaids().getId(raid).orElse(System.identityHashCode(raid));
                var tally = raids.computeIfAbsent(raid, r -> new Tally(at, key, new HashSet<>()));
                tally.players().add(p.getUUID());
                record(p, DeedKind.RAID_DEFENDED, tally.place(), key, "", List.of(), 1, false, raider);
                return;
            }
        }
        if (entity instanceof Mob m && m instanceof Enemy) {
            Villager victim = m.getTarget() instanceof Villager v && target(v).hasAttached(HOME) ? v : null;
            if (victim == null) {
                var id = GuardController.recentVictim(m);
                if (id != null && level.getEntity(id) instanceof Villager v && target(v).hasAttached(HOME)) victim = v;
            }
            if (victim != null && victim.isAlive() && record(p, DeedKind.SAVED_FROM_MONSTER, place(victim), "r:" + VillageSocieties.id(victim), "", resident(victim), 1, victim.isBaby(), victim) != null)
                keep(victim, p, DeedKind.SAVED_FROM_MONSTER, p.getName().getString() + " saved me from a " + m.getName().getString().toLowerCase(Locale.ROOT) + ".");
        }
    }
    private static void tick(MinecraftServer server) {
        if (server.getTickCount() % 100 != 17 || raids.isEmpty()) return;
        for (var e : List.copyOf(raids.entrySet())) {
            var raid = e.getKey(); var tally = e.getValue();
            if (raid.isVictory()) {
                for (var id : tally.players()) {
                    var p = server.getPlayerList().getPlayer(id);
                    if (p != null) record(p, DeedKind.RAID_WON, tally.place(), tally.key(), "", List.of(), 1, false, null);
                }
                raids.remove(raid);
            } else if (raid.isOver() || raid.isStopped()) raids.remove(raid);
        }
    }

    // -- a resident's house: breaking and taking -----------------------------------------------------

    private static Optional<HouseBounds.HouseRef> house(ServerLevel level, BlockPos pos) {
        return HouseBounds.current().houseAt(level, pos).filter(h -> !h.residents().isEmpty());
    }
    private static Place place(ServerLevel level, HouseBounds.HouseRef house, BlockPos pos) {
        return VillageSettlements.book(level).villages().containsKey(house.village()) ? new Place(level, house.village()) : place(level, pos);
    }
    /** Item counts by id, for a container (both halves of a double chest). */
    private static Map<String, Integer> counts(Container c) {
        var out = new HashMap<String, Integer>();
        for (int i = 0; i < c.getContainerSize(); i++) {
            var stack = c.getItem(i);
            if (!stack.isEmpty()) out.merge(BuiltInRegistries.ITEM.getKey(stack.getItem()).toString(), stack.getCount(), Integer::sum);
        }
        return out;
    }
    private static Container container(Level level, BlockPos pos) {
        var state = level.getBlockState(pos);
        if (state.getBlock() instanceof ChestBlock chest) { var c = ChestBlock.getContainer(chest, state, level, pos, true); if (c != null) return c; }
        return level.getBlockEntity(pos) instanceof Container c ? c : null;
    }
    private static InteractionResult use(Player player, Level world, InteractionHand hand, BlockHitResult hit) {
        if (!(player instanceof ServerPlayer p) || !(world instanceof ServerLevel level) || hand != InteractionHand.MAIN_HAND || p.isCreative() || p.isSpectator()) return InteractionResult.PASS;
        var pos = hit.getBlockPos();
        if (!(level.getBlockEntity(pos) instanceof Container)) return InteractionResult.PASS;
        var house = house(level, pos);
        if (house.isEmpty()) return InteractionResult.PASS;
        var c = container(level, pos);
        if (c != null) opened.put(p.getUUID(), new Snapshot(level, pos, house.get(), counts(c), level.getGameTime()));
        return InteractionResult.PASS;
    }
    /** A player closed a container menu: whatever left a resident's container with them is theft. */
    public static void closed(Player player, AbstractContainerMenu menu) {
        if (!(player instanceof ServerPlayer p) || menu == p.inventoryMenu) return;
        var snapshot = opened.remove(p.getUUID());
        if (snapshot == null || p.level() != snapshot.level() || snapshot.level().getGameTime() - snapshot.tick() > 20 * 60 * 10) return;
        var c = container(snapshot.level(), snapshot.pos());
        if (c == null) return;
        var now = counts(c); int taken = 0;
        for (var e : snapshot.counts().entrySet()) taken += Math.max(0, e.getValue() - now.getOrDefault(e.getKey(), 0));
        if (taken > 0) stole(p, snapshot.level(), snapshot.house(), snapshot.pos(), taken);
    }
    private static void stole(ServerPlayer p, ServerLevel level, HouseBounds.HouseRef house, BlockPos pos, int items) {
        record(p, DeedKind.STOLE, place(level, house, pos), "house:" + house.village() + ":" + house.house(), house.name(), house.residents(), items, false, p);
    }
    private static boolean breaking(Level world, Player player, BlockPos pos, BlockState state, BlockEntity entity) {
        if (world instanceof ServerLevel level && player instanceof ServerPlayer p && entity instanceof Container && house(level, pos).isPresent()) {
            var c = container(level, pos);
            int items = c == null ? 0 : counts(c).values().stream().mapToInt(Integer::intValue).sum();
            if (items > 0) breaking.put(p.getUUID() + "|" + pos.asLong(), items);
        }
        return true;
    }
    private static void broke(Level world, Player player, BlockPos pos, BlockState state, BlockEntity entity) {
        if (!(world instanceof ServerLevel level) || !(player instanceof ServerPlayer p)) return;
        Integer items = breaking.remove(p.getUUID() + "|" + pos.asLong());
        var house = house(level, pos);
        if (items != null && house.isPresent()) stole(p, level, house.get(), pos, items);
        if (!state.is(BlockTags.BEDS) && !state.is(BlockTags.DOORS) && !PoiTypes.hasPoi(state)) return;
        var owners = HouseBounds.current().owners(level, pos);
        if (owners.isEmpty()) return;
        var ref = HouseBounds.current().houseAt(level, pos);
        var place = ref.map(h -> place(level, h, pos)).orElse(place(level, pos));
        String key = ref.map(h -> "house:" + h.village() + ":" + h.house()).orElse("home:" + pos.asLong());
        record(p, DeedKind.BROKE_HOME, place, key, ref.map(HouseBounds.HouseRef::name).orElse(""), owners, 1, false, p);
    }

    private Deeds() {}
}
