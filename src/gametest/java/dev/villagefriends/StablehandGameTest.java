package dev.villagefriends;

import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.minecraft.client.gui.screens.worldselection.WorldCreationUiState;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.level.levelgen.presets.WorldPresets;

/**
 * Stablehand in a flat world, in four scenes that each start from a clean 48 x 48 pad: breeds, foals, coats, bond
 * and the whistle ({@link StableBreedScenes}); tack, barding, pack slots, the lance and pack animals
 * ({@link StableGearScenes}); stalls, troughs, papers and the stable building ({@link StableYardScenes}); knights on
 * horseback, companions' horses, caravan guards, horse theft and spooking ({@link StableRiderScenes}). A failing
 * scene doesn't stop the others: {@link StableTestKit#finish} reports every failure at the end. Screenshots:
 * {@code stablehand-<name>}, and {@code stablehand-fail-<scene>} for a scene that failed.
 *
 * <p>Not in the default test list: run it with {@code gradlew runClientGameTest -Ptests=StablehandGameTest -PtestHeap=2560m}.
 */
@SuppressWarnings("UnstableApiUsage")
public final class StablehandGameTest implements FabricClientGameTest {
    @Override public void runTest(ClientGameTestContext c) {
        c.getInput().resizeWindow(1280, 800);
        try (var w = c.worldBuilder().adjustSettings(ui -> {
            var flat = ui.getSettings().worldgenLoadContext().lookupOrThrow(Registries.WORLD_PRESET).getOrThrow(WorldPresets.FLAT);
            ui.setWorldType(new WorldCreationUiState.WorldTypeEntry(flat));
            ui.setGenerateStructures(false);
            ui.setSeed("11");
        }).create()) {
            for (int attempt = 0; attempt < 3; attempt++) { try { w.getConnection().waitForChunksRender(); break; } catch (AssertionError slow) { c.waitTicks(100); } }
            w.getServer().runCommand("gamemode survival @a");
            w.getServer().runCommand("difficulty easy");
            w.getServer().runCommand("weather clear");
            w.getServer().runCommand("gamerule spawn_mobs false");
            w.getServer().runCommand("gamerule advance_time false");
            w.getServer().runCommand("time set 6000");
            BlockPos origin = w.getServer().computeOnServer(s -> {
                var p = w.getConnection().getServerPlayer();
                p.addEffect(new MobEffectInstance(MobEffects.RESISTANCE, 1_000_000, 4, false, false));
                return p.blockPosition();
            });
            var kit = new StableTestKit(c, w, origin);
            kit.scene("breeds", () -> StableBreedScenes.run(c, w, kit));
            kit.scene("gear", () -> StableGearScenes.run(c, w, kit));
            kit.scene("yard", () -> StableYardScenes.run(c, w, kit));
            kit.scene("riders", () -> StableRiderScenes.run(c, w, kit));
            kit.finish();
        }
    }
}
