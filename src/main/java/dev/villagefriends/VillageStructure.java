package dev.villagefriends;

import com.mojang.serialization.Codec;
import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Holder;
import net.minecraft.core.QuartPos;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.Identifier;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.structure.BoundingBox;
import net.minecraft.world.level.levelgen.structure.PoolElementStructurePiece;
import net.minecraft.world.level.levelgen.structure.Structure;
import net.minecraft.world.level.levelgen.structure.StructurePiece;
import net.minecraft.world.level.levelgen.structure.StructureType;
import net.minecraft.world.level.levelgen.structure.pools.JigsawPlacement;
import net.minecraft.world.level.levelgen.structure.pools.SinglePoolElement;
import net.minecraft.world.level.levelgen.structure.pools.StructureTemplatePool;
import net.minecraft.world.level.levelgen.structure.pools.alias.PoolAliasLookup;
import net.minecraft.world.level.levelgen.structure.structures.JigsawStructure;

/**
 * A jigsaw village that chooses its ground before it grows.
 *
 * <p>Vanilla jigsaw villages start wherever their placement lands and sit the whole
 * town square on one column of terrain, so they climb hillsides, hang off cliffs and
 * spill onto beaches. This structure first surveys the raw terrain around the start:
 * it rejects steep ground, water and land that is mostly another biome, then sets the
 * square at the median height of its footprint. After assembly it prunes lots that
 * would sit buried in a slope, hang over a drop, stand in water or be painted over by a
 * street. Civic buildings and anything with children are always kept.
 */
