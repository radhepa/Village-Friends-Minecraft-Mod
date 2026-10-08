package dev.villagefriends.rpg;

import dev.villagefriends.Emote;
import dev.villagefriends.FriendshipPayload;
import dev.villagefriends.GuardController;
import dev.villagefriends.VillageFriends;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.entity.npc.villager.Villager;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

/**
 * Jobs from villagers, told through Village Friends' own conversation window: an "Any work for me?"
 * choice on the talk tab opens an "rpg" tab where the resident offers a job, takes it back, or pays up.
 */
public final class Quests {
    private Quests() {}
    /** The job each player is looking at but hasn't accepted yet. */
    private static final Map<UUID, Quest> OFFERS = new HashMap<>();
    static void clear() { OFFERS.clear(); }

    static List<String> pools(Villager v) { return v.isBaby() ? List.of() : QuestBook.pools(VillageFriends.profession(v), GuardController.isGuard(v)); }
    private static Quest from(ServerPlayer p, Villager v) {
        String id = v.getUUID().toString();
        return Rpg.sheet(p).quests().stream().filter(q -> q.giver().equals(id)).findFirst().orElse(null);
    }
    private static boolean ready(ServerPlayer p, Quest q) { return q.kind().equals("gather") ? Life.count(p, Life.item(q.target())) >= q.need() : q.done(); }

    /** The extra choice on the talk tab, or null for villagers who never have work. */
    public static FriendshipPayload.Choice talkChoice(Villager v, ServerPlayer p) {
        var q = from(p, v);
        if (q != null) return new FriendshipPayload.Choice("rpg_work", ready(p, q) ? "About that job... (done!)" : "About that job...", true, q.label());
        if (pools(v).isEmpty()) return null;
        return new FriendshipPayload.Choice("rpg_work", "Any work for me?", true, "Jobs give experience, emeralds and friendship");
    }
    /** Choices on the "rpg" tab. */
    public static List<FriendshipPayload.Choice> choices(Villager v, ServerPlayer p) {
        var offer = OFFERS.get(p.getUUID());
        if (offer != null && offer.giver().equals(v.getUUID().toString())) {
            boolean room = Rpg.sheet(p).quests().size() < Balance.maxQuests(Rpg.sheet(p).level());
            return List.of(new FriendshipPayload.Choice("rpg_accept", "I'll do it", room, "You already have " + Balance.maxQuests(Rpg.sheet(p).level()) + " jobs"),
                    new FriendshipPayload.Choice("talk_tab", "Not right now", true));
        }
        var q = from(p, v);
        if (q != null) return List.of(new FriendshipPayload.Choice("rpg_turnin", q.kind().equals("gather") ? "Here, I brought them" : "It's done", ready(p, q), "Not finished yet"),
                new FriendshipPayload.Choice("rpg_abandon", "I can't do this one", true),
                new FriendshipPayload.Choice("talk_tab", "I'm still on it", true));
        return List.of(new FriendshipPayload.Choice("talk_tab", "Back to talking", true));
    }

