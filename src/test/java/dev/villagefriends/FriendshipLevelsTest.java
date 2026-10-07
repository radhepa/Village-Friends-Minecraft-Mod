package dev.villagefriends;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

class FriendshipLevelsTest {
    private static FriendshipState points(int p) { return new FriendshipState(p, -1, -1, 0, ""); }

    @Test void tenLevelsSitInsideTheFiveTiers() {
        int[] boundaries = {0, 4, 5, 15, 27, 28, 40, 58, 80, 104, 105, 140, 169, 170, 200};
        int[] levels = {0, 0, 1, 2, 2, 3, 4, 5, 6, 6, 7, 8, 8, 9, 10};
        for (int i = 0; i < boundaries.length; i++) assertEquals(levels[i], FriendshipLevels.byPoints(boundaries[i]), "points " + boundaries[i]);
        for (int p = 0; p <= 200; p++) assertEquals(points(p).level(), FriendshipLevels.tier(FriendshipLevels.byPoints(p)), "tier at " + p);
        assertEquals("Lifelong Friend", FriendshipLevels.name(10));
        assertEquals("Best Friend", FriendshipLevels.name(8));
    }

    @Test void levelsRespectStoryGatesAndMatchTheExistingTier() {
        var fresh = BondState.NEW;
        assertEquals(3, FriendshipLevels.level(points(200), fresh), "gifts alone stop at Friendly Neighbor");
        assertTrue(FriendshipLevels.goal(points(200), fresh).contains("Share an experience"));
        var shared = fresh.activity(0, "walk");
        assertEquals(5, FriendshipLevels.level(points(200), shared));
        var story = shared.chapter(4);
        for (int day = 0; day < 5; day++) story = story.visit(day);
        assertEquals(10, FriendshipLevels.level(points(200), story));
        assertTrue(FriendshipLevels.goal(points(200), story).startsWith("Lifelong"));
        for (var bond : new BondState[]{fresh, shared, shared.chapter(3), story, BondState.migrated(3)})
            for (int p = 0; p <= 200; p += 3)
                assertEquals(bond.level(points(p)), FriendshipLevels.tier(FriendshipLevels.level(points(p), bond)));
        assertEquals(6, FriendshipLevels.level(points(0), BondState.migrated(3)), "earned tiers are kept");
        assertTrue(FriendshipLevels.goal(points(30), shared).startsWith("10 more to Lv. 4"));
    }
}
