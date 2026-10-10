package dev.villagefriends.stable.yard;

import static dev.villagefriends.VillageFriends.target;

import dev.villagefriends.deed.Deeds;
import dev.villagefriends.stable.api.Horses;
import dev.villagefriends.stable.api.Stables;
import dev.villagefriends.stable.data.StableBlocks;
import dev.villagefriends.stable.data.StableData;
import dev.villagefriends.stable.data.StableTable;
import dev.villagefriends.stable.data.StableTags;
import dev.villagefriends.stable.data.StallHome;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;
import java.util.UUID;
import net.minecraft.core.BlockPos;
import net.minecraft.core.GlobalPos;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.entity.npc.villager.VillagerType;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.entity.EntityTypeTest;

/**
 * The village's own horses. A stable template's horses carry the entity tag {@link StableTags#STABLE_HORSE} and no
 * stall; each settles into a free Horse Stall near it, takes a breed its village keeps, and becomes the village's
 * horse ({@code keeper = "village"}).
 *
 * <p>Settling reads blocks, never the point-of-interest index: in a freshly generated chunk the stalls may not be
 * indexed yet when the template's horses load. Loading only queues a horse; it settles on the next server tick,
 * when every horse from the same chunk has loaded, so two horses never claim one stall. A horse that finds no free
 * stall looks again every yard tick and gives up after {@link StallRules#MAX_TRIES} tries: then it keeps a breed
 * for where it stands and stays a tame horse without a stall. The yard tick also lists tagged horses, so one whose
 * queue entry was lost when its chunk unloaded is picked up again; and it feeds stalled horses ({@link Troughs}) and
 * frees a player's horse whose stall block is gone.
 */
public final class StableHorses {
    /** How far from a template horse a stall can be, across and up or down (a 17 x 5 x 17 box). */
    public static final int SETTLE_REACH = 8, SETTLE_REACH_Y = 2;
    /** A queued horse: where it is, how many times it has looked for a stall, and the server tick it looks next. */
    private record Pending(ResourceKey<Level> dimension, int tries, long due) {}
    private static final Map<UUID, Pending> pending = new HashMap<>();

    public static void clear() { pending.clear(); }
    static void unloaded(Entity entity) { pending.remove(entity.getUUID()); }

    /** A stable template's horse that hasn't settled yet. */
    public static boolean unsettled(AbstractHorse horse) { return horse.entityTags().contains(StableTags.STABLE_HORSE) && !target(horse).hasAttached(StableData.STALL); }

    /** ENTITY_LOAD: queue a template horse for the next tick (nothing reads blocks here). */
    static void loaded(Entity entity, ServerLevel level) {
        if (entity instanceof AbstractHorse horse && unsettled(horse))
            pending.put(horse.getUUID(), new Pending(level.dimension(), tries(horse), level.getServer().getTickCount() + 1));
    }
    private static int tries(AbstractHorse horse) { var p = pending.get(horse.getUUID()); return p == null ? 0 : p.tries(); }

    /** END_SERVER_TICK: settles the horses whose turn it is. */
    static void tick(MinecraftServer server) {
        if (pending.isEmpty()) return;
        long now = server.getTickCount();
        Set<GlobalPos> claimed = new HashSet<>();
        for (var entry : List.copyOf(pending.entrySet())) {
            var p = entry.getValue();
            if (p.due() > now) continue;
            var level = server.getLevel(p.dimension());
            var horse = level == null ? null : level.getEntity(entry.getKey()) instanceof AbstractHorse h ? h : null;
            if (horse == null || !horse.isAlive() || !unsettled(horse)) { pending.remove(entry.getKey()); continue; }
            settle(level, horse, p.tries(), claimed, now);
        }
    }

    /** One try: the nearest free stall, a retry later, or giving up. */
    private static void settle(ServerLevel level, AbstractHorse horse, int tries, Set<GlobalPos> claimed, long now) {
        var stall = freeStall(level, horse.blockPosition(), claimed);
        var random = level.getRandom();
        switch (StallRules.settle(stall != null, tries)) {
            case STALL -> {
                claimed.add(GlobalPos.of(level.dimension(), stall));
                String type = StallRules.villageType(VillagerType.byBiome(level.getBiome(stall)).identifier().getPath());
                Horses.assignBreed(horse, StallRules.stableBreed(StableTable.breeds(), type, new Random(random.nextLong())), random);
                horse.setTamed(true);
                var place = Deeds.place(level, stall);
                Stables.stall(horse, stall, place == null ? "" : place.village(), "village");
                horse.removeTag(StableTags.STABLE_HORSE);
                pending.remove(horse.getUUID());
            }
            case RETRY -> pending.put(horse.getUUID(), new Pending(level.dimension(), tries + 1, now + YardFeature.YARD_TICKS));
            case GIVE_UP -> {
                Horses.assignBreed(horse, Horses.pickBreed(level, horse.blockPosition(), random), random);
                horse.removeTag(StableTags.STABLE_HORSE);
                pending.remove(horse.getUUID());
            }
        }
    }

    /** The nearest Horse Stall no loaded horse lives in and no horse took earlier this tick, or null. */
    static BlockPos freeStall(ServerLevel level, BlockPos near, Set<GlobalPos> claimed) {
        for (var stall : Troughs.find(level, near, SETTLE_REACH, SETTLE_REACH_Y, s -> s.is(StableBlocks.HORSE_STALL)))
            if (!claimed.contains(GlobalPos.of(level.dimension(), stall)) && Stalls.residents(level, stall).isEmpty()) return stall;
        return null;
    }

    /**
     * The yard tick for one level: unsettled template horses (re)join the queue, stalled horses that are hurt or
     * young eat, and a player's horse whose stall block was broken loses its stall (the village's horses keep
     * theirs, so the stall can be rebuilt and a horse can't be freed for the taking by breaking it).
     */
    static void yard(ServerLevel level) {
        long now = level.getServer().getTickCount();
        var stalled = new ArrayList<AbstractHorse>();
        String dimension = Stalls.dimension(level);
        for (var horse : level.getEntities(EntityTypeTest.forClass(AbstractHorse.class),
                h -> h.isAlive() && (target(h).hasAttached(StableData.STALL) || h.entityTags().contains(StableTags.STABLE_HORSE)))) {
            if (unsettled(horse)) {
                if (!pending.containsKey(horse.getUUID())) pending.put(horse.getUUID(), new Pending(level.dimension(), 0, now));
                continue;
            }
            StallHome home = target(horse).getAttached(StableData.STALL);
            if (home == null || !home.dimension().equals(dimension)) continue;
            var stall = home.stall();
            if (home.playerKept() && level.getChunkSource().getChunkNow(stall.getX() >> 4, stall.getZ() >> 4) != null
                    && !level.getBlockState(stall).is(StableBlocks.HORSE_STALL)) { Stalls.evict(horse); continue; }
            stalled.add(horse);
        }
        Troughs.feed(level, stalled);
    }

    private StableHorses() {}
}
