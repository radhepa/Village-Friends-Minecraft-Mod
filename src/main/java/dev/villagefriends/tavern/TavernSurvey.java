package dev.villagefriends.tavern;

import dev.villagefriends.VillageBlocks;
import dev.villagefriends.VillageProfessions;
import dev.villagefriends.tavern.Patronage.Kind;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.BlockTags;
import net.minecraft.world.entity.ai.village.poi.PoiManager;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.CampfireBlock;
import net.minecraft.world.level.block.DoorBlock;
import net.minecraft.world.level.block.HorizontalDirectionalBlock;
import net.minecraft.world.level.block.StairBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.properties.Half;
import net.minecraft.world.level.block.state.properties.StairsShape;
import net.minecraft.world.level.levelgen.structure.BoundingBox;
import net.minecraft.world.level.levelgen.structure.PoolElementStructurePiece;
import net.minecraft.world.level.levelgen.structure.pools.SinglePoolElement;

/**
 * Looks a tavern over: the building (its village structure piece, so taverns of every village type and
 * any future redesign are understood the same way, or a box around the keeper's station for a tavern
 * players built themselves), its seats and which table each belongs to, which seats are by the fire or
 * out on the terrace, where people can stand at the bar, and the bard's stage.
 */
public final class TavernSurvey {
    /** A place to sit: which way it faces, how high its surface is, and the table it belongs to. */
    public record Spot(BlockPos pos, float yaw, double surface, Kind kind, int table, boolean hearth, boolean outdoor) {}
    /** A place to stand and lean on the bar, facing it. */
    public record Stand(BlockPos pos, float yaw) {}
    public record Tavern(String key, BoundingBox box, List<BlockPos> stations, List<Spot> seats, List<Stand> standing, BlockPos stage,
            Map<Integer, Integer> tableSeats, List<BlockPos> stoves) {
        public Spot seat(BlockPos pos) {
            for (var s : seats) if (s.pos().equals(pos)) return s;
            return null;
        }
        public boolean contains(BlockPos pos) { return box.inflatedBy(2).isInside(pos); }
    }

    private static final int FALLBACK_REACH = 10, HEARTH_REACH = 4;

    /** The tavern whose keeper's station is at {@code station}, looked over fresh. */
    public static Tavern survey(ServerLevel level, BlockPos station) {
        var box = building(level, station);
        var poi = VillageProfessions.poiKey("tavern_keeper");
        var stations = level.getPoiManager().findAll(h -> h.is(poi), box::isInside, box.getCenter(),
                Math.max(box.getXSpan(), box.getZSpan()), PoiManager.Occupancy.ANY).map(BlockPos::immutable).sorted().toList();
        if (stations.isEmpty()) stations = List.of(station.immutable());
        var seats = new ArrayList<Spot>(); var fires = new ArrayList<BlockPos>(); var stoves = new ArrayList<BlockPos>(); BlockPos stage = null;
        var tables = new HashSet<BlockPos>();
        var stove = VillageBlocks.get("kitchen_stove");
        for (var p : BlockPos.betweenClosed(box.minX(), box.minY(), box.minZ(), box.maxX(), box.maxY(), box.maxZ())) {
            var state = level.getBlockState(p);
            if (state.isAir()) continue;
            if (state.is(Blocks.CAMPFIRE) && state.getValue(CampfireBlock.LIT) || state.is(BlockTags.FIRE)) fires.add(p.immutable());
            if (stage == null && (state.is(Blocks.NOTE_BLOCK) || state.is(Blocks.JUKEBOX))) stage = p.immutable();
            if (state.is(stove)) stoves.add(p.immutable());
            if (table(level, p)) tables.add(p.immutable());
            var spot = seatAt(level, p, state);
            if (spot != null) seats.add(spot);
        }
        // Which table each seat belongs to: the table in front of it, the bar for a stool, or its neighbors for loose benches.
        var group = new HashMap<BlockPos, Integer>(); int next = 0;
        for (var t : tables) if (!group.containsKey(t)) { flood(t, tables, group, next); next++; }
        var grouped = new ArrayList<Spot>();
        var loose = new ArrayList<Spot>();
        for (var s : seats) {
            var front = s.pos().relative(Direction.fromYRot(s.yaw()));
            Integer id = group.get(front);
            if (id == null && s.kind() == Kind.STOOL && counter(level, front)) {
                id = group.get(front);
                if (id == null) {
                    // A bar counter is one long table for everyone on its stools.
                    var bar = new HashSet<BlockPos>(); collectCounter(level, front, bar, 24);
                    for (var c : bar) group.put(c, next);
                    id = next++;
                }
            }
            if (id == null) { loose.add(s); continue; }
            grouped.add(with(s, id, fires, level));
        }
        // Benches and armchairs with no table join up with whatever loose seats are beside them (two armchairs at the fire).
        var looseGroup = new HashMap<Spot, Integer>();
        for (var s : loose) {
            Integer id = null;
            for (var o : looseGroup.keySet()) if (o.pos().distManhattan(s.pos()) <= 3) { id = looseGroup.get(o); break; }
            looseGroup.put(s, id == null ? next++ : id);
        }
        for (var s : loose) grouped.add(with(s, looseGroup.get(s), fires, level));
        var tableSeats = new HashMap<Integer, Integer>();
        for (var s : grouped) tableSeats.merge(s.table(), 1, Integer::sum);
        String key = level.dimension().identifier() + "@" + box.minX() + "," + box.minY() + "," + box.minZ();
        return new Tavern(key, box, stations, List.copyOf(grouped), standing(level, box, stations, grouped), stage, Map.copyOf(tableSeats), List.copyOf(stoves));
    }

