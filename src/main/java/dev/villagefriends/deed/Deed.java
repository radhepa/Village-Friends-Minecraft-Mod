package dev.villagefriends.deed;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * One thing a player did in a village. {@code key} decides what repeats fold into it (the victim, the raid,
 * the house or the pet), {@code label} names the place or pet for dialogue ("the Ashford House"),
 * {@code involved} lists the residents it happened to (by id), {@code count} how many times it was done
 * (hits, raiders, items taken) and {@code points10} what it is worth, in tenths of a notice, before fading.
 * {@code spread} is the last day rumors were passed on, so unloaded days are caught up. {@code knowers} maps
 * each resident who knows about it to how they know.
 */
public record Deed(int serial, DeedKind kind, String key, String label, long day, long tick, List<String> involved, int count,
        int points10, boolean apologized, long spread, Map<String, Know> knowers) {
    public static final Codec<Deed> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.INT.fieldOf("serial").forGetter(Deed::serial),
            DeedKind.CODEC.fieldOf("kind").forGetter(Deed::kind),
            Codec.STRING.optionalFieldOf("key", "").forGetter(Deed::key),
            Codec.STRING.optionalFieldOf("label", "").forGetter(Deed::label),
            Codec.LONG.optionalFieldOf("day", 0L).forGetter(Deed::day),
            Codec.LONG.optionalFieldOf("tick", 0L).forGetter(Deed::tick),
            Codec.STRING.listOf().optionalFieldOf("involved", List.of()).forGetter(Deed::involved),
            Codec.INT.optionalFieldOf("count", 1).forGetter(Deed::count),
            Codec.INT.optionalFieldOf("points", 0).forGetter(Deed::points10),
            Codec.BOOL.optionalFieldOf("apologized", false).forGetter(Deed::apologized),
            Codec.LONG.optionalFieldOf("spread", 0L).forGetter(Deed::spread),
            Codec.unboundedMap(Codec.STRING, Know.CODEC).optionalFieldOf("knowers", Map.of()).forGetter(Deed::knowers)
    ).apply(i, Deed::new));
    /** Residents stop bringing a deed up after this many days (good) or {@link #BAD_WINDOW} (bad); knowers are dropped after it. */
    public static final int GOOD_WINDOW = 14, BAD_WINDOW = 28;

    public Deed {
        key = key == null ? "" : key; label = label == null ? "" : label;
        involved = List.copyOf(involved); knowers = Map.copyOf(knowers);
        count = Math.max(1, count);
    }

    public boolean good() { return kind.good; }
    public Know know(String resident) { return knowers.get(resident); }
    public boolean knows(String resident) { return knowers.containsKey(resident); }
    /** The first resident it happened to, or "". */
    public String victim() { return involved.isEmpty() ? "" : involved.getFirst(); }

    /** Someone learns about it, keeping the closest way they know it. */
    public Deed learn(String resident, Know how) {
        var old = knowers.get(resident);
        var next = old == null ? how : old.closer(how);
        if (next.equals(old)) return this;
        var map = new HashMap<>(knowers); map.put(resident, next);
        return withKnowers(map);
    }
    public Deed withKnowers(Map<String, Know> next) {
        return new Deed(serial, kind, key, label, day, tick, involved, count, points10, apologized, spread, next);
    }
    public Deed replace(String resident, Know know) {
        var map = new HashMap<>(knowers); map.put(resident, know); return withKnowers(map);
    }
    public Deed spreadTo(long today) { return new Deed(serial, kind, key, label, day, tick, involved, count, points10, apologized, Math.max(spread, today), knowers); }
    public Deed apologize() { return new Deed(serial, kind, key, label, day, tick, involved, count, points10, true, spread, knowers); }
    /** Another of the same deed within the merge window: counted together. */
    public Deed again(long now, int more, int points, List<String> alsoInvolved) {
        var who = new java.util.ArrayList<>(involved);
        for (var id : alsoInvolved) if (!who.contains(id)) who.add(id);
        return new Deed(serial, kind, key, label, day, now, who, count + more, points, apologized, spread, knowers);
    }
    /** Whether residents still bring it up, {@code today}. */
    public boolean fresh(long today) { return today - day <= (good() ? GOOD_WINDOW : BAD_WINDOW); }
}
