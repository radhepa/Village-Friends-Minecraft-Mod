package dev.villagefriends;

import static org.junit.jupiter.api.Assertions.*;
import dev.villagefriends.social.*;
import java.util.Map;
import org.junit.jupiter.api.Test;

class GossipTest {
    private static Townsfolk person(String id, String name, String gender, boolean adult) {
        return Townsfolk.newcomer(id, name, gender, "farmer", "warmhearted", adult, 0);
    }
    /** Mira and Tobin are married with a daughter, Pip; Wren lives alone. */
    private static Society family() {
        var s = Society.create("v", 0).register(person("mira", "Mira Ash", "FEMALE", true)).register(person("tobin", "Tobin Ash", "MALE", true))
                .register(person("pip", "Pip Ash", "FEMALE", false)).register(person("wren", "Wren Hale", "NON_BINARY", true));
        var mira = s.get("mira").partner("tobin", 3, true).kin("tobin", "spouse");
        var tobin = s.get("tobin").partner("mira", 3, true).kin("mira", "spouse");
        s = new Society("v", Map.of("mira", mira, "tobin", tobin, "pip", s.get("pip"), "wren", s.get("wren")), Map.of(), s.news(), 0);
        return s.born("pip", "mira", "tobin", 4);
    }

    @Test void residentsTalkAboutTheirRealFamiliesAndPartners() {
        var s = family();
        String heart = Gossip.heart(s, "mira", 30, 1);
        assertTrue(heart.contains("Tobin") && heart.contains("married"), heart);
        assertTrue(heart.contains("my daughter Pip"), heart);
        assertTrue(Gossip.heart(s, "pip", 30, 0).contains("frogs"));
        boolean mentioned = false;
        for (int salt = 0; salt < 12; salt++) mentioned |= Gossip.mention(s, "tobin", "chat", 30, salt).contains("Mira") || Gossip.mention(s, "tobin", "chat", 30, salt).contains("Pip");
        assertTrue(mentioned, "everyday chat mentions family");
        assertEquals("Married to Tobin Ash", Gossip.about(s, "mira", 30).getFirst());
        assertTrue(Gossip.about(s, "pip", 30).stream().anyMatch(line -> line.contains("Mother Mira Ash") && line.contains("Father Tobin Ash")));
    }

    @Test void newsIsToldFromEachResidentsPointOfView() {
        var s = family();
        assertTrue(Gossip.news(s, "wren", 5, 0, false).contains("welcomed a baby, Pip"));
        assertTrue(Gossip.news(s, "mira", 5, 0, false).contains("new little one: Pip"));
        assertTrue(Gossip.greeting(s, "wren", 5, 0).startsWith("Oh! Did you hear?"));
        assertEquals("", Gossip.greeting(s, "wren", 30, 0), "old news isn't breathless news");
        String quiet = Gossip.news(s, "wren", 60, 0, false);
        assertFalse(quiet.isBlank());
        var cursed = s.cursed("tobin", 61);
        assertTrue(Gossip.news(cursed, "wren", 62, 0, false).contains("golden apple"), "a cursed neighbor is a call to action");
    }

    @Test void everyLineIsSafeForAnyVillage() {
        var s = Society.create("v", 0);
        for (int n = 0; n < 16; n++) s = s.register(Townsfolk.newcomer("r" + n, "Resident " + n, n % 2 == 0 ? "MALE" : "FEMALE", n % 3 == 0 ? "none" : "librarian", "playful", n < 13, 0));
        for (long day = 1; day < 400; day++) s = s.advance(day);
        for (var t : s.living()) for (int salt = 0; salt < 6; salt++) {
            for (String topic : new String[]{"chat", "work", "adventure"}) assertNotNull(Gossip.mention(s, t.id(), topic, 400, salt));
            assertFalse(Gossip.news(s, t.id(), 400, salt, true).isBlank());
            assertFalse(Gossip.heart(s, t.id(), 400, salt).isBlank());
            for (var line : Gossip.about(s, t.id(), 400)) assertFalse(line.contains("someone") && line.contains("null"));
        }
        assertEquals("", Gossip.mention(Society.create("v", 0).register(person("solo", "Solo Person", "MALE", true)), "solo", "chat", 1, 0));
    }
}
