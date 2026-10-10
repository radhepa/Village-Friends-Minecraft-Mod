package dev.villagefriends.stable.yard;

import static dev.villagefriends.VillageFriends.target;

import dev.villagefriends.deed.Deeds;
import dev.villagefriends.stable.api.Horses;
import dev.villagefriends.stable.api.Stables;
import dev.villagefriends.stable.data.StableData;
import dev.villagefriends.stable.data.StableTable;
import dev.villagefriends.stable.data.StallHome;
import java.util.Comparator;
import java.util.List;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.animal.Animal;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.entity.animal.equine.Donkey;
import net.minecraft.world.entity.animal.equine.Mule;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;
import org.jspecify.annotations.Nullable;

/**
 * The Horse Stall block in use. Right-click it while riding a horse you own, or while leading one on a lead
 * (within {@link #LEAD_REACH} blocks), and that horse is stabled there: the stall becomes its home and it stays
 * within six blocks of it. A stall holds one horse; a player's horse already living there moves out (the
 * village's own horses keep their stalls). With an empty hand and no horse, it tells you whose stall it is.
 */
public final class Stalls {
    /** How far away a horse on your lead can be when you stable it. */
    public static final int LEAD_REACH = 10;
    /** How far from its stall a horse that lives there may be wandering and still be found. */
    private static final int HOME_REACH = 24;

    /** The stall was used (the yard's UseBlockCallback, main hand only; the game test calls it directly). */
    public static InteractionResult use(Player player, Level level, BlockPos pos) {
        if (player.isShiftKeyDown() || player.isSpectator()) return InteractionResult.PASS;
        if (!(level instanceof ServerLevel server))
            return player.getVehicle() instanceof AbstractHorse || player.getMainHandItem().isEmpty() || led(player, level, pos) != null ? InteractionResult.SUCCESS : InteractionResult.PASS;
        var horse = player.getVehicle() instanceof AbstractHorse ridden ? ridden : led(player, level, pos);
        if (horse == null) {
            if (!player.getMainHandItem().isEmpty()) return InteractionResult.PASS;
            player.sendOverlayMessage(Component.literal(describe(server, pos, player)));
            return InteractionResult.SUCCESS_SERVER;
        }
        var home = Stables.stallOf(horse).orElse(null);
        boolean owner = horse.getOwnerReference() != null && horse.getOwnerReference().getUUID().equals(player.getUUID());
        boolean kept = home != null && home.keeper().equals(keeper(player));
        if (!StallRules.canStall(owner, kept, home != null && home.residentOwned())) {
            player.sendOverlayMessage(Component.literal(home != null && home.residentOwned()
                    ? "This horse belongs to the village. It already has a stall of its own."
                    : "Only a horse you own can be stabled here. Tame it first."));
            return InteractionResult.SUCCESS_SERVER;
        }
        if (home != null && home.stall().equals(pos) && home.dimension().equals(dimension(server))) {
            player.sendOverlayMessage(Component.literal(yours(horse) + " already lives in this stall."));
            return InteractionResult.SUCCESS_SERVER;
        }
        var occupants = residents(server, pos);
        occupants.remove(horse);
        for (var other : occupants) {
            var theirs = Stables.stallOf(other).orElseThrow();
            if (!StallRules.mayEvict(theirs.residentOwned())) {
                player.sendOverlayMessage(Component.literal("This stall belongs to one of the village's horses."));
                return InteractionResult.SUCCESS_SERVER;
            }
        }
        for (var other : occupants) evict(other);
        var place = Deeds.place(server, pos);
        Stables.stall(horse, pos, place == null ? "" : place.village(), keeper(player));
        server.playSound(null, pos, SoundEvents.HORSE_BREATHE, SoundSource.NEUTRAL, 1F, 1F);
        var gone = occupants.isEmpty() ? null : occupants.getFirst();
        String moved = gone == null ? "" : gone.hasCustomName() ? " " + label(gone) + " moved out." : " The " + label(gone) + " that lived here moved out.";
        player.sendOverlayMessage(Component.literal(yours(horse) + " is stabled here now. It will stay close to this stall." + moved));
        return InteractionResult.SUCCESS_SERVER;
    }

