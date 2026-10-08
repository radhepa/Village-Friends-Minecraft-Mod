package dev.villagefriends.home;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.level.levelgen.structure.BoundingBox;

/**
 * Finds the rooms of a house a player built, starting from its House Plaque. Pure: the world is read
 * through a {@link Grid}, so it is unit-tested.
 *
 * <p>The first room is the open air the plaque looks into (or, for a plaque on an outside wall, the air
 * just behind that wall). Doors, fence gates and trapdoors are always walls. Past each door the search
 * floods the far side: if that leaks to the open sky or grows too large the door leads outdoors, otherwise
 * it is another room. The house is accepted when its first room is closed.
 */
public final class FloodFill {
    /** What the search sees at a cell: open air (empty collision), a wall, a door, open air under the sky, or a chunk that isn't loaded. */
    public enum Cell { OPEN, SOLID, DOOR, SKY, UNLOADED }
    public interface Grid { Cell cell(int x, int y, int z); }

    public enum Status { OK, OPEN_TO_SKY, TOO_BIG, UNLOADED, NO_ROOM }
    /** At most this many open cells in the whole house, a box at most this big, and at most this many rooms. */
    public static final int MAX_CELLS = 6000, MAX_WIDTH = 32, MAX_HEIGHT = 24, MAX_ROOMS = 12;

    /**
     * The search's answer. {@code rooms} are each room's cells, {@code doors} every door cell met (both halves of
     * a door), {@code exterior} the door cells that lead outdoors, {@code leak} where the first room is open to the
     * sky (when it is), and {@code start} the cell the accepted first room was flooded from.
     */
    public record Result(Status status, List<Set<BlockPos>> rooms, Set<BlockPos> doors, Set<BlockPos> exterior, BlockPos leak, BlockPos start) {
        public boolean ok() { return status == Status.OK; }
        public int cells() { int n = 0; for (var r : rooms) n += r.size(); return n; }
        /** The room a cell is in, or -1. */
        public int room(BlockPos pos) {
            for (int r = 0; r < rooms.size(); r++) if (rooms.get(r).contains(pos)) return r;
            return -1;
        }
        public BoundingBox box() {
            BoundingBox box = null;
            for (var room : rooms) for (var p : room) box = box == null ? new BoundingBox(p) : box.encapsulate(p);
            return box;
        }
        public static BoundingBox box(Set<BlockPos> cells) {
            BoundingBox box = null;
            for (var p : cells) box = box == null ? new BoundingBox(p) : box.encapsulate(p);
            return box;
        }
    }

    /** One flood: its cells, the door cells around it and where it stopped. */
    private record Flood(Status status, Set<BlockPos> cells, Map<BlockPos, Direction> doors, BlockPos leak) {}

    /** The house around a plaque at {@code plaque} facing {@code facing} (the way it is read from). */
    public static Result fromPlaque(Grid grid, BlockPos plaque, Direction facing, boolean standing) {
        var starts = new ArrayList<BlockPos>();
        if (standing) {
            // A plaque on a post stands in the room it names.
            starts.add(plaque.relative(facing)); starts.add(plaque.above());
            for (var d : Direction.Plane.HORIZONTAL) if (d != facing) starts.add(plaque.relative(d));
        } else {
            // In front of the plaque, or for one on an outside wall, just behind the wall it hangs on.
            starts.add(plaque.relative(facing));
            for (int depth = 2; depth <= 3; depth++) starts.add(plaque.relative(facing.getOpposite(), depth));
        }
        return fill(grid, starts);
    }

    /**
     * The house around the first of {@code starts} whose room is closed; failing that, why the first one that was
     * indoor air didn't close. Starts out under the open sky are outdoors, not a room.
     */
    public static Result fill(Grid grid, List<BlockPos> starts) {
        Result first = null;
        for (var start : starts) {
            var cell = grid.cell(start.getX(), start.getY(), start.getZ());
            if (cell == Cell.UNLOADED) return failure(Status.UNLOADED, null, start);
            if (cell != Cell.OPEN) continue;
            var result = fill(grid, start);
            if (result.ok()) return result;
            if (first == null) first = result;
        }
        return first != null ? first : failure(Status.NO_ROOM, null, null);
    }

