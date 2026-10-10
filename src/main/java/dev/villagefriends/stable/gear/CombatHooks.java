package dev.villagefriends.stable.gear;

import dev.villagefriends.stable.api.Horses;
import dev.villagefriends.stable.api.StablehandEvents;
import dev.villagefriends.stable.api.StablehandEvents.Aspect;
import dev.villagefriends.stable.data.StableItems;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.projectile.Projectile;
import org.jspecify.annotations.Nullable;

/**
 * Mounted combat, called by the foundation's {@code StabAttackMixin} and {@code ProjectileSteadyMixin}. Owned by
 * the gear package; the signatures are frozen.
 *
 * <p>The couched lance: a kinetic charge is an item use, so a stab counts as couched only while the attacker is
 * using the lance; the left-click jab also stabs but is not a use and stays vanilla. Only a player on a horse gets
 * the bond bonus (mobs riding with a lance keep vanilla's numbers). The bond counts only for the horse's own bond
 * partner: a borrowed or stolen horse fights for nobody.
 */
public final class CombatHooks {
    /**
     * The damage of a stab ({@code stabAttack}, used by spears and the lance), at its start. Called for players
     * ({@code Player} has its own {@code stabAttack}) and for every other living entity.
     */
    public static float stab(LivingEntity attacker, float damage) {
        if (!(attacker instanceof ServerPlayer player) || !(player.getVehicle() instanceof AbstractHorse horse) || !couching(player)) return damage;
        return LanceMath.mounted(damage, tier(player, horse), StablehandEvents.ridingBonus(player, Aspect.LANCE_DAMAGE));
    }

    /** After a stab: {@code hit} is what {@code stabAttack} returned. */
    public static void stabbed(LivingEntity attacker, EquipmentSlot slot, Entity target, float damage, boolean hit) {
        if (!hit || !(attacker instanceof ServerPlayer player) || !(player.getVehicle() instanceof AbstractHorse horse) || !couching(player)) return;
        if (!(target instanceof LivingEntity victim)) return;
        // A stab can also only knock back or unseat; LANCE_HIT is for hits that hurt, which leave this tick's damage source.
        var source = victim.getLastDamageSource(0);
        if (source == null || source.getEntity() != player) return;
        double speed = horse.getKnownMovement().horizontalDistance() * 20;
        StablehandEvents.LANCE_HIT.invoker().onLanceHit(player, victim, damage, speed);
    }

    /** The inaccuracy a projectile is shot with ({@code Projectile.shoot}, reached by bows and crossbows); its owner is the shooter. */
    public static float aim(Projectile projectile, float inaccuracy) {
        var shooter = rider(projectile.getOwner());
        if (shooter == null || !(shooter.getVehicle() instanceof AbstractHorse horse)) return inaccuracy;
        return ArcheryMath.uncertainty(inaccuracy, tier(shooter, horse), bonus(shooter, Aspect.MOUNTED_AIM));
    }

    /** End of {@code Projectile.shootFromRotation}, which has just added the shooter's own movement to the projectile's. */
    public static void shot(Projectile projectile, Entity shooter) {
        var rider = rider(shooter);
        if (rider == null || !(rider.getVehicle() instanceof AbstractHorse horse)) return;
        var known = rider.getKnownMovement();
        double damp = ArcheryMath.damping(tier(rider, horse), bonus(rider, Aspect.MOUNTED_AIM));
        projectile.setDeltaMovement(projectile.getDeltaMovement().subtract(known.x * damp, 0, known.z * damp));
    }

    /** Whether someone is holding a couched lance (a kinetic charge is an item use). */
    public static boolean couching(LivingEntity e) {
        return StableItems.JOUSTING_LANCE != null && e.isUsingItem() && e.getUseItem().is(StableItems.JOUSTING_LANCE);
    }

    /** The bond tier a rider fights with: the horse's tier for its bond partner, 0 for anyone else (and for residents). */
    public static int tier(LivingEntity rider, AbstractHorse horse) {
        if (!(rider instanceof Player)) return 0;
        return Horses.bondPartner(horse).filter(rider.getUUID()::equals).isPresent() ? Horses.bondTier(horse) : 0;
    }

    /** Players and residents shoot steadier from horseback; anything else that rides keeps vanilla's aim. */
    private static @Nullable LivingEntity rider(@Nullable Entity shooter) {
        return shooter instanceof Player || shooter instanceof Villager ? (LivingEntity) shooter : null;
    }
    private static double bonus(LivingEntity rider, Aspect aspect) { return rider instanceof ServerPlayer p ? StablehandEvents.ridingBonus(p, aspect) : 0; }

    private CombatHooks() {}
}
