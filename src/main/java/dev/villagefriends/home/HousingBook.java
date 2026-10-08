package dev.villagefriends.home;

import com.mojang.serialization.Codec;
import com.mojang.serialization.DataResult;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import java.util.HashMap;
import java.util.Map;

/**
 * Every village's housing index on one level (the level that records the village), keyed by village id.
 * Saved as the {@code villagefriends:housing} attachment; an absent attachment is an empty book.
 */
public record HousingBook(int format, Map<String, HousingIndex> villages) {
    public static final int FORMAT = 1;
    public static final HousingBook EMPTY = new HousingBook(FORMAT, Map.of());
    public static final Codec<HousingBook> CODEC = RecordCodecBuilder.<HousingBook>create(i -> i.group(
            Codec.INT.optionalFieldOf("format", FORMAT).forGetter(HousingBook::format),
            Codec.unboundedMap(Codec.STRING, HousingIndex.CODEC).optionalFieldOf("villages", Map.of()).forGetter(HousingBook::villages)
    ).apply(i, HousingBook::new)).validate(b -> b.format() <= FORMAT ? DataResult.success(b)
            : DataResult.error(() -> "Housing format " + b.format() + " is newer than this version understands (" + FORMAT + ")"));

    public HousingBook { villages = Map.copyOf(villages); }
    public HousingIndex get(String village) { return villages.getOrDefault(village, HousingIndex.empty(village)); }
    public HousingBook put(HousingIndex index) {
        if (index == villages.get(index.village())) return this;
        var next = new HashMap<>(villages); next.put(index.village(), index); return new HousingBook(format, next);
    }
}
