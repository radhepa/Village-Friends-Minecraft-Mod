package dev.villagefriends;

import dev.villagefriends.homestead.Dwelling;
import dev.villagefriends.homestead.Homesteads;
import dev.villagefriends.outfit.Gender;
import dev.villagefriends.outfit.ResidentLook;
import dev.villagefriends.talk.Talk;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.minecraft.client.gui.screens.worldselection.WorldCreationUiState;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.entity.ai.memory.MemoryModuleType;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.level.levelgen.presets.WorldPresets;
import net.minecraft.world.phys.AABB;
import static dev.villagefriends.VillageFriends.*;

/**
 * Every homestead, placed for real with {@code /place structure}: its residents settle in with the right role,
 * nameplate and personality (the farmstead couple as husband and wife with one surname), never join a village,
 * talk only from their own dialogue on every topic, turn back for home when they wander, and the veteran walks
 * the watch at night. Screenshots: {@code homestead-<name>-1/2}. Run with {@code -Ptests=HomesteadGameTest}.
 */
@SuppressWarnings("UnstableApiUsage")
public final class HomesteadGameTest implements FabricClientGameTest {
    private static final int GROUND = -61, SPACING = 90;
    private static final Map<String, List<String>> HOMESTEADS = Map.of(
            "farmstead", List.of("homesteader", "homesteader"), "pariah_house", List.of("pariah"), "shepherd_fold", List.of("shepherd"),
            "herbalist_cottage", List.of("herbalist"), "watchtower", List.of("veteran"));
    private static final List<String> ORDER = List.of("farmstead", "pariah_house", "shepherd_fold", "herbalist_cottage", "watchtower");
    private static final List<String> TOPICS = List.of("greet", "chat", "work", "adventure", "joke", "news", "heart");

    private static void check(boolean ok, String why) { if (!ok) throw new AssertionError(why); }
    private static List<Villager> residents(TestSingleplayerContext w, int x) {
        return w.getConnection().getServerLevel().getEntitiesOfClass(Villager.class, new AABB(x - 40, GROUND - 4, -40, x + 40, GROUND + 30, 40));
    }
    private static void view(ClientGameTestContext c, TestSingleplayerContext w, double x, double y, double z, float yaw, float pitch, String name) {
        w.getServer().runCommand(String.format(java.util.Locale.ROOT, "tp @a %.1f %.1f %.1f %.1f %.1f", x, y, z, yaw, pitch));
        c.waitTicks(Integer.getInteger("villagefriends.galleryWait", 140));
        c.runOnClient(client -> client.gui.toastManager().clear());
        c.takeScreenshot("homestead-" + name);
    }

