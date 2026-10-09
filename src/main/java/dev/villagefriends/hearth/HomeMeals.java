package dev.villagefriends.hearth;

import dev.villagefriends.routine.Routine;
import dev.villagefriends.routine.Routine.Block;
import dev.villagefriends.tavern.Patronage;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import net.fabricmc.fabric.api.attachment.v1.AttachmentRegistry;
import net.fabricmc.fabric.api.attachment.v1.AttachmentSyncPredicate;
import net.fabricmc.fabric.api.attachment.v1.AttachmentTarget;
import net.fabricmc.fabric.api.attachment.v1.AttachmentType;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerEntityEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.minecraft.core.particles.ItemParticleOption;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.entity.ai.memory.MemoryModuleType;
import net.minecraft.world.entity.npc.villager.Villager;

/**
 * Residents eat at home: at breakfast, lunch at home and supper, once they're back at their own house they
 * eat a real dish ({@link Tastes#homeMeal}: what suits them and the meal, now and then their favorite), dish
 * in hand, with bites, crumbs and a pause to chew. Birthday guests eat the party cake the same way. What they
 * are eating is shared with clients as {@link #STATE} ({@code eat:<item>} / {@code done:<item>}, the tavern's
 * format), so the tavern's client code draws the dish and picks dining animations.
 */
public final class HomeMeals {
    public static final AttachmentType<String> STATE = AttachmentRegistry.create(Hearth.id("meal"),
            b -> b.syncWith(ByteBufCodecs.STRING_UTF8, AttachmentSyncPredicate.all()));
    private record Meal(String item, long start, long end, String key) {}
    private static final Map<UUID, Meal> eating = new HashMap<>();
    /** "day|block" of the last meal each resident had, so a meal block gives one meal. */
    private static final Map<UUID, String> fed = new HashMap<>();

    static void register() {
        ServerEntityEvents.ENTITY_UNLOAD.register((entity, level) -> { if (entity instanceof Villager v) { eating.remove(v.getUUID()); fed.remove(v.getUUID()); } });
        ServerLifecycleEvents.SERVER_STOPPED.register(server -> { eating.clear(); fed.clear(); });
    }
    private static AttachmentTarget target(Villager v) { return (AttachmentTarget) v; }

    private static String meal(Block block) {
        return switch (block) { case BREAKFAST -> "breakfast"; case LUNCH_HOME -> "lunch"; case SUPPER -> "supper"; default -> null; };
    }

    /**
     * Once a second for every resident ({@code ResidentRoutines}). True while they are eating, so nothing walks
     * them off with a bowl in their hand.
     */
    public static boolean update(Villager v, ServerLevel level, Routine.Plan plan) {
        long now = level.getGameTime();
        var current = eating.get(v.getUUID());
        if (current != null) {
            boolean party = current.key.startsWith("party|");
            if (!party && meal(plan.block()) == null || v.isSleeping() || v.isPassenger()) { stop(v); return false; }
            if (now >= current.end + 100) { stop(v); return false; }
            if (now >= current.end) { done(v, current); return false; }
            chew(v, level, current, now);
            return true;
        }
        String meal = meal(plan.block());
        if (meal == null || v.isPassenger() || v.isSleeping()) return false;
        String key = dev.villagefriends.VillageFriends.day(level) + "|" + plan.block().id();
        if (key.equals(fed.get(v.getUUID()))) return false;
        // Home first: they eat once they're back at their own house (or wherever they are, if they have none).
        if (dev.villagefriends.home.Homes.homeward(v, level) != null || v.getNavigation().isInProgress() && v.getRandom().nextInt(4) != 0) return false;
        var dish = Tastes.homeMeal(HearthVillage.eater(v), meal, dev.villagefriends.VillageFriends.day(level), Dishes.all());
        if (dish == null) return false;
        fed.put(v.getUUID(), key);
        eat(v, dish.id(), 18 + v.getRandom().nextInt(14), key);
        return true;
    }
    /** Starts eating this item for a while: the dish in hand, bites and crumbs. */
    public static void eat(Villager v, String item, int seconds, String key) {
        long now = v.level().getGameTime();
        eating.put(v.getUUID(), new Meal(item, now, now + seconds * 20L, key));
        target(v).setAttached(STATE, Patronage.state(Patronage.Phase.EAT, item));
        v.getNavigation().stop();
        v.getBrain().eraseMemory(MemoryModuleType.WALK_TARGET);
    }
    private static void chew(Villager v, ServerLevel level, Meal m, long now) {
        v.getNavigation().stop();
        v.getBrain().eraseMemory(MemoryModuleType.WALK_TARGET);
        if (Math.floorMod(now - m.start + v.getId(), 80) < 20) {
            var stack = HearthItems.stack(m.item, 1);
            if (!stack.isEmpty()) {
                var look = v.getLookAngle();
                level.sendParticles(new ItemParticleOption(ParticleTypes.ITEM, stack.getItem()), v.getX() + look.x * .35, v.getEyeY() - .25, v.getZ() + look.z * .35, 4, .08, .04, .08, .02);
            }
            level.playSound(null, v.blockPosition(), SoundEvents.GENERIC_EAT.value(), SoundSource.NEUTRAL, .45F, .9F + v.getRandom().nextFloat() * .3F);
        }
    }
    private static void done(Villager v, Meal m) {
        String leftover = Patronage.leftover(m.item);
        if (leftover == null) { var d = Dishes.get(m.item); leftover = d == null ? null : d.vesselItem(); }
        target(v).setAttached(STATE, Patronage.state(Patronage.Phase.DONE, leftover));
    }
    public static void stop(Villager v) {
        eating.remove(v.getUUID());
        if (target(v).hasAttached(STATE)) target(v).removeAttached(STATE);
    }

    /** What they're eating right now, for conversation ("onion pottage"), or null. */
    public static String eatingNow(Villager v) {
        var m = eating.get(v.getUUID());
        if (m == null) return null;
        var d = Dishes.get(m.item);
        return d != null ? d.spoken() : dev.villagefriends.VillageFriends.itemName(m.item);
    }
    /** "Having supper · eating onion pottage" for the conversation window. */
    public static String doing(Villager v, String label) {
        String now = eatingNow(v);
        return now == null ? label : label + " · eating " + now;
    }

    private HomeMeals() {}
}
