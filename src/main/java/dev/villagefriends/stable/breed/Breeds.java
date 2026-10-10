package dev.villagefriends.stable.breed;

import static dev.villagefriends.VillageFriends.target;

import dev.villagefriends.stable.data.HorseBreed;
import dev.villagefriends.stable.data.StableData;
import dev.villagefriends.stable.data.StableTable;
import dev.villagefriends.stable.data.StableTags;
import dev.villagefriends.stable.mixin.HorseAccessor;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Set;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.function.Predicate;
import java.util.random.RandomGenerator;
import net.fabricmc.fabric.api.biome.v1.BiomeModifications;
import net.fabricmc.fabric.api.biome.v1.BiomeSelectionContext;
import net.fabricmc.fabric.api.biome.v1.BiomeSelectors;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Holder;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.BiomeTags;
import net.minecraft.tags.BlockTags;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.entity.SpawnGroupData;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.animal.Animal;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.entity.animal.equine.Horse;
import net.minecraft.world.entity.animal.equine.Markings;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.biome.Biomes;
import net.minecraft.world.level.chunk.LevelChunk;
import net.minecraft.world.level.gamerules.GameRules;
import net.minecraft.world.level.levelgen.Heightmap;

/**
 * Breeds in the world: which breed a horse is when it first loads (by its biome), what a breed does to a horse
 * (stats, markings, coat), foals, and the extra biome spawns. The rules themselves are pure ({@link BreedPicker},
 * {@link BreedRolls}, {@link Inheritance}); this class only reads and writes horses. Breeds belong to plain
 * {@link Horse}s: donkeys, mules (a horse x donkey foal too), camels and undead horses have none.
 */
public final class Breeds {
    private Breeds() {}

    // -- picking ---------------------------------------------------------------------------------------------

    /** The keywords of a biome that breed rows are picked by (see {@code tools/stablehand/breeds.py}); always has "any". */
    public static Set<String> keywords(Holder<Biome> biome) {
        var out = new HashSet<String>();
        out.add(BreedPicker.ANY);
        String path = biome.unwrapKey().map(k -> k.identifier().getPath()).orElse("");
        if (path.contains("plains") && !path.contains("snowy")) out.add("plains");
        if (biome.is(Biomes.MEADOW)) out.add("meadow");
        if (biome.is(BiomeTags.IS_FOREST)) out.add("forest");
        if (biome.is(BiomeTags.IS_SAVANNA)) out.add("savanna");
        if (biome.is(Biomes.DESERT)) out.add("desert");
        if (biome.is(BiomeTags.IS_BADLANDS)) out.add("badlands");
        if (biome.is(BiomeTags.IS_TAIGA)) out.add("taiga");
        if (biome.is(BiomeTags.SPAWNS_COLD_VARIANT_FARM_ANIMALS)) out.add("snowy");
        if (path.startsWith("windswept")) out.add("windswept");
        return out;
    }

    /** The breed a horse found at {@code pos} would be. */
    public static String pick(ServerLevel level, BlockPos pos, RandomSource random) {
        return BreedPicker.pick(keywords(level.getBiome(pos)), StableTable.breeds(), generator(random));
    }

    /** A breed's name for players ("Draft Horse"), from its row; the id itself for an unknown breed. */
    public static String name(String id) {
        return StableTable.breed(id).map(b -> b.raw().has("name") ? b.raw().get("name").getAsString() : id).orElse(id);
    }

    // -- making a horse a breed ----------------------------------------------------------------------------

    /**
     * Makes a horse this breed: rolls its health, speed and jump from the breed's ranges as base values (vanilla saves
     * those, so nothing more is needed on reload), heals it to full, gives it one of the breed's markings and a coat.
     * An unknown breed id leaves the horse as it is.
     */
    public static void assign(Horse horse, String breed, RandomSource random) {
        var row = StableTable.breed(breed).orElse(null);
        if (row == null) return;
        var rng = generator(random);
        apply(horse, BreedRolls.roll(row, rng));
        horse.setHealth(horse.getMaxHealth());
        mark(horse, row, rng);
        target(horse).setAttached(StableData.BREED, new HorseBreed(row.id(), rng.nextInt(Math.max(1, row.coats()))));
    }

    /** A horse that loads without a breed gets its biome's (natural spawns, spawn eggs, /summon, horses in old worlds). */
    static void loaded(Entity entity, ServerLevel level) {
        if (entity instanceof Horse horse && !target(horse).hasAttached(StableData.BREED) && !horse.entityTags().contains(StableTags.STABLE_HORSE))
            assign(horse, pick(level, horse.blockPosition(), horse.getRandom()), horse.getRandom());
    }

