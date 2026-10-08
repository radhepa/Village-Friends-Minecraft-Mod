package dev.villagefriends.home;

import dev.villagefriends.VillageSettlements;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Optional;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.Registries;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.BlockTags;
import net.minecraft.tags.PoiTypeTags;
import net.minecraft.tags.StructureTags;
import net.minecraft.world.entity.ai.village.poi.PoiManager;
import net.minecraft.world.entity.ai.village.poi.PoiTypes;
import net.minecraft.world.level.block.AbstractBedBlock;
import net.minecraft.world.level.block.FenceGateBlock;
import net.minecraft.world.level.block.HorizontalDirectionalBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.properties.BedPart;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.structure.BoundingBox;
import net.minecraft.world.level.levelgen.structure.PoolElementStructurePiece;
import net.minecraft.world.level.levelgen.structure.StructureStart;
import net.minecraft.world.level.levelgen.structure.pools.SinglePoolElement;

/**
 * Reads houses from the world. A village's own houses come from its structure: every piece whose template
 * has beds becomes a house from the catalog, turned and moved the way the piece was placed, without reading
 * a block. Once a house's chunks are loaded it is checked once against the real beds and job sites (a bed
 * that was broken is no longer slept in; one a player added is). A house a player built is found by
 * flooding the air around its House Plaque ({@link FloodFill}); beds in a village with no structure (one
 * placed by command, or claimed with a marker) get a house flooded from the room they stand in.
 */
public final class HouseSurvey {
    /** How far to look for loose beds around a resident when a village has no structure to read. */
    public static final int FOUND_REACH = 48;

    /** What looking for a village's structure found: its start (null for none), or {@code retry} when it couldn't tell yet. */
    public record Probe(StructureStart start, boolean retry) {}

    /**
     * Finds a village's structure from a resident's position and from the village's center: a piece at either,
     * or else the structure's bounds around either (a resident on the grass between a house and the street).
     * A village found through its structure ({@code natural:}) always has one, so when a probe can't be made yet
     * (its chunk isn't loaded, or the structure's chunks aren't ready) the answer is "try again later", never
     * "no structure"; only a village with none (placed by command, or claimed with a marker) falls back to
     * houses found around its beds.
     */
    public static Probe structureFor(ServerLevel level, BlockPos pos, String village) {
        var probes = new ArrayList<BlockPos>(List.of(pos));
        var record = VillageSettlements.book(level).villages().get(village);
        if (record != null) probes.add(new BlockPos(record.x(), record.y(), record.z()));
        boolean unsure = false;
        for (var p : probes) {
            if (!level.isLoaded(p)) { unsure = true; continue; }
            try {
                var start = level.structureManager().getStructureWithPieceAt(p, StructureTags.VILLAGE);
                if (start == null || !start.isValid()) start = level.structureManager().getStructureAt(p, level.registryAccess().lookupOrThrow(Registries.STRUCTURE).getOrThrow(StructureTags.VILLAGE));
                if (start != null && start.isValid()) return new Probe(start, false);
            } catch (RuntimeException e) {
                // Structure references can point at chunks that aren't ready yet.
                unsure = true;
            }
        }
        return new Probe(null, unsure && village.startsWith("natural:"));
    }

    /** Every house a village structure built, from its pieces and the catalog. Reads no blocks. */
    public static List<House> fromStructure(StructureStart start) {
        var catalog = HouseCatalog.builtin(); var out = new ArrayList<House>();
        for (var piece : start.getPieces()) {
            if (!(piece instanceof PoolElementStructurePiece pool) || !(pool.getElement() instanceof SinglePoolElement single)) continue;
            var template = catalog.template(single.getTemplateLocation().toString());
            if (template == null) continue;
            out.add(HouseCatalog.house(template, pool.getRotation(), pool.getPosition(), pool.getBoundingBox()));
        }
        out.sort(Comparator.comparing(House::id));
        return out;
    }

    /** Whether every chunk a house stands in is loaded, so it can be checked without loading any. */
    public static boolean loaded(ServerLevel level, BoundingBox box) {
        return level.hasChunksAt(box.minX(), box.minZ(), box.maxX(), box.maxZ());
    }

