package dev.villagefriends;

import static dev.villagefriends.VillageFriends.*;
import java.util.*;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Pose;
import net.minecraft.world.entity.ai.memory.MemoryModuleType;
import net.minecraft.world.entity.ai.memory.WalkTarget;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.level.block.AbstractBedBlock;
import net.minecraft.world.phys.Vec3;
import net.minecraft.core.BlockPos;
import net.minecraft.core.GlobalPos;
import dev.villagefriends.home.Homes;

/**
 * A resident who would die is knocked out instead: they lie hurt on the ground for a day of play (24 real
 * hours of ticks, counted only while the world runs). Smelling Salts wake them with a fifth of their health,
 * a Revival Tonic with all of it; a Bandage Wrap buys twelve more hours, and the village apothecary will
 * come and dress their wounds once, then help them to their own bed (or a cot at the apothecary's) to wait.
 * If the clock runs out they die for good. The void and /kill still kill
 * outright. Recruited companions keep their own, gentler downing (see {@link CompanionController}) but lie
 * on the ground the same way.
 */
public final class Knockouts {
    /** Knocked-out residents in loaded chunks, for apothecaries looking for patients. */
    private static final Set<Villager> patients = new HashSet<>();
    /** Which apothecary is on the way to which patient. */
    private static final Map<UUID, UUID> visits = new HashMap<>();

    public static void clear() { patients.clear(); visits.clear(); }
    public static void unload(Villager v) { patients.remove(v); visits.remove(v.getUUID()); visits.values().remove(v.getUUID()); }

    public static KnockoutState state(Villager v) { return target(v).getAttached(KNOCKOUT); }
    public static boolean knockedOut(Villager v) { return target(v).hasAttached(KNOCKOUT); }
    /** Lying hurt on the ground: knocked out or a downed companion. Works on both sides. */
    public static boolean injured(Entity e) { return e instanceof Villager && Boolean.TRUE.equals(target(e).getAttached(INJURED)); }

    // -- lying down and getting up -----------------------------------------------------------------

    public static void lieDown(Villager v) {
        if (!injured(v)) target(v).setAttached(INJURED, true);
        if (v.isPassenger()) v.stopRiding();
        // Someone helped into their own bed stays in it.
        if (v.isSleeping() && !inBed(v)) v.stopSleeping();
        if (v.getPose() != Pose.SLEEPING) v.setPose(Pose.SLEEPING);
        // The injured hitbox depends on the attachment as well as the pose.
        v.refreshDimensions();
    }
    public static void getUp(Villager v) {
        target(v).removeAttached(INJURED);
        v.setPose(Pose.STANDING);
        v.refreshDimensions();
    }

    // -- damage ------------------------------------------------------------------------------------

    /** Nothing hurts someone already lying unconscious, except the void and /kill. */
    public static boolean allowDamage(LivingEntity entity, DamageSource source) {
        return !(entity instanceof Villager v) || !knockedOut(v) || source.is(DamageTypeTags.BYPASSES_INVULNERABILITY);
    }
    public static boolean allowDeath(LivingEntity entity, DamageSource source) {
        if (!(entity instanceof Villager v) || !(v.level() instanceof ServerLevel level)) return true;
        if (source.is(DamageTypeTags.BYPASSES_INVULNERABILITY)) return true;
        var by = GuardController.attacker(source) instanceof ServerPlayer p && !p.isCreative() && !p.isSpectator() ? p : null;
        boolean fresh = !knockedOut(v);
        knockOut(v, level, by == null ? "" : by.getUUID().toString());
        if (by != null && fresh) dev.villagefriends.deed.Deeds.knockedOut(by, v);
        return false;
    }
    public static void knockOut(Villager v, ServerLevel level) { knockOut(v, level, ""); }
    /** {@code by}: the UUID of the player who did it, or "". */
    public static void knockOut(Villager v, ServerLevel level, String by) {
        v.setHealth(1); v.clearFire(); v.removeAllEffects(); v.setTradingPlayer(null); v.stopUsingItem();
        v.getNavigation().stop(); v.getBrain().eraseMemory(MemoryModuleType.WALK_TARGET);
        GuardController.unload(v);
        if (!knockedOut(v)) target(v).setAttached(KNOCKOUT, KnockoutState.knockedOut(level.getGameTime(), by));
        lieDown(v);
        patients.add(v);
        level.playSound(null, v.blockPosition(), SoundEvents.VILLAGER_HURT, SoundSource.NEUTRAL, 1F, .8F);
        var line = Component.literal(name(v) + " was knocked out! Revive them with Smelling Salts or a Revival Tonic within a day of play ("
                + KnockoutState.duration(KnockoutState.DAY) + "), or they will die. A Bandage Wrap buys 12 more hours.");
        for (var p : level.players()) if (p.distanceToSqr(v) < 64 * 64) p.sendSystemMessage(line, false);
    }

