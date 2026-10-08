package dev.villagefriends;

import static dev.villagefriends.VillageFriends.*;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;
import java.util.UUID;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.Identifier;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.npc.villager.VillagerData;
import net.minecraft.world.entity.projectile.arrow.AbstractArrow;

/** Server authority for saved progression and ephemeral kill contributions. */
public final class GuardProgression {
    public static final Identifier HEALTH_BONUS = Identifier.fromNamespaceAndPath("villagefriends", "guard_level_health");
    private record Probe(DamageSource source, float health, UUID guard, long tick) {}
    private static final class Credit {
        final ServerLevel level;
        final GuardDamageLedger ledger = new GuardDamageLedger();
        DamageSource lastSource;
        UUID lastGuard;
        Credit(ServerLevel level) { this.level = level; }
    }
    private static final Map<UUID, Probe> probes = new HashMap<>();
    private static final Map<UUID, Credit> credits = new HashMap<>();

    public static GuardProgress progress(Villager v) { return target(v).getAttached(GUARD_PROGRESS); }
    public static void loaded(Villager v) { refresh(v); }
    public static void refresh(Villager v) {
        if (!(v.level() instanceof ServerLevel)) return;
        var saved = progress(v);
        if (saved != null && !saved.lockedProfession().isEmpty() && !v.isBaby()) {
            var locked = lockedData(v, v.getVillagerData());
            if (!locked.profession().equals(v.getVillagerData().profession())) v.setVillagerData(locked);
        }
        float health = v.getHealth(), oldMaximum = v.getMaxHealth();
        boolean initialized = false;
        if (GuardController.isGuard(v)) {
            if (saved == null) {
                saved = GuardProgress.initialize(null, v.getUUID(), target(v).getAttachedOrElse(GUARD_OBSERVED, false), target(v).hasAttached(PROFILE));
                target(v).setAttached(GUARD_PROGRESS, saved); initialized = true;
            }
        } else if (!target(v).getAttachedOrElse(GUARD_OBSERVED, false)) target(v).setAttached(GUARD_OBSERVED, true);
        var attribute = v.getAttribute(Attributes.MAX_HEALTH);
        if (attribute == null) return;
        double amount = GuardController.isGuard(v) && saved != null ? saved.extraHealth() : 0;
        var old = attribute.getModifier(HEALTH_BONUS);
        if (amount == 0) {
            if (old != null) attribute.removeModifier(HEALTH_BONUS);
        } else if (old == null || old.amount() != amount) {
            // Persist the modifier so native NBT health loading does not clamp an injured veteran to 20 HP.
            attribute.addOrReplacePermanentModifier(new AttributeModifier(HEALTH_BONUS, amount, AttributeModifier.Operation.ADD_VALUE));
        }
        float nextHealth = initialized && oldMaximum > 0 ? health / oldMaximum * v.getMaxHealth() : health;
        nextHealth = Math.min(nextHealth, v.getMaxHealth());
        if (v.getHealth() != nextHealth) v.setHealth(nextHealth);
    }
    /** Practice at the training dummy or archery target: a little experience, without a kill. */
    public static void train(Villager v, double xp) {
        if (!GuardController.isGuard(v)) return;
        refresh(v);
        var saved = progress(v);
        if (saved == null) return;
        target(v).setAttached(GUARD_PROGRESS, saved.award(xp)); refresh(v);
    }
    public static VillagerData lockedData(Villager v, VillagerData proposed) {
        var saved = progress(v);
        if (saved == null || saved.lockedProfession().isEmpty() || v.isBaby()) return proposed;
        String job = saved.lockedProfession().substring("villagefriends:".length());
        return proposed.withProfession(v.level().registryAccess(), VillageProfessions.key(job));
    }
    public static void converted(Entity after) {
        if (after instanceof Villager v) refresh(v);
        else if (after instanceof LivingEntity living && living.getAttribute(Attributes.MAX_HEALTH) != null) {
            living.getAttribute(Attributes.MAX_HEALTH).removeModifier(HEALTH_BONUS);
            living.setHealth(Math.min(living.getHealth(), living.getMaxHealth()));
        }
    }
    public static double damageMultiplier(Villager v) {
        var saved = progress(v);
        return GuardController.isGuard(v) && saved != null ? saved.damageMultiplier() : 1;
    }
    public static float arrowDamage(AbstractArrow arrow, float nativeDamage) {
        int level = target(arrow).getAttachedOrElse(GUARD_ARROW_LEVEL, 0);
        return (float)(nativeDamage * (1 + .005 * Math.clamp(level, 0, GuardProgress.MAX_LEVEL)));
    }
    public static void captureArrow(Villager v, AbstractArrow arrow) {
        var saved = progress(v);
        target(arrow).setAttached(GUARD_ARROW_LEVEL, saved == null ? 0 : saved.level());
    }
    public static String journal(Villager v) {
        var saved = progress(v);
        if (!GuardController.isGuard(v) || saved == null) return "";
        String xp = saved.level() == GuardProgress.MAX_LEVEL ? "MAX" : String.format(Locale.ROOT, "%.2f / %d", saved.xp(), GuardProgress.nextLevelXp(saved.level()));
        return String.format(Locale.ROOT, "Guard level: %d / %d\nGuard XP: %s\nLevel bonuses: +%.1f HP, +%.1f%% direct damage\nProfession: %s\n\n",
                saved.level(), GuardProgress.MAX_LEVEL, xp, saved.extraHealth(), 100 * (saved.damageMultiplier() - 1),
                saved.lockedProfession().isEmpty() ? "Not combat-locked yet; first qualifying kill locks this role." : "Combat-locked " + VillageProfessions.label(profession(v)) + ".");
    }

