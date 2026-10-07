package dev.villagefriends.social;

/** Words for how residents are connected, shared by dialogue and the Village Ledger. */
public final class Relations {
    /** The family word for a relative of the given gender: ("parent", "FEMALE") is "Mother". */
    public static String kin(String relation, String gender) {
        int g = gender.equals("FEMALE") ? 0 : gender.equals("MALE") ? 1 : 2;
        String[] words = switch (relation) {
            case "spouse" -> new String[]{"Wife", "Husband", "Spouse"};
            case "parent" -> new String[]{"Mother", "Father", "Parent"};
            case "child" -> new String[]{"Daughter", "Son", "Child"};
            case "sibling" -> new String[]{"Sister", "Brother", "Sibling"};
            case "grandparent" -> new String[]{"Grandmother", "Grandfather", "Grandparent"};
            case "grandchild" -> new String[]{"Granddaughter", "Grandson", "Grandchild"};
            case "aunt_uncle" -> new String[]{"Aunt", "Uncle", "Parent's sibling"};
            case "niece_nephew" -> new String[]{"Niece", "Nephew", "Sibling's child"};
            case "cousin" -> new String[]{"Cousin", "Cousin", "Cousin"};
            case "sweetheart" -> new String[]{"Sweetheart", "Sweetheart", "Sweetheart"};
            case "relative" -> new String[]{"Relative", "Relative", "Relative"};
            default -> new String[]{"", "", ""};
        };
        return words[g];
    }
    /** How a resident feels about an unrelated neighbor, from their meter. */
    public static String feeling(int affinity) {
        if (affinity >= 85) return "Best friends";
        if (affinity >= 65) return "Good friends";
        if (affinity >= 40) return "Friends";
        if (affinity >= 15) return "Friendly";
        if (affinity >= -10) return "Neighbors";
        if (affinity >= -40) return "Not close";
        return "Rivals";
    }
    /** What {@code b} is to {@code a}, in one or two words: "Sister", "Sweetheart", "Good friends". */
    public static String label(Society society, String a, String b, long day) {
        var y = society.get(b); if (y == null) return "";
        String romance = society.romance(a, b, day);
        if (romance.equals("married")) return kin("spouse", y.gender());
        if (romance.equals("sweethearts")) return "Sweetheart";
        String relation = society.relation(a, b);
        if (!relation.isEmpty()) return kin(relation, y.gender());
        return feeling(society.affinity(a, b, day));
    }
    /** Subject, object and possessive pronouns: he/him/his, she/her/her or they/them/their. */
    public static String[] pronouns(String gender) {
        return switch (gender) {
            case "MALE" -> new String[]{"he", "him", "his"};
            case "FEMALE" -> new String[]{"she", "her", "her"};
            default -> new String[]{"they", "them", "their"};
        };
    }
    private Relations() {}
}