    public static void handle(ServerPlayer p, Villager v, String action) {
        var s = Rpg.sheet(p); long today = VillageFriends.day(v.level()); String who = v.getUUID().toString();
        switch (action) {
            case "rpg_work" -> {
                OFFERS.remove(p.getUUID());
                var q = from(p, v);
                if (q != null) {
                    String have = q.kind().equals("gather") ? Life.count(p, Life.item(q.target())) + "/" + q.need() : q.have() + "/" + q.need();
                    show(p, v, ready(p, q) ? "Is that what I think it is?" : "How's it coming along? No rush, I know it's no small thing.",
                            q.label() + " (" + have + ")", ready(p, q) ? Emote.EXCLAIM : Emote.QUESTION);
                    return;
                }
                var pools = pools(v);
                if (pools.isEmpty()) { show(p, v, "I don't have any work for you, but thank you for asking.", "", Emote.NOTE); return; }
                if (s.mark("took:" + who) == today + 1) { show(p, v, "That's all the work I have today. Come back tomorrow?", "One job per villager per day.", Emote.DOTS); return; }
                long seed = v.getUUID().getMostSignificantBits() ^ v.getUUID().getLeastSignificantBits() * 31 ^ today * 0x9E3779B97F4A7C15L ^ p.getUUID().hashCode();
                var offer = QuestBook.offer(pools, seed, s.level(), who + ":" + today, who, VillageFriends.name(v), VillageFriends.profession(v));
                if (offer == null) { show(p, v, "Nothing I'd trust you with yet. Come back when you've seen a bit more of the world.", "", Emote.DOTS); return; }
                OFFERS.put(p.getUUID(), offer);
                double barter = 1 + Balance.BARTER_REWARD * s.skill(Skill.BARTERING);
                show(p, v, QuestBook.flavor(VillageFriends.profession(v), GuardController.isGuard(v), seed) + " " + offer.label() + "?",
                        "Reward: " + Math.round(offer.xp() * barter) + " XP, " + Math.round(offer.emeralds() * barter) + " emeralds, +" + offer.friendship() + " friendship", Emote.IDEA);
            }
            case "rpg_accept" -> {
                var offer = OFFERS.remove(p.getUUID());
                if (offer == null || !offer.giver().equals(who) || from(p, v) != null || s.quests().size() >= Balance.maxQuests(s.level())) { show(p, v, "Let's talk about it another time.", "", Emote.DOTS); return; }
                var list = new ArrayList<>(s.quests()); list.add(offer);
                var next = s.withQuests(list);
                for (var key : s.marks().keySet()) if (key.startsWith("took:") && s.mark(key) <= today) next = next.unmark(key);
                Rpg.set(p, next.mark("took:" + who, today + 1));
                track(p);
                show(p, v, "Thank you! Come and find me when it's done.", "Job taken: " + offer.label() + ". Track it on your character sheet (K).", Emote.HEART);
            }
            case "rpg_turnin" -> turnIn(p, v);
            case "rpg_abandon" -> { abandon(p, who + ":"); show(p, v, "Oh. Well, thank you for trying.", "Job abandoned.", Emote.GLOOM); }
            default -> {}
        }
    }
    private static void turnIn(ServerPlayer p, Villager v) {
        var q = from(p, v);
        if (q == null || !ready(p, q)) { show(p, v, "Not quite yet, I think.", "", Emote.QUESTION); return; }
        if (q.kind().equals("gather")) Life.take(p, Life.item(q.target()), q.need());
        var s = Rpg.sheet(p);
        Rpg.set(p, s.withQuests(s.quests().stream().filter(x -> x != q).toList()).mark("quests_done", s.mark("quests_done") + 1));
        double barter = 1 + Balance.BARTER_REWARD * s.skill(Skill.BARTERING);
        long xp = Math.round(q.xp() * barter); int emeralds = (int) Math.round(q.emeralds() * barter);
        Progress.xp(p, xp, null);
        Progress.skill(p, Skill.BARTERING, 40);
        VillageFriends.giveItem(p, "minecraft:emerald", emeralds);
        VillageFriends.reward(v, p, q.friendship());
        p.level().playSound(null, p.blockPosition(), SoundEvents.VILLAGER_CELEBRATE, SoundSource.NEUTRAL, 1, 1);
        show(p, v, "You actually did it! Here, you've more than earned this.", "Job done: +" + xp + " XP, +" + emeralds + " emeralds, +" + q.friendship() + " friendship", Emote.HEART);
    }
    /** Drops a job by id (or id prefix, used for "this villager's job"). */
    static void abandon(ServerPlayer p, String id) {
        var s = Rpg.sheet(p);
        var left = s.quests().stream().filter(q -> !q.id().startsWith(id)).toList();
        if (left.size() != s.quests().size()) Rpg.set(p, s.withQuests(left));
    }
    private static void show(ServerPlayer p, Villager v, String line, String status, Emote emote) {
        VillageFriends.show(p, v, "rpg", line, status, false, emote);
    }

    // -- progress ----------------------------------------------------------------------------------
    /** Counts progress for jobs of one kind ("" target matches any), announcing any that just finished. */
    public static void advance(ServerPlayer p, String kind, String target, int n) {
        var s = Rpg.sheet(p);
        var next = s.mapQuests(q -> q.kind().equals(kind) && (target.isEmpty() || q.target().equals(target)) && !q.done() ? q.progress(n) : q);
        if (next == s) return;
        Rpg.set(p, next);
        announce(p, s, next);
    }
    /** Once a second: gather counts from the inventory, explore jobs from where the player stands. */
    static void track(ServerPlayer p) {
        var s = Rpg.sheet(p);
        if (s.quests().isEmpty()) return;
        String biome = p.level().getBiome(p.blockPosition()).unwrapKey().map(k -> "biome:" + k.identifier()).orElse("");
        String dim = "dim:" + p.level().dimension().identifier();
        var next = s.mapQuests(q -> switch (q.kind()) {
            case "gather" -> q.withHave(Life.count(p, Life.item(q.target())));
            case "explore" -> q.target().equals(biome) || q.target().equals(dim) ? q.withHave(1) : q;
            default -> q;
        });
        if (next == s) return;
        Rpg.set(p, next);
        announce(p, s, next);
    }
    private static void announce(ServerPlayer p, Sheet before, Sheet after) {
        for (int i = 0; i < after.quests().size(); i++) {
            var q = after.quests().get(i);
            if (q.done() && i < before.quests().size() && !before.quests().get(i).done()) {
                p.sendSystemMessage(Component.literal("Job ready: " + q.label() + ". Return to " + q.giverName() + ".").withStyle(ChatFormatting.YELLOW));
                p.level().playSound(null, p.blockPosition(), SoundEvents.NOTE_BLOCK_BELL.value(), SoundSource.PLAYERS, .6F, 1.4F);
            }
        }
    }
}
