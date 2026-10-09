package dev.villagefriends;

import static dev.villagefriends.VillageFriends.*;

import dev.villagefriends.client.FriendshipScreen;
import dev.villagefriends.client.StationScreen;
import dev.villagefriends.hearth.Cookbook;
import dev.villagefriends.hearth.Dishes;
import dev.villagefriends.hearth.Hearth;
import dev.villagefriends.hearth.HearthApi;
import dev.villagefriends.hearth.HearthBlocks;
import dev.villagefriends.hearth.HearthItems;
import dev.villagefriends.hearth.HearthVillage;
import dev.villagefriends.hearth.HomeMeals;
import dev.villagefriends.hearth.RecipeCardItem;
import dev.villagefriends.hearth.Station;
import dev.villagefriends.hearth.StationBlock;
import dev.villagefriends.hearth.StationBlockEntity;
import dev.villagefriends.hearth.StationMenu;
import dev.villagefriends.hearth.WellFed;
import dev.villagefriends.routine.Routine;
import dev.villagefriends.tavern.Patronage;
import java.util.List;
import java.util.UUID;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.fabricmc.loader.api.FabricLoader;
import net.minecraft.client.gui.screens.inventory.MerchantScreen;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.npc.villager.VillagerProfession;
import net.minecraft.world.inventory.ContainerInput;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.CampfireBlock;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.EntityHitResult;
import net.minecraft.world.phys.Vec3;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Hearth & Harvest in a real client: the three stations placed and photographed; a dish cooked at each one
 * through its screen and recipe book (pot on a lit campfire, oven on coal, prep table); Well Fed from eating
 * (tiers, the dish the mod already had, slower hunger); a family recipe that won't cook until its recipe
 * card is learned; a favorite-dish gift; a Friend handing over their family recipe; the tavern keeper selling
 * the dish of the day (and changing it the next day); and a resident eating supper with the dish in hand.
 * Runs with or without the RPG add-on ({@code -Ptests=HearthGameTest}).
 */
@SuppressWarnings("UnstableApiUsage")
public final class HearthGameTest implements FabricClientGameTest {
    private static final Logger LOGGER = LoggerFactory.getLogger("HearthGameTest");
    private static void check(boolean ok, String reason) { if (!ok) throw new AssertionError(reason); }
    private static ServerLevel level(TestSingleplayerContext w) { return w.getConnection().getServerLevel(); }
    private static ServerPlayer player(TestSingleplayerContext w) { return w.getConnection().getServerPlayer(); }
    private static void flush(TestSingleplayerContext w) { w.getConnection().waitForServerboundPackets(); w.getConnection().waitForClientboundPackets(); }
    private static Villager villager(TestSingleplayerContext w, UUID id) { return (Villager) level(w).getEntity(id); }
    private static Item item(String path) { return HearthItems.get(path); }
    private static StationBlockEntity station(TestSingleplayerContext w, BlockPos pos) { return (StationBlockEntity) level(w).getBlockEntity(pos); }
    private static int count(TestSingleplayerContext w, Item item) {
        return w.getServer().computeOnServer(s -> { var inv = player(w).getInventory(); int n = 0;
            for (int i = 0; i < inv.getContainerSize(); i++) if (inv.getItem(i).is(item)) n += inv.getItem(i).getCount(); return n; });
    }
    private static void give(TestSingleplayerContext w, ItemStack... stacks) {
        w.getServer().runOnServer(s -> { for (var stack : stacks) player(w).getInventory().add(stack); });
    }
    /** A real right click with an empty hand: opens the station's screen. */
    private static void open(ClientGameTestContext c, TestSingleplayerContext w, BlockPos pos) {
        c.runOnClient(client -> {
            client.gui.setScreen(null);
            client.player.getInventory().setSelectedSlot(8);
            client.gameMode.useItemOn(client.player, InteractionHand.MAIN_HAND, new BlockHitResult(Vec3.atCenterOf(pos), Direction.UP, pos, false));
        });
        flush(w); c.waitForScreen(StationScreen.class); flush(w); c.waitTicks(5);
    }
    /** Presses a recipe in the open screen's book, as a click would. */
    private static void fill(ClientGameTestContext c, TestSingleplayerContext w, String recipe) {
        c.runOnClient(client -> {
            var menu = (StationMenu) client.player.containerMenu;
            int index = -1;
            for (int i = 0; i < menu.opening.book().size(); i++) if (menu.opening.book().get(i).id().equals(recipe)) index = i;
            check(index >= 0, "The recipe book lists " + recipe);
            client.gameMode.handleInventoryButtonClick(menu.containerId, index);
        });
        flush(w); c.waitTicks(3); flush(w);
    }
    private static void takeOutput(ClientGameTestContext c, TestSingleplayerContext w) {
        c.runOnClient(client -> {
            var menu = (StationMenu) client.player.containerMenu;
            client.gameMode.handleContainerInput(menu.containerId, menu.station.output(), 0, ContainerInput.QUICK_MOVE, client.player);
        });
        flush(w); c.waitTicks(3); flush(w);
    }
    private static void close(ClientGameTestContext c) { c.runOnClient(client -> client.player.closeContainer()); c.waitForScreen(null); }
    private static void talk(ClientGameTestContext c, TestSingleplayerContext w, UUID id) {
        w.getConnection().waitForClientboundEntityUpdates(EntityTypes.VILLAGER);
        int eid = w.getServer().computeOnServer(s -> villager(w, id).getId());
        c.runOnClient(client -> { client.gui.setScreen(null); client.player.getInventory().setSelectedSlot(0); var e = client.level.getEntity(eid);
            client.gameMode.interact(client.player, e, new EntityHitResult(e), InteractionHand.MAIN_HAND); });
        c.waitForScreen(FriendshipScreen.class); flush(w); c.waitTicks(10);
    }
    private static UUID resident(TestSingleplayerContext w, double dx, double dz, ResourceKey<VillagerProfession> job, boolean ai) {
        return w.getServer().computeOnServer(s -> {
            var p = player(w);
            var v = new Villager(EntityTypes.VILLAGER, level(w));
            v.setPos(p.getX() + dx, p.getY(), p.getZ() + dz); v.setNoAi(!ai);
            v.setYRot(180); v.yBodyRot = v.yHeadRot = 180;
            v.setVillagerData(v.getVillagerData().withProfession(s.registryAccess(), job));
            level(w).addFreshEntity(v);
            VillageSettlements.identify(v, true);
            return v.getUUID();
        });
    }

