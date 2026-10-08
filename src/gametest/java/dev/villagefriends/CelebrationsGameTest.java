package dev.villagefriends;

import static dev.villagefriends.VillageFriends.*;
import dev.villagefriends.client.*;
import dev.villagefriends.quest.Board;
import dev.villagefriends.quest.Notice;
import dev.villagefriends.routine.Routine;
import dev.villagefriends.social.Calendar;
import java.util.*;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.*;
import net.fabricmc.fabric.api.client.gametest.v1.world.TestWorldSave;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.npc.villager.VillagerProfession;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.EntityHitResult;
import net.minecraft.world.phys.Vec3;

/**
 * Birthdays and notice boards in a real world: a resident's birthday with the party hat, the evening party
 * by the bell and cake time, birthday wishes and a doubled birthday gift; then the village notice board with
 * its pinned notes, a monster hunt counted kill by kill, a fetch turned in at the board, a sealed letter
 * carried to a neighbor, the rewards and standing, and save/reload. Screenshots are named {@code celebrations-*}.
 */
@SuppressWarnings("UnstableApiUsage")
public final class CelebrationsGameTest implements FabricClientGameTest {
    private static void check(boolean ok, String reason) { if (!ok) throw new AssertionError(reason); }
    private static Villager villager(TestSingleplayerContext w, UUID id) { return (Villager) w.getConnection().getServerLevel().getEntity(id); }
    private static void flush(TestSingleplayerContext w) { w.getConnection().waitForServerboundPackets(); w.getConnection().waitForClientboundPackets(); }
    private static void talk(ClientGameTestContext c, TestSingleplayerContext w, UUID id) {
        w.getConnection().waitForClientboundEntityUpdates(EntityTypes.VILLAGER);
        int eid = w.getServer().computeOnServer(s -> villager(w, id).getId());
        c.runOnClient(client -> { client.gui.setScreen(null); var e = client.level.getEntity(eid); client.gameMode.interact(client.player, e, new EntityHitResult(e), InteractionHand.MAIN_HAND); });
        c.waitForScreen(FriendshipScreen.class); flush(w); c.waitTicks(10);
    }
    private static void board(ClientGameTestContext c, TestSingleplayerContext w, BlockPos pos) {
        c.runOnClient(client -> { client.gui.setScreen(null); client.gameMode.useItemOn(client.player, InteractionHand.MAIN_HAND, new BlockHitResult(Vec3.atCenterOf(pos), Direction.NORTH, pos, false)); });
        flush(w); c.waitForScreen(NoticeBoardScreen.class); c.waitTicks(5);
    }
    private static NoticeBoardScreen screen(ClientGameTestContext c) { return c.computeOnClient(client -> (NoticeBoardScreen) client.gui.screen()); }
    private static int count(TestSingleplayerContext w, net.minecraft.world.item.Item item) {
        return w.getServer().computeOnServer(s -> { var inv = w.getConnection().getServerPlayer().getInventory(); int n = 0;
            for (int i = 0; i < inv.getContainerSize(); i++) if (inv.getItem(i).is(item)) n += inv.getItem(i).getCount(); return n; });
    }