    /**
     * Two horses had a foal (called before the foal joins the world, after vanilla mixed the parents' stats): the foal
     * takes one parent's breed and a blend of both parents' stats inside that breed's range (see {@link Inheritance}).
     * A parent that never got a breed counts as its biome's pick. Its markings are kept when the breed allows them.
     */
    public static void bred(Animal parent, ServerLevel level, Animal partner, AgeableMob child) {
        if (!(parent instanceof Horse a) || !(partner instanceof Horse b) || !(child instanceof Horse foal) || StableTable.breeds().isEmpty()) return;
        var rng = generator(level.getRandom());
        var rowA = row(a, level, rng);
        var rowB = row(b, level, rng);
        var f = Inheritance.foal(rowA, stats(a), coat(a), rowB, stats(b), coat(b), rng);
        apply(foal, f.stats());
        foal.setHealth(foal.getMaxHealth());
        var row = f.breed().equals(rowA.id()) ? rowA : rowB;
        if (!row.markings().contains(foal.getMarkings().name().toLowerCase(Locale.ROOT))) mark(foal, row, rng);
        target(foal).setAttached(StableData.BREED, new HorseBreed(f.breed(), f.coat()));
    }

    private static StableTable.Breed row(Horse horse, ServerLevel level, RandomGenerator rng) {
        var own = target(horse).getAttached(StableData.BREED);
        if (own != null) { var row = StableTable.breed(own.breed()); if (row.isPresent()) return row.get(); }
        String picked = BreedPicker.pick(keywords(level.getBiome(horse.blockPosition())), StableTable.breeds(), rng);
        return StableTable.breed(picked).orElse(StableTable.breeds().getFirst());
    }
    private static int coat(Horse horse) {
        var own = target(horse).getAttached(StableData.BREED);
        return own == null ? 0 : own.coat();
    }
    /** A horse's bred stats: the base values of its health, speed and jump (bond bonuses are modifiers on top). */
    public static BreedRolls.Stats stats(AbstractHorse horse) {
        return new BreedRolls.Stats(horse.getAttributeBaseValue(Attributes.MAX_HEALTH), horse.getAttributeBaseValue(Attributes.MOVEMENT_SPEED),
                horse.getAttributeBaseValue(Attributes.JUMP_STRENGTH));
    }
    private static void apply(AbstractHorse horse, BreedRolls.Stats stats) {
        horse.getAttribute(Attributes.MAX_HEALTH).setBaseValue(stats.health());
        horse.getAttribute(Attributes.MOVEMENT_SPEED).setBaseValue(stats.speed());
        horse.getAttribute(Attributes.JUMP_STRENGTH).setBaseValue(stats.jump());
    }
    /** One of the breed's vanilla markings (drawn on top of the painted coat), keeping the horse's vanilla colour. */
    private static void mark(Horse horse, StableTable.Breed row, RandomGenerator rng) {
        if (row.markings().isEmpty()) return;
        var name = row.markings().get(rng.nextInt(row.markings().size()));
        Markings marking;
        try { marking = Markings.valueOf(name.toUpperCase(Locale.ROOT)); } catch (IllegalArgumentException e) { marking = Markings.NONE; }
        ((HorseAccessor) horse).villagefriends$setVariantAndMarkings(horse.getVariant(), marking);
    }

    /** Minecraft's random as a {@link RandomGenerator}, for the pure rules. */
    public static RandomGenerator generator(RandomSource random) {
        return new RandomGenerator() {
            @Override public long nextLong() { return random.nextLong(); }
            @Override public int nextInt(int bound) { return random.nextInt(bound); }
            @Override public double nextDouble() { return random.nextDouble(); }
            @Override public boolean nextBoolean() { return random.nextBoolean(); }
        };
    }

    // -- extra biome spawns -----------------------------------------------------------------------------------

    /** Keywords whose ground is sand or terracotta, where vanilla's grass-only animal spawn rule never places a horse. */
    private static final Set<String> SANDY = Set.of("desert", "badlands");
    /** A sandy extra spawn row of weight w puts a herd on about w in this many newly generated chunks of its biome. */
    private static final int HERD_ODDS = 120;
    /** Chunks generated since the last tick (filled from the chunk event, read on the server thread). */
    private static final ConcurrentLinkedQueue<Fresh> FRESH = new ConcurrentLinkedQueue<>();
    private record Fresh(ResourceKey<Level> dimension, int x, int z) {}
    /** The sandy extra spawn rows (filled once by {@link #spawns}). */
    private static final List<StableTable.ExtraSpawn> HERDS = new ArrayList<>();

