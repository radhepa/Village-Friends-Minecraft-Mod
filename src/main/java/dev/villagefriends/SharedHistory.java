package dev.villagefriends;
import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
public record SharedHistory(Map<String, String> outcomes, List<String> neighbors, Map<String, Integer> residentFriends, long socialDay) {
    public static final SharedHistory EMPTY = new SharedHistory(Map.of(), List.of());
    public static final Codec<SharedHistory> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.unboundedMap(Codec.STRING, Codec.STRING).optionalFieldOf("outcomes", Map.of()).forGetter(SharedHistory::outcomes),
            Codec.STRING.listOf().optionalFieldOf("neighbors", List.of()).forGetter(SharedHistory::neighbors),
            Codec.unboundedMap(Codec.STRING, Codec.intRange(0, 20)).optionalFieldOf("resident_friends", Map.of()).forGetter(SharedHistory::residentFriends),
            Codec.LONG.optionalFieldOf("social_day", -1L).forGetter(SharedHistory::socialDay)
    ).apply(i, SharedHistory::new));
    public SharedHistory { outcomes = Map.copyOf(outcomes); neighbors = List.copyOf(neighbors.stream().limit(4).toList()); residentFriends = Map.copyOf(residentFriends); }
    public SharedHistory(Map<String, String> outcomes, List<String> neighbors) { this(outcomes, neighbors, Map.of(), -1); }
    public boolean done(String id) { return outcomes.containsKey(id); }
    public SharedHistory complete(String id, String contributor) {
        var next = new HashMap<>(outcomes); next.putIfAbsent(id, contributor); return new SharedHistory(next, neighbors, residentFriends, socialDay);
    }
    public SharedHistory neighbors(List<String> names) { return new SharedHistory(outcomes, names, residentFriends, socialDay); }
    public SharedHistory mingle(long day, Map<String, Integer> company) {
        if (day == socialDay || company.isEmpty()) return this;
        var next = new HashMap<>(residentFriends);
        company.forEach((id, amount) -> next.merge(id, amount, (a, b) -> Math.min(20, a + b)));
        var kept = new HashMap<String, Integer>();
        next.entrySet().stream().sorted(java.util.Comparator.<Map.Entry<String,Integer>>comparingInt(Map.Entry::getValue).reversed().thenComparing(Map.Entry::getKey))
                .limit(16).forEach(e -> kept.put(e.getKey(), e.getValue()));
        return new SharedHistory(outcomes, neighbors, kept, day);
    }
}