    /** The house whose first room holds {@code start}. */
    public static Result fill(Grid grid, BlockPos start) {
        var room0 = flood(grid, start, MAX_CELLS, null);
        if (room0.status() != Status.OK) return failure(room0.status(), room0.leak(), start);
        var rooms = new ArrayList<Set<BlockPos>>(); rooms.add(room0.cells());
        var doors = new LinkedHashSet<BlockPos>(); var exterior = new LinkedHashSet<BlockPos>();
        var claimed = new HashSet<>(room0.cells());
        var queue = new ArrayDeque<Map.Entry<BlockPos, Direction>>(room0.doors().entrySet());
        int total = room0.cells().size();
        var box = Result.box(room0.cells());
        while (!queue.isEmpty()) {
            var door = queue.poll();
            var d = door.getKey(); var through = door.getValue();
            if (!doors.add(d)) continue;
            // Straight on through the door: a door in a wall has a room on each side.
            var far = d.relative(through);
            if (claimed.contains(far)) continue;
            var cell = grid.cell(far.getX(), far.getY(), far.getZ());
            if (cell == Cell.SKY) { exterior.add(d); continue; }
            if (cell != Cell.OPEN) continue;
            if (rooms.size() >= MAX_ROOMS) continue;
            var next = flood(grid, far, MAX_CELLS - total, box);
            if (next.status() == Status.UNLOADED) return failure(Status.UNLOADED, null, start);
            if (next.status() != Status.OK) { exterior.add(d); continue; }
            rooms.add(next.cells()); claimed.addAll(next.cells()); total += next.cells().size();
            for (var p : next.cells()) box = box.encapsulate(p);
            queue.addAll(next.doors().entrySet());
        }
        // Both halves of an outside door lead outdoors.
        for (var d : List.copyOf(exterior)) for (var v : new BlockPos[]{d.above(), d.below()}) if (doors.contains(v)) exterior.add(v);
        return new Result(Status.OK, List.copyOf(rooms), Set.copyOf(doors), Set.copyOf(exterior), null, start);
    }
    private static Result failure(Status status, BlockPos leak, BlockPos start) { return new Result(status, List.of(), Set.of(), Set.of(), leak, start); }

    /** Floods open air from {@code start} with doors as walls, up to {@code budget} cells, within the size limits around {@code house}. */
    private static Flood flood(Grid grid, BlockPos start, int budget, BoundingBox house) {
        var cells = new LinkedHashSet<BlockPos>(); var doors = new HashMap<BlockPos, Direction>();
        var queue = new ArrayDeque<BlockPos>();
        var startCell = grid.cell(start.getX(), start.getY(), start.getZ());
        if (startCell == Cell.SKY) return new Flood(Status.OPEN_TO_SKY, Set.of(), Map.of(), start);
        if (startCell != Cell.OPEN) return new Flood(Status.NO_ROOM, Set.of(), Map.of(), null);
        cells.add(start); queue.add(start);
        // BoundingBox grows in place, so work on a copy of the house's box.
        var box = house == null ? new BoundingBox(start) : house.moved(0, 0, 0).encapsulate(start);
        while (!queue.isEmpty()) {
            var p = queue.poll();
            for (var d : Direction.values()) {
                var n = p.relative(d);
                if (cells.contains(n) || doors.containsKey(n)) continue;
                switch (grid.cell(n.getX(), n.getY(), n.getZ())) {
                    case UNLOADED -> { return new Flood(Status.UNLOADED, Set.of(), Map.of(), n); }
                    case SKY -> { return new Flood(Status.OPEN_TO_SKY, Set.of(), Map.of(), n); }
                    case DOOR -> { if (d.getAxis().isHorizontal()) doors.put(n, d); }
                    case OPEN -> {
                        box = box.encapsulate(n);
                        if (cells.size() >= budget || box.getXSpan() > MAX_WIDTH || box.getZSpan() > MAX_WIDTH || box.getYSpan() > MAX_HEIGHT)
                            return new Flood(Status.TOO_BIG, Set.of(), Map.of(), n);
                        cells.add(n); queue.add(n);
                    }
                    case SOLID -> {}
                }
            }
        }
        return new Flood(Status.OK, Set.copyOf(cells), Map.copyOf(doors), null);
    }

    private FloodFill() {}
}
