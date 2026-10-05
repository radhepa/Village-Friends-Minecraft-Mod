package dev.villagefriends;
import com.mojang.serialization.Codec;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
public record BondBook(Map<String, BondState> bonds) {
    public static final Codec<BondBook> CODEC = Codec.unboundedMap(Codec.STRING, BondState.CODEC).xmap(BondBook::new, BondBook::bonds);
    public BondBook { bonds = Map.copyOf(bonds); }
    public static BondBook empty() { return new BondBook(Map.of()); }
    public BondState get(UUID id) { return bonds.getOrDefault(id.toString(), BondState.NEW); }
    public BondBook with(UUID id, BondState bond) {
        var next = new HashMap<>(bonds); next.put(id.toString(), bond); return new BondBook(next);
    }
}
