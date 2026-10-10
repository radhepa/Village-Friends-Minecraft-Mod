package dev.villagefriends.stable.yard;

import static dev.villagefriends.VillageFriends.profession;

import dev.villagefriends.ResidentRoutines;
import dev.villagefriends.VillageFriends;
import dev.villagefriends.routine.Routine;
import dev.villagefriends.stable.api.Stables;
import dev.villagefriends.stable.data.HayTroughBlock;
import dev.villagefriends.stable.data.StableBlocks;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import net.minecraft.core.BlockPos;
import net.minecraft.core.GlobalPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.ai.memory.MemoryModuleType;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.entity.npc.villager.Villager;

/**
 * The stablehand's working day. Once a second during work hours they pick a chore near their Saddle Rack: top up a
 * Hay Trough that isn't full (each trough once a day, so a horse that eats it down gets more tomorrow), or look in on
 * a stalled horse (a pat, a little health back and hearts, each horse at most every two minutes, the hurt ones
 * first). They walk there, do it, and pick the next; with nothing left to do they go back to the ordinary work
 * routine at the rack. Called from the routine chain in {@code ResidentRoutines.update}.
 * Owned by the stables package; the signature of {@link #update} is frozen.
 */
public final class StableWork {
    /** How far from the rack the stablehand tends troughs (across; and up or down {@link #TROUGH_REACH_Y}) and horses. */
    public static final int TROUGH_REACH = 12, TROUGH_REACH_Y = 3, HORSE_REACH = 24;
    /** How often the troughs around a rack are looked up again. */
    private static final long TROUGH_SCAN_TICKS = 600;
    private static final double CLOSE = 2.5;

    private enum Kind { TROUGH, HORSE }
    private record Chore(Kind kind, BlockPos trough, UUID horse, long since) {}
    private record Scan(BlockPos rack, long at, List<BlockPos> troughs) {}
    /** Stablehand to the chore they're on. */
    private static final Map<UUID, Chore> chores = new HashMap<>();
    /** Stablehand to the troughs around their rack. */
    private static final Map<UUID, Scan> scans = new HashMap<>();
    /** Horse to the game time of its last visit. */
    private static final Map<UUID, Long> visits = new HashMap<>();
    /** Trough to the day it was last topped up. */
    private static final Map<GlobalPos, Long> refills = new HashMap<>();

    public static void clear() { chores.clear(); scans.clear(); visits.clear(); refills.clear(); }
    static void unload(Entity entity) {
        if (entity instanceof Villager) { chores.remove(entity.getUUID()); scans.remove(entity.getUUID()); }
        else if (entity instanceof AbstractHorse) visits.remove(entity.getUUID());
    }

    /** True while this resident is busy with stable work this update (the rest of the routine chain is skipped). */
    public static boolean update(Villager v, ServerLevel level, Routine.Plan plan) {
        if (plan.block() != Routine.Block.WORK || v.isBaby() || v.isSleeping() || !profession(v).equals("stablehand")) { chores.remove(v.getUUID()); return false; }
        var rack = v.getBrain().getMemory(MemoryModuleType.JOB_SITE).filter(g -> g.dimension() == level.dimension()).map(GlobalPos::pos).orElse(null);
        if (rack == null || !rack.closerToCenterThan(v.position(), HORSE_REACH * 2)) { chores.remove(v.getUUID()); return false; }
        long now = level.getGameTime(), today = VillageFriends.day(level);
        var chore = chores.get(v.getUUID());
        if (chore != null && now - chore.since() > StallRules.CHORE_TICKS) { setAside(level, chore, now, today); chore = null; }
        if (chore == null || !current(level, chore, rack, now, today)) chore = next(v, level, rack, now, today);
        if (chore == null) { chores.remove(v.getUUID()); return false; }
        chores.put(v.getUUID(), chore);
        var horse = chore.kind() == Kind.HORSE ? level.getEntity(chore.horse()) instanceof AbstractHorse h ? h : null : null;
        var spot = horse != null ? horse.blockPosition() : chore.trough();
        if (spot == null) { chores.remove(v.getUUID()); return false; }
        if (!spot.closerToCenterThan(v.position(), CLOSE)) { ResidentRoutines.walk(v, spot, .5F, 1); return true; }
        if (horse != null) groom(v, level, horse, now); else topUp(v, level, chore.trough(), today);
        chores.remove(v.getUUID());
        return true;
    }

