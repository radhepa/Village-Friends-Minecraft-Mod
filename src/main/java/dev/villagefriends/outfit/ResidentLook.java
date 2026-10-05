package dev.villagefriends.outfit;

import java.util.Objects;
import java.util.SplittableRandom;
import java.util.UUID;

/** Versioned generation seed. Palette names are stable identifiers, not numeric catalog indices. */
public record ResidentLook(int complexion, Gender gender, PaletteID palette, long seed, int version) {
    public ResidentLook(int complexion, Gender gender, PaletteID palette, long seed) { this(complexion,gender,palette,seed,4); }
    public ResidentLook {
        if (version<1 || version>4) throw new IllegalArgumentException("Unsupported outfit version");
        if (complexion < 0 || complexion > 5) throw new IllegalArgumentException("Invalid complexion");
        Objects.requireNonNull(gender, "gender"); Objects.requireNonNull(palette, "palette");
    }
    public static ResidentLook generate(UUID id) {
        Objects.requireNonNull(id, "id");
        long seed = id.getMostSignificantBits() ^ Long.rotateLeft(id.getLeastSignificantBits(), 19);
        var random = new SplittableRandom(seed);
        return new ResidentLook(random.nextInt(6), Gender.values()[random.nextInt(Gender.values().length)],
            PaletteID.values()[random.nextInt(PaletteID.values().length)], seed);
    }
    public static ResidentLook parse(String recipe) {
        if (recipe == null) return null;
        var parts = recipe.split(":", -1);
        if (parts.length != 5 || !parts[0].matches("outfit[1-4]")) return null;
        try {
            return new ResidentLook(Integer.parseInt(parts[1]), Gender.valueOf(parts[2]),
                PaletteID.valueOf(parts[3]), Long.parseLong(parts[4]), parts[0].charAt(6)-'0');
        } catch (IllegalArgumentException ignored) { return null; }
    }
    public String recipe() { return "outfit" + version + ":" + complexion + ":" + gender + ":" + palette + ":" + seed; }
    public Outfit outfit(Profession profession) { return OutfitFactory.assembleOutfit(gender,profession,palette,seed); }
}
