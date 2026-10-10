package dev.villagefriends;

import dev.villagefriends.client.FishingClient;
import dev.villagefriends.client.JournalScreen;
import dev.villagefriends.client.StationScreen;
import dev.villagefriends.fishing.Angling;
import dev.villagefriends.fishing.Contest;
import dev.villagefriends.fishing.Contests;
import dev.villagefriends.fishing.DockAnglers;
import dev.villagefriends.fishing.Docks;
import dev.villagefriends.fishing.FishTable;
import dev.villagefriends.fishing.Fishing;
import dev.villagefriends.fishing.FishingApi;
import dev.villagefriends.fishing.FishingCompat;
import dev.villagefriends.fishing.FishingConfig;
import dev.villagefriends.fishing.FishingItems;
import dev.villagefriends.fishing.Gear;
import dev.villagefriends.fishing.TrophyMount;
import dev.villagefriends.hearth.HearthBlocks;
import dev.villagefriends.hearth.HearthItems;
import dev.villagefriends.hearth.StationBlock;
import dev.villagefriends.hearth.StationBlockEntity;
import dev.villagefriends.hearth.StationMenu;
import dev.villagefriends.mixin.FishingHookAccess;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import net.fabricmc.fabric.api.attachment.v1.AttachmentTarget;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.fabricmc.loader.api.FabricLoader;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.stats.Stats;
import net.minecraft.tags.ItemTags;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.npc.villager.VillagerProfession;
import net.minecraft.world.inventory.ContainerInput;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.Vec3;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Tall Tales Fishing in a real client: a fish caught through the catch-bar minigame (cast with a real right
 * click, the bar played every tick on the client, the catch handed over by the server) with bait and tackle used
 * up; the journal before and after (silhouette to revealed); a legend landed as a trophy and hung on a Trophy
 * Mount; vanilla fishing with the minigame switched off; a village dock built at the water and its fisherman
 * fishing off it; a contest day with the scoreboard, a resident entrant, results and prizes; a tall tale and a
 * message in a bottle noted in the journal; a fish dish cooked at the prep table; and the optional ties (RPG
 * Fishing skill, a Brineclaw from Not-So-Vanilla Mobs). {@code -Ptests=FishingGameTest}, with or without the
 * add-ons.
 */
@SuppressWarnings("UnstableApiUsage")
public final class FishingGameTest implements FabricClientGameTest {
    private static final Logger LOGGER = LoggerFactory.getLogger("FishingGameTest");
    private static void check(boolean ok, String reason) { if (!ok) throw new AssertionError(reason); }
    private static ServerLevel level(TestSingleplayerContext w) { return w.getConnection().getServerLevel(); }
    private static ServerPlayer player(TestSingleplayerContext w) { return w.getConnection().getServerPlayer(); }
    private static void flush(TestSingleplayerContext w) { w.getConnection().waitForServerboundPackets(); w.getConnection().waitForClientboundPackets(); }
    private static Item fishItem(String id) { return BuiltInRegistries.ITEM.getValue(Identifier.parse(FishTable.get(id).item())); }
    private static int count(TestSingleplayerContext w, Item item) {
        return w.getServer().computeOnServer(s -> { var inv = player(w).getInventory(); int n = 0;
            for (int i = 0; i < inv.getContainerSize(); i++) if (inv.getItem(i).is(item)) n += inv.getItem(i).getCount(); return n; });
    }
    /** On the server thread: whether the player holds any of this item. */
    private static boolean has(TestSingleplayerContext w, Item item) {
        var inv = player(w).getInventory();
        for (int i = 0; i < inv.getContainerSize(); i++) if (inv.getItem(i).is(item)) return true;
        return false;
    }
    private static ItemStack find(TestSingleplayerContext w, Item item) {
        return w.getServer().computeOnServer(s -> { var inv = player(w).getInventory();
            for (int i = 0; i < inv.getContainerSize(); i++) if (inv.getItem(i).is(item)) return inv.getItem(i).copy(); return ItemStack.EMPTY; });
    }
    private static void slot(TestSingleplayerContext w, int slot, ItemStack stack) { w.getServer().runOnServer(s -> player(w).getInventory().setItem(slot, stack)); }

