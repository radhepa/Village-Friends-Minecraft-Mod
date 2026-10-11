package dev.villagefriends.rpg;

import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.server.MinecraftServer;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * The development audit's modpack half (-Dvillagefriends_rpg.audit=true): with the other mods of the pack
 * loaded, checks that every monster, place, item and profession the add-on names really exists in the game,
 * so a renamed mob or structure in another mod shows up here instead of as a job nobody can finish.
 */
final class ModpackAudit {
    private ModpackAudit() {}
    /** Which mod registers each of the other mods' professions the job board knows. */
    private static final Map<String, String> JOB_MODS = Map.of("miner", "caveexpansion", "lightkeeper", "oceanexpansion", "smuggler", "oceanexpansion",
            "pearl_diver", "seafriends", "kelp_farmer", "seafriends", "shellwright", "seafriends", "tide_singer", "seafriends",
            "lightwright", "seafriends", "spongekeeper", "seafriends");

    /** Logs what was checked and every name that didn't resolve; returns the problems. */
    static List<String> run(MinecraftServer server) {
        var problems = new ArrayList<String>(); int checked = 0;
        for (var e : Bestiary.modpackMobs().entrySet()) {
            if (!Modpack.installed(Modpack.modOf(e.getKey()))) continue;
            checked++;
            if (!BuiltInRegistries.ENTITY_TYPE.containsKey(Identifier.parse(e.getKey()))) problems.add("monster " + e.getKey() + " (" + e.getValue() + ")");
        }
        var structures = server.registryAccess().lookupOrThrow(Registries.STRUCTURE);
        for (var pl : Atlas.shown()) for (var st : pl.structures()) {
            checked++;
            if (!structures.containsKey(Identifier.parse(st))) problems.add("place " + st + " (" + pl.name() + ")");
        }
        for (var pool : QuestBook.poolNames()) for (var t : QuestBook.pool(pool)) {
            if (!Modpack.installed(t.mod())) continue;
            checked++;
            switch (t.kind()) {
                case "gather" -> {
                    var id = Identifier.parse(t.target().indexOf(':') < 0 ? "minecraft:" + t.target() : t.target());
                    if (!BuiltInRegistries.ITEM.containsKey(id)) problems.add("job item " + id + " (" + pool + ")");
                }
                case "slay" -> { if (Bestiary.byId(t.target()) == null) problems.add("job family " + t.target() + " (" + pool + ")"); }
                case "explore" -> { if (!t.target().equals("*") && (!t.target().startsWith("place:") || Atlas.byId(t.target().substring(6)) == null)) problems.add("job place " + t.target() + " (" + pool + ")"); }
                default -> {}
            }
        }
        var professions = BuiltInRegistries.VILLAGER_PROFESSION.keySet().stream().map(Identifier::getPath).toList();
        for (var job : JOB_MODS.entrySet()) {
            if (!Modpack.installed(job.getValue())) continue;
            checked++;
            if (!professions.contains(job.getKey())) problems.add("profession " + job.getValue() + ":" + job.getKey());
        }
        Rpg.LOGGER.info("Modpack audit: mods present {}; {} names checked, {} problems{}", Modpack.present(), checked, problems.size(),
                problems.isEmpty() ? "" : ": " + String.join(", ", problems));
        return problems;
    }
}
