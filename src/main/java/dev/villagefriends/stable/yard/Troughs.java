package dev.villagefriends.stable.yard;

import dev.villagefriends.stable.api.Stables;
import dev.villagefriends.stable.data.HayTroughBlock;
import dev.villagefriends.stable.data.StableBlocks;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.function.Predicate;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.level.block.state.BlockState;

/**
 * Hay Troughs and the horses that eat from them. There is no index of troughs to keep or clear: every yard tick
 * ({@link YardFeature#YARD_TICKS}) each stalled horse that is hurt or still a foal looks for the nearest trough with
 * hay within {@link #REACH} blocks of its stall (a 13 x 3 x 13 box), walks over and eats: two health back, or a minute
 * off growing up, and one time in three a serving of hay is gone. Searches never load a chunk.
 */
public final class Troughs {
    /** How far from a stall its horse will go for hay, across and up or down. */
    public static final int REACH = 6, REACH_Y = 1;

    /** Blocks of a kind around a spot, nearest first. Positions in chunks that aren't loaded are skipped, never loaded. */
    public static List<BlockPos> find(ServerLevel level, BlockPos center, int reach, int reachY, Predicate<BlockState> test) {
        var found = new ArrayList<BlockPos>();
        var cursor = new BlockPos.MutableBlockPos();
        for (int x = center.getX() - reach; x <= center.getX() + reach; x++)
            for (int z = center.getZ() - reach; z <= center.getZ() + reach; z++) {
                if (level.getChunkSource().getChunkNow(x >> 4, z >> 4) == null) continue;
                for (int y = center.getY() - reachY; y <= center.getY() + reachY; y++)
                    if (test.test(level.getBlockState(cursor.set(x, y, z)))) found.add(cursor.immutable());
            }
        found.sort(Comparator.comparingDouble(p -> p.distSqr(center)));
        return found;
    }
    /** Hay Troughs around a spot, nearest first. */
    public static List<BlockPos> near(ServerLevel level, BlockPos center, int reach, int reachY) {
        return find(level, center, reach, reachY, s -> s.is(StableBlocks.HAY_TROUGH));
    }

    /** Hurt or young stalled horses eat from the nearest trough with hay (the yard tick). */
    static void feed(ServerLevel level, List<AbstractHorse> stalled) {
        for (var horse : stalled) {
            boolean hurt = horse.getHealth() < horse.getMaxHealth(), baby = horse.isBaby();
            if (!hurt && !baby || !horse.isAlive()) continue;
            var home = Stables.stallOf(horse).orElse(null);
            if (home == null) continue;
            for (var trough : near(level, home.stall(), REACH, REACH_Y)) {
                var state = level.getBlockState(trough);
                int hay = state.getValue(HayTroughBlock.HAY);
                if (!StallRules.eats(hay, hurt, baby)) continue;
                if (hurt) horse.heal(2F);
                if (baby) horse.ageUp(60);
                if (StallRules.usesHay(level.getRandom().nextInt(3))) level.setBlock(trough, state.setValue(HayTroughBlock.HAY, hay - 1), 3);
                if (horse.getPassengers().isEmpty() && !horse.isLeashed())
                    horse.getNavigation().moveTo(trough.getX() + .5, trough.getY(), trough.getZ() + .5, 1.0);
                level.playSound(null, trough, SoundEvents.HORSE_EAT, SoundSource.NEUTRAL, .8F, baby ? 1.3F : 1F);
                level.sendParticles(ParticleTypes.HAPPY_VILLAGER, trough.getX() + .5, trough.getY() + .7, trough.getZ() + .5, 3, .3, .1, .3, 0);
                break;
            }
        }
    }

    private Troughs() {}
}
