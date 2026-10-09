package dev.villagefriends.hearth;

import java.util.Locale;

/**
 * The three kitchen stations. Each has six ingredient slots and an output; the pot also takes the bowl or
 * bottle the dish is served in and needs a lit fire under it, the oven burns fuel, and the prep table needs
 * neither.
 */
public enum Station {
    POT("cooking_pot"), OVEN("clay_oven"), PREP("prep_table");

    public static final int GRID = 6;
    /** The block's registry path. */
    public final String block;
    Station(String block) { this.block = block; }

    public String id() { return name().toLowerCase(Locale.ROOT); }
    /** Whether the station has a seventh slot below the grid: the pot's vessel, the oven's fuel. */
    public boolean extraSlot() { return this != PREP; }
    /** Slots: the grid, then the extra slot if any, then the output. */
    public int slots() { return GRID + (extraSlot() ? 1 : 0) + 1; }
    public int output() { return slots() - 1; }
    public static Station byId(String id) {
        for (var s : values()) if (s.id().equals(id) || s.block.equals(id)) return s;
        throw new IllegalArgumentException("Unknown station " + id);
    }
}
