package dev.villagefriends;

import static org.junit.jupiter.api.Assertions.*;

import com.mojang.serialization.JsonOps;
import dev.villagefriends.animation.AnimationLibrary;
import dev.villagefriends.pet.PetKeeping;
import dev.villagefriends.pet.PetPlays;
import dev.villagefriends.pet.PetProfile;
import dev.villagefriends.pet.PetTrick;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.*;
import org.junit.jupiter.api.Test;

class ResidentPetsTest {
    private static final List<String> PERSONALITIES = List.of("warmhearted", "thoughtful", "playful", "adventurous", "meticulous", "steadfast",
            "reserved", "imaginative", "pragmatic", "curious", "protective", "gentle");

    private static Map<String, PetTrick> tricks() throws IOException {
        try (var in = ResidentPetsTest.class.getResourceAsStream("/assets/villagefriends/pet_tricks/pets.json")) {
            assertNotNull(in, "the bundled pet tricks");
            return PetTrick.parse("pets.json", new String(in.readAllBytes(), StandardCharsets.UTF_8));
        }
    }

    @Test void someResidentsWantACatOrADogAndOthersDont() {
        var random = new Random(7);
        int cats = 0, dogs = 0, none = 0;
        for (int i = 0; i < 4000; i++) {
            var id = new UUID(random.nextLong(), random.nextLong());
            String personality = PERSONALITIES.get(i % PERSONALITIES.size());
            String wish = PetKeeping.wish(id, personality, i % 5 == 0);
            assertEquals(wish, PetKeeping.wish(id, personality, i % 5 == 0), "a resident's wish never changes");
            switch (wish) { case "cat" -> cats++; case "dog" -> dogs++; default -> none++; }
        }
        assertTrue(none > 1600 && none < 2800, "not everyone wants a pet: " + none);
        assertTrue(cats > 500 && dogs > 500, "both cats and dogs are wanted: " + cats + " cats, " + dogs + " dogs");
        // Adventurous and protective residents lean toward dogs, thoughtful and reserved ones toward cats.
        assertTrue(lean("protective", random) > .65 && lean("thoughtful", random) < .35);
    }
    private static double lean(String personality, Random random) {
        int dogs = 0, pets = 0;
        for (int i = 0; i < 3000; i++) {
            String wish = PetKeeping.wish(new UUID(random.nextLong(), random.nextLong()), personality, false);
            if (wish.isEmpty()) continue;
            pets++; if (wish.equals("dog")) dogs++;
        }
        return dogs / (double) pets;
    }

    @Test void everyPetHasANameANatureAFavoriteGameAndTreat() {
        var random = new Random(11);
        for (String species : List.of(PetKeeping.CAT, PetKeeping.DOG)) for (int i = 0; i < 200; i++) {
            var pet = PetKeeping.newProfile(random, species, "resident", "Mira Ash", 120, i % 4 == 0);
            assertFalse(pet.name().isBlank());
            assertTrue(PetKeeping.games(species).contains(pet.game()), pet.game());
            assertTrue(PetKeeping.natures(species).stream().anyMatch(n -> n.id().equals(pet.personality())));
            assertTrue(pet.treat().startsWith("minecraft:"));
            assertEquals(120, pet.adopted());
            if (i % 4 == 0) assertEquals(120, pet.born(), "a kitten or puppy is born the day they come home");
            else assertTrue(pet.born() <= 100, "strays are a few weeks old at least");
            String game = PetKeeping.pickGame(random, pet, PetKeeping.games(species));
            assertTrue(PetKeeping.games(species).contains(game));
            assertTrue(PetKeeping.playPause(random, pet, "playful") > 0);
        }
        assertEquals("Kitten", PetKeeping.stage("cat", true, 0));
        assertEquals("Grown dog", PetKeeping.stage("dog", false, 41));
        assertEquals("born today", PetKeeping.age(0));
        assertEquals("1 day old", PetKeeping.age(1));
        assertEquals("British shorthair", PetKeeping.breed("minecraft:british_shorthair"));
    }

