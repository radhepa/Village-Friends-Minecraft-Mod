package dev.villagefriends.outfit;

import java.util.Locale;
import java.util.Objects;

/** Vanilla jobs, the ten Village Friends jobs, and fantasy archetypes. */
public enum Profession {
    NONE, NITWIT, ARMORER, BUTCHER, CARTOGRAPHER, CLERIC, FARMER, FISHERMAN,
    FLETCHER, LEATHERWORKER, LIBRARIAN, MASON, SHEPHERD, TOOLSMITH, WEAPONSMITH,
    KNIGHT, ARCHER, COOK, TAVERN_KEEPER, APOTHECARY, PAINTER, BARD, TAILOR,
    CARPENTER, SCHOLAR, MERCHANT, ADVENTURER, GUARD, MAGE;

    public OutfitStyle preferredStyle() {
        return switch (this) {
            case NONE, NITWIT, SHEPHERD, BARD -> OutfitStyle.RELAXED;
            case CLERIC, SCHOLAR, MAGE, APOTHECARY -> OutfitStyle.ROBES;
            case MERCHANT, LIBRARIAN, TAILOR, TAVERN_KEEPER -> OutfitStyle.TAILORED;
            case CARTOGRAPHER, FLETCHER, ARCHER, KNIGHT, ADVENTURER, GUARD -> OutfitStyle.TRAVELER;
            default -> OutfitStyle.WORKWEAR;
        };
    }

    /** Unknown/modded jobs get a neutral fallback; preserve the full key upstream. */
    public static Profession fromId(String id) {
        Objects.requireNonNull(id, "profession");
        String key = id.substring(id.indexOf(':') + 1).toUpperCase(Locale.ROOT);
        try { return valueOf(key); }
        catch (IllegalArgumentException ignored) { return NONE; }
    }
}