    /** Waits (on the test thread) until a check on the server holds, up to {@code ticks}. */
    private static void waitServer(ClientGameTestContext c, TestSingleplayerContext w, java.util.function.Predicate<net.minecraft.server.MinecraftServer> test, int ticks) {
        for (int i = 0; i < ticks; i++) {
            if (w.getServer().computeOnServer(test::test)) return;
            c.waitTick();
        }
        throw new AssertionError("Timed out waiting for the server");
    }
    /** A real right click with the item in {@code slot}, then waits for the hook to settle in the water. */
    private static void cast(ClientGameTestContext c, TestSingleplayerContext w, int slot) {
        flush(w); c.waitTicks(5); flush(w);
        // Aim well out over the pond (vanilla's throw varies a little), on both sides so the server casts the same way.
        w.getServer().runOnServer(s -> { player(w).setYRot(180); player(w).setXRot(12); });
        c.runOnClient(client -> { client.gui.setScreen(null); client.player.getInventory().setSelectedSlot(slot); client.player.setYRot(180); client.player.setXRot(12);
            client.gameMode.useItem(client.player, InteractionHand.MAIN_HAND); });
        flush(w);
        for (int i = 0; i < 200; i++) {
            if (w.getServer().computeOnServer(s -> player(w).fishing != null && player(w).fishing.isInWater())) { c.waitTicks(10); return; }
            c.waitTick();
        }
        c.takeScreenshot("fishing-cast-failed");
        String state = w.getServer().computeOnServer(s -> { var p = player(w); var h = p.fishing;
            return "player " + p.position() + " yaw " + p.getYRot() + " pitch " + p.getXRot() + " holding " + p.getMainHandItem() + " hook "
                    + (h == null ? "none" : h.position() + " removed " + h.isRemoved()); });
        throw new AssertionError("The cast never reached the water: " + state);
    }
    /** Something (this fish) bites at once. */
    private static void bite(TestSingleplayerContext w, String fish) {
        w.getServer().runOnServer(s -> {
            var p = player(w);
            check(p.fishing != null, "The line is out");
            Angling.next(p, FishTable.get(fish));
            ((FishingHookAccess) p.fishing).villagefriends$setTimeUntilLured(1);
        });
    }
    /** Waits for the minigame to come up, photographs it, and lets the test player play it out. True if the fish was landed. */
    private static boolean playOut(ClientGameTestContext c, TestSingleplayerContext w, String shot) {
        c.waitFor(client -> FishingClient.game() != null, 400);
        c.waitTicks(30);
        if (shot != null) c.takeScreenshot(shot);
        c.waitFor(client -> FishingClient.game() == null || FishingClient.game().done(), 2000);
        boolean won = c.computeOnClient(client -> FishingClient.game() != null && FishingClient.game().won());
        c.waitFor(client -> FishingClient.game() == null, 100);
        flush(w); c.waitTicks(10); flush(w);
        return won;
    }
    private static int journalCount(ClientGameTestContext c, String fish) {
        return c.computeOnClient(client -> {
            var j = ((AttachmentTarget) client.player).getAttachedOrElse(Fishing.JOURNAL, dev.villagefriends.fishing.Journal.EMPTY);
            return j.caught(fish) ? j.entry(fish).count() : 0;
        });
    }
    private static void use(ClientGameTestContext c, TestSingleplayerContext w, int slot) {
        c.runOnClient(client -> { client.gui.setScreen(null); client.player.getInventory().setSelectedSlot(slot); client.gameMode.useItem(client.player, InteractionHand.MAIN_HAND); });
        flush(w);
    }
    private static long skill(ServerPlayer p, String skill) {
        try {
            var sheet = Class.forName("dev.villagefriends.rpg.Rpg").getMethod("sheet", net.minecraft.world.entity.player.Player.class).invoke(null, p);
            @SuppressWarnings("unchecked") var skills = (Map<String, Long>) sheet.getClass().getMethod("skills").invoke(sheet);
            return skills.getOrDefault(skill, 0L);
        } catch (ReflectiveOperationException e) { throw new AssertionError("RPG sheet unreadable", e); }
    }