    @Test void petProfilesSaveAndLoad() {
        var pet = PetKeeping.newProfile(new Random(3), "dog", "a-resident", "Tobin Reed", 50, false)
                .fondness(UUID.nameUUIDFromBytes("p".getBytes()), new PetProfile.Fondness(42, 50, 49));
        var json = PetProfile.CODEC.encodeStart(JsonOps.INSTANCE, pet).getOrThrow();
        assertEquals(pet, PetProfile.CODEC.parse(JsonOps.INSTANCE, json).getOrThrow());
        var released = pet.released();
        assertFalse(released.owned());
        assertEquals("Tobin Reed", released.former(), "a pet remembers who they belonged to");
        assertEquals(pet.name(), released.name());
        assertTrue(released.adoptedBy("b", "Mira Ash", 70).owned());
    }

    @Test void fondnessStaysBetweenZeroAndAHundred() {
        var f = PetProfile.Fondness.NONE;
        for (int i = 0; i < 30; i++) f = f.add(15);
        assertEquals(PetKeeping.MAX_FONDNESS, f.points());
        assertEquals(0, f.add(-500).points());
        assertEquals("Adores you", PetKeeping.fondnessLabel(95));
        assertEquals("Wary of you", PetKeeping.fondnessLabel(0));
    }

    @Test void everyTrickAndPartTheGamesUseExists() throws IOException {
        var tricks = tricks();
        var pack = AnimationLibrary.builtin();
        var tamingSpecies = new HashMap<String, String>();
        for (String species : List.of(PetKeeping.CAT, PetKeeping.DOG)) {
            var steps = new ArrayList<PetPlays.Step>();
            for (String game : PetKeeping.games(species)) steps.addAll(PetPlays.game(game, species.equals("cat") ? "minecraft:cod" : "minecraft:cooked_beef", 2));
            steps.addAll(PetPlays.taming(species, true)); steps.addAll(PetPlays.taming(species, false));
            for (var step : steps) {
                if (!step.trick().isEmpty()) assertNotNull(tricks.get(species + ":" + step.trick()), "trick " + species + ":" + step.trick());
                if (step.phase().isEmpty()) continue;
                for (String age : List.of("adult", "child")) {
                    var tags = Set.of(age, "day", "play:" + step.phase(), "pet:" + species);
                    assertTrue(pack.clips("pet").stream().anyMatch(c -> c.eligible(tags)), "a " + age + "'s clip for " + species + " phase " + step.phase());
                }
                tamingSpecies.put(step.phase(), species);
            }
        }
        // Only the pet trigger plays these: they never show up as everyday idles.
        assertTrue(pack.clips("pet").size() >= 20);
        assertTrue(pack.clips("idle").stream().noneMatch(c -> c.id().contains(":pet_coax")));
        // Steps that wait for someone to arrive always have a fallback length.
        for (var step : PetPlays.everyStep()) assertTrue(step.ticks() > 0);
    }

    @Test void trickFilesAreValidated() {
        assertThrows(IllegalArgumentException.class, () -> PetTrick.parse("bad", "{\"format\": 1, \"tricks\": [{\"id\": \"x\", \"species\": \"horse\", \"length\": 1, \"tracks\": {}}]}"));
        assertThrows(IllegalArgumentException.class, () -> PetTrick.parse("bad", "{\"format\": 1, \"tricks\": [{\"id\": \"x\", \"species\": \"cat\", \"length\": 1, \"tracks\": {\"wing.rot\": [[0, 0, 0, 0]]}}]}"));
        assertThrows(IllegalArgumentException.class, () -> PetTrick.parse("bad", "{\"format\": 1, \"tricks\": [{\"id\": \"x\", \"species\": \"cat\", \"length\": 1, \"tracks\": {\"head.rot\": [[0, 0, 0, 0], [2, 0, 0, 0]]}}]}"));
        var ok = PetTrick.parse("ok", "{\"format\": 1, \"tricks\": [{\"id\": \"x\", \"species\": \"dog\", \"length\": 1, \"loop\": true, \"tracks\": {\"head.rot\": [[0, 0, 0, 0], [0.5, 10, 0, 0], [1, 0, 0, 0]]}}]}");
        var trick = ok.get("dog:x");
        assertEquals(.25F, trick.time(1.25F), 1e-4, "loops wrap around");
        assertTrue(trick.envelope(5) > .99F, "a loop stays on until its pet does something else");
    }
}
