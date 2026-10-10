package dev.villagefriends.fishing;

import net.fabricmc.loader.api.FabricLoader;
import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.projectile.FishingHook;
import net.minecraft.world.phys.Vec3;

/**
 * Optional ties to other mods. With Not-So-Vanilla Mobs installed, a sea bite now and then is no fish at all:
 * a Brineclaw, the giant challenger crab, grabs the line and is hauled up out of the water at you. Looked up by
 * id, so nothing here needs the mod to compile or run.
 */
public final class FishingCompat {
    public static final String NSV = "nsvmobs";
    public static final Identifier BRINECLAW = Identifier.fromNamespaceAndPath(NSV, "brineclaw");
    /** Chance a sea bite is a Brineclaw (three times that on a Legend Lure). */
    public static final double CHALLENGER_CHANCE = .004;

    /** True if a challenger took the bait instead of a fish (it's already been hauled out). */
    static boolean challenger(ServerPlayer p, FishingHook hook, Spot spot, Gear.Bait bait) {
        if (!FabricLoader.getInstance().isModLoaded(NSV) || !spot.waters().contains("ocean")) return false;
        double chance = CHALLENGER_CHANCE * (bait == Gear.Bait.LEGEND_LURE ? 3 : 1);
        if (p.getRandom().nextDouble() >= chance) return false;
        return haul(p, hook);
    }
    /** Hauls a Brineclaw out of the water at the hook toward the angler. */
    public static boolean haul(ServerPlayer p, FishingHook hook) {
        var type = BuiltInRegistries.ENTITY_TYPE.getOptional(BRINECLAW).orElse(null);
        if (type == null || !(hook.level() instanceof ServerLevel level)) return false;
        var entity = type.create(level, EntitySpawnReason.EVENT);
        if (entity == null) return false;
        entity.snapTo(hook.getX(), hook.getY(), hook.getZ(), p.getYRot() + 180, 0);
        if (entity instanceof Mob mob) mob.setTarget(p);
        var toward = p.position().subtract(hook.position());
        entity.setDeltaMovement(new Vec3(toward.x * .12, Math.min(1.2, .5 + toward.length() * .04), toward.z * .12));
        level.addFreshEntity(entity);
        level.sendParticles(ParticleTypes.SPLASH, hook.getX(), hook.getY() + .4, hook.getZ(), 40, .8, .3, .8, .2);
        level.playSound(null, hook.getX(), hook.getY(), hook.getZ(), SoundEvents.GENERIC_SPLASH, SoundSource.HOSTILE, 1.5F, .6F);
        hook.discard();
        p.sendSystemMessage(Component.literal("Something enormous grabs the line... a Brineclaw!").withStyle(ChatFormatting.RED));
        return true;
    }

    private FishingCompat() {}
}
