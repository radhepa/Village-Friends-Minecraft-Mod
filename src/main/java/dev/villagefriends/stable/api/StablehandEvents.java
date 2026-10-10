package dev.villagefriends.stable.api;

import net.fabricmc.fabric.api.event.Event;
import net.fabricmc.fabric.api.event.EventFactory;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.animal.equine.AbstractHorse;

/**
 * Stablehand's hooks for add-ons (the RPG add-on's Riding skill listens to all three). Register listeners during
 * mod initialization; they run on the server thread. Village Friends never depends on who listens.
 */
public final class StablehandEvents {
    /** What a {@link RidingBonus} can improve. */
    public enum Aspect { HORSE_SPEED, BOND_GAIN, LANCE_DAMAGE, MOUNTED_AIM }

    /** After a bond gain has been applied. {@code source}: "groom", "feed", "ride" or "api"; tiers are 0 (Wary) to 4 (Devoted). */
    @FunctionalInterface public interface BondGained {
        void onBondGained(ServerPlayer player, AbstractHorse horse, String source, int amount, int tierBefore, int tierAfter);
    }
    /** A couched lance from horseback hit something. {@code speed} is the horse's speed in blocks per second. */
    @FunctionalInterface public interface LanceHit {
        void onLanceHit(ServerPlayer player, LivingEntity target, float damage, double speed);
    }
    /** An extra fraction for an aspect (0.1 = +10%). The listeners' answers are added up; Village Friends alone gives 0. */
    @FunctionalInterface public interface RidingBonus {
        double bonus(ServerPlayer player, Aspect aspect);
    }

    public static final Event<BondGained> BOND_GAINED = EventFactory.createArrayBacked(BondGained.class,
            listeners -> (player, horse, source, amount, before, after) -> { for (var l : listeners) l.onBondGained(player, horse, source, amount, before, after); });
    public static final Event<LanceHit> LANCE_HIT = EventFactory.createArrayBacked(LanceHit.class,
            listeners -> (player, target, damage, speed) -> { for (var l : listeners) l.onLanceHit(player, target, damage, speed); });
    public static final Event<RidingBonus> RIDING_BONUS = EventFactory.createArrayBacked(RidingBonus.class,
            listeners -> (player, aspect) -> {
                double sum = 0;
                for (var l : listeners) sum += l.bonus(player, aspect);
                return sum;
            });

    /** The summed bonus for a player, never negative; 0 with no listeners or no player. */
    public static double ridingBonus(ServerPlayer p, Aspect a) { return p == null ? 0 : Math.max(0, RIDING_BONUS.invoker().bonus(p, a)); }

    private StablehandEvents() {}
}
