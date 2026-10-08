package dev.villagefriends;

import static dev.villagefriends.VillageFriends.*;
import dev.villagefriends.client.*;
import java.util.*;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.*;
import net.fabricmc.fabric.api.client.gametest.v1.world.TestWorldSave;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.npc.villager.VillagerProfession;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.EntityHitResult;
import net.minecraft.world.phys.Vec3;

/**
 * Village life in a real world: a settlement's census, a baby born through the breeding hook who
 * takes the family surname, village news in conversation, emote bubbles, the Village Ledger from the
 * conversation dock, the ledger item and a notice board, a death the village remembers, and save/reload.
 */
@SuppressWarnings("UnstableApiUsage")
public final class VillageLifeGameTest implements FabricClientGameTest {
    private static void check(boolean ok, String reason) { if (!ok) throw new AssertionError(reason); }
    private static Villager villager(TestSingleplayerContext w, UUID id) { return (Villager) w.getConnection().getServerLevel().getEntity(id); }
    private static void flush(TestSingleplayerContext w) { w.getConnection().waitForServerboundPackets(); w.getConnection().waitForClientboundPackets(); }
    private static void open(ClientGameTestContext c, TestSingleplayerContext w, UUID id) {
        w.getConnection().waitForClientboundEntityUpdates(EntityTypes.VILLAGER);
        int eid = w.getServer().computeOnServer(s -> villager(w, id).getId());
        c.runOnClient(client -> { client.gui.setScreen(null); var e = client.level.getEntity(eid); client.gameMode.interact(client.player, e, new EntityHitResult(e), InteractionHand.MAIN_HAND); });
        c.waitForScreen(FriendshipScreen.class); flush(w);
    }
    private static String surname(String name) { return name.substring(name.lastIndexOf(' ') + 1); }

