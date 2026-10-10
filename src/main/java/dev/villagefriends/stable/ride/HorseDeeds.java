package dev.villagefriends.stable.ride;

import static dev.villagefriends.VillageFriends.target;

import dev.villagefriends.VillageSettlements;
import dev.villagefriends.deed.DeedKind;
import dev.villagefriends.deed.Deeds;
import dev.villagefriends.stable.api.Horses;
import dev.villagefriends.stable.api.Stables;
import dev.villagefriends.stable.data.StableData;
import dev.villagefriends.stable.data.StableTable;
import dev.villagefriends.stable.data.StallHome;
import dev.villagefriends.stable.ride.TheftRule.Seen;
import dev.villagefriends.stable.ride.TheftRule.Verdict;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.Leashable;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.entity.EntityTypeTest;
import net.minecraft.world.phys.Vec3;
import org.jspecify.annotations.Nullable;

/**
 * Stable horses that belong to a resident or the village, and the players around them ({@link TheftRule} decides):
 * riding or leading one far from its stall is Stole a Horse, bringing a lost or stolen one home is Returned a
 * Horse, and a loose one that wandered (or that a knight left after the watch) drifts back beside its stall when
 * nobody is near enough to see it move. Who took a horse out is saved on it ({@link StallHome#takenBy}), so neither
 * a restart nor a long wait turns its taker into its finder.
 *
 * <p>Cheap by construction: every 40 ticks it looks only at the horses players ride or lead; every 200 ticks it
 * lists the loaded stalled horses once per level, for what needs a horse with no player around (lost, home,
 * drift). Never every entity every tick.
 */
public final class HorseDeeds {
    static final int PLAYER_EVERY = 40, SWEEP_EVERY = 200;
    /** Last game time each stalled horse had anyone in the saddle or on a lead (first sight counts as attended). */
    private static final Map<UUID, Long> attended = new HashMap<>();
    /** Horses a player rode or led at the last check (the sweep leaves those to the player check). */
    private static Set<UUID> carried = new HashSet<>();

    public static void clear() { attended.clear(); carried = new HashSet<>(); }
    public static void unload(Entity e) { if (e instanceof AbstractHorse) { attended.remove(e.getUUID()); carried.remove(e.getUUID()); } }

    static void tick(MinecraftServer server) {
        int tick = server.getTickCount();
        if (tick % PLAYER_EVERY == 0) players(server);
        if (tick % SWEEP_EVERY == SWEEP_EVERY / 2) sweep(server);
    }

    // -- horses with players --------------------------------------------------------------------------

    private static void players(MinecraftServer server) {
        var now = new HashSet<UUID>();
        for (var p : server.getPlayerList().getPlayers()) {
            if (p.isSpectator()) continue;
            for (var horse : with(p)) {
                var home = Stables.stallOf(horse).orElse(null);
                if (home == null || !home.residentOwned()) continue;
                long time = horse.level().getGameTime();
                now.add(horse.getUUID());
                attended.put(horse.getUUID(), time);
                // Creative players build and test; Deeds ignores them too.
                if (p.isCreative()) continue;
                String me = p.getUUID().toString();
                double distance = distance(horse, home);
                if (TheftRule.takes(distance, home.flagged()) && !me.equals(home.takenBy())) save(horse, home = home.withTakenBy(me));
                var seen = Seen.withPlayer(distance, me.equals(home.stolenBy()) || me.equals(home.takenBy()));
                var verdict = TheftRule.assess(seen, !home.stolenBy().isEmpty(), home.awaySince(), !home.takenBy().isEmpty(), home.returnedAt(), time);
                // Just taken up a lost horse: tell the finder whose it is, so they know where to take it.
                if (verdict == Verdict.NONE && home.awaySince() > 0 && !seen.byTaker() && !carried.contains(horse.getUUID())) found(p, horse, home);
                apply(horse, home, verdict, p, time);
            }
        }
        carried = now;
    }
    /** The horses a player rides or leads. */
    private static List<AbstractHorse> with(ServerPlayer p) {
        var out = new ArrayList<AbstractHorse>();
        if (p.getVehicle() instanceof AbstractHorse h) out.add(h);
        for (var leashed : Leashable.leashableLeashedTo(p)) if (leashed instanceof AbstractHorse h && !out.contains(h)) out.add(h);
        return out;
    }