    private static Spot with(Spot s, int table, List<BlockPos> fires, ServerLevel level) {
        boolean hearth = false;
        for (var f : fires) if (Math.abs(f.getX() - s.pos().getX()) <= HEARTH_REACH && Math.abs(f.getZ() - s.pos().getZ()) <= HEARTH_REACH && Math.abs(f.getY() - s.pos().getY()) <= 2) { hearth = true; break; }
        return new Spot(s.pos(), s.yaw(), s.surface(), s.kind(), table, hearth, level.canSeeSky(s.pos().above()));
    }
    private static void flood(BlockPos start, Set<BlockPos> blocks, Map<BlockPos, Integer> group, int id) {
        var queue = new ArrayDeque<BlockPos>(); queue.add(start); group.put(start, id);
        while (!queue.isEmpty()) {
            var p = queue.poll();
            for (var d : Direction.Plane.HORIZONTAL) {
                var n = p.relative(d);
                if (blocks.contains(n) && !group.containsKey(n)) { group.put(n, id); queue.add(n); }
            }
        }
    }
    private static void collectCounter(BlockGetter level, BlockPos start, Set<BlockPos> out, int limit) {
        var queue = new ArrayDeque<BlockPos>(); queue.add(start); out.add(start);
        while (!queue.isEmpty() && out.size() < limit) {
            var p = queue.poll();
            for (var d : Direction.Plane.HORIZONTAL) {
                var n = p.relative(d);
                if (!out.contains(n) && counter(level, n)) { out.add(n); queue.add(n); }
            }
        }
    }

    // -- what counts as a seat or a table ----------------------------------------------------------

