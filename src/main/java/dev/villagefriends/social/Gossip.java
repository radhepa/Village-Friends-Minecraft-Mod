package dev.villagefriends.social;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/**
 * What residents say about each other. Lines name real neighbors and follow the village's actual
 * friendships, families, romances and news, so every village talks about its own people.
 * {@code salt} varies the wording from day to day and from player to player.
 */
public final class Gossip {
    private static String pick(int salt, String... lines) { return lines[Math.floorMod(salt, lines.length)]; }
    private static String first(String name) { int space = name.indexOf(' '); return space > 0 ? name.substring(0, space) : name; }
    private static String job(String job) {
        if (job.equals("none") || job.equals("nitwit")) return "";
        return job.replace('_', ' ').toLowerCase(Locale.ROOT);
    }
    private static String kinWord(Society s, String me, String other) {
        var t = s.get(other); String relation = s.relation(me, other);
        if (t == null || relation.isEmpty()) return "";
        return Relations.kin(relation, t.gender()).toLowerCase(Locale.ROOT);
    }

    /** A remark about a neighbor for everyday chat, work or adventure talk; "" if there's nobody to mention. */
    public static String mention(Society s, String me, String topic, long day, int salt) {
        var self = s.get(me);
        if (self == null || s.living().size() < 2) return "";
        String partner = self.partner(), friend = s.bestFriend(me, day), rival = s.rival(me, day);
        var family = s.family(me).stream().filter(id -> !id.equals(partner)).toList();
        if (!self.adult()) {
            if (!friend.isEmpty() && salt % 2 == 0) return pick(salt, "Me and " + first(s.nameOf(friend)) + " are building a fort behind the haystacks. It's secret. Oops.",
                    first(s.nameOf(friend)) + " can whistle with two fingers! I'm still practicing.");
            if (!family.isEmpty()) return "My " + kinWord(s, me, family.getFirst()) + " " + first(s.nameOf(family.getFirst())) + " says I have to be home before the bell. Every. Single. Day.";
            return "";
        }
        String p = first(s.nameOf(partner)), f = first(s.nameOf(friend));
        return switch (topic) {
            case "work" -> {
                var colleague = s.living().stream().filter(t -> !t.id().equals(me) && t.adult() && t.job().equals(self.job()) && !job(self.job()).isEmpty()).findFirst();
                if (colleague.isPresent() && salt % 2 == 0) yield first(colleague.get().name()) + " is a " + job(self.job()) + " too. We trade tips, and complaints.";
                if (!partner.isEmpty()) yield p + " brings me lunch while I work. Small kindnesses add up.";
                if (!friend.isEmpty()) yield f + " always stops by to see how the work is going. It helps more than you'd think.";
                yield "";
            }
            case "adventure" -> {
                if (!partner.isEmpty() && salt % 2 == 0) yield p + " and I keep saying we'll travel somewhere together. Maybe this year.";
                if (!friend.isEmpty()) yield f + " says I should see the ocean someday. Maybe we'll go together.";
                yield "";
            }
            default -> {
                var lines = new ArrayList<String>();
                if (!partner.isEmpty()) lines.add(self.married()
                        ? pick(salt, p + " made breakfast for me this morning. I'm a lucky one.", p + " and I are thinking of planting a little garden together.", "I keep finding wildflowers on my doorstep. " + p + " pretends not to know anything about it.")
                        : pick(salt, "I'm meeting " + p + " by the bell later. Don't tell anyone I've been practicing what to say.", "Have you noticed " + p + "'s laugh? No? Just me, then."));
                if (!family.isEmpty()) {
                    String kid = family.getFirst(), word = kinWord(s, me, kid), name = first(s.nameOf(kid));
                    lines.add(switch (s.relation(me, kid)) {
                        case "child" -> "My " + word + " " + name + " has been chasing chickens all morning. Where does all that energy come from?";
                        case "parent" -> "My " + word + " " + name + " still checks whether I've eaten. Some things never change.";
                        case "sibling" -> "My " + word + " " + name + " borrowed my good scarf again. Family!";
                        default -> "I had supper with my " + word + " " + name + ". Family keeps a person steady.";
                    });
                }
                if (!friend.isEmpty()) lines.add(pick(salt, "I had lunch with " + f + " today. We always end up laughing about nothing.",
                        f + " is the first person I'd tell good news to.", f + " and I sat by the well until the lanterns came on."));
                if (!rival.isEmpty()) lines.add(first(s.nameOf(rival)) + " and I don't see eye to eye. I'm trying to be patient. Trying.");
                yield lines.isEmpty() ? "" : lines.get(Math.floorMod(salt / 3, lines.size()));
            }
        };
    }