    // -- horses without players -----------------------------------------------------------------------

    private static void sweep(MinecraftServer server) {
        for (var level : server.getAllLevels()) {
            long time = level.getGameTime();
            var horses = level.getEntities(EntityTypeTest.forClass(AbstractHorse.class), h -> h.isAlive() && Stables.stallOf(h).filter(StallHome::residentOwned).isPresent());
            for (var horse : horses) {
                // The player check has them (a player rides or leads them).
                if (carried.contains(horse.getUUID()) || horse.getFirstPassenger() instanceof Player || horse.getLeashHolder() instanceof Player) continue;
                var home = Stables.stallOf(horse).orElse(null);
                if (home == null) continue;
                boolean loose = !horse.isVehicle() && !horse.isLeashed() && !horse.isPassenger();
                if (!loose) attended.put(horse.getUUID(), time);
                long alone = time - attended.computeIfAbsent(horse.getUUID(), k -> time);
                var seen = Seen.withoutPlayer(distance(horse, home), loose, alone, nearestPlayer(level, horse));
                apply(horse, home, TheftRule.assess(seen, !home.stolenBy().isEmpty(), home.awaySince(), !home.takenBy().isEmpty(), home.returnedAt(), time), null, time);
            }
        }
    }
    private static double nearestPlayer(ServerLevel level, Entity horse) {
        double best = Double.POSITIVE_INFINITY;
        for (var p : level.players()) if (!p.isSpectator()) best = Math.min(best, p.distanceTo(horse));
        return best;
    }

    // -- verdicts -------------------------------------------------------------------------------------

    private static void apply(AbstractHorse horse, StallHome home, Verdict verdict, @Nullable ServerPlayer p, long time) {
        switch (verdict) {
            case NONE -> {}
            case LOST -> save(horse, home.withAwaySince(time));
            case HOME -> save(horse, home.home());
            case DRIFT -> drift(horse, home);
            case STOLEN -> {
                if (p == null) return;
                save(horse, known(horse, home).withStolenBy(p.getUUID().toString()).withTakenBy(p.getUUID().toString()));
                Deeds.record(p, DeedKind.STOLE_HORSE, place(horse, home), "horse:" + horse.getUUID(), name(horse), involved(home), 1, false, horse);
                String village = villageName(horse, home);
                p.sendSystemMessage(Component.literal("This horse belongs to " + (village == null ? "a village stable" : village) + ". Taking it this far from its stable is theft."), false);
            }
            case RETURNED -> {
                if (p == null) { save(horse, home.home()); return; }
                save(horse, known(horse, home).home().withReturnedAt(time));
                Deeds.record(p, DeedKind.RETURNED_HORSE, place(horse, home), "horse:" + horse.getUUID(), name(horse), involved(home), 1, false, horse);
                String village = villageName(horse, home);
                String who = horse.hasCustomName() ? name(horse) : "their " + name(horse).toLowerCase(java.util.Locale.ROOT);
                p.sendSystemMessage(Component.literal((village == null ? "The stable" : village) + " will be glad to have " + who + " back."), false);
            }
        }
    }
    private static void save(AbstractHorse horse, StallHome home) { target(horse).setAttached(StableData.STALL, home); }
    private static void found(ServerPlayer p, AbstractHorse horse, StallHome home) {
        String village = villageName(horse, home);
        p.sendSystemMessage(Component.literal("This horse is a long way from its stable" + (village == null ? "." : " in " + village + ".")
                + " Bring it home and they'll be glad of it."), false);
    }
    /** Fills in the stall's village id the first time it is known (stables from templates may not know it yet). */
    private static StallHome known(AbstractHorse horse, StallHome home) {
        if (!home.village().isEmpty()) return home;
        var place = place(horse, home);
        return place == null ? home : home.withVillage(place.village());
    }

