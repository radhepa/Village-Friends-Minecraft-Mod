package dev.villagefriends;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.npc.villager.Villager;
import dev.villagefriends.social.Gossip;
import static dev.villagefriends.VillageFriends.*;

public final class NarrativeEngine {
    private static FriendshipPayload.Choice choice(String id, String label, boolean enabled) { return new FriendshipPayload.Choice(id, label, enabled); }
    private static NarrativeContent.Story arc(Villager v) { return NarrativeContent.current().story(profile(v).story()); }
    public static String greeting(Villager v, ServerPlayer p) {
        var b = bond(v, p);
        if (CompanionController.state(v).downed()) return "I can't get up. Could you help me?";
        if (b.has("hurt")) return "I'm still shaken by what happened. I need to know you won't hurt me again.";
        if (b.has("adventure_return")) return "It's good to see you safely home. I still think about our adventure together.";
        if (b.has("activity:picnic")) return "I was remembering our picnic. It was nice having time just to be together.";
        String written = TalkWorld.line(v, p, "greet");
        String greeting = written != null ? written : Dialogue.greeting(name(v), b.level(state(v, p)), v.isBaby(), day(v.level()));
        var society = VillageSocieties.of(v); long today = day(v.level());
        String news = society == null ? "" : Gossip.greeting(society, profile(v).id(), today, salt(v, p, today));
        if (!news.isEmpty()) return greeting + " " + news;
        String village = VillageSettlements.reference(v,"chat",today);
        return village.isEmpty()?greeting:greeting+" "+village;
    }
    private static int salt(Villager v, ServerPlayer p, long day) { return Math.floorMod(Long.hashCode(day * 31 + p.getUUID().hashCode()) ^ v.getUUID().hashCode(), 9973); }
    /** The bubble a resident greets you with: a heart for dear friends, a sweat drop when they're shaken. */
    public static Emote greetingMood(Villager v, ServerPlayer p) {
        var b = bond(v, p);
        if (CompanionController.state(v).downed()) return Emote.SWEAT;
        if (b.has("hurt")) return Emote.GLOOM;
        int level = FriendshipLevels.level(state(v, p), b);
        return level >= FriendshipLevels.HEART_GREETING ? Emote.HEART : level >= 4 ? Emote.NOTE : Emote.EXCLAIM;
    }
    /** The bubble that goes with a reply on a talk topic. */
    public static Emote mood(Villager v, ServerPlayer p, String topic) {
        if (bond(v, p).has("hurt")) return Emote.DOTS;
        return switch (topic) {
            case "joke" -> Emote.NOTE;
            case "news" -> Emote.IDEA;
            case "adventure" -> Emote.SPARKLE;
            case "heart" -> {
                var society = VillageSocieties.of(v); String id = profile(v).id();
                var self = society == null ? null : society.get(id);
                yield self != null && (!self.partner().isEmpty() || !society.crush(id, day(v.level())).isEmpty()) ? Emote.BLUSH : Emote.DOTS;
            }
            default -> Emote.DOTS;
        };
    }
    public static String conversation(Villager v, ServerPlayer p, String topic) {
        var profile = profile(v); var b = bond(v, p); long today = day(v.level());
        if (v.isBaby()) {
            String said = TalkWorld.line(v, p, topic);
            // Children always mention home, like before.
            return ((said != null ? said : Dialogue.conversation(UUID.fromString(profile.id()), topic, profession(v), true, today, b.level(state(v, p))))
                    + " " + VillageSettlements.reference(v,topic,today)).strip();
        }
        if (b.has("hurt")) return "I'd like to talk about what happened before we pretend everything is fine. An apology would be a beginning.";
        var society = VillageSocieties.of(v); int salt = salt(v, p, today);
        if (topic.equals("news")) return society == null || !society.has(profile.id()) ? "I haven't settled anywhere yet, so I don't hear much news. Ask me again once I have a hometown."
                : Gossip.news(society, profile.id(), today, salt, FriendshipLevels.level(state(v, p), b) >= FriendshipLevels.SECRETS);
        if (topic.equals("heart")) return society == null || !society.has(profile.id()) ? "My heart? It's still looking for a place to call home, let alone a person."
                : Gossip.heart(society, profile.id(), today, salt);
        var personality = NarrativeContent.current().personality(profile.personality());
        var lines = personality.lines().get(topic);
        // Written-dialogue entries ("t:...") share the recent-lines memory; the personality pack's rotation ignores them.
        int packLines = (int) b.recentLines().stream().filter(id -> !id.startsWith("t:")).count();
        int start = Math.floorMod(Long.hashCode(today) + p.getUUID().hashCode() + packLines, lines.size());
        int index = start;
        for (int n = 0; n < lines.size(); n++) {
            int candidate = (start + n) % lines.size();
            if (!b.recentLines().contains(topic + ":" + candidate)) { index = candidate; break; }
        }
        var next = b.line(topic + ":" + index);
        if (topic.equals("chat") && state(v, p).points() >= 15 && !b.has("preferences")) {
            next = next.flag("preferences"); saveBond(v, p, next);
            return "You asked about me. I spend a lot of time " + profile.hobby() + ". I especially like " + itemName(profile.love())
                    + ", though " + itemName(profile.dislike()) + " isn't for me. I care a lot about " + profile.value() + ".";
        }
        saveBond(v, p, next);
        String villageLine=VillageSettlements.reference(v,topic,today+index);
        if (topic.equals("adventure") && b.has("adventure_defense")) return "When that attacker came toward us, I was frightened too. I'm glad we watched out for each other. Next time, let's leave room to turn back.";
        if (topic.equals("adventure") && b.has("adventure_return")) return "I remember our outing. Coming home together felt as important as setting out. I'd like to go again when you're ready.";
        if (topic.equals("chat") && b.has("activity:picnic") && today % 2 == 0) return "I was thinking about our picnic. There wasn't anything to finish or prove. I'd forgotten how much I needed an afternoon like that.";
        var story = arc(v);
        if (topic.equals("work") && story != null && shared(v).done(story.id() + "/" + story.requests().getFirst().id()))
            return "The " + story.requests().getFirst().title().toLowerCase() + " you helped with mattered to me. " + (b.chapter() >= 3 ? "You know why now. Thank you for listening as well as helping." : "When I find the words, I'd like to tell you why.");
        // Handwritten dialogue for this moment; the personality pack's own lines join in now and then.
        String said = TalkWorld.line(v, p, topic);
        String text = said != null && Math.floorMod(salt + index, 6) != 0 ? said : lines.get(index);
        var roll = new java.util.Random(salt * 31L + index + packLines);
        if(!villageLine.isEmpty() && (topic.equals("chat") || topic.equals("work") || topic.equals("adventure")) && (index%2==0 || today%3==1))text=villageLine+" "+text;
        var neighbors = shared(v).neighbors();
        String mention = society == null || !society.has(profile.id()) ? "" : Gossip.mention(society, profile.id(), topic, today, salt);
        if (!mention.isEmpty() && roll.nextInt(topic.equals("chat") ? 3 : 4) == 0) text += " " + mention;
        else if (topic.equals("chat") && !neighbors.isEmpty() && roll.nextInt(8) == 0) text += " I've also been keeping " + neighbors.getFirst() + " company around the village.";
        return text;
    }
    public static List<FriendshipPayload.Choice> choices(Villager v, ServerPlayer p, String tab) {
        var b = bond(v, p); var s = arc(v);
        if (tab.equals("question")) return TalkWorld.choices(v, p);
        if (tab.equals("journal")) return List.of(choice("journal", "Recent memories", true), choice("about", "About this resident", true), choice("story_notes", "Story notes", true), choice("talk_tab", "Back to talking", true));
        if (tab.equals("together")) return CompanionController.activityChoices(v, p);
        if (tab.equals("companion")) return CompanionController.choices(v, p);
        if (tab.equals("request")) return List.of(choice("deliver_side", "Deliver supplies", true), choice("cancel_request", "I can't help right now", true), choice("story", "Back to your story", true));
        if (tab.equals("story")) {
            if (v.isBaby() || s == null) return List.of(choice("talk_tab", "Let's just talk", true));
            return switch (b.chapter()) {
                case 0 -> List.of(choice("listen", "I'd like to hear more", true), choice("pledge", "You can count on me", true));
                case 1 -> List.of(choice("deliver", "Help with your request", true), choice("pledge", "I'll help when I can", !b.has("promise")), choice("cancel_request", "I can't promise that", b.has("promise")));
                case 2 -> List.of(choice("share", "I'm here to listen", b.visits() >= s.conditions().confessionVisits() && (!s.conditions().requireSharedExperience() || b.has("shared_experience"))), choice("together", "Let's spend time together", true), choice("request", "Anything else you need?", true));
                case 3 -> List.of(choice("encourage", "Your hopes matter to me", b.visits() >= s.conditions().endingVisits() && b.trust() >= s.conditions().endingTrust()), choice("practical", "Let's take one small step", b.visits() >= s.conditions().endingVisits() && b.trust() >= s.conditions().endingTrust()), choice("together", "Let's make more memories", true));
                default -> List.of(choice("request", "Anything else you need?", true), choice("together", "Let's spend time together", true), choice("companion", "Come on an adventure?", !v.isBaby()));
            };
        }
        int level = FriendshipLevels.level(state(v, p), b);
        return List.of(choice("chat", "How's your day?", true), choice("work", "Tell me about work", true),
                choice("adventure", "Talk about adventures", true), choice(b.has("hurt") || b.has("broken_promise") ? "apologize" : "joke", b.has("hurt") || b.has("broken_promise") ? "I'm sorry" : "Share a joke", true),
                new FriendshipPayload.Choice("news", "Any village news?", level >= FriendshipLevels.NEWS, "Unlocks at friendship Lv. " + FriendshipLevels.NEWS),
                new FriendshipPayload.Choice("heart", "Anyone special?", level >= FriendshipLevels.HEART_TO_HEART, "Unlocks at friendship Lv. " + FriendshipLevels.HEART_TO_HEART));
    }
    private static String storyText(Villager v, ServerPlayer p) {
        var s = arc(v); var b = bond(v, p);
        if (v.isBaby()) return "I'd like to hear your stories! My own adventures can wait until I'm grown.";
        if (s == null) return "My story pack is unavailable at the moment. We can still enjoy each other's company.";
        return switch (b.chapter()) {
            case 0 -> s.intro();
            case 1 -> s.requests().getFirst().prompt() + (b.has("promise") ? " I remember you said you'd help. There's no rush." : " Only if you have time.");
            case 2 -> b.visits() < s.conditions().confessionVisits() ? "Thank you for showing up for me. I'm still finding the words for why this matters. Visit on a few different days; I'd like us to get to know each other." : "There's something more personal behind this project. If you're willing to listen, I think I'm ready to tell you.";
            case 3 -> s.confide() + (b.visits() < s.conditions().endingVisits() ? " I'd like a little more time together before deciding what comes next." : " What do you think?");
            default -> b.has("ending:practical") ? s.practical() : s.encourage();
        };
    }
    public static boolean handle(ServerPlayer p, Villager v, String action) {
        var b = bond(v, p); var s = arc(v); long today = day(v.level());
        switch (action) {
            case "talk_tab" -> show(p, v, "talk", greeting(v, p), "Take your time.", false);
            case "story" -> show(p, v, "story", storyText(v, p), s == null ? "Story unavailable" : s.title() + " / Chapter " + Math.min(4, b.chapter() + 1), false);
            case "journal", "about", "story_notes" -> {
                String text = action.equals("about") ? about(v, p) : action.equals("story_notes") ? notes(v, p) : journal(v, p);
                show(p, v, "journal", text, "Journal / scroll to read", false);
            }
            case "apologize" -> {
                if (!b.has("hurt") && !b.has("broken_promise")) return false;
                saveBond(v, p, b.trust(b.has("hurt") ? 8 : 5).unflag("hurt").unflag("broken_promise").remember(today, "You apologized, and we began repairing trust."));
                show(p, v, "talk", "Thank you for saying that. I want to feel safe with you. What happens next will matter more than the words.", "A beginning toward repairing trust.", false);
            }
            case "listen", "pledge" -> {
                if (s == null || v.isBaby() || b.chapter() > 1 || (action.equals("listen") && b.chapter() != 0) || (action.equals("pledge") && b.has("promise"))) return false;
                var next = b.chapter(Math.max(1, b.chapter())).trust(b.chapter() == 0 ? 2 : 0).remember(today, "You listened to why " + s.title().toLowerCase() + " matters to me.");
                if (action.equals("pledge")) next = next.flag("promise");
                saveBond(v, p, next);
                show(p, v, "story", s.requests().getFirst().prompt(), "Hold the requested supplies, then offer them.", false);
            }
            case "deliver" -> {
                if (s == null || v.isBaby() || b.chapter() != 1) return false;
                deliver(p, v, s, s.requests().getFirst(), true);
            }
            case "share" -> {
                if (s == null || b.chapter() != 2 || b.visits() < s.conditions().confessionVisits() || (s.conditions().requireSharedExperience() && !b.has("shared_experience"))) return false;
                saveBond(v, p, b.chapter(3).trust(8).remember(today, "I trusted you with the feelings behind my project."));
                reward(v, p, 16); show(p, v, "story", s.confide(), "Trust grows through shared history.", false);
            }
            case "encourage", "practical" -> {
                if (s == null || b.chapter() != 3 || b.visits() < s.conditions().endingVisits() || b.trust() < s.conditions().endingTrust()) return false;
                // Commit the reward flag before inserting items; retries cannot issue another gift.
                saveBond(v, p, b.chapter(4).trust(10).flag("ending:" + action).flag("story_gift")
                        .remember(today, action.equals("encourage") ? "You encouraged me to try something I cared about." : "You helped me find a practical first step."));
                reward(v, p, 30); giveItem(p, s.gift(), 2);
                show(p, v, "story", (action.equals("encourage") ? s.encourage() : s.practical()) + " I saved a little " + itemName(s.gift()) + " for you. You matter to me too.", "Story complete. A gift from your friend.", false);
            }
            case "request" -> {
                if (s == null || b.chapter() < 2 || v.isBaby()) return false;
                var request = s.requests().stream().skip(1).filter(r -> !shared(v).done(s.id() + "/" + r.id())).findFirst();
                if (request.isEmpty()) { show(p, v, "story", "You've helped with everything I needed for this project. I'd love your company, though.", "All requests completed.", false); break; }
                var r = request.get();
                var next = b;
                for (String f : b.flags()) if (f.startsWith("request:")) next = next.unflag(f);
                saveBond(v, p, next.flag("request:" + r.id()).flag("promise"));
                show(p, v, "request", r.prompt(), r.title() + " / " + r.count() + " " + itemName(r.item()), false);
            }
            case "deliver_side" -> {
                if (s == null || b.chapter() < 2) return false;
                var r = s.requests().stream().skip(1).filter(q -> b.has("request:" + q.id())).findFirst();
                if (r.isEmpty()) return false; deliver(p, v, s, r.get(), false);
            }
            case "cancel_request" -> {
                if (!b.has("promise")) return false;
                var next = b.unflag("promise").trust(-5).flag("broken_promise").remember(today, "You told me you couldn't keep a promise. We can talk it through.");
                for (String f : b.flags()) if (f.startsWith("request:")) next = next.unflag(f);
                saveBond(v, p, next);
                show(p, v, "talk", "I'm disappointed, but thank you for telling me. I'd rather know than keep wondering. We can try again when you're ready.", "Trust can be repaired. No deadline penalty.", false);
            }
            default -> { return (action.startsWith("answer:") || action.equals("skip_question")) && TalkWorld.answer(p, v, action); }
        }
        return true;
    }
    private static void deliver(ServerPlayer p, Villager v, NarrativeContent.Story s, NarrativeContent.Request r, boolean first) {
        String key = s.id() + "/" + r.id(); var history = shared(v); var b = bond(v, p); long today = day(v.level());
        if (history.done(key)) {
            var next = b.unflag("promise").unflag("request:" + r.id());
            if (first) next = next.chapter(2);
            saveBond(v, p, next.remember(today, "We talked about help already given to my project."));
            show(p, v, "story", "Those supplies are already taken care of, thanks to " + history.outcomes().get(key) + ". I'd still like to get to know you in our own way.", "Your supplies were kept. Try a shared activity.", false); return;
        }
        var stack = p.getMainHandItem();
        if (!BuiltInRegistries.ITEM.getKey(stack.getItem()).toString().equals(r.item()) || stack.getCount() < r.count()) {
            show(p, v, first ? "story" : "request", r.prompt(), "Hold " + r.count() + " " + itemName(r.item()) + " in your main hand.", false); return;
        }
        if (!p.getAbilities().instabuild) stack.shrink(r.count());
        shared(v, history.complete(key, p.getName().getString()));
        var next = b.trust(6).flag("shared_experience").unflag("promise").unflag("request:" + r.id())
                .remember(today, "You helped with " + r.title().toLowerCase() + ".");
        if (first) next = next.chapter(2);
        int points = first ? 20 : 16;
        saveBond(v, p, next); reward(v, p, points);
        show(p, v, "story", r.thanks(), "+" + points + " friendship. Your help is remembered.", false);
    }
    public static String journal(Villager v, ServerPlayer p) {
        var b = bond(v, p); var text = new StringBuilder("OUR SHARED HISTORY\n");
        if (b.memories().isEmpty()) text.append("Our story is just beginning. Talk, listen, and spend time together.\n");
        for (int i = b.memories().size() - 1; i >= 0; i--) text.append(b.memories().get(i)).append('\n');
        return text.toString();
    }
    private static String about(Villager v, ServerPlayer p) {
        var profile = profile(v); var b = bond(v, p);
        return name(v) + "\n" + NarrativeContent.current().personality(profile.personality()).label() + "\nHobby: " + profile.hobby()
                + "\nHome village: " + (VillageSettlements.home(v)==null?"Not yet settled":VillageSettlements.home(v).name())
                + "\nValues: " + profile.value() + "\nLoves: " + itemName(profile.love()) + "\nDislikes: " + itemName(profile.dislike())
                + "\nTrust: " + b.trustLabel() + "\nVisits on different days: " + b.visits()
                + "\nFriendship: Lv. " + FriendshipLevels.level(state(v, p), b) + " " + FriendshipLevels.name(FriendshipLevels.level(state(v, p), b))
                + village(v)
                + "\nNeighbors: " + (shared(v).neighbors().isEmpty() ? "Still getting acquainted" : String.join(", ", shared(v).neighbors()));
    }
    private static String village(Villager v) {
        var society = VillageSocieties.of(v); String id = profile(v).id();
        if (society == null || !society.has(id)) return "\nResident friendships: " + shared(v).residentFriends().values().stream().filter(score -> score >= 3).count();
        return "\n" + String.join("\n", Gossip.about(society, id, day(v.level())));
    }
    private static String notes(Villager v, ServerPlayer p) {
        var s = arc(v); var b = bond(v, p);
        if (s == null) return "This resident's story pack is currently unavailable.";
        var text = new StringBuilder(s.title()).append("\nPersonal chapters: ").append(b.chapter()).append(" / 4\n");
        for (var r : s.requests()) text.append(shared(v).done(s.id() + "/" + r.id()) ? "Completed: " : "Request: ").append(r.title()).append(" - ").append(r.count()).append(' ').append(itemName(r.item())).append('\n');
        text.append("\nPersonal confession: ").append(s.conditions().confessionVisits()).append(" visiting days");
        text.append("\nEnding: ").append(s.conditions().endingVisits()).append(" visiting days, ").append(s.conditions().endingTrust()).append(" trust");
        text.append("\nClose friendship: share experiences and hear their story.\nBest friendship: finish their story across at least five visiting days.\nGifts alone cannot unlock these milestones.");
        return text.toString();
    }
    private NarrativeEngine() {}
}
