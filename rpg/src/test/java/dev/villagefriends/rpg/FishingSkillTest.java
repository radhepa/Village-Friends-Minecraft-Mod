package dev.villagefriends.rpg;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class FishingSkillTest {
    @Test void fishingStaysModestAtTheCap() {
        double zone = Balance.FISH_ZONE * Balance.SKILL_CAP, reel = Balance.FISH_REEL * Balance.SKILL_CAP;
        assertTrue(zone <= 64, "a master angler's catch zone grows by at most about a ninth of the track: " + zone);
        assertTrue(reel <= .3, "and reels at most 30% faster: " + reel);
        for (int r = 1; r <= 4; r++) assertTrue(Balance.fishXp(r, false) > Balance.fishXp(r - 1, false), "rarer fish teach more");
        assertTrue(Balance.fishXp(2, true) > Balance.fishXp(2, false), "a perfect catch teaches more");
        assertEquals(0, Balance.fishXp(0, false));
        assertEquals("+0.3 luck, +6.0% reel speed", Skill.FISHING.effect(10));
    }
}
