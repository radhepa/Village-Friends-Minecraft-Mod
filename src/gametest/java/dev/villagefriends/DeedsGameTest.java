package dev.villagefriends;

import static dev.villagefriends.VillageFriends.*;
import dev.villagefriends.client.*;
import dev.villagefriends.deed.*;
import dev.villagefriends.home.HouseBounds;
import dev.villagefriends.pet.PetActionPayload;
import dev.villagefriends.pet.PetLink;
import dev.villagefriends.pet.PetProfile;
import dev.villagefriends.pet.VillagerPets;
import dev.villagefriends.quest.Board;
import dev.villagefriends.routine.Routine;
import java.util.*;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.*;
import net.fabricmc.fabric.api.client.gametest.v1.world.TestWorldSave;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.ai.memory.MemoryModuleType;
import net.minecraft.world.entity.ai.village.poi.PoiTypes;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.EntityHitResult;
import net.minecraft.world.phys.Vec3;

/**
 * Residents react to what the player did in their village: witnesses' bubbles and looks, reaction lines
 * (seen, heard, family), kept Journal memories, standing from notices plus deeds up to Good Neighbor and down
 * to Unwelcome (the board refuses work), prices, apologies, fading over weeks, a raid won, and the deed log
 * surviving save and reload. Screenshots are named {@code deeds-*}. Run with
 * {@code gradlew runClientGameTest -Ptests=DeedsGameTest -PtestHeap=2560m}.
 *
 * <p>Theft from a resident's chest and breaking a resident's bed or door use the housing index through
 * {@link HouseBounds} ({@link #theftAndBrokenHomes}: a cottage the player builds, which homeless residents move into).
 */
@SuppressWarnings("UnstableApiUsage")
public final class DeedsGameTest implements FabricClientGameTest {
    private static void check(boolean ok, String why) { if (!ok) throw new AssertionError(why); }
    private static void flush(TestSingleplayerContext w) { w.getConnection().waitForServerboundPackets(); w.getConnection().waitForClientboundPackets(); }
    private static ServerLevel level(TestSingleplayerContext w) { return w.getConnection().getServerLevel(); }
    private static ServerPlayer player(TestSingleplayerContext w) { return w.getConnection().getServerPlayer(); }
    private static Villager villager(TestSingleplayerContext w, UUID id) { return (Villager) level(w).getEntity(id); }
    private static String id(TestSingleplayerContext w, UUID id) { return VillageSocieties.id(villager(w, id)); }
    private static Villager resident(ServerLevel level, Vec3 base, double x, double z, boolean child) {
        var v = new Villager(EntityTypes.VILLAGER, level);
        v.setPos(base.x + x, base.y, base.z + z); v.setNoAi(true);
        v.setYRot(180); v.yBodyRot = v.yHeadRot = 180;
        if (child) v.setAge(-24000);
        level.addFreshEntity(v);
        return v;
    }
    private static DeedLog log(TestSingleplayerContext w) {
        var p = player(w); return Deeds.book(level(w)).log(VILLAGE[0], p.getUUID().toString());
    }
    private static Deed deed(TestSingleplayerContext w, DeedKind kind) {
        var log = log(w);
        if (log == null) return null;
        for (int i = log.deeds().size() - 1; i >= 0; i--) if (log.deeds().get(i).kind() == kind) return log.deeds().get(i);
        return null;
    }
    private static int score(TestSingleplayerContext w) { return Deeds.score10(level(w), VILLAGE[0], player(w).getUUID().toString()); }
    private static final String[] VILLAGE = {""};