    @Override public void runTest(ClientGameTestContext c) {
        c.getInput().resizeWindow(1280, 800);
        c.runOnClient(client -> { client.options.guiScale().set(2); if (!client.gui.hud.isHidden()) client.gui.hud.toggle(); client.resizeGui(); });
        try (var w = c.worldBuilder().adjustSettings(ui -> {
            var flat = ui.getSettings().worldgenLoadContext().lookupOrThrow(Registries.WORLD_PRESET).getOrThrow(WorldPresets.FLAT);
            ui.setWorldType(new WorldCreationUiState.WorldTypeEntry(flat));
            ui.setGenerateStructures(false);
            ui.setSeed("11");
        }).create()) {
            for (int attempt = 0; attempt < 3; attempt++) { try { w.getConnection().waitForChunksRender(); break; } catch (AssertionError slow) { c.waitTicks(100); } }
            c.runOnClient(client -> { client.options.renderDistance().set(8); client.options.broadcastOptions(); });
            w.getServer().runCommand("gamemode creative @a");
            w.getServer().runCommand("weather clear");
            w.getServer().runCommand("gamerule advance_time false");
            w.getServer().runCommand("gamerule spawn_mobs false");
            w.getServer().runCommand("time set 3000");
            w.getServer().runOnServer(server -> server.getPlayerList().setViewDistance(8));

            for (int i = 0; i < ORDER.size(); i++) {
                int x = 300 + i * SPACING; String name = ORDER.get(i);
                w.getServer().runOnServer(server -> {
                    var level = server.overworld();
                    for (int cx = (x - 48) >> 4; cx <= (x + 48) >> 4; cx++) for (int cz = -3; cz <= 3; cz++) level.getChunk(cx, cz);
                });
                w.getServer().runCommand("place structure villagefriends:homestead_" + name + " " + x + " " + (GROUND + 1) + " 0");
            }
            c.waitTicks(40);
            var report = new ArrayList<String>();
            var middles = new java.util.concurrent.ConcurrentHashMap<String, int[]>();
            for (int i = 0; i < ORDER.size(); i++) {
                int x = 300 + i * SPACING; String name = ORDER.get(i);
                // Their residents load (and settle in) once someone comes near, as in a real world.
                w.getServer().runCommand("tp @a " + x + " " + (GROUND + 2) + " -30");
                c.waitTicks(60);
                w.getServer().runOnServer(server -> {
                    var level = w.getConnection().getServerLevel(); var p = w.getConnection().getServerPlayer();
                    var found = residents(w, x);
                    var roles = new ArrayList<String>();
                    for (var v : found) {
                        var d = Homesteads.dweller(v);
                        check(d != null, name + ": " + v.getName().getString() + " settled in as a homestead resident");
                        roles.add(d.role());
                        check(target(v).getAttached(HOME) == null && VillageSocieties.of(v) == null, name + ": homestead folk belong to no village");
                        String label = v.getCustomName().getString();
                        check(label.equals(Dwelling.label(d.kind(), d.name(), d.place())), name + ": nameplate " + label);
                        check(profile(v).personality().equals(d.kind().personality(ResidentLook.parse(profile(v).look()).gender())), name + ": personality fits the life");
                        for (var topic : TOPICS) {
                            var context = TalkWorld.context(v, p, topic);
                            check(context.fill().get("dweller").equals(d.role()) && context.fill().get("place").equals(d.place()), name + ": talk knows where they live");
                            var pools = Talk.pools(context);
                            check(!pools.isEmpty() && pools.keySet().stream().allMatch(k -> k.startsWith(d.role() + ".")), name + ": " + topic + " comes from their own lines: " + pools.keySet());
                            String line = TalkWorld.line(v, p, topic);
                            check(line != null && !line.contains("{"), name + ": something to say about " + topic + ": " + line);
                            if (topic.equals("chat")) report.add(label + " (" + ResidentRoutines.doing(v) + "): " + line);
                        }
                        String opening = NarrativeEngine.greeting(v, p);
                        check(opening != null && !opening.contains("{"), name + ": a greeting");
                        String about = NarrativeEngine.conversation(v, p, "chat");
                        check(about != null && !about.isBlank(), name + ": a conversation");
                    }
                    java.util.Collections.sort(roles);
                    check(roles.equals(HOMESTEADS.get(name)), name + ": residents " + roles + " (expected " + HOMESTEADS.get(name) + ")");
                    if (name.equals("farmstead")) {
                        var a = found.get(0); var b = found.get(1);
                        var genders = List.of(ResidentLook.parse(profile(a).look()).gender(), ResidentLook.parse(profile(b).look()).gender());
                        check(genders.contains(Gender.MALE) && genders.contains(Gender.FEMALE), "The farmstead is a husband and wife: " + genders);
                        String surnameA = Homesteads.dweller(a).name().split(" ")[1], surnameB = Homesteads.dweller(b).name().split(" ")[1];
                        check(surnameA.equals(surnameB), "The couple share a surname: " + surnameA + " / " + surnameB);
                        check(Homesteads.dweller(a).place().equals(Homesteads.dweller(b).place()), "They live at the same farm");
                        var fill = TalkWorld.context(a, p, "chat").fill();
                        check(first(Homesteads.dweller(b).name()).equals(fill.get("partner")), "Each knows their spouse: " + fill.get("partner"));
                        check(fill.get("spouse").equals(ResidentLook.parse(profile(b).look()).gender() == Gender.FEMALE ? "wife" : "husband"), "Husband or wife: " + fill.get("spouse"));
                    }
                    if (name.equals("pariah_house")) check(found.getFirst().getCustomName().getString().endsWith(", the Outcast"), "The pariah belongs nowhere");
                    if (name.equals("watchtower")) check(profession(found.getFirst()).equals("archer"), "The veteran keeps an archer's trade");
                    // Wandering off while awake, they turn back for home (asleep, vanilla takes them to bed).
                    var v = found.getFirst(); var d = Homesteads.dweller(v);
                    middles.put(name, new int[]{d.x(), d.z()});
                    if (!ResidentRoutines.plan(v).block().sleep) {
                        v.teleportTo(d.x() + 40.5, v.getY(), d.z() + .5);
                        v.getBrain().eraseMemory(MemoryModuleType.WALK_TARGET);
                        ResidentRoutines.update(v);
                        var walk = v.getBrain().getMemory(MemoryModuleType.WALK_TARGET);
                        check(walk.isPresent() && walk.get().getTarget().currentBlockPosition().distSqr(new net.minecraft.core.BlockPos(d.x(), d.y(), d.z())) < 30 * 30,
                                name + ": a resident who strays heads home");
                        v.teleportTo(d.x() + .5, v.getY(), d.z() + 2.5);
                    }
                });
            }
            // At night the veteran keeps the watch, walking the corners of the tower.
            w.getServer().runCommand("time set 15500");
            int tower = 300 + ORDER.indexOf("watchtower") * SPACING;
            w.getServer().runCommand("tp @a " + tower + " " + (GROUND + 2) + " -30");
            c.waitTicks(20);
            w.getServer().runOnServer(server -> {
                var v = residents(w, tower).getFirst();
                check(ResidentRoutines.plan(v).block() == dev.villagefriends.routine.Routine.Block.NIGHT_WATCH, "The veteran keeps the watch at 21:30");
                check(ResidentRoutines.doing(v).startsWith("Keeping the watch"), "The window says so: " + ResidentRoutines.doing(v));
                v.getBrain().eraseMemory(MemoryModuleType.WALK_TARGET);
                ResidentRoutines.update(v);
                check(v.getBrain().getMemory(MemoryModuleType.WALK_TARGET).isPresent(), "The veteran sets off round the tower");
            });
            w.getServer().runCommand("time set 3000");
            for (var line : report) VillageFriends.LOGGER.info("HOMESTEAD: {}", line);

            w.getServer().runCommand("gamemode spectator @a");
            for (var name : ORDER) {
                int[] m = middles.get(name);
                int d = name.equals("watchtower") ? 25 : 21, h = name.equals("watchtower") ? 17 : 13;
                view(c, w, m[0] - d, GROUND + h, m[1] - d, -45f, 27f, name + "-1");
                view(c, w, m[0] + d, GROUND + h, m[1] + d, 135f, 27f, name + "-2");
            }
        }
        VillageFriends.LOGGER.info("HOMESTEADS CHECKED: {}", ORDER);
    }
    private static String first(String name) { int s = name.indexOf(' '); return s > 0 ? name.substring(0, s) : name; }
}