    @Override public void runTest(ClientGameTestContext c) {
        var residents = new ArrayList<UUID>(); TestWorldSave saved; BlockPos boardPos; String village;
        c.getInput().resizeWindow(1280, 800); c.runOnClient(client -> { client.options.guiScale().set(2); client.resizeGui(); });
        try (var w = c.worldBuilder().create()) {
            w.getConnection().waitForChunksRender();
            for (var cmd : List.of("gamemode creative @a", "gamerule advance_time false", "gamerule advance_weather false", "gamerule spawn_mobs false", "weather clear", "tp @a ~ ~ ~ 0 12"))
                w.getServer().runCommand(cmd);
            // Seven neighbors and a child in front of the player, in a settlement called Candlewick.
            w.getServer().runOnServer(s -> {
                var p = w.getConnection().getServerPlayer(); var level = w.getConnection().getServerLevel();
                double[][] spots = {{0, 3}, {-2.2, 4}, {2.2, 4}, {-4.2, 6}, {4.2, 6}, {-1.2, 7}, {1.4, 7.2}, {0.8, 4.6}};
                var jobs = List.of(VillagerProfession.FARMER, VillagerProfession.LIBRARIAN, VillagerProfession.CLERIC, VillagerProfession.FISHERMAN,
                        VillagerProfession.ARMORER, VillagerProfession.SHEPHERD, VillagerProfession.BUTCHER, VillagerProfession.NONE);
                for (int i = 0; i < spots.length; i++) {
                    var v = new Villager(EntityTypes.VILLAGER, level); v.setPos(p.getX() + spots[i][0], p.getY(), p.getZ() + spots[i][1]); v.setNoAi(true);
                    v.setYRot(180); v.yBodyRot = v.yHeadRot = 180;
                    v.setVillagerData(v.getVillagerData().withProfession(s.registryAccess(), jobs.get(i)));
                    if (i == spots.length - 1) v.setAge(-24000);
                    level.addFreshEntity(v); residents.add(v.getUUID());
                }
                VillageSettlements.mark(level, p.blockPosition().offset(0, 0, -3), "Candlewick");
                for (var id : residents) VillageSettlements.identify(villager(w, id), true);
            });
            village = w.getServer().computeOnServer(s -> target(villager(w, residents.getFirst())).getAttached(HOME).village());

            // -- a birthday --------------------------------------------------------------------------
            // Jump to the first resident's birthday a year on, in the evening.
            long birthdayDay = w.getServer().computeOnServer(s -> {
                var society = VillageSocieties.of(villager(w, residents.getFirst()));
                return (long) society.get(profile(villager(w, residents.getFirst())).id()).birthday() + Calendar.YEAR;
            });
            w.getServer().runCommand("time set " + (birthdayDay * 24000 + Routine.at(16, 45)));
            c.waitTicks(230); flush(w);
            String celebrant = w.getServer().computeOnServer(s -> {
                var host = villager(w, residents.getFirst()); var society = VillageSocieties.of(host);
                check(day(host.level()) == birthdayDay, "It is the birthday");
                check(Birthdays.celebrating(host) && Birthdays.wearingHat(host), "The birthday resident wears a party hat");
                check(!Birthdays.wearingHat(villager(w, residents.get(1))), "Nobody else does");
                check(society.recent(birthdayDay, 0).stream().anyMatch(n -> n.kind().equals("birthday")), "The birthday is village news");
                check("party".equals(target(host).getAttached(ROUTINE)), "They're at their party by the bell: " + target(host).getAttached(ROUTINE));
                check("party".equals(target(villager(w, residents.getLast())).getAttached(ROUTINE)), "Children go to every party");
                return name(host);
            });
            int hostEntity = w.getServer().computeOnServer(s -> villager(w, residents.getFirst()).getId());
            c.runOnClient(client -> check(Birthdays.wearingHat((Villager) client.level.getEntity(hostEntity)), "Clients see the party hat"));
            c.waitTicks(20); c.takeScreenshot("celebrations-party");
            // Cake time: everyone nearby gets a slice.
            w.getServer().runCommand("time set " + (birthdayDay * 24000 + Routine.at(17, 50)));
            c.waitTicks(60); flush(w);
            check(count(w, VillageItems.get("birthday_cake_slice")) == 1, "Cake time hands the player a slice of birthday cake");
            c.takeScreenshot("celebrations-cake-time");
            // Wish them a happy birthday, then give a cake: twice the friendship.
            talk(c, w, residents.getFirst());
            c.takeScreenshot("celebrations-birthday-greeting");
            c.clickScreenButton("Happy birthday!"); flush(w); c.waitTicks(40);
            w.getServer().runOnServer(s -> {
                var host = villager(w, residents.getFirst()); var p = w.getConnection().getServerPlayer();
                check(bond(host, p).has("birthday_wish:" + Calendar.year(birthdayDay)), "The birthday wish is remembered");
                check(bond(host, p).memories().stream().anyMatch(m -> m.contains("happy birthday")), "And it's a memory");
            });
            c.takeScreenshot("celebrations-birthday-wish");
            w.getServer().runOnServer(s -> w.getConnection().getServerPlayer().setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.CAKE)));
            flush(w);
            int before = w.getServer().computeOnServer(s -> state(villager(w, residents.getFirst()), w.getConnection().getServerPlayer()).points());
            c.clickScreenButton("Give gift"); flush(w); c.waitTicks(40);
            int after = w.getServer().computeOnServer(s -> state(villager(w, residents.getFirst()), w.getConnection().getServerPlayer()).points());
            check(after - before >= 28, "A cake on their birthday is worth double their favorite gift: " + (after - before));
            c.takeScreenshot("celebrations-birthday-gift");
            c.clickScreenButton("Goodbye"); c.waitForScreen(null);
            check(celebrant != null, "named celebrant");

