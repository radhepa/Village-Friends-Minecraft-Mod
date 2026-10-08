package dev.villagefriends;

import static dev.villagefriends.VillageFriends.*;

import dev.villagefriends.routine.Routine;
import dev.villagefriends.tavern.Patronage;
import dev.villagefriends.tavern.Seat;
import dev.villagefriends.tavern.TavernBlocks;
import dev.villagefriends.tavern.Taverns;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import net.fabricmc.fabric.api.attachment.v1.AttachmentTarget;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.minecraft.client.gui.screens.worldselection.WorldCreationUiState;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.GlobalPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.ai.memory.MemoryModuleType;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.Mirror;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.levelgen.presets.WorldPresets;
import net.minecraft.world.level.levelgen.structure.templatesystem.JigsawReplacementProcessor;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructurePlaceSettings;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.Vec3;

/**
 * The tavern: The Hearth placed on a flat world with its keeper, its cook and a dozen and a half residents.
 * On a Market Day evening they find seats, are served by the keeper and eat and drink; at bedtime they get up
 * and give their seats back; at lunch the next day they eat the cook's dish. A player sits on a chair too.
 * Screenshots are named {@code tavern-*}.
 */
@SuppressWarnings("UnstableApiUsage")
public final class TavernGameTest implements FabricClientGameTest {
    private static final int GROUND = -61, PATRONS = 18;
    private static void check(boolean ok, String why) { if (!ok) throw new AssertionError(why); }
    private static ServerLevel level(TestSingleplayerContext w) { return w.getConnection().getServerLevel(); }
    private static Villager villager(TestSingleplayerContext w, UUID id) { return (Villager) level(w).getEntity(id); }
    private static String state(Villager v) { return ((AttachmentTarget) v).getAttached(Taverns.STATE); }

    /** {seated, eating, drinking, waiting, served so far} among the patrons. */
    private static int[] census(TestSingleplayerContext w, List<UUID> patrons) {
        return w.getServer().computeOnServer(s -> {
            int seated = 0, eating = 0, drinking = 0, waiting = 0;
            for (var id : patrons) {
                var v = villager(w, id); if (v == null) continue;
                if (Seat.seated(v)) seated++;
                String st = state(v);
                if (st == null) continue;
                if (st.startsWith("eat")) eating++; else if (st.startsWith("drink")) drinking++; else if (st.startsWith("wait")) waiting++;
            }
            return new int[]{seated, eating, drinking, waiting};
        });
    }
    private static void view(ClientGameTestContext c, TestSingleplayerContext w, double x, double y, double z, float yaw, float pitch, String name) {
        w.getServer().runCommand(String.format(java.util.Locale.ROOT, "tp @a %.2f %.2f %.2f %.1f %.1f", x, y, z, yaw, pitch));
        c.waitTicks(40);
        c.runOnClient(client -> client.gui.toastManager().clear());
        c.takeScreenshot("tavern-" + name);
    }

