package dev.villagefriends;

import static dev.villagefriends.VillageFriends.*;

import dev.villagefriends.client.FriendshipScreen;
import dev.villagefriends.routine.Routine;
import dev.villagefriends.routine.RoutineBrain;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.GlobalPos;
import net.minecraft.core.component.DataComponents;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.ai.memory.MemoryModuleType;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.npc.villager.VillagerProfession;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.EntityHitResult;
import net.minecraft.world.phys.Vec3;

/**
 * The workstations in a real world: every redesigned model placed and photographed, each station's use
 * for players (stove, barrel, tap, press, easel, sawmill, sewing table, archives, music stand, dummy,
 * target), residents working at them (the cook's dish of the day, the painter's canvas, the tavern
 * keeper's restocking, a knight's training), and residents following their routine through the day and
 * the weather.
 */
@SuppressWarnings("UnstableApiUsage")
public final class WorkstationGameTest implements FabricClientGameTest {
    private static void check(boolean ok, String reason) { if (!ok) throw new AssertionError(reason); }
    private static ServerLevel level(TestSingleplayerContext w) { return w.getConnection().getServerLevel(); }
    private static ServerPlayer player(TestSingleplayerContext w) { return w.getConnection().getServerPlayer(); }
    private static void flush(TestSingleplayerContext w) { w.getConnection().waitForServerboundPackets(); w.getConnection().waitForClientboundPackets(); }
    /** A real right click on the station with this item in hand. */
    private static void use(TestSingleplayerContext w, BlockPos pos, ItemStack held) {
        // The last hotbar slot is the "hand"; rewards land in the earlier slots and are never overwritten.
        var p = player(w); p.getInventory().setSelectedSlot(8); p.setItemInHand(InteractionHand.MAIN_HAND, held);
        p.gameMode.useItemOn(p, level(w), p.getMainHandItem(), InteractionHand.MAIN_HAND, new BlockHitResult(Vec3.atCenterOf(pos), Direction.NORTH, pos, false));
    }
    private static int count(ServerPlayer p, net.minecraft.world.item.Item item) {
        int n = 0; var inv = p.getInventory();
        for (int i = 0; i < inv.getContainerSize(); i++) if (inv.getItem(i).is(item)) n += inv.getItem(i).getCount();
        return n;
    }
    private static WorkstationBlockEntity station(TestSingleplayerContext w, BlockPos pos) { return (WorkstationBlockEntity) level(w).getBlockEntity(pos); }

