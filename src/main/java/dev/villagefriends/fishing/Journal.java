package dev.villagefriends.fishing;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import io.netty.buffer.ByteBuf;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;

/**
 * A player's angler's journal: for every fish they've caught, how many and the biggest (in tenths of a
 * centimetre) and the day of the first; and the legends whose tall tales they've heard. Immutable; the
 * journal screen shows an uncaught fish as a silhouette and "???".
 */
public record Journal(Map<String, Entry> entries, Set<String> tales) {
    public record Entry(int count, int best, long first) {
        static final Codec<Entry> CODEC = RecordCodecBuilder.create(i -> i.group(
                Codec.INT.fieldOf("count").forGetter(Entry::count), Codec.INT.fieldOf("best").forGetter(Entry::best),
                Codec.LONG.fieldOf("first").forGetter(Entry::first)).apply(i, Entry::new));
        static final StreamCodec<ByteBuf, Entry> STREAM_CODEC = StreamCodec.composite(
                ByteBufCodecs.VAR_INT, Entry::count, ByteBufCodecs.VAR_INT, Entry::best, ByteBufCodecs.VAR_LONG, Entry::first, Entry::new);
    }
    /** What a catch did to the journal. */
    public record Result(Journal journal, boolean first, boolean record, int previousBest) {}

    public static final Journal EMPTY = new Journal(Map.of(), Set.of());
    public static final Codec<Journal> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.unboundedMap(Codec.STRING, Entry.CODEC).optionalFieldOf("fish", Map.of()).forGetter(Journal::entries),
            Codec.STRING.listOf().xmap(l -> (Set<String>) new LinkedHashSet<>(l), s -> List.copyOf(s)).optionalFieldOf("tales", Set.of()).forGetter(Journal::tales)
    ).apply(i, Journal::new));
    public static final StreamCodec<ByteBuf, Journal> STREAM_CODEC = StreamCodec.composite(
            ByteBufCodecs.map(LinkedHashMap::new, ByteBufCodecs.STRING_UTF8, Entry.STREAM_CODEC), j -> new LinkedHashMap<>(j.entries()),
            ByteBufCodecs.STRING_UTF8.apply(ByteBufCodecs.list()), j -> List.copyOf(j.tales()),
            (m, t) -> new Journal(m, new LinkedHashSet<>(t)));

    public Journal {
        entries = Map.copyOf(entries);
        tales = Set.copyOf(tales);
    }

    public boolean caught(String fish) { return entries.containsKey(fish); }
    public Entry entry(String fish) { return entries.get(fish); }
    public boolean heard(String legend) { return tales.contains(legend); }
    public int species() { return entries.size(); }

    /** Logs a catch of {@code size} tenths of a centimetre on {@code day}. */
    public Result record(String fish, int size, long day) {
        var old = entries.get(fish);
        var next = new LinkedHashMap<>(entries);
        next.put(fish, old == null ? new Entry(1, size, day) : new Entry(old.count() + 1, Math.max(old.best(), size), old.first()));
        return new Result(new Journal(next, tales), old == null, old == null || size > old.best(), old == null ? 0 : old.best());
    }
    /** Notes down a legend's tall tale; the same journal if they'd heard it already. */
    public Journal hear(String legend) {
        if (tales.contains(legend)) return this;
        var next = new LinkedHashSet<>(tales); next.add(legend);
        return new Journal(entries, next);
    }
}