    // -- while they lie there ----------------------------------------------------------------------

    /** Runs instead of the brain while knocked out. Returns false for conscious residents. */
    public static boolean drive(Villager v, ServerLevel level) {
        var s = state(v);
        if (s == null) return false;
        if (level.getGameTime() >= s.until()) { expire(v, level); return true; }
        patients.add(v);
        if (!injured(v) || v.getPose() != Pose.SLEEPING) lieDown(v);
        var bed = s.bed().orElse(null);
        if (bed != null && !v.isSleeping() && level.getGameTime() % 20 == 0) {
            // Back into bed after a reload; a bed that was broken leaves them where they are.
            var at = level.getBlockState(bed);
            if (at.getBlock() instanceof AbstractBedBlock && !at.getValue(AbstractBedBlock.OCCUPIED)) v.startSleeping(bed);
            else if (at.getBlock() != VillageBlocks.get("apothecary_cot")) target(v).setAttached(KNOCKOUT, s.in(null));
        }
        v.getNavigation().stop(); v.clearFire();
        if (v.getHealth() > 1) v.setHealth(1);
        return true;
    }
    /** "Unconscious · 23h 59m left", for the conversation status line and the Ledger. */
    public static String status(Villager v) {
        var s = state(v);
        return s == null ? null : "Unconscious · " + KnockoutState.duration(s.left(v.level().getGameTime())) + " left";
    }
    private static void expire(Villager v, ServerLevel level) {
        unload(v);
        String name = name(v);
        var line = Component.literal(name + " died of their injuries.");
        for (var p : level.players()) {
            if (p.distanceToSqr(v) < 128 * 128 || target(v).getAttachedOrCreate(FRIENDSHIPS).get(p.getUUID()).points() > 0)
                p.sendSystemMessage(line, false);
        }
        String by = state(v).by();
        // The village blames whoever knocked them out (before they are gone, so their family is still known).
        dev.villagefriends.deed.Deeds.died(v, by);
        target(v).removeAttached(KNOCKOUT);
        v.kill(level);
    }

    // -- treatment ---------------------------------------------------------------------------------

