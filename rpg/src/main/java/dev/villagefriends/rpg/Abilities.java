package dev.villagefriends.rpg;

import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.particles.ParticleOptions;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectCategory;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.core.Holder;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.monster.Enemy;
import net.minecraft.world.entity.projectile.EvokerFangs;
import net.minecraft.world.entity.projectile.hurtingprojectile.LargeFireball;
import net.minecraft.world.entity.projectile.hurtingprojectile.SmallFireball;
import net.minecraft.world.entity.projectile.hurtingprojectile.WitherSkull;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;

import java.util.ArrayList;

/**
 * Legend abilities: one active power per monster family, used with the ability key. Each costs
 * hunger and has its own cooldown (plus a 1 second shared one), and they borrow vanilla mechanics
 * (fireballs, evoker fangs, potion effects, a pearl-style teleport) so they feel like Minecraft.
 * Offensive abilities only touch monsters, never villagers or players.
 */
public final class Abilities {
    private Abilities() {}

    /** Uses a family's Legend ability; returns quietly with a reason if it can't. */
    public static void use(ServerPlayer p, String familyId) {
        var f = Bestiary.byId(familyId); var s = Rpg.sheet(p);
        if (f == null || s.tier(f) < 5 || p.isSpectator() || !p.isAlive() || !(p.level() instanceof ServerLevel level)) return;
        var a = f.active(); long now = level.getGameTime();
        long ready = s.mark("cd:" + f.id());
        if (ready > now) { say(p, a.name() + " is ready in " + (ready - now + 19) / 20 + "s."); return; }
        if (s.mark("cd:any") > now) return;
        if (a.count() > 0 && !p.getAbilities().instabuild && p.getFoodData().getFoodLevel() <= 6) { say(p, "You're too hungry to use " + a.name() + "."); return; }
        String fail = run(f.id(), p, level, now);
        if (fail != null) { say(p, fail); return; }
        Rpg.set(p, Rpg.sheet(p).mark("cd:" + f.id(), now + Math.round(a.amount() * 20)).mark("cd:any", now + 20));
        if (a.count() > 0) p.causeFoodExhaustion(4F * a.count());
    }
    private static void say(ServerPlayer p, String text) { p.sendSystemMessage(Component.literal(text).withStyle(ChatFormatting.GRAY), true); }

