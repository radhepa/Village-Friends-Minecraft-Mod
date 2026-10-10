package dev.villagefriends.fishing;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import dev.villagefriends.VillageRecord;
import dev.villagefriends.VillageSettlements;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import net.fabricmc.fabric.api.attachment.v1.AttachmentRegistry;
import net.fabricmc.fabric.api.attachment.v1.AttachmentTarget;
import net.fabricmc.fabric.api.attachment.v1.AttachmentType;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.BlockTags;
import net.minecraft.tags.FluidTags;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Mirror;
import net.minecraft.world.level.block.RotatedPillarBlock;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructurePlaceSettings;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplate;

/**
 * Village docks. Once a village's surroundings are loaded, it looks along its shores (out to 16 blocks past its
 * edge) for a stretch of bank with open water in front, at least ten blocks of it; if it finds one it builds a
 * small fishing dock there in its own style ({@code villagefriends:dock/<type>}, designed in
 * {@code tools/village_design/buildings/docks.py}), drives the pilings down to the bed, and remembers where its
 * fishermen stand. A village with no good water gets none. Kept per level in {@code villagefriends:docks}.
 *
 * <p>The templates point out over the water toward +z: the land end is rows z 0–1, the deck z 2–11 at y 0, the
 * three fishing places at x 1–3 on the last row; pilings are the logs and walls at y 0.
 */
public final class Docks {
    public static final int WIDTH = 5, LENGTH = 12;

    /** A village's dock: built or not, its land end and facing, where fishers stand and where their bobbers land. */
    public record Dock(boolean built, long origin, int facing, List<Long> spots, List<Long> casts) {
        static final Codec<Dock> CODEC = RecordCodecBuilder.create(i -> i.group(
                Codec.BOOL.fieldOf("built").forGetter(Dock::built), Codec.LONG.optionalFieldOf("origin", 0L).forGetter(Dock::origin),
                Codec.INT.optionalFieldOf("facing", 0).forGetter(Dock::facing),
                Codec.LONG.listOf().optionalFieldOf("spots", List.of()).forGetter(Dock::spots),
                Codec.LONG.listOf().optionalFieldOf("casts", List.of()).forGetter(Dock::casts)).apply(i, Dock::new));
        static final Dock NONE = new Dock(false, 0, 0, List.of(), List.of());
        public Direction direction() { return Direction.from2DDataValue(facing); }
    }
    public static final AttachmentType<Map<String, Dock>> STATE = AttachmentRegistry.create(Fishing.id("docks"),
            b -> b.initializer(Map::of).persistent(Codec.unboundedMap(Codec.STRING, Dock.CODEC)));

    /** A place to build: the land end's middle at deck height, which way is out over the water, and how good it is. */
    record Site(BlockPos origin, Direction out, int waterY, double score) {}

    static void register() { ServerTickEvents.END_SERVER_TICK.register(Docks::tick); }

    private static Map<String, Dock> all(ServerLevel level) { return ((AttachmentTarget) level).getAttachedOrElse(STATE, Map.of()); }
    public static Dock dock(ServerLevel level, String village) {
        var d = all(level).get(village);
        return d == null || !d.built() ? null : d;
    }
    private static void put(ServerLevel level, String village, Dock dock) {
        var next = new HashMap<>(all(level)); next.put(village, dock);
        ((AttachmentTarget) level).setAttached(STATE, Map.copyOf(next));
    }

    private static void tick(MinecraftServer server) {
        if (server.getTickCount() % 100 != 31) return;
        for (var level : server.getAllLevels()) {
            var done = all(level);
            for (var village : VillageSettlements.book(level).villages().values()) {
                if (done.containsKey(village.id())) continue;
                if (survey(level, village)) break; // one survey a pass is plenty
            }
        }
    }

    /** Looks for a shore and builds the dock; false if the area isn't loaded yet (try again later). */
    static boolean survey(ServerLevel level, VillageRecord village) {
        int r = Math.min(village.radius() + 16, 96);
        int cx = village.x(), cz = village.z();
        for (int x = (cx - r) >> 4; x <= (cx + r) >> 4; x++)
            for (int z = (cz - r) >> 4; z <= (cz + r) >> 4; z++) if (!level.hasChunk(x, z)) return false;
        var site = find(level, new BlockPos(cx, village.y(), cz), r);
        put(level, village.id(), site == null ? Dock.NONE : build(level, site, FishingVillage.villageType(level, new BlockPos(cx, village.y(), cz))));
        return true;
    }