    /**
     * A foal born to a stalled horse shares its parent's stall ({@link StallRules#foalStall} picks which), so it grows
     * up at home: it stays near the stall, eats from the trough (a minute off growing up per serving) and the
     * stablehand looks in on it. Runs from {@code BreedHooks.bred}, before the foal joins the world. Knights and
     * companions never take a foal, so it is left alone until it is grown.
     */
    public static void foaled(Animal parent, Animal partner, @Nullable AgeableMob child) {
        if (!(child instanceof AbstractHorse foal) || !(parent instanceof AbstractHorse a) || !(partner instanceof AbstractHorse b)
                || !(foal.level() instanceof ServerLevel level)) return;
        StallHome ha = atHome(a, level), hb = atHome(b, level);
        int pick = StallRules.foalStall(ha != null, ha != null && ha.playerKept(), hb != null, hb != null && hb.playerKept());
        if (pick < 0) return;
        var home = pick == 0 ? ha : hb;
        Stables.stall(foal, home.stall(), home.village(), home.keeper());
    }
    /** A parent's stall when it is at home (same dimension, within {@link StallRules#FOAL_REACH} blocks), else null. */
    private static @Nullable StallHome atHome(AbstractHorse parent, ServerLevel level) {
        StallHome home = target(parent).getAttached(StableData.STALL);
        return home != null && home.dimension().equals(dimension(level)) && parent.blockPosition().closerThan(home.stall(), StallRules.FOAL_REACH) ? home : null;
    }

    /** "player:&lt;uuid&gt;", the keeper of a horse a player stabled. */
    public static String keeper(Player player) { return "player:" + player.getUUID(); }

    /** Takes a horse's stall away: it forgets the stall and its vanilla home. */
    public static void evict(AbstractHorse horse) {
        target(horse).removeAttached(StableData.STALL);
        horse.clearHome();
    }

    /** Loaded horses whose stall is this block (normally one). */
    public static List<AbstractHorse> residents(ServerLevel level, BlockPos stall) {
        String dimension = dimension(level);
        return new java.util.ArrayList<>(level.getEntitiesOfClass(AbstractHorse.class, new AABB(stall).inflate(HOME_REACH), h -> h.isAlive() && lives(h, stall, dimension)));
    }
    static boolean lives(AbstractHorse horse, BlockPos stall, String dimension) {
        StallHome home = target(horse).getAttached(StableData.STALL);
        return home != null && home.stall().equals(stall) && home.dimension().equals(dimension);
    }
    static String dimension(ServerLevel level) { return level.dimension().identifier().toString(); }

    /** The horse a player is leading to this stall, the nearest if they lead several. */
    private static AbstractHorse led(Player player, Level level, BlockPos pos) {
        return level.getEntitiesOfClass(AbstractHorse.class, player.getBoundingBox().inflate(LEAD_REACH), h -> h.isAlive() && h.getLeashHolder() == player)
                .stream().min(Comparator.comparingDouble(h -> h.distanceToSqr(Vec3.atCenterOf(pos)))).orElse(null);
    }

    /** "Bramble's stall.", "Your Desert Horse's stall.", "An empty stall. ..." */
    static String describe(ServerLevel level, BlockPos pos, Player player) {
        var horses = residents(level, pos);
        if (horses.isEmpty()) return "An empty stall. Ride or lead a horse you own here to stable it.";
        var horse = horses.getFirst();
        var home = Stables.stallOf(horse).orElseThrow();
        if (horse.hasCustomName()) return label(horse) + "'s stall." + (home.keeper().equals(keeper(player)) ? " Yours." : "");
        if (home.keeper().equals(keeper(player))) return "Your " + label(horse) + "'s stall.";
        return home.residentOwned() ? "The village's " + label(horse) + " lives here." : "A " + label(horse) + "'s stall.";
    }

    /** "Bramble" for a named horse, else "Your Destrier". */
    private static String yours(AbstractHorse horse) { return horse.hasCustomName() ? label(horse) : "Your " + label(horse); }
    /** A horse's name for messages: its own name, else its breed ("Destrier"), else what it is ("Donkey"). */
    public static String label(AbstractHorse horse) {
        if (horse.hasCustomName()) return horse.getCustomName().getString();
        var breed = Horses.breed(horse).flatMap(StableTable::breed);
        if (breed.isPresent() && breed.get().raw().has("name")) return breed.get().raw().get("name").getAsString();
        if (horse instanceof Donkey) return "Donkey";
        if (horse instanceof Mule) return "Mule";
        return "Horse";
    }

    private Stalls() {}
}
