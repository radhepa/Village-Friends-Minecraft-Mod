package dev.villagefriends.stable.gear;

import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.projectile.Projectile;

/**
 * Mounted combat, called by the foundation's {@code StabAttackMixin} and {@code ProjectileSteadyMixin}. Owned by
 * the gear package; the signatures are frozen.
 */
public final class CombatHooks {
    /**
     * The damage of a stab ({@code stabAttack}, used by spears and the lance), at its start. Called for players
     * ({@code Player} has its own {@code stabAttack}) and for every other living entity.
     */
    public static float stab(LivingEntity attacker, float damage) { return damage; }
    /** After a stab: {@code hit} is what {@code stabAttack} returned. */
    public static void stabbed(LivingEntity attacker, EquipmentSlot slot, Entity target, float damage, boolean hit) {}
    /** The inaccuracy a projectile is shot with ({@code Projectile.shoot}, reached by bows and crossbows); its owner is the shooter. */
    public static float aim(Projectile projectile, float inaccuracy) { return inaccuracy; }
    /** End of {@code Projectile.shootFromRotation}, which has just added the shooter's own movement to the projectile's. */
    public static void shot(Projectile projectile, Entity shooter) {}

    private CombatHooks() {}
}