    /** The effect itself; returns why it failed (and no cooldown is spent), or null. */
    private static String run(String id, ServerPlayer p, ServerLevel level, long now) {
        Vec3 look = p.getLookAngle();
        switch (id) {
            case "zombie" -> { buff(p, MobEffects.REGENERATION, 120, 1); sound(p, SoundEvents.ZOMBIE_AMBIENT, .8F); }
            case "skeleton" -> {
                var near = monsters(p, 32);
                if (near.isEmpty()) return "No monsters nearby.";
                near.forEach(e -> e.addEffect(new MobEffectInstance(MobEffects.GLOWING, 200, 0)));
                sound(p, SoundEvents.SKELETON_AMBIENT, 1.2F);
            }
            case "spider" -> {
                var t = target(p, 20); if (t == null) return "Look at a monster within 20 blocks.";
                t.addEffect(new MobEffectInstance(MobEffects.SLOWNESS, 80, 3));
                line(level, p, t.position().add(0, t.getBbHeight() / 2, 0), ParticleTypes.ITEM_COBWEB); sound(p, SoundEvents.SPIDER_AMBIENT, 1.4F);
            }
            case "creeper" -> {
                for (var e : monsters(p, 4)) {
                    double d = Math.max(1, e.distanceTo(p));
                    e.hurtServer(level, level.damageSources().explosion(p, p), (float) (8 * (1 - (d - 1) / 4)));
                    push(e, e.position().subtract(p.position()), .9, .4);
                }
                p.hurtServer(level, level.damageSources().explosion(p, p), 2);
                level.sendParticles(ParticleTypes.EXPLOSION_EMITTER, p.getX(), p.getY() + 1, p.getZ(), 1, 0, 0, 0, 0);
                level.playSound(null, p.blockPosition(), SoundEvents.GENERIC_EXPLODE.value(), SoundSource.PLAYERS, 1, 1);
            }
            case "vermin" -> { buff(p, MobEffects.HASTE, 400, 1); sound(p, SoundEvents.SILVERFISH_AMBIENT, 1); }
            case "slime" -> {
                p.setDeltaMovement(look.x * .6, 1.25, look.z * .6); p.needsSync = true; safeFall(p, now, 160);
                level.sendParticles(ParticleTypes.ITEM_SLIME, p.getX(), p.getY(), p.getZ(), 20, .4, .1, .4, .1); sound(p, SoundEvents.SLIME_JUMP, 1);
            }
            case "enderman" -> { return blink(p, level); }
            case "blaze" -> {
                var ball = new SmallFireball(level, p, look.scale(.1)); ball.setPos(p.getX() + look.x, p.getEyeY() - .1, p.getZ() + look.z);
                level.addFreshEntity(ball); sound(p, SoundEvents.BLAZE_SHOOT, 1);
            }
            case "witch" -> {
                p.heal(4);
                for (var e : new ArrayList<>(p.getActiveEffects())) if (e.getEffect().value().getCategory() == MobEffectCategory.HARMFUL) p.removeEffect(e.getEffect());
                level.sendParticles(ParticleTypes.WITCH, p.getX(), p.getY() + 1, p.getZ(), 20, .4, .6, .4, .05); sound(p, SoundEvents.WITCH_DRINK, 1);
            }
            case "drowned" -> {
                if (!p.isInWaterOrRain()) return "Riptide only works in water or rain.";
                p.setDeltaMovement(look.scale(2.2)); p.needsSync = true; safeFall(p, now, 80);
                level.playSound(null, p.blockPosition(), SoundEvents.TRIDENT_RIPTIDE_1.value(), SoundSource.PLAYERS, 1, 1);
            }
            case "piglin" -> { buff(p, MobEffects.STRENGTH, 200, 0); sound(p, SoundEvents.PIGLIN_ANGRY, 1); }
            case "illager" -> {
                var flat = new Vec3(look.x, 0, look.z).normalize(); float yaw = (float) Math.atan2(flat.z, flat.x);
                for (int i = 0; i < 8; i++) {
                    double dist = 1.5 + i * 1.25; var at = p.position().add(flat.scale(dist));
                    var floor = floor(level, BlockPos.containing(at));
                    if (floor != null) level.addFreshEntity(new EvokerFangs(level, at.x, floor.getY(), at.z, yaw, i * 2, p));
                }
                sound(p, SoundEvents.EVOKER_CAST_SPELL, 1);
            }
            case "guardian" -> { buff(p, MobEffects.CONDUIT_POWER, 1200, 0); sound(p, SoundEvents.CONDUIT_ACTIVATE, 1); }
            case "wither_skeleton" -> {
                Rpg.set(p, Rpg.sheet(p).mark("until:wither_strike", now + 200));
                level.sendParticles(ParticleTypes.SMOKE, p.getX(), p.getY() + 1, p.getZ(), 15, .3, .5, .3, .02); say(p, "Your next hit within 10s withers.");
            }
            case "ghast" -> {
                var ball = new LargeFireball(level, p, look.scale(.1), 1); ball.setPos(p.getX() + look.x * 1.5, p.getEyeY() - .2, p.getZ() + look.z * 1.5);
                level.addFreshEntity(ball); sound(p, SoundEvents.GHAST_SHOOT, 1);
            }
            case "phantom" -> {
                buff(p, MobEffects.SLOW_FALLING, 300, 0); p.setDeltaMovement(p.getDeltaMovement().add(look.x * .8, .3, look.z * .8)); p.needsSync = true;
                sound(p, SoundEvents.PHANTOM_FLAP, 1);
            }
            case "shulker" -> {
                var t = target(p, 24); if (t == null) return "Look at a monster within 24 blocks.";
                t.addEffect(new MobEffectInstance(MobEffects.LEVITATION, 80, 0));
                line(level, p, t.position().add(0, t.getBbHeight() / 2, 0), ParticleTypes.END_ROD); sound(p, SoundEvents.SHULKER_SHOOT, 1);
            }
            case "breeze" -> {
                for (var e : monsters(p, 5)) push(e, e.position().subtract(p.position()), 1.4, .5);
                p.setDeltaMovement(p.getDeltaMovement().add(0, .7, 0)); p.needsSync = true; safeFall(p, now, 100);
                level.sendParticles(ParticleTypes.GUST, p.getX(), p.getY() + .5, p.getZ(), 4, 1, .3, 1, 0);
                level.playSound(null, p.blockPosition(), SoundEvents.WIND_CHARGE_BURST.value(), SoundSource.PLAYERS, 1, 1);
            }
            case "warden" -> {
                var t = target(p, 15); if (t == null) return "Look at a monster within 15 blocks.";
                t.hurtServer(level, level.damageSources().sonicBoom(p), 10);
                line(level, p, t.position().add(0, t.getBbHeight() / 2, 0), ParticleTypes.SONIC_BOOM); sound(p, SoundEvents.WARDEN_SONIC_BOOM, 1);
            }
            case "wither" -> {
                var skull = new WitherSkull(level, p, look.scale(.1)); skull.setPos(p.getX() + look.x * 1.5, p.getEyeY() - .1, p.getZ() + look.z * 1.5);
                level.addFreshEntity(skull); sound(p, SoundEvents.WITHER_SHOOT, 1);
            }
            case "dragon" -> {
                for (var e : monsters(p, 8)) { e.hurtServer(level, level.damageSources().indirectMagic(p, p), 6); push(e, e.position().subtract(p.position()), 1, .3); }
                level.sendParticles(ParticleTypes.REVERSE_PORTAL, p.getX(), p.getY() + 1, p.getZ(), 80, 3, .5, 3, .02); sound(p, SoundEvents.ENDER_DRAGON_GROWL, .6F);
            }
            case "elder_guardian" -> { buff(p, MobEffects.RESISTANCE, 160, 1); sound(p, SoundEvents.ELDER_GUARDIAN_CURSE, .5F); }
            default -> { return "Nothing happens."; }
        }
        return null;
    }

