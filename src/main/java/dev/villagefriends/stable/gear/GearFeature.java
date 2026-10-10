package dev.villagefriends.stable.gear;

import dev.villagefriends.stable.api.StablehandEvents;
import dev.villagefriends.stable.data.StableItems;
import java.util.Locale;
import net.minecraft.core.particles.ItemParticleOption;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;

/**
 * Tack, barding, pack saddles, the lance and mounted archery (the gear package): registers that package's
 * listeners. Called once from {@code Stablehand.register()}.
 *
 * <p>Most of the gear needs no listener at all: barding is vanilla horse armor, tack is any SADDLE-slot item, the pack
 * resizes through {@link PackHooks} and the lance is vanilla's kinetic spear with {@link CombatHooks} on top. What is
 * left is the rider's feedback for a couched hit, as Village Friends' own listener on {@code LANCE_HIT} (add-ons such
 * as the RPG's Riding skill listen to the same event).
 */
public final class GearFeature {
    /** A hit this hard splinters the lance's tip (only a show of splinters; the lance itself takes vanilla wear). */
    static final float SPLINTER = 15;

    public static void register() {
        StablehandEvents.LANCE_HIT.register((player, target, damage, speed) -> {
            if (!(player.level() instanceof ServerLevel level)) return;
            level.sendParticles(ParticleTypes.CRIT, target.getX(), target.getY(0.6), target.getZ(), 14, .3, .4, .3, .25);
            if (damage >= SPLINTER && StableItems.JOUSTING_LANCE != null) {
                level.sendParticles(new ItemParticleOption(ParticleTypes.ITEM, StableItems.JOUSTING_LANCE), target.getX(), target.getY(0.7), target.getZ(), 12, .25, .25, .25, .15);
                level.playSound(null, target.blockPosition(), SoundEvents.SHIELD_BREAK.value(), SoundSource.PLAYERS, .7f, 1.4f);
            }
            player.sendOverlayMessage(Component.literal(String.format(Locale.ROOT, "Couched lance: %.0f damage at %.1f blocks a second.", damage, speed)));
        });
    }

    private GearFeature() {}
}