    /**
     * Each row's {@code extra_spawns} become a natural horse spawn in biomes vanilla gives no horses (the loaded horse
     * then picks its breed from the biome, so a taiga horse is usually a fjord). Vanilla only lets animals spawn on
     * grass, which deserts and badlands hardly have, so those rows also place a small herd on the sand of some newly
     * generated chunks, the way vanilla fills a new chunk with its animals.
     */
    static void spawns() {
        for (var b : StableTable.breeds()) for (var s : b.extraSpawns()) {
            BiomeModifications.addSpawn(BiomeSelectors.foundInOverworld().and(selector(s.biome())), MobCategory.CREATURE, EntityTypes.HORSE, s.weight(), s.min(), s.max());
            if (SANDY.contains(s.biome())) HERDS.add(s);
        }
    }

    static Predicate<BiomeSelectionContext> selector(String keyword) {
        return switch (keyword) {
            case "plains" -> c -> path(c).contains("plains") && !path(c).contains("snowy");
            case "meadow" -> BiomeSelectors.includeByKey(Biomes.MEADOW);
            case "forest" -> BiomeSelectors.tag(BiomeTags.IS_FOREST);
            case "savanna" -> BiomeSelectors.tag(BiomeTags.IS_SAVANNA);
            case "desert" -> BiomeSelectors.includeByKey(Biomes.DESERT);
            case "badlands" -> BiomeSelectors.tag(BiomeTags.IS_BADLANDS);
            case "taiga" -> BiomeSelectors.tag(BiomeTags.IS_TAIGA);
            case "snowy" -> BiomeSelectors.tag(BiomeTags.SPAWNS_COLD_VARIANT_FARM_ANIMALS);
            case "windswept" -> c -> path(c).startsWith("windswept");
            default -> BiomeSelectors.all();
        };
    }
    private static String path(BiomeSelectionContext c) { return c.getBiomeKey().identifier().getPath(); }

    /** A chunk was generated: remember it, cheaply (the event may come from chunk loading code). */
    static void generated(ServerLevel level, LevelChunk chunk) {
        if (level.dimension() == Level.OVERWORLD && !HERDS.isEmpty()) FRESH.add(new Fresh(level.dimension(), chunk.getPos().getMinBlockX(), chunk.getPos().getMinBlockZ()));
    }

    /** Places the herds of the chunks generated since the last tick (at most 32 chunks a tick). */
    static void tick(MinecraftServer server) {
        for (int n = 0; n < 32 && !FRESH.isEmpty(); n++) {
            var fresh = FRESH.poll();
            var level = server.getLevel(fresh.dimension());
            if (level != null && level.getGameRules().get(GameRules.SPAWN_MOBS)) herd(level, fresh);
        }
    }

    private static void herd(ServerLevel level, Fresh fresh) {
        var random = level.getRandom();
        // Kept 3 blocks inside the chunk, so the herd (within 3 blocks of here) never reaches into an unloaded neighbour.
        int x = fresh.x() + 3 + random.nextInt(10), z = fresh.z() + 3 + random.nextInt(10);
        if (!level.hasChunkAt(new BlockPos(x, 0, z))) return;
        int y = level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, x, z);
        var keywords = keywords(level.getBiome(new BlockPos(x, y, z)));
        for (var row : HERDS) {
            if (!keywords.contains(row.biome()) || random.nextInt(HERD_ODDS) >= row.weight()) continue;
            int count = row.min() + random.nextInt(Math.max(1, row.max() - row.min() + 1));
            SpawnGroupData group = null;
            for (int tries = 0, placed = 0; tries < count * 3 && placed < count; tries++) {
                int hx = x + random.nextInt(7) - 3, hz = z + random.nextInt(7) - 3;
                var ground = new BlockPos(hx, level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, hx, hz) - 1, hz);
                var state = level.getBlockState(ground);
                if (!(state.is(BlockTags.SAND) || state.is(BlockTags.TERRACOTTA) || state.is(BlockTags.BADLANDS_TERRACOTTA)) || !level.getFluidState(ground.above()).isEmpty()) continue;
                var horse = EntityTypes.HORSE.create(level, EntitySpawnReason.CHUNK_GENERATION);
                if (horse == null) return;
                horse.snapTo(hx + .5, ground.getY() + 1, hz + .5, random.nextFloat() * 360, 0);
                if (!level.noCollision(horse)) continue;
                group = horse.finalizeSpawn(level, level.getCurrentDifficultyAt(ground), EntitySpawnReason.CHUNK_GENERATION, group);
                level.addFreshEntity(horse);
                placed++;
            }
            return;
        }
    }

    static void clear() { FRESH.clear(); }
}