    @Override public void runTest(ClientGameTestContext c) {
        c.getInput().resizeWindow(1280, 800);
        try (var w = c.worldBuilder().adjustSettings(ui -> {
            var flat = ui.getSettings().worldgenLoadContext().lookupOrThrow(Registries.WORLD_PRESET).getOrThrow(WorldPresets.FLAT);
            ui.setWorldType(new WorldCreationUiState.WorldTypeEntry(flat));
            ui.setGenerateStructures(false);
            ui.setSeed("11");
        }).create()) {
            for (int attempt = 0; attempt < 3; attempt++) { try { w.getConnection().waitForChunksRender(); break; } catch (AssertionError slow) { c.waitTicks(100); } }
            for (var cmd : List.of("gamerule advance_time false", "gamerule advance_weather false", "gamerule spawn_mobs false", "weather clear", "gamemode creative @a", "difficulty peaceful"))
                w.getServer().runCommand(cmd);

            // --- The Hearth, its stations, its keeper and cook.
            int[] size = w.getServer().computeOnServer(s -> {
                var level = level(w);
                var template = level.getStructureTemplateManager().get(VillageBlocks.id("village/tavern")).orElseThrow();
                for (int cx = -3; cx <= 4; cx++) for (int cz = -3; cz <= 4; cz++) level.getChunk(cx, cz);
                var pos = new BlockPos(0, GROUND, 0);
                template.placeInWorld(level, pos, pos, new StructurePlaceSettings().setRotation(Rotation.NONE).setMirror(Mirror.NONE)
                        .setIgnoreEntities(true).setKnownShape(true).addProcessor(JigsawReplacementProcessor.INSTANCE), level.getRandom(), 18);
                return new int[]{template.getSize().getX(), template.getSize().getY(), template.getSize().getZ()};
            });
            var stations = new ArrayList<BlockPos>(); var stove = new BlockPos[1];
            w.getServer().runOnServer(s -> {
                var level = level(w);
                for (var p : BlockPos.betweenClosed(0, GROUND, 0, size[0], GROUND + size[1], size[2])) {
                    var state = level.getBlockState(p);
                    if (state.is(VillageBlocks.get("tap_stand")) || state.is(VillageBlocks.get("drinks_barrel"))) stations.add(p.immutable());
                    if (state.is(VillageBlocks.get("kitchen_stove"))) stove[0] = p.immutable();
                }
            });
            check(stations.size() >= 2 && stove[0] != null, "The Hearth has a tap stand, a drinks barrel and a kitchen stove");
            UUID keeper = w.getServer().computeOnServer(s -> staff(level(w), "tavern_keeper", stations.getFirst()));
            // Nobody else takes the other station's job while the test runs.
            w.getServer().runOnServer(s -> { for (var st : stations.subList(1, stations.size()))
                level(w).getPoiManager().take(h -> h.is(VillageProfessions.poiKey("tavern_keeper")), (h, p) -> p.equals(st), st, 1); });
            UUID cook = w.getServer().computeOnServer(s -> staff(level(w), "cook", stove[0]));

            // --- Market Day evening: most of the village comes out.
            w.getServer().runCommand("time set " + (6 * 24000 + Routine.at(18, 50)));
            var patrons = new ArrayList<UUID>();
            w.getServer().runOnServer(s -> {
                var level = level(w);
                check(Routine.marketDay(day(level)), "It's Market Day");
                for (int i = 0; i < PATRONS; i++) {
                    var v = new Villager(EntityTypes.VILLAGER, level);
                    v.setPos(2.5 + i % 9 * 1.5, GROUND + 1, -3.5 - i / 9 * 1.5);
                    level.addFreshEntity(v); patrons.add(v.getUUID());
                }
            });
            c.waitTicks(40);
            int expected = w.getServer().computeOnServer(s -> {
                int n = 0;
                for (var id : patrons) if (Routine.atTavern(ResidentRoutines.plan(villager(w, id)).block())) n++;
                return n;
            });
            check(expected >= 5, "Plenty of residents spend Market Day evening at the tavern: " + expected);
            boolean carried = false; int[] now = {0, 0, 0, 0};
            for (int i = 0; i < 90; i++) {
                c.waitTicks(20);
                if (!carried) carried = w.getServer().computeOnServer(s -> { var k = villager(w, keeper); return k != null && state(k) != null && state(k).startsWith("carry"); });
                now = census(w, patrons);
                if (now[0] >= Math.min(expected, 6) && now[1] + now[2] >= 3 && carried) break;
            }
            LOGGER.info("TAVERN EVENING: {} of {} came; seated {}, eating {}, drinking {}, waiting {}; keeper carried an order: {}", expected, PATRONS, now[0], now[1], now[2], now[3], carried);
            String described = w.getServer().computeOnServer(s -> Taverns.describe(level(w)));
            LOGGER.info("TAVERN STATE: {}", described);
            check(now[0] >= Math.min(expected, 4), "Residents sit down at the tavern: " + now[0] + " of " + expected);
            check(now[1] + now[2] >= 2, "They are served and eat or drink: " + (now[1] + now[2]));
            check(carried, "The tavern keeper carries orders out to the tables");
            w.getServer().runOnServer(s -> {
                var tavern = Taverns.tavernAt(level(w), stations.getFirst());
                check(tavern != null && tavern.seats().size() >= 6, "The survey finds the tavern's seats: " + (tavern == null ? 0 : tavern.seats().size()));
                LOGGER.info("TAVERN SURVEY: {} seats ({} by the hearth, {} outdoors), {} standing places, stage {}", tavern.seats().size(),
                        tavern.seats().stream().filter(x -> x.hearth()).count(), tavern.seats().stream().filter(x -> x.outdoor()).count(), tavern.standing().size(), tavern.stage());
                for (var id : patrons) {
                    var v = villager(w, id);
                    if (!Seat.seated(v)) continue;
                    var seat = (Seat) v.getVehicle();
                    check(Math.abs(net.minecraft.util.Mth.wrapDegrees(v.yBodyRot - seat.getYRot())) < 1, "Diners sit square to their table");
                    check(v.getY() < seat.seatPos().getY() + .1, "Diners sit down onto the seat: " + v.getY() + " at seat " + seat.seatPos().getY());
                }
            });
            // The client draws them seated, with their dish on the table or in hand.
            c.waitTicks(10);
            var seatedIds = w.getServer().computeOnServer(s -> {
                var ids = new ArrayList<Integer>();
                for (var id : patrons) { var v = villager(w, id); if (Seat.seated(v)) ids.add(v.getId()); }
                return ids;
            });
            c.runOnClient(client -> {
                int seated = 0, dishes = 0;
                for (int id : seatedIds) {
                    if (!(client.level.getEntity(id) instanceof Villager v)) continue;
                    var renderer = (dev.villagefriends.client.ResidentRenderer) client.getEntityRenderDispatcher().getRenderer(v);
                    var rs = renderer.createRenderState(v, 1);
                    if (rs.seated && rs.isPassenger) seated++;
                    if (rs.tableItemShown || !rs.rightHandItemState.isEmpty() || !rs.leftHandItemState.isEmpty()) dishes++;
                }
                check(seated > 0, "The client draws diners sitting");
                LOGGER.info("TAVERN CLIENT: {} drawn seated, {} with a dish on the table or in hand", seated, dishes);
            });
            w.getServer().runCommand("gamemode spectator @a");
            c.runOnClient(client -> { if (!client.gui.hud.isHidden()) client.gui.hud.toggle(); });
            double cx = size[0] / 2.0, cz = size[2] / 2.0;
            view(c, w, cx, GROUND + size[1] * .55, -7, 0, 28, "front");
            view(c, w, 2.6, GROUND + 3.4, 6.2, -50, 22, "hall");
            view(c, w, size[0] - 2.4, GROUND + 3.4, cz + 3, 135, 24, "hall-back");
            view(c, w, cx, GROUND + 5.5, cz, 0, 70, "overhead");
            // Close-ups of two diners from beside their table, served ones first.
            for (int i = 0; i < 30 && w.getServer().computeOnServer(s -> patrons.stream().noneMatch(id -> Seat.seated(villager(w, id)) && state(villager(w, id)) != null
                    && (state(villager(w, id)).startsWith("eat") || state(villager(w, id)).startsWith("drink")))); i++) c.waitTicks(20);
            var diners = w.getServer().computeOnServer(s -> {
                var out = new ArrayList<double[]>();
                for (var id : patrons) {
                    var v = villager(w, id);
                    if (!Seat.seated(v) || v.level().canSeeSky(v.blockPosition().above(2))) continue;
                    var seat = (Seat) v.getVehicle();
                    String st = state(v);
                    boolean served = st != null && (st.startsWith("eat") || st.startsWith("drink"));
                    if (served) out.addFirst(new double[]{v.getX(), v.getY(), v.getZ(), seat.getYRot()});
                    else out.add(new double[]{v.getX(), v.getY(), v.getZ(), seat.getYRot()});
                }
                return out;
            });
            for (int i = 0; i < Math.min(2, diners.size()); i++) {
                var d = diners.get(i);
                // Off to the diner's front-right, looking back at them and their place at the table.
                double yaw = Math.toRadians(d[3]), fx = -Math.sin(yaw), fz = Math.cos(yaw), rx = -fz, rz = fx;
                double ex = d[0] + fx * 1.7 + rx * 1.3, ez = d[2] + fz * 1.7 + rz * 1.3;
                float look = (float) Math.toDegrees(Math.atan2(-(d[0] - ex), d[2] - ez));
                view(c, w, ex, d[1] + 1.25, ez, look, 22, "diner" + i);
            }
            c.runOnClient(client -> { if (client.gui.hud.isHidden()) client.gui.hud.toggle(); });

            // --- A player sits on a Tavern Chair of their own with an empty hand, and gets up again.
            w.getServer().runCommand("gamemode creative @a");
            var chair = new BlockPos(-4, GROUND + 1, -9);
            w.getServer().runOnServer(s -> level(w).setBlock(chair, TavernBlocks.CHAIR.defaultBlockState()
                    .setValue(net.minecraft.world.level.block.HorizontalDirectionalBlock.FACING, Direction.SOUTH), 3));
            w.getServer().runOnServer(s -> {
                var level = level(w); var p = w.getConnection().getServerPlayer();
                p.teleportTo(level, chair.getX() + .5, chair.getY(), chair.getZ() - .8, java.util.Set.of(), 0, 0, true);
                p.setItemInHand(InteractionHand.MAIN_HAND, ItemStack.EMPTY);
                p.gameMode.useItemOn(p, level, ItemStack.EMPTY, InteractionHand.MAIN_HAND, new BlockHitResult(Vec3.atCenterOf(chair), Direction.UP, chair, false));
                check(Seat.seated(p), "A player sits down on a chair with an empty hand");
                check(p.getY() < chair.getY() + .1, "and sits down onto it: " + p.getY());
                check(Math.abs(net.minecraft.util.Mth.wrapDegrees(p.getVehicle().getYRot() - Direction.SOUTH.toYRot())) < 1, "facing the way the chair faces");
            });
            c.waitTicks(10);
            w.getServer().runCommand("gamemode spectator @a");
            w.getServer().runOnServer(s -> w.getConnection().getServerPlayer().stopRiding());
            c.waitTicks(5);
            w.getServer().runOnServer(s -> check(!Seat.seated(w.getConnection().getServerPlayer()), "and gets up again"));

            // --- Bedtime: everyone gets up and the seats are free again.
            w.getServer().runCommand("time set " + (6 * 24000 + Routine.at(23, 30)));
            c.waitTicks(80);
            int[] late = census(w, patrons);
            w.getServer().runOnServer(s -> {
                int seats = level(w).getEntitiesOfClass(Seat.class, new net.minecraft.world.phys.AABB(-4, GROUND - 2, -8, size[0] + 4, GROUND + size[1], size[2] + 4)).size();
                check(seats == 0, "No seats are left behind: " + seats);
                check(state(villager(w, keeper)) == null, "The keeper puts the tray down");
            });
            check(late[0] == 0 && late[3] == 0, "At bedtime nobody stays seated or waiting: " + late[0] + "/" + late[3]);

            // --- Lunch the next day: the cook's dish of the day, or a ploughman's when the stove is cold.
            w.getServer().runCommand("time set " + (7 * 24000 + Routine.at(11, 20)));
            int lunchers = w.getServer().computeOnServer(s -> {
                int n = 0;
                for (var id : patrons) if (ResidentRoutines.plan(villager(w, id)).block() == Routine.Block.LUNCH_TAVERN) n++;
                return n;
            });
            int eatingLunch = 0;
            for (int i = 0; i < 60 && lunchers > 0; i++) {
                c.waitTicks(20);
                eatingLunch = census(w, patrons)[1];
                if (eatingLunch >= Math.min(2, lunchers)) break;
            }
            LOGGER.info("TAVERN LUNCH: {} lunching at the tavern, {} eating", lunchers, eatingLunch);
            if (lunchers > 0) {
                check(eatingLunch >= 1, "Tavern lunchers get their lunch");
                w.getServer().runOnServer(s -> {
                    for (var id : patrons) {
                        String st = state(villager(w, id));
                        if (st == null || !st.startsWith("eat")) continue;
                        String dish = Patronage.item(st);
                        check(Patronage.DISHES.contains(dish) || dish.equals("villagefriends:ploughmans_lunch"), "Lunch is a proper dish: " + dish);
                    }
                });
                w.getServer().runCommand("gamemode spectator @a");
                c.runOnClient(client -> { if (!client.gui.hud.isHidden()) client.gui.hud.toggle(); });
                view(c, w, 2.6, GROUND + 3.4, 6.2, -50, 22, "lunch");
                c.runOnClient(client -> { if (client.gui.hud.isHidden()) client.gui.hud.toggle(); });
            }
            check(w.getServer().computeOnServer(s -> villager(w, cook) != null), "The cook is still about");
            LOGGER.info("TAVERN PASSED: residents sit with their friends, are served by the keeper, eat and drink, get up at bedtime and lunch on the dish of the day; players sit too.");
        }
    }

    /** A keeper or cook standing at their station, with it as their job site. */
    private static UUID staff(ServerLevel level, String job, BlockPos station) {
        var v = new Villager(EntityTypes.VILLAGER, level);
        BlockPos spot = station;
        for (var d : Direction.Plane.HORIZONTAL) {
            var cell = station.relative(d);
            if (level.getBlockState(cell).getCollisionShape(level, cell).isEmpty() && level.getBlockState(cell.above()).getCollisionShape(level, cell.above()).isEmpty()) { spot = cell; break; }
        }
        v.setPos(spot.getX() + .5, spot.getY(), spot.getZ() + .5);
        v.setVillagerData(v.getVillagerData().withProfession(level.registryAccess(), VillageProfessions.key(job)));
        v.setVillagerXp(1);
        level.addFreshEntity(v);
        level.getPoiManager().take(h -> h.is(VillageProfessions.poiKey(job)), (h, p) -> p.equals(station), station, 1);
        v.getBrain().setMemory(MemoryModuleType.JOB_SITE, GlobalPos.of(level.dimension(), station));
        return v.getUUID();
    }
}
