package dev.villagefriends;

import static dev.villagefriends.VillageFriends.*;

import dev.villagefriends.client.LedgerScreen;
import dev.villagefriends.home.FloodFill;
import dev.villagefriends.home.House;
import dev.villagefriends.home.HouseCatalog;
import dev.villagefriends.home.HouseSurvey;
import dev.villagefriends.home.Homes;
import dev.villagefriends.home.HousingBook;
import dev.villagefriends.home.HousingIndex;
import dev.villagefriends.pet.PetKeeping;
import dev.villagefriends.pet.PetLink;
import dev.villagefriends.pet.VillagerPets;
import dev.villagefriends.quest.Notice;
import dev.villagefriends.routine.Routine;
import dev.villagefriends.social.Society;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Random;
import java.util.UUID;
import java.util.function.BooleanSupplier;
import java.util.function.Supplier;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.fabricmc.fabric.api.client.gametest.v1.world.TestWorldSave;
import net.minecraft.client.gui.screens.worldselection.WorldCreationUiState;
import net.minecraft.core.BlockPos;
import net.minecraft.core.GlobalPos;
import net.minecraft.core.HolderSet;
import net.minecraft.core.registries.Registries;
import net.minecraft.nbt.NbtOps;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.TamableAnimal;
import net.minecraft.world.entity.ai.memory.MemoryModuleType;
import net.minecraft.world.entity.animal.feline.Cat;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.level.ChunkPos;
import net.minecraft.world.level.block.AbstractBedBlock;
import net.minecraft.world.level.block.HorizontalDirectionalBlock;
import net.minecraft.world.level.block.state.properties.BedPart;
import net.minecraft.world.level.levelgen.densityfunction.SamplerContext;
import net.minecraft.world.level.levelgen.presets.WorldPresets;
import net.minecraft.world.level.levelgen.structure.BoundingBox;
import net.minecraft.world.level.levelgen.structure.PoolElementStructurePiece;
import net.minecraft.world.level.levelgen.structure.StructureStart;
import net.minecraft.world.level.levelgen.structure.pools.SinglePoolElement;

/**
 * Homes and beds in the world: a house a player built and plaqued, a homeless couple moving in, the plaque's
 * readout, a house open to the sky and one too big, a broken bed, a newborn's bed, a knocked-out resident
 * helped into their own bed with their cat beside it, a death that frees a bed, the Ledger and the "bigger
 * house" notice, save and reload, the houses of all five village types read from their structures, and
 * bedtime in a naturally generated village. Screenshots are named {@code homes-*}.
 */
@SuppressWarnings("UnstableApiUsage")
public final class HomesGameTest implements FabricClientGameTest {
    private static void check(boolean ok, String why) { if (!ok) throw new AssertionError(why); }
    private static Villager villager(TestSingleplayerContext w, UUID id) { return (Villager) w.getConnection().getServerLevel().getEntity(id); }
    private static ServerLevel level(TestSingleplayerContext w) { return w.getConnection().getServerLevel(); }
    private static void until(ClientGameTestContext c, BooleanSupplier test, int ticks, Supplier<String> what) {
        for (int i = 0; i < ticks; i += 5) { if (test.getAsBoolean()) return; c.waitTicks(5); }
        if (!test.getAsBoolean()) throw new AssertionError("Timed out: " + what.get());
    }
    private static boolean onServer(TestSingleplayerContext w, Supplier<Boolean> test) { return w.getServer().computeOnServer(s -> test.get()); }
    private static void cmd(TestSingleplayerContext w, String format, Object... args) { w.getServer().runCommand(String.format(Locale.ROOT, format, args)); }
    private static void view(ClientGameTestContext c, TestSingleplayerContext w, double x, double y, double z, float yaw, float pitch, String name) {
        cmd(w, "tp @a %.2f %.2f %.2f %.1f %.1f", x, y, z, yaw, pitch);
        c.waitTicks(40);
        c.runOnClient(client -> client.gui.toastManager().clear());
        c.takeScreenshot("homes-" + name);
    }
    private static String id(TestSingleplayerContext w, UUID v) { return w.getServer().computeOnServer(s -> profile(villager(w, v)).id()); }
    private static Villager spawn(ServerLevel level, double x, double y, double z, String job) {
        var v = new Villager(EntityTypes.VILLAGER, level);
        v.setPos(x, y, z);
        if (job != null) {
            var key = VillageProfessions.JOBS.contains(job) ? VillageProfessions.key(job)
                    : ResourceKey.create(Registries.VILLAGER_PROFESSION, net.minecraft.resources.Identifier.withDefaultNamespace(job));
            v.setVillagerData(v.getVillagerData().withProfession(level.registryAccess(), key)); v.setVillagerXp(1);
        }
        level.addFreshEntity(v);
        return v;
    }

