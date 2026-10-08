package dev.villagefriends;

import static org.junit.jupiter.api.Assertions.*;

import dev.villagefriends.home.FloodFill;
import dev.villagefriends.home.FloodFill.Cell;
import dev.villagefriends.home.FloodFill.Status;
import java.util.HashMap;
import java.util.Map;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import org.junit.jupiter.api.Test;

class FloodFillTest {
    /** A tiny world: solid ground at y <= 0, open sky above it, and whatever a test builds. */
    private static final class World implements FloodFill.Grid {
        final Map<BlockPos, Cell> cells = new HashMap<>();
        int unloadedFromX = Integer.MAX_VALUE;
        @Override public Cell cell(int x, int y, int z) {
            if (x >= unloadedFromX) return Cell.UNLOADED;
            var c = cells.get(new BlockPos(x, y, z));
            if (c != null) return c;
            return y <= 0 ? Cell.SOLID : Cell.SKY;
        }
        World fill(int x0, int y0, int z0, int x1, int y1, int z1, Cell cell) {
            for (int x = x0; x <= x1; x++) for (int y = y0; y <= y1; y++) for (int z = z0; z <= z1; z++) cells.put(new BlockPos(x, y, z), cell);
            return this;
        }
        World set(int x, int y, int z, Cell cell) { cells.put(new BlockPos(x, y, z), cell); return this; }
        /** A closed box house: walls, floor and roof from (x0,y0,z0) to (x1,y1,z1), air inside. */
        World house(int x0, int y0, int z0, int x1, int y1, int z1) {
            fill(x0, y0, z0, x1, y1, z1, Cell.SOLID);
            return fill(x0 + 1, y0 + 1, z0 + 1, x1 - 1, y1 - 1, z1 - 1, Cell.OPEN);
        }
        /** A two-block door at (x, y..y+1, z). */
        World door(int x, int y, int z) { set(x, y, z, Cell.DOOR); return set(x, y + 1, z, Cell.DOOR); }
    }
    /** A 7x5x7 house from (0,0,0) to (6,5,6) with a plaque on the inside of its west wall, facing east. */
    private static World cottage() { return new World().house(0, 0, 0, 6, 5, 6).set(1, 2, 3, Cell.SOLID); }
    private static final BlockPos PLAQUE = new BlockPos(1, 2, 3);

    @Test void aClosedOneRoomHouse() {
        var r = FloodFill.fromPlaque(cottage(), PLAQUE, Direction.EAST, false);
        assertEquals(Status.OK, r.status());
        assertEquals(1, r.rooms().size());
        assertEquals(5 * 4 * 5 - 1, r.cells(), "Every open cell inside but the plaque's own");
        assertTrue(r.doors().isEmpty() && r.exterior().isEmpty());
    }

    @Test void aDoorSplitsTwoRooms() {
        var w = cottage().fill(3, 1, 1, 3, 4, 5, Cell.SOLID).door(3, 1, 3);
        var r = FloodFill.fromPlaque(w, PLAQUE, Direction.EAST, false);
        assertEquals(Status.OK, r.status());
        assertEquals(2, r.rooms().size(), "The door between them makes two rooms");
        assertEquals(0, r.room(new BlockPos(2, 1, 2)));
        assertEquals(1, r.room(new BlockPos(4, 1, 2)));
        assertTrue(r.doors().contains(new BlockPos(3, 1, 3)) && r.doors().contains(new BlockPos(3, 2, 3)));
        assertTrue(r.exterior().isEmpty(), "An inside door doesn't lead outdoors");
    }

    @Test void anOutsideDoorLeadsOut() {
        var w = cottage().door(6, 1, 3);
        var r = FloodFill.fromPlaque(w, PLAQUE, Direction.EAST, false);
        assertEquals(Status.OK, r.status(), "A front door doesn't open the house to the sky");
        assertEquals(1, r.rooms().size());
        assertTrue(r.exterior().contains(new BlockPos(6, 1, 3)) && r.exterior().contains(new BlockPos(6, 2, 3)), "Both halves of the front door lead outdoors");
    }

    @Test void aHoleInTheRoofLeaksToTheSky() {
        var w = cottage().set(3, 5, 3, Cell.SKY);
        var r = FloodFill.fromPlaque(w, PLAQUE, Direction.EAST, false);
        assertEquals(Status.OPEN_TO_SKY, r.status());
        assertEquals(new BlockPos(3, 5, 3), r.leak(), "The leak is where the sky gets in");
    }

    @Test void aHugeHallIsTooBig() {
        var w = new World().house(0, 0, 0, 41, 11, 41).set(1, 2, 3, Cell.SOLID);
        var r = FloodFill.fromPlaque(w, PLAQUE, Direction.EAST, false);
        assertEquals(Status.TOO_BIG, r.status(), "A 40x10x40 hall is over the limit");
        // A long thin hall is over the width limit even with few cells.
        var thin = new World().house(0, 0, 0, 40, 3, 2).set(1, 2, 1, Cell.SOLID);
        assertEquals(Status.TOO_BIG, FloodFill.fromPlaque(thin, new BlockPos(1, 2, 1), Direction.EAST, false).status());
    }

    @Test void anUnloadedChunkStopsTheSearch() {
        var w = cottage(); w.unloadedFromX = 4;
        assertEquals(Status.UNLOADED, FloodFill.fromPlaque(w, PLAQUE, Direction.EAST, false).status());
    }

    @Test void aBedBelongsToTheRoomAboveIt() {
        // A bed is solid; the air above its head is in the room.
        var w = cottage().set(5, 1, 5, Cell.SOLID).set(5, 1, 4, Cell.SOLID);
        var r = FloodFill.fromPlaque(w, PLAQUE, Direction.EAST, false);
        assertEquals(Status.OK, r.status());
        assertEquals(-1, r.room(new BlockPos(5, 1, 5)), "The bed itself is no room cell");
        assertEquals(0, r.room(new BlockPos(5, 2, 5)), "The cell above its head is in the room");
    }

    @Test void aPlaqueOnTheOutsideWallFindsTheRoomBehindIt() {
        // Hung outside, beside the front door, facing west.
        var w = cottage().set(-1, 2, 3, Cell.SOLID);
        w.cells.remove(new BlockPos(1, 2, 3)); w.set(1, 2, 3, Cell.OPEN);
        var r = FloodFill.fromPlaque(w, new BlockPos(-1, 2, 3), Direction.WEST, false);
        assertEquals(Status.OK, r.status());
        assertEquals(new BlockPos(1, 2, 3), r.start(), "It floods from just behind the wall it hangs on");
        assertEquals(5 * 4 * 5, r.cells());
        // A plaque on a fence in a field finds no room.
        var field = new World().set(10, 1, 10, Cell.SOLID);
        assertNotEquals(Status.OK, FloodFill.fromPlaque(field, new BlockPos(10, 1, 10), Direction.NORTH, true).status());
    }
}
