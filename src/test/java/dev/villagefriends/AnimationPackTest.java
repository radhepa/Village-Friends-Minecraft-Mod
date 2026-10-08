package dev.villagefriends;

import static org.junit.jupiter.api.Assertions.*;
import dev.villagefriends.animation.*;
import java.util.*;
import org.junit.jupiter.api.Test;

class AnimationPackTest {
    private static final AnimationLibrary PACK = AnimationLibrary.builtin();
    private static final List<String> VANILLA_JOBS = List.of("armorer", "butcher", "cartographer", "cleric", "farmer", "fisherman",
            "fletcher", "leatherworker", "librarian", "mason", "shepherd", "toolsmith", "weaponsmith", "nitwit", "none");

    private static Set<String> adult(String... extra) {
        var tags = new HashSet<>(Set.of("adult", "day")); tags.addAll(List.of(extra)); return tags;
    }
    private static long eligible(String trigger, Set<String> tags, String requiredTag) {
        return PACK.clips(trigger).stream().filter(c -> c.eligible(tags))
                .filter(c -> c.require().stream().anyMatch(g -> g.contains(requiredTag))).count();
    }

    @Test void villageLifeIsALargeVariedFirstPack() {
        assertEquals(2, PACK.packs().size());
        assertEquals("Village Life", PACK.packs().getFirst().name());
        assertEquals("Tavern", PACK.packs().get(1).name());
        assertTrue(PACK.clips().size() >= 349, "a large first pack: " + PACK.clips().size());
        for (String trigger : AnimationPack.TRIGGERS) assertFalse(PACK.clips(trigger).isEmpty(), "clips for " + trigger);
        assertTrue(PACK.clips("idle").size() >= 210);
        assertTrue(PACK.clips("talk").size() >= 24 && PACK.clips("chat_speak").size() >= 15 && PACK.clips("chat_listen").size() >= 15);
        assertTrue(PACK.clips("greet").stream().filter(c -> c.eligible(Set.of("child"))).count() >= 4, "children greet too");
        for (String trigger : List.of("laugh", "delighted", "thanks", "decline", "happy", "love", "angry", "nervous"))
            assertTrue(PACK.clips(trigger).size() >= 6, "a varied set of reactions for " + trigger);
    }

    @Test void everyPersonalityHasAHobbyAndEveryProfessionAWorkMotion() {
        for (var personality : NarrativeContent.current().personalities())
            assertTrue(eligible("idle", adult("personality:" + personality.id()), "personality:" + personality.id()) >= 3, "hobbies for " + personality.id());
        var jobs = new ArrayList<>(VANILLA_JOBS); jobs.addAll(VillageProfessions.JOBS);
        for (String job : jobs) {
            var tags = adult(); ResidentBehavior.jobTags(job, tags);
            assertTrue(eligible("idle", tags, "job:" + job) >= 4, "work motions for " + job);
        }
        var guard = adult(); ResidentBehavior.jobTags("knight", guard);
        assertTrue(PACK.clips("greet").stream().anyMatch(c -> c.eligible(guard) && c.name().equals("Salutes")));
    }

    @Test void childrenPlayAndWeatherChangesTheMood() {
        var child = Set.of("child", "day");
        assertTrue(PACK.clips("idle").stream().filter(c -> c.eligible(child) && c.require().stream().anyMatch(g -> g.contains("child"))).count() >= 20);
        assertTrue(PACK.clips("idle").stream().noneMatch(c -> c.eligible(child) && c.name().equals("Hammers at the anvil")));
        var rain = adult("rain");
        assertTrue(PACK.clips("idle").stream().filter(c -> c.eligible(rain) && c.require().stream().anyMatch(g -> g.contains("rain"))).count() >= 7);
        assertTrue(PACK.clips("idle").stream().anyMatch(c -> c.eligible(adult("thunder")) && c.require().stream().anyMatch(g -> g.contains("thunder"))));
        assertTrue(PACK.clips("idle").stream().noneMatch(c -> c.eligible(rain) && c.name().equals("Big stretch")), "nobody stretches in the rain");
        assertTrue(PACK.clips("idle").stream().anyMatch(c -> c.eligible(adult("cold")) && c.name().equals("Shivers")));
    }

    @Test void clipsStartAndEndAtRestAndStayInBounds() {
        float[] out = new float[3];
        for (var clip : PACK.clips()) {
            assertTrue(clip.length() > .5F && clip.length() <= 8, clip.id());
            for (var bone : AnimationClip.Bone.ALL) {
                for (var track : new AnimationTrack[]{clip.rotations()[bone.ordinal()], clip.positions()[bone.ordinal()]}) {
                    if (track == null) continue;
                    for (float t : new float[]{0, clip.length()}) {
                        track.sample(t, out, 0);
                        for (float v : out) assertEquals(0, Math.IEEEremainder(v, 360), .001, clip.id() + " " + bone + " rests at " + t);
                    }
                    for (float t = 0; t <= clip.length(); t += .01F) {
                        track.sample(t, out, 0);
                        for (float v : out) assertTrue(Float.isFinite(v) && Math.abs(v) <= 400, clip.id());
                    }
                }
            }
            if (clip.lid() != null) for (float t = 0; t <= clip.length(); t += .01F) {
                clip.lid().sample(t, out, 0); assertTrue(out[0] >= -.001F && out[0] <= 1.001F, clip.id() + " eyelids stay in range");
            }
            assertEquals(0, clip.envelope(-.1F)); assertEquals(0, clip.envelope(clip.length() + .1F));
        }
    }

