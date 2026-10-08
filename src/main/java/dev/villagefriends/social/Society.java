package dev.villagefriends.social;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import java.util.*;

/**
 * Everyone who lives in one village and how they feel about each other.
 *
 * <p>Every pair of residents has a relationship meter from -100 to 100. It starts at polite
 * neighborliness and grows over the days they have known each other toward a level set by their
 * {@link Chemistry}; days spent side by side raise it and quarrels dent it for a while. Family
 * starts close. Only the shared days and quarrels are saved ({@link Tie}); the rest is computed, so
 * a village of any history costs little to store.
 *
 * <p>Single, compatible adults who are not related can fall in love once they have known each other
 * for their pair's own 50 to 1000 days and like each other enough; some never do. Sweethearts marry
 * after a courtship. Newcomers may arrive with family; babies are born to the parents who had them.
 */
public record Society(String village, Map<String, Townsfolk> folk, Map<String, Tie> ties, List<News> news, long day) {
    public static final int MAX_NEWS = 40, CATCH_UP = 30, WEB = 120;
    public static final int LOVE_AFFINITY = 50, CRUSH_AFFINITY = 40, MARRY_AFFINITY = 65;
    public static final Codec<Society> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.STRING.fieldOf("village").forGetter(Society::village),
            Codec.unboundedMap(Codec.STRING, Townsfolk.CODEC).optionalFieldOf("folk", Map.of()).forGetter(Society::folk),
            Codec.unboundedMap(Codec.STRING, Tie.CODEC).optionalFieldOf("ties", Map.of()).forGetter(Society::ties),
            News.CODEC.listOf().optionalFieldOf("news", List.of()).forGetter(Society::news),
            Codec.LONG.optionalFieldOf("day", -1L).forGetter(Society::day)
    ).apply(i, Society::new));

    public Society {
        folk = Map.copyOf(folk); ties = Map.copyOf(ties);
        news = List.copyOf(news.subList(Math.max(0, news.size() - MAX_NEWS), news.size()));
    }
    public static Society create(String village, long day) { return new Society(village, Map.of(), Map.of(), List.of(), day); }

    // -- reading -----------------------------------------------------------------------------------

    public Townsfolk get(String id) { return folk.get(id); }
    public boolean has(String id) { return folk.containsKey(id); }
    public String nameOf(String id) {
        if (id == null || id.isEmpty()) return "";
        var t = folk.get(id); return t == null ? "someone" : t.name();
    }
    /** Residents who are alive (including any who were turned into zombie villagers), by name. */
    public List<Townsfolk> living() {
        return folk.values().stream().filter(Townsfolk::living).sorted(Comparator.comparing(Townsfolk::name).thenComparing(Townsfolk::id)).toList();
    }
    public List<Townsfolk> everyone() {
        return folk.values().stream().sorted(Comparator.comparing(Townsfolk::living).reversed().thenComparing(Townsfolk::name).thenComparing(Townsfolk::id)).toList();
    }
    public int affinity(String a, String b, long today) { return affinity(folk, ties, a, b, today); }
    public Tie tie(String a, String b) { return ties.getOrDefault(Chemistry.pair(a, b), Tie.NONE); }
    public long known(String a, String b, long today) { return known(folk.get(a), folk.get(b), today); }

    /** Family by blood within three steps (parents, siblings, grandparents, aunts and uncles, cousins). */
    public boolean blood(String a, String b) { return blood(folk, a, b); }

    /** What {@code b} is to {@code a}: "parent", "grandchild", "cousin"... or "" when unrelated. */
    public String relation(String a, String b) {
        var x = folk.get(a); if (x == null || a.equals(b)) return "";
        String direct = x.kinOf(b);
        if (!direct.isEmpty()) return direct;
        for (var hop : x.kin().entrySet()) {
            var mid = folk.get(hop.getKey()); if (mid == null || hop.getValue().equals("spouse")) continue;
            String second = mid.kinOf(b);
            if (second.isEmpty() || second.equals("spouse")) continue;
            switch (hop.getValue() + ">" + second) {
                case "parent>parent": return "grandparent";
                case "child>child": return "grandchild";
                case "parent>sibling": return "aunt_uncle";
                case "sibling>child": return "niece_nephew";
                case "parent>child", "sibling>sibling": return "sibling";
                default: break;
            }
        }
        for (var hop : x.kin().entrySet()) if (hop.getValue().equals("parent")) {
            var parent = folk.get(hop.getKey()); if (parent == null) continue;
            for (var aunt : parent.kin().entrySet()) if (aunt.getValue().equals("sibling")) {
                var t = folk.get(aunt.getKey()); if (t != null && t.kinOf(b).equals("child")) return "cousin";
            }
        }
        return blood(a, b) ? "relative" : "";
    }

    /** "", "smitten" (a secret crush), "sweethearts" or "married". */
    public String romance(String a, String b, long today) {
        var x = folk.get(a); var y = folk.get(b);
        if (x == null || y == null) return "";
        if (x.partner().equals(b)) return x.married() ? "married" : "sweethearts";
        if (!eligible(folk, x, y)) return "";
        long known = known(x, y, today);
        return known * 10 >= Chemistry.loveDays(a, b) * 6L && affinity(a, b, today) >= CRUSH_AFFINITY ? "smitten" : "";
    }
    /** The single resident {@code a} is quietly falling for, if any. */
    public String crush(String a, long today) {
        var x = folk.get(a); if (x == null || !x.single() || !x.adult()) return "";
        String best = ""; double progress = 0;
        for (var y : folk.values()) {
            if (!romance(a, y.id(), today).equals("smitten")) continue;
            double p = (double) known(x, y, today) / Chemistry.loveDays(a, y.id());
            if (p > progress) { progress = p; best = y.id(); }
        }
        return best;
    }
    /** The living resident {@code a} likes most outside their family, once they are at least friendly, or "". */
    public String bestFriend(String a, long today) {
        String best = extreme(a, today, true);
        return !best.isEmpty() && affinity(a, best, today) >= 25 ? best : "";
    }
    /** The living resident {@code a} gets along with worst, if they are actually at odds, or "". */
    public String rival(String a, long today) {
        String worst = extreme(a, today, false);
        return !worst.isEmpty() && affinity(a, worst, today) < -10 ? worst : "";
    }
    private String extreme(String a, long today, boolean best) {
        String pick = ""; int score = best ? Integer.MIN_VALUE : Integer.MAX_VALUE;
        for (var y : living()) {
            if (y.id().equals(a) || !relation(a, y.id()).isEmpty() || y.id().equals(folk.get(a) == null ? "" : folk.get(a).partner())) continue;
            int value = affinity(a, y.id(), today);
            if (best ? value > score : value < score) { score = value; pick = y.id(); }
        }
        return pick;
    }
    /** The living people {@code a} is related to, closest first. */
    public List<String> family(String a) {
        var x = folk.get(a); if (x == null) return List.of();
        var order = List.of("spouse", "parent", "child", "sibling", "grandparent", "grandchild", "aunt_uncle", "niece_nephew", "cousin", "relative");
        return folk.values().stream().filter(y -> !y.id().equals(a) && y.living()).map(y -> Map.entry(y.id(), relation(a, y.id())))
                .filter(e -> !e.getValue().isEmpty()).sorted(Comparator.comparingInt((Map.Entry<String, String> e) -> order.indexOf(e.getValue())).thenComparing(e -> nameOf(e.getKey())))
                .map(Map.Entry::getKey).toList();
    }
    /** Residents at home whose birthday is {@code today}, by name. */
    public List<Townsfolk> celebrants(long today) {
        return living().stream().filter(t -> t.home() && Calendar.isBirthday(t.birthday(), today)).toList();
    }
    /** The next birthdays of residents at home, soonest first (today's included). */
    public List<Townsfolk> birthdays(long today, int limit) {
        return living().stream().filter(Townsfolk::home)
                .sorted(Comparator.comparingInt((Townsfolk t) -> Calendar.daysUntil(t.birthday(), today)).thenComparing(Townsfolk::name))
                .limit(limit).toList();
    }
    /** News from the last {@code window} days, newest first. */
    public List<News> recent(long today, long window) {
        var list = new ArrayList<News>();
        for (int i = news.size() - 1; i >= 0; i--) if (today - news.get(i).day() <= window) list.add(news.get(i));
        return list;
    }

    // -- changes -----------------------------------------------------------------------------------

    /** Adds a newcomer. Returns this society unchanged if they are already known. */
    public Society register(Townsfolk t) {
        if (folk.containsKey(t.id())) return this;
        var nextFolk = new HashMap<>(folk); nextFolk.put(t.id(), t);
        var nextNews = new ArrayList<>(news);
        // A village found for the first time doesn't announce everyone; latecomers are news.
        boolean settled = folk.values().stream().anyMatch(o -> o.joined() < t.joined() - 1);
        if (settled && t.adult()) nextNews.add(new News(t.joined(), "arrived", t.id(), "", ""));
        return new Society(village, nextFolk, ties, nextNews, day);
    }
    public Society seen(String id, String name, String job, boolean adult, long today) {
        var t = folk.get(id); if (t == null) return this;
        var next = t.seen(name, job, adult, today);
        if (next.equals(t)) return this;
        var nextNews = news;
        if (adult && !t.adult()) { nextNews = new ArrayList<>(news); nextNews.add(new News(today, "grew_up", id, "", "")); }
        return with(next, nextNews);
    }
    /** Two residents spent part of a day near each other. */
    public Society together(String a, String b, long today) {
        if (a.equals(b) || !folk.containsKey(a) || !folk.containsKey(b)) return this;
        String key = Chemistry.pair(a, b); var tie = ties.getOrDefault(key, Tie.NONE); var next = tie.together(today);
        if (next == tie) return this;
        var nextTies = new HashMap<>(ties); nextTies.put(key, next);
        return new Society(village, folk, nextTies, news, day);
    }
    /**
     * A letter carried from {@code from} to {@code to}: it counts as a day spent together, and an apology
     * forgives their last quarrel.
     */
    public Society letter(String from, String to, long today, boolean apology) {
        if (from.equals(to) || !folk.containsKey(from) || !folk.containsKey(to)) return this;
        String key = Chemistry.pair(from, to); var tie = ties.getOrDefault(key, Tie.NONE); var next = tie.together(today);
        if (apology) next = next.reconciled();
        if (next.equals(tie)) return this;
        var nextTies = new HashMap<>(ties); nextTies.put(key, next);
        return new Society(village, folk, nextTies, news, day);
    }
    /** A player ({@code helper}, by name) answered a resident's notice on the village board. */
    public Society helped(String poster, String helper, long today) {
        if (!folk.containsKey(poster)) return this;
        var nextNews = new ArrayList<>(news); nextNews.add(new News(today, "helped", poster, "", helper));
        return new Society(village, folk, ties, nextNews, day);
    }
    /** Something a player did that the whole village talks about ({@code "deed:<kind>"} news). */
    public Society report(News n) {
        var nextNews = new ArrayList<>(news); nextNews.add(n);
        return new Society(village, folk, ties, nextNews, day);
    }
    public Society passed(String id, long today) {
        var t = folk.get(id); if (t == null || !t.living()) return this;
        var work = new Work(this);
        work.folk.put(id, t.status(Townsfolk.PASSED).partner("", -1, false));
        var partner = work.folk.get(t.partner());
        if (partner != null && partner.partner().equals(id)) work.folk.put(partner.id(), partner.partner("", -1, false));
        work.news.add(new News(today, "passed", id, "", ""));
        return work.freeze(day);
    }
    public Society cursed(String id, long today) {
        var t = folk.get(id); if (t == null || !t.home()) return this;
        var nextNews = new ArrayList<>(news); nextNews.add(new News(today, "cursed", id, "", ""));
        return with(t.status(Townsfolk.CURSED), nextNews);
    }
    public Society cured(String id, long today) {
        var t = folk.get(id); if (t == null || !t.status().equals(Townsfolk.CURSED)) return this;
        var nextNews = new ArrayList<>(news); nextNews.add(new News(today, "cured", id, "", ""));
        return with(t.status(Townsfolk.HOME), nextNews);
    }
    /** A baby born to two residents joins their family. */
    public Society born(String baby, String parentA, String parentB, long today) {
        var t = folk.get(baby); if (t == null || !t.kin().isEmpty()) return this;
        var work = new Work(this);
        var parents = new ArrayList<String>();
        for (String p : new String[]{parentA, parentB}) if (p != null && !p.isEmpty() && !p.equals(baby) && work.folk.containsKey(p) && !parents.contains(p)) parents.add(p);
        if (parents.isEmpty()) return this;
        for (String p : parents) {
            for (var sibling : List.copyOf(work.folk.get(p).kin().entrySet())) if (sibling.getValue().equals("child")) work.link(baby, sibling.getKey(), "sibling");
            work.link(baby, p, "parent");
        }
        var first = work.folk.get(parents.getFirst());
        // Their birthday is the day they were born.
        work.folk.put(baby, work.folk.get(baby).household(first.household().isEmpty() ? first.id() : first.household()).born(today));
        work.news.add(new News(today, "born", baby, parents.getFirst(), parents.size() > 1 ? parents.get(1) : ""));
        return work.freeze(day);
    }
    /**
     * A newly settled resident who {@link Chemistry#bringsFamily brings family} joins the household of
     * the nearest other newcomer who does too: as a couple, siblings, or parent and child.
     */
    public Society household(String id, List<String> nearby, long today) {
        var x = folk.get(id);
        if (x == null || !x.kin().isEmpty() || !Chemistry.bringsFamily(id)) return this;
        for (String other : nearby) {
            var y = folk.get(other);
            if (y == null || other.equals(id) || !y.home() || !Chemistry.bringsFamily(other)) continue;
            var work = new Work(this);
            if (!work.join(x, y, today)) continue;
            String house = y.household().isEmpty() ? y.id() : y.household();
            for (String member : List.of(id, other)) work.folk.put(member, work.folk.get(member).household(house));
            work.news.add(new News(today, "family", id, other, ""));
            return work.freeze(day);
        }
        return this;
    }
    /** Lives every day up to {@code today}: friendships grow, quarrels flare, and love may bloom. */
    public Society advance(long today) {
        if (today <= day) return this;
        var work = new Work(this);
        for (long d = Math.max(day + 1, today - CATCH_UP + 1); d <= today; d++) work.live(d);
        return work.freeze(today);
    }

    private Society with(Townsfolk t, List<News> nextNews) {
        var nextFolk = new HashMap<>(folk); nextFolk.put(t.id(), t);
        return new Society(village, nextFolk, ties, nextNews, day);
    }

    // -- the model ---------------------------------------------------------------------------------

    static long known(Townsfolk x, Townsfolk y, long today) {
        return x == null || y == null ? 0 : Math.max(0, today - Math.max(x.joined(), y.joined()));
    }
    static int affinity(Map<String, Townsfolk> folk, Map<String, Tie> ties, String a, String b, long today) {
        if (a.equals(b)) return 100;
        var x = folk.get(a); var y = folk.get(b);
        if (x == null || y == null) return 0;
        double chemistry = Chemistry.chemistry(x, y);
        String kin = x.kinOf(b);
        boolean partners = x.partner().equals(b);
        double target;
        if (kin.equals("spouse") || partners && x.married()) target = 92;
        else if (partners) target = 86;
        else if (kin.equals("parent") || kin.equals("child")) target = 78 + chemistry * 12;
        else if (kin.equals("sibling")) target = 66 + chemistry * 22; // siblings bicker
        else if (blood(folk, a, b)) target = 50 + chemistry * 20;
        else target = Math.clamp(14 + chemistry * 62, -45, 80);
        double start = kin.isEmpty() && !partners ? 3 : target;
        double growth = 1 - Math.exp(-known(x, y, today) / 40.0);
        var tie = ties.getOrDefault(Chemistry.pair(a, b), Tie.NONE);
        double penalty = tie.quarrel() >= 0 && today >= tie.quarrel() ? Math.max(0, 30 - (today - tie.quarrel())) : 0;
        return (int) Math.clamp(Math.round(start + (target - start) * growth + tie.together() * .5 - penalty), -100, 100);
    }
    static boolean blood(Map<String, Townsfolk> folk, String a, String b) {
        if (a.equals(b)) return true;
        var seen = new HashSet<String>(); seen.add(a);
        var frontier = List.of(a);
        for (int depth = 0; depth < 3 && !frontier.isEmpty(); depth++) {
            var next = new ArrayList<String>();
            for (String id : frontier) {
                var t = folk.get(id); if (t == null) continue;
                for (var e : t.kin().entrySet()) {
                    if (e.getValue().equals("spouse") || !seen.add(e.getKey())) continue;
                    if (e.getKey().equals(b)) return true;
                    next.add(e.getKey());
                }
            }
            frontier = next;
        }
        return false;
    }
    static boolean eligible(Map<String, Townsfolk> folk, Townsfolk x, Townsfolk y) {
        return !x.id().equals(y.id()) && x.adult() && y.adult() && x.home() && y.home() && x.single() && y.single()
                && Chemistry.compatible(x, y) && !blood(folk, x.id(), y.id());
    }

    /** A mutable working copy for multi-step changes. */
    private static final class Work {
        final String village;
        final Map<String, Townsfolk> folk;
        final Map<String, Tie> ties;
        final List<News> news;
        Work(Society s) { village = s.village; folk = new HashMap<>(s.folk); ties = new HashMap<>(s.ties); news = new ArrayList<>(s.news); }
        Society freeze(long day) { return new Society(village, folk, ties, news, day); }

        /** Records that {@code other} is {@code relation} to {@code id}, and the inverse. */
        void link(String id, String other, String relation) {
            if (id.equals(other)) return;
            String inverse = switch (relation) { case "parent" -> "child"; case "child" -> "parent"; default -> relation; };
            folk.put(id, folk.get(id).kin(other, relation));
            folk.put(other, folk.get(other).kin(id, inverse));
        }
        void children(String parent, String child) {
            for (var e : List.copyOf(folk.get(parent).kin().entrySet())) if (e.getValue().equals("child")) link(child, e.getKey(), "sibling");
            link(child, parent, "parent");
            var spouse = folk.get(parent).partner();
            if (!spouse.isEmpty() && folk.get(parent).married() && folk.containsKey(spouse) && !folk.get(child).kin().containsKey(spouse)) link(child, spouse, "parent");
        }
        boolean join(Townsfolk x, Townsfolk y, long day) {
            if (!x.adult() && y.adult()) { children(y.id(), x.id()); return true; }
            if (x.adult() && !y.adult()) {
                var parents = y.kin().entrySet().stream().filter(e -> e.getValue().equals("parent")).map(Map.Entry::getKey).toList();
                if (parents.size() >= 2) return false;
                if (parents.size() == 1) {
                    var other = folk.get(parents.getFirst());
                    if (other == null || !other.single() || !other.adult() || !Chemistry.compatible(x, other)) return false;
                    marry(x.id(), other.id(), day);
                    return true; // marrying a single parent makes x a parent of their children
                }
                children(x.id(), y.id());
                for (var e : List.copyOf(folk.get(y.id()).kin().entrySet())) if (e.getValue().equals("sibling")) children(x.id(), e.getKey());
                return true;
            }
            if (x.adult() && y.single() && Chemistry.compatible(x, y) && Chemistry.arriveAsCouple(x.id(), y.id())) { marry(x.id(), y.id(), day); return true; }
            // Otherwise they are siblings, sharing parents and brothers and sisters.
            for (var e : List.copyOf(folk.get(y.id()).kin().entrySet())) {
                if (e.getValue().equals("sibling")) link(x.id(), e.getKey(), "sibling");
                if (e.getValue().equals("parent")) link(x.id(), e.getKey(), "parent");
            }
            link(x.id(), y.id(), "sibling");
            return true;
        }
        void marry(String a, String b, long day) {
            folk.put(a, folk.get(a).partner(b, day, true));
            folk.put(b, folk.get(b).partner(a, day, true));
            link(a, b, "spouse");
            for (String spouse : List.of(a, b)) {
                String other = spouse.equals(a) ? b : a;
                for (var e : List.copyOf(folk.get(spouse).kin().entrySet()))
                    if (e.getValue().equals("child") && !folk.get(e.getKey()).kin().containsKey(other) && folk.get(e.getKey()).kin().values().stream().filter("parent"::equals).count() < 2)
                        link(e.getKey(), other, "parent");
            }
        }

        void live(long d) {
            var people = folk.values().stream().filter(Townsfolk::home)
                    .sorted(Comparator.comparingLong(Townsfolk::joined).thenComparing(Townsfolk::id)).limit(WEB).toList();
            // Birthdays: everyone at home who was already here before today.
            for (var x : people) if (x.joined() < d && Calendar.isBirthday(x.birthday(), d)) news.add(new News(d, "birthday", x.id(), "", ""));
            int milestones = 0; boolean quarreled = false;
            String loveA = null, loveB = null; long loveScore = Long.MIN_VALUE;
            for (int i = 0; i < people.size(); i++) for (int j = i + 1; j < people.size(); j++) {
                var x = people.get(i); var y = people.get(j);
                String a = x.id(), b = y.id();
                boolean family = !x.kinOf(b).isEmpty() || x.partner().equals(b) || blood(folk, a, b);
                int now = affinity(folk, ties, a, b, d);
                if (!family && milestones < 2) {
                    int before = affinity(folk, ties, a, b, d - 1);
                    if (before < 85 && now >= 85) { news.add(new News(d, "best_friends", a, b, "")); milestones++; }
                    else if (before < 65 && now >= 65) { news.add(new News(d, "friends", a, b, "")); milestones++; }
                }
                if (!quarreled && !x.partner().equals(b)) {
                    var tie = ties.getOrDefault(Chemistry.pair(a, b), Tie.NONE);
                    // Rare: a village of twenty sees a squabble every couple of weeks, mostly between people who don't click.
                    double odds = now < 15 && Chemistry.chemistry(x, y) < -.2 ? .0015 : now < 40 ? .0001 : 0;
                    if (odds > 0 && (tie.quarrel() < 0 || d - tie.quarrel() > 20) && Chemistry.unit(Chemistry.pairSeed(a, b, d * 31 + 0x9a77eL)) < odds) {
                        ties.put(Chemistry.pair(a, b), tie.quarrel(d));
                        news.add(new News(d, "quarrel", a, b, "")); quarreled = true;
                    }
                }
                if (eligible(folk, x, y) && now >= LOVE_AFFINITY) {
                    long ready = known(x, y, d) - Chemistry.loveDays(a, b);
                    if (ready >= 0 && ready > loveScore) { loveScore = ready; loveA = a; loveB = b; }
                }
            }
            if (loveA != null) {
                folk.put(loveA, folk.get(loveA).partner(loveB, d, false));
                folk.put(loveB, folk.get(loveB).partner(loveA, d, false));
                news.add(new News(d, "sweethearts", loveA, loveB, ""));
            }
            for (var x : people) {
                var t = folk.get(x.id()); var y = folk.get(t.partner());
                if (y == null || t.married() || t.id().compareTo(y.id()) > 0 || !y.home()) continue;
                if (d - t.partnerSince() >= Chemistry.marryDays(t.id(), y.id()) && affinity(folk, ties, t.id(), y.id(), d) >= MARRY_AFFINITY) {
                    marry(t.id(), y.id(), d);
                    news.add(new News(d, "married", t.id(), y.id(), ""));
                    break;
                }
            }
        }
    }
}