    @Override public void runTest(ClientGameTestContext c) {
        c.getInput().resizeWindow(1600, 900); c.runOnClient(client -> { client.options.guiScale().set(2); client.resizeGui(); });
        var names = VillageBlocks.stations();
        var positions = new ArrayList<BlockPos>();
        try (var w = c.worldBuilder().create()) {
            w.getConnection().waitForChunksRender();
            w.getServer().runCommand("time set 6000"); w.getServer().runCommand("gamerule advance_time false"); w.getServer().runCommand("gamerule advance_weather false");
            w.getServer().runCommand("gamerule spawn_mobs false"); w.getServer().runCommand("weather clear"); w.getServer().runCommand("gamemode creative @a");
            // A plank floor with every workstation in a row, fronts facing the player.
            w.getServer().runOnServer(s -> {
                var level = level(w); var p = player(w); var origin = p.blockPosition();
                for (int x = -14; x <= 14; x++) for (int z = -2; z <= 9; z++) {
                    level.setBlock(origin.offset(x, -1, z), Blocks.SPRUCE_PLANKS.defaultBlockState(), 3);
                    for (int y = 0; y < 4; y++) level.setBlock(origin.offset(x, y, z), Blocks.AIR.defaultBlockState(), 3);
                }
                for (int i = 0; i < names.size(); i++) {
                    var pos = origin.offset(i * 2 - 10, 0, 6); positions.add(pos);
                    level.setBlock(pos, VillageBlocks.get(names.get(i)).defaultBlockState(), 3);
                    check(level.getBlockEntity(pos) instanceof WorkstationBlockEntity, "Every workstation has its block entity: " + names.get(i));
                }
                VillageSettlements.mark(level, origin.offset(0, 0, 2), "Thistlewick");
                p.teleportTo(level, origin.getX() + .5, origin.getY() + 1.5, origin.getZ() - 1.5, java.util.Set.of(), 0, 18, true);
            });
            flush(w); c.waitTicks(40);
            c.takeScreenshot("workstations-row");
            // Close-ups, left half and right half.
            for (int half = 0; half < 2; half++) {
                int from = half * 6;
                w.getServer().runOnServer(s -> {
                    var a = positions.get(from); var b = positions.get(Math.min(positions.size() - 1, from + 5));
                    player(w).teleportTo(level(w), (a.getX() + b.getX()) / 2.0 + .5, a.getY() + 1.2, a.getZ() - 5.2, java.util.Set.of(), 0, 14, true);
                });
                flush(w); c.waitTicks(20);
                c.takeScreenshot("workstations-closeup-" + (half + 1));
            }
            // From behind, to see the backs.
            w.getServer().runOnServer(s -> { var mid = positions.get(5); player(w).teleportTo(level(w), mid.getX() + .5, mid.getY() + 2.2, mid.getZ() + 6.5, java.util.Set.of(), 180, 18, true); });
            flush(w); c.waitTicks(20); c.takeScreenshot("workstations-backs");

            w.getServer().runCommand("gamemode survival @a");
            BlockPos stove = positions.get(names.indexOf("kitchen_stove")), barrel = positions.get(names.indexOf("drinks_barrel")), tap = positions.get(names.indexOf("tap_stand")),
                    press = positions.get(names.indexOf("alchemical_press")), easel = positions.get(names.indexOf("easel_canvas")), music = positions.get(names.indexOf("music_stand")),
                    sewing = positions.get(names.indexOf("sewing_table")), saw = positions.get(names.indexOf("sawmill")), archives = positions.get(names.indexOf("archives")),
                    dummy = positions.get(names.indexOf("training_dummy")), target = positions.get(names.indexOf("archery_target"));
            w.getServer().runOnServer(s -> {
                var p = player(w); var level = level(w);
                p.teleportTo(level, stove.getX() + .5, stove.getY(), stove.getZ() - 2, java.util.Set.of(), 0, 20, true);
                // Stove: raw food goes on, one at a time, and the fire lights.
                use(w, stove, new ItemStack(Items.BEEF, 2));
                check(p.getMainHandItem().getCount() == 1 && station(w, stove).items().get(0).is(Items.BEEF), "The stove takes one piece of raw food");
                // Barrel and tap: press and brew, then pour a mug.
                use(w, barrel, new ItemStack(Items.APPLE, 1)); check(station(w, barrel).stock() == 2, "An apple presses two mugs of cider");
                use(w, barrel, new ItemStack(VillageItems.get("empty_coffee_mug")));
                check(count(p, VillageItems.get("mug_of_cider")) == 1 && station(w, barrel).stock() == 1, "An empty mug is filled with cider");
                use(w, tap, new ItemStack(Items.COCOA_BEANS, 1)); use(w, tap, new ItemStack(VillageItems.get("empty_coffee_mug")));
                check(count(p, VillageItems.get("steaming_coffee_mug")) == 1, "The tap pours coffee");
                // Press: three herbs make a tonic.
                for (int i = 0; i < 3; i++) use(w, press, new ItemStack(Items.POPPY));
                check(station(w, press).stock() == 3, "Three flowers in the press");
                use(w, press, new ItemStack(Items.GLASS_BOTTLE));
                boolean tonic = false; var inv = p.getInventory();
                for (int i = 0; i < inv.getContainerSize(); i++) if (inv.getItem(i).is(Items.POTION) && inv.getItem(i).getHoverName().getString().equals("Herbal Tonic")) tonic = true;
                check(tonic && station(w, press).stock() == 0, "The press bottles an Herbal Tonic");
                // Easel: sketch, finish with blue (a ship at sea), take it home.
                use(w, easel, new ItemStack(Items.DYE.red())); check(level.getBlockState(easel).getValue(WorkstationBlock.ART) == WorkstationBlock.SKETCH, "A dye sketches the canvas");
                use(w, easel, new ItemStack(Items.DYE.blue())); check(level.getBlockState(easel).getValue(WorkstationBlock.ART) == Workstations.paintingFor(Items.DYE.blue()), "A second dye finishes a painting");
            });
            flush(w); c.waitTicks(5);
            w.getServer().runOnServer(s -> { var mid = positions.get(5); player(w).teleportTo(level(w), mid.getX() + .5, mid.getY() + 1.2, mid.getZ() - 4.5, java.util.Set.of(), 0, 12, true); });
            flush(w); c.waitTicks(20); c.takeScreenshot("workstations-in-use");
            w.getServer().runOnServer(s -> {
                var p = player(w); var level = level(w);
                use(w, easel, ItemStack.EMPTY);
                check(count(p, Items.PAINTING) == 1 && level.getBlockState(easel).getValue(WorkstationBlock.ART) == 0, "The finished painting comes off the easel");
                // Sawmill: half again as many planks, three sticks a plank, the whole stack when sneaking.
                use(w, saw, new ItemStack(Items.OAK_LOG)); check(count(p, Items.OAK_PLANKS) == 6, "A log saws into six planks");
                use(w, saw, new ItemStack(Items.SPRUCE_PLANKS)); check(count(p, Items.STICK) == 3, "A plank saws into three sticks");
                use(w, saw, new ItemStack(Items.BIRCH_LOG, 20));
                check(count(p, Items.BIRCH_PLANKS) == 96 && p.getMainHandItem().getCount() == 4, "A click saws up to sixteen logs");
                // Sewing table: wool unravels; string mends leather.
                use(w, sewing, new ItemStack(Items.WOOL.white())); check(count(p, Items.STRING) == 3, "Wool unravels into string");
                var boots = new ItemStack(Items.LEATHER_BOOTS); boots.setDamageValue(40);
                p.getInventory().clearContent(); p.setItemInHand(InteractionHand.MAIN_HAND, boots); p.getInventory().add(new ItemStack(Items.STRING, 5));
                p.gameMode.useItemOn(p, level, p.getMainHandItem(), InteractionHand.MAIN_HAND, new BlockHitResult(Vec3.atCenterOf(sewing), Direction.NORTH, sewing, false));
                check(p.getMainHandItem().getDamageValue() == 0 && count(p, Items.STRING) == 2, "Three lengths of string mend worn leather boots");
                // Archives: a book becomes the village chronicle.
                use(w, archives, new ItemStack(Items.BOOK));
                boolean chronicle = false; var items = p.getInventory();
                for (int i = 0; i < items.getContainerSize(); i++) {
                    var book = items.getItem(i).get(DataComponents.WRITTEN_BOOK_CONTENT);
                    if (book != null && book.title().raw().equals("Chronicle of Thistlewick")) chronicle = true;
                }
                check(chronicle, "The archives copy out the village chronicle");
                // Music stand: a tune lifts the spirits.
                use(w, music, ItemStack.EMPTY); check(p.hasEffect(MobEffects.HASTE), "Playing the music stand grants Haste");
                // Training dummy: a strike is measured, not mined.
                p.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.IRON_SWORD));
                check(Workstations.attack(p, level, InteractionHand.MAIN_HAND, dummy, Direction.NORTH).consumesAction(), "Striking the dummy is handled");
                check(level.getBlockState(dummy).is(VillageBlocks.get("training_dummy")), "and the dummy is still standing");
                check(Workstations.targetScore(0, 0) == 10 && Workstations.targetScore(3, 3) == 4, "Target rings score from the bullseye out");
            });
            // Holding attack on the dummy in survival never breaks it.
            c.runOnClient(client -> { client.gameMode.startDestroyBlock(dummy, Direction.NORTH); });
            for (int i = 0; i < 40; i++) { c.runOnClient(client -> client.gameMode.continueDestroyBlock(dummy, Direction.NORTH)); c.waitTicks(1); }
            flush(w);
            w.getServer().runOnServer(s -> check(level(w).getBlockState(dummy).is(VillageBlocks.get("training_dummy")), "Holding attack doesn't mine the dummy"));
            // The stove finishes cooking in half the campfire's time.
            c.waitTicks(320); flush(w);
            w.getServer().runOnServer(s -> {
                var cooked = level(w).getEntitiesOfClass(ItemEntity.class, new net.minecraft.world.phys.AABB(stove).inflate(2), e -> e.getItem().is(Items.COOKED_BEEF));
                check(!cooked.isEmpty() && !station(w, stove).cooking(), "Raw beef comes off the stove cooked");
            });