    /** The best dock site within {@code r} of {@code center}: closest to the centre, with deep water at the end. */
    public static Site find(ServerLevel level, BlockPos center, int r) {
        Site best = null;
        for (int x = center.getX() - r; x <= center.getX() + r; x += 2) {
            for (int z = center.getZ() - r; z <= center.getZ() + r; z += 2) {
                int top = level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, x, z) - 1;
                var ground = new BlockPos(x, top, z);
                if (!level.getFluidState(ground).isEmpty()) continue;
                for (var dir : Direction.Plane.HORIZONTAL) {
                    var w = ground.relative(dir, 2);
                    int wy = level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, w.getX(), w.getZ()) - 1;
                    if (!water(level, new BlockPos(w.getX(), wy, w.getZ())) || top < wy || top > wy + 1) continue;
                    double score = check(level, new BlockPos(x, wy + 1, z), dir, wy);
                    if (score < 0) continue;
                    score -= Math.sqrt(ground.distSqr(center)) * .5;
                    if (best == null || score > best.score()) best = new Site(new BlockPos(x, wy + 1, z), dir, wy, score);
                }
            }
        }
        return best;
    }
    private static boolean water(ServerLevel level, BlockPos p) { return level.getFluidState(p).is(FluidTags.WATER); }
    private static boolean open(ServerLevel level, BlockPos p) {
        var s = level.getBlockState(p);
        return s.isAir() || s.canBeReplaced() && s.getFluidState().isEmpty();
    }
    /** How good a site is (−1 if it won't do): solid bank under the land end, clear water under the deck, room above. */
    private static double check(ServerLevel level, BlockPos origin, Direction out, int waterY) {
        var right = out.getClockWise();
        int depth = 0;
        for (int along = 0; along < LENGTH; along++) {
            for (int across = -2; across <= 2; across++) {
                var deck = origin.relative(out, along).relative(right, across);
                if (!open(level, deck.above()) || !open(level, deck.above(2))) return -1;
                if (along < 2) {
                    var below = deck.below();
                    if (water(level, below) || water(level, deck)) return -1;
                    var s = level.getBlockState(below);
                    if (!s.isFaceSturdy(level, below, Direction.UP) && !s.canBeReplaced()) return -1;
                } else {
                    if (!water(level, deck.below()) || !open(level, deck) && !water(level, deck)) return -1;
                    if (water(level, deck)) return -1; // the water rises over the deck: not a bank at all
                }
            }
        }
        // Water past the end, and how deep it is there.
        var end = origin.relative(out, LENGTH + 2);
        if (!water(level, end.below())) return -1;
        for (int d = 1; d <= 6 && water(level, end.below(d)); d++) depth++;
        return depth * 4;
    }

    /** Builds the dock at a site; the record of where its fishers stand. */
    public static Dock build(ServerLevel level, Site site, String type) {
        var manager = level.getServer().getStructureTemplateManager();
        var template = manager.get(Fishing.id("dock/" + type)).or(() -> manager.get(Fishing.id("dock/plains"))).orElse(null);
        if (template == null) return Dock.NONE;
        var rotation = switch (site.out()) { case WEST -> Rotation.CLOCKWISE_90; case NORTH -> Rotation.CLOCKWISE_180; case EAST -> Rotation.COUNTERCLOCKWISE_90; default -> Rotation.NONE; };
        var settings = new StructurePlaceSettings().setRotation(rotation).setMirror(Mirror.NONE).setIgnoreEntities(true);
        var at = site.origin().subtract(local(2, 0, 0, rotation));
        template.placeInWorld(level, at, at, settings, level.getRandom(), Block.UPDATE_CLIENTS);
        // Drive the pilings down to the bed.
        for (int x = 0; x < WIDTH; x++) for (int z = 0; z < LENGTH; z++) {
            var top = at.offset(local(x, 0, z, rotation));
            var state = level.getBlockState(top);
            if (!state.is(BlockTags.LOGS) && !state.is(BlockTags.WALLS)) continue;
            var post = state.hasProperty(RotatedPillarBlock.AXIS) ? state.setValue(RotatedPillarBlock.AXIS, Direction.Axis.Y) : state;
            for (var p = top.below(); p.getY() > level.getMinY() && top.getY() - p.getY() <= 24; p = p.below()) {
                var here = level.getBlockState(p);
                if (!here.canBeReplaced() && !here.getFluidState().is(FluidTags.WATER) && !here.isAir()) break;
                level.setBlock(p, post, Block.UPDATE_CLIENTS);
            }
        }
        var spots = new ArrayList<Long>(); var casts = new ArrayList<Long>();
        for (int x = 1; x <= 3; x++) {
            spots.add(at.offset(local(x, 1, LENGTH - 1, rotation)).asLong());
            var cast = at.offset(local(x + (x - 2), 0, LENGTH + 2, rotation));
            casts.add(new BlockPos(cast.getX(), site.waterY(), cast.getZ()).asLong());
        }
        return new Dock(true, site.origin().asLong(), site.out().get2DDataValue(), List.copyOf(spots), List.copyOf(casts));
    }
    private static BlockPos local(int x, int y, int z, Rotation rotation) { return StructureTemplate.transform(new BlockPos(x, y, z), Mirror.NONE, rotation, BlockPos.ZERO); }

    /** For {@code /fishing dock build}: a dock at the best shore near {@code pos}, for the village there if any. */
    public static Dock buildNear(ServerLevel level, BlockPos pos) {
        var site = find(level, pos, 32);
        if (site == null) return null;
        var village = VillageSettlements.book(level).at(pos);
        var dock = build(level, site, FishingVillage.villageType(level, pos));
        if (village != null && dock.built()) put(level, village.id(), dock);
        return dock;
    }
    static BlockState air() { return net.minecraft.world.level.block.Blocks.AIR.defaultBlockState(); }

    private Docks() {}
}
