package dev.villagefriends.stable.yard;

import dev.villagefriends.stable.data.StableTable;
import java.util.List;
import java.util.random.RandomGenerator;

/**
 * The stable's rules, kept free of the world so they can be tested on their own: who may stall which horse,
 * how a trough fills and feeds, when the stablehand tops a trough up or visits a horse, how a horse from a
 * stable template settles into a stall, and which breeds a village keeps.
 */
public final class StallRules {
    /** A trough holds four servings of hay. */
    public static final int MAX_HAY = 4;
    /** A template horse looks for a free stall this many times (one tick after loading, then every yard tick) before it gives up. */
    public static final int MAX_TRIES = 3;
    /** A stablehand visits each stalled horse at most once every two minutes. */
    public static final long VISIT_TICKS = 2400;
    /** How long a stablehand keeps at one chore before giving up on it (unreachable trough, wandering horse). */
    public static final long CHORE_TICKS = 600;

    public enum Settle { STALL, RETRY, GIVE_UP }

    /**
     * May a player stall this horse? Only their own: one they tamed ({@code owner}) or one already stabled in their
     * name ({@code keeperIsPlayer}). A resident's or the village's horse never, even when the player rides it, so a
     * stolen horse can't be passed off as theirs by giving it a new stall.
     */
    public static boolean canStall(boolean owner, boolean keeperIsPlayer, boolean residentOwned) { return !residentOwned && (owner || keeperIsPlayer); }
    /** May a new horse take a stall another horse lives in? Not a resident's or the village's; a player's horse moves out. */
    public static boolean mayEvict(boolean occupantResidentOwned) { return !occupantResidentOwned; }
    /** The trough's hay after adding {@code add} servings (wheat 1, a hay bale 4), never above {@link #MAX_HAY}. */
    public static int fill(int hay, int add) { return Math.max(0, Math.min(MAX_HAY, hay + add)); }
    /** A stalled horse eats from a trough when it is hurt or still a foal, and there is hay. */
    public static boolean eats(int hay, boolean hurt, boolean baby) { return hay > 0 && (hurt || baby); }
    /** Eating takes a serving one time in three ({@code roll} is 0, 1 or 2), so a full trough feeds a stall for a while. */
    public static boolean usesHay(int roll) { return roll == 0; }
    /** The stablehand tops up a trough that isn't full, once per trough per day. */
    public static boolean refill(int hay, long lastRefillDay, long today) { return hay < MAX_HAY && lastRefillDay != today; }
    /** Is a stalled horse due a visit from the stablehand? {@code last} is -1 when it has never had one. */
    public static boolean visitDue(long last, long now) { return last < 0 || now - last >= VISIT_TICKS; }

    /** What a horse from a stable template does next: take the stall it found, look again later, or stop looking. */
    public static Settle settle(boolean stallFound, int triesSoFar) {
        if (stallFound) return Settle.STALL;
        return triesSoFar + 1 < MAX_TRIES ? Settle.RETRY : Settle.GIVE_UP;
    }

    /** The village type a vanilla villager type belongs to (jungle and swamp villagers live in plains-style villages). */
    public static String villageType(String villagerType) {
        return switch (villagerType) {
            case "desert", "savanna", "taiga" -> villagerType;
            case "snow" -> "snowy";
            default -> "plains";
        };
    }

    /**
     * A breed for a horse in a village stable: one of the breeds that village type keeps ({@code village} in the
     * breed table), weighted by how often each is found in the wild. Rouncey, the common horse, when none fits.
     */
    public static String stableBreed(List<StableTable.Breed> breeds, String villageType, RandomGenerator random) {
        int total = 0;
        for (var b : breeds) if (b.village().contains(villageType)) total += weight(b);
        if (total <= 0) return "rouncey";
        int roll = random.nextInt(total);
        for (var b : breeds) {
            if (!b.village().contains(villageType)) continue;
            roll -= weight(b);
            if (roll < 0) return b.id();
        }
        return "rouncey";
    }
    private static int weight(StableTable.Breed b) {
        int w = 0;
        for (var s : b.spawns()) w += Math.max(0, s.weight());
        return Math.max(1, w);
    }

    private StallRules() {}
}
