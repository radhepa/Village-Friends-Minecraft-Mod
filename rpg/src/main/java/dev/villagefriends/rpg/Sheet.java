package dev.villagefriends.rpg;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * A player's whole RPG character, stored on the player (kept through death) and synced to its owner.
 * Immutable: every change returns a new sheet. {@code xp} is progress inside the current level;
 * {@code marks} holds counters, cooldowns and remembered stat values.
 */
public record Sheet(int level, long xp, int points, Map<String, Integer> attrs, Map<String, Long> skills,
                    Map<String, Integer> kills, List<Quest> quests, Map<String, Long> marks) {
    public static final Sheet NEW = new Sheet(1, 0, 0, Map.of(), Map.of(), Map.of(), List.of(), Map.of());
    public static final Codec<Sheet> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.INT.optionalFieldOf("level", 1).forGetter(Sheet::level),
            Codec.LONG.optionalFieldOf("xp", 0L).forGetter(Sheet::xp),
            Codec.INT.optionalFieldOf("points", 0).forGetter(Sheet::points),
            Codec.unboundedMap(Codec.STRING, Codec.INT).optionalFieldOf("attrs", Map.of()).forGetter(Sheet::attrs),
            Codec.unboundedMap(Codec.STRING, Codec.LONG).optionalFieldOf("skills", Map.of()).forGetter(Sheet::skills),
            Codec.unboundedMap(Codec.STRING, Codec.INT).optionalFieldOf("kills", Map.of()).forGetter(Sheet::kills),
            Quest.CODEC.listOf().optionalFieldOf("quests", List.of()).forGetter(Sheet::quests),
            Codec.unboundedMap(Codec.STRING, Codec.LONG).optionalFieldOf("marks", Map.of()).forGetter(Sheet::marks)
    ).apply(i, Sheet::new));

    public int attr(Attr a) { return attrs.getOrDefault(a.id(), 0); }
    public long skillXp(Skill s) { return skills.getOrDefault(s.id(), 0L); }
    public int skill(Skill s) { return Balance.skillLevel(skillXp(s)); }
    public int kills(String family) { return kills.getOrDefault(family, 0); }
    public int tier(Bestiary.Family f) { return f.tier(kills(f.id())); }
    public long mark(String key) { return marks.getOrDefault(key, 0L); }
    public int spentPoints() { return attrs.values().stream().mapToInt(Integer::intValue).sum(); }

    // -- changes -----------------------------------------------------------------------------------
    /** Adds character experience, levelling up as often as it covers; points come with each level. */
    public Sheet gain(long amount) {
        int l = level; long x = xp + Math.max(0, amount); int pts = points;
        while (l < Balance.MAX_LEVEL && x >= Balance.need(l)) { x -= Balance.need(l); l++; pts += Balance.pointsAt(l); }
        if (l >= Balance.MAX_LEVEL) x = 0;
        return new Sheet(l, x, pts, attrs, skills, kills, quests, marks);
    }
    /** Death: lose a share of the progress into the current level, never a level. */
    public Sheet penalized(double share) { return new Sheet(level, Math.round(xp * (1 - share)), points, attrs, skills, kills, quests, marks); }
    public Sheet withLevel(int l) {
        l = Math.clamp(l, 1, Balance.MAX_LEVEL);
        return new Sheet(l, 0, Math.max(0, Balance.pointsThrough(l) - spentPoints()), attrs, skills, kills, quests, marks);
    }
    public Sheet spend(Attr a, int count) {
        int n = Math.min(count, Math.min(points, Balance.ATTR_CAP - attr(a)));
        if (n <= 0) return this;
        return new Sheet(level, xp, points - n, put(attrs, a.id(), attr(a) + n), skills, kills, quests, marks);
    }
    public Sheet respec() { return new Sheet(level, xp, points + spentPoints(), Map.of(), skills, kills, quests, marks); }
    public Sheet skillGain(Skill s, long amount) { return amount <= 0 ? this : new Sheet(level, xp, points, attrs, put(skills, s.id(), skillXp(s) + amount), kills, quests, marks); }
    public Sheet withSkillXp(Skill s, long total) { return new Sheet(level, xp, points, attrs, put(skills, s.id(), Math.max(0, total)), kills, quests, marks); }
    public Sheet kill(String family, int n) { return new Sheet(level, xp, points, attrs, skills, put(kills, family, kills(family) + n), quests, marks); }
    public Sheet withQuests(List<Quest> q) { return new Sheet(level, xp, points, attrs, skills, kills, List.copyOf(q), marks); }
    public Sheet mark(String key, long value) { return new Sheet(level, xp, points, attrs, skills, kills, quests, put(marks, key, value)); }
    public Sheet unmark(String key) {
        if (!marks.containsKey(key)) return this;
        var m = new HashMap<>(marks); m.remove(key);
        return new Sheet(level, xp, points, attrs, skills, kills, quests, Map.copyOf(m));
    }
    /** Applies {@code fn} to every quest, keeping order. */
    public Sheet mapQuests(java.util.function.UnaryOperator<Quest> fn) {
        var out = new ArrayList<Quest>(quests.size()); boolean changed = false;
        for (var q : quests) { var n = fn.apply(q); changed |= n != q; out.add(n); }
        return changed ? withQuests(out) : this;
    }
    private static <V> Map<String, V> put(Map<String, V> map, String key, V value) {
        var m = new HashMap<>(map); m.put(key, value); return Map.copyOf(m);
    }

    // -- mastery perks -----------------------------------------------------------------------------
    /** Sum of unlocked perk amounts of one kind and key ("" key matches any). */
    public double perk(String kind, String key) {
        double sum = 0;
        for (var f : Bestiary.FAMILIES) {
            int t = tier(f); if (t < 3) continue;
            for (var p : f.perks()) if (p.tier() <= t && p.kind().equals(kind) && (key.isEmpty() || p.key().equals(key))) sum += p.amount();
        }
        return sum;
    }
    public boolean special(String id) { return hasPerk("special", id); }
    public boolean immune(String effect) {
        for (var f : Bestiary.FAMILIES) {
            int t = tier(f); if (t < 3) continue;
            for (var p : f.perks()) if (p.tier() <= t && p.kind().equals("immune") && List.of(p.key().split(",")).contains(effect)) return true;
        }
        return false;
    }
    private boolean hasPerk(String kind, String key) {
        for (var f : Bestiary.FAMILIES) {
            int t = tier(f); if (t < 3) continue;
            for (var p : f.perks()) if (p.tier() <= t && p.kind().equals(kind) && p.key().equals(key)) return true;
        }
        return false;
    }
    public int masteries() { int n = 0; for (var f : Bestiary.FAMILIES) if (tier(f) >= 5) n++; return n; }
}