    /** A seat at {@code pos}, with its own facing and surface; its table and surroundings come later. */
    public static Spot seatAt(BlockGetter level, BlockPos pos, BlockState state) {
        var block = state.getBlock();
        Kind kind = null; double surface = .5;
        if (block == TavernBlocks.CHAIR) kind = Kind.CHAIR;
        else if (block == TavernBlocks.ARMCHAIR) kind = Kind.ARMCHAIR;
        else if (block == TavernBlocks.STOOL) { kind = Kind.STOOL; surface = TavernBlocks.STOOL_SURFACE; }
        else if (block == VillageBlocks.get("village_bench") || block == VillageBlocks.get("campfire_bench")) { kind = Kind.BENCH; surface = 9 / 16.0; }
        if (kind != null) {
            if (!headroom(level, pos)) return null;
            var facing = state.getValue(HorizontalDirectionalBlock.FACING);
            // A stool turns to whichever counter or table is beside it.
            if (kind == Kind.STOOL) for (var d : new Direction[]{facing, facing.getClockWise(), facing.getCounterClockWise(), facing.getOpposite()})
                if (counter(level, pos.relative(d)) || table(level, pos.relative(d))) { facing = d; break; }
            return new Spot(pos.immutable(), facing.toYRot(), surface, kind, -1, false, false);
        }
        // The chairs every village building already has: a bottom stair with a table in front of it (its back is the high side).
        if (block instanceof StairBlock && state.getValue(StairBlock.HALF) == Half.BOTTOM && state.getValue(StairBlock.SHAPE) == StairsShape.STRAIGHT
                && !state.getValue(StairBlock.WATERLOGGED)) {
            var front = state.getValue(StairBlock.FACING).getOpposite();
            if (table(level, pos.relative(front)) && headroom(level, pos)) return new Spot(pos.immutable(), front.toYRot(), .5, Kind.CHAIR, -1, false, false);
        }
        return null;
    }
    public static boolean seat(BlockGetter level, BlockPos pos) { return seatAt(level, pos, level.getBlockState(pos)) != null || sittable(level.getBlockState(pos)); }
    /** Furniture anyone can sit on, table or not. */
    public static boolean sittable(BlockState state) {
        var block = state.getBlock();
        return block == TavernBlocks.CHAIR || block == TavernBlocks.ARMCHAIR || block == TavernBlocks.STOOL
                || block == VillageBlocks.get("village_bench") || block == VillageBlocks.get("campfire_bench");
    }
    public static double surface(BlockState state) {
        var block = state.getBlock();
        if (block == TavernBlocks.STOOL) return TavernBlocks.STOOL_SURFACE;
        if (block == VillageBlocks.get("village_bench") || block == VillageBlocks.get("campfire_bench")) return 9 / 16.0;
        return .5;
    }
    private static boolean headroom(BlockGetter level, BlockPos pos) {
        var above = pos.above();
        return level.getBlockState(above).getCollisionShape(level, above).isEmpty();
    }
    /** A Tavern Table, or a fence topped with a pressure plate or carpet. */
    public static boolean table(BlockGetter level, BlockPos pos) {
        var state = level.getBlockState(pos);
        if (state.getBlock() == TavernBlocks.TABLE) return true;
        if (!state.is(BlockTags.FENCES)) return false;
        var top = level.getBlockState(pos.above());
        return top.is(BlockTags.PRESSURE_PLATES) || top.is(BlockTags.WOOL_CARPETS);
    }
    /** How high above its block a table's top is, for setting dishes on it. */
    public static double tableTop(BlockGetter level, BlockPos pos) {
        var state = level.getBlockState(pos);
        if (state.getBlock() == TavernBlocks.TABLE) return TavernBlocks.TABLE_TOP;
        var above = level.getBlockState(pos.above());
        if (state.is(BlockTags.FENCES) && (above.is(BlockTags.PRESSURE_PLATES) || above.is(BlockTags.WOOL_CARPETS))) return 1 + 1 / 16.0;
        var shape = state.getCollisionShape(level, pos);
        if (shape.isEmpty()) return -1;
        double top = shape.max(Direction.Axis.Y);
        // A counter with a slab or trapdoor laid on it.
        var aboveShape = above.getCollisionShape(level, pos.above());
        if (top >= 1 && !aboveShape.isEmpty() && aboveShape.max(Direction.Axis.Y) <= .55) top = 1 + aboveShape.max(Direction.Axis.Y);
        return top;
    }
    /** Something to lean on: solid to about waist height with open space (or a slab) above it, like a bar or a counter. */
    public static boolean counter(BlockGetter level, BlockPos pos) {
        var state = level.getBlockState(pos);
        if (state.getBlock() instanceof DoorBlock || state.getBlock() == TavernBlocks.TABLE) return state.getBlock() == TavernBlocks.TABLE;
        var shape = state.getCollisionShape(level, pos);
        if (shape.isEmpty() || shape.max(Direction.Axis.Y) < .8 || sittable(state) || state.getBlock() instanceof StairBlock) return false;
        var above = level.getBlockState(pos.above()).getCollisionShape(level, pos.above());
        return above.isEmpty() || above.max(Direction.Axis.Y) <= .55;
    }

