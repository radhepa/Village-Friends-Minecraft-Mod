package dev.villagefriends;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

/** Actual health damage, including non-guard contributions; temporary and bounded by time. */
public final class GuardDamageLedger {
    private record Hit(long tick, double damage, UUID guard) {}
    private final List<Hit> hits = new ArrayList<>();

    public boolean record(long now, double before, double after, UUID guard) {
        prune(now);
        double damage = Math.max(0, before - Math.max(0, after));
        if (!Double.isFinite(damage) || damage <= 0) return false;
        hits.add(new Hit(now, damage, guard));
        return true;
    }
    public void prune(long now) { hits.removeIf(h -> now - h.tick() >= GuardPolicy.RECENT_ATTACK_TICKS); }
    public boolean empty(long now) { prune(now); return hits.isEmpty(); }
    public void forgetGuard(UUID id) {
        hits.replaceAll(h -> id.equals(h.guard()) ? new Hit(h.tick(), h.damage(), null) : h);
    }
    public Map<UUID, Double> shares(long now, double pool) {
        prune(now);
        double total = hits.stream().mapToDouble(Hit::damage).sum();
        if (!Double.isFinite(pool) || pool <= 0 || total <= 0) return Map.of();
        var damage = new HashMap<UUID, Double>();
        for (var hit : hits) if (hit.guard() != null) damage.merge(hit.guard(), hit.damage(), Double::sum);
        damage.replaceAll((id, contribution) -> pool * contribution / total);
        return Map.copyOf(damage);
    }
}