    /** Ender Blink: a pearl's teleport without the pearl, to the block you look at, up to 24 blocks away. */
    private static String blink(ServerPlayer p, ServerLevel level) {
        Vec3 eye = p.getEyePosition(), end = eye.add(p.getLookAngle().scale(24));
        var hit = level.clip(new ClipContext(eye, end, ClipContext.Block.COLLIDER, ClipContext.Fluid.NONE, p));
        if (hit.getType() == HitResult.Type.MISS) return "Look at a block within 24 blocks.";
        BlockPos at = hit.getBlockPos().relative(hit.getDirection());
        for (int down = 0; down < 4 && hit.getDirection() != Direction.UP && level.getBlockState(at.below()).getCollisionShape(level, at.below()).isEmpty(); down++) at = at.below();
        Vec3 to = new Vec3(at.getX() + .5, at.getY(), at.getZ() + .5);
        if (!level.noCollision(p, p.getBoundingBox().move(to.subtract(p.position())))) return "There's no room to land there.";
        level.sendParticles(ParticleTypes.PORTAL, p.getX(), p.getY() + 1, p.getZ(), 40, .3, .8, .3, .4);
        sound(p, SoundEvents.ENDERMAN_TELEPORT, 1);
        p.teleportTo(to.x, to.y, to.z); p.resetFallDistance();
        level.sendParticles(ParticleTypes.PORTAL, to.x, to.y + 1, to.z, 40, .3, .8, .3, .4);
        sound(p, SoundEvents.ENDERMAN_TELEPORT, 1);
        return null;
    }

    // -- helpers -----------------------------------------------------------------------------------
    private static void buff(ServerPlayer p, Holder<MobEffect> effect, int ticks, int amp) { p.addEffect(new MobEffectInstance(effect, ticks, amp)); }
    private static void sound(ServerPlayer p, SoundEvent sound, float pitch) { p.level().playSound(null, p.blockPosition(), sound, SoundSource.PLAYERS, 1, pitch); }
    private static void safeFall(ServerPlayer p, long now, int ticks) { Rpg.set(p, Rpg.sheet(p).mark("until:no_fall", now + ticks)); }
    private static void push(LivingEntity e, Vec3 away, double strength, double up) {
        var d = new Vec3(away.x, 0, away.z); if (d.lengthSqr() < 1e-4) d = new Vec3(1, 0, 0);
        d = d.normalize().scale(strength); e.push(d.x, up, d.z); e.needsSync = true;
    }
    private static java.util.List<LivingEntity> monsters(ServerPlayer p, double r) {
        return p.level().getEntitiesOfClass(LivingEntity.class, p.getBoundingBox().inflate(r), e -> e instanceof Enemy && e.isAlive() && e.distanceTo(p) <= r);
    }
    /** The monster closest to where the player is looking, in sight and range. */
    private static LivingEntity target(ServerPlayer p, double range) {
        Vec3 eye = p.getEyePosition(), look = p.getLookAngle(); LivingEntity best = null; double bestDot = .97;
        for (var e : p.level().getEntitiesOfClass(LivingEntity.class, p.getBoundingBox().inflate(range), e -> e instanceof Enemy && e.isAlive())) {
            Vec3 to = e.position().add(0, e.getBbHeight() / 2, 0).subtract(eye);
            if (to.length() > range) continue;
            double dot = to.normalize().dot(look);
            if (dot > bestDot && p.hasLineOfSight(e)) { bestDot = dot; best = e; }
        }
        return best;
    }
    private static void line(ServerLevel level, ServerPlayer p, Vec3 to, ParticleOptions particle) {
        Vec3 from = p.getEyePosition(), step = to.subtract(from); int n = (int) Math.max(2, step.length() * 1.5);
        for (int i = 1; i <= n; i++) { var at = from.add(step.scale(i / (double) n)); level.sendParticles(particle, at.x, at.y, at.z, 1, 0, 0, 0, 0); }
    }
    /** Standing spot at or near {@code pos}: air with a sturdy block under it, within 3 blocks up or down. */
    private static BlockPos floor(ServerLevel level, BlockPos pos) {
        for (int dy = 2; dy >= -3; dy--) {
            var at = pos.offset(0, dy, 0);
            if (level.getBlockState(at).getCollisionShape(level, at).isEmpty() && level.getBlockState(at.below()).isFaceSturdy(level, at.below(), Direction.UP)) return at;
        }
        return null;
    }
}
