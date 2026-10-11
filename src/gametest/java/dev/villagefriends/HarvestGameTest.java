package dev.villagefriends;

import dev.villagefriends.hearth.HearthItems;
import java.util.List;
import java.util.Map;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.enchantment.Enchantments;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.CropBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.storage.loot.LootParams;
import net.minecraft.world.level.storage.loot.parameters.LootContextParams;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Hearth & Harvest's crop and station loot tables in a real world: an unripe crop gives back only its seed; a
 * ripe one gives 1 to its most produce and 1-3 seeds, Fortune adds seeds, an explosion thins the drops out; a
 * survival player's break drops the same on the ground; every other block with a loot table (stations,
 * workstations, furniture) drops itself unless blown up. Every case is rolled hundreds of times through the
 * block's own loot table ({@code -Ptests=HarvestGameTest}).
 */
@SuppressWarnings("UnstableApiUsage")
public final class HarvestGameTest implements FabricClientGameTest {
    private static final Logger LOGGER = LoggerFactory.getLogger("HarvestGameTest");
    private static final int ROLLS = 400;
    /** Produce per ripe harvest, the drops column of tools/hearth/crops.tsv. */
    private static final Map<String, Integer> MOST = Map.of("onion", 3, "cabbage", 2, "barley", 2, "leek", 2, "garlic", 3, "herbs", 3);
    private static void check(boolean ok, String reason) { if (!ok) throw new AssertionError(reason); }
    private static ServerLevel level(TestSingleplayerContext w) { return w.getConnection().getServerLevel(); }
    private static ServerPlayer player(TestSingleplayerContext w) { return w.getConnection().getServerPlayer(); }

    /** One break of the block through its loot table, with a tool and, when radius > 0, an explosion. */
    private static List<ItemStack> drops(ServerLevel level, BlockState state, BlockPos pos, ItemStack tool, float radius) {
        var params = new LootParams.Builder(level).withParameter(LootContextParams.ORIGIN, Vec3.atCenterOf(pos)).withParameter(LootContextParams.TOOL, tool);
        if (radius > 0) params.withParameter(LootContextParams.EXPLOSION_RADIUS, radius);
        return state.getDrops(params);
    }

    /** What ROLLS breaks gave: the fewest and most of each item in one break, and the total. */
    private record Tally(int fewestProduce, int mostProduce, int produce, int fewestSeeds, int mostSeeds, int seeds) {
        static Tally of(ServerLevel level, BlockState state, BlockPos pos, ItemStack tool, float radius, Item produceItem, Item seedItem) {
            int fp = Integer.MAX_VALUE, mp = 0, p = 0, fs = Integer.MAX_VALUE, ms = 0, s = 0;
            for (int i = 0; i < ROLLS; i++) {
                int np = 0, ns = 0;
                for (var stack : drops(level, state, pos, tool, radius)) {
                    if (stack.isEmpty()) continue; // explosion_decay took the whole stack; the game drops nothing
                    if (stack.is(produceItem)) np += stack.getCount();
                    else if (stack.is(seedItem)) ns += stack.getCount();
                    else throw new AssertionError(state + " dropped something else: " + stack);
                }
                fp = Math.min(fp, np); mp = Math.max(mp, np); p += np;
                fs = Math.min(fs, ns); ms = Math.max(ms, ns); s += ns;
            }
            return new Tally(fp, mp, p, fs, ms, s);
        }
        @Override public String toString() {
            return "produce " + fewestProduce + "-" + mostProduce + " (avg " + String.format("%.2f", produce / (double) ROLLS) + "), seeds "
                    + fewestSeeds + "-" + mostSeeds + " (avg " + String.format("%.2f", seeds / (double) ROLLS) + ")";
        }
    }

