package dev.villagefriends.deed;

import dev.villagefriends.quest.Board;
import java.util.List;

/**
 * A player's standing in a village: notices answered plus what they did there. Pure.
 *
 * <p>{@code score10 = 10·favors + banked + Σ good points + Σ bad points · ½^(age / half-life) · (½ if apologized)},
 * in tenths of a notice. The five titles keep the board's thresholds ({@link Board#STANDING}); below them is a
 * sixth, {@link #UNWELCOME}, at {@code score10 <= -20}, which only deeds can reach and which fades as bad
 * deeds do. Prices follow the same deeds through {@link #reputation}.
 */
public final class Standing {
    /** The tier below Newcomer. */
    public static final int UNWELCOME = -1;
    /** At or below this score (tenths) a player is Unwelcome. */
    public static final int UNWELCOME_AT = -20;
    /** What deeds can add to or take from one resident's vanilla reputation, so a village never turns golems hostile by itself. */
    public static final int REP_MIN = -60, REP_MAX = 40;

    /** How much of a deed still counts {@code today}: good deeds keep their worth, bad ones halve every half-life. */
    public static double decay(Deed d, long today) {
        int half = d.kind().halfLifeDays;
        if (d.good() || half <= 0) return 1;
        return Math.pow(.5, Math.max(0, today - d.day()) / (double) half);
    }
    /** An apology halves what is left of a bad deed. */
    public static double apology(Deed d) { return !d.good() && d.apologized() ? .5 : 1; }

    public static int score10(int favors, DeedLog log, long today) {
        double score = 10.0 * favors;
        if (log != null) {
            score += log.banked10();
            for (var d : log.deeds()) score += d.points10() * decay(d, today) * apology(d);
        }
        return (int) Math.round(score);
    }
    /** -1 Unwelcome, then 0 to 4: Newcomer, Helping Hand, Good Neighbor, Pillar of the Community, Hero of the village. */
    public static int tier(int score10) {
        return score10 <= UNWELCOME_AT ? UNWELCOME : Board.standing(Math.floorDiv(score10, 10));
    }
    public static String title(int tier, String villageName) { return tier == UNWELCOME ? "Unwelcome" : Board.title(tier, villageName); }

    /**
     * What a change of standing means: rewards only on reaching a higher tier than ever before
     * ({@code peak}), a sorry message on falling, nothing otherwise.
     */
    public record Change(int before, int after, boolean reward, boolean fell) {}
    public static Change change(int before, int after, int peak) {
        return new Change(before, after, after > before && after > peak && after > 0, after < before);
    }

    /** "3 more notices to become a Good Neighbor", the board's hint line. */
    public static String hint(int score10, String villageName) {
        int tier = tier(score10);
        if (tier == UNWELCOME) return "Nobody here will give you work until they trust you again. Bad deeds fade; apologies and good deeds help.";
        if (tier + 1 >= Board.STANDING.length) return "Everyone here knows your name. Trades are cheaper all over the village.";
        int needed = Math.max(1, (int) Math.ceil((Board.STANDING[tier + 1] * 10 - score10) / 10.0));
        return needed + " more " + (needed == 1 ? "notice" : "notices") + " to become " + Board.title(tier + 1, villageName);
    }

    /**
     * The deeds {@code resident} knows about, as a change to their vanilla reputation for this player:
     * {@code Σ rep · how they know it (1, .8, .6, .3) · decay · (½ if apologized)}, clamped to
     * {@link #REP_MIN}..{@link #REP_MAX}.
     */
    public static int reputation(List<Deed> deeds, String resident, long today) {
        double sum = 0;
        for (var d : deeds) {
            var know = d.know(resident);
            if (know == null || d.kind().rep == 0) continue;
            sum += d.kind().rep * know.weight() * decay(d, today) * apology(d);
        }
        return (int) Math.clamp(Math.round(sum), REP_MIN, REP_MAX);
    }

    private Standing() {}
}