    /** Moves a wandering horse back to a free standing spot beside its stall, never into a wall or water. */
    private static void drift(AbstractHorse horse, StallHome home) {
        if (!(horse.level() instanceof ServerLevel level) || !home.dimension().equals(level.dimension().identifier().toString()) || !level.isLoaded(home.stall())) return;
        var spot = standing(level, horse, home.stall());
        if (spot == null) return;
        horse.teleportTo(spot.x, spot.y, spot.z);
        horse.getNavigation().stop();
    }
    /** The nearest spot within 2 blocks of the stall where the horse fits on solid, dry ground, or null. */
    static @Nullable Vec3 standing(ServerLevel level, AbstractHorse horse, BlockPos stall) {
        var spots = new ArrayList<BlockPos>();
        for (var pos : BlockPos.betweenClosed(stall.offset(-2, -1, -2), stall.offset(2, 1, 2))) spots.add(pos.immutable());
        spots.sort(Comparator.comparingDouble(pos -> pos.distSqr(stall)));
        var size = horse.getDimensions(horse.getPose());
        for (var pos : spots) {
            // A spot across an unloaded chunk border is skipped: reading it would load the chunk.
            if (!level.isLoaded(pos) || !level.isLoaded(pos.below())) continue;
            if (!level.getFluidState(pos).isEmpty() || level.getBlockState(pos.below()).getCollisionShape(level, pos.below()).isEmpty()) continue;
            double x = pos.getX() + .5, y = pos.getY(), z = pos.getZ() + .5;
            if (level.noCollision(horse, size.makeBoundingBox(x, y, z))) return new Vec3(x, y, z);
        }
        return null;
    }

    // -- the horse, its stall and its village ---------------------------------------------------------

    /** Blocks from the horse to its stall; infinite in another dimension. */
    static double distance(AbstractHorse horse, StallHome home) {
        if (!horse.level().dimension().identifier().toString().equals(home.dimension())) return Double.POSITIVE_INFINITY;
        return Math.sqrt(horse.distanceToSqr(Vec3.atBottomCenterOf(home.stall())));
    }
    private static @Nullable ServerLevel stallLevel(AbstractHorse horse, StallHome home) {
        if (!(horse.level() instanceof ServerLevel level)) return null;
        var id = Identifier.tryParse(home.dimension());
        return id == null ? null : level.getServer().getLevel(ResourceKey.create(Registries.DIMENSION, id));
    }
    private static Deeds.@Nullable Place place(AbstractHorse horse, StallHome home) {
        var level = stallLevel(horse, home);
        return level == null ? null : Deeds.place(level, home.stall());
    }
    private static @Nullable String villageName(AbstractHorse horse, StallHome home) {
        var level = stallLevel(horse, home);
        var record = level == null ? null : VillageSettlements.book(level).at(home.stall());
        return record == null ? null : record.name();
    }
    /** The resident who keeps the horse (they and their family hear of it at once); nobody for a communal horse. */
    private static List<String> involved(StallHome home) {
        return home.keeper().isEmpty() || home.keeper().equals("village") || home.playerKept() ? List.of() : List.of(home.keeper());
    }
    /** The horse's name, else its breed ("Destrier"), else its kind ("Donkey"). */
    public static String name(AbstractHorse horse) {
        if (horse.hasCustomName()) return horse.getCustomName().getString();
        return Horses.breed(horse).flatMap(StableTable::breed)
                .map(b -> b.raw() != null && b.raw().has("name") ? b.raw().get("name").getAsString() : b.id())
                .orElseGet(() -> horse.getType().getDescription().getString());
    }

    private HorseDeeds() {}
}
