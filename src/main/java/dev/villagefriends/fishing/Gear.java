package dev.villagefriends.fishing;

import java.util.Locale;

/**
 * What fishing gear does, in one place. Rods: the vanilla Fishing Rod (plain), the Reinforced Rod (takes bait
 * and tackle, a bigger catch zone) and the Angler's Rod (bigger still, a steadier reel and better odds of rare
 * fish). Bait is used up one per fish caught; tackle wears out after {@link #TACKLE_USES} fish. Load either onto
 * a Reinforced or Angler's Rod by clicking it onto the rod in your inventory.
 */
public final class Gear {
    public static final int TACKLE_USES = 20, MAX_BAIT = 64;

    public enum Rod {
        PLAIN(0, 0, 0, false), REINFORCED(1, .05, .1, true), ANGLERS(2, .1, .2, true);
        public final int tier;
        /** Added to the catch zone (as a share of the track). */
        public final double zone;
        /** The catch meter fills this much faster. */
        public final double reel;
        public final boolean loads;
        Rod(int tier, double zone, double reel, boolean loads) { this.tier = tier; this.zone = zone; this.reel = reel; this.loads = loads; }
        /** Rare, epic and legendary fish bite this much more often on this rod. */
        public double rareOdds() { return 1 + .12 * tier; }
    }

    public enum Bait {
        /** Bites come quicker; freshwater fish like them most. */
        BAIT_WORMS(.25),
        /** Sea fish come in for it. */
        CHUM(.25),
        /** Night and cave fish can't resist it. */
        GLOW_BAIT(.2),
        /** Legends and epic fish are drawn to it. */
        LEGEND_LURE(.1);
        /** Shorter wait for a bite (share of the wait). */
        public final double quicker;
        Bait(double quicker) { this.quicker = quicker; }
        public String id() { return name().toLowerCase(Locale.ROOT); }
        public static Bait byId(String id) {
            for (var b : values()) if (b.id().equals(id)) return b;
            return null;
        }
        /** How much likelier this bait makes a fish. */
        public double odds(Fish f) {
            return switch (this) {
                case BAIT_WORMS -> f.water().contains("river") || f.water().contains("lake") || f.water().contains("swamp") ? 1.5 : 1;
                case CHUM -> f.water().contains("ocean") || f.water().contains("warm") || f.water().contains("cold") || f.water().contains("deep") ? 1.5 : 1;
                case GLOW_BAIT -> f.time().contains("night") || f.water().contains("cave") || f.water().contains("deepcave") ? 2 : 1;
                case LEGEND_LURE -> f.legendary() ? 4 : f.rarity() == Fish.Rarity.EPIC ? 2 : 1;
            };
        }
    }

    public enum Tackle {
        /** A bigger catch zone. */
        CORK_BOBBER,
        /** Fish move more slowly. */
        LEAD_SINKER,
        /** The catch meter drains more slowly while the fish is out of the zone. */
        BARBED_HOOK,
        /** Treasure turns up twice as often. */
        TREASURE_HOOK,
        /** Bites come quicker. */
        SPINNER;
        public String id() { return name().toLowerCase(Locale.ROOT); }
        public static Tackle byId(String id) {
            for (var t : values()) if (t.id().equals(id)) return t;
            return null;
        }
        public String effect() {
            return switch (this) {
                case CORK_BOBBER -> "Bigger catch zone";
                case LEAD_SINKER -> "Fish move more slowly";
                case BARBED_HOOK -> "The catch meter drains more slowly";
                case TREASURE_HOOK -> "Treasure turns up twice as often";
                case SPINNER -> "Fish bite sooner";
            };
        }
    }

    public static String baitEffect(Bait b) {
        return switch (b) {
            case BAIT_WORMS -> "Quicker bites; river and lake fish love them";
            case CHUM -> "Quicker bites; draws in sea fish";
            case GLOW_BAIT -> "Night and cave fish can't resist it";
            case LEGEND_LURE -> "Legendary fish bite four times as often";
        };
    }

    /** Ticks shaved off the wait for a bite: bait and a spinner. */
    public static int quicker(Bait bait, Tackle tackle, int wait) {
        double share = (bait == null ? 0 : bait.quicker) + (tackle == Tackle.SPINNER ? .2 : 0);
        return (int) Math.round(wait * Math.min(.6, share));
    }

    private Gear() {}
}