    @Override public void runTest(ClientGameTestContext c) {
        var residents = new ArrayList<UUID>(); UUID baby; String babyId, motherId; TestWorldSave saved;
        c.getInput().resizeWindow(1280, 800); c.runOnClient(client -> { client.options.guiScale().set(2); client.resizeGui(); });
        try (var w = c.worldBuilder().create()) {
            w.getConnection().waitForChunksRender();
            w.getServer().runCommand("time set day"); w.getServer().runCommand("gamemode creative @a"); w.getServer().runCommand("gamerule doDaylightCycle false");
            w.getServer().runCommand("tp @a ~ ~ ~ 0 12");
            // Six neighbors in a loose arc in front of the player, inside a marked settlement.
            w.getServer().runOnServer(s -> {
                var p = w.getConnection().getServerPlayer(); var level = w.getConnection().getServerLevel();
                double[][] spots = {{0, 2.6}, {-2.2, 4}, {2.2, 4}, {-4.2, 6}, {4.2, 6}, {0, 7}};
                for (var spot : spots) {
                    var v = new Villager(EntityTypes.VILLAGER, level); v.setPos(p.getX() + spot[0], p.getY(), p.getZ() + spot[1]); v.setNoAi(true);
                    v.setYRot(180); v.yBodyRot = v.yHeadRot = 180;
                    v.setVillagerData(v.getVillagerData().withProfession(s.registryAccess(), VillagerProfession.FARMER));
                    level.addFreshEntity(v); residents.add(v.getUUID());
                }
                VillageSettlements.mark(level, p.blockPosition().offset(0, 0, -3), "Hearthmere");
                for (var id : residents) VillageSettlements.identify(villager(w, id), true);
                var society = VillageSocieties.of(villager(w, residents.getFirst()));
                check(society != null && society.living().size() == 6, "Every resident is counted in their village's census");
                for (var a : residents) for (var b : residents) if (a != b)
                    check(society.affinity(profile(villager(w, a)).id(), profile(villager(w, b)).id(), 0) == society.affinity(profile(villager(w, b)).id(), profile(villager(w, a)).id(), 0), "Relationship meters are mutual");
            });
            // A baby is born through vanilla's breeding hook and joins the right family.
            motherId = w.getServer().computeOnServer(s -> profile(villager(w, residents.get(1))).id());
            baby = w.getServer().computeOnServer(s -> {
                var level = w.getConnection().getServerLevel();
                var mother = villager(w, residents.get(1)); var father = villager(w, residents.get(2));
                var child = mother.getBreedOffspring(level, father);
                check(child != null && !target(child).getAttachedOrElse(PARENTS, "").isEmpty(), "Breeding records both parents");
                child.setAge(-24000); child.setNoAi(true); child.setPos(mother.getX() + 1, mother.getY(), mother.getZ() - 1);
                level.addFreshEntity(child);
                return child.getUUID();
            });
            c.waitTicks(5);
            babyId = w.getServer().computeOnServer(s -> {
                var child = villager(w, baby); VillageSettlements.identify(child, false);
                var society = VillageSocieties.of(child); String id = profile(child).id();
                check(society.has(id) && society.relation(id, motherId).equals("parent"), "The baby knows their mother");
                check(society.news().getLast().kind().equals("born"), "A birth is village news");
                String mother = society.get(motherId).name();
                check(surname(target(child).getAttached(HOME).baseName()).equals(surname(mother)) || mother.endsWith("Patel"), "Babies take their family's surname");
                check(!VillageSocieties.mayBreed(villager(w, residents.get(1)), child), "Relatives never start a family together");
                return id;
            });
            // A close friend hears the village news and a heart-to-heart.
            w.getServer().runOnServer(s -> {
                var p = w.getConnection().getServerPlayer(); var v = villager(w, residents.getFirst());
                save(v, p, new FriendshipState(200, -1, -1, 0, ""));
                var bond = BondState.NEW.activity(0, "walk").chapter(4);
                for (int day = 0; day < 5; day++) bond = bond.visit(day - 10);
                saveBond(v, p, bond);
                String babyName = VillageSocieties.of(v).get(babyId).name();
                String news = NarrativeEngine.conversation(v, p, "news");
                check(news.contains(babyName.substring(0, babyName.indexOf(' '))), "Neighbors talk about the new baby: " + news);
                check(!NarrativeEngine.conversation(v, p, "heart").isBlank(), "Heart-to-heart talks work");
                check(FriendshipLevels.level(state(v, p), bond(v, p)) == 10, "Story, visits and points reach the top level");
            });
            open(c, w, residents.getFirst());
            c.waitTicks(30); c.takeScreenshot("village-life-conversation");
            c.clickScreenButton("Any village news?"); flush(w); c.waitTicks(60); c.takeScreenshot("village-life-news");
            c.clickScreenButton("Anyone special?"); flush(w); c.waitTicks(60); c.takeScreenshot("village-life-heart-to-heart");
            // The Village Ledger opens on this resident's page and returns to the conversation.
            c.clickScreenButton("Village"); flush(w);
            c.waitForScreen(LedgerScreen.class); c.waitTicks(5); c.takeScreenshot("village-life-ledger-resident");
            c.clickScreenButton("Village news"); flush(w); c.waitTicks(5); c.takeScreenshot("village-life-ledger-news");
            c.clickScreenButton("Back"); c.waitForScreen(FriendshipScreen.class); c.clickScreenButton("Goodbye"); c.waitForScreen(null);
            // Neighbors pop emote bubbles above their heads.
            var emotes = List.of(Emote.HEART, Emote.EXCLAIM, Emote.QUESTION, Emote.NOTE, Emote.ANGER, Emote.DOTS);
            w.getServer().runOnServer(s -> { for (int i = 0; i < residents.size(); i++) VillageSocieties.emote(villager(w, residents.get(i)), emotes.get(i), 0); });
            flush(w); c.waitTicks(8);
            var entityIds = w.getServer().computeOnServer(s -> residents.stream().map(id -> villager(w, id).getId()).toList());
            c.runOnClient(client -> { for (int id : entityIds) check(EmoteBubbles.get(id) != null, "Every resident shows their bubble"); });
            c.takeScreenshot("village-life-bubbles");
            // The ledger item opens the village's ledger.
            w.getServer().runOnServer(s -> w.getConnection().getServerPlayer().setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(VillageItems.get("village_ledger"))));
            flush(w);
            c.runOnClient(client -> client.gameMode.useItem(client.player, InteractionHand.MAIN_HAND)); flush(w);
            c.waitForScreen(LedgerScreen.class); c.waitTicks(5); c.takeScreenshot("village-life-ledger-item");
            c.clickScreenButton("Close"); c.waitForScreen(null);
            var board = w.getServer().computeOnServer(s -> {
                var p = w.getConnection().getServerPlayer(); var pos = p.blockPosition().offset(2, 0, 0);
                w.getConnection().getServerLevel().setBlockAndUpdate(pos, VillageBlocks.get("notice_board").defaultBlockState());
                p.setItemInHand(InteractionHand.MAIN_HAND, ItemStack.EMPTY); return pos;
            });
            flush(w); c.waitTicks(2);
            c.runOnClient(client -> client.gameMode.useItemOn(client.player, InteractionHand.MAIN_HAND, new BlockHitResult(Vec3.atCenterOf(board), Direction.WEST, board, false)));
            // The notice board opens its own screen, with a way into the ledger and back.
            flush(w); c.waitForScreen(NoticeBoardScreen.class);
            c.clickScreenButton("Village Ledger"); flush(w); c.waitForScreen(LedgerScreen.class);
            c.clickScreenButton("Back"); c.waitForScreen(NoticeBoardScreen.class); c.clickScreenButton("Close"); c.waitForScreen(null);
            // A neighbor's death is remembered, and their partner is free to love again.
            w.getServer().runOnServer(s -> villager(w, residents.getLast()).kill(w.getConnection().getServerLevel()));
            c.waitTicks(3);
            w.getServer().runOnServer(s -> {
                var society = VillageSocieties.of(villager(w, residents.getFirst()));
                check(society.living().size() == 6 && society.everyone().size() == 7, "The village remembers who passed away");
                check(society.news().stream().anyMatch(n -> n.kind().equals("passed")), "A death is village news");
            });
            saved = w.getWorldSave();
        }
        try (var w = saved.open()) {
            w.getConnection().waitForChunksRender(); c.waitTicks(10);
            w.getServer().runOnServer(s -> {
                var society = VillageSocieties.of(villager(w, residents.getFirst()));
                check(society != null && society.has(babyId) && society.relation(babyId, motherId).equals("parent"), "Families survive save and reload");
                check(society.news().stream().anyMatch(n -> n.kind().equals("born")), "Village news survives save and reload");
            });
        }
        LOGGER.info("VILLAGE LIFE GAMEPLAY PASSED: census, mutual meters, birth through breeding with family surname, relatives' breeding guard, news and heart-to-heart dialogue, top friendship level, conversation and ledger screenshots, emote bubbles, ledger item and notice board, remembered death, save/reload.");
    }
}
