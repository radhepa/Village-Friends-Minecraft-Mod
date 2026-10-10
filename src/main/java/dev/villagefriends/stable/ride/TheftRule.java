package dev.villagefriends.stable.ride;

/**
 * What a village's stable horse being away from its stall means, pure: stolen, lost, brought back, home again,
 * or simply wandered and due to drift back. Only horses kept by a resident or the village are judged (a horse a
 * player stabled is theirs to ride anywhere).
 *
 * <p>A player who rides or leads the horse more than {@link #NEAR} blocks from its stall <b>took</b> it
 * ({@link #takes}): they answer for it until it is home again, and that is saved with the horse. Nothing else makes a
 * player its taker: tempting it out with a golden carrot doesn't, but then it was never theirs to lose either.
 *
 * <ul>
 * <li>{@link Verdict#STOLEN}: ridden or led by a player more than {@link #FAR} blocks from its stall, unless it is
 * already stolen, or it is lost and this player is not the one who took it. There is no "I found it out there"
 * for the taker: hopping off at 47 blocks, coaxing it a little further and coming back for it later is still
 * theft. A horse that no player took (a knight left it, or it was tempted out) drifts home when unseen instead.</li>
 * <li>{@link Verdict#LOST}: a horse a player took, more than {@link #FAR} blocks out with nobody riding or leading
 * it for over {@link #ALONE} ticks. Anyone but its taker or thief may then bring it home.</li>
 * <li>{@link Verdict#RETURNED}: a stolen or lost horse brought within {@link #NEAR} blocks of its stall by a
 * player who neither stole nor took it, at most once a game day per horse ({@link #COOLDOWN}). The thief or the
 * taker bringing it back, or a second return the same day, is {@link Verdict#HOME}: the flags clear and nobody
 * earns anything, so taking a horse out and back (alone or with a friend's help, once a day) is no way to farm
 * standing.</li>
 * <li>{@link Verdict#HOME}: a flagged or taken horse back within {@link #NEAR} blocks; everything clears.</li>
 * <li>{@link Verdict#DRIFT}: an unflagged, loose horse more than {@link #NEAR} blocks out with no player within
 * {@link #QUIET} blocks; it is moved back beside its stall, unseen. From any distance when no player took it (a
 * knight's horse left after the watch, one that wandered, was tempted out or bolted), within {@link #FAR} when a
 * player did (beyond that it waits to be lost and found). Never from another dimension (infinitely far).</li>
 * </ul>
 */
public final class TheftRule {
    public enum Verdict { NONE, STOLEN, LOST, RETURNED, HOME, DRIFT }

    /** Farther than this from its stall a horse is away (stolen or lost). */
    public static final double FAR = 48;
    /** Within this of its stall a horse is home; riding or leading it further out is taking it. */
    public static final double NEAR = 8;
    /** A wandering horse only drifts home when no player is this close (nobody sees it move). */
    public static final double QUIET = 32;
    /** How long a horse a player took and left far from home must be left alone before it counts as lost. */
    public static final long ALONE = 1200;
    /** One Returned a Horse deed per horse per game day. */
    public static final long COOLDOWN = 24000;

    /**
     * How the horse is found. {@code distance}: blocks from its stall (infinite in another dimension).
     * {@code withPlayer}: ridden by or leashed to a player; {@code byTaker}: that player stole it or is the one who
     * took it. {@code loose}: no rider (player or resident), no lead, and not itself riding in something (a boat).
     * {@code alone}: ticks since anyone last rode or led it. {@code nearestPlayer}: blocks to the nearest player
     * (infinite with none).
     */
    public record Seen(double distance, boolean withPlayer, boolean byTaker, boolean loose, long alone, double nearestPlayer) {
        /** Ridden or led by a player (who is right there). */
        public static Seen withPlayer(double distance, boolean byTaker) { return new Seen(distance, true, byTaker, false, 0, 0); }
        /** Without a player: maybe ridden by a resident or leashed to a post ({@code loose} false), maybe free. */
        public static Seen withoutPlayer(double distance, boolean loose, long alone, double nearestPlayer) {
            return new Seen(distance, false, false, loose, alone, nearestPlayer);
        }
    }

    /**
     * True when a player riding or leading a horse {@code distance} blocks from its stall becomes its taker: it is
     * out of its stable's reach and not already stolen or lost (who took it then stays as it was).
     */
    public static boolean takes(double distance, boolean flagged) { return !flagged && distance > NEAR; }

    /**
     * The verdict for a horse found as {@code seen}, given its flags: {@code stolen} (someone's uuid is in
     * {@code stolenBy}), {@code awaySince} (0 = not lost), {@code taken} (a player took it since it was last home)
     * and {@code returnedAt} (0 = never returned).
     */
    public static Verdict assess(Seen seen, boolean stolen, long awaySince, boolean taken, long returnedAt, long now) {
        boolean flagged = stolen || awaySince > 0;
        if (seen.withPlayer()) {
            if (flagged && seen.distance() <= NEAR) return seen.byTaker() || !cooled(returnedAt, now) ? Verdict.HOME : Verdict.RETURNED;
            if (!stolen && seen.distance() > FAR && (awaySince == 0 || seen.byTaker())) return Verdict.STOLEN;
            return Verdict.NONE;
        }
        if ((flagged || taken) && seen.distance() <= NEAR) return Verdict.HOME;
        if (awaySince == 0 && taken && seen.distance() > FAR && seen.alone() > ALONE) return Verdict.LOST;
        if (!flagged && seen.loose() && seen.distance() > NEAR && seen.distance() <= (taken ? FAR : Double.MAX_VALUE) && seen.nearestPlayer() > QUIET) return Verdict.DRIFT;
        return Verdict.NONE;
    }

    /** True when a return now may earn the deed: never returned before, or a full day since the last one. */
    public static boolean cooled(long returnedAt, long now) { return returnedAt == 0 || now - returnedAt >= COOLDOWN; }

    private TheftRule() {}
}
