package dev.villagefriends;

import dev.villagefriends.social.Gossip;
import dev.villagefriends.social.Relations;
import dev.villagefriends.social.Society;
import dev.villagefriends.social.Townsfolk;
import dev.villagefriends.home.Homes;
import java.util.*;
import net.fabricmc.fabric.api.networking.v1.ServerPlayNetworking;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.npc.villager.Villager;
import static dev.villagefriends.VillageFriends.*;

/** Builds Village Ledger pages: the census of a village as the reading player knows it, and where everyone lives. */
public final class VillageLedger {
    private static final Map<UUID, Long> lastRequest = new HashMap<>();
    public static void clear() { lastRequest.clear(); }

    /** The ledger of the village the player is standing in. */
    public static void openHere(ServerPlayer player) { openAt(player, player.blockPosition()); }
    /** The ledger of the village around a place, such as a notice board. */
    public static void openAt(ServerPlayer player, net.minecraft.core.BlockPos pos) {
        var level = (ServerLevel) player.level();
        var record = VillageSettlements.discover(level, pos);
        if (record == null) { player.sendSystemMessage(Component.literal("The ledger's pages are blank here. Stand in a village to read about its residents."), true); return; }
        send(player, level, record, "");
    }
    /** The ledger of a resident's hometown, open at their page. */
    public static void open(ServerPlayer player, Villager v) {
        var home = target(v).getAttached(HOME); var origin = VillageSocieties.origin(v);
        var record = home == null || origin == null ? null : VillageSettlements.book(origin).villages().get(home.village());
        if (record == null) { player.sendSystemMessage(Component.literal(name(v) + " hasn't settled in a village yet."), true); return; }
        send(player, origin, record, profile(v).id());
    }
    public static void request(ServerPlayer player, LedgerRequestPayload request) {
        long now = player.level().getGameTime();
        if (lastRequest.getOrDefault(player.getUUID(), -10L) + 3 > now) return;
        lastRequest.put(player.getUUID(), now);
        var level = (ServerLevel) player.level();
        var record = VillageSettlements.book(level).villages().get(request.village());
        if (record != null) send(player, level, record, request.focus());
    }

