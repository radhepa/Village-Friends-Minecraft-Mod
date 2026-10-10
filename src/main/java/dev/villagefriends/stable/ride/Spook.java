package dev.villagefriends.stable.ride;

import dev.villagefriends.stable.api.Horses;
import dev.villagefriends.stable.api.Stables;
import dev.villagefriends.stable.bond.BondMath;
import dev.villagefriends.stable.data.StableTable;
import dev.villagefriends.stable.data.StableTags;
import dev.villagefriends.stable.data.StallHome;
import dev.villagefriends.stable.ride.SpookRule.Reaction;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import net.fabricmc.loader.api.FabricLoader;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.ai.goal.AvoidEntityGoal;
import net.minecraft.world.entity.ai.util.DefaultRandomPos;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.entity.animal.equine.Donkey;
import net.minecraft.world.entity.animal.equine.Mule;
import net.minecraft.world.entity.monster.Monster;
import org.jspecify.annotations.Nullable;

/**
 * Horses taking fright at monsters ({@link SpookRule} decides). Not-So-Vanilla Mobs' challenger bosses (the
 * optional {@code villagefriends:challengers} tag, only looked at when {@code nsvmobs} is loaded) frighten every
 * horse; ordinary monsters only a cared-for horse with no bond to steady it yet.
 *
 * <ul>
 * <li>A horse with no rider bolts through {@link SpookGoal}, which every horse, donkey and mule gets when it loads.</li>
 * <li>Every second, a horse a player rides rears (and neighs), or rears and throws the player.</li>
 * <li>A horse under a resident never spooks: vanilla already switches its goals off while a mob rides it.</li>
 * <li>A Devoted horse (or a Loyal one under a Bridle) faces a challenger with a challenge neigh instead.</li>
 * </ul>
 */
public final class Spook {
    private static final boolean NSV = FabricLoader.getInstance().isModLoaded("nsvmobs");
    /** Game time each horse last spooked (for the cooldown). */
    private static final Map<UUID, Long> last = new HashMap<>();

    /** A monster and how the horse reacts to it. */
    record Threat(Monster mob, Reaction reaction) {}

    public static void clear() { last.clear(); }
    public static void unload(Entity e) { if (e instanceof AbstractHorse) last.remove(e.getUUID()); }
    /** Game time the horse last reared, bolted or threw its rider, or -1 if it hasn't (since it loaded). */
    public static long last(AbstractHorse horse) { return last.getOrDefault(horse.getUUID(), -1L); }
    static void mark(AbstractHorse horse, long now) { last.put(horse.getUUID(), now); }

    /** Gives a loading horse, donkey or mule its bolting goal (once). */
    static void loaded(Entity entity) {
        if (!(entity instanceof AbstractHorse horse) || !Mounts.rideable(horse)) return;
        var goals = ((dev.villagefriends.mixin.MobGoalsAccessor) horse).villagefriends$goals();
        if (goals.getAvailableGoals().stream().noneMatch(g -> g.getGoal() instanceof SpookGoal)) goals.addGoal(1, new SpookGoal(horse));
    }

    /** Once a second: horses players ride, near a monster that frightens them. */
    static void tick(MinecraftServer server) {
        if (server.getTickCount() % 20 != 0) return;
        for (var p : server.getPlayerList().getPlayers()) {
            if (!(p.getVehicle() instanceof AbstractHorse horse) || !Mounts.rideable(horse) || !(horse.level() instanceof ServerLevel level)) continue;
            long now = level.getGameTime();
            if (!SpookRule.ready(last(horse), now)) continue;
            var threat = threat(horse, true);
            if (threat == null) { if (NSV) challenge(horse, p, now); continue; }
            String mob = threat.mob().getName().getString();
            switch (threat.reaction()) {
                case REAR -> {
                    horse.makeMad(); mark(horse, now);
                    p.sendSystemMessage(Component.literal("Your horse shies at the " + mob + "."), true);
                }
                case THROW -> {
                    horse.makeMad(); horse.ejectPassengers(); mark(horse, now);
                    p.sendSystemMessage(Component.literal("Your horse panics at the sight of the " + mob + "!"), true);
                }
                default -> {}
            }
        }
    }