            // Residents at work.
            var residents = new ArrayList<UUID>();
            w.getServer().runOnServer(s -> {
                var level = level(w); var p = player(w);
                String[][] jobs = {{"cook", "kitchen_stove"}, {"painter", "easel_canvas"}, {"tavern_keeper", "drinks_barrel"}, {"knight", "training_dummy"}};
                for (var job : jobs) {
                    var pos = positions.get(names.indexOf(job[1]));
                    var v = new Villager(EntityTypes.VILLAGER, level); v.setPos(pos.getX() + .5, pos.getY(), pos.getZ() - 1.2); v.setNoAi(true);
                    v.setVillagerData(v.getVillagerData().withProfession(s.registryAccess(), VillageProfessions.key(job[0])));
                    level.addFreshEntity(v); residents.add(v.getUUID());
                    v.getBrain().setMemory(MemoryModuleType.JOB_SITE, GlobalPos.of(level.dimension(), pos));
                }
                var cook = (Villager) level.getEntity(residents.get(0));
                Workstations.worked(level, cook);
                check(station(w, stove).mealDay == day(level), "The cook makes the dish of the day");
                int before = count(p, VillageItems.get("hearty_stew")) + count(p, VillageItems.get("fresh_village_bread"));
                p.teleportTo(level, stove.getX() + .5, stove.getY(), stove.getZ() - 2, java.util.Set.of(), 0, 20, true);
                use(w, stove, ItemStack.EMPTY);
                check(count(p, VillageItems.get("hearty_stew")) + count(p, VillageItems.get("fresh_village_bread")) > before, "A visitor gets a helping");
                use(w, stove, ItemStack.EMPTY);
                check(count(p, VillageItems.get("hearty_stew")) + count(p, VillageItems.get("fresh_village_bread")) == before + (day(level) % 2 == 1 ? 1 : 2), "Only one helping a day");
                var painter = (Villager) level.getEntity(residents.get(1));
                for (int i = 0; i < 8; i++) Workstations.worked(level, painter);
                check(level.getBlockState(easel).getValue(WorkstationBlock.ART) >= WorkstationBlock.FIRST_PAINTING, "The painter finishes a painting at work");
                var keeper = (Villager) level.getEntity(residents.get(2));
                int stock = station(w, barrel).stock(); Workstations.worked(level, keeper);
                check(station(w, barrel).stock() == Math.min(16, stock + 4), "The tavern keeper restocks the barrel");
                var knight = (Villager) level.getEntity(residents.get(3));
                GuardProgression.refresh(knight);
                double xp = GuardProgression.progress(knight).xp(); int lvl = GuardProgression.progress(knight).level();
                Workstations.worked(level, knight);
                check(GuardProgression.progress(knight).xp() > xp || GuardProgression.progress(knight).level() > lvl, "A knight gains a little experience training");
            });