    /** A player right-clicks a knocked-out resident: treat them with a medical supply, or check on them. */
    public static void interact(ServerPlayer p, Villager v) {
        var level = (ServerLevel) v.level(); var s = state(v); long now = level.getGameTime();
        var held = p.getMainHandItem();
        if (!(held.getItem() instanceof MedicalSupplyItem medicine)) {
            p.sendSystemMessage(Component.literal(name(v) + " is unconscious · " + KnockoutState.duration(s.left(now))
                    + " left · Smelling Salts or a Revival Tonic will wake them; a Bandage Wrap buys 12 hours"), true);
            return;
        }
        var treatment = medicine.treatment();
        if (treatment == MedicalSupplyItem.Treatment.BANDAGE_WRAP) {
            if (!s.canBandage(now)) {
                p.sendSystemMessage(Component.literal(name(v) + "'s wounds are already well bandaged (" + KnockoutState.duration(s.left(now)) + " left)."), true);
                return;
            }
            var next = s.bandaged(now, false);
            target(v).setAttached(KNOCKOUT, next);
            if (!p.getAbilities().instabuild) held.shrink(1);
            dev.villagefriends.deed.Deeds.bandaged(p, v);
            level.playSound(null, v.blockPosition(), SoundEvents.WOOL_PLACE, SoundSource.PLAYERS, 1F, 1.1F);
            level.sendParticles(ParticleTypes.HAPPY_VILLAGER, v.getX(), v.getY() + .4, v.getZ(), 6, .4, .1, .4, 0);
            p.sendSystemMessage(Component.literal("You bandage " + name(v) + "'s wounds · " + KnockoutState.duration(next.left(now)) + " left"), true);
            return;
        }
        // Where they were helped to lie, if anywhere: they come to in their own bed or on the apothecary's cot.
        var bed = s.bed().orElse(null);
        boolean cot = bed != null && level.getBlockState(bed).getBlock() == VillageBlocks.get("apothecary_cot");
        if (!p.getAbilities().instabuild) held.shrink(1);
        revive(v, treatment.restoredHealthFraction());
        saveBond(v, p, bond(v, p).trust(10).remember(day(level), "You revived me after I was knocked out."));
        dev.villagefriends.deed.Deeds.revived(p, v);
        p.sendSystemMessage(Component.literal(name(v) + " comes to. " + (treatment == MedicalSupplyItem.Treatment.REVIVAL_TONIC ? "Fully restored." : "Still weak: let them rest.")), true);
        if (bed != null) {
            String said = TalkWorld.say(v, p, cot ? "home.carried.cot" : "home.carried", Map.of());
            if (said != null) p.sendSystemMessage(Component.literal(name(v) + ": \"" + said + "\""), false);
        }
    }
    public static void revive(Villager v, float healthFraction) {
        var level = (ServerLevel) v.level();
        unload(v);
        if (v.isSleeping()) v.stopSleeping();
        target(v).removeAttached(KNOCKOUT);
        getUp(v);
        v.setHealth(Math.max(2, v.getMaxHealth() * healthFraction));
        GuardController.unload(v);
        level.playSound(null, v.blockPosition(), SoundEvents.VILLAGER_YES, SoundSource.NEUTRAL, 1F, 1F);
        level.sendParticles(ParticleTypes.HEART, v.getX(), v.getY() + 1.8, v.getZ(), 3, .3, .2, .3, 0);
        VillageSocieties.emote(v, Emote.SPARKLE, 10);
    }

