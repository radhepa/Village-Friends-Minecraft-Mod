package dev.villagefriends;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import java.util.ArrayList;
import java.util.List;

/** Personal history is distinct from the resident's shared, physical story outcomes. */
public record BondState(int trust, int chapter, int legacyLevel, int visits, long visitDay,
        long activityDay, List<String> memories, List<String> flags, List<String> recentLines) {
    public static final BondState NEW = new BondState(50, 0, 0, 0, -1, -1, List.of(), List.of(), List.of());
    public static final Codec<BondState> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.INT.optionalFieldOf("trust", 50).forGetter(BondState::trust),
            Codec.INT.optionalFieldOf("chapter", 0).forGetter(BondState::chapter),
            Codec.INT.optionalFieldOf("legacy_level", 0).forGetter(BondState::legacyLevel),
            Codec.INT.optionalFieldOf("visits", 0).forGetter(BondState::visits),
            Codec.LONG.optionalFieldOf("visit_day", -1L).forGetter(BondState::visitDay),
            Codec.LONG.optionalFieldOf("activity_day", -1L).forGetter(BondState::activityDay),
            Codec.STRING.listOf().optionalFieldOf("memories", List.of()).forGetter(BondState::memories),
            Codec.STRING.listOf().optionalFieldOf("flags", List.of()).forGetter(BondState::flags),
            Codec.STRING.listOf().optionalFieldOf("recent_lines", List.of()).forGetter(BondState::recentLines)
    ).apply(i, BondState::new));
    public BondState {
        trust = Math.clamp(trust, 0, 100); chapter = Math.clamp(chapter, 0, 4);
        legacyLevel = Math.clamp(legacyLevel, 0, 4); visits = Math.max(visits, 0);
        memories = bounded(memories, 24); flags = List.copyOf(flags.stream().distinct().toList()); recentLines = bounded(recentLines, 12);
    }
    private static List<String> bounded(List<String> list, int max) {
        return List.copyOf(list.subList(Math.max(0, list.size() - max), list.size()));
    }
    public static BondState migrated(int oldLevel) { return NEW.copy(50, 0, oldLevel, 0, -1, -1, NEW.memories, NEW.flags, NEW.recentLines); }
    private BondState copy(int t, int c, int l, int v, long vd, long ad, List<String> m, List<String> f, List<String> r) {
        return new BondState(t, c, l, v, vd, ad, m, f, r);
    }
    public BondState visit(long day) {
        return visitDay == day ? this : copy(trust, chapter, legacyLevel, visits + 1, day, activityDay, memories, flags, recentLines);
    }
    public BondState chapter(int next) { return copy(trust, next, legacyLevel, visits, visitDay, activityDay, memories, flags, recentLines); }
    public BondState trust(int amount) { return copy(trust + amount, chapter, legacyLevel, visits, visitDay, activityDay, memories, flags, recentLines); }
    public BondState flag(String flag) {
        if (has(flag)) return this;
        var next = new ArrayList<>(flags); next.add(flag);
        return copy(trust, chapter, legacyLevel, visits, visitDay, activityDay, memories, next, recentLines);
    }
    public BondState unflag(String flag) {
        var next = new ArrayList<>(flags); next.remove(flag);
        return copy(trust, chapter, legacyLevel, visits, visitDay, activityDay, memories, next, recentLines);
    }
    public boolean has(String flag) { return flags.contains(flag); }
    public BondState remember(long day, String event) {
        var next = new ArrayList<>(memories); next.add("Day " + (day + 1) + ": " + event.substring(0, Math.min(200, event.length())));
        return copy(trust, chapter, legacyLevel, visits, visitDay, activityDay, next, flags, recentLines);
    }
    public BondState line(String id) {
        var next = new ArrayList<>(recentLines); next.remove(id); next.add(id);
        return copy(trust, chapter, legacyLevel, visits, visitDay, activityDay, memories, flags, next);
    }
    public BondState activity(long day, String type) {
        return copy(trust + (activityDay == day ? 0 : 5), chapter, legacyLevel, visits, visitDay, day, memories, flags, recentLines)
                .flag("activity:" + type).flag("shared_experience").remember(day, "We shared " + type + " together.");
    }
    public int level(FriendshipState affinity) {
        int gate = chapter >= 4 && visits >= 5 ? 4 : chapter >= 3 ? 3 : has("shared_experience") ? 2 : 1;
        return Math.max(legacyLevel, Math.min(affinity.level(), gate));
    }
    public String trustLabel() { return trust < 30 ? "Wary" : trust < 50 ? "Hesitant" : trust < 70 ? "Comfortable" : "Trusting"; }
}