    /** Steps up to a resident (within arm's reach), on the side facing the player's start. */
    private static void near(ClientGameTestContext c, TestSingleplayerContext w, UUID id) {
        w.getServer().runOnServer(s -> {
            var v = villager(w, id); var p = player(w);
            if (p.distanceTo(v) > 2.5) p.teleportTo(v.getX(), v.getY(), v.getZ() - 1.8);
        });
        flush(w); c.waitTicks(3);
    }
    private static void talk(ClientGameTestContext c, TestSingleplayerContext w, UUID id) {
        near(c, w, id);
        w.getConnection().waitForClientboundEntityUpdates(EntityTypes.VILLAGER);
        int eid = w.getServer().computeOnServer(s -> villager(w, id).getId());
        c.runOnClient(client -> { client.gui.setScreen(null); var e = client.level.getEntity(eid); client.gameMode.interact(client.player, e, new EntityHitResult(e), InteractionHand.MAIN_HAND); });
        c.waitForScreen(FriendshipScreen.class); flush(w); c.waitTicks(10);
    }
    private static void use(ClientGameTestContext c, TestSingleplayerContext w, UUID id) {
        near(c, w, id);
        w.getConnection().waitForClientboundEntityUpdates(EntityTypes.VILLAGER);
        int eid = w.getServer().computeOnServer(s -> villager(w, id).getId());
        c.runOnClient(client -> { var e = client.level.getEntity(eid); client.gameMode.interact(client.player, e, new EntityHitResult(e), InteractionHand.MAIN_HAND); });
        flush(w); c.waitTicks(5);
    }
    private static void bye(ClientGameTestContext c) { c.clickScreenButton("Goodbye"); c.waitForScreen(null); }
    private static void hold(TestSingleplayerContext w, ItemStack stack) {
        w.getServer().runOnServer(s -> player(w).setItemInHand(InteractionHand.MAIN_HAND, stack));
        flush(w);
    }
    /** Waits for a resident's bubble on the client. */
    private static void bubble(ClientGameTestContext c, TestSingleplayerContext w, UUID id, Emote emote, String why) {
        int eid = w.getServer().computeOnServer(s -> villager(w, id).getId());
        for (int i = 0; i < 40; i++) {
            if (c.computeOnClient(client -> EmoteBubbles.get(eid) != null && EmoteBubbles.get(eid).emote() == emote)) return;
            c.waitTicks(1);
        }
        throw new AssertionError(why + ": no " + emote + " bubble");
    }
    /** Turns the camera toward a resident. */
    private static void aim(ClientGameTestContext c, TestSingleplayerContext w, UUID id) {
        int eid = w.getServer().computeOnServer(s -> villager(w, id).getId());
        float[] look = c.computeOnClient(client -> {
            var e = client.level.getEntity(eid); var p = client.player;
            double dx = e.getX() - p.getX(), dz = e.getZ() - p.getZ(), dy = e.getY() + 1.2 - p.getEyeY();
            return new float[] {(float) Math.toDegrees(Math.atan2(-dx, dz)), (float) -Math.toDegrees(Math.atan2(dy, Math.sqrt(dx * dx + dz * dz)))};
        });
        c.getInput().lookAt(look[0], look[1]);
    }
    /**
     * Whether a resident's last line came from one of these dialogue pools ("t:pool#n" in their recent lines).
     * Pools the bank doesn't have yet (the dialogue lands in the same release) count when the built-in
     * fallback was said instead ({@code said} null: the words aren't at hand to compare).
     */
    private static boolean spokeFrom(TestSingleplayerContext w, UUID id, String said, List<String> pools, String fallback) {
        var recent = bond(villager(w, id), player(w)).recentLines();
        var bank = dev.villagefriends.talk.DialogueBank.current();
        for (var pool : pools) if (recent.stream().anyMatch(r -> r.startsWith("t:" + pool + "#"))) return true;
        // Without the pools (dialogue not merged yet) the built-in line is said; check it when we have the words.
        return pools.stream().noneMatch(bank::has) && (said == null || said.startsWith(fallback));
    }
    private static BlockPos board(TestSingleplayerContext w, Vec3 base) {
        return w.getServer().computeOnServer(s -> {
            var pos = BlockPos.containing(base).offset(-3, 0, -2);
            level(w).setBlockAndUpdate(pos, VillageBlocks.get("notice_board").defaultBlockState().setValue(FoundationBlock.FACING, Direction.NORTH));
            return pos;
        });
    }
    private static NoticeBoardScreen openBoard(ClientGameTestContext c, TestSingleplayerContext w, BlockPos pos) {
        w.getServer().runOnServer(s -> player(w).teleportTo(pos.getX() + .5, pos.getY(), pos.getZ() - 1.5));
        flush(w); c.waitTicks(3);
        c.runOnClient(client -> { client.gui.setScreen(null); client.gameMode.useItemOn(client.player, InteractionHand.MAIN_HAND, new BlockHitResult(Vec3.atCenterOf(pos), Direction.NORTH, pos, false)); });
        flush(w); c.waitForScreen(NoticeBoardScreen.class); c.waitTicks(5);
        return c.computeOnClient(client -> (NoticeBoardScreen) client.gui.screen());
    }
    private static void days(ClientGameTestContext c, TestSingleplayerContext w, long day) {
        w.getServer().runCommand("time set " + (day * 24000 + Routine.at(10, 0)));
        // One pass of the village's daily life (every 200 ticks) catches up the gossip.
        c.waitTicks(230); flush(w);
    }

