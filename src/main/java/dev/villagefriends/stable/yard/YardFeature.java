package dev.villagefriends.stable.yard;

import dev.villagefriends.stable.data.StableBlocks;
import dev.villagefriends.stable.data.StableItems;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerEntityEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.fabricmc.fabric.api.event.player.UseBlockCallback;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.BlockHitResult;

/**
 * Stalls, troughs, the stablehand, Horse Papers and stable horses (the stables package): registers that
 * package's listeners. Called once from {@code Stablehand.register()}.
 *
 * <ul>
 * <li>Using a block: Horse Papers on any block's top ({@link Papers}), the Horse Stall ({@link Stalls}). The Hay
 * Trough handles its own use ({@code HayTroughBlock}).</li>
 * <li>Every tick: template horses queued on load settle ({@link StableHorses}).</li>
 * <li>Every {@link #YARD_TICKS} ticks, per level: the yard tick (feeding, settling retries, stalls that are gone).</li>
 * <li>The stablehand's work runs from the routine chain ({@link StableWork}).</li>
 * </ul>
 */
public final class YardFeature {
    /** The yard tick: every 30 seconds. */
    public static final int YARD_TICKS = 600;

    public static void register() {
        UseBlockCallback.EVENT.register(YardFeature::use);
        ServerEntityEvents.ENTITY_LOAD.register(StableHorses::loaded);
        ServerEntityEvents.ENTITY_UNLOAD.register((entity, level) -> { StableHorses.unloaded(entity); StableWork.unload(entity); });
        ServerTickEvents.END_SERVER_TICK.register(YardFeature::tick);
        ServerLifecycleEvents.SERVER_STOPPED.register(server -> { StableHorses.clear(); StableWork.clear(); });
    }

    private static InteractionResult use(Player player, Level level, InteractionHand hand, BlockHitResult hit) {
        var stack = player.getItemInHand(hand);
        if (stack.is(StableItems.HORSE_PAPERS)) return Papers.use(player, level, hit, stack);
        if (hand == InteractionHand.MAIN_HAND && level.getBlockState(hit.getBlockPos()).is(StableBlocks.HORSE_STALL)) return Stalls.use(player, level, hit.getBlockPos());
        return InteractionResult.PASS;
    }

    private static void tick(MinecraftServer server) {
        StableHorses.tick(server);
        if (server.getTickCount() % YARD_TICKS == 0) for (var level : server.getAllLevels()) yardTick(level);
    }
    /** One yard tick for a level, now: feeding, settling retries and stalls that are gone (the game test calls it). */
    public static void yardTick(ServerLevel level) { StableHorses.yard(level); }

    private YardFeature() {}
}