    /** A steady horse under a player meets a challenger with a challenge neigh instead of fleeing (at most every 10 s). */
    private static void challenge(AbstractHorse horse, ServerPlayer p, long now) {
        int calm = calm(horse);
        if (calm < SpookRule.STEADY) return;
        double reach = SpookRule.CHALLENGER_REACH;
        for (var mob : horse.level().getEntitiesOfClass(Monster.class, horse.getBoundingBox().inflate(reach, 4, reach), m -> m.isAlive() && m.typeHolder().is(StableTags.CHALLENGERS))) {
            if (!SpookRule.standsGround(calm, true, horse.distanceTo(mob))) continue;
            horse.playSound(horse instanceof Donkey ? SoundEvents.DONKEY_ANGRY : horse instanceof Mule ? SoundEvents.MULE_ANGRY : SoundEvents.HORSE_ANGRY, 1.5F, .9F);
            mark(horse, now);
            p.sendSystemMessage(Component.literal("Your horse stands its ground against the " + mob.getName().getString() + "."), true);
            return;
        }
    }

    /**
     * The monster that frightens this horse most right now, or null. Cheap when nothing can: without NSV, only a
     * cared-for horse at calm 0 is scanned at all, and then only 4 blocks around it.
     */
    static @Nullable Threat threat(AbstractHorse horse, boolean ridden) {
        int calm = calm(horse);
        boolean cared = cared(horse);
        if (!NSV && (!cared || calm > 0)) return null;
        double reach = NSV ? SpookRule.CHALLENGER_REACH : SpookRule.MONSTER_REACH;
        Threat best = null; double bestDistance = 0;
        for (var mob : horse.level().getEntitiesOfClass(Monster.class, horse.getBoundingBox().inflate(reach, 4, reach), Monster::isAlive)) {
            double distance = horse.distanceTo(mob);
            var reaction = SpookRule.react(calm, NSV && mob.typeHolder().is(StableTags.CHALLENGERS), distance, ridden, cared);
            if (reaction == Reaction.NONE) continue;
            if (best == null || reaction.ordinal() > best.reaction().ordinal() || reaction == best.reaction() && distance < bestDistance) {
                best = new Threat(mob, reaction); bestDistance = distance;
            }
        }
        return best;
    }
    /** {@code BondMath.calm}: the horse's bond tier plus its tack's calm (a Bridle adds 1). */
    public static int calm(AbstractHorse horse) { return BondMath.calm(Horses.bondTier(horse), tackCalm(horse)); }
    /** Someone cares for it: it has a bond partner, or a player keeps it in a stall. */
    public static boolean cared(AbstractHorse horse) {
        return Horses.bondPartner(horse).isPresent() || Stables.stallOf(horse).map(StallHome::playerKept).orElse(false);
    }
    private static int tackCalm(AbstractHorse horse) {
        var saddle = horse.getItemBySlot(EquipmentSlot.SADDLE);
        if (saddle.isEmpty()) return 0;
        var id = BuiltInRegistries.ITEM.getKey(saddle.getItem());
        if (!id.getNamespace().equals("villagefriends")) return 0;
        return StableTable.gear(id.getPath()).map(StableTable.Gear::calm).orElse(0);
    }

    /**
     * Runs from a frightening monster when nobody is riding: vanilla's avoid-entity goal, with the target and the
     * decision from {@link SpookRule}. Looked at twice a second, and it also lets a steadier horse rear in place.
     */
    static final class SpookGoal extends AvoidEntityGoal<Monster> {
        private final AbstractHorse horse;
        /** Goal selectors ask every other tick; a horse only looks around for monsters twice a second. */
        private long nextLook;

        SpookGoal(AbstractHorse horse) { super(horse, Monster.class, (float) SpookRule.CHALLENGER_REACH, 1.2, 1.6); this.horse = horse; }

        @Override public boolean canUse() {
            if (horse.isVehicle() || horse.isLeashed() || !(horse.level() instanceof ServerLevel level)) return false;
            long now = level.getGameTime();
            if (now < nextLook) return false;
            nextLook = now + 10;
            if (!SpookRule.ready(last(horse), now)) return false;
            var threat = threat(horse, false);
            if (threat == null) return false;
            if (threat.reaction() == Reaction.REAR) { horse.makeMad(); mark(horse, now); return false; }
            if (threat.reaction() != Reaction.BOLT) return false;
            var away = DefaultRandomPos.getPosAway(horse, 16, 7, threat.mob().position());
            if (away == null || threat.mob().distanceToSqr(away) < threat.mob().distanceToSqr(horse)) return false;
            path = pathNav.createPath(away.x, away.y, away.z, 0);
            if (path == null) return false;
            toAvoid = threat.mob();
            mark(horse, now);
            return true;
        }
        @Override public boolean canContinueToUse() { return toAvoid != null && !horse.isVehicle() && super.canContinueToUse(); }
    }

    private Spook() {}
}