public final class VillageStructure extends Structure {
    /** Start-site survey: a square grid of samples {@code step} apart out to {@code radius}. */
    public record Terrain(int radius, int step, int coreRadius, int maxHeightRange, float maxWater, float maxCoreWater, float minBiome) {
        public static final Terrain DEFAULT = new Terrain(64, 16, 32, 14, 0.2f, 0.25f, 0.4f);
        public static final Codec<Terrain> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.intRange(8, 128).optionalFieldOf("radius", DEFAULT.radius).forGetter(Terrain::radius),
            Codec.intRange(4, 64).optionalFieldOf("step", DEFAULT.step).forGetter(Terrain::step),
            Codec.intRange(8, 128).optionalFieldOf("core_radius", DEFAULT.coreRadius).forGetter(Terrain::coreRadius),
            Codec.intRange(1, 384).optionalFieldOf("max_height_range", DEFAULT.maxHeightRange).forGetter(Terrain::maxHeightRange),
            Codec.floatRange(0, 1).optionalFieldOf("max_water", DEFAULT.maxWater).forGetter(Terrain::maxWater),
            Codec.floatRange(0, 1).optionalFieldOf("max_core_water", DEFAULT.maxCoreWater).forGetter(Terrain::maxCoreWater),
            Codec.floatRange(0, 1).optionalFieldOf("min_biome", DEFAULT.minBiome).forGetter(Terrain::minBiome)
        ).apply(i, Terrain::new));
    }

    /** Lot pruning: a lot is dropped when more than {@code tolerance} of its samples break a limit. */
    public record Prune(int maxBuried, int maxFloating, float tolerance, List<Identifier> keep) {
        public static final Prune DEFAULT = new Prune(5, 5, 0.25f, List.of());
        public static final Codec<Prune> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.intRange(0, 64).optionalFieldOf("max_buried", DEFAULT.maxBuried).forGetter(Prune::maxBuried),
            Codec.intRange(0, 64).optionalFieldOf("max_floating", DEFAULT.maxFloating).forGetter(Prune::maxFloating),
            Codec.floatRange(0, 1).optionalFieldOf("tolerance", DEFAULT.tolerance).forGetter(Prune::tolerance),
            Identifier.CODEC.listOf().optionalFieldOf("keep", List.of()).forGetter(Prune::keep)
        ).apply(i, Prune::new));
    }

    public static final MapCodec<VillageStructure> CODEC = RecordCodecBuilder.mapCodec(i -> i.group(
        settingsCodec(i),
        StructureTemplatePool.CODEC.fieldOf("start_pool").forGetter(s -> s.startPool),
        Identifier.CODEC.fieldOf("start_jigsaw_name").forGetter(s -> s.startJigsaw),
        Codec.intRange(0, 20).fieldOf("size").forGetter(s -> s.size),
        JigsawStructure.MaxDistance.CODEC.fieldOf("max_distance_from_center").forGetter(s -> s.maxDistance),
        Terrain.CODEC.optionalFieldOf("terrain", Terrain.DEFAULT).forGetter(s -> s.terrain),
        Prune.CODEC.optionalFieldOf("prune", Prune.DEFAULT).forGetter(s -> s.prune)
    ).apply(i, VillageStructure::new));
    public static final StructureType<VillageStructure> TYPE = () -> CODEC;

    /** Why sites were turned down, for the development survey. */
    public static final java.util.Map<String, java.util.concurrent.atomic.AtomicInteger> VERDICTS = new java.util.concurrent.ConcurrentHashMap<>();

    private static Optional<Integer> verdict(String reason, Optional<Integer> result) {
        VERDICTS.computeIfAbsent(reason, k -> new java.util.concurrent.atomic.AtomicInteger()).incrementAndGet();
        return result;
    }

    private final Holder<StructureTemplatePool> startPool;
    private final Identifier startJigsaw;
    private final int size;
    private final JigsawStructure.MaxDistance maxDistance;
    private final Terrain terrain;
    private final Prune prune;

    public VillageStructure(StructureSettings settings, Holder<StructureTemplatePool> startPool, Identifier startJigsaw, int size,
                            JigsawStructure.MaxDistance maxDistance, Terrain terrain, Prune prune) {
        super(settings);
        this.startPool = startPool;
        this.startJigsaw = startJigsaw;
        this.size = size;
        this.maxDistance = maxDistance;
        this.terrain = terrain;
        this.prune = prune;
    }

    public static void register() {
        Registry.register(BuiltInRegistries.STRUCTURE_TYPE, VillageBlocks.id("village"), TYPE);
    }

    @Override public StructureType<?> type() { return TYPE; }

    private static int surface(GenerationContext c, int x, int z) {
        return c.chunkGenerator().getFirstOccupiedHeight(x, z, Heightmap.Types.WORLD_SURFACE_WG, c.heightAccessor(), c.randomState());
    }

    private static int floor(GenerationContext c, int x, int z) {
        return c.chunkGenerator().getFirstOccupiedHeight(x, z, Heightmap.Types.OCEAN_FLOOR_WG, c.heightAccessor(), c.randomState());
    }

    /** The square's ground height, or empty when the site is too steep, wet or foreign. */
    private Optional<Integer> survey(GenerationContext c, int cx, int cz) {
        // Vanilla only checks the biome at the start; do that first so foreign sites stay cheap.
        int centre = surface(c, cx, cz);
        if (!biomeAt(c, cx, centre, cz)) return verdict("foreign start", Optional.empty());
        int samples = 0, water = 0, biome = 0, core = 0, coreWater = 0, low = Integer.MAX_VALUE, high = Integer.MIN_VALUE;
        var square = new ArrayList<Integer>();
        int r = terrain.radius(), step = terrain.step();
        for (int dx = -r; dx <= r; dx += step) for (int dz = -r; dz <= r; dz += step) {
            int x = cx + dx, z = cz + dz;
            int top = surface(c, x, z);
            boolean wet = top > floor(c, x, z);
            samples++;
            if (wet) water++;
            int distance = Math.max(Math.abs(dx), Math.abs(dz));
            if (distance <= terrain.coreRadius()) {
                // The square itself must be dry; a river past the civic ring gets bridges.
                if (wet && distance <= 16) return verdict("square water", Optional.empty());
                core++;
                if (wet) { coreWater++; continue; }
                low = Math.min(low, top);
                high = Math.max(high, top);
                if (distance <= 16) square.add(top);
            }
            if (biomeAt(c, x, top, z)) biome++;
        }
        if (coreWater > core * terrain.maxCoreWater()) return verdict("core water", Optional.empty());
        if (biome < samples * terrain.minBiome()) return verdict("biome " + biome * 10 / samples * 10 + "%", Optional.empty());
        if (high - low > terrain.maxHeightRange()) return verdict("slope " + Math.min(high - low, 40) / 4 * 4, Optional.empty());
        if (water > samples * terrain.maxWater()) return verdict("water", Optional.empty());
        int[] heights = square.stream().mapToInt(Integer::intValue).sorted().toArray();
        return verdict("accepted", Optional.of(heights[heights.length / 2]));
    }

    private static boolean biomeAt(GenerationContext c, int x, int y, int z) {
        return c.validBiome().test(c.biomeResolver().getNoiseBiome(QuartPos.fromBlock(x), QuartPos.fromBlock(y), QuartPos.fromBlock(z)));
    }

    @Override
    protected Optional<GenerationStub> findGenerationPoint(GenerationContext context) {
        int cx = context.chunkPos().getMinBlockX(), cz = context.chunkPos().getMinBlockZ();
        var ground = survey(context, cx, cz);
        if (ground.isEmpty()) return Optional.empty();
        // Without a heightmap projection JigsawPlacement lowers the start piece by its
        // anchor height plus one, so the square's ground layer lands on {@code ground}.
        var start = new BlockPos(cx, ground.get() + 2, cz);
        return JigsawPlacement.addPieces(context, startPool, Optional.of(startJigsaw), size, start, false, Optional.empty(), maxDistance,
                PoolAliasLookup.EMPTY, JigsawStructure.DEFAULT_DIMENSION_PADDING, JigsawStructure.DEFAULT_LIQUID_SETTINGS)
            .map(stub -> new GenerationStub(stub.position(), builder -> {
                var pieces = stub.getPiecesBuilder().build().pieces();
                for (var piece : kept(context, pieces)) builder.addPiece(piece);
            }));
    }

    private List<StructurePiece> kept(GenerationContext c, List<StructurePiece> pieces) {
        var streets = new ArrayList<BoundingBox>();
        for (var piece : pieces)
            if (piece instanceof PoolElementStructurePiece p && p.getElement().getProjection() == StructureTemplatePool.Projection.TERRAIN_MATCHING)
                streets.add(p.getBoundingBox());
        var out = new ArrayList<StructurePiece>(pieces.size());
        for (int i = 0; i < pieces.size(); i++) {
            var piece = pieces.get(i);
            if (i == 0 || !(piece instanceof PoolElementStructurePiece p) || !prunable(p) || fits(c, p.getBoundingBox(), streets)) out.add(piece);
        }
        return out;
    }

    /** Only rigid leaves (lots with nothing attached to them) outside the keep list may go. */
    private boolean prunable(PoolElementStructurePiece p) {
        if (p.getElement().getProjection() != StructureTemplatePool.Projection.RIGID || p.getJunctions().size() > 1) return false;
        return !(p.getElement() instanceof SinglePoolElement single) || !prune.keep().contains(single.getTemplateLocation());
    }

    private boolean fits(GenerationContext c, BoundingBox box, List<BoundingBox> streets) {
        for (var street : streets)
            if (street.minX() <= box.maxX() - 1 && street.maxX() >= box.minX() + 1 && street.minZ() <= box.maxZ() - 1 && street.maxZ() >= box.minZ() + 1)
                return false;
        int ground = box.minY(), samples = 0, bad = 0;
        int[] xs = axis(box.minX(), box.maxX()), zs = axis(box.minZ(), box.maxZ());
        for (int x : xs) for (int z : zs) {
            int top = surface(c, x, z);
            samples++;
            if (top - ground > prune.maxBuried() || ground - top > prune.maxFloating() || top > floor(c, x, z)) bad++;
        }
        return bad <= samples * prune.tolerance();
    }

    private static int[] axis(int min, int max) {
        int span = max - min, n = Math.max(2, Math.min(5, span / 4 + 1));
        int[] values = new int[n];
        for (int i = 0; i < n; i++) values[i] = min + 1 + (span - 2) * i / (n - 1);
        return Arrays.stream(values).distinct().toArray();
    }
}