    @Override public void runTest(ClientGameTestContext c) {
        try (var w = c.worldBuilder().create()) {
            w.getConnection().waitForChunksRender();
            for (var cmd : List.of("time set 6000", "gamerule advance_time false", "gamerule spawn_mobs false", "gamerule random_tick_speed 0", "tp @a ~ ~ ~ 0 15"))
                w.getServer().runCommand(cmd);
            check(w.getServer().computeOnServer(s -> HearthItems.crops().size()) == MOST.size(), "Six Hearth crops are registered");

            // -- every crop, through its loot table ------------------------------------------------------------
            w.getServer().runOnServer(s -> {
                var level = level(w);
                var pos = player(w).blockPosition().offset(0, 0, 3);
                var fortune = new ItemStack(Items.IRON_HOE);
                fortune.enchant(s.registryAccess().lookupOrThrow(Registries.ENCHANTMENT).getOrThrow(Enchantments.FORTUNE), 3);
                for (Block block : HearthItems.crops()) {
                    var crop = (CropBlock) block;
                    var name = BuiltInRegistries.BLOCK.getKey(block).getPath().replace("_crop", "");
                    Item produce = HearthItems.get(name), seed = block.asItem();
                    int most = MOST.get(name);
                    for (int age = 0; age < crop.getMaxAge(); age++) {
                        var t = Tally.of(level, crop.getStateForAge(age), pos, ItemStack.EMPTY, 0, produce, seed);
                        check(t.mostProduce == 0 && t.fewestSeeds == 1 && t.mostSeeds == 1,
                                "An unripe " + name + " (age " + age + ") gives back just its seed, got " + t);
                    }
                    var ripe = crop.getStateForAge(crop.getMaxAge());
                    var bare = Tally.of(level, ripe, pos, ItemStack.EMPTY, 0, produce, seed);
                    LOGGER.info("Ripe {} by hand: {}", name, bare);
                    check(bare.fewestProduce == 1 && bare.mostProduce == most, "A ripe " + name + " gives 1-" + most + " produce, got " + bare);
                    // The seed entry gives 1, and binomial_with_bonus_count adds 2 (+ Fortune) tries at 4/7, as wheat's 3 do.
                    check(bare.fewestSeeds == 1 && bare.mostSeeds == 3, "A ripe " + name + " gives 1-3 seeds, got " + bare);
                    double seedAvg = bare.seeds / (double) ROLLS;
                    check(seedAvg > 1.95 && seedAvg < 2.35, "A ripe " + name + " averages 1 + 2 x 4/7 seeds, got " + bare);

                    var lucky = Tally.of(level, ripe, pos, fortune, 0, produce, seed);
                    LOGGER.info("Ripe {} with Fortune III: {}", name, lucky);
                    check(lucky.fewestProduce == 1 && lucky.mostProduce == most, "Fortune leaves a ripe " + name + "'s produce alone, got " + lucky);
                    check(lucky.fewestSeeds >= 1 && lucky.mostSeeds == 6 && lucky.seeds > bare.seeds * 3 / 2, "Fortune III gives a ripe " + name + " up to 6 seeds, got " + lucky);

                    var blown = Tally.of(level, ripe, pos, ItemStack.EMPTY, 8, produce, seed);
                    LOGGER.info("Ripe {} in a radius-8 explosion: {}", name, blown);
                    check(blown.produce + blown.seeds < (bare.produce + bare.seeds) / 3, "An explosion destroys most of a ripe " + name + "'s drops, got " + blown);
                }
            });

            // -- a survival player breaking a ripe and an unripe barley crop -----------------------------------
            w.getServer().runCommand("gamemode survival @a");
            w.getServer().runOnServer(s -> {
                var level = level(w);
                var origin = player(w).blockPosition();
                var barley = (CropBlock) HearthItems.crops().stream().filter(b -> BuiltInRegistries.BLOCK.getKey(b).getPath().equals("barley_crop")).findFirst().orElseThrow();
                Item produce = HearthItems.get("barley"), seed = barley.asItem();
                for (int age : new int[]{0, barley.getMaxAge()}) {
                    var pos = origin.offset(age == 0 ? -1 : 1, 0, 2);
                    level.setBlock(pos.below(), Blocks.FARMLAND.defaultBlockState(), 3);
                    level.setBlock(pos, barley.getStateForAge(age), 3);
                    check(player(w).gameMode.destroyBlock(pos), "The player breaks the barley crop at age " + age);
                    var box = new AABB(pos).inflate(1.5);
                    int p = 0, sd = 0;
                    for (var e : level.getEntitiesOfClass(ItemEntity.class, box)) {
                        if (e.getItem().is(produce)) p += e.getItem().getCount();
                        else if (e.getItem().is(seed)) sd += e.getItem().getCount();
                        e.discard();
                    }
                    LOGGER.info("Survival break of barley at age {}: {} barley, {} seeds", age, p, sd);
                    if (age == 0) check(p == 0 && sd == 1, "Breaking young barley drops one seed, got " + p + " barley and " + sd + " seeds");
                    else check(p >= 1 && p <= 2 && sd >= 1 && sd <= 3, "Breaking ripe barley drops 1-2 barley and 1-3 seeds, got " + p + " barley and " + sd + " seeds");
                }
            });

            // -- the stations, workstations and furniture drop themselves, unless an explosion takes them --------
            w.getServer().runOnServer(s -> {
                var level = level(w);
                var pos = player(w).blockPosition().offset(0, 0, 4);
                var crops = HearthItems.crops();
                int checked = 0;
                for (Block block : BuiltInRegistries.BLOCK) {
                    var id = BuiltInRegistries.BLOCK.getKey(block);
                    if (!id.getNamespace().equals("villagefriends") || crops.contains(block)) continue;
                    var state = block.defaultBlockState();
                    var whole = drops(level, state, pos, ItemStack.EMPTY, 0);
                    if (whole.isEmpty()) continue; // no loot table (seats and other helper blocks)
                    check(whole.size() == 1 && whole.getFirst().is(block.asItem()) && whole.getFirst().getCount() == 1, id + " drops itself, got " + whole);
                    int kept = 0;
                    for (int i = 0; i < ROLLS; i++) for (var stack : drops(level, state, pos, ItemStack.EMPTY, 8)) kept += stack.getCount();
                    LOGGER.info("{} survived {} of {} radius-8 explosions", id, kept, ROLLS);
                    check(kept > ROLLS / 8 / 3 && kept < ROLLS / 8 * 3, id + " survives about 1 in 8 radius-8 explosions, got " + kept + " of " + ROLLS);
                    checked++;
                }
                check(checked == 29, "The 29 blocks with their own loot table were checked, got " + checked);
            });
            LOGGER.info("Harvest loot checks passed");
        }
    }
}
