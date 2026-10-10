package dev.villagefriends;

import dev.villagefriends.stable.api.Horses;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.function.BooleanSupplier;
import java.util.function.Supplier;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.animal.equine.Horse;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;
import org.jspecify.annotations.Nullable;

/**
 * Helpers for {@code StablehandGameTest} and its four scene classes. Game runs are rare (they need the user's
 * permission, RAM and time), so one run reports <b>every</b> failure at once: each {@link #scene} runs on a clean pad
 * inside its own try/catch, a failing scene is recorded with a screenshot and the next one still runs, and
 * {@link #finish} fails the test with the whole list.
 *
 * <p>{@link #check} is a hard check (it ends the scene; use it for preconditions such as "the horse spawned");
 * {@link #expect} is a soft one (it records and lets the scene go on; use it for every outcome). Never call these
 * from inside a client or server callback: they run on the test thread.
 */
@SuppressWarnings("UnstableApiUsage")
public final class StableTestKit {
    /** A scene's body; anything it throws ends that scene only. */
    @FunctionalInterface public interface Body { void run() throws Throwable; }

    /** Half the pad's width: the pad is 48 x 48 blocks of grass around {@link #origin}, cleared 8 blocks up. */
    public static final int PAD = 24;
    private final ClientGameTestContext c;
    private final TestSingleplayerContext w;
    private final List<String> failures = new ArrayList<>();
    private String scene = "setup";
    /** The middle of the pad, on top of the grass (where the player stands at the start of each scene). */
    public BlockPos origin;

    public StableTestKit(ClientGameTestContext c, TestSingleplayerContext w, BlockPos origin) { this.c = c; this.w = w; this.origin = origin; }

    // -- scenes and failures -------------------------------------------------------------------------

    /** Runs one scene from a clean pad; a failure is recorded (with a screenshot) and the next scene still runs. */
    public void scene(String name, Body body) {
        scene = name;
        try {
            pad(w);
            body.run();
        } catch (Throwable t) {
            failures.add(name + ": " + (t.getMessage() == null ? t.toString() : t.getMessage()));
            try { c.takeScreenshot("stablehand-fail-" + name); } catch (Throwable ignored) { /* the failure is already recorded */ }
        } finally {
            scene = "between scenes";
        }
    }
    /** Hard check: ends the current scene when it fails. */
    public void check(boolean ok, String why) { if (!ok) throw new AssertionError(why); }
    /** Soft check: records the failure and lets the scene go on. */
    public boolean expect(boolean ok, String why) {
        if (!ok) failures.add(scene + ": " + why);
        return ok;
    }
    /** Every failure so far. */
    public List<String> failures() { return List.copyOf(failures); }
    /** Fails the test with every recorded failure, one per line, or returns when there were none. */
    public void finish() {
        if (!failures.isEmpty()) throw new AssertionError(failures.size() + " Stablehand failure(s):\n  " + String.join("\n  ", failures));
    }

    // -- waiting and the server ---------------------------------------------------------------------

    /** Polls from the test thread, one tick at a time; on timeout it fails through {@link #check}. */
    public void until(ClientGameTestContext c, BooleanSupplier condition, int ticks, String what) { until(c, condition, ticks, () -> what); }
    public void until(ClientGameTestContext c, BooleanSupplier condition, int ticks, Supplier<String> what) {
        for (int i = 0; i < ticks; i++) { if (condition.getAsBoolean()) return; c.waitTicks(1); }
        check(condition.getAsBoolean(), "Timed out: " + what.get());
    }
    /** Evaluates a test on the server thread. */
    public boolean onServer(TestSingleplayerContext w, Supplier<Boolean> test) { return w.getServer().computeOnServer(s -> test.get()); }
    /** The entity with this id in the overworld (server side), or null. Call it on the server thread. */
    public @Nullable Entity entity(TestSingleplayerContext w, UUID id) { return w.getConnection().getServerLevel().getEntity(id); }
    public ServerLevel level() { return w.getConnection().getServerLevel(); }
    public ServerPlayer player() { return w.getConnection().getServerPlayer(); }

    /** A tame adult horse of a breed at {@code pos} (server thread), owned by {@code owner} when given. */
    public Horse horse(ServerLevel level, Vec3 pos, String breed, @Nullable Player owner) {
        var horse = EntityTypes.HORSE.create(level, EntitySpawnReason.COMMAND);
        check(horse != null, "a horse could be created");
        horse.snapTo(pos.x, pos.y, pos.z, 0, 0);
        if (owner != null) horse.tameWithName(owner); else horse.setTamed(true);
        Horses.assignBreed(horse, breed, level.getRandom());
        level.addFreshEntity(horse);
        return horse;
    }

    // -- the pad, pictures and moving things ------------------------------------------------------------

    /**
     * Rebuilds the 48 x 48 grass pad around {@link #origin}, clears the air above it, removes every entity on it but
     * the player, and puts the player back in the middle.
     */
    public void pad(TestSingleplayerContext w) {
        w.getServer().runOnServer(s -> {
            var level = w.getConnection().getServerLevel(); var p = w.getConnection().getServerPlayer();
            var box = new AABB(origin).inflate(PAD + 8, 16, PAD + 8);
            for (var e : level.getEntitiesOfClass(Entity.class, box, e -> !(e instanceof Player))) e.discard();
            for (int x = -PAD; x < PAD; x++) for (int z = -PAD; z < PAD; z++) {
                level.setBlock(origin.offset(x, -1, z), Blocks.GRASS_BLOCK.defaultBlockState(), 3);
                for (int y = 0; y < 8; y++) level.setBlock(origin.offset(x, y, z), Blocks.AIR.defaultBlockState(), 3);
            }
            p.stopRiding();
            p.teleportTo(origin.getX() + .5, origin.getY(), origin.getZ() + .5);
        });
        c.waitTicks(5);
    }
    /** Waits a moment, clears toasts and takes {@code stablehand-<name>} from wherever the player is looking. */
    public void view(ClientGameTestContext c, TestSingleplayerContext w, String name) {
        c.waitTicks(20);
        c.runOnClient(client -> client.gui.toastManager().clear());
        c.takeScreenshot("stablehand-" + name);
    }
    /** Moves the player to a spot and a facing first, then {@link #view(ClientGameTestContext, TestSingleplayerContext, String)}. */
    public void view(ClientGameTestContext c, TestSingleplayerContext w, Vec3 at, float yaw, float pitch, String name) {
        w.getServer().runCommand(String.format(java.util.Locale.ROOT, "tp @a %.2f %.2f %.2f %.1f %.1f", at.x, at.y, at.z, yaw, pitch));
        view(c, w, name);
    }
    /**
     * Moves an entity server side to {@code target} in {@code step}-block hops, two ticks apart, as if it travelled
     * there. {@code teleportTo(x, y, z)} carries its passengers along, so a rider moves with its horse.
     */
    public void stepTo(TestSingleplayerContext w, Entity entity, Vec3 target, double step) {
        UUID id = entity.getUUID();
        for (int hop = 0; hop < 1000; hop++) {
            boolean there = w.getServer().computeOnServer(s -> {
                var e = entity(w, id);
                if (e == null) return true;
                var from = e.position(); var delta = target.subtract(from);
                double length = delta.horizontalDistance();
                var next = length <= step ? target : from.add(delta.scale(step / Math.max(length, 1e-6)));
                e.teleportTo(next.x, next.y, next.z);
                return length <= step;
            });
            c.waitTicks(2);
            if (there) return;
        }
        check(false, "stepTo never reached " + target);
    }
}