    /** Answer to "Any village news?". Close friends hear the secrets too. */
    public static String news(Society s, String me, long day, int salt, boolean secrets) {
        var fresh = s.recent(day, 7).stream().filter(n -> !n.kind().equals("family") && !n.kind().equals("grew_up") || n.day() >= day - 2).toList();
        if (!fresh.isEmpty()) return tell(s, me, fresh.get(Math.floorMod(salt, Math.min(3, fresh.size()))));
        if (secrets) {
            for (var t : s.living()) {
                String crush = s.crush(t.id(), day);
                if (!crush.isEmpty() && !t.id().equals(me) && !crush.equals(me))
                    return "Between you and me... " + first(t.name()) + " keeps finding reasons to walk past " + first(s.nameOf(crush)) + "'s door. Someone's smitten.";
            }
        }
        var pairs = new ArrayList<String[]>();
        for (var e : s.ties().entrySet()) if (e.getValue().together() >= 8 && day - e.getValue().lastTogether() <= 7) pairs.add(e.getKey().split("\\|"));
        if (!pairs.isEmpty()) {
            var pair = pairs.get(Math.floorMod(salt, pairs.size()));
            if (s.has(pair[0]) && s.has(pair[1]) && s.get(pair[0]).living() && s.get(pair[1]).living())
                return pair[0].equals(me) || pair[1].equals(me) ? "Quiet week. I've been spending most of it with " + first(s.nameOf(pair[0].equals(me) ? pair[1] : pair[0])) + ", if I'm honest."
                        : "Quiet week. " + first(s.nameOf(pair[0])) + " and " + first(s.nameOf(pair[1])) + " have been spending a lot of time together, though.";
        }
        return pick(salt, "Nothing much! The well still squeaks, the bread still rises. I like a quiet village.",
                "No news is good news, my grandmother used to say. I think she just liked naps.");
    }
    private static String tell(Society s, String me, News n) {
        String a = first(s.nameOf(n.a())), b = first(s.nameOf(n.b())), c = first(s.nameOf(n.c()));
        boolean mine = n.a().equals(me) || n.b().equals(me), parent = n.b().equals(me) || n.c().equals(me);
        String other = n.a().equals(me) ? b : a;
        return switch (n.kind()) {
            case "sweethearts" -> mine ? "Well... since you ask. " + other + " and I are sweethearts now! I keep smiling at nothing."
                    : "Have you heard? " + a + " and " + b + " fell in love! I saw them sharing a pie by the well. Sweet, isn't it?";
            case "married" -> mine ? other + " and I got married! It was small and lovely. You should have seen the flowers."
                    : a + " and " + b + " got married! The whole village turned out. I may have cried a little.";
            case "born" -> parent ? "We have a new little one: " + a + "! I haven't slept, and I've never been happier."
                    : b + (c.isEmpty() ? "" : " and " + c) + " welcomed a baby, " + a + "! The village is getting livelier.";
            case "passed" -> "We lost " + a + " recently. The village feels quieter. Remember " + a + " kindly tonight.";
            case "cursed" -> "It's " + a + "... the zombies got " + a + ". A splash of weakness and a golden apple could still bring " + a + " home. Please, if you can.";
            case "cured" -> a + " is back to normal! Cured and home again. We had a little party.";
            case "quarrel" -> mine ? other + " and I had words. I said things I didn't mean. I'll make it right... eventually."
                    : a + " and " + b + " had a quarrel near the well. I stayed out of it. Mostly.";
            case "friends", "best_friends" -> mine ? other + " and I have become thick as thieves lately. I'm glad."
                    : a + " and " + b + " have become inseparable. It's lovely to see.";
            case "grew_up" -> n.a().equals(me) ? "I'm all grown up now! Everyone keeps saying so, anyway." : "Can you believe " + a + " is all grown up? It feels like yesterday " + a + " was playing tag by the bell.";
            case "arrived" -> n.a().equals(me) ? "Me! I'm the news. I only just settled here." : "There's a new face in town: " + a + ". Say hello if you pass by.";
            case "family" -> mine ? "I came here with family. It's good to start somewhere new together." : a + " and " + b + " moved here together. Family is a good thing to bring along.";
            default -> "Oh, the usual comings and goings.";
        };
    }