    /** Is the chore still worth doing? */
    private static boolean current(ServerLevel level, Chore chore, BlockPos rack, long now, long today) {
        if (chore.kind() == Kind.TROUGH) {
            var state = level.getBlockState(chore.trough());
            return state.is(StableBlocks.HAY_TROUGH) && StallRules.refill(state.getValue(HayTroughBlock.HAY), refills.getOrDefault(key(level, chore.trough()), -1L), today);
        }
        return level.getEntity(chore.horse()) instanceof AbstractHorse h && h.isAlive() && !h.isVehicle() && Stables.stallOf(h).filter(s -> s.stall().closerThan(rack, HORSE_REACH)).isPresent()
                && StallRules.visitDue(visits.getOrDefault(h.getUUID(), -1L), now);
    }
    /**
     * A chore that took too long (a trough they can't reach, a horse that keeps wandering off or was ridden away)
     * waits its turn as if it were done: the trough until tomorrow, the horse until its next visit is due.
     * Otherwise the same chore would be picked again at once and the stablehand would chase it all day.
     */
    private static void setAside(ServerLevel level, Chore chore, long now, long today) {
        if (chore.kind() == Kind.TROUGH) refills.put(key(level, chore.trough()), today); else visits.put(chore.horse(), now);
    }

    /** A trough that needs topping up today, else the horse most in need of a visit, else nothing. */
    private static Chore next(Villager v, ServerLevel level, BlockPos rack, long now, long today) {
        for (var trough : troughs(v, level, rack, now)) {
            var state = level.getBlockState(trough);
            if (state.is(StableBlocks.HAY_TROUGH) && StallRules.refill(state.getValue(HayTroughBlock.HAY), refills.getOrDefault(key(level, trough), -1L), today))
                return new Chore(Kind.TROUGH, trough, null, now);
        }
        return Stables.stalledHorses(level, rack, HORSE_REACH).stream()
                .filter(h -> StallRules.visitDue(visits.getOrDefault(h.getUUID(), -1L), now) && !h.isVehicle())
                .min(Comparator.comparing((AbstractHorse h) -> h.getHealth() >= h.getMaxHealth()).thenComparingDouble(h -> h.distanceToSqr(v)))
                .map(h -> new Chore(Kind.HORSE, null, h.getUUID(), now)).orElse(null);
    }
    private static List<BlockPos> troughs(Villager v, ServerLevel level, BlockPos rack, long now) {
        var scan = scans.get(v.getUUID());
        if (scan == null || !scan.rack().equals(rack) || now - scan.at() > TROUGH_SCAN_TICKS) {
            scan = new Scan(rack, now, Troughs.near(level, rack, TROUGH_REACH, TROUGH_REACH_Y));
            scans.put(v.getUUID(), scan);
        }
        return scan.troughs();
    }
    private static GlobalPos key(ServerLevel level, BlockPos pos) { return GlobalPos.of(level.dimension(), pos); }

    private static void topUp(Villager v, ServerLevel level, BlockPos trough, long today) {
        var state = level.getBlockState(trough);
        if (!state.is(StableBlocks.HAY_TROUGH)) return;
        level.setBlock(trough, state.setValue(HayTroughBlock.HAY, StallRules.fill(state.getValue(HayTroughBlock.HAY), StallRules.MAX_HAY)), 3);
        refills.put(key(level, trough), today);
        v.getLookControl().setLookAt(trough.getX() + .5, trough.getY() + .5, trough.getZ() + .5);
        v.swingForAttack(InteractionHand.MAIN_HAND);
        level.playSound(null, trough, SoundEvents.GRASS_PLACE, SoundSource.NEUTRAL, 1F, .9F);
    }
    private static void groom(Villager v, ServerLevel level, AbstractHorse horse, long now) {
        visits.put(horse.getUUID(), now);
        v.getLookControl().setLookAt(horse, 30, 30);
        v.swingForAttack(InteractionHand.MAIN_HAND);
        horse.heal(1F);
        level.playSound(null, horse.blockPosition(), SoundEvents.HORSE_BREATHE, SoundSource.NEUTRAL, .8F, 1F);
        level.sendParticles(ParticleTypes.HEART, horse.getX(), horse.getY() + horse.getBbHeight() + .2, horse.getZ(), 2, .3, .1, .3, 0);
    }

    private StableWork() {}
}