    @Override public void runTest(ClientGameTestContext c) {
        c.getInput().resizeWindow(1280, 800);
        TestWorldSave saved;
        Map<String, HousingIndex.BedKey> before;
        String village;
        try (var w = c.worldBuilder().adjustSettings(ui -> {
            var flat = ui.getSettings().worldgenLoadContext().lookupOrThrow(Registries.WORLD_PRESET).getOrThrow(WorldPresets.FLAT);
            ui.setWorldType(new WorldCreationUiState.WorldTypeEntry(flat));
            ui.setGenerateStructures(false);
            ui.setSeed("23");
        }).create()) {
            for (int attempt = 0; attempt < 3; attempt++) { try { w.getConnection().waitForChunksRender(); break; } catch (AssertionError slow) { c.waitTicks(100); } }
            for (var command : List.of("gamerule advance_time false", "gamerule advance_weather false", "gamerule spawn_mobs false", "weather clear",
                    "difficulty peaceful", "gamemode creative @a", "time set 4000"))
                w.getServer().runCommand(command);
            BlockPos base = w.getServer().computeOnServer(s -> w.getConnection().getServerPlayer().blockPosition());
            int x0 = base.getX() + 10, y0 = base.getY() - 1, z0 = base.getZ() + 10;
            village = w.getServer().computeOnServer(s -> VillageSettlements.mark(level(w), base, "Ashford").id());

            // --- A house a player built: a 7x5x7 cottage with a door, two beds and a plaque.
            cmd(w, "fill %d %d %d %d %d %d minecraft:oak_planks hollow", x0, y0, z0, x0 + 6, y0 + 5, z0 + 6);
            cmd(w, "setblock %d %d %d minecraft:oak_door[facing=south,half=lower]", x0 + 3, y0 + 1, z0 + 6);
            cmd(w, "setblock %d %d %d minecraft:oak_door[facing=south,half=upper]", x0 + 3, y0 + 2, z0 + 6);
            for (int dx : new int[]{1, 2}) {
                cmd(w, "setblock %d %d %d minecraft:red_bed[facing=north,part=head]", x0 + dx, y0 + 1, z0 + 1);
                cmd(w, "setblock %d %d %d minecraft:red_bed[facing=north,part=foot]", x0 + dx, y0 + 1, z0 + 2);
            }
            var plaque = new BlockPos(x0 + 1, y0 + 2, z0 + 4);
            cmd(w, "setblock %d %d %d villagefriends:house_plaque[facing=east,mount=wall]", plaque.getX(), plaque.getY(), plaque.getZ());
            String placed = w.getServer().computeOnServer(s -> ((HousePlaqueBlockEntity) level(w).getBlockEntity(plaque)).scanForBeds());
            check(placed.startsWith("★") && placed.contains("1 room") && placed.contains("2 beds"), "The plaque finds the house's room and beds: " + placed);
            String houseId = "p:" + plaque.getX() + "," + plaque.getY() + "," + plaque.getZ();
            w.getServer().runOnServer(s -> {
                var h = Homes.index(level(w), village).house(houseId);
                check(h != null && h.kind() == House.Kind.PLAYER && h.presentBeds().size() == 2 && h.doors().size() == 2, "The player's house is in the index with its door: " + h);
            });

            // --- A homeless couple moves in.
            UUID a = w.getServer().computeOnServer(s -> spawn(level(w), x0 + 3.5, y0 + 1, z0 + 9, "farmer").getUUID());
            UUID b = w.getServer().computeOnServer(s -> spawn(level(w), x0 + 4.5, y0 + 1, z0 + 9, "fisherman").getUUID());
            until(c, () -> onServer(w, () -> VillageSocieties.of(villager(w, a)) != null && VillageSocieties.of(villager(w, b)) != null
                    && VillageSocieties.of(villager(w, b)).has(profile(villager(w, b)).id())), 200, () -> "the couple settles in Ashford");
            String idA = id(w, a), idB = id(w, b);
            w.getServer().runOnServer(s -> {
                var society = VillageSocieties.society(level(w), village); long today = day(level(w));
                var folk = new HashMap<>(society.folk());
                folk.put(idA, folk.get(idA).partner(idB, today, true)); folk.put(idB, folk.get(idB).partner(idA, today, true));
                VillageSocieties.put(level(w), new Society(society.village(), folk, society.ties(), society.news(), society.day()));
                Homes.changed(level(w), village);
            });
            until(c, () -> onServer(w, () -> { var i = Homes.index(level(w), village); var h = i.houseOf(idA); return h != null && h.id().equals(houseId) && houseId.equals(i.houseOf(idB) == null ? "" : i.houseOf(idB).id()); }),
                    400, () -> "the couple moves into the player's house: " + w.getServer().computeOnServer(s -> Homes.index(level(w), village).beds().toString()));
            until(c, () -> onServer(w, () -> villager(w, a).getBrain().getMemory(MemoryModuleType.HOME).map(GlobalPos::pos)
                    .equals(Homes.index(level(w), village).bedOf(idA).map(House.Bed::head))), 100, () -> "their vanilla home is their own bed");
            w.getServer().runOnServer(s -> {
                var i = Homes.index(level(w), village);
                check(i.bedOf(idA).orElseThrow().beside(i.bedOf(idB).orElseThrow()), "Partners sleep side by side");
                check(i.needs().isEmpty() && i.homeless().isEmpty(), "Nobody is short of room now: " + i.needs());
            });

            // --- The plaque's readout.
            w.getServer().runOnServer(s -> {
                var i = Homes.index(level(w), village);
                var lines = Homes.readout(level(w), i, i.house(houseId)).stream().map(l -> l.getString()).toList();
                LOGGER.info("HOMES READOUT: {}", lines);
                check(lines.getFirst().contains("House"), "The house is named after its family: " + lines.getFirst());
                check(lines.get(1).startsWith("Lives here:") && lines.get(1).contains(name(villager(w, a)).split(" ")[0]) && lines.get(1).contains("Farmer"), "Who lives there: " + lines.get(1));
                check(lines.get(2).startsWith("Beds: 2 of 2 used"), "How many beds are used: " + lines.get(2));
                Homes.readout(w.getConnection().getServerPlayer(), plaque);
            });
            view(c, w, x0 + 4.5, y0 + 1, z0 + 3.5, 90, 10, "plaque-readout");
            view(c, w, x0 + 4.5, y0 + 2.2, z0 + 5.3, 150, 25, "player-house");

            // --- A hole in the roof opens the house to the sky; a huge hall is too big.
            cmd(w, "setblock %d %d %d minecraft:air", x0 + 3, y0 + 5, z0 + 3);
            String open = w.getServer().computeOnServer(s -> Homes.scanPlaque(level(w), plaque, ""));
            check(open.contains("open to the sky above " + (x0 + 3) + " ") && open.endsWith(" " + (z0 + 3) + "."), "The plaque says where the house is open: " + open);
            until(c, () -> onServer(w, () -> Homes.index(level(w), village).house(houseId).beds().isEmpty()), 100, () -> "an open house has no beds to give");
            w.getServer().runOnServer(s -> Homes.readout(w.getConnection().getServerPlayer(), plaque));
            view(c, w, x0 + 3.5, y0 + 1, z0 + 4.5, 180, -70, "player-house-open");
            cmd(w, "setblock %d %d %d minecraft:oak_planks", x0 + 3, y0 + 5, z0 + 3);
            // Walls and roofs aren't watched block by block: using the plaque looks the house over again.
            String mended = w.getServer().computeOnServer(s -> Homes.scanPlaque(level(w), plaque, ""));
            check(mended.startsWith("★") && mended.contains("2 beds"), "The mended house is whole again: " + mended);
            until(c, () -> onServer(w, () -> Homes.index(level(w), village).house(houseId).beds().size() == 2 && Homes.index(level(w), village).houseOf(idA) != null),
                    400, () -> "the mended house takes its residents back");
            w.getServer().runOnServer(s -> { for (int cx = (x0 + 30) >> 4; cx <= (x0 + 75) >> 4; cx++) for (int cz = (z0 - 75) >> 4; cz <= (z0 - 30) >> 4; cz++) level(w).getChunk(cx, cz); });
            cmd(w, "fill %d %d %d %d %d %d minecraft:stone_bricks hollow", x0 + 30, y0, z0 - 72, x0 + 71, y0 + 11, z0 - 31);
            var hall = new BlockPos(x0 + 31, y0 + 2, z0 - 50);
            cmd(w, "setblock %d %d %d villagefriends:house_plaque[facing=east,mount=wall]", hall.getX(), hall.getY(), hall.getZ());
            String big = w.getServer().computeOnServer(s -> Homes.scanPlaque(level(w), hall, ""));
            check(big.contains("too big"), "A 40x10x40 hall is too big for a house: " + big);
            check(FloodFill.MAX_CELLS == 6000, "The house size limit");

            // --- A broken bed: the house is looked at again and its owner is short of a bed.
            HousingIndex.BedKey brokenKey = w.getServer().computeOnServer(s -> Homes.index(level(w), village).beds().get(idA));
            cmd(w, "setblock %d %d %d minecraft:air destroy", brokenKey.head().getX(), brokenKey.head().getY(), brokenKey.head().getZ());
            until(c, () -> onServer(w, () -> { var i = Homes.index(level(w), village); return !i.beds().containsKey(idA) && i.needOf(idA) != null; }), 200,
                    () -> "the owner of a broken bed is flagged: " + w.getServer().computeOnServer(s -> Homes.index(level(w), village).needs().toString()));
            w.getServer().runOnServer(s -> check(HousingIndex.CROWDED.equals(Homes.index(level(w), village).needOf(idA).kind()), "A household short of a bed is crowded"));

            // --- The bed is mended and a third added; a baby is born and gets a bed in the family's house.
            var foot = brokenKey.head().south();
            cmd(w, "setblock %d %d %d minecraft:red_bed[facing=north,part=head]", brokenKey.head().getX(), brokenKey.head().getY(), brokenKey.head().getZ());
            cmd(w, "setblock %d %d %d minecraft:red_bed[facing=north,part=foot]", foot.getX(), foot.getY(), foot.getZ());
            cmd(w, "setblock %d %d %d minecraft:red_bed[facing=north,part=head]", x0 + 5, y0 + 1, z0 + 1);
            cmd(w, "setblock %d %d %d minecraft:red_bed[facing=north,part=foot]", x0 + 5, y0 + 1, z0 + 2);
            until(c, () -> onServer(w, () -> Homes.index(level(w), village).house(houseId).presentBeds().size() == 3), 200, () -> "the house counts three beds");
            UUID baby = w.getServer().computeOnServer(s -> {
                var child = new Villager(EntityTypes.VILLAGER, level(w));
                target(child).setAttached(PARENTS, idA + "|" + idB);
                child.setAge(-24000); child.setPos(x0 + 3.5, y0 + 1, z0 + 9.5);
                level(w).addFreshEntity(child);
                return child.getUUID();
            });
            until(c, () -> onServer(w, () -> villager(w, baby) != null && VillageSocieties.of(villager(w, baby)) != null && VillageSocieties.of(villager(w, baby)).has(profile(villager(w, baby)).id())),
                    200, () -> "the baby joins the family");
            String idBaby = id(w, baby);
            until(c, () -> onServer(w, () -> { var h = Homes.index(level(w), village).houseOf(idBaby); return h != null && h.id().equals(houseId); }), 400,
                    () -> "the newborn gets a bed in their parents' house: " + w.getServer().computeOnServer(s -> Homes.index(level(w), village).needs().toString()));
            w.getServer().runOnServer(s -> check(Homes.index(level(w), village).houseOf(idA).id().equals(houseId), "Their parents still live there too"));

            // --- A knocked-out resident is helped into their own bed, and their cat curls up beside it.
            UUID cat = w.getServer().computeOnServer(s -> {
                var level = level(w); var owner = villager(w, a);
                var pet = new Cat(EntityTypes.CAT, level);
                pet.setPos(x0 + 3.5, y0 + 1, z0 + 11.5);
                pet.setTame(true, true); pet.setOwner(owner); pet.setPersistenceRequired();
                var profile = PetKeeping.newProfile(new Random(5), "cat", idA, name(owner), day(level), false);
                target(pet).setAttached(VillagerPets.PROFILE, profile); pet.setCustomName(net.minecraft.network.chat.Component.literal(profile.name()));
                target(owner).setAttached(VillagerPets.LINK, new PetLink(pet.getUUID().toString(), "cat", profile.name(), day(level)));
                level.addFreshEntity(pet);
                return pet.getUUID();
            });
            UUID healer = w.getServer().computeOnServer(s -> spawn(level(w), x0 + 3.5, y0 + 1, z0 + 20.5, "apothecary").getUUID());
            w.getServer().runOnServer(s -> { var v = villager(w, a); v.teleportTo(x0 + 3.5, y0 + 1, z0 + 14.5); v.hurtServer(level(w), v.damageSources().generic(), 100); });
            check(onServer(w, () -> Knockouts.knockedOut(villager(w, a))), "A fatal blow knocks them out");
            HousingIndex.BedKey own = w.getServer().computeOnServer(s -> Homes.index(level(w), village).beds().get(idA));
            until(c, () -> onServer(w, () -> villager(w, a).isSleeping() && villager(w, a).getSleepingPos().map(p -> p.equals(own.head())).orElse(false)), 900,
                    () -> "the apothecary helps them into their own bed: " + w.getServer().computeOnServer(s -> Knockouts.state(villager(w, a)) + " at " + villager(w, a).blockPosition()));
            w.getServer().runOnServer(s -> {
                var st = Knockouts.state(villager(w, a));
                check(st.tended() && st.bed().isPresent() && st.bed().get().equals(own.head()), "They lie in their own bed, tended: " + st);
                check(Knockouts.knockedOut(villager(w, a)) && Knockouts.injured(villager(w, a)), "Still knocked out while they wait");
            });
            int patientEntity = w.getServer().computeOnServer(s -> villager(w, a).getId());
            c.waitFor(client -> client.level.getEntity(patientEntity) instanceof Villager v && v.getSleepingPos().isPresent() && v.getBedOrientation() != null, 100);
            String clientSide = c.computeOnClient(client -> { var v = (Villager) client.level.getEntity(patientEntity); return v.getSleepingPos() + " " + v.getBedOrientation() + " " + v.getPose() + " yaw " + v.yBodyRot; });
            LOGGER.info("HOMES PATIENT ON THE CLIENT: {}", clientSide);
            c.runOnClient(client -> { if (!client.gui.hud.isHidden()) client.gui.hud.toggle(); });
            view(c, w, x0 + 4.5, y0 + 2.6, z0 + 4.2, 140, 35, "patient-in-bed");
            BlockPos bedside = w.getServer().computeOnServer(s -> Homes.bedside(villager(w, a)).orElse(null));
            check(bedside != null, "There's floor beside the patient's bed");
            until(c, () -> onServer(w, () -> ((TamableAnimal) level(w).getEntity(cat)).position().distanceTo(net.minecraft.world.phys.Vec3.atBottomCenterOf(bedside)) < 1.2), 600,
                    () -> "the cat curls up at the bedside " + bedside + ": " + w.getServer().computeOnServer(s -> level(w).getEntity(cat).position().toString()));
            view(c, w, x0 + 4.5, y0 + 2.6, z0 + 4.8, 130, 40, "pet-bedside");
            c.runOnClient(client -> { if (client.gui.hud.isHidden()) client.gui.hud.toggle(); });
            w.getServer().runOnServer(s -> { Knockouts.revive(villager(w, a), 1); villager(w, healer).kill(level(w)); });
            check(onServer(w, () -> !villager(w, a).isSleeping()), "Revived, they get out of bed");

            // --- A death frees a bed and is remembered for the village to mourn.
            HousingIndex.BedKey bedB = w.getServer().computeOnServer(s -> Homes.index(level(w), village).beds().get(idB));
            w.getServer().runOnServer(s -> villager(w, b).kill(level(w)));
            until(c, () -> onServer(w, () -> Homes.index(level(w), village).vacated().stream().anyMatch(v -> v.resident().equals(idB) && v.why().equals("passed"))), 400,
                    () -> "a death frees the bed and leaves a vacancy");
            w.getServer().runOnServer(s -> {
                var vacancy = Homes.index(level(w), village).vacated().getLast();
                check(vacancy.bed().equals(bedB.head()) && vacancy.house().equals(houseId), "The vacancy remembers whose bed it was: " + vacancy);
                check(!Homes.index(level(w), village).beds().containsKey(idB), "The bed is free");
            });

            // --- Two more newcomers: one takes the free bed, the other has no home and asks on the notice board.
            UUID newcomerC = w.getServer().computeOnServer(s -> spawn(level(w), x0 - 4.5, y0 + 1, z0 + 9.5, "mason").getUUID());
            UUID newcomerD = w.getServer().computeOnServer(s -> spawn(level(w), x0 - 6.5, y0 + 1, z0 + 9.5, "mason").getUUID());
            until(c, () -> onServer(w, () -> { var i = Homes.index(level(w), village); return i.homeless().size() >= 1 && !i.needs().isEmpty()
                    && VillageSocieties.of(villager(w, newcomerD)) != null && VillageSocieties.of(villager(w, newcomerD)).has(profile(villager(w, newcomerD)).id())
                    && (i.beds().containsKey(profile(villager(w, newcomerC)).id()) || i.beds().containsKey(profile(villager(w, newcomerD)).id())); }), 400,
                    () -> "one newcomer moves in and one is homeless: " + w.getServer().computeOnServer(s -> Homes.index(level(w), village).needs().toString()));
            w.getServer().runOnServer(s -> {
                var level = level(w); var record = VillageSettlements.book(level).villages().get(village);
                var board = VillageQuests.board(level, record);
                var house = board.notices().stream().filter(n -> n.kind().equals(Notice.HOUSE)).findFirst().orElse(null);
                check(house != null, "A household with no home asks for a house on the notice board: " + board.notices());
                check(VillageQuests.objective(house).contains("House Plaque"), "The notice asks for a house with a plaque: " + VillageQuests.objective(house));
                var society = VillageSocieties.society(level, village);
                String line = Homes.ledgerLine(level, village, society, idA);
                check(line != null && line.startsWith("Home: ") && line.contains("House"), "The Ledger shows their home: " + line);
                check(!Homes.needLines(level, village, society).isEmpty(), "The Ledger news lists households short of room");
                VillageLedger.openAt(w.getConnection().getServerPlayer(), base);
            });
            c.waitForScreen(LedgerScreen.class); c.waitTicks(10);
            c.takeScreenshot("homes-ledger");
            c.runOnClient(client -> client.gui.setScreen(null));

            // --- Saved and loaded, the beds are the same.
            check(onServer(w, () -> {
                var book = Homes.book(level(w));
                var nbt = HousingBook.CODEC.encodeStart(NbtOps.INSTANCE, book).getOrThrow();
                return HousingBook.CODEC.parse(NbtOps.INSTANCE, nbt).getOrThrow().equals(book);
            }), "The housing book round-trips through NBT");
            before = w.getServer().computeOnServer(s -> Homes.index(level(w), village).beds());
            saved = w.getWorldSave();
        }
        try (var w = saved.open()) {
            w.getConnection().waitForChunksRender();
            String reloaded = village;
            var again = w.getServer().computeOnServer(s -> Homes.index(level(w), reloaded).beds());
            check(again.equals(before), "Beds are the same after a save and reload: " + before + " vs " + again);
            c.waitTicks(200);
            var later = w.getServer().computeOnServer(s -> Homes.index(level(w), reloaded).beds());
            check(later.equals(before), "and stay the same once the residents load again: " + later);
            LOGGER.info("HOMES PLAYER HOUSE PASSED: {} beds kept across a reload", later.size());

            // --- Sneak and use the plaque: the house is private and its residents move out; again, and it's open.
            BlockPos plaqueAgain = w.getServer().computeOnServer(s -> Homes.index(level(w), reloaded).houses().stream().filter(House::player).findFirst().orElseThrow().plaque().orElseThrow());
            String playerHouse = "p:" + plaqueAgain.getX() + "," + plaqueAgain.getY() + "," + plaqueAgain.getZ();
            w.getServer().runOnServer(s -> Homes.togglePrivate(w.getConnection().getServerPlayer(), plaqueAgain));
            until(c, () -> onServer(w, () -> { var i = Homes.index(level(w), reloaded); return i.house(playerHouse).privateHome() && i.residents(playerHouse).isEmpty(); }), 300,
                    () -> "a private house is left to its builder");
            w.getServer().runOnServer(s -> Homes.togglePrivate(w.getConnection().getServerPlayer(), plaqueAgain));
            until(c, () -> onServer(w, () -> { var i = Homes.index(level(w), reloaded); return !i.house(playerHouse).privateHome() && !i.residents(playerHouse).isEmpty(); }), 300,
                    () -> "opened again, the homeless move back in");

            // --- Every village type's houses, read from its structure without reading a block.
            String[] types = {"village", "village_desert", "village_savanna", "village_snowy", "village_taiga"};
            for (int t = 0; t < types.length; t++) {
                String type = types[t]; int vx = 3000 + t * 700, vz = 3000;
                int[] center = w.getServer().computeOnServer(s -> {
                    var level = level(w);
                    var holder = level.registryAccess().lookupOrThrow(Registries.STRUCTURE).getOrThrow(ResourceKey.create(Registries.STRUCTURE, VillageBlocks.id(type)));
                    var generator = level.getChunkSource().getGenerator(); var random = level.getChunkSource().randomState();
                    StructureStart start = holder.value().generate(holder, level.dimension(), level.registryAccess(), generator, generator.getBiomeSource(),
                            random.createClimateSampler(SamplerContext.EMPTY_UNCACHED), random, level.getStructureTemplateManager(), level.getSeed(), ChunkPos.containing(new BlockPos(vx, 0, vz)), 0, level, biome -> true);
                    check(start.isValid(), type + " generates");
                    var box = start.getBoundingBox();
                    for (int cx = box.minX() >> 4; cx <= box.maxX() >> 4; cx++) for (int cz = box.minZ() >> 4; cz <= box.maxZ() >> 4; cz++) level.getChunk(cx, cz);
                    for (int cx = box.minX() >> 4; cx <= box.maxX() >> 4; cx++) for (int cz = box.minZ() >> 4; cz <= box.maxZ() >> 4; cz++) {
                        var chunk = new ChunkPos(cx, cz);
                        start.placeInChunk(level, level.structureManager(), generator, level.getRandom(),
                                new BoundingBox(chunk.getMinBlockX(), level.getMinY(), chunk.getMinBlockZ(), chunk.getMaxBlockX(), level.getMaxY() + 1, chunk.getMaxBlockZ()), chunk);
                    }
                    var houses = HouseSurvey.fromStructure(start);
                    int pieces = 0, homes = 0, catalogBeds = 0, found = 0;
                    var catalog = HouseCatalog.builtin();
                    for (var piece : start.getPieces()) if (piece instanceof PoolElementStructurePiece pool && pool.getElement() instanceof SinglePoolElement single) {
                        var template = catalog.template(single.getTemplateLocation().toString());
                        if (template == null) continue;
                        pieces++; catalogBeds += template.bedFeet().size();
                        if (template.use() == House.Use.HOME) homes++;
                    }
                    check(houses.size() == pieces, type + ": every building with beds is a house: " + houses.size() + " of " + pieces);
                    check(homes >= 3, type + " has family homes: " + homes);
                    for (var h : houses) {
                        var verified = HouseSurvey.verify(level, h, level.getGameTime());
                        for (var bed : h.beds()) {
                            var state = level.getBlockState(bed.foot());
                            check(state.getBlock() instanceof AbstractBedBlock && state.getValue(AbstractBedBlock.PART) == BedPart.FOOT
                                    && state.getValue(HorizontalDirectionalBlock.FACING) == bed.facing(), type + ": " + h.id() + " has its bed foot at " + bed.foot() + " facing " + bed.facing() + ", found " + state);
                            found++;
                        }
                        check(verified.presentBeds().size() >= h.beds().size(), type + ": every catalog bed of " + h.id() + " is there");
                    }
                    check(found == catalogBeds, type + ": " + found + " beds found of " + catalogBeds + " in the catalog");
                    LOGGER.info("HOMES {}: {} houses ({} homes), {} beds, all where the catalog says", type, houses.size(), homes, found);
                    var mid = box.getCenter();
                    return new int[]{mid.getX(), box.maxY(), mid.getZ()};
                });
                c.runOnClient(client -> { if (!client.gui.hud.isHidden()) client.gui.hud.toggle(); });
                view(c, w, center[0], center[1] + 45, center[2] - 55, 0, 45, type.replace("village_", "").replace("village", "plains") + "-village");
                c.runOnClient(client -> { if (client.gui.hud.isHidden()) client.gui.hud.toggle(); });
            }
            LOGGER.info("HOMES STRUCTURES PASSED: all five village types' houses read from their structures");
        }

        // --- Bedtime in a naturally generated village: everyone in their own bed, partners side by side.
        try (var w = c.worldBuilder().adjustSettings(ui -> {
            var normal = ui.getSettings().worldgenLoadContext().lookupOrThrow(Registries.WORLD_PRESET).getOrThrow(WorldPresets.NORMAL);
            ui.setWorldType(new WorldCreationUiState.WorldTypeEntry(normal));
            ui.setGenerateStructures(true);
            ui.setSeed("1");
        }).create()) {
            w.getConnection().waitForChunksDownload();
            for (var command : List.of("gamemode spectator @a", "gamerule advance_time false", "gamerule advance_weather false", "gamerule spawn_mobs false",
                    "weather clear", "difficulty peaceful", "time set " + (2 * 24000 + Routine.at(9, 0)), "effect give @a minecraft:night_vision 100000 0 true"))
                w.getServer().runCommand(command);
            int[] center = w.getServer().computeOnServer(s -> {
                var level = level(w);
                var holder = level.registryAccess().lookupOrThrow(Registries.STRUCTURE).getOrThrow(ResourceKey.create(Registries.STRUCTURE, VillageBlocks.id("village")));
                var located = level.getChunkSource().getGenerator().findNearestMapStructure(level, HolderSet.direct(holder), BlockPos.ZERO, 80, false);
                check(located != null, "A normal world has a village");
                var entrance = located.getFirst(); level.getChunkAt(entrance);
                StructureStart start = StructureStart.INVALID_START;
                for (int y = 32; y < 256 && !start.isValid(); y += 4) start = level.structureManager().getStructureAt(new BlockPos(entrance.getX(), y, entrance.getZ()), holder.value());
                check(start.isValid(), "The village has a structure start");
                var mid = start.getBoundingBox().getCenter();
                return new int[]{mid.getX(), start.getBoundingBox().maxY(), mid.getZ()};
            });
            cmd(w, "tp @a %d %d %d", center[0], center[1] + 20, center[2]);
            String[] natural = new String[1];
            until(c, () -> onServer(w, () -> {
                var record = VillageSettlements.book(level(w)).at(new BlockPos(center[0], center[1], center[2]));
                if (record == null) return false;
                natural[0] = record.id();
                var index = Homes.index(level(w), record.id());
                return index.surveyed() && index.houses().stream().filter(House::verified).count() >= 8 && !index.beds().isEmpty();
            }), 2400, () -> "the natural village's houses are read from its structure and beds handed out");
            c.waitTicks(400);
            String naturalVillage = natural[0];
            w.getServer().runOnServer(s -> {
                var level = level(w); var index = Homes.index(level, naturalVillage); var society = VillageSocieties.society(level, naturalVillage);
                check(index.houses().stream().allMatch(h -> h.kind() == House.Kind.GENERATED), "Every house came from the village structure");
                int residents = 0;
                for (var t : society.living()) if (t.home()) {
                    residents++;
                    check(index.beds().containsKey(t.id()) || index.needOf(t.id()) != null, t.name() + " has a bed or a recorded need");
                }
                LOGGER.info("HOMES NATURAL VILLAGE: {} houses ({} checked), {} residents, {} beds given, needs {}", index.houses().size(),
                        index.houses().stream().filter(House::verified).count(), residents, index.beds().size(), index.needs().values());
            });
            // Bedtime.
            cmd(w, "time set %d", 2 * 24000 + Routine.at(22, 30));
            int[] best = new int[1];
            until(c, () -> {
                int sleeping = w.getServer().computeOnServer(s -> (int) CompanionController.loaded.stream().filter(v -> v.isAlive() && v.isSleeping()).count());
                best[0] = Math.max(best[0], sleeping);
                return sleeping >= 6;
            }, 2400, () -> "residents go to bed: " + best[0] + " asleep");
            c.waitTicks(200);
            double[] shot = w.getServer().computeOnServer(s -> {
                var level = level(w); var index = Homes.index(level, naturalVillage); var society = VillageSocieties.society(level, naturalVillage);
                int own = 0, sleepers = 0; Villager sample = null;
                for (var v : List.copyOf(CompanionController.loaded)) {
                    if (!v.isAlive() || !v.isSleeping() || v.level() != level) continue;
                    String rid = profile(v).id(); var mine = index.beds().get(rid); var at = v.getSleepingPos().orElseThrow();
                    sleepers++;
                    if (mine != null) {
                        check(at.equals(mine.head()), name(v) + " sleeps in their own bed: " + at + " vs " + mine.head());
                        own++;
                        if (sample == null) sample = v;
                    } else check(index.owner(at) == null, name(v) + " has no bed of their own and sleeps in nobody else's");
                }
                for (var t : society.living()) {
                    if (t.partner().isEmpty() || t.id().compareTo(t.partner()) > 0) continue;
                    var mine = index.bedOf(t.id()); var theirs = index.bedOf(t.partner());
                    if (mine.isEmpty() || theirs.isEmpty()) continue;
                    check(index.houseOf(t.id()).id().equals(index.houseOf(t.partner()).id()) && mine.get().room() == theirs.get().room(), t.name() + " and their partner share a room");
                }
                check(own >= 3, "Sleepers are in their own beds: " + own + " of " + sleepers);
                LOGGER.info("HOMES BEDTIME: {} asleep, {} in their own assigned bed", sleepers, own);
                var bed = index.bedOf(profile(sample).id()).orElseThrow();
                var eye = bed.head().relative(bed.facing().getOpposite(), 3).relative(bed.facing().getClockWise());
                return new double[]{eye.getX() + .5, eye.getY() + 1.6, eye.getZ() + .5, bed.head().getX() + .5, bed.head().getZ() + .5};
            });
            float yaw = (float) Math.toDegrees(Math.atan2(-(shot[3] - shot[0]), shot[4] - shot[2]));
            c.runOnClient(client -> { if (!client.gui.hud.isHidden()) client.gui.hud.toggle(); });
            view(c, w, shot[0], shot[1], shot[2], yaw, 30, "bedtime-plains");
            c.runOnClient(client -> { if (client.gui.hud.isHidden()) client.gui.hud.toggle(); });
            LOGGER.info("HOMES PASSED: player houses, plaques, beds, newborns, patients, pets, vacancies, notices, reloads, five village types and bedtime");
        }
    }
}