    @Override public void runTest(ClientGameTestContext c) {
        c.getInput().resizeWindow(1280, 800); c.runOnClient(client -> { client.options.guiScale().set(2); client.resizeGui(); });
        boolean rpg = FabricLoader.getInstance().isModLoaded("villagefriends_rpg"), nsv = FabricLoader.getInstance().isModLoaded("nsvmobs");
        try (var w = c.worldBuilder().create()) {
            w.getConnection().waitForChunksRender();
            for (var cmd : List.of("gamemode survival @a", "time set 6000", "gamerule advance_time false", "gamerule advance_weather false",
                    "gamerule spawn_mobs false", "weather clear", "tp @a ~ ~ ~ 180 35"))
                w.getServer().runCommand(cmd);
            // A plank landing on the south side of a pond 9 wide, 18 long and 3 deep, to the north of the player.
            BlockPos origin = w.getServer().computeOnServer(s -> {
                var level = level(w); var o = player(w).blockPosition();
                player(w).addEffect(new MobEffectInstance(MobEffects.RESISTANCE, 20 * 600, 4, true, false));
                player(w).addEffect(new MobEffectInstance(MobEffects.SATURATION, 20 * 600, 0, true, false));
                for (int x = -10; x <= 10; x++) for (int z = -24; z <= 6; z++) {
                    for (int y = -5; y < 0; y++) level.setBlock(o.offset(x, y, z), Blocks.STONE.defaultBlockState(), 3);
                    for (int y = 0; y < 6; y++) level.setBlock(o.offset(x, y, z), Blocks.AIR.defaultBlockState(), 3);
                    boolean pond = x >= -4 && x <= 4 && z <= -3 && z >= -20;
                    level.setBlock(o.offset(x, -1, z), pond ? Blocks.WATER.defaultBlockState() : Blocks.SPRUCE_PLANKS.defaultBlockState(), 3);
                    if (pond) { level.setBlock(o.offset(x, -2, z), Blocks.WATER.defaultBlockState(), 3); level.setBlock(o.offset(x, -3, z), Blocks.WATER.defaultBlockState(), 3); }
                }
                return o;
            });
            // The setting is saved in the config file: start from the minigame on, whatever an earlier run left.
            w.getServer().runOnServer(s -> FishingConfig.minigame(true));
            check(w.getServer().computeOnServer(s -> FishTable.all().size()) >= 80, "The fish table loaded");
            check(w.getServer().computeOnServer(s -> new ItemStack(fishItem("perch")).is(FishingApi.FISH) && new ItemStack(fishItem("perch")).is(ItemTags.FISHES)
                    && new ItemStack(fishItem("perch")).is(ItemTags.CAT_FOOD) && new ItemStack(fishItem("perch")).is(ItemTags.WOLF_FOOD)
                    && new ItemStack(fishItem("pike")).is(dev.villagefriends.hearth.HearthApi.FISH)), "Fish are fish, cat and dog treats, and kitchen fish");
            flush(w); c.waitTicks(40);
            c.takeScreenshot("fishing-pond");

            // -- the journal, empty ------------------------------------------------------------------------
            slot(w, 8, new ItemStack(FishingItems.JOURNAL));
            use(c, w, 8);
            c.waitForScreen(JournalScreen.class); c.waitTicks(10);
            c.takeScreenshot("fishing-journal-empty");
            c.runOnClient(client -> client.gui.setScreen(null)); c.waitForScreen(null);

            // -- a perch through the minigame, on a Reinforced Rod with worms and a cork bobber ---------------
            var rod = new ItemStack(FishingItems.REINFORCED_ROD);
            rod.set(Fishing.BAIT, new Fishing.Loaded("villagefriends:bait_worms", 8));
            rod.set(Fishing.TACKLE, new Fishing.Loaded("villagefriends:cork_bobber", Gear.TACKLE_USES));
            slot(w, 0, rod);
            int caughtBefore = w.getServer().computeOnServer(s -> player(w).getStats().getValue(Stats.CUSTOM.get(Stats.FISH_CAUGHT)));
            long fishingXp = rpg ? w.getServer().computeOnServer(s -> skill(player(w), "fishing")) : 0;
            FishingClient.autoplay = true;
            cast(c, w, 0);
            c.takeScreenshot("fishing-cast");
            bite(w, "perch");
            check(playOut(c, w, "fishing-minigame"), "The test angler lands an easy perch");
            waitServer(c, w, s -> has(w, fishItem("perch")), 100);
            check(count(w, fishItem("perch")) == 1, "The perch came to the player");
            check(journalCount(c, "perch") == 1, "and went in the journal (synced to the client)");
            var rodAfter = w.getServer().computeOnServer(s -> player(w).getInventory().getItem(0).copy());
            check(rodAfter.get(Fishing.BAIT).count() == 7, "One worm used: " + rodAfter.get(Fishing.BAIT));
            check(rodAfter.get(Fishing.TACKLE).count() == Gear.TACKLE_USES - 1, "The bobber wore a little");
            check(w.getServer().computeOnServer(s -> player(w).getStats().getValue(Stats.CUSTOM.get(Stats.FISH_CAUGHT))) == caughtBefore + 1, "Counted as a fish caught");
            check(w.getServer().computeOnServer(s -> player(w).fishing == null), "The line was reeled in");

            // -- the journal again: the perch is revealed ------------------------------------------------------
            JournalScreen.show(0, "perch");
            use(c, w, 8);
            c.waitForScreen(JournalScreen.class); c.waitTicks(10);
            c.takeScreenshot("fishing-journal-perch");
            c.runOnClient(client -> client.gui.setScreen(null)); c.waitForScreen(null);

            // -- a legend on an Angler's Rod: a trophy for the wall ---------------------------------------------
            var anglers = new ItemStack(FishingItems.ANGLERS_ROD);
            anglers.set(Fishing.TACKLE, new Fishing.Loaded("villagefriends:cork_bobber", Gear.TACKLE_USES));
            slot(w, 1, anglers);
            boolean landed = false;
            for (int attempt = 0; attempt < 4 && !landed; attempt++) {
                cast(c, w, 1);
                bite(w, "old_whiskers");
                landed = playOut(c, w, attempt == 0 ? "fishing-minigame-legend" : null);
            }
            check(landed, "Old Whiskers landed within four tries");
            waitServer(c, w, s -> has(w, fishItem("old_whiskers")), 100);
            var whiskers = find(w, fishItem("old_whiskers"));
            check(whiskers.get(Fishing.TROPHY) != null && whiskers.getMaxStackSize() == 1, "A legend is a trophy and doesn't stack");
            c.waitTicks(5); c.takeScreenshot("fishing-legend-title");
            BlockPos mount = origin.offset(3, 1, 4);
            w.getServer().runOnServer(s -> {
                level(w).setBlock(mount.south(), Blocks.SPRUCE_PLANKS.defaultBlockState(), 3);
                level(w).setBlock(mount, TrophyMount.BLOCK.defaultBlockState().setValue(TrophyMount.FACING, Direction.NORTH), 3);
                var inv = player(w).getInventory();
                for (int i = 0; i < inv.getContainerSize(); i++) if (inv.getItem(i).is(fishItem("old_whiskers"))) { inv.setItem(2, inv.getItem(i).copy()); if (i != 2) inv.setItem(i, ItemStack.EMPTY); }
            });
            flush(w);
            c.runOnClient(client -> { client.player.getInventory().setSelectedSlot(2);
                client.gameMode.useItemOn(client.player, InteractionHand.MAIN_HAND, new BlockHitResult(Vec3.atCenterOf(mount), Direction.NORTH, mount, false)); });
            flush(w); c.waitTicks(5);
            check(w.getServer().computeOnServer(s -> level(w).getBlockEntity(mount) instanceof TrophyMount.Entity e && e.fish().is(fishItem("old_whiskers"))), "Old Whiskers hangs on the trophy mount");
            w.getServer().runCommand("tp @a " + (origin.getX() + 3.5) + " " + origin.getY() + " " + (origin.getZ() + 1.5) + " 0 10");
            flush(w); c.waitTicks(20);
            c.takeScreenshot("fishing-trophy-mount");
            w.getServer().runCommand("tp @a " + (origin.getX() + .5) + " " + origin.getY() + " " + (origin.getZ() + .5) + " 180 35");

            // -- the minigame off: vanilla fishing, fish from the table --------------------------------------------
            w.getServer().runOnServer(s -> FishingConfig.minigame(false));
            cast(c, w, 0);
            bite(w, "roach");
            waitServer(c, w, s -> player(w).fishing != null && ((FishingHookAccess) player(w).fishing).villagefriends$nibble() > 0, 300);
            use(c, w, 0); c.waitTicks(10); flush(w);
            waitServer(c, w, s -> has(w, fishItem("roach")), 100);
            check(FishingClient.game() == null, "No minigame with it switched off");
            check(count(w, fishItem("roach")) == 1, "Reeled in on the dip: a roach from the fish table");
            w.getServer().runOnServer(s -> FishingConfig.minigame(true));

            // -- a village by the pond: its dock, and its fisherman fishing off it ----------------------------------
            var village = w.getServer().computeOnServer(s -> VillageSettlements.mark(level(w), origin.offset(0, 0, 3), "Pondsend"));
            waitServer(c, w, s -> Docks.dock(level(w), village.id()) != null, 400);
            var dock = w.getServer().computeOnServer(s -> Docks.dock(level(w), village.id()));
            check(dock.spots().size() == 3 && dock.direction() == Direction.NORTH, "A dock out over the pond with three places to fish: " + dock);
            w.getServer().runOnServer(s -> {
                var end = BlockPos.of(dock.spots().get(1));
                check(level(w).getBlockState(end.below()).isFaceSturdy(level(w), end.below(), Direction.UP), "The far end of the deck is solid to stand on");
            });
            w.getServer().runCommand("time set 2500");
            UUID fisher = w.getServer().computeOnServer(s -> {
                var v = new Villager(EntityTypes.VILLAGER, level(w));
                v.setPos(origin.getX() + 3.5, origin.getY(), origin.getZ() + 2.5);
                v.setVillagerData(v.getVillagerData().withProfession(s.registryAccess(), VillagerProfession.FISHERMAN));
                v.setVillagerXp(1); // keeps his trade without a barrel (vanilla resets a brand-new villager's job otherwise)
                level(w).addFreshEntity(v);
                VillageSettlements.identify(v, true);
                return v.getUUID();
            });
            for (int i = 0; ; i++) {
                if (w.getServer().computeOnServer(s -> DockAnglers.angling((Villager) level(w).getEntity(fisher)))) break;
                if (i > 1200) {
                    c.takeScreenshot("fishing-fisherman-failed");
                    throw new AssertionError("The fisherman never started fishing: " + w.getServer().computeOnServer(s -> {
                        var v = (Villager) level(w).getEntity(fisher); var home = VillageSettlements.home(v);
                        return "plan " + ResidentRoutines.plan(v).block() + ", doing " + ResidentRoutines.doing(v) + ", job " + VillageFriends.profession(v)
                                + ", home " + (home == null ? "none" : home.id()) + ", at " + v.position() + ", noAi " + v.isNoAi() + ", dock " + Docks.dock(level(w), village.id());
                    }));
                }
                c.waitTick();
            }
            waitServer(c, w, s -> {
                String st = ((AttachmentTarget) level(w).getEntity(fisher)).getAttached(DockAnglers.STATE);
                return st != null && st.startsWith("wait");
            }, 400);
            w.getServer().runCommand("tp @a " + (origin.getX() + 7.5) + " " + (origin.getY() + 2) + " " + (origin.getZ() - 4.5) + " 110 15");
            flush(w); c.waitTicks(40);
            c.takeScreenshot("fishing-dock-fisherman");
            check(w.getServer().computeOnServer(s -> ResidentRoutines.doing((Villager) level(w).getEntity(fisher))).startsWith("Fishing"), "The fisherman's status says he's fishing");

            // -- contest day: the board, a resident entrant, results and prizes ----------------------------------
            // The dock now runs out in front of the old spot: fish from the bank beside it.
            w.getServer().runCommand("tp @a " + (origin.getX() + 3.5) + " " + origin.getY() + " " + (origin.getZ() + .5) + " 180 35");
            w.getServer().runOnServer(s -> Contests.start(level(w), origin));
            cast(c, w, 0);
            bite(w, "pike");
            check(playOut(c, w, null), "A pike for the contest");
            w.getServer().runOnServer(s -> {
                var v = (Villager) level(w).getEntity(fisher);
                Contests.residentCaught(level(w), v, FishTable.get("roach"), 245);
                var st = Contests.state(level(w), village.id());
                check(st.standings().size() == 2 && st.standings().getFirst().player(), "Two entrants; the player's pike leads: " + st.standings());
            });
            c.waitTicks(130); flush(w);
            c.takeScreenshot("fishing-contest-board");
            // The village's own anglers fish the contest too, so the player may not win: check the prize for their actual place.
            int place = w.getServer().computeOnServer(s -> Contest.place(Contests.state(level(w), village.id()).standings(), player(w).getUUID().toString()));
            check(place >= 1 && place <= 3, "The player placed: " + place);
            var prizes = Contest.prizes(place);
            int[] before = new int[prizes.size()];
            for (int i = 0; i < prizes.size(); i++) before[i] = count(w, FishingItems.stack(prizes.get(i).item(), 1).getItem());
            w.getServer().runOnServer(s -> check(Contests.finish(level(w), origin), "The contest ends: results"));
            c.waitTicks(40); flush(w);
            for (int i = 0; i < prizes.size(); i++)
                check(count(w, FishingItems.stack(prizes.get(i).item(), 1).getItem()) == before[i] + prizes.get(i).count(), Contest.ordinal(place) + " prize collected: " + prizes.get(i));
            check(w.getServer().computeOnServer(s -> Contests.recentWinner(level(w), village.id(), VillageFriends.day(level(w))) != null), "The village remembers who won");
            c.takeScreenshot("fishing-contest-results");

            // -- tall tales and a message in a bottle --------------------------------------------------------------
            w.getServer().runOnServer(s -> {
                var p = player(w); var v = (Villager) level(w).getEntity(fisher);
                String tale = TalkWorld.say(v, p, "tale.legend", Map.of());
                check(tale != null && FishTable.all().stream().anyMatch(f -> f.legendary() && tale.contains(f.name().replace("The ", "the ")) || tale.contains(f.name())), "A tall tale about a legend: " + tale);
                dev.villagefriends.fishing.FishingVillage.heard(p, "rimefin");
                check(Angling.journal(p).heard("rimefin"), "A tale goes in the journal");
                p.getInventory().setItem(3, new ItemStack(FishingItems.BOTTLE));
            });
            int talesBefore = w.getServer().computeOnServer(s -> Angling.journal(player(w)).tales().size());
            use(c, w, 3); c.waitTicks(5); flush(w);
            check(w.getServer().computeOnServer(s -> Angling.journal(player(w)).tales().size()) == talesBefore + 1, "The note in the bottle tells another tale");
            JournalScreen.show(2, "rimefin");
            use(c, w, 8);
            c.waitForScreen(JournalScreen.class); c.waitTicks(10);
            c.takeScreenshot("fishing-journal-tale");
            c.runOnClient(client -> client.gui.setScreen(null)); c.waitForScreen(null);

            // -- a fish dish: pickled herring at the prep table ---------------------------------------------------------
            BlockPos prep = origin.offset(-3, 0, 3);
            w.getServer().runOnServer(s -> {
                level(w).setBlock(prep, HearthBlocks.PREP_TABLE.defaultBlockState().setValue(StationBlock.FACING, Direction.NORTH), 3);
                var inv = player(w).getInventory();
                inv.setItem(27, new ItemStack(fishItem("herring"), 2)); inv.setItem(28, new ItemStack(HearthItems.get("onion")));
                inv.setItem(29, new ItemStack(Items.SUGAR)); inv.setItem(30, new ItemStack(Items.GLASS_BOTTLE));
                inv.setItem(31, inv.getItem(6).copy()); inv.setItem(6, ItemStack.EMPTY);
            });
            w.getServer().runCommand("tp @a " + (origin.getX() - 2.5) + " " + origin.getY() + " " + (origin.getZ() + 1.5) + " 90 30");
            flush(w); c.waitTicks(5);
            c.runOnClient(client -> { client.player.getInventory().setSelectedSlot(6);
                client.gameMode.useItemOn(client.player, InteractionHand.MAIN_HAND, new BlockHitResult(Vec3.atCenterOf(prep), Direction.UP, prep, false)); });
            flush(w); c.waitForScreen(StationScreen.class); flush(w); c.waitTicks(5);
            c.runOnClient(client -> {
                var menu = (StationMenu) client.player.containerMenu;
                int index = -1;
                for (int i = 0; i < menu.opening.book().size(); i++) if (menu.opening.book().get(i).id().equals("villagefriends:pickled_herring")) index = i;
                check(index >= 0, "The prep table's book has pickled herring");
                client.gameMode.handleInventoryButtonClick(menu.containerId, index);
            });
            flush(w); c.waitTicks(20 * 6 + 20); flush(w);
            c.takeScreenshot("fishing-pickled-herring");
            c.runOnClient(client -> { var menu = (StationMenu) client.player.containerMenu;
                client.gameMode.handleContainerInput(menu.containerId, menu.station.output(), 0, ContainerInput.QUICK_MOVE, client.player); });
            flush(w); c.waitTicks(5); flush(w);
            c.runOnClient(client -> client.player.closeContainer()); c.waitForScreen(null);
            check(count(w, HearthItems.get("pickled_herring")) == 2, "Two jars of pickled herring from the prep table");

            // -- pets love fish -------------------------------------------------------------------------------------------
            check(dev.villagefriends.pet.PetKeeping.treatLine(new dev.villagefriends.pet.PetProfile("r", "Wren", "Biscuit", dev.villagefriends.pet.PetKeeping.DOG, "loyal", "fetch",
                    "minecraft:cooked_beef", 0, 0, "", Map.of()), "villagefriends:perch", true, "perch").contains("wolfs it down"), "Dogs love a fish treat");

            // -- the optional ties ------------------------------------------------------------------------------------------
            if (rpg) check(w.getServer().computeOnServer(s -> skill(player(w), "fishing")) > fishingXp + 150, "With the RPG add-on, landing a legend trains Fishing a lot");
            if (nsv) {
                cast(c, w, 0);
                boolean hauled = w.getServer().computeOnServer(s -> FishingCompat.haul(player(w), player(w).fishing));
                check(hauled, "With Not-So-Vanilla Mobs a Brineclaw can be hauled out of the water");
                check(w.getServer().computeOnServer(s -> !level(w).getEntitiesOfClass(net.minecraft.world.entity.Mob.class, player(w).getBoundingBox().inflate(24),
                        m -> BuiltInRegistries.ENTITY_TYPE.getKey(m.getType()).equals(FishingCompat.BRINECLAW)).isEmpty()), "and there it is");
                c.waitTicks(20); c.takeScreenshot("fishing-brineclaw");
            }
            FishingClient.autoplay = false;
            LOGGER.info("FISHING PASSED{}: minigame catch with bait and tackle, journal silhouette to revealed, a legend as a trophy on the wall, vanilla mode,"
                    + " a village dock and its fisherman, a contest with scoreboard and prizes, tall tales and a bottle, pickled herring, pets{}",
                    rpg ? " (with the RPG add-on)" : "", nsv ? ", a Brineclaw" : "");
        }
    }
}