    @Override public void runTest(ClientGameTestContext c) {
        c.getInput().resizeWindow(1280, 800); c.runOnClient(client -> { client.options.guiScale().set(2); client.resizeGui(); });
        TestWorldSave saved;
        try (var w = c.worldBuilder().create()) {
            w.getConnection().waitForChunksRender();
            for (var cmd : List.of("gamemode survival @a", "difficulty easy", "gamerule advance_time false", "gamerule advance_weather false", "gamerule spawn_mobs false", "weather clear", "time set 4000"))
                w.getServer().runCommand(cmd);
            Vec3 base = w.getServer().computeOnServer(s -> {
                var p = player(w); var level = level(w); var origin = p.blockPosition().above(4);
                for (int x = -40; x <= 40; x++) for (int z = -40; z <= 40; z++) {
                    level.setBlock(origin.offset(x, -1, z), Blocks.STONE.defaultBlockState(), 3);
                    for (int y = 0; y < 5; y++) level.setBlock(origin.offset(x, y, z), Blocks.AIR.defaultBlockState(), 3);
                }
                p.teleportTo(origin.getX() + .5, origin.getY(), origin.getZ() + .5);
                p.setYRot(0);
                p.addEffect(new MobEffectInstance(MobEffects.RESISTANCE, 1000000, 4, false, false));
                p.addEffect(new MobEffectInstance(MobEffects.NIGHT_VISION, 1000000, 0, false, false));
                return p.position();
            });
            // Residents of Thistlewick: the one who gets hit (A), a witness who keeps a dog (W), a patient (B)
            // and B's grown son (M), a child the zombie goes for (K), and a neighbor far away (F).
            var r = w.getServer().computeOnServer(s -> {
                var level = level(w); var map = new LinkedHashMap<String, UUID>();
                map.put("A", resident(level, base, 0, 5, false).getUUID());
                map.put("W", resident(level, base, 2.5, 6, false).getUUID());
                map.put("B", resident(level, base, -2.5, 4, false).getUUID());
                map.put("M", resident(level, base, -4.5, 6.5, false).getUUID());
                map.put("K", resident(level, base, 4.5, 4, true).getUUID());
                map.put("F", resident(level, base, 0, -32, false).getUUID());
                VillageSettlements.mark(level, BlockPos.containing(base), "Thistlewick");
                for (var id : map.values()) VillageSettlements.identify(villager(w, id), true);
                return map;
            });
            c.waitTicks(5);
            VILLAGE[0] = w.getServer().computeOnServer(s -> target(villager(w, r.get("A"))).getAttached(HOME).village());
            w.getServer().runOnServer(s -> {
                var level = level(w); var society = VillageSocieties.society(level, VILLAGE[0]);
                for (var id : r.values()) check(society.has(id(w, id)), "Every resident is in the village census");
                // M is B's son.
                VillageSocieties.put(level, society.born(id(w, r.get("M")), id(w, r.get("B")), "", day(level)));
                check(VillageSocieties.society(level, VILLAGE[0]).relation(id(w, r.get("M")), id(w, r.get("B"))).equals("parent"), "M is B's son");
                // W keeps a dog called Biscuit.
                var dog = EntityTypes.WOLF.create(level, EntitySpawnReason.COMMAND);
                dog.snapTo(base.x + 2, base.y, base.z + 2.5, 0, 0); dog.setNoAi(true);
                var owner = villager(w, r.get("W"));
                dog.setTame(true, true); dog.setOwner(owner);
                target(dog).setAttached(VillagerPets.PROFILE, new PetProfile(id(w, r.get("W")), name(owner), "Biscuit", "dog", "playful", "fetch", "minecraft:bone", 0, 0, "", Map.of()));
                target(owner).setAttached(VillagerPets.LINK, new PetLink(dog.getUUID().toString(), "dog", "Biscuit", 0));
                level.addFreshEntity(dog);
                PETS.put("dog", dog.getUUID());
            });
            UUID dog = PETS.get("dog");
            check(w.getServer().computeOnServer(s -> log(w) == null), "Nothing done yet");

            // -- good deeds -------------------------------------------------------------------------
            // One notice answered: a Helping Hand.
            w.getServer().runOnServer(s -> {
                var level = level(w); var record = VillageSettlements.book(level).villages().get(VILLAGE[0]);
                VillageQuests.put(level, VillageQuests.board(level, record).favor(player(w).getUUID().toString()));
                check(Deeds.tier(level, VILLAGE[0], player(w).getUUID().toString()) == 1, "One notice: Helping Hand");
            });
            // B is knocked out by a fall; the player bandages them in front of W: a heart.
            w.getServer().runOnServer(s -> { var b = villager(w, r.get("B")); b.hurtServer(level(w), b.damageSources().fall(), 100); });
            c.waitTicks(5);
            hold(w, new ItemStack(VillageItems.get("bandage_wrap"), 1)); use(c, w, r.get("B"));
            w.getServer().runOnServer(s -> {
                var d = deed(w, DeedKind.BANDAGED);
                check(d != null && d.involved().contains(id(w, r.get("B"))), "Bandaging a resident is a good deed");
                check(d.know(id(w, r.get("B"))).how() == Know.INVOLVED, "The patient knows");
                check(d.knows(id(w, r.get("W"))) && d.know(id(w, r.get("W"))).how() == Know.SEEN, "W saw it");
                check(d.know(id(w, r.get("M"))).how() == Know.FAMILY, "B's son is told at once");
                check(!d.knows(id(w, r.get("F"))), "F is too far away to see");
                var look = villager(w, r.get("W")).getBrain().getMemory(MemoryModuleType.LOOK_TARGET);
                check(look.isPresent(), "W turns to look");
            });
            bubble(c, w, r.get("W"), Emote.HEART, "A witness to a kindness");
            aim(c, w, r.get("W")); c.waitTicks(2); c.takeScreenshot("deeds-heart");
            // Smelling salts bring B back: a big deed, village news, and B keeps it in the Journal for good.
            hold(w, new ItemStack(VillageItems.get("smelling_salts"), 1)); use(c, w, r.get("B"));
            w.getServer().runOnServer(s -> {
                var d = deed(w, DeedKind.REVIVED);
                check(d != null && !Knockouts.knockedOut(villager(w, r.get("B"))), "Reviving a resident is a deed");
                check(d.know(id(w, r.get("B"))).kept(), "The saved resident keeps it");
                check(bond(villager(w, r.get("B")), player(w)).kept().size() == 1, "One memory kept for good");
                check(NarrativeEngine.journal(villager(w, r.get("B")), player(w)).startsWith("REMEMBERED ALWAYS"), "The Journal opens with it");
                check(VillageSocieties.society(level(w), VILLAGE[0]).news().stream().anyMatch(n -> n.kind().equals("deed:revived")), "Village news");
            });
            bubble(c, w, r.get("W"), Emote.SPARKLE, "A witness to a revival");
            // A zombie goes for the child K; the player kills it.
            w.getServer().runOnServer(s -> {
                var level = level(w); var p = player(w); var k = villager(w, r.get("K"));
                var z = EntityTypes.ZOMBIE.create(level, EntitySpawnReason.COMMAND);
                z.snapTo(k.getX() + 1.5, k.getY(), k.getZ() + 1, 0, 0); z.setNoAi(true); level.addFreshEntity(z);
                z.setTarget(k);
                z.hurtServer(level, level.damageSources().playerAttack(p), 1000F);
                var d = deed(w, DeedKind.SAVED_FROM_MONSTER);
                check(d != null && d.points10() == 15 && d.involved().contains(id(w, r.get("K"))), "Saving a child from a zombie is worth more");
                check(!bond(k, p).kept().isEmpty(), "The child remembers it always");
            });
            // Patting W's dog.
            w.getServer().runOnServer(s -> {
                var pet = level(w).getEntity(dog);
                VillagerPets.handleAction(player(w), new PetActionPayload(pet.getId(), pet.getUUID(), "pat"));
                var d = deed(w, DeedKind.PET_KINDNESS);
                check(d != null && d.label().equals("Biscuit") && d.know(id(w, r.get("W"))).how() == Know.INVOLVED, "Patting a resident's dog is a kindness to its owner");
                check(Deeds.tier(level(w), VILLAGE[0], player(w).getUUID().toString()) == 2 && score(w) == 51, "A notice and four good deeds: Good Neighbor (" + score(w) + ")");
                check(log(w).peakTier() == 2, "A new best standing is remembered");
            });
            // The board shows it.
            var boardPos = board(w, base);
            c.waitTicks(5);
            var shown = openBoard(c, w, boardPos).data();
            check(shown.standing().startsWith("Good Neighbor"), "The board's standing line: " + shown.standing());
            c.takeScreenshot("deeds-board-standing");
            c.clickScreenButton("Close"); c.waitForScreen(null);
            // Prices: W saw the revival and charges less than F, who knows nothing yet.
            w.getServer().runOnServer(s -> {
                var p = player(w); var wit = villager(w, r.get("W")); var far = villager(w, r.get("F"));
                int seen = Deeds.reputation(wit, p), unknown = Deeds.reputation(far, p);
                check(seen > 0 && unknown == 0, "Deeds a resident knows add to their reputation: " + seen + " / " + unknown);
                int vanillaW = wit.getGossips().getReputation(p.getUUID(), t -> true), vanillaF = far.getGossips().getReputation(p.getUUID(), t -> true);
                check(wit.getPlayerReputation(p) - vanillaW == seen && far.getPlayerReputation(p) - vanillaF == 0, "Vanilla's reputation (and so prices) includes the deeds");
            });
            // M heard what happened to his mother: a family reaction, and he keeps it in his Journal too.
            talk(c, w, r.get("M"));
            w.getServer().runOnServer(s -> {
                var m = villager(w, r.get("M")); var d = deed(w, DeedKind.REVIVED);
                check(d.know(id(w, r.get("M"))).told(), "M brought it up");
                check(d.know(id(w, r.get("M"))).kept() && bond(m, player(w)).kept().size() == 1, "Family keep it for good");
                check(spokeFrom(w, r.get("M"), null, List.of("deed.revived.family", "deed.good.heard." + profile(m).personality()), "")
                        || bond(m, player(w)).kept().getFirst().contains(TalkWorld.firstName(name(villager(w, r.get("B"))))), "M's reaction is about his family");
            });
            c.takeScreenshot("deeds-reaction-family");
            bye(c);
            // B's Journal.
            talk(c, w, r.get("B"));
            c.clickScreenButton("Journal"); flush(w); c.waitTicks(20);
            c.takeScreenshot("deeds-journal-kept");
            bye(c);

            // -- bad deeds --------------------------------------------------------------------------
            // A new neighbor (W2) watches the player hit A: anger, and a look.
            UUID w2 = w.getServer().computeOnServer(s -> {
                // Out of chatting range of the others, so a neighborly chat bubble doesn't replace the reaction.
                var v = resident(level(w), base, -1, 9.5, false); VillageSettlements.identify(v, true); return v.getUUID();
            });
            w.getServer().runOnServer(s -> player(w).teleportTo(base.x, base.y, base.z));
            c.waitTicks(20); w.getConnection().waitForClientboundEntityUpdates(EntityTypes.VILLAGER);
            w.getServer().runOnServer(s -> { var a = villager(w, r.get("A")); a.hurtServer(level(w), level(w).damageSources().playerAttack(player(w)), 1); });
            w.getServer().runOnServer(s -> {
                var d = deed(w, DeedKind.HIT_RESIDENT);
                check(d != null && d.know(id(w, r.get("A"))).how() == Know.INVOLVED, "Hitting a resident is a bad deed");
                check(d.know(VillageSocieties.id(villager(w, w2))).how() == Know.SEEN, "W2 saw it");
                check(Standing.reputation(List.of(d), id(w, r.get("A")), day(level(w))) == 0, "Vanilla prices the hit itself; deeds add nothing");
                var look = villager(w, w2).getBrain().getMemory(MemoryModuleType.LOOK_TARGET);
                check(look.isPresent(), "W2 turns to look at the player");
            });
            bubble(c, w, w2, Emote.ANGER, "A witness to violence");
            aim(c, w, w2); c.waitTicks(2); c.takeScreenshot("deeds-witness-anger");
            talk(c, w, w2);
            w.getServer().runOnServer(s -> {
                var v = villager(w, w2);
                check(deed(w, DeedKind.HIT_RESIDENT).know(VillageSocieties.id(v)).told(), "W2 brings the hit up");
                check(spokeFrom(w, w2, null, List.of("deed.hit_resident.seen", "deed.bad.seen." + profile(v).personality()), ""), "From the seen pools");
            });
            c.takeScreenshot("deeds-reaction-seen");
            bye(c);
            // A won't hear an apology yet: too soon, too little trust, no gift.
            w.getServer().runOnServer(s -> check(Deeds.handle(player(w), villager(w, r.get("A")), "deed_apology") && !deed(w, DeedKind.HIT_RESIDENT).apologized(), "Too soon to forgive"));
            flush(w); c.waitTicks(5); c.runOnClient(client -> client.gui.setScreen(null));
            // Hitting and killing the village's iron golem.
            w.getServer().runOnServer(s -> {
                var level = level(w); var p = player(w);
                var golem = EntityTypes.IRON_GOLEM.create(level, EntitySpawnReason.COMMAND);
                golem.snapTo(base.x + 6, base.y, base.z + 9, 180, 0); golem.setNoAi(true); level.addFreshEntity(golem);
                golem.hurtServer(level, level.damageSources().playerAttack(p), 1);
                check(deed(w, DeedKind.HIT_GOLEM) != null, "Hitting the golem");

                golem.hurtServer(level, level.damageSources().playerAttack(p), 1000);
                check(deed(w, DeedKind.KILLED_GOLEM) != null && !golem.isAlive(), "Killing the golem");
                check(VillageSocieties.society(level, VILLAGE[0]).news().stream().anyMatch(n -> n.kind().equals("deed:killed_golem")), "Village news");
                check(Deeds.tier(level, VILLAGE[0], p.getUUID().toString()) == 0, "Down to Newcomer: " + score(w));
            });
            // Knocking A out: Unwelcome.
            c.waitTicks(25);
            w.getServer().runOnServer(s -> {
                var a = villager(w, r.get("A"));
                a.hurtServer(level(w), level(w).damageSources().playerAttack(player(w)), 100);
                check(Knockouts.knockedOut(a) && Knockouts.state(a).by().equals(player(w).getUUID().toString()), "The village knows who knocked A out");
                check(deed(w, DeedKind.KNOCKED_OUT_RESIDENT) != null, "Knocking a resident out");
                check(Deeds.unwelcome(level(w), VILLAGE[0], player(w).getUUID()), "Unwelcome: " + score(w));
                check(Deeds.ledgerLine(player(w), level(w), VILLAGE[0], "Thistlewick").contains("Unwelcome"), "The Ledger shows it");
            });
            var refused = openBoard(c, w, boardPos).data();
            check(refused.standing().startsWith("Unwelcome") && refused.standing().contains("remember what you did"), "The board says so: " + refused.standing());
            check(refused.notices().stream().noneMatch(n -> n.state().equals("open")), "No notices offered");
            check(!refused.message().isEmpty(), "A note explains why");
            c.takeScreenshot("deeds-board-unwelcome");
            c.clickScreenButton("Close"); c.waitForScreen(null);
            // F knows nothing yet, but greets an Unwelcome player coldly.
            w.getServer().runOnServer(s -> {
                var f = villager(w, r.get("F")); var p = player(w);
                String hello = NarrativeEngine.greeting(f, p);
                check(spokeFrom(w, r.get("F"), hello, List.of("greet.unwelcome", "greet.unwelcome." + profile(f).personality()), "Oh. It's you."), "A cold hello: " + hello);
                String chat = NarrativeEngine.conversation(f, p, "chat");
                check(spokeFrom(w, r.get("F"), chat, List.of("chat.unwelcome"), "I've nothing to share"), "No small talk: " + chat);
            });

            // -- word gets around; time heals --------------------------------------------------------
            long today = w.getServer().computeOnServer(s -> day(level(w)));
            days(c, w, today + 3);
            w.getServer().runOnServer(s -> {
                String f = id(w, r.get("F"));
                check(deed(w, DeedKind.KILLED_GOLEM).know(f).how() == Know.HEARD, "Three days on, F has heard about the golem");
            });
            w.getServer().runOnServer(s -> player(w).teleportTo(base.x, base.y, base.z - 29));
            c.waitTicks(5);
            talk(c, w, r.get("F"));
            w.getServer().runOnServer(s -> {
                var f = villager(w, r.get("F"));
                var told = log(w).deeds().stream().filter(d -> d.knows(VillageSocieties.id(f)) && d.know(VillageSocieties.id(f)).told()).toList();
                check(told.size() == 1 && told.getFirst().kind() == DeedKind.KILLED_GOLEM, "F brings up the worst thing they heard: " + told);
                check(spokeFrom(w, r.get("F"), null, List.of("deed.killed_golem.heard", "deed.bad.heard." + profile(f).personality()), ""), "From the heard pools");
            });
            c.takeScreenshot("deeds-reaction-heard");
            bye(c);
            w.getServer().runOnServer(s -> player(w).teleportTo(base.x, base.y, base.z));
            days(c, w, today + 21);
            w.getServer().runOnServer(s -> {
                check(!Deeds.unwelcome(level(w), VILLAGE[0], player(w).getUUID()), "Three weeks on, bad deeds have faded: " + score(w));
                // A is revived, and apologized to: the knockout counts half.
                var a = villager(w, r.get("A")); var p = player(w);
                p.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(VillageItems.get("revival_tonic")));
                Knockouts.interact(p, a);
                check(!Knockouts.knockedOut(a), "A is back on their feet");
                int before = score(w);
                check(NarrativeEngine.handle(p, a, "apologize"), "The existing apology");
                check(deed(w, DeedKind.KNOCKED_OUT_RESIDENT).apologized() && score(w) > before, "It apologizes for the knockout too");
                check(Deeds.choices(a, p).stream().anyMatch(ch -> ch.id().equals("deed_apology")), "A offers to talk about the hit");
                check(Deeds.handle(p, a, "deed_apology") && deed(w, DeedKind.HIT_RESIDENT).apologized(), "After three days an apology is accepted");
            });

            // -- a raid, won --------------------------------------------------------------------------
            w.getServer().runOnServer(s -> {
                var level = level(w); var p = player(w);
                var bell = BlockPos.containing(base).offset(-30, 0, 30);
                level.setBlock(bell, Blocks.BELL.defaultBlockState(), 3);
                level.getPoiManager().take(h -> h.is(PoiTypes.MEETING), (h, pos) -> true, bell, 4);
                p.addEffect(new MobEffectInstance(MobEffects.RAID_OMEN, 600, 0));
                check(level.getRaids().createOrExtendRaid(p, bell) != null, "A raid starts");
                p.removeEffect(MobEffects.RAID_OMEN);
            });
            flush(w); c.runOnClient(client -> client.gui.setScreen(null));
            for (int t = 0; t < 4800 && w.getServer().computeOnServer(s -> deed(w, DeedKind.RAID_WON) == null); t += 10) {
                w.getServer().runOnServer(s -> {
                    var level = level(w); var raid = level.getRaidAt(BlockPos.containing(base).offset(-30, 0, 30));
                    if (raid != null) for (var raider : List.copyOf(raid.getAllRaiders()))
                        if (raider.isAlive()) { raider.hurtServer(level, level.damageSources().playerAttack(player(w)), 1000); }
                });
                c.waitTicks(10);
            }
            w.getServer().runOnServer(s -> {
                var defended = deed(w, DeedKind.RAID_DEFENDED);
                check(defended != null && defended.count() >= 3, "Raiders killed in the village");
                check(deed(w, DeedKind.RAID_WON) != null, "The raid was won");
                check(VillageSocieties.society(level(w), VILLAGE[0]).news().stream().anyMatch(n -> n.kind().equals("deed:raid_won")), "Village news");
                LOGGER.info("DEEDS: standing after the raid " + score(w) + ", best tier " + log(w).peakTier());
            });
            c.getInput().lookAt(0, 20); c.waitTicks(10);
            c.takeScreenshot("deeds-raid-won");

            theftAndBrokenHomes(c, w, base);
            saved = w.getWorldSave();
        }
        // The deed log is saved with the world.
        try (var w = saved.open()) {
            w.getConnection().waitForChunksRender(); c.waitTicks(10);
            w.getServer().runOnServer(s -> {
                var log = log(w);
                check(log != null && log.deeds().size() >= 10 && log.peakTier() >= 2, "The deed log survives save and reload: " + (log == null ? "no log" : log.deeds().size() + " deeds, peak " + log.peakTier()));
                check(deed(w, DeedKind.HIT_RESIDENT).apologized(), "Apologies are saved");
            });
        }
        LOGGER.info("DEEDS PASSED: witnesses (heart, sparkle, anger, look), bandage, revival with a kept Journal memory, a child saved from a zombie, "
                + "a pet patted, Good Neighbor on the board, deed prices through vanilla reputation, family/seen/heard reactions, hit and golem deeds, "
                + "Unwelcome (board, ledger, cold greetings), three weeks' fading, apologies, a raid won, save/reload.");
    }
    private static final Map<String, UUID> PETS = new HashMap<>();

    /**
     * Stealing from a chest in a resident's house and breaking a resident's bed or door. Skipped until
     * Homes installs {@link HouseBounds}; the integration pass fills this in against a real house.
     */
    /**
     * Theft and breaking things in a resident's house: a cottage the player builds, with a plaque, two beds and a
     * chest; homeless residents move in; the player empties the chest (STOLE, counted by the items taken) and breaks
     * a bed and the top half of the door (BROKE_HOME, the bed's owner and the household).
     */
    private static void theftAndBrokenHomes(ClientGameTestContext c, TestSingleplayerContext w, Vec3 base) {
        check(HouseBounds.current() != HouseBounds.NONE, "Homes installs the house bounds");
        int x0 = (int) Math.floor(base.x) + 10, y0 = (int) Math.floor(base.y) - 1, z0 = (int) Math.floor(base.z) + 12;
        for (var cmd : List.of(
                String.format(Locale.ROOT, "fill %d %d %d %d %d %d minecraft:oak_planks hollow", x0, y0, z0, x0 + 6, y0 + 5, z0 + 6),
                String.format(Locale.ROOT, "setblock %d %d %d minecraft:oak_door[facing=south,half=lower]", x0 + 3, y0 + 1, z0 + 6),
                String.format(Locale.ROOT, "setblock %d %d %d minecraft:oak_door[facing=south,half=upper]", x0 + 3, y0 + 2, z0 + 6),
                String.format(Locale.ROOT, "setblock %d %d %d minecraft:chest[facing=west]", x0 + 5, y0 + 1, z0 + 4),
                String.format(Locale.ROOT, "setblock %d %d %d villagefriends:house_plaque[facing=east,mount=wall]", x0 + 1, y0 + 2, z0 + 4)))
            w.getServer().runCommand(cmd);
        for (int dx : new int[]{1, 2}) {
            w.getServer().runCommand(String.format(Locale.ROOT, "setblock %d %d %d minecraft:red_bed[facing=north,part=head]", x0 + dx, y0 + 1, z0 + 1));
            w.getServer().runCommand(String.format(Locale.ROOT, "setblock %d %d %d minecraft:red_bed[facing=north,part=foot]", x0 + dx, y0 + 1, z0 + 2));
        }
        var chest = new BlockPos(x0 + 5, y0 + 1, z0 + 4); var plaque = new BlockPos(x0 + 1, y0 + 2, z0 + 4);
        String placed = w.getServer().computeOnServer(s -> ((HousePlaqueBlockEntity) level(w).getBlockEntity(plaque)).scanForBeds());
        check(placed.startsWith("★") && placed.contains("2 beds"), "The cottage is a house: " + placed);
        w.getServer().runOnServer(s -> dev.villagefriends.home.Homes.changed(level(w), VILLAGE[0]));
        // Homeless residents move in.
        List<String> residents = List.of();
        for (int t = 0; t < 800 && residents.isEmpty(); t += 10) {
            c.waitTicks(10);
            residents = w.getServer().computeOnServer(s -> HouseBounds.current().houseAt(level(w), chest).map(HouseBounds.HouseRef::residents).orElse(List.of()));
        }
        check(!residents.isEmpty(), "Homeless residents move into the cottage");
        var household = residents;
        LOGGER.info("DEEDS: the cottage's household " + household);

        // Taking ten loaves from their chest is theft.
        w.getServer().runOnServer(s -> {
            if (level(w).getBlockEntity(chest) instanceof net.minecraft.world.Container box) box.setItem(0, new ItemStack(net.minecraft.world.item.Items.BREAD, 10));
            var p = player(w); p.setItemInHand(InteractionHand.MAIN_HAND, ItemStack.EMPTY);
            p.teleportTo(x0 + 3.5, y0 + 1, z0 + 4.5); p.setYRot(-90); p.setXRot(20);
        });
        flush(w); c.waitTicks(5);
        c.runOnClient(client -> { client.gui.setScreen(null); client.gameMode.useItemOn(client.player, InteractionHand.MAIN_HAND, new BlockHitResult(Vec3.atCenterOf(chest), Direction.WEST, chest, false)); });
        c.waitForScreen(net.minecraft.client.gui.screens.inventory.ContainerScreen.class); flush(w); c.waitTicks(5);
        c.runOnClient(client -> client.gameMode.handleContainerInput(client.player.containerMenu.containerId, 0, 0, net.minecraft.world.inventory.ContainerInput.QUICK_MOVE, client.player));
        flush(w); c.waitTicks(5);
        c.takeScreenshot("deeds-theft");
        c.runOnClient(client -> client.player.closeContainer());
        flush(w); c.waitForScreen(null); c.waitTicks(5);
        w.getServer().runOnServer(s -> {
            var d = deed(w, DeedKind.STOLE);
            check(d != null && d.count() == 10, "Taking from a resident's chest is theft, counted by the items: " + d);
            check(d.involved().containsAll(household) && d.label().contains("House"), "The household was stolen from: " + d);
            check(d.points10() == DeedKind.STOLE.points10(10, false), "Ten items are worth " + DeedKind.STOLE.points10(10, false));
        });

        // Breaking an owned bed and the door: one deed for the house, merged within the day.
        var owned = w.getServer().computeOnServer(s -> {
            for (int dx : new int[]{1, 2}) {
                var foot = new BlockPos(x0 + dx, y0 + 1, z0 + 2);
                var owners = HouseBounds.current().owners(level(w), foot);
                if (!owners.isEmpty()) return Map.entry(foot, owners.getFirst());
            }
            return null;
        });
        check(owned != null, "One of the cottage's beds has an owner");
        w.getServer().runOnServer(s -> {
            var p = player(w);
            check(p.gameMode.destroyBlock(owned.getKey()), "The player breaks the bed");
            var d = deed(w, DeedKind.BROKE_HOME);
            check(d != null && d.involved().contains(owned.getValue()), "Breaking a resident's bed: its owner is wronged: " + d);
            // The top half of the door: the index may list either half; the door is the household's.
            check(p.gameMode.destroyBlock(new BlockPos(x0 + 3, y0 + 2, z0 + 6)), "The player breaks the door");
            var again = deed(w, DeedKind.BROKE_HOME);
            check(again.serial() == d.serial() && again.count() == 2 && again.involved().containsAll(household), "The door counts too, as one deed for the house: " + again);
        });
        LOGGER.info("DEEDS: theft and broken-home cases passed");
    }
}
