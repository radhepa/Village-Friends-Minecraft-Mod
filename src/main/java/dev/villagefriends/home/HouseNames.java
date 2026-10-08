package dev.villagefriends.home;

import dev.villagefriends.social.Townsfolk;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import java.util.function.Function;

/**
 * What a house is called: the name a player gave its plaque; "The Ashford House" after the family who
 * lives there; what it is for ("The Garrison", "The Apothecary's Rooms", "Guest rooms at the tavern");
 * or, for an empty house, what it looks like ("Oak Cottage"). Pure.
 */
public final class HouseNames {
    /** Building words that read better last: "cottage_oak" is an "Oak Cottage". */
    private static final Set<String> NOUNS = Set.of("cottage", "house", "townhouse", "bungalow", "hut", "cabin", "lodge");
    private static final Map<String, String> ROOMS = Map.of("apothecary", "The Apothecary's Rooms", "library", "The Library Rooms",
            "workshop", "The Workshop Loft");

    /** The house's name, given who lives there ({@code residents}, looked up with {@code folk}). */
    public static String name(House h, List<String> residents, Function<String, Townsfolk> folk) {
        if (!h.customName().isBlank()) return h.customName();
        if (h.use() == House.Use.HOME) {
            String surname = surname(residents, folk);
            if (!surname.isEmpty()) return "The " + surname + " House";
        }
        return switch (h.use()) {
            case BARRACKS -> "The Garrison";
            case INN -> "Guest rooms at the tavern";
            case QUARTERS -> ROOMS.getOrDefault(last(h.template()), label(h.template()));
            default -> h.kind() == House.Kind.PLAYER ? "A house you built" : h.template().isEmpty() ? "A little house" : label(h.template());
        };
    }
    /** The household head's surname: the grown-up who has lived there longest. */
    static String surname(List<String> residents, Function<String, Townsfolk> folk) {
        var head = residents.stream().map(folk).filter(t -> t != null && t.adult())
                .min(Comparator.comparingLong(Townsfolk::joined).thenComparing(Townsfolk::id)).orElse(null);
        if (head == null) head = residents.stream().map(folk).filter(t -> t != null).min(Comparator.comparing(Townsfolk::id)).orElse(null);
        if (head == null) return "";
        String name = head.name().trim();
        int space = name.lastIndexOf(' ');
        return space > 0 ? name.substring(space + 1) : "";
    }
    private static String last(String template) {
        int slash = template.lastIndexOf('/');
        return slash < 0 ? template.substring(template.indexOf(':') + 1) : template.substring(slash + 1);
    }
    /** "Oak Cottage" for "villagefriends:village/cottage_oak", "Tall Brick House" for ".../house_tall_brick". */
    public static String label(String template) {
        var words = new java.util.ArrayList<>(List.of(last(template).split("_")));
        if (words.size() > 1 && NOUNS.contains(words.getFirst())) words.add(words.removeFirst());
        if (words.size() == 2 && words.get(0).equals("a") && words.get(1).equals("frame")) return "A-Frame";
        var out = new StringBuilder();
        for (var w : words) {
            if (w.isEmpty()) continue;
            if (!out.isEmpty()) out.append(' ');
            out.append(w.substring(0, 1).toUpperCase(Locale.ROOT)).append(w.substring(1));
        }
        return out.toString();
    }

    private HouseNames() {}
}