    public static void beforeDamage(LivingEntity entity, DamageSource source) {
        if (!(entity instanceof Mob mob) || entity instanceof Villager || !(entity.level() instanceof ServerLevel level)) return;
        UUID guard = null;
        Entity owner = GuardController.attacker(source);
        if (owner instanceof Villager v && GuardController.isGuard(v) && GuardController.threat(mob, level)
                && (source.getDirectEntity() == v || source.getDirectEntity() instanceof AbstractArrow arrow && target(arrow).hasAttached(GUARD_ARROW_TARGET)))
            guard = v.getUUID();
        probes.put(entity.getUUID(), new Probe(source, entity.getHealth(), guard, level.getGameTime()));
    }
    public static void afterDamage(LivingEntity entity, DamageSource source) {
        var probe = probes.remove(entity.getUUID());
        if (probe == null || probe.source() != source || !(entity.level() instanceof ServerLevel level)) return;
        var credit = credits.computeIfAbsent(entity.getUUID(), id -> new Credit(level));
        if (credit.ledger.record(probe.tick(), probe.health(), entity.getHealth(), probe.guard())) {
            credit.lastSource = source; credit.lastGuard = probe.guard();
        }
        if (credit.ledger.empty(level.getGameTime())) credits.remove(entity.getUUID());
    }
    public static void afterDeath(LivingEntity entity, DamageSource source) {
        afterDamage(entity, source);
        var credit = credits.remove(entity.getUUID()); // Removal makes duplicate death notifications harmless.
        if (credit == null || credit.level != entity.level()) return;
        int pool = GuardProgress.killXp(BuiltInRegistries.ENTITY_TYPE.getKey(entity.getType()).toString());
        for (var share : credit.ledger.shares(credit.level.getGameTime(), pool).entrySet()) {
            if (!(credit.level.getEntity(share.getKey()) instanceof Villager v) || !v.isAlive() || !GuardController.isGuard(v)) continue;
            refresh(v);
            var saved = progress(v).award(share.getValue());
            if (credit.lastSource == source && v.getUUID().equals(credit.lastGuard))
                saved = saved.lock(v.getVillagerData().profession().unwrapKey().orElseThrow().identifier().toString());
            target(v).setAttached(GUARD_PROGRESS, saved); refresh(v);
        }
    }
    public static void unload(Entity entity) {
        probes.remove(entity.getUUID()); credits.remove(entity.getUUID());
        if (entity instanceof Villager) for (var credit : credits.values()) credit.ledger.forgetGuard(entity.getUUID());
    }
    public static void tick(MinecraftServer server) {
        probes.clear();
        if (server.getTickCount() % 20 == 0)
            credits.entrySet().removeIf(e -> e.getValue().level.getEntity(e.getKey()) == null
                    || e.getValue().ledger.empty(e.getValue().level.getGameTime()));
    }
    public static void clear() { probes.clear(); credits.clear(); }
}