    /**
     * Checks a house against the world: catalog beds that are gone, beds and job sites a player added. One
     * block read per known bed; beds and job sites are found through vanilla's points of interest.
     */
    public static House verify(ServerLevel level, House house, long tick) {
        var box = house.box();
        var beds = new ArrayList<House.Bed>();
        var known = new HashMap<BlockPos, House.Bed>();
        for (var b : house.beds()) known.put(b.head(), b);
        for (var b : house.beds()) {
            var state = level.getBlockState(b.foot());
            boolean present = state.getBlock() instanceof AbstractBedBlock && state.getValue(AbstractBedBlock.PART) == BedPart.FOOT
                    && state.getValue(HorizontalDirectionalBlock.FACING) == b.facing();
            beds.add(b.present(present));
        }
        var poi = level.getPoiManager(); int radius = radius(box);
        poi.findAll(h -> h.is(PoiTypes.HOME), box::isInside, center(box), radius, PoiManager.Occupancy.ANY).sorted().forEach(head -> {
            if (known.containsKey(head)) return;
            var bed = bedAt(level, head);
            if (bed != null) beds.add(new House.Bed(bed.head(), bed.foot(), bed.facing(), Math.max(0, roomOf(house, bed)), true));
        });
        var stations = new ArrayList<House.Workstation>();
        poi.findAllWithType(h -> h.is(PoiTypeTags.ACQUIRABLE_JOB_SITE), box::isInside, center(box), radius, PoiManager.Occupancy.ANY)
                .sorted(Comparator.comparing(p -> p.getSecond()))
                .forEach(p -> stations.add(new House.Workstation(p.getSecond().immutable(), p.getFirst().unwrapKey().map(k -> k.identifier().toString()).orElse("minecraft:unknown"))));
        return house.verified(beds, stations, tick);
    }
    private static int radius(BoundingBox box) { return Math.max(box.getXSpan(), Math.max(box.getYSpan(), box.getZSpan())) / 2 + 2; }
    private static BlockPos center(BoundingBox box) { return box.getCenter(); }
    /** The room a bed belongs to: the room above its head or foot, or the nearest one. */
    static int roomOf(House house, House.Bed bed) {
        int r = house.roomAt(bed.head().above());
        if (r < 0) r = house.roomAt(bed.foot().above());
        if (r >= 0 || house.rooms().isEmpty()) return r;
        int best = 0; double distance = Double.MAX_VALUE;
        for (int i = 0; i < house.rooms().size(); i++) {
            double d = house.rooms().get(i).box().getCenter().distSqr(bed.head());
            if (d < distance) { distance = d; best = i; }
        }
        return best;
    }
    /** The bed whose head is at {@code head}, read from the world, or null. */
    public static House.Bed bedAt(ServerLevel level, BlockPos head) {
        var state = level.getBlockState(head);
        if (!(state.getBlock() instanceof AbstractBedBlock)) return null;
        var facing = state.getValue(HorizontalDirectionalBlock.FACING);
        if (state.getValue(AbstractBedBlock.PART) == BedPart.FOOT) { head = head.relative(facing); }
        return new House.Bed(head.immutable(), head.relative(facing.getOpposite()).immutable(), facing, 0, true);
    }

    // -- flooding rooms ----------------------------------------------------------------------------

    /** The world as {@link FloodFill} sees it: loaded chunks only. */
    public static FloodFill.Grid grid(ServerLevel level) {
        var cursor = new BlockPos.MutableBlockPos();
        return (x, y, z) -> {
            cursor.set(x, y, z);
            if (!level.isLoaded(cursor)) return FloodFill.Cell.UNLOADED;
            var state = level.getBlockState(cursor);
            if (door(state)) return FloodFill.Cell.DOOR;
            if (!state.getCollisionShape(level, cursor).isEmpty()) return FloodFill.Cell.SOLID;
            // Under the open sky: nothing above it blocks movement. (The heightmap, unlike sky light, is current the moment a roof goes on.)
            return y >= level.getHeight(Heightmap.Types.MOTION_BLOCKING, x, z) ? FloodFill.Cell.SKY : FloodFill.Cell.OPEN;
        };
    }
    /** Doors, fence gates and trapdoors: always the edge of a room. */
    public static boolean door(BlockState state) {
        return state.is(BlockTags.DOORS) || state.is(BlockTags.TRAPDOORS) || state.getBlock() instanceof FenceGateBlock;
    }