            // -- the notice board ---------------------------------------------------------------------
            w.getServer().runCommand("time set " + ((birthdayDay + 1) * 24000 + Routine.at(9, 0)));
            boardPos = w.getServer().computeOnServer(s -> {
                var p = w.getConnection().getServerPlayer(); var pos = p.blockPosition().offset(-2, 0, 2);
                w.getConnection().getServerLevel().setBlockAndUpdate(pos, VillageBlocks.get("notice_board").defaultBlockState().setValue(FoundationBlock.FACING, Direction.NORTH));
                p.setItemInHand(InteractionHand.MAIN_HAND, ItemStack.EMPTY); return pos;
            });
            c.waitTicks(110); flush(w);
            int notes = w.getServer().computeOnServer(s -> w.getConnection().getServerLevel().getBlockState(boardPos).getValue(NoticeBoardBlock.NOTES));
            check(notes == 3, "A fresh board is crowded with notes: " + notes);
            c.takeScreenshot("celebrations-board-block");
            board(c, w, boardPos);
            var shown = screen(c).data();
            check(shown.notices().size() >= 3 && shown.notices().stream().allMatch(n -> n.state().equals("open")), "Four notices are up for grabs: " + shown.notices().size());
            check(!shown.birthdays().isEmpty(), "The board lists upcoming birthdays");
            c.takeScreenshot("celebrations-notice-board");
            // Pin three known notices: a zombie hunt, wheat for the farmer, and a letter to the librarian.
            var ids = w.getServer().computeOnServer(s -> {
                var level = w.getConnection().getServerLevel(); var record = VillageSettlements.book(level).villages().get(village);
                var b = VillageQuests.board(level, record); long today = day(level);
                String farmer = profile(villager(w, residents.getFirst())).id(), librarian = profile(villager(w, residents.get(1))).id();
                var hunt = new Notice("t-hunt", Notice.HUNT, farmer, VillageSocieties.baseName(villager(w, residents.getFirst())), "farmer", "zombies", 2, "", "",
                        new Notice.Reward(3, "minecraft:bread", 2), "Zombie trouble", "Zombies trampled my carrots again. Could you deal with 2 zombies?", today, today + 3, "");
                var fetch = new Notice("t-fetch", Notice.FETCH, farmer, hunt.posterName(), "farmer", "minecraft:wheat", 6, "", "",
                        new Notice.Reward(2, "minecraft:pumpkin_pie", 1), "Wanted: 6 wheat", "Bread day is coming. Could you bring me 6 wheat?", today, today + 3, "");
                var letter = new Notice("t-letter", Notice.LETTER, farmer, hunt.posterName(), "farmer", librarian, 1, "friend", VillageSocieties.baseName(villager(w, residents.get(1))),
                        new Notice.Reward(2, "minecraft:bread", 1), "A letter for a friend", "Could you carry a letter for me? It's sealed, so no peeking.", today, today + 3, "");
                var pinned = new ArrayList<>(b.notices()); pinned.addAll(List.of(hunt, fetch, letter));
                VillageQuests.put(level, new Board(b.village(), pinned, b.day(), b.serial(), b.favors()));
                var p = w.getConnection().getServerPlayer();
                for (var id : List.of("t-hunt", "t-fetch", "t-letter")) check(!VillageQuests.accept(p, level, record, id).contains("first"), "Took notice " + id);
                check(VillageQuests.log(p).quests().size() == 3 && VillageQuests.log(p).full(), "Three notices in hand at most");
                check(VillageQuests.accept(p, level, record, b.open(today).getFirst().id()).contains("already have"), "A fourth notice is refused");
                return List.of("t-hunt", "t-fetch", "t-letter");
            });
            check(count(w, VillageItems.get("sealed_letter")) == 1, "Taking a letter notice hands over the sealed letter");
            // Two zombies, defeated by the player, finish the hunt.
            w.getServer().runOnServer(s -> {
                var level = w.getConnection().getServerLevel(); var p = w.getConnection().getServerPlayer();
                for (int i = 0; i < 2; i++) {
                    var z = EntityTypes.ZOMBIE.create(level, EntitySpawnReason.COMMAND);
                    z.setPos(p.getX() + 6, p.getY(), p.getZ() - 4 - i); z.setNoAi(true); level.addFreshEntity(z);
                    z.hurtServer(level, level.damageSources().playerAttack(p), 1000F);
                }
                var q = VillageQuests.log(p).find(village, "t-hunt");
                check(q != null && q.hunted(), "Both zombies counted toward the hunt");
            });
            board(c, w, boardPos);
            c.runOnClient(client -> ((NoticeBoardScreen) client.gui.screen()).select("t-hunt")); c.waitTicks(3);
            check(screen(c).data().notices().stream().anyMatch(n -> n.id().equals("t-hunt") && n.state().equals("ready")), "The board shows the hunt is ready");
            c.takeScreenshot("celebrations-hunt-ready");
            int emeralds = count(w, Items.EMERALD);
            c.clickScreenButton("Turn it in"); flush(w); c.waitTicks(5);
            check(count(w, Items.EMERALD) == emeralds + 3, "Turning in pays the emeralds");
            check(count(w, Items.BREAD) >= 2, "And the poster's gift");
            // Wheat for the farmer, turned in at the board.
            w.getServer().runOnServer(s -> w.getConnection().getServerPlayer().getInventory().add(new ItemStack(Items.WHEAT, 8)));
            flush(w); board(c, w, boardPos);
            c.runOnClient(client -> ((NoticeBoardScreen) client.gui.screen()).select("t-fetch")); c.waitTicks(3);
            c.takeScreenshot("celebrations-fetch-ready");
            c.clickScreenButton("Turn it in"); flush(w); c.waitTicks(5);
            check(count(w, Items.WHEAT) == 2, "The farmer took exactly six wheat");
            c.runOnClient(client -> client.gui.setScreen(null));
            // The letter goes to the librarian in person.
            talk(c, w, residents.get(1));
            c.clickScreenButton("I have a letter for you"); flush(w); c.waitTicks(40);
            check(count(w, VillageItems.get("sealed_letter")) == 0, "The letter was handed over");
            c.takeScreenshot("celebrations-letter");
            c.clickScreenButton("Goodbye"); c.waitForScreen(null);
            w.getServer().runOnServer(s -> {
                var level = w.getConnection().getServerLevel(); var p = w.getConnection().getServerPlayer();
                var log = VillageQuests.log(p);
                check(log.quests().isEmpty() && log.answered() == 3, "All three notices answered");
                var b = VillageQuests.boards(level).get(village);
                check(b.favors(p.getUUID().toString()) == 3 && Board.standing(3) == 1, "Three notices make a Helping Hand");
                check(b.find("t-hunt") == null && b.find("t-letter") == null, "Answered notices come down");
                var society = VillageSocieties.society(level, village);
                check(society.news().stream().filter(n -> n.kind().equals("helped")).count() == 3, "The village talks about the help");
                check(villager(w, residents.getFirst()).getGossips().getReputation(p.getUUID(), t -> true) > 0, "The poster gives better prices");
            });
            board(c, w, boardPos);
            c.takeScreenshot("celebrations-board-after");
            c.clickScreenButton("Close"); c.waitForScreen(null);
            saved = w.getWorldSave();
        }
        try (var w = saved.open()) {
            w.getConnection().waitForChunksRender(); c.waitTicks(10);
            w.getServer().runOnServer(s -> {
                var level = w.getConnection().getServerLevel(); var p = w.getConnection().getServerPlayer();
                check(VillageQuests.boards(level).get(village).favors(p.getUUID().toString()) == 3, "Standing survives save and reload");
                check(VillageQuests.log(p).answered() == 3, "The quest log survives save and reload");
            });
        }
        LOGGER.info("CELEBRATIONS PASSED: birthday news, party hat on server and client, evening party with a child guest, cake time slice, birthday wish, doubled birthday gift, "
                + "notice board notes and screen, birthdays on the board, three-notice limit, zombie hunt counted by kills, board turn-ins with emeralds and gifts, "
                + "sealed letter delivered in person, standing, village news, better prices, save/reload.");
    }
}
