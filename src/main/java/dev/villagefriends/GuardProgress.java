package dev.villagefriends;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import java.util.Random;
import java.util.UUID;

/** Combat progression is independent of vanilla trading XP and player friendship. */
public record GuardProgress(int level, double xp, String origin, String lockedProfession) {
    public static final int MAX_LEVEL = 50;
    public static final Codec<GuardProgress> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.INT.optionalFieldOf("level", 0).forGetter(GuardProgress::level),
            Codec.DOUBLE.optionalFieldOf("xp", 0D).forGetter(GuardProgress::xp),
            Codec.STRING.optionalFieldOf("origin", "trained").forGetter(GuardProgress::origin),
            Codec.STRING.optionalFieldOf("locked_profession", "").forGetter(GuardProgress::lockedProfession)
    ).apply(i, GuardProgress::new));

    public GuardProgress {
        level = Math.clamp(level, 0, MAX_LEVEL);
        xp = Double.isFinite(xp) ? Math.max(0, xp) : 0;
        while (level < MAX_LEVEL && xp + 1e-9 >= nextLevelXp(level)) { xp = Math.max(0, xp - nextLevelXp(level)); level++; }
        if (level == MAX_LEVEL) xp = 0;
        if (!"generated".equals(origin) && !"migrated".equals(origin)) origin = "trained";
        if (!isGuardProfession(lockedProfession)) lockedProfession = "";
    }
    public static boolean isGuardProfession(String key) {
        return "villagefriends:knight".equals(key) || "villagefriends:archer".equals(key);
    }
    public static int nextLevelXp(int level) { return 20 + 3 * Math.clamp(level, 0, MAX_LEVEL); }
    public static GuardProgress initialize(GuardProgress existing, UUID id, boolean trained, boolean legacy) {
        if (existing != null) return existing;
        var random = new Random(id.getMostSignificantBits() ^ Long.rotateLeft(id.getLeastSignificantBits(), 23) ^ 0x47554152444C564CL);
        int start = trained ? 0 : 15 + (random.nextInt(16) + random.nextInt(16)) / 2;
        return new GuardProgress(start, 0, trained ? "trained" : legacy ? "migrated" : "generated", "");
    }
    public GuardProgress award(double gained) {
        return Double.isFinite(gained) && gained > 0 && level < MAX_LEVEL
                ? new GuardProgress(level, xp + gained, origin, lockedProfession) : this;
    }
    public GuardProgress lock(String profession) {
        return lockedProfession.isEmpty() && isGuardProfession(profession)
                ? new GuardProgress(level, xp, origin, profession) : this;
    }
    public double extraHealth() { return .2 * level; }
    public double damageMultiplier() { return 1 + .005 * level; }
    public static int killXp(String entityType) {
        return switch (entityType) {
            case "minecraft:pillager" -> 15;
            case "minecraft:vindicator", "minecraft:illusioner", "minecraft:zoglin" -> 20;
            case "minecraft:evoker" -> 30;
            case "minecraft:ravager" -> 50;
            default -> 10;
        };
    }
}