    /**
     * The village apothecary goes to the nearest knocked-out neighbor nobody has tended and dresses their
     * wounds (twelve more hours, once per patient). Called once a second; returns true while on the way.
     */
    public static boolean tend(Villager apothecary, ServerLevel level) {
        if (apothecary.isBaby() || apothecary.isSleeping() || injured(apothecary) || !profession(apothecary).equals("apothecary")) return false;
        Villager patient = null;
        var assigned = visits.get(apothecary.getUUID());
        for (var p : patients) {
            if (p.isRemoved() || p.level() != level || !knockedOut(p) || state(p).tended() || p.distanceToSqr(apothecary) > 32 * 32) continue;
            var other = visits.entrySet().stream().filter(e -> e.getValue().equals(p.getUUID()) && !e.getKey().equals(apothecary.getUUID())).findAny();
            if (other.isPresent()) continue;
            if (p.getUUID().equals(assigned)) { patient = p; break; }
            if (patient == null || p.distanceToSqr(apothecary) < patient.distanceToSqr(apothecary)) patient = p;
        }
        if (patient == null) { visits.remove(apothecary.getUUID()); return false; }
        visits.put(apothecary.getUUID(), patient.getUUID());
        if (apothecary.distanceToSqr(patient) > 2.5 * 2.5) {
            apothecary.getBrain().setMemory(MemoryModuleType.WALK_TARGET, new WalkTarget(patient.blockPosition(), .6F, 1));
            return true;
        }
        long now = level.getGameTime();
        var next = state(patient).bandaged(now, true);
        target(patient).setAttached(KNOCKOUT, next);
        visits.remove(apothecary.getUUID());
        apothecary.getLookControl().setLookAt(patient, 30, 30);
        level.playSound(null, patient.blockPosition(), SoundEvents.WOOL_PLACE, SoundSource.NEUTRAL, 1F, 1.1F);
        level.sendParticles(ParticleTypes.HAPPY_VILLAGER, patient.getX(), patient.getY() + .4, patient.getZ(), 6, .4, .1, .4, 0);
        var line = Component.literal(name(apothecary) + " dressed " + name(patient) + "'s wounds · " + KnockoutState.duration(next.left(now)) + " left to revive them");
        for (var p : level.players()) if (p.distanceToSqr(patient) < 48 * 48) p.sendSystemMessage(line, true);
        helpHome(apothecary, patient, level);
        return false;
    }
    private static boolean inBed(Villager v) {
        var s = state(v);
        return s != null && s.bed().isPresent() && v.getSleepingPos().map(p -> p.equals(s.bed().get())).orElse(false);
    }
    /**
     * Once their wounds are dressed, a patient is helped to their own bed when it is close by ({@link Homes#CARRY_REACH}
     * blocks), loaded and free; otherwise onto the nearest free apothecary cot; otherwise they stay where they fell.
     */
    static void helpHome(Villager apothecary, Villager patient, ServerLevel level) {
        var s = state(patient);
        if (s == null || s.bed().isPresent()) return;
        var from = patient.position();
        var bed = Homes.bedOf(patient).map(dev.villagefriends.home.House.Bed::head).orElse(null);
        String where = null;
        if (bed != null && level.isLoaded(bed) && bed.closerToCenterThan(from, Homes.CARRY_REACH)) {
            var at = level.getBlockState(bed);
            if (at.getBlock() instanceof AbstractBedBlock && !at.getValue(AbstractBedBlock.OCCUPIED)) {
                target(patient).setAttached(KNOCKOUT, s.in(bed));
                patient.startSleeping(bed);
                if (patient.isSleeping()) where = "their own bed";
                else target(patient).setAttached(KNOCKOUT, s);
            }
        }
        if (where == null) {
            var cot = cot(apothecary, patient, level);
            if (cot != null) {
                patient.teleportTo(cot.getX() + .5, cot.getY() + 9 / 16.0, cot.getZ() + .5);
                target(patient).setAttached(KNOCKOUT, s.in(cot));
                lieDown(patient);
                where = "a cot at the apothecary's";
            }
        }
        if (where == null) return;
        level.sendParticles(ParticleTypes.POOF, from.x, from.y + .4, from.z, 10, .4, .2, .4, .02);
        level.sendParticles(ParticleTypes.POOF, patient.getX(), patient.getY() + .4, patient.getZ(), 10, .4, .2, .4, .02);
        var line = Component.literal(name(apothecary) + " helped " + name(patient) + " to " + where + ".");
        for (var p : level.players()) if (p.distanceToSqr(patient) < 48 * 48 || p.position().distanceToSqr(from) < 48 * 48) p.sendSystemMessage(line, false);
    }
    /** The nearest free apothecary cot around the apothecary's workstation (or the apothecary), within reach of the patient. */
    private static BlockPos cot(Villager apothecary, Villager patient, ServerLevel level) {
        var anchor = apothecary.getBrain().getMemory(MemoryModuleType.JOB_SITE).filter(g -> g.dimension() == level.dimension())
                .map(GlobalPos::pos).orElse(apothecary.blockPosition());
        if (!anchor.closerToCenterThan(patient.position(), Homes.CARRY_REACH)) return null;
        var block = VillageBlocks.get("apothecary_cot");
        BlockPos best = null; double bestDistance = Double.MAX_VALUE;
        for (var p : BlockPos.betweenClosed(anchor.offset(-8, -3, -8), anchor.offset(8, 3, 8))) {
            if (!level.isLoaded(p) || level.getBlockState(p).getBlock() != block) continue;
            var top = Vec3.atBottomCenterOf(p).add(0, 9 / 16.0, 0);
            boolean taken = false;
            for (var other : patients) if (other != patient && other.position().distanceToSqr(top) < 1) taken = true;
            double d = p.distSqr(anchor);
            if (!taken && d < bestDistance) { best = p.immutable(); bestDistance = d; }
        }
        return best;
    }
    private Knockouts() {}
}
