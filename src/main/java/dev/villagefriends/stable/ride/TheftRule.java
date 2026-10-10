package dev.villagefriends.stable.ride;

/**
 * What a village's stable horse being away from its stall means, pure: stolen, lost, brought back, home again,
 * or simply wandered and due to drift back. Only horses kept by a resident or the village are judged (a horse a
 * player stabled is theirs to ride anywhere).
 *
 * <ul>
 * <li>{@link Verdict#STOLEN}: ridden or led by a player more than {@link #FAR} blocks from its stall, and not
 * flagged yet. A horse a player first picks up when it is already that far away was lost, not taken from its
 * stable: it counts as {@link Verdict#LOST} instead, so whoever finds it can bring it home.</li>
 * <li>{@link Verdict#LOST}: more than {@link #FAR} blocks out with nobody riding or leading it for over
 * {@link #ALONE} ticks.</li>
 * <li>{@link Verdict#RETURNED}: a stolen or lost horse brought within {@link #NEAR} blocks of its stall by a
 * player who is not the thief, at most once a game day per horse ({@link #COOLDOWN}), so leading the same horse
 * out and back is no way to farm standing. The thief bringing it back, or a second return the same day, is
 * {@link Verdict#HOME}: the flags clear and nobody earns anything.</li>
 * <li>{@link Verdict#HOME}: a flagged horse back within {@link #NEAR} blocks; the flags clear.</li>
 * <li>{@link Verdict#DRIFT}: an unflagged, loose horse {@link #NEAR} to {@link #FAR} blocks out with no player within
 * {@link #QUIET} blocks; it is moved back beside its stall, unseen (a knight's horse left after the watch, or one
 * that wandered or bolted).</li>
 * </ul>
 */
public final class TheftRule {
    public enum Verdict { NONE, STOLEN, LOST, RETURNED, HOME, DRIFT }

    /** Farther than this from its stall a horse is away (stolen or lost). */
    public static final double FAR = 48;
    /** Within this of its stall a horse is home. */
    public static final double NEAR = 8;
    /** A wandering horse only drifts home when no player is this close (nobody sees it move). */
    public static final double QUIET = 32;
    /** How long a horse far from home must be left alone before it counts as lost. */
    public static final long ALONE = 1200;
    /** One Returned a Horse deed per horse per game day. */
    public static final long COOLDOWN = 24000;

    /**
     * How the horse is found. {@code distance}: blocks from its stall (infinite in another dimension).
     * {@code withPlayer}: ridden by or leashed to a player; {@code pickedUp}: that player had not been riding or
     * leading it at the previous check; {@code byThief}: that player is the one who stole it. {@code loose}: no
     * rider (player or resident), no lead, and not itself riding in something (a boat). {@code alone}: ticks since
     * anyone last rode or led it.
     * {@code nearestPlayer}: blocks to the nearest player (infinite with none).
     */
    public record Seen(double distance, boolean withPlayer, boolean pickedUp, boolean byThief, boolean loose, long alone, double nearestPlayer) {
        /** Ridden or led by a player (who is right there). */
        public static Seen withPlayer(double distance, boolean pickedUp, boolean byThief) {
            return new Seen(distance, true, pickedUp, byThief, false, 0, 0);
        }
        /** Without a player: maybe ridden by a resident or leashed to a post ({@code loose} false), maybe free. */
        public static Seen withoutPlayer(double distance, boolean loose, long alone, double nearestPlayer) {
            return new Seen(distance, false, false, false, loose, alone, nearestPlayer);
        }
    }

    /**
     * The verdict for a horse found as {@code seen}, given its flags: {@code stolen} (someone's uuid is in
     * {@code stolenBy}), {@code awaySince} (0 = not lost) and {@code returnedAt} (0 = never returned).
     */
    public static Verdict assess(Seen seen, boolean stolen, long awaySince, long returnedAt, long now) {
        boolean flagged = stolen || awaySince > 0;
        if (seen.withPlayer()) {
            if (flagged && seen.distance() <= NEAR) return seen.byThief() || !cooled(returnedAt, now) ? Verdict.HOME : Verdict.RETURNED;
            if (!flagged && seen.distance() > FAR) return seen.pickedUp() ? Verdict.LOST : Verdict.STOLEN;
            return Verdict.NONE;
        }
        if (flagged && seen.distance() <= NEAR) return Verdict.HOME;
        if (awaySince == 0 && seen.distance() > FAR && seen.alone() > ALONE) return Verdict.LOST;
        if (!flagged && seen.loose() && seen.distance() > NEAR && seen.distance() <= FAR && seen.nearestPlayer() > QUIET) return Verdict.DRIFT;
        return Verdict.NONE;
    }

    /** True when a return now may earn the deed: never returned before, or a full day since the last one. */
    public static boolean cooled(long returnedAt, long now) { return returnedAt == 0 || now - returnedAt >= COOLDOWN; }

    private TheftRule() {}
}
