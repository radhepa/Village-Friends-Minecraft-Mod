package dev.villagefriends.rpg;

import dev.villagefriends.fishing.FishingEvents;

/**
 * The Fishing skill, through Tall Tales Fishing's hooks. Every fish already trains it (the "fish caught" statistic,
 * in {@link Life}); rarer fish and perfect catches (the fish never left the zone) teach more. Each level adds
 * luck (better odds of rare fish and treasure), a slightly bigger catch zone in the minigame and a faster reel.
 */
final class Angler {
    static void register() {
        FishingEvents.TUNE.register((player, fish, tuning) -> {
            int s = Rpg.sheet(player).skill(Skill.FISHING);
            return tuning.widen((float) (Balance.FISH_ZONE * s)).reel((float) (Balance.FISH_REEL * s));
        });
        FishingEvents.CAUGHT.register((player, fish, size, perfect) -> {
            double xp = Balance.fishXp(fish.rarity().ordinal(), perfect);
            if (xp > 0) Progress.skill(player, Skill.FISHING, xp);
        });
    }

    private Angler() {}
}
