package dev.villagefriends.outfit;

import java.util.List;
import java.util.Objects;
import java.util.SplittableRandom;
import java.util.concurrent.ThreadLocalRandom;
import java.util.random.RandomGenerator;

/**
 * Pick profession -> assign template -> pick palette -> vary. Hair and hair color come from the
 * seed alone, so a resident keeps their look when they change jobs. The profession's preferred
 * template wins most of the time; the bottom is sometimes swapped for any compatible one.
 */
public final class OutfitFactory {
    static final int PREFERRED_TEMPLATE_PERCENT = 70, TEMPLATE_BOTTOM_PERCENT = 60;

    public static Outfit assembleOutfit(Gender gender, Profession job, PaletteID palette) {
        return assembleOutfit(gender, job, palette, ThreadLocalRandom.current().nextLong());
    }
    public static Outfit assembleOutfit(Gender gender, Profession job, PaletteID palette, long seed) {
        Objects.requireNonNull(gender, "gender"); Objects.requireNonNull(job, "profession");
        var active = MasterPalettes.get(palette);
        var identity = new SplittableRandom(seed);
        var hair = pick(Wardrobe.HAIR, identity);
        var hairColor = pick(Wardrobe.HAIR_COLORS, identity);
        // Job-dependent choices use their own stream: changing jobs never rerolls identity.
        var work = new SplittableRandom(seed ^ 0x6A09E667F3BCC909L);
        var templates = Wardrobe.templates(job);
        var template = templates.size() == 1 || work.nextInt(100) < PREFERRED_TEMPLATE_PERCENT ? templates.getFirst()
            : templates.get(1 + work.nextInt(templates.size() - 1));
        var bottom = work.nextInt(100) < TEMPLATE_BOTTOM_PERCENT ? template.bottom() : pick(Wardrobe.bottomsFor(template.top()), work);
        return new Outfit(gender, job, active, hair, hairColor, template.top(), bottom, template);
    }
    private static <T> T pick(List<T> values, RandomGenerator random) {
        if (values.isEmpty()) throw new IllegalStateException("No wardrobe candidates");
        return values.get(random.nextInt(values.size()));
    }
    private OutfitFactory() {}
}
