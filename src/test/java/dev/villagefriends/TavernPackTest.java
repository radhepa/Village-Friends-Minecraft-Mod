package dev.villagefriends;

import static org.junit.jupiter.api.Assertions.*;

import dev.villagefriends.animation.AnimationClip.Bone;
import dev.villagefriends.animation.AnimationLibrary;
import java.util.HashMap;
import java.util.Random;
import java.util.Set;
import org.junit.jupiter.api.Test;

class TavernPackTest {
    private static final AnimationLibrary PACK = AnimationLibrary.builtin();
    private static long count(String prefix) { return PACK.clips().stream().filter(c -> c.id().startsWith("tavern:")).filter(c -> c.id().contains(prefix)).count(); }

    @Test void theTavernPackShipsWithTheMod() {
        long tavern = PACK.clips().stream().filter(c -> c.id().startsWith("tavern:")).count();
        assertTrue(tavern >= 50, "a full tavern pack: " + tavern);
        for (var clip : PACK.clips()) {
            if (!clip.seated()) continue;
            for (var bone : new Bone[]{Bone.RIGHT_LEG, Bone.LEFT_LEG, Bone.ROOT})
                assertFalse(clip.uses(bone), clip.id() + " leaves the legs to the seat");
        }
    }

    @Test void sittingResidentsOnlyDoSeatedThings() {
        var random = new Random(5);
        var seated = Set.of("adult", "seated", "tavern", "evening", "routine:tavern");
        for (String trigger : new String[]{"idle", "chat_speak", "chat_listen", "talk"})
            for (int i = 0; i < 200; i++) {
                var clip = PACK.pick(trigger, seated, random);
                assertNotNull(clip, "a seated " + trigger);
                assertTrue(clip.seated(), trigger + " while seated picked a standing clip: " + clip.id());
            }
        // Standing residents never pick a seated clip.
        var standing = Set.of("adult", "day", "job:mason");
        for (int i = 0; i < 400; i++) assertFalse(PACK.pick("idle", standing, random).seated());
        // Reactions use a seated version when there is one.
        for (int i = 0; i < 50; i++) assertTrue(PACK.pick("laugh", seated, random).seated());
        assertNotNull(PACK.pick("hurt", seated, random), "and fall back to any reaction otherwise");
    }

    @Test void dinersMostlyEat() {
        var random = new Random(9);
        var tags = Set.of("adult", "seated", "tavern", "day", "routine:lunch_tavern", "dining:eat", "food:stew");
        var picks = new HashMap<Boolean, Integer>();
        for (int i = 0; i < 1000; i++) {
            var clip = PACK.pick("idle", tags, random);
            boolean eating = clip.require().stream().anyMatch(g -> g.contains("dining:eat"));
            picks.merge(eating, 1, Integer::sum);
        }
        assertTrue(picks.getOrDefault(true, 0) > 700, "Eating clips while the food is in front of them: " + picks);
        assertTrue(count("stew") >= 1 && count("bread") >= 1 && count("pie") >= 1, "a clip for each dish");
        var waiting = Set.of("adult", "seated", "tavern", "evening", "dining:wait");
        int craning = 0;
        for (int i = 0; i < 400; i++) if (PACK.pick("idle", waiting, random).require().stream().anyMatch(g -> g.contains("dining:wait"))) craning++;
        assertTrue(craning > 80, "Waiting for the food shows: " + craning);
    }
}