            // Routines: an ordinary resident sleeps at midnight, shelters from a storm and keeps the market.
            UUID resident = w.getServer().computeOnServer(s -> {
                var level = level(w); var origin = positions.get(5).offset(0, 0, -4);
                var v = new Villager(EntityTypes.VILLAGER, level); v.setPos(origin.getX() + .5, origin.getY(), origin.getZ() + .5);
                v.setVillagerData(v.getVillagerData().withProfession(s.registryAccess(), VillagerProfession.LIBRARIAN));
                level.addFreshEntity(v); return v.getUUID();
            });
            c.waitTicks(5);
            // Weather needs a rainy biome under the test resident.
            w.getServer().runOnServer(s -> {
                var o = positions.get(5);
                s.getCommands().performPrefixedCommand(s.createCommandSourceStack(), "fillbiome " + (o.getX() - 24) + " " + (o.getY() - 8) + " " + (o.getZ() - 24) + " "
                        + (o.getX() + 24) + " " + (o.getY() + 16) + " " + (o.getZ() + 24) + " minecraft:plains");
            });
            w.getServer().runCommand("time set 18000");
            w.getServer().runOnServer(s -> {
                var v = (Villager) level(w).getEntity(resident); ResidentRoutines.update(v);
                check(target(v).getAttached(ROUTINE).equals("sleep"), "At midnight a librarian is asleep (in their routine): " + target(v).getAttached(ROUTINE));
                check(((RoutineBrain) v.getBrain()).villagefriends$routine() == net.minecraft.world.entity.schedule.Activity.REST, "and their brain is resting");
            });
            w.getServer().runCommand("time set " + Routine.at(16, 45)); w.getServer().runCommand("weather thunder");
            // Rain normally fades in over a few seconds; set it at full strength now.
            w.getServer().runOnServer(s -> { level(w).setRainLevel(1); level(w).setThunderLevel(1); });
            c.waitTicks(3);
            w.getServer().runOnServer(s -> {
                var v = (Villager) level(w).getEntity(resident); ResidentRoutines.update(v);
                check(target(v).getAttached(ROUTINE).equals("storm"), "A thunderstorm sends them indoors: " + target(v).getAttached(ROUTINE));
                check(!((RoutineBrain) v.getBrain()).villagefriends$maySleep(), "awake, not in bed");
            });
            w.getServer().runCommand("weather clear");
            w.getServer().runOnServer(s -> { level(w).setRainLevel(0); level(w).setThunderLevel(0); });
            c.waitTicks(3);
            w.getServer().runOnServer(s -> {
                var v = (Villager) level(w).getEntity(resident); ResidentRoutines.update(v);
                check(target(v).getAttached(ROUTINE).equals("social"), "Clear skies: back out to see the neighbors: " + target(v).getAttached(ROUTINE));
            });
            // The conversation window shows what they're doing.
            int eid = w.getServer().computeOnServer(s -> { var v = (Villager) level(w).getEntity(resident); v.setNoAi(true);
                player(w).teleportTo(level(w), v.getX(), v.getY(), v.getZ() - 2.5, java.util.Set.of(), 0, 10, true); return v.getId(); });
            flush(w); c.waitTicks(5);
            w.getConnection().waitForClientboundEntityUpdates(EntityTypes.VILLAGER);
            c.runOnClient(client -> { var e = client.level.getEntity(eid); client.gameMode.interact(client.player, e, new EntityHitResult(e), InteractionHand.MAIN_HAND); });
            c.waitForScreen(FriendshipScreen.class); flush(w); c.waitTicks(40);
            c.takeScreenshot("workstations-routine-conversation");
            c.clickScreenButton("Goodbye"); c.waitForScreen(null);
        }
        LOGGER.info("WORKSTATIONS PASSED: 11 redesigned workstations placed and photographed; stove, barrel, tap, press, easel, sawmill, sewing table, archives, music stand, dummy and target used by a player; cook, painter, tavern keeper and knight at work; a resident's routine through midnight, a storm and clear skies.");
    }
}