    /** Answer to "Anyone special in your life?": their love life and family, in their own words. */
    public static String heart(Society s, String me, long day, int salt) {
        var self = s.get(me);
        if (self == null) return "My heart? Busy with today's chores, mostly.";
        if (!self.adult()) return pick(salt, "Ew! Love is for grown-ups. I like frogs.", "Grown-ups say I'll understand when I'm older. I understand frogs right now.");
        String partner = self.partner(), crush = s.crush(me, day);
        String love;
        if (!partner.isEmpty() && self.married())
            love = first(s.nameOf(partner)) + " and I have been married since day " + (self.partnerSince() + 1) + ". Every morning still feels like a small festival.";
        else if (!partner.isEmpty())
            love = "Can I tell you something? " + first(s.nameOf(partner)) + " and I are sweethearts. We're taking it slow... but not too slow.";
        else if (self.kin().entrySet().stream().anyMatch(e -> e.getValue().equals("spouse") && s.get(e.getKey()) != null && !s.get(e.getKey()).living())) {
            String late = self.kin().entrySet().stream().filter(e -> e.getValue().equals("spouse") && !s.get(e.getKey()).living()).findFirst().get().getKey();
            love = "I still talk to " + first(s.nameOf(late)) + " sometimes, by the bell where we met. Love doesn't really leave, does it?";
        }
        else if (!crush.isEmpty())
            love = "Don't laugh... I think I'm falling for " + first(s.nameOf(crush)) + ". Every time " + first(s.nameOf(crush)) + " walks by the well, I forget what I was saying.";
        else if (!Chemistry.romantic(me))
            love = pick(salt, "I'm happy as I am. Good friends, good work, a warm bed. My heart feels full enough.", "Romance? Not for me, and that's all right. I have my friends and my little routines.");
        else love = pick(salt, "No one special yet. Love takes its time, I think. When it comes, I'd like it to feel like coming home.",
                    "Not yet. But I'm in no hurry. The best things in this village grow slowly.");
        var family = s.family(me).stream().filter(id -> !id.equals(partner)).limit(3).toList();
        if (family.isEmpty()) return love;
        var names = new ArrayList<String>();
        for (String id : family) names.add("my " + kinWord(s, me, id) + " " + first(s.nameOf(id)));
        return love + " And there's " + join(names) + ". Family keeps me steady.";
    }

    /** A breathless "did you hear?" for the first hello after something big happened, or "". */
    public static String greeting(Society s, String me, long day, int salt) {
        for (var n : s.recent(day, 1)) {
            if (!List.of("sweethearts", "married", "born", "cured").contains(n.kind()) || salt % 2 != 0) continue;
            return "Oh! Did you hear? " + tell(s, me, n);
        }
        return "";
    }

    /** Family, partner and friends as plain lines for the Journal and the Village Ledger. */
    public static List<String> about(Society s, String me, long day) {
        var self = s.get(me); var lines = new ArrayList<String>();
        if (self == null) return lines;
        String partner = self.partner();
        if (!partner.isEmpty()) lines.add((self.married() ? "Married to " : "Sweethearts with ") + s.nameOf(partner));
        else lines.add(self.adult() ? "Single" : "Too young for romance");
        var family = s.family(me).stream().filter(id -> !id.equals(partner)).toList();
        if (!family.isEmpty()) {
            var names = new ArrayList<String>();
            for (String id : family) names.add(Relations.kin(s.relation(me, id), s.get(id).gender()) + " " + s.nameOf(id));
            lines.add("Family: " + String.join(", ", names));
        }
        String friend = s.bestFriend(me, day), rival = s.rival(me, day);
        if (!friend.isEmpty()) lines.add("Closest friend: " + s.nameOf(friend) + " (" + Relations.feeling(s.affinity(me, friend, day)).toLowerCase(Locale.ROOT) + ")");
        if (!rival.isEmpty()) lines.add("Not fond of: " + s.nameOf(rival));
        return lines;
    }
    private static String join(List<String> parts) {
        if (parts.size() == 1) return parts.getFirst();
        return String.join(", ", parts.subList(0, parts.size() - 1)) + " and " + parts.getLast();
    }
    private Gossip() {}
}
