package dev.villagefriends;
import com.mojang.serialization.Codec;
import java.util.*;
import net.minecraft.core.BlockPos;
public record VillageBook(Map<String,VillageRecord> villages) {
    public static final VillageBook EMPTY = new VillageBook(Map.of());
    public static final Codec<VillageBook> CODEC = Codec.unboundedMap(Codec.STRING,VillageRecord.CODEC).xmap(VillageBook::new,VillageBook::villages);
    public VillageBook { villages = Map.copyOf(villages); }
    public VillageBook put(VillageRecord village) { var next=new HashMap<>(villages);next.put(village.id(),village);return new VillageBook(next); }
    public VillageRecord at(BlockPos pos) { return villages.values().stream().filter(v -> v.contains(pos)).min(Comparator.comparingLong((VillageRecord v)->v.distance(pos)).thenComparing(VillageRecord::id)).orElse(null); }
}
