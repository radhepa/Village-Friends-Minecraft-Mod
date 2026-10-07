package dev.villagefriends.social;

import com.mojang.serialization.Codec;
import java.util.HashMap;
import java.util.Map;

/** Every village's society on one level, keyed by village ID. */
public record SocietyBook(Map<String, Society> villages) {
    public static final SocietyBook EMPTY = new SocietyBook(Map.of());
    public static final Codec<SocietyBook> CODEC = Codec.unboundedMap(Codec.STRING, Society.CODEC).xmap(SocietyBook::new, SocietyBook::villages);
    public SocietyBook { villages = Map.copyOf(villages); }
    public Society get(String village, long day) { return villages.getOrDefault(village, Society.create(village, day)); }
    public SocietyBook put(Society society) {
        if (society == villages.get(society.village())) return this;
        var next = new HashMap<>(villages); next.put(society.village(), society); return new SocietyBook(next);
    }
}
