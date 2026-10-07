package dev.villagefriends.outfit;

import java.util.List;
import java.util.Objects;
import java.util.SplittableRandom;
import java.util.concurrent.ThreadLocalRandom;
import java.util.random.RandomGenerator;

/**
 * Pick profession -> assign template -> pick palette -> vary. Everything is drawn from the
 * resident's own gender's wardrobe (non-binary residents wear every set). Hair and hair color come
 * from the seed alone, so a resident keeps their look when they change jobs. The profession's
 * preferred template comes up often, the rest share the remainder; the bottom is sometimes swapped
 * for any compatible one, except in a locked set, which is always worn whole.
 */
public final class OutfitFactory {
    static final int PREFERRED_TEMPLATE_PERCENT = 30, TEMPLATE_BOTTOM_PERCENT = 50;

    public static Outfit assembleOutfit(Gender gender, Profession job, PaletteID palette) {
        return assembleOutfit(gender, job, palette, ThreadLocalRandom.current().nextLong());
    }
    public static Outfit assembleOutfit(Gender gender, Profession job, PaletteID palette, long seed) {
        Objects.requireNonNull(gender, "gender"); Objects.requireNonNull(job, "profession");
        var active = MasterPalettes.get(palette);
        var identity = new SplittableRandom(seed);
        var hair = pick(Wardrobe.hair(gender), identity);
        var hairColor = pick(Wardrobe.HAIR_COLORS, identity);
        // Job-dependent choices use their own stream: changing jobs never rerolls identity.
        var work = new SplittableRandom(seed ^ 0x6A09E667F3BCC909L);
        var templates = Wardrobe.templates(job, gender);
        var template = templates.size() == 1 || work.nextInt(100) < PREFERRED_TEMPLATE_PERCENT ? templates.getFirst()
            : templates.get(1 + work.nextInt(templates.size() - 1));
        boolean keep = work.nextInt(100) < TEMPLATE_BOTTOM_PERCENT || template.locked();
        var bottom = keep ? template.bottom() : pick(Wardrobe.bottomsFor(template.top(), gender), work);
        return new Outfit(gender, job, active, hair, hairColor, template.top(), bottom, template);
    }
    private static <T> T pick(List<T> values, RandomGenerator random) {
        if (values.isEmpty()) throw new IllegalStateException("No wardrobe candidates");
        return values.get(random.nextInt(values.size()));
    }
    private OutfitFactory() {}
}
