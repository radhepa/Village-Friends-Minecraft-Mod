package dev.villagefriends.stable.gear;

import dev.villagefriends.stable.data.StableTable;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/**
 * The plain-words tooltip lines for gear and the lance, built from the same rows the game uses (so a number tuned
 * in {@code tools/stablehand/gear.py} shows up in the tooltip by itself). Pure; the client adds them under the name.
 */
public final class GearText {
    /** What a gear row does, one short line each. Barding's armor numbers are left to vanilla's own lines. */
    public static List<String> lines(StableTable.Gear g) {
        var out = new ArrayList<String>();
        if (g.tack()) {
            int columns = 0;
            for (var animal : g.animals()) columns = Math.max(columns, Math.max(0, PackCapacity.columns(animal, false, PackCapacity.tackColumns(g, animal))));
            out.add("Counts as a saddle: ride and steer with it");
            if (columns > 0) out.add(PackCapacity.slots(columns) + " pack slots" + (g.animals().contains("horse") ? "" : ", no chest needed"));
            if (g.bondRide() > 1) out.add("Bond grows " + number(g.bondRide()) + "x faster while riding");
            if (g.calm() > 0) out.add("Keeps the animal calmer near monsters");
        }
        if (g.dyeable()) out.add("Dye it like leather armor; a cauldron washes it");
        out.add("For " + animals(g.animals()));
        return out;
    }

    /** How the couched lance works, with its real threshold. */
    public static List<String> lance(StableTable.Lance l) {
        return List.of("Hold use while galloping to couch it",
                "Lands only above " + number(l.damageThreshold()) + " blocks a second",
                "The faster the horse, the harder the hit");
    }

    /** "horses", "donkeys and mules", "horses, donkeys and mules". */
    static String animals(List<String> animals) {
        var names = animals.stream().map(a -> a + "s").toList();
        if (names.isEmpty()) return "nothing";
        if (names.size() == 1) return names.getFirst();
        return String.join(", ", names.subList(0, names.size() - 1)) + " and " + names.getLast();
    }

    /** 1.5 stays 1.5, 2.0 becomes 2. */
    static String number(double v) {
        return v == Math.rint(v) ? Long.toString((long) v) : String.format(Locale.ROOT, "%.1f", v);
    }

    private GearText() {}
}