    /** The house a flood found: rooms "Room 1".."Room n", the beds whose head or foot has a room cell above it, its doors and job sites. */
    public static House fromFlood(ServerLevel level, String id, House.Kind kind, FloodFill.Result flood, BlockPos plaque, String name, boolean privateHome, long tick) {
        var rooms = new ArrayList<House.Room>();
        for (int i = 0; i < flood.rooms().size(); i++) rooms.add(new House.Room("Room " + (i + 1), FloodFill.Result.box(flood.rooms().get(i))));
        // The house is its rooms and the walls, floor and roof around them.
        var box = flood.box().inflatedBy(1);
        var beds = new ArrayList<House.Bed>();
        var seen = new java.util.HashSet<BlockPos>();
        for (var p : BlockPos.betweenClosed(box.minX(), box.minY(), box.minZ(), box.maxX(), box.maxY(), box.maxZ())) {
            var state = level.getBlockState(p);
            if (!(state.getBlock() instanceof AbstractBedBlock) || state.getValue(AbstractBedBlock.PART) != BedPart.HEAD) continue;
            var bed = bedAt(level, p.immutable());
            if (bed == null || !seen.add(bed.head())) continue;
            int room = flood.room(bed.head().above());
            if (room < 0) room = flood.room(bed.foot().above());
            if (room >= 0) beds.add(new House.Bed(bed.head(), bed.foot(), bed.facing(), room, true));
        }
        var doors = new ArrayList<>(flood.doors()); doors.sort(Comparator.naturalOrder());
        var stations = new ArrayList<House.Workstation>();
        level.getPoiManager().findAllWithType(h -> h.is(PoiTypeTags.ACQUIRABLE_JOB_SITE), box::isInside, box.getCenter(), radius(box), PoiManager.Occupancy.ANY)
                .sorted(Comparator.comparing(p -> p.getSecond()))
                .forEach(p -> stations.add(new House.Workstation(p.getSecond().immutable(), p.getFirst().unwrapKey().map(k -> k.identifier().toString()).orElse("minecraft:unknown"))));
        return new House(id, kind, "", House.Use.HOME, box, rooms, beds, doors, stations, Optional.ofNullable(plaque), name, privateHome, true, tick);
    }

    /** A bed that no house covers, in a village with no structure: the house flooded from the room it stands in, or a nook around the bed alone. */
    public static House found(ServerLevel level, BlockPos head, long tick) {
        var bed = bedAt(level, head);
        if (bed == null) return null;
        var grid = grid(level);
        var flood = FloodFill.fill(grid, List.of(bed.head().above(), bed.foot().above()));
        String id = "f:" + bed.head().getX() + "," + bed.head().getY() + "," + bed.head().getZ();
        if (flood.status() == FloodFill.Status.UNLOADED) return null;
        if (flood.ok()) return fromFlood(level, id, House.Kind.FOUND, flood, null, "", false, tick);
        // An open shelter or a bed under the stars still belongs to someone.
        var box = BoundingBox.fromCorners(bed.head(), bed.foot()).inflatedBy(1);
        return new House(id, House.Kind.FOUND, "", House.Use.HOME, box, List.of(new House.Room("Bed nook", box)), List.of(bed),
                List.of(), List.of(), Optional.empty(), "", false, true, tick);
    }

    /** Whether a block change can matter to a house: beds, doors, plaques and anything vanilla counts as a point of interest. */
    public static boolean relevant(BlockState state) {
        return state.getBlock() instanceof AbstractBedBlock || state.getBlock() instanceof HousePlaqueBlock || door(state) || PoiTypes.hasPoi(state);
    }

    private HouseSurvey() {}
}
