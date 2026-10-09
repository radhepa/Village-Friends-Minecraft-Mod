package dev.villagefriends.rpg;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class CookingSkillTest {
    @Test void cookingStaysModestAtTheCap() {
        double wellFed = 1 + Balance.COOK_WELL_FED * Balance.SKILL_CAP, fine = Balance.COOK_FINE * Balance.SKILL_CAP;
        assertTrue(wellFed <= 1.5, "a master cook's Well Fed lasts at most half as long again: " + wellFed);
        assertTrue(fine <= .4, "most dishes still come out ordinary: " + fine);
        assertTrue(Balance.cookXp(3) > Balance.cookXp(2) && Balance.cookXp(2) > Balance.cookXp(1) && Balance.cookXp(1) > Balance.cookXp(0));
        assertEquals("+10.0% Well Fed time, 8.0% fine dish", Skill.COOKING.effect(10));
        assertEquals("cooking", Skill.COOKING.id());
    }
}
