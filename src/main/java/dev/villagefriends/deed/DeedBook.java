package dev.villagefriends.deed;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import java.util.HashMap;
import java.util.Map;

/**
 * Every player's deeds in every village recorded on one level: village id, then player UUID. Kept as a
 * level attachment next to the village societies; absent means nobody has done anything yet.
 */
public record DeedBook(int format, Map<String, Map<String, DeedLog>> villages) {
    public static final int FORMAT = 1;
    public static final DeedBook EMPTY = new DeedBook(FORMAT, Map.of());
    public static final Codec<DeedBook> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.INT.optionalFieldOf("format", FORMAT).forGetter(DeedBook::format),
            Codec.unboundedMap(Codec.STRING, Codec.unboundedMap(Codec.STRING, DeedLog.CODEC)).optionalFieldOf("villages", Map.of()).forGetter(DeedBook::villages)
    ).apply(i, DeedBook::new));

    public DeedBook {
        var copy = new HashMap<String, Map<String, DeedLog>>();
        villages.forEach((village, logs) -> copy.put(village, Map.copyOf(logs)));
        villages = Map.copyOf(copy);
    }

    /** All players' logs in a village. */
    public Map<String, DeedLog> logs(String village) { return villages.getOrDefault(village, Map.of()); }
    /** A player's log in a village, or null. */
    public DeedLog log(String village, String player) { return logs(village).get(player); }
    public DeedBook put(String village, DeedLog log) {
        if (log == log(village, log.player())) return this;
        var logs = new HashMap<>(logs(village)); logs.put(log.player(), log);
        var next = new HashMap<>(villages); next.put(village, logs);
        return new DeedBook(format, next);
    }
}
