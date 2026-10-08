package dev.villagefriends.home;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import dev.villagefriends.VillageProfessions;
import java.io.InputStreamReader;
import java.io.Reader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.level.block.Mirror;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.levelgen.structure.BoundingBox;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplate;

/**
 * The houses every village type can build, read from the structure catalog the compiler writes
 * ({@code tools/create_village_structures.py}): for each template with beds, its role, bedrooms, beds (with
 * their facing and room), doors and anchors, in the template's own coordinates. A generated house is this
 * geometry turned and moved to where its structure piece was placed, so finding a village's houses reads no
 * blocks at all. Loaded once from the mod's resources.
 */
public final class HouseCatalog {
    private static final String PATH = "/data/villagefriends/villagefriends/structure-catalog.json";
    private static volatile HouseCatalog builtin;

    public record RoomSpec(String name, BlockPos min, BlockPos max) {}
    public record Anchor(String id, BlockPos pos) {}
    /** A template with beds, in its own coordinates (0,0,0 is its corner before rotation). */
    public record Template(String id, House.Use use, List<RoomSpec> rooms, List<BlockPos> doors, List<BlockPos> exteriorDoors,
                           List<BlockPos> bedFeet, List<Direction> bedFacing, List<Integer> bedRoom, List<Anchor> anchors) {
        /** "taiga/log_lodge" for "villagefriends:village/taiga/log_lodge". */
        public String name() { int slash = id.indexOf("village/"); return slash < 0 ? id : id.substring(slash + 8); }
        public Optional<BlockPos> plaque() {
            return anchors.stream().filter(a -> a.id().equals("villagefriends:house_plaque")).map(Anchor::pos).findFirst();
        }
        /** The jobs whose workstations the template has, from its anchors. */
        public List<String> jobs() {
            return anchors.stream().map(a -> JOB_OF_STATION.get(a.id())).filter(j -> j != null).distinct().sorted().toList();
        }
    }

    /** "villagefriends:alchemical_press" to "apothecary", for every Village Friends workstation. */
    static final Map<String, String> JOB_OF_STATION = new HashMap<>();
    static {
        for (String job : VillageProfessions.JOBS) for (String station : VillageProfessions.workstations(job)) JOB_OF_STATION.put("villagefriends:" + station, job);
    }

    private final Map<String, Template> templates;
    private HouseCatalog(Map<String, Template> templates) { this.templates = Map.copyOf(templates); }

    public static HouseCatalog builtin() {
        var catalog = builtin;
        if (catalog == null) {
            try (var stream = HouseCatalog.class.getResourceAsStream(PATH)) {
                if (stream == null) throw new IllegalStateException("Bundled structure catalog missing");
                builtin = catalog = parse(new InputStreamReader(stream, StandardCharsets.UTF_8));
            } catch (java.io.IOException e) { throw new IllegalStateException("Cannot read the structure catalog", e); }
        }
        return catalog;
    }

    /** Reads a structure catalog, keeping only the templates with beds. */
    public static HouseCatalog parse(Reader reader) {
        var root = JsonParser.parseReader(reader).getAsJsonObject();
        var out = new LinkedHashMap<String, Template>();
        for (var e : root.getAsJsonArray("templates")) {
            var t = e.getAsJsonObject();
            var feet = positions(t.getAsJsonArray("bed_feet"));
            if (feet.isEmpty()) continue;
            String id = t.get("id").getAsString();
            var rooms = new ArrayList<RoomSpec>();
            for (var r : t.getAsJsonArray("rooms")) {
                var room = r.getAsJsonObject();
                rooms.add(new RoomSpec(room.get("name").getAsString(), pos(room.getAsJsonArray("min")), pos(room.getAsJsonArray("max"))));
            }
            var facing = new ArrayList<Direction>();
            var facings = t.getAsJsonArray("bed_facing");
            for (int n = 0; n < feet.size(); n++) facing.add(facings == null || n >= facings.size() ? Direction.NORTH : Direction.byName(facings.get(n).getAsString()));
            var bedRoom = new ArrayList<Integer>();
            var bedRooms = t.getAsJsonArray("bed_room");
            for (int n = 0; n < feet.size(); n++) bedRoom.add(bedRooms == null || n >= bedRooms.size() ? -1 : bedRooms.get(n).getAsInt());
            var anchors = new ArrayList<Anchor>();
            for (var a : t.getAsJsonArray("anchors")) anchors.add(new Anchor(a.getAsJsonObject().get("id").getAsString(), pos(a.getAsJsonObject().getAsJsonArray("pos"))));
            out.put(id, new Template(id, House.Use.of(string(t, "use")), List.copyOf(rooms), positions(t.getAsJsonArray("doors")),
                    positions(t.getAsJsonArray("exterior_doors")), feet, List.copyOf(facing), List.copyOf(bedRoom), List.copyOf(anchors)));
        }
        return new HouseCatalog(out);
    }
    private static String string(JsonObject o, String key) { var e = o.get(key); return e == null || e.isJsonNull() ? "" : e.getAsString(); }
    private static BlockPos pos(JsonArray a) { return new BlockPos(a.get(0).getAsInt(), a.get(1).getAsInt(), a.get(2).getAsInt()); }
    private static List<BlockPos> positions(JsonArray list) {
        if (list == null) return List.of();
        var out = new ArrayList<BlockPos>();
        for (JsonElement e : list) out.add(pos(e.getAsJsonArray()));
        return List.copyOf(out);
    }

    /** The template with beds called {@code id} ("villagefriends:village/cottage_oak"), or null. */
    public Template template(String id) { return templates.get(id); }
    public java.util.Collection<Template> templates() { return templates.values(); }

    // -- placing a template ------------------------------------------------------------------------

    /** Where a point of a template ends up once its piece is turned by {@code rotation} and moved to {@code origin}, as the jigsaw places it. */
    public static BlockPos place(BlockPos local, Rotation rotation, BlockPos origin) {
        return StructureTemplate.transform(local, Mirror.NONE, rotation, BlockPos.ZERO).offset(origin);
    }

    /** The house a template becomes when its structure piece was placed at {@code origin}, turned by {@code rotation}, filling {@code box}. */
    public static House house(Template t, Rotation rotation, BlockPos origin, BoundingBox box) {
        var rooms = new ArrayList<House.Room>();
        for (var r : t.rooms()) rooms.add(new House.Room(r.name(), BoundingBox.fromCorners(place(r.min(), rotation, origin), place(r.max(), rotation, origin))));
        var beds = new ArrayList<House.Bed>();
        for (int n = 0; n < t.bedFeet().size(); n++) {
            var foot = place(t.bedFeet().get(n), rotation, origin);
            var facing = rotation.rotate(t.bedFacing().get(n));
            beds.add(new House.Bed(foot.relative(facing), foot, facing, Math.max(0, t.bedRoom().get(n)), true));
        }
        var doors = new ArrayList<BlockPos>();
        for (var d : t.doors()) doors.add(place(d, rotation, origin));
        var stations = new ArrayList<House.Workstation>();
        for (var a : t.anchors()) {
            String job = JOB_OF_STATION.get(a.id());
            if (job != null) stations.add(new House.Workstation(place(a.pos(), rotation, origin), "villagefriends:" + job));
        }
        var plaque = t.plaque().map(p -> place(p, rotation, origin));
        String id = "g:" + t.name() + "@" + box.minX() + "," + box.minY() + "," + box.minZ();
        return new House(id, House.Kind.GENERATED, t.id(), t.use(), box, rooms, beds, doors, stations, plaque, "", false, false, 0);
    }
}
