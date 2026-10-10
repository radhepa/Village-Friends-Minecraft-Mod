package dev.villagefriends.stable.breed;

import dev.villagefriends.stable.data.StableTable;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.random.RandomGenerator;

/**
 * Which breed a horse found in a biome is, pure so it can be unit tested. The world side ({@link Breeds#keywords})
 * turns a biome into keywords ("plains", "taiga", "snowy"...); every breed row lists the keywords it is found under
 * with a weight, and "any" matches everywhere. The pick is weighted over every matching row, so a plains horse is
 * usually a rouncey or palfrey and only sometimes a destrier.
 */
public final class BreedPicker {
    /** The breed used when nothing matches (an empty table or a biome no row names). */
    public static final String FALLBACK = "rouncey";
    /** The keyword every biome has. */
    public static final String ANY = "any";

    public static String pick(Set<String> keywords, List<StableTable.Breed> breeds, RandomGenerator random) {
        var weights = weights(keywords, breeds);
        int total = weights.values().stream().mapToInt(Integer::intValue).sum();
        if (total <= 0) return FALLBACK;
        int roll = random.nextInt(total);
        for (var e : weights.entrySet()) if ((roll -= e.getValue()) < 0) return e.getKey();
        return FALLBACK;
    }

    /** Each breed's summed weight for these keywords (breeds that don't match are left out), in table order. */
    public static Map<String, Integer> weights(Set<String> keywords, List<StableTable.Breed> breeds) {
        var out = new LinkedHashMap<String, Integer>();
        for (var b : breeds) for (var s : b.spawns())
            if (s.weight() > 0 && (s.biome().equals(ANY) || keywords.contains(s.biome()))) out.merge(b.id(), s.weight(), Integer::sum);
        return out;
    }

    private BreedPicker() {}
}
