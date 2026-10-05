package dev.villagefriends.outfit;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

final class ModelChecks {
    static void id(String id) {
        if (id == null || !id.matches("[a-z0-9_]+")) throw new IllegalArgumentException("Invalid model id");
    }
    static <T> List<T> nonempty(List<T> values, String label) {
        var copy = List.copyOf(values);
        if (copy.isEmpty()) throw new IllegalArgumentException("Missing " + label);
        return copy;
    }
    static <T> Set<T> nonempty(Set<T> values, String label) {
        var copy = Set.copyOf(values);
        if (copy.isEmpty()) throw new IllegalArgumentException("Missing " + label);
        return copy;
    }
    static void unique(List<String> ids) {
        if (new HashSet<>(ids).size() != ids.size()) throw new IllegalArgumentException("Duplicate model ids");
    }
    private ModelChecks() {}
}