    // -- the building --------------------------------------------------------------------------------

    /** The village structure piece the station stands in, or a box around it for a tavern players built. */
    static BoundingBox building(ServerLevel level, BlockPos station) {
        try {
            var start = level.structureManager().getStructureWithPieceAt(station, holder -> true);
            if (start != null && start.isValid()) {
                BoundingBox best = null;
                for (var piece : start.getPieces()) {
                    var b = piece.getBoundingBox();
                    if (!b.isInside(station)) continue;
                    if (piece instanceof PoolElementStructurePiece pool && pool.getElement() instanceof SinglePoolElement single
                            && single.getTemplateLocation().getPath().contains("tavern")) return b;
                    if (best == null || b.getXSpan() * b.getZSpan() < best.getXSpan() * best.getZSpan()) best = b;
                }
                if (best != null && best.getXSpan() <= 40 && best.getZSpan() <= 40) return best;
            }
        } catch (RuntimeException ignored) {
            // Structure references point at chunks that aren't loaded yet; the fallback box is good enough.
        }
        return new BoundingBox(station.getX() - FALLBACK_REACH, station.getY() - 3, station.getZ() - FALLBACK_REACH,
                station.getX() + FALLBACK_REACH, station.getY() + 4, station.getZ() + FALLBACK_REACH);
    }

    /** Room at the bar: free floor beside a counter near the keeper's station, a little apart from each other. */
    private static List<Stand> standing(ServerLevel level, BoundingBox box, List<BlockPos> stations, List<Spot> seats) {
        var taken = new HashSet<BlockPos>();
        for (var s : seats) taken.add(s.pos());
        var found = new ArrayList<Stand>();
        var origin = stations.getFirst();
        int y0 = origin.getY() - 1, y1 = origin.getY() + 1;
        var cells = new ArrayList<BlockPos>();
        for (var p : BlockPos.betweenClosed(Math.max(box.minX(), origin.getX() - 7), y0, Math.max(box.minZ(), origin.getZ() - 7),
                Math.min(box.maxX(), origin.getX() + 7), y1, Math.min(box.maxZ(), origin.getZ() + 7))) cells.add(p.immutable());
        cells.sort(Comparator.comparingDouble(p -> p.distSqr(origin)));
        for (var p : cells) {
            if (found.size() >= 10) break;
            if (taken.contains(p) || !floor(level, p) || level.canSeeSky(p)) continue;
            Direction lean = null;
            for (var d : Direction.Plane.HORIZONTAL) if (counter(level, p.relative(d)) && !stations.contains(p.relative(d))) { lean = d; break; }
            if (lean == null) continue;
            boolean apart = true;
            for (var s : found) if (s.pos().distSqr(p) < 2.1) { apart = false; break; }
            if (apart) found.add(new Stand(p, lean.toYRot()));
        }
        return List.copyOf(found);
    }
    /** Somewhere a resident can stand: open at feet and head, a solid floor, and not a doorway. */
    static boolean floor(BlockGetter level, BlockPos p) {
        var at = level.getBlockState(p);
        if (!at.getCollisionShape(level, p).isEmpty() || at.getBlock() instanceof DoorBlock) return false;
        if (!level.getBlockState(p.above()).getCollisionShape(level, p.above()).isEmpty()) return false;
        var below = p.below();
        return level.getBlockState(below).isFaceSturdy(level, below, Direction.UP);
    }

    private TavernSurvey() {}
}
