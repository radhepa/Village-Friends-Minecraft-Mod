package dev.villagefriends.stable.gear;

import dev.villagefriends.stable.data.StableTable;

/**
 * How many pack columns (three slots each) a horse, donkey or mule has. Pure: the answer depends only on the
 * animal's kind, its chest and the tack in its SADDLE slot.
 *
 * <p>Never on breed or bond, on purpose. The pack is sized while the animal loads ({@code readAdditionalSaveData}),
 * and Fabric may read attachments after that, so a count that read the breed could size the container wrong at
 * load and silently lose the items saved in it.
 */
public final class PackCapacity {
    /** The vanilla mount screen fits five columns: its grid starts at x = 79, and 79 + 5 x 18 fits the 176 px background. */
    public static final int MAX_COLUMNS = 5;
    /** Saddlebags are two bags behind a riding saddle, not a pack frame: a horse carries at most three columns. */
    public static final int HORSE_COLUMNS = 3;
    /** What a chest gives a donkey or a mule (vanilla's own count). */
    public static final int CHEST_COLUMNS = 5;
    /** Returned for animals this does not decide (llamas, camels, undead horses): keep vanilla's count. */
    public static final int KEEP = -1;

    /**
     * Pack columns for an animal ("horse", "donkey" or "mule"; anything else gives {@link #KEEP}). A donkey or mule
     * takes the bigger of its chest and its tack, so a pack saddle on a chested donkey adds nothing and loses nothing.
     */
    public static int columns(String animal, boolean chest, int tackColumns) {
        int tack = Math.max(0, tackColumns);
        return switch (animal == null ? "" : animal) {
            case "horse" -> Math.min(HORSE_COLUMNS, tack);
            case "donkey", "mule" -> Math.min(MAX_COLUMNS, Math.max(chest ? CHEST_COLUMNS : 0, tack));
            default -> KEEP;
        };
    }

    /** The columns a gear row gives this animal: its {@code columns} when it is tack the animal may wear, else 0. */
    public static int tackColumns(StableTable.Gear gear, String animal) {
        return gear != null && gear.tack() && gear.animals().contains(animal) ? Math.max(0, gear.columns()) : 0;
    }

    /** Slots in that many columns (three rows each). */
    public static int slots(int columns) { return Math.max(0, columns) * 3; }

    private PackCapacity() {}
}
