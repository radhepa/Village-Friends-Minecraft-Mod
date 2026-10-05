package dev.villagefriends.outfit;

import java.util.List;
import java.util.Objects;
import java.util.SplittableRandom;
import java.util.concurrent.ThreadLocalRandom;
import java.util.random.RandomGenerator;

public final class OutfitFactory {
    public static Outfit assembleOutfit(Gender gender, Profession job, PaletteID palette) {
        return assembleOutfit(gender, job, palette, ThreadLocalRandom.current());
    }
    public static Outfit assembleOutfit(Gender gender, Profession job, PaletteID palette, long seed) {
        return assembleOutfit(gender, job, palette, new SplittableRandom(seed));
    }
    public static Outfit assembleOutfit(Gender gender, Profession job, PaletteID palette, RandomGenerator random) {
        Objects.requireNonNull(gender, "gender"); Objects.requireNonNull(job, "profession");
        Objects.requireNonNull(random, "random");
        var active = MasterPalettes.get(palette);
        // Hair is selected first so job-dependent garment choices cannot reroll identity.
        var hair = pick(OutfitCatalog.hair(gender).stream().filter(h -> h.genders().contains(gender)).toList(), random);
        int hairRgb = pick(OutfitCatalog.HAIR_COLORS, random);
        // Choose the profession's silhouette family, then vary construction within it.
        var tops = OutfitCatalog.tops(gender).stream().filter(t -> t.genders().contains(gender)
            && t.style() == job.preferredStyle()).toList();
        var top = pick(tops, random);
        var bottoms = OutfitCatalog.bottoms(gender).stream().filter(b -> b.genders().contains(gender)
            && b.compatibleStyles().contains(top.style())).toList();
        return new Outfit(gender, job, active, hair, hairRgb, top, pick(bottoms, random));
    }
    private static <T> T pick(List<T> values, RandomGenerator random) {
        if (values.isEmpty()) throw new IllegalStateException("No compatible wardrobe candidates");
        return values.get(random.nextInt(values.size()));
    }
    private OutfitFactory() {}
}
