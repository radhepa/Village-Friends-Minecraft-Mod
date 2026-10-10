package dev.villagefriends.deed;

import com.mojang.serialization.Codec;
import java.util.Locale;

/**
 * Everything a player can do that a village remembers. Each kind has its standing worth in tenths of a
 * notice ({@code points10}: answering one notice is 10), what each repeat adds within the merge window and
 * the most one merged deed can be worth, how fast a bad deed fades ({@code halfLifeDays}, 0 = never), how
 * far the news travels ({@link Size}), and its weight in trade prices ({@code rep}, added on top of vanilla's
 * villager gossip). {@code mergeTicks} folds repeats into one deed: hits within a minute, bandages and rescues
 * within a day; -1 merges for as long as the key matches (one raid).
 */
public enum DeedKind {
    RAID_DEFENDED(true, 10, 2, 30, 0, Size.NOTABLE, 10, -1),
    /** Vanilla's Hero of the Village (given for the same win) already prices it, so this adds nothing to prices. */
    RAID_WON(true, 30, 0, 30, 0, Size.BIG, 0, -1),
    REVIVED(true, 20, 0, 20, 0, Size.BIG, 15, 0),
    BANDAGED(true, 5, 0, 5, 0, Size.SMALL, 4, 24000),
    /** Once a day per resident saved: a night of zombies at the walls is one rescue for each neighbor, not one per kill. */
    SAVED_FROM_MONSTER(true, 10, 0, 15, 0, Size.NOTABLE, 8, 24000),
    RESCUED_COMPANION(true, 5, 0, 5, 0, Size.SMALL, 5, 24000),
    /** Counted in the board's favors; a deed only so residents can talk about it. */
    NOTICE_ANSWERED(true, 0, 0, 0, 0, Size.SMALL, 0, 0),
    BIRTHDAY_GIFT(true, 5, 0, 5, 0, Size.SMALL, 4, 24000),
    PET_KINDNESS(true, 1, 0, 1, 0, Size.SMALL, 1, 24000),
    /** Bringing a lost or stolen stable horse home; once a day per horse, so leading one out and back earns nothing. */
    RETURNED_HORSE(true, 10, 0, 10, 0, Size.NOTABLE, 6, 24000),
    /** Vanilla already prices hitting a villager (VILLAGER_HURT gossip), so this adds nothing to prices. */
    HIT_RESIDENT(false, -10, -3, -25, 7, Size.NOTABLE, 0, 1200),
    KNOCKED_OUT_RESIDENT(false, -30, 0, -30, 14, Size.BIG, -20, 0),
    KILLED_RESIDENT(false, -80, 0, -80, 28, Size.BIG, -40, 0),
    HIT_GOLEM(false, -5, 0, -5, 7, Size.SMALL, -5, 1200),
    KILLED_GOLEM(false, -40, 0, -40, 14, Size.BIG, -25, 0),
    HURT_PET(false, -15, 0, -15, 7, Size.NOTABLE, -10, 1200),
    KILLED_PET(false, -40, 0, -40, 14, Size.BIG, -25, 0),
    BROKE_HOME(false, -10, 0, -10, 7, Size.NOTABLE, -8, 24000),
    /** {@code count} is the number of items taken: -1 more per 8 items. */
    STOLE(false, -10, 0, -30, 10, Size.NOTABLE, -10, 24000),
    /** Riding or leading a resident's or the village's horse far from its stall. */
    STOLE_HORSE(false, -25, 0, -25, 14, Size.NOTABLE, -15, 0);

    /** How far word travels: small deeds are told person to person, big ones become village news. */
    public enum Size { SMALL, NOTABLE, BIG }

    public static final Codec<DeedKind> CODEC = Codec.STRING.xmap(DeedKind::byId, DeedKind::id);

    public final boolean good;
    public final int points10, extra10, max10, halfLifeDays, rep, mergeTicks;
    public final Size size;

    DeedKind(boolean good, int points10, int extra10, int max10, int halfLifeDays, Size size, int rep, int mergeTicks) {
        this.good = good; this.points10 = points10; this.extra10 = extra10; this.max10 = max10;
        this.halfLifeDays = halfLifeDays; this.size = size; this.rep = rep; this.mergeTicks = mergeTicks;
    }

    /** "raid_won", as saved and as dialogue pools name it. */
    public String id() { return name().toLowerCase(Locale.ROOT); }
    public static DeedKind byId(String id) {
        for (var k : values()) if (k.id().equals(id)) return k;
        return NOTICE_ANSWERED;
    }
    public boolean big() { return size == Size.BIG; }
    /** Violence (anger in a witness's bubble) as opposed to breaking or taking things (gloom). */
    public boolean violent() { return !good && this != BROKE_HOME && this != STOLE && this != STOLE_HORSE; }

    /**
     * What a deed done {@code count} times (or with {@code count} raiders, or items) is worth, in tenths.
     * {@code child}: a monster was chasing a child, which counts for more.
     */
    public int points10(int count, boolean child) {
        count = Math.max(1, count);
        return switch (this) {
            case SAVED_FROM_MONSTER -> child ? 15 : 10;
            case STOLE -> Math.max(max10, points10 - count / 8);
            default -> good ? Math.min(max10, points10 + extra10 * (count - 1)) : Math.max(max10, points10 + extra10 * (count - 1));
        };
    }
}
