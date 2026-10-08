package dev.villagefriends.deed;

import dev.villagefriends.social.Society;
import dev.villagefriends.social.Townsfolk;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.Map;
import java.util.Set;

/**
 * How word of a deed gets around a village. Pure and deterministic: every roll is seeded by the deed,
 * the two residents and the day, so checking the same pair twice in a day gives the same answer and a
 * village that was unloaded catches up exactly as if it had lived those days.
 *
 * <ul>
 * <li>Standing together: when one of two neighbors knows and the other doesn't, the other hears it with
 * chance {@link #TOGETHER} at each check of the village's daily life (every ten seconds), three times as
 * likely over lunch, at the tavern, the market or a party, twice as likely between partners, family and
 * good friends. Once heard it is known, so a pair passes each deed on at most once.</li>
 * <li>Each day: everyone who knows tells their family and the neighbors they spend time with
 * ({@link #DAILY}, {@link #DAILY_FAMILY} for family). The dead and the cursed tell nobody.</li>
 * <li>Big deeds are village news: the next day everyone has heard.</li>
 * </ul>
 */
public final class Rumors {
    public static final double TOGETHER = .15, DAILY = .25, DAILY_FAMILY = .5;
    /** Ties with at least this many shared days pass gossip on. */
    public static final int CLOSE_TIE = 3;
    /** Unloaded days caught up, like {@link Society#CATCH_UP}. */
    public static final int CATCH_UP = Society.CATCH_UP;
    /** Routines where neighbors sit together and talk. */
    public static final Set<String> SOCIAL = Set.of("lunch", "lunch_tavern", "tavern", "supper_tavern", "social", "market", "party");

    /** A roll in [0, 1) for one deed, two residents and a day. */
    public static double roll(int serial, String teller, String listener, long day, long salt) {
        long h = serial * 0x9E3779B97F4A7C15L ^ teller.hashCode() * 0xC2B2AE3D27D4EB4FL ^ (long) listener.hashCode() << 21 ^ day * 0x165667B19E3779F9L ^ salt;
        h = (h ^ h >>> 30) * 0xBF58476D1CE4E5B9L; h = (h ^ h >>> 27) * 0x94D049BB133111EBL; h ^= h >>> 31;
        return (h >>> 11) * 0x1.0p-53;
    }
    /** The chance two neighbors standing together pass a deed on today. */
    public static double chance(boolean social, boolean close) { return Math.min(1, TOGETHER * (social ? 3 : 1) * (close ? 2 : 1)); }
    /** Partners, family and friends (affinity 40 or more) talk more. */
    public static boolean close(Society s, String a, String b, long today) {
        var x = s.get(a);
        return x != null && (x.partner().equals(b) || !s.relation(a, b).isEmpty() || s.affinity(a, b, today) >= 40);
    }
    /** Living at home in the village: the dead and the cursed neither hear nor tell. */
    public static boolean present(Society s, String id) { var t = s.get(id); return t != null && t.home(); }

    /**
     * Two residents spent time near each other doing {@code routineA} and {@code routineB}: maybe one tells
     * the other. {@code check} numbers the daily-life pass (game time / 200) so each pass rolls afresh.
     */
    public static Deed together(Deed d, Society s, String a, String routineA, String b, String routineB, long today, long check) {
        if (!d.fresh(today) || !present(s, a) || !present(s, b)) return d;
        boolean ka = d.knows(a), kb = d.knows(b);
        if (ka == kb) return d;
        String teller = ka ? a : b, listener = ka ? b : a;
        double p = chance(SOCIAL.contains(routineA) && SOCIAL.contains(routineB), close(s, a, b, today));
        return roll(d.serial(), teller, listener, today, 0x7061697253L ^ check * 0x2545F4914F6CDD1DL) < p ? d.learn(listener, Know.of(Know.HEARD, today, teller)) : d;
    }

    /** Who lives at home in a village and who their family is, worked out once for a whole day's gossip. */
    public record Circles(Society society, java.util.List<String> people, Map<String, Set<String>> family) {
        public static Circles of(Society s) {
            var people = s.living().stream().filter(Townsfolk::home).map(Townsfolk::id).toList();
            var family = new java.util.HashMap<String, Set<String>>();
            for (var id : people) {
                var kin = new java.util.HashSet<>(s.family(id));
                if (!s.get(id).partner().isEmpty()) kin.add(s.get(id).partner());
                family.put(id, kin);
            }
            return new Circles(s, people, family);
        }
        boolean family(String a, String b) { return family.getOrDefault(a, Set.of()).contains(b); }
    }

    /** Lives a deed's rumor days up to {@code today}; does nothing if already done today. */
    public static Deed daily(Deed d, Society s, long today) { return today <= d.spread() ? d : daily(d, Circles.of(s), today); }
    public static Deed daily(Deed d, Circles c, long today) {
        if (today <= d.spread()) return d;
        var next = d;
        for (long day = Math.max(d.spread() + 1, today - CATCH_UP + 1); day <= today; day++) {
            if (!next.fresh(day)) break;
            next = spread(next, c, day);
        }
        return next.spreadTo(today);
    }
    private static Deed spread(Deed d, Circles c, long day) {
        if (d.kind().big() && day > d.day()) {
            for (var id : c.people()) if (!d.knows(id)) d = d.learn(id, Know.of(Know.HEARD, day, ""));
            return d;
        }
        var tellers = new ArrayList<Map.Entry<String, Know>>(d.knowers().entrySet());
        tellers.sort(Map.Entry.comparingByKey(Comparator.naturalOrder()));
        for (var teller : tellers) {
            String x = teller.getKey();
            if (teller.getValue().day() >= day || !c.family().containsKey(x)) continue;
            for (var y : c.people()) {
                if (y.equals(x) || d.knows(y)) continue;
                boolean family = c.family(x, y);
                if (!family && c.society().tie(x, y).together() < CLOSE_TIE) continue;
                if (roll(d.serial(), x, y, day, 0x6461696cL) < (family ? DAILY_FAMILY : DAILY)) d = d.learn(y, Know.of(Know.HEARD, day, x));
            }
        }
        return d;
    }

    private Rumors() {}
}