    static void send(ServerPlayer player, ServerLevel level, VillageRecord record, String focus) {
        if (!ServerPlayNetworking.canSend(player, LedgerPayload.TYPE)) return;
        long today = day(level);
        var society = VillageSocieties.society(level, record.id());
        if (society == null) society = Society.create(record.id(), today);
        var known = target(player).getAttachedOrCreate(ACQUAINTANCES);
        var loaded = new HashMap<String, Villager>();
        for (var v : CompanionController.loaded) if (v.isAlive() && v.level() == player.level()) loaded.put(VillageSocieties.id(v), v);
        var entries = new ArrayList<LedgerPayload.Entry>();
        var homeless = Homes.homeless(level, record.id());
        for (var t : society.everyone()) {
            if (entries.size() >= LedgerPayload.MAX_RESIDENTS) break;
            var v = loaded.get(t.id());
            entries.add(new LedgerPayload.Entry(t.id(), t.name(), job(t), t.status(), t.adult(), known.getOrDefault(t.id(), -1), note(society, t, today, homeless), v == null ? -1 : v.getId(), t.gender()));
        }
        // Households short of room come first in the news.
        var news = new ArrayList<String>(Homes.needLines(level, record.id(), society));
        for (var n : society.recent(today, 60)) { if (news.size() >= 12) break; news.add("Day " + (n.day() + 1) + ": " + n.headline(society)); }
        if (news.isEmpty()) news.add("No news yet. Life in " + record.name() + " is just getting started.");
        var detail = society.has(focus) ? detail(society, focus, today, known.getOrDefault(focus, -1), loaded.get(focus), record.name(),
                Homes.ledgerLine(level, record.id(), society, focus)) : LedgerPayload.Detail.NONE;
        ServerPlayNetworking.send(player, new LedgerPayload(record.id(), record.name(), today, society.has(focus) ? focus : "", entries, news, detail));
    }
    private static String job(Townsfolk t) {
        if (!t.adult()) return "Child";
        return switch (t.job()) { case "none" -> "Neighbor"; case "nitwit" -> "Free Spirit"; default -> VillageProfessions.label(t.job()); };
    }
    /** One short line under a name in the list. */
    private static String note(Society s, Townsfolk t, long today, Set<String> homeless) {
        if (t.status().equals(Townsfolk.PASSED)) return "Remembered fondly";
        if (t.status().equals(Townsfolk.CURSED)) return "Zombified. Cure them to bring them home";
        if (t.home() && dev.villagefriends.social.Calendar.isBirthday(t.birthday(), today)) return "Birthday today!";
        if (t.home() && homeless.contains(t.id())) return "Looking for a home";
        if (!t.partner().isEmpty()) return (t.married() ? "Married to " : "Sweethearts with ") + s.nameOf(t.partner());
        if (!t.adult()) {
            var parents = s.family(t.id()).stream().filter(id -> s.relation(t.id(), id).equals("parent")).map(s::nameOf).toList();
            return parents.isEmpty() ? "Growing up in the village" : "Child of " + String.join(" & ", parents);
        }
        var family = s.family(t.id());
        // What this resident is to their closest relative: "Mother of Pip Ash", "Brother of Wren Hale".
        if (!family.isEmpty()) return Relations.kin(s.relation(family.getFirst(), t.id()), t.gender()) + " of " + s.nameOf(family.getFirst());
        return "Single";
    }
    private static LedgerPayload.Detail detail(Society s, String id, long today, int level, Villager loaded, String village, String home) {
        var t = s.get(id); var about = new ArrayList<String>();
        var personality = NarrativeContent.current().personality(t.personality());
        about.add(personality.label() + " · loves " + personality.hobby());
        about.add("Lives in " + village + " since day " + (t.joined() + 1) + (t.status().equals(Townsfolk.PASSED) ? " · passed away" : ""));
        if (home != null) about.add(home);
        if (t.home()) {
            // Their day, as the neighbors know it: when they're up, at work, at the bell and in bed.
            var day = dev.villagefriends.routine.Routine.day(ResidentRoutines.seed(id), t.job(), t.personality(), !t.adult(), today);
            about.add(day.chronotype().label + (loaded != null ? " · Now: " + ResidentRoutines.doing(loaded) : ""));
            about.add((day.marketDay() ? "Market Day: " : "Today: ") + dev.villagefriends.routine.Routine.summary(day));
        }
        about.addAll(Gossip.about(s, id, today));
        String crush = s.crush(id, today);
        if (!crush.isEmpty() && level >= FriendshipLevels.SECRETS) about.add("Secretly smitten with " + s.nameOf(crush) + " (shh!)");
        else if (!crush.isEmpty()) about.add("Seems a little distracted lately...");
        if (level >= FriendshipLevels.PREFERENCES && loaded != null) {
            var profile = profile(loaded);
            about.add("Favorite gift: " + itemName(profile.love()) + " · Dislikes: " + itemName(profile.dislike()));
        } else if (level < FriendshipLevels.PREFERENCES) about.add("Become acquaintances to learn their favorite things.");
        about.add(level < 0 ? "You haven't met yet." : "Your friendship: Lv. " + level + " " + FriendshipLevels.name(level));
        var ties = new ArrayList<LedgerPayload.Tie>();
        for (var other : s.living()) {
            if (other.id().equals(id)) continue;
            boolean family = !s.relation(id, other.id()).isEmpty() || t.partner().equals(other.id());
            ties.add(new LedgerPayload.Tie(other.id(), other.name(), s.affinity(id, other.id(), today), Relations.label(s, id, other.id(), today), family));
        }
        ties.sort(Comparator.comparing(LedgerPayload.Tie::family).reversed().thenComparing(Comparator.comparingInt(LedgerPayload.Tie::affinity).reversed()).thenComparing(LedgerPayload.Tie::name));
        return new LedgerPayload.Detail(id, about, ties);
    }
    private VillageLedger() {}
}