    /** The RPG add-on's Cooking experience, read without depending on the add-on. */
    private static long rpgCooking(ServerPlayer p) {
        try {
            var sheet = Class.forName("dev.villagefriends.rpg.Rpg").getMethod("sheet", net.minecraft.world.entity.player.Player.class).invoke(null, p);
            @SuppressWarnings("unchecked") var skills = (java.util.Map<String, Long>) sheet.getClass().getMethod("skills").invoke(sheet);
            return skills.getOrDefault("cooking", 0L);
        } catch (ReflectiveOperationException e) { throw new AssertionError("RPG sheet unreadable", e); }
    }

    @Override public void runTest(ClientGameTestContext c) {
        c.getInput().resizeWindow(1280, 800); c.runOnClient(client -> { client.options.guiScale().set(2); client.resizeGui(); });
        boolean rpg = FabricLoader.getInstance().isModLoaded("villagefriends_rpg");
        try (var w = c.worldBuilder().create()) {
            w.getConnection().waitForChunksRender();
            for (var cmd : List.of("gamemode creative @a", "time set 6000", "gamerule advance_time false", "gamerule advance_weather false",
                    "gamerule spawn_mobs false", "weather clear", "tp @a ~ ~ ~ 0 15"))
                w.getServer().runCommand(cmd);
            // A plank kitchen floor: a cooking pot on a lit campfire, a clay oven and a prep table, fronts to the player.
            BlockPos[] at = w.getServer().computeOnServer(s -> {
                var level = level(w); var origin = player(w).blockPosition();
                for (int x = -8; x <= 8; x++) for (int z = -3; z <= 10; z++) {
                    level.setBlock(origin.offset(x, -1, z), Blocks.SPRUCE_PLANKS.defaultBlockState(), 3);
                    for (int y = 0; y < 4; y++) level.setBlock(origin.offset(x, y, z), Blocks.AIR.defaultBlockState(), 3);
                }
                var fire = origin.offset(-2, 0, 3);
                level.setBlock(fire, Blocks.CAMPFIRE.defaultBlockState().setValue(CampfireBlock.LIT, true), 3);
                BlockPos pot = fire.above(), oven = origin.offset(0, 0, 3), prep = origin.offset(2, 0, 3);
                level.setBlock(pot, HearthBlocks.COOKING_POT.defaultBlockState().setValue(StationBlock.FACING, Direction.NORTH), 3);
                level.setBlock(oven, HearthBlocks.CLAY_OVEN.defaultBlockState().setValue(StationBlock.FACING, Direction.NORTH), 3);
                level.setBlock(prep, HearthBlocks.PREP_TABLE.defaultBlockState().setValue(StationBlock.FACING, Direction.NORTH), 3);
                for (var pos : List.of(pot, oven, prep)) check(level.getBlockEntity(pos) instanceof StationBlockEntity, "Every station has its block entity");
                check(StationBlockEntity.heated(level, pot), "A lit campfire heats the pot above it");
                return new BlockPos[]{pot, oven, prep};
            });
            BlockPos pot = at[0], oven = at[1], prep = at[2];
            int recipes = w.getServer().computeOnServer(s -> Cookbook.all().size());
            check(recipes >= 65, "The station recipes loaded from the data pack: " + recipes);
            check(w.getServer().computeOnServer(s -> Cookbook.get("villagefriends:boar_stew") == null) || FabricLoader.getInstance().isModLoaded("nsvmobs"),
                    "Not-So-Vanilla Mobs recipes only load with that mod");
            flush(w); c.waitTicks(30);
            c.takeScreenshot("hearth-stations");

            // -- the cooking pot: onion pottage, filled from the recipe book -----------------------------
            give(w, new ItemStack(item("onion"), 4), new ItemStack(item("barley"), 2), new ItemStack(item("herbs"), 2), new ItemStack(Items.BOWL, 2));
            open(c, w, pot);
            fill(c, w, "villagefriends:onion_pottage");
            w.getServer().runOnServer(s -> {
                var be = station(w, pot);
                check(be.getItem(Station.GRID).is(Items.BOWL), "The book put a bowl in the pot's vessel slot");
                int onions = 0; for (int i = 0; i < Station.GRID; i++) if (be.getItem(i).is(item("onion"))) onions += be.getItem(i).getCount();
                check(onions == 2, "and one batch of ingredients in the grid: " + onions + " onions");
            });
            c.waitTicks(60); flush(w);
            w.getServer().runOnServer(s -> {
                check(level(w).getBlockState(pot).getValue(StationBlock.LIT), "The pot bubbles while it cooks");
                check(level(w).getBlockState(pot).getValue(StationBlock.FILLED), "and shows a stew inside");
                check(station(w, pot).data().get(StationBlockEntity.DATA_PROGRESS) > 0, "The pot is cooking");
            });
            c.takeScreenshot("hearth-pot-screen");
            close(c);
            c.runOnClient(client -> { client.player.setYRot(32); client.player.setXRot(18); });
            c.waitTicks(30); c.takeScreenshot("hearth-pot-steam");
            c.waitTicks(150); flush(w);
            check(w.getServer().computeOnServer(s -> station(w, pot).getItem(Station.POT.output()).is(item("onion_pottage"))), "Ten seconds later: a bowl of onion pottage");
            open(c, w, pot); takeOutput(c, w); close(c);
            check(count(w, item("onion_pottage")) == 1, "Taken out of the pot");
            if (rpg) check(w.getServer().computeOnServer(s -> rpgCooking(player(w))) > 0, "With the RPG add-on, taking it out trains Cooking");

            // -- the clay oven: a wastel loaf on coal ------------------------------------------------------
            give(w, new ItemStack(item("flour"), 3), new ItemStack(Items.EGG, 1));
            open(c, w, oven);
            fill(c, w, "villagefriends:wastel");
            w.getServer().runOnServer(s -> station(w, oven).setItem(Station.GRID, new ItemStack(Items.COAL)));
            c.waitTicks(60); flush(w);
            w.getServer().runOnServer(s -> {
                check(level(w).getBlockState(oven).getValue(StationBlock.LIT), "The oven burns its coal");
                check(station(w, oven).data().get(StationBlockEntity.DATA_PROGRESS) > 0, "and bakes");
            });
            c.takeScreenshot("hearth-oven-screen");
            close(c); c.runOnClient(client -> { client.player.setYRot(0); client.player.setXRot(25); });
            c.waitTicks(10); c.takeScreenshot("hearth-oven-lit");
            c.waitTicks(200); flush(w);
            check(w.getServer().computeOnServer(s -> station(w, oven).getItem(Station.OVEN.output()).is(item("wastel"))), "A wastel loaf comes out of the oven");

            // -- the prep table: herb salad --------------------------------------------------------------
            give(w, new ItemStack(item("cabbage")), new ItemStack(item("herbs")), new ItemStack(item("leek")), new ItemStack(item("onion")), new ItemStack(Items.BOWL));
            open(c, w, prep);
            fill(c, w, "villagefriends:herb_salad");
            c.waitTicks(80); flush(w);
            check(w.getServer().computeOnServer(s -> station(w, prep).getItem(Station.PREP.output()).is(item("herb_salad"))), "The prep table makes a herb salad");
            takeOutput(c, w);
            c.takeScreenshot("hearth-prep-screen");
            close(c);
            check(count(w, item("herb_salad")) == 1, "Taken off the prep table");

            // -- Well Fed ----------------------------------------------------------------------------------
            w.getServer().runOnServer(s -> {
                var p = player(w); var level = level(w);
                new ItemStack(item("onion_pottage")).finishUsingItem(level, p);
                var effect = p.getEffect(WellFed.EFFECT);
                check(effect != null && effect.getAmplifier() == 0, "Onion pottage gives Well Fed I");
                int expected = Dishes.get("villagefriends:onion_pottage").buff() * 20;
                check(rpg || Math.abs(effect.getDuration() - expected) <= 2, "for its table time: " + effect.getDuration() + " vs " + expected);
                new ItemStack(item("beef_stew")).finishUsingItem(level, p);
                check(p.getEffect(WellFed.EFFECT).getAmplifier() == 1, "Beef stew replaces it with Well Fed II");
                int before = p.getEffect(WellFed.EFFECT).getDuration();
                new ItemStack(item("beef_stew")).finishUsingItem(level, p);
                check(p.getEffect(WellFed.EFFECT).getDuration() <= before + 2 && p.getEffect(WellFed.EFFECT).getAmplifier() == 1, "A second helping doesn't stack");
                p.removeEffect(WellFed.EFFECT);
                new ItemStack(BuiltInRegistries.ITEM.getValue(Identifier.parse("villagefriends:hearty_stew"))).finishUsingItem(level, p);
                check(p.hasEffect(WellFed.EFFECT), "The village's old hearty stew now gives Well Fed too");
                var fine = HearthApi.makeFine(new ItemStack(item("onion_pottage")));
                check(fine.getHoverName().getString().startsWith("Fine "), "A fine dish says so: " + fine.getHoverName().getString());
                check(WellFed.exhaustion(p, 4F) < 4F, "Well Fed slows hunger");
            });
            c.waitTicks(5); c.takeScreenshot("hearth-well-fed");

            // -- a family recipe: locked until its card is learned (in survival) ---------------------------
            w.getServer().runCommand("gamemode survival @a");
            give(w, new ItemStack(item("onion")), new ItemStack(item("cabbage")), new ItemStack(item("leek")), new ItemStack(item("garlic")),
                    new ItemStack(Items.CARROT), new ItemStack(Items.POTATO), new ItemStack(Items.BOWL));
            open(c, w, pot);
            c.runOnClient(client -> {
                var menu = (StationMenu) client.player.containerMenu;
                var entry = menu.opening.book().stream().filter(e -> e.id().equals("villagefriends:harvest_stew")).findFirst().orElseThrow();
                check(entry.secret() && !entry.known(), "Harvest stew is a sealed family recipe in the book");
            });
            c.takeScreenshot("hearth-family-recipe-sealed");
            close(c);
            w.getServer().runOnServer(s -> {
                var be = station(w, pot); int slot = 0;
                for (var id : List.of("villagefriends:onion", "villagefriends:cabbage", "villagefriends:leek", "villagefriends:garlic", "minecraft:carrot", "minecraft:potato"))
                    be.setItem(slot++, new ItemStack(BuiltInRegistries.ITEM.getValue(Identifier.parse(id))));
                be.setItem(Station.GRID, new ItemStack(Items.BOWL));
            });
            c.waitTicks(40); flush(w);
            check(w.getServer().computeOnServer(s -> station(w, pot).data().get(StationBlockEntity.DATA_PROGRESS) == 0), "It won't cook for someone who doesn't know it");
            w.getServer().runOnServer(s -> {
                var p = player(w);
                p.setItemInHand(InteractionHand.MAIN_HAND, RecipeCardItem.of("villagefriends:harvest_stew"));
                p.getMainHandItem().use(level(w), p, InteractionHand.MAIN_HAND);
                check(Hearth.known(p).contains("villagefriends:harvest_stew"), "The recipe card teaches the family recipe");
                check(p.getMainHandItem().isEmpty(), "and is used up");
            });
            open(c, w, pot); c.waitTicks(30); flush(w);
            check(w.getServer().computeOnServer(s -> station(w, pot).data().get(StationBlockEntity.DATA_PROGRESS) > 0), "Now it cooks");
            c.takeScreenshot("hearth-family-recipe-cooking");
            close(c);
            w.getServer().runCommand("gamemode creative @a");

            // -- a favorite dish as a gift ---------------------------------------------------------------
            UUID farmer = resident(w, 0, 5.5, VillagerProfession.FARMER, false), friend = resident(w, -3.5, 4.8, VillagerProfession.LIBRARIAN, false);
            String favorite = w.getServer().computeOnServer(s -> {
                var v = villager(w, farmer); var fav = HearthVillage.favorite(v);
                var p = player(w); p.getInventory().setSelectedSlot(0);
                p.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(BuiltInRegistries.ITEM.getValue(Identifier.parse(fav.id()))));
                return fav.id();
            });
            talk(c, w, farmer);
            int before = w.getServer().computeOnServer(s -> state(villager(w, farmer), player(w)).points());
            c.clickScreenButton("Give gift"); flush(w); c.waitTicks(30);
            int after = w.getServer().computeOnServer(s -> state(villager(w, farmer), player(w)).points());
            check(after - before >= 18, "Their favorite dish (" + favorite + ") is the best gift there is: +" + (after - before));
            check(w.getServer().computeOnServer(s -> bond(villager(w, farmer), player(w)).memories().stream().anyMatch(m -> m.contains("my favorite"))), "and they remember it");
            c.takeScreenshot("hearth-gift-favorite");
            c.clickScreenButton("Goodbye"); c.waitForScreen(null);

            // -- a Friend hands over their family recipe --------------------------------------------------
            w.getServer().runOnServer(s -> {
                var v = villager(w, friend); var p = player(w);
                save(v, p, new FriendshipState(60, -1, -1, 0, ""));
                saveBond(v, p, bond(v, p).flag("shared_experience"));
            });
            talk(c, w, friend);
            String family = w.getServer().computeOnServer(s -> {
                var inv = player(w).getInventory();
                for (int i = 0; i < inv.getContainerSize(); i++) if (inv.getItem(i).is(HearthItems.RECIPE_CARD)) return inv.getItem(i).get(Hearth.RECIPE);
                return null;
            });
            check(family != null && w.getServer().computeOnServer(s -> Cookbook.get(family).secret()), "A Friend gives you a family recipe card: " + family);
            c.takeScreenshot("hearth-family-recipe-card");
            c.clickScreenButton("Goodbye"); c.waitForScreen(null);

            // -- the tavern keeper sells the cook's dish of the day ----------------------------------------
            UUID keeper = resident(w, 3.5, 4.8, ResourceKey.create(Registries.VILLAGER_PROFESSION, VillageBlocks.id("tavern_keeper")), false);
            String special = w.getServer().computeOnServer(s -> {
                var v = villager(w, keeper); var p = player(w);
                String dish = Patronage.dishOfTheDay(day(level(w)));
                check(Dishes.get(dish) != null && Dishes.get(dish).meal("tavern"), "The dish of the day comes from the dish table: " + dish);
                v.setTradingPlayer(p); v.setTradingPlayer(null);
                var item = BuiltInRegistries.ITEM.getValue(Identifier.parse(dish));
                check(v.getOffers().stream().anyMatch(o -> o.getResult().is(item)), "The tavern keeper sells it");
                return dish;
            });
            talk(c, w, keeper);
            c.clickScreenButton("Trade"); c.waitForScreen(MerchantScreen.class); c.waitTicks(10);
            c.takeScreenshot("hearth-dish-of-the-day");
            c.runOnClient(client -> client.player.closeContainer()); c.waitForScreen(null);
            w.getServer().runCommand("time add 24000"); flush(w);
            w.getServer().runOnServer(s -> {
                var v = villager(w, keeper); var p = player(w);
                v.setTradingPlayer(p); v.setTradingPlayer(null);
                String next = Patronage.dishOfTheDay(day(level(w)));
                var old = BuiltInRegistries.ITEM.getValue(Identifier.parse(special)); var now = BuiltInRegistries.ITEM.getValue(Identifier.parse(next));
                check(v.getOffers().stream().anyMatch(o -> o.getResult().is(now)), "Tomorrow's dish goes on sale");
                check(next.equals(special) || v.getOffers().stream().noneMatch(o -> o.getResult().is(old) && o.getMaxUses() == HearthVillage.SPECIAL_USES), "and yesterday's comes off");
            });

            // -- supper at home: a resident eats a real dish, dish in hand ---------------------------------
            UUID diner = resident(w, -4.5, 4.0, VillagerProfession.FARMER, true);
            long supper = w.getServer().computeOnServer(s -> {
                var day = ResidentRoutines.day(villager(w, diner));
                for (int t = Routine.at(15, 0); t < Routine.at(22, 0); t += 100) if (day.at(t) == Routine.Block.SUPPER) return (long) t + 200;
                return -1L;
            });
            check(supper > 0, "The diner has a supper in their day");
            w.getServer().runCommand("time set " + (w.getServer().computeOnServer(s -> day(level(w))) * 24000 + supper));
            String eating = null;
            for (int i = 0; i < 20 && eating == null; i++) {
                c.waitTicks(20); flush(w);
                eating = w.getServer().computeOnServer(s -> ((net.fabricmc.fabric.api.attachment.v1.AttachmentTarget) villager(w, diner)).getAttached(HomeMeals.STATE));
            }
            check(eating != null && eating.startsWith("eat:"), "At supper the resident eats a dish: " + eating);
            String dishEaten = eating.substring(4);
            check(Dishes.get(dishEaten) != null && Dishes.get(dishEaten).meal("supper"), "a supper dish: " + dishEaten);
            int dinerEntity = w.getServer().computeOnServer(s -> villager(w, diner).getId());
            c.waitTicks(10);
            c.runOnClient(client -> check(((net.fabricmc.fabric.api.attachment.v1.AttachmentTarget) client.level.getEntity(dinerEntity)).getAttached(HomeMeals.STATE) != null,
                    "Clients see what they're eating"));
            c.runOnClient(client -> { client.player.setYRot(46); client.player.setXRot(12); });
            c.waitTicks(20); c.takeScreenshot("hearth-home-meal");

            // -- a farmstead out in the wild grows Hearth crops in its fields ------------------------------
            int fx = 240, gy = w.getServer().computeOnServer(s -> player(w).blockPosition().getY());
            w.getServer().runOnServer(s -> { for (int cx = (fx - 32) >> 4; cx <= (fx + 32) >> 4; cx++) for (int cz = -3; cz <= 3; cz++) level(w).getChunk(cx, cz); });
            w.getServer().runCommand("place structure villagefriends:homestead_farmstead " + fx + " " + gy + " 0");
            c.waitTicks(20);
            int[] fields = w.getServer().computeOnServer(s -> {
                var hearth = net.minecraft.tags.TagKey.create(Registries.BLOCK, Hearth.id("hearth/crops"));
                int ours = 0, vanilla = 0, sx = 0, sz = 0;
                for (var pos : BlockPos.betweenClosed(fx - 30, gy - 4, -30, fx + 30, gy + 4, 30)) {
                    var state = level(w).getBlockState(pos);
                    if (state.is(hearth)) { ours++; sx += pos.getX(); sz += pos.getZ(); } else if (state.is(net.minecraft.tags.BlockTags.CROPS)) vanilla++;
                }
                return new int[]{ours, vanilla, ours == 0 ? fx : sx / ours, ours == 0 ? 0 : sz / ours};
            });
            check(fields[0] > 0 && fields[1] > 0, "The farmstead's fields mix Hearth crops in with the wheat: " + fields[0] + " Hearth, " + fields[1] + " vanilla");
            LOGGER.info("Farmstead fields: {} Hearth crops, {} vanilla crops", fields[0], fields[1]);
            // Hover over the field, looking down at it.
            w.getServer().runOnServer(s -> { var p = player(w); p.getAbilities().flying = true; p.onUpdateAbilities(); });
            w.getServer().runCommand("tp @a " + (fields[2] + .5) + " " + (gy + 7) + " " + (fields[3] - 6.5) + " 0 42");
            c.waitTicks(60); c.takeScreenshot("hearth-farmstead-fields");
        }
        LOGGER.info("HEARTH PASSED{}: pot, oven and prep table cooking through the recipe book, Well Fed tiers and no stacking, a family recipe locked then learned, "
                + "a favorite-dish gift, a Friend's recipe card, the tavern keeper's dish of the day, supper at home, Hearth crops in a farmstead's fields", rpg ? " (with the RPG add-on)" : "");
    }
}
