package dev.villagefriends.deed;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * What one player has done in one village. Keeps the last {@link #MAX} deeds; when it is full the oldest
 * good deed's worth is {@code banked10} for good before it goes, and bad deeds long faded (four half-lives)
 * are simply forgotten. {@code peakTier} is the highest standing ever reached here, so its rewards come once.
 */
public record DeedLog(String player, String playerName, List<Deed> deeds, int banked10, int peakTier, int serial) {
    public static final int MAX = 48;
    public static final Codec<DeedLog> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.STRING.fieldOf("player").forGetter(DeedLog::player),
            Codec.STRING.optionalFieldOf("player_name", "").forGetter(DeedLog::playerName),
            Deed.CODEC.listOf().optionalFieldOf("deeds", List.of()).forGetter(DeedLog::deeds),
            Codec.INT.optionalFieldOf("banked", 0).forGetter(DeedLog::banked10),
            Codec.INT.optionalFieldOf("peak_tier", 0).forGetter(DeedLog::peakTier),
            Codec.INT.optionalFieldOf("serial", 0).forGetter(DeedLog::serial)
    ).apply(i, DeedLog::new));

    public DeedLog { deeds = List.copyOf(deeds); playerName = playerName == null ? "" : playerName; }
    public static DeedLog create(String player, String name) { return new DeedLog(player, name, List.of(), 0, 0, 0); }

    /** What {@link #record} did: the log afterwards, the deed as it now stands, and whether it folded into an earlier one. */
    public record Recorded(DeedLog log, Deed deed, boolean merged) {}

    /**
     * Records a deed, folding it into the last one of the same kind and key when that is within the kind's
     * merge window. {@code count} is how many (hits, raiders, items) this time; {@code child} is for
     * {@link DeedKind#SAVED_FROM_MONSTER}.
     */
    public Recorded record(DeedKind kind, String key, String label, long day, long tick, List<String> involved, int count, boolean child) {
        count = Math.max(1, count);
        for (int i = deeds.size() - 1; i >= 0 && !key.isEmpty(); i--) {
            var d = deeds.get(i);
            if (d.kind() != kind || !d.key().equals(key)) continue;
            if (kind.mergeTicks == 0 || kind.mergeTicks > 0 && tick - d.tick() > kind.mergeTicks) break;
            int points = kind.good ? Math.max(d.points10(), kind.points10(d.count() + count, child)) : kind.points10(d.count() + count, child);
            var merged = d.again(tick, count, points, involved);
            var next = new ArrayList<>(deeds); next.set(i, merged);
            return new Recorded(new DeedLog(player, playerName, next, banked10, peakTier, serial), merged, true);
        }
        var deed = new Deed(serial + 1, kind, key, label, day, tick, involved, count, kind.points10(count, child), false, day, Map.of());
        var next = new ArrayList<>(deeds); next.add(deed);
        return new Recorded(new DeedLog(player, playerName, next, banked10, peakTier, serial + 1).pruned(day), deed, false);
    }
    /** Replaces a deed (same serial) with a newer version of it. */
    public DeedLog with(Deed deed) {
        var next = new ArrayList<>(deeds);
        for (int i = 0; i < next.size(); i++) if (next.get(i).serial() == deed.serial()) { next.set(i, deed); return new DeedLog(player, playerName, next, banked10, peakTier, serial); }
        return this;
    }
    public Deed find(int serial) {
        for (var d : deeds) if (d.serial() == serial) return d;
        return null;
    }
    public DeedLog peak(int tier) { return tier <= peakTier ? this : new DeedLog(player, playerName, deeds, banked10, tier, serial); }
    public DeedLog named(String name) { return name.equals(playerName) ? this : new DeedLog(player, name, deeds, banked10, peakTier, serial); }

    /** Long-faded bad deeds forgotten, old knowers let go, and the oldest good deeds banked once the log is full. */
    public DeedLog pruned(long today) {
        var next = new ArrayList<Deed>(); int bank = banked10;
        for (var deed : deeds) {
            var d = deed;
            if (!d.good() && d.kind().halfLifeDays > 0 && today - d.day() > 4L * d.kind().halfLifeDays) continue;
            // Past the reaction window only those who lived or saw it still carry it; hearsay is let go.
            if (!d.fresh(today) && d.knowers().values().stream().anyMatch(k -> k.how() == Know.HEARD)) {
                var kept = new java.util.HashMap<String, Know>();
                deed.knowers().forEach((id, k) -> { if (k.how() != Know.HEARD) kept.put(id, k); });
                d = d.withKnowers(kept);
            }
            next.add(d);
        }
        while (next.size() > MAX) {
            int oldest = -1;
            for (int i = 0; i < next.size(); i++) if (next.get(i).good()) { oldest = i; break; }
            if (oldest < 0) oldest = 0; else bank += next.get(oldest).points10();
            next.remove(oldest);
        }
        return new DeedLog(player, playerName, next, bank, peakTier, serial);
    }
}
