package dev.villagefriends;

import static org.junit.jupiter.api.Assertions.*;
import com.google.gson.JsonParser;
import com.mojang.serialization.JsonOps;
import java.util.*;
import org.junit.jupiter.api.Test;

class RoadmapTest {
    private static FriendshipState full() { return new FriendshipState(200, 0, 0, 0, ""); }
    @Test void giftsCannotFinishFriendshipButMigratedTiersStayUnlocked() {
        assertEquals(1, BondState.NEW.level(full()));
        var b = BondState.NEW.activity(0, "walk");
        assertEquals(2, b.level(full()));
        assertEquals(3, b.chapter(3).level(full()));
        b = b.chapter(4);
        for (int day = 0; day < 5; day++) b = b.visit(day);
        assertEquals(4, b.level(full()));
        for (int old = 0; old <= 4; old++) assertEquals(old, BondState.migrated(old).level(new FriendshipState(new int[]{0,15,40,80,140}[old], -1,-1,0,"")));
    }
    @Test void timeAwayDoesNotDecayTrustAndVisitsCountDistinctDays() {
        var b = BondState.NEW.visit(2).visit(2).visit(90_000);
        assertEquals(2, b.visits()); assertEquals(50, b.trust());
        assertEquals(55, b.activity(90_000, "walk").activity(90_000, "picnic").trust());
        assertEquals(60, b.activity(90_000, "walk").activity(90_001, "picnic").trust());
    }
    @Test void recentHistoryIsBoundedWithoutEvictingPermanentMilestones() {
        var b = BondState.NEW.flag("story_gift").chapter(4);
        for (int i = 0; i < 100; i++) b = b.remember(i, "Memory " + i).line("line:" + i).flag("milestone:" + i);
        assertEquals(24, b.memories().size()); assertEquals(12, b.recentLines().size());
        assertTrue(b.has("story_gift")); assertEquals(4, b.chapter());
        assertTrue(b.memories().getFirst().contains("Memory 76"));
    }
    @Test void personalBooksAndSharedOutcomesSurviveCodecsAndKeepCredit() {
        UUID a = UUID.randomUUID(), z = UUID.randomUUID();
        var book = BondBook.empty().with(a, BondState.NEW.chapter(3).flag("ending:encourage").remember(1,"You helped me"));
        var encoded = BondBook.CODEC.encodeStart(JsonOps.INSTANCE, book).getOrThrow();
        var restored = BondBook.CODEC.parse(JsonOps.INSTANCE, encoded).getOrThrow();
        assertEquals(book, restored); assertEquals(0, restored.get(z).chapter());
        var history = SharedHistory.EMPTY.complete("garden/seeds", "Alex").complete("garden/seeds", "Sam");
        assertEquals("Alex", history.outcomes().get("garden/seeds"));
        assertEquals(history, SharedHistory.CODEC.parse(JsonOps.INSTANCE, SharedHistory.CODEC.encodeStart(JsonOps.INSTANCE, history).getOrThrow()).getOrThrow());
        assertEquals(BondState.NEW, BondState.CODEC.parse(JsonOps.INSTANCE, JsonParser.parseString("{}")).getOrThrow());
    }
    @Test void residentIdentityAndRecipeRoundTripIndependentlyOfEntityUuid() {
        var profile = ResidentProfile.generate(UUID.randomUUID(), ResidentAppearance.generate(UUID.fromString("01234567-89ab-cdef-0123-456789abcdef")));
        assertEquals(profile, ResidentProfile.CODEC.parse(JsonOps.INSTANCE, ResidentProfile.CODEC.encodeStart(JsonOps.INSTANCE, profile).getOrThrow()).getOrThrow());
        assertEquals(ResidentAppearance.generate(UUID.fromString("01234567-89ab-cdef-0123-456789abcdef")), profile.look());
        var state = new CompanionState(UUID.randomUUID().toString(), "downed", 5,64,8,1200,true,0);
        assertEquals(state, CompanionState.CODEC.parse(JsonOps.INSTANCE, CompanionState.CODEC.encodeStart(JsonOps.INSTANCE, state).getOrThrow()).getOrThrow());
    }
    @Test void bundledContentMeetsCastAndStoryTargets() {
        var content = NarrativeContent.current();
        assertEquals(12, content.personalities().size()); assertEquals(8, content.stories().size());
        assertEquals(24, content.stories().stream().mapToInt(s -> s.requests().size()).sum());
        assertSame(content, NarrativeContent.validate(content));
        assertTrue(content.stories().stream().allMatch(s -> s.conditions().confessionVisits()==3 && s.conditions().endingVisits()==5 && s.conditions().requireSharedExperience()));
    }
    @Test void residentFriendshipsGrowOncePerDayAndStayBoundedAndPersistent() {
        var history = SharedHistory.EMPTY.mingle(0, Map.of("neighbor",1)).mingle(0,Map.of("neighbor",1));
        assertEquals(1, history.residentFriends().get("neighbor"));
        history = history.mingle(1,Map.of("neighbor",2));
        assertEquals(3, history.residentFriends().get("neighbor"));
        var neighbors = new HashMap<String,Integer>(); for(int n=0;n<100;n++) neighbors.put("resident:"+n,1);
        history = history.mingle(2,neighbors);
        assertEquals(16, history.residentFriends().size());
        assertEquals(history, SharedHistory.CODEC.parse(JsonOps.INSTANCE, SharedHistory.CODEC.encodeStart(JsonOps.INSTANCE, history).getOrThrow()).getOrThrow());
    }
    @Test void invalidContentIsRejectedBeforeItCanReplaceTheWorkingPack() {
        var content = NarrativeContent.current();
        assertThrows(IllegalArgumentException.class, () -> NarrativeContent.parse("{\"version\":2}"));
        assertThrows(IllegalArgumentException.class, () -> NarrativeContent.validate(new NarrativeContent.Data(1, List.of(content.personalities().getFirst(), content.personalities().getFirst()), content.stories())));
        var s = content.stories().getFirst(); var r = s.requests().getFirst();
        var bad = new NarrativeContent.Request(r.id(), r.title(), r.item(), 65, r.prompt(), r.thanks());
        assertThrows(IllegalArgumentException.class, () -> NarrativeContent.validate(new NarrativeContent.Data(1, content.personalities(), List.of(new NarrativeContent.Story(s.id(),s.title(),s.intro(),s.confide(),s.encourage(),s.practical(),s.gift(),List.of(bad,s.requests().get(1),s.requests().get(2)))))));
        assertSame(content, NarrativeContent.current());
    }

}

