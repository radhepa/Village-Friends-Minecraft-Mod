package dev.villagefriends.stable.bond;

import dev.villagefriends.stable.data.StableItems;
import java.util.Locale;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;

/**
 * The Grooming Brush: use it on a horse, donkey or mule. It runs before the horse's own interaction, so an untamed
 * horse is brushed instead of being mounted and bucking. Every stroke heals a little; an untamed horse grows
 * calmer (temper, which helps taming); your own horse's bond grows (three grooms a day count) and the action bar
 * shows its breed, bond and stats. Shift-use on a tamed horse still opens its inventory.
 */
public final class Grooming {
    public static InteractionResult use(Player player, Level level, InteractionHand hand, Entity entity) {
        if (hand != InteractionHand.MAIN_HAND || player.isSpectator() || !(entity instanceof AbstractHorse horse) || !Bonds.bondable(horse)) return InteractionResult.PASS;
        if (!player.getItemInHand(hand).is(StableItems.GROOMING_BRUSH) || horse.isTamed() && player.isSecondaryUseActive()) return InteractionResult.PASS;
        if (player instanceof ServerPlayer sp) groom(sp, horse, hand);
        return InteractionResult.SUCCESS;
    }

    /** One stroke of the brush in {@code hand} (the game test calls this too). Returns the bond points it added. */
    public static int groom(ServerPlayer player, AbstractHorse horse, InteractionHand hand) {
        var level = (ServerLevel) horse.level();
        level.playSound(null, horse.getX(), horse.getY() + 1, horse.getZ(), SoundEvents.BRUSH_GENERIC, SoundSource.PLAYERS, 1, .9F + level.getRandom().nextFloat() * .2F);
        level.sendParticles(ParticleTypes.HAPPY_VILLAGER, horse.getX(), horse.getY() + horse.getBbHeight() * .7, horse.getZ(), 6, horse.getBbWidth() * .5, .3, horse.getBbWidth() * .5, 0);
        player.getItemInHand(hand).hurtAndBreak(1, player, hand);
        horse.heal(1);
        String kind = Bonds.kind(horse), name = Bonds.customName(horse);
        if (!horse.isTamed()) {
            horse.modifyTemper(8);
            player.sendSystemMessage(Component.literal("The " + kind.toLowerCase(Locale.ROOT) + " calms a little."), true);
            return 0;
        }
        if (!Bonds.owns(player, horse)) {
            player.sendSystemMessage(Component.literal((name != null ? name : "This " + kind.toLowerCase(Locale.ROOT)) + " belongs to someone else."), true);
            return 0;
        }
        int was = BondMath.tierBefore(Bonds.bond(horse), player.getStringUUID());
        int gained = Bonds.gain(horse, player, BondMath.Source.GROOM, 0, null);
        int points = Bonds.bond(horse).points();
        // A new tier has its own line on the action bar (from Bonds.gain); otherwise show where the bond stands.
        if (BondMath.tier(points) == was) {
            String line = BondMath.describe(name, kind, points, horse.getAttributeValue(Attributes.MOVEMENT_SPEED),
                    horse.getAttributeValue(Attributes.JUMP_STRENGTH), horse.getMaxHealth());
            // Nothing gained means today's grooms are used up, unless the bond is already full.
            player.sendSystemMessage(Component.literal(gained > 0 || points >= BondMath.MAX ? line : line + " Groomed enough for today."), true);
        }
        return gained;
    }

    private Grooming() {}
}
