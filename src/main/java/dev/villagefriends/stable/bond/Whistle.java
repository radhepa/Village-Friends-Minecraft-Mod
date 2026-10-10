package dev.villagefriends.stable.bond;

import dev.villagefriends.stable.data.StableItems;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;
import org.jspecify.annotations.Nullable;

/**
 * The Horse Whistle: two flute notes call your most bonded horse that is Loyal or better and loaded within 96
 * blocks (not ridden, not tied to someone else). A horse that is near and can walk to you comes at a canter,
 * re-pathing for up to 20 seconds; one that is far (over 40 blocks) or has no way through is brought to a free spot
 * a few blocks behind you, never into a wall or water. Unloaded horses can't hear it in v1.
 */
public final class Whistle {
    public static final double REACH = 96, FAR = 40, ARRIVED = 3, CANTER = 2.2;
    public static final int COOLDOWN = 60, FOLLOW_TICKS = 400;
    /** Horses on their way to a whistle, by horse id. */
    private static final Map<UUID, Call> CALLS = new HashMap<>();
    private record Call(ResourceKey<Level> dimension, UUID player, long until) {}
    /** The whistle's second, higher note, a few ticks after the first. */
    private static final List<Note> NOTES = new ArrayList<>();
    private record Note(ResourceKey<Level> dimension, Vec3 at, long when) {}

    public static InteractionResult use(Player player, Level level, InteractionHand hand) {
        var stack = player.getItemInHand(hand);
        if (!stack.is(StableItems.HORSE_WHISTLE) || player.isSpectator() || player.getCooldowns().isOnCooldown(stack)) return InteractionResult.PASS;
        if (player instanceof ServerPlayer sp) blow(sp, stack);
        return InteractionResult.SUCCESS;
    }

    /** Blows the whistle (the game test calls this too): returns the horse that answered, or null. */
    public static @Nullable AbstractHorse blow(ServerPlayer player, ItemStack stack) {
        var level = player.level();
        player.getCooldowns().addCooldown(stack, COOLDOWN);
        level.playSound(null, player.getX(), player.getEyeY(), player.getZ(), SoundEvents.NOTE_BLOCK_FLUTE.value(), SoundSource.PLAYERS, 1.5F, 1.8F);
        NOTES.add(new Note(level.dimension(), player.getEyePosition(), level.getGameTime() + 4));
        var horse = answering(player, level);
        if (horse == null) {
            player.sendSystemMessage(Component.literal("No horse of yours is close enough to hear the whistle."), true);
            return null;
        }
        String who = BondMath.call(Bonds.customName(horse), Bonds.kind(horse), true);
        horse.setEating(false);
        horse.playAmbientSound();
        var path = horse.distanceTo(player) > FAR ? null : horse.getNavigation().createPath(player, 1);
        if (path != null && path.canReach()) {
            horse.getNavigation().moveTo(path, CANTER);
            CALLS.put(horse.getUUID(), new Call(level.dimension(), player.getUUID(), level.getGameTime() + FOLLOW_TICKS));
            player.sendSystemMessage(Component.literal(who + " heard you and is on the way."), true);
        } else if (fetch(horse, player, level)) {
            player.sendSystemMessage(Component.literal(who + " comes at your whistle."), true);
        } else {
            player.sendSystemMessage(Component.literal(who + " heard you, but can't find a way to you."), true);
        }
        return horse;
    }

    /** The bonded horse that answers: the highest bond, then the nearest. */
    static @Nullable AbstractHorse answering(ServerPlayer player, ServerLevel level) {
        String me = player.getStringUUID();
        AbstractHorse best = null;
        int bestPoints = -1;
        double bestDistance = 0;
        for (var horse : level.getEntitiesOfClass(AbstractHorse.class, player.getBoundingBox().inflate(REACH), h -> h.isAlive() && Bonds.bondable(h))) {
            var bond = Bonds.bond(horse);
            double distance = horse.distanceToSqr(player);
            if (!bond.partner().equals(me) || !Bonds.owns(player, horse) || BondMath.tier(bond.points()) < BondMath.WHISTLE_TIER || horse.isVehicle()
                    || horse.isLeashed() && horse.getLeashHolder() != player || distance > REACH * REACH) continue;
            if (bond.points() > bestPoints || bond.points() == bestPoints && distance < bestDistance) { best = horse; bestPoints = bond.points(); bestDistance = distance; }
        }
        return best;
    }

    /** Brings the horse to a free spot 3-6 blocks behind the player (solid ground, no water, room for a horse). */
    static boolean fetch(AbstractHorse horse, ServerPlayer player, ServerLevel level) {
        var back = Vec3.directionFromRotation(0, player.getYRot()).scale(-1);
        var side = new Vec3(-back.z, 0, back.x);
        for (int distance = 3; distance <= 6; distance++) for (int across : new int[]{0, 1, -1, 2, -2}) {
            var spot = standable(horse, level, BlockPos.containing(player.position().add(back.scale(distance)).add(side.scale(across))));
            if (spot == null) continue;
            horse.getNavigation().stop();
            horse.teleportTo(spot.x, spot.y, spot.z);
            horse.setYRot(player.getYRot());
            return true;
        }
        return false;
    }

    private static @Nullable Vec3 standable(AbstractHorse horse, ServerLevel level, BlockPos column) {
        for (int dy : new int[]{0, 1, -1, 2, -2, 3, -3}) {
            var pos = column.above(dy);
            var below = pos.below();
            if (!level.getBlockState(below).isFaceSturdy(level, below, Direction.UP)) continue;
            if (!level.getFluidState(pos).isEmpty() || !level.getFluidState(pos.above()).isEmpty()) continue;
            var at = Vec3.atBottomCenterOf(pos);
            if (level.noCollision(horse, horse.getDimensions(horse.getPose()).makeBoundingBox(at))) return at;
        }
        return null;
    }

    /** The second note, and called horses keeping on toward their rider (re-pathing twice a second). */
    public static void tick(MinecraftServer server) {
        if (!NOTES.isEmpty()) NOTES.removeIf(note -> {
            var level = server.getLevel(note.dimension());
            if (level == null) return true;
            if (level.getGameTime() < note.when()) return false;
            level.playSound(null, note.at().x, note.at().y, note.at().z, SoundEvents.NOTE_BLOCK_FLUTE.value(), SoundSource.PLAYERS, 1.5F, 2.0F);
            return true;
        });
        if (!CALLS.isEmpty() && server.getTickCount() % 10 == 0) CALLS.entrySet().removeIf(e -> !follow(server, e.getKey(), e.getValue()));
    }

    /** Keeps a called horse coming; false once it arrived, gave up or can't any more. */
    private static boolean follow(MinecraftServer server, UUID id, Call call) {
        var level = server.getLevel(call.dimension());
        var player = server.getPlayerList().getPlayer(call.player());
        if (level == null || player == null || player.level() != level || level.getGameTime() > call.until()) return false;
        if (!(level.getEntity(id) instanceof AbstractHorse horse) || !horse.isAlive() || horse.isVehicle()) return false;
        if (horse.distanceToSqr(player) <= ARRIVED * ARRIVED) {
            horse.getNavigation().stop();
            horse.getLookControl().setLookAt(player);
            return false;
        }
        horse.setEating(false);
        horse.getNavigation().moveTo(player, CANTER);
        return true;
    }

    /** Whether a horse is on its way to a whistle (for tests). */
    public static boolean called(AbstractHorse horse) { return CALLS.containsKey(horse.getUUID()); }

    public static void clear() { CALLS.clear(); NOTES.clear(); }

    private Whistle() {}
}