    @Test void curvesAreSmoothWithoutOvershootOrPops() {
        var track = new AnimationTrack(new float[]{0, .5F, 1, 1.2F, 2}, new float[]{0, 0, 0, -90, 10, 0, -90, 10, 0, -20, 0, 0, 0, 0, 0});
        float[] out = new float[3]; float previous = 0;
        for (float t = 0; t <= 2; t += .005F) {
            track.sample(t, out, 0);
            assertTrue(out[0] >= -90.001F && out[0] <= .001F, "no overshoot past the keys: " + out[0]);
            assertTrue(Math.abs(out[0] - previous) < 6, "no pops between frames");
            if (t > .5F && t < 1) assertEquals(-90, out[0], .001F, "a hold stays perfectly still");
            previous = out[0];
        }
        track.sample(0, out, 0); assertEquals(0, out[0]);
        track.sample(2, out, 0); assertEquals(0, out[0]);
    }

    @Test void pickingRespectsTagsAndAvoidsRepeats() {
        var random = new Random(4);
        var counts = new HashMap<String, Integer>();
        String last = null;
        int repeats = 0;
        for (int i = 0; i < 2000; i++) {
            var clip = PACK.pick("idle", adult("job:cleric", "personality:gentle"), random, last);
            assertTrue(clip.eligible(adult("job:cleric", "personality:gentle")));
            if (clip.id().equals(last)) repeats++;
            counts.merge(clip.name(), 1, Integer::sum);
            last = clip.id();
        }
        assertTrue(counts.size() > 20, "a resident has a wide repertoire: " + counts.size());
        assertTrue(counts.getOrDefault("Prays", 0) > 60, "the cleric's work shows up often");
        assertTrue(counts.getOrDefault("Smells a flower", 0) > 40, "the gentle hobby shows up often");
        assertTrue(repeats < 20, "rarely the same clip twice in a row: " + repeats);
        assertNull(PACK.pick("greet", Set.of(), random), "no greeting fits a resident with no age");
    }

    @Test void brokenPacksAreRejectedWithClearReasons() {
        String ok = "{\"format\":1,\"clips\":[{\"id\":\"a\",\"length\":1,\"tracks\":{\"head.rot\":[[0,0,0,0],[1,10,0,0]]}}]}";
        assertEquals(1, AnimationPack.parse("test", ok).clips().size());
        assertThrows(IllegalArgumentException.class, () -> AnimationPack.parse("test", ok.replace("\"format\":1", "\"format\":2")));
        assertThrows(IllegalArgumentException.class, () -> AnimationPack.parse("test", ok.replace("\"length\":1", "\"length\":1,\"trigger\":\"dance\"")));
        assertThrows(IllegalArgumentException.class, () -> AnimationPack.parse("test", ok.replace("[1,10,0,0]", "[0,10,0,0]")));
        assertThrows(IllegalArgumentException.class, () -> AnimationPack.parse("test", ok.replace("[1,10,0,0]", "[2,10,0,0]")));
        assertThrows(IllegalArgumentException.class, () -> AnimationPack.parse("test", ok.replace("head.rot", "tail.rot")));
        assertThrows(IllegalArgumentException.class, () -> AnimationPack.parse("test", ok.replace("[1,10,0,0]", "[1,999,0,0]")));
        assertThrows(IllegalArgumentException.class, () -> AnimationPack.parse("test", "{not json"));
        var replaced = new AnimationLibrary(List.of(PACK.packs().getFirst(),
                AnimationPack.parse("mine", "{\"format\":1,\"disable\":[\"village_life:sneeze\"],\"clips\":[]}")));
        assertNull(replaced.clip("village_life:sneeze"), "a resource pack can switch clips off");
        assertNotNull(replaced.clip("village_life:yawn"));
    }

    @Test void situationRules() {
        assertEquals("morning", ResidentBehavior.timeTag(0)); assertEquals("day", ResidentBehavior.timeTag(6000));
        assertEquals("evening", ResidentBehavior.timeTag(12000)); assertEquals("night", ResidentBehavior.timeTag(18000));
        assertEquals("morning", ResidentBehavior.timeTag(23500 + 24000L * 9));
        int lefties = 0;
        for (int i = 0; i < 9000; i++) if (ResidentBehavior.leftHanded(ResidentMotion.seed(new UUID(i * 31L, i)))) lefties++;
        assertTrue(lefties > 600 && lefties < 1500, "about one in nine residents is left-handed: " + lefties);
        assertTrue(ResidentBehavior.pause(1.35F, .5F) < ResidentBehavior.pause(.8F, .5F), "lively residents fidget sooner");
    }
}
