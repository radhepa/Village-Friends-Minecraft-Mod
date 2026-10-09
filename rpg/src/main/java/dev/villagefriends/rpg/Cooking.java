package dev.villagefriends.rpg;

import dev.villagefriends.hearth.HearthApi;
import dev.villagefriends.hearth.HearthEvents;

/**
 * The Cooking skill, through Hearth & Harvest's hooks. Taking food out of a cooking pot, clay oven or prep
 * table trains it (more for better dishes). Each level makes the Well Fed you get from eating last 1% longer
 * and gives the dishes you cook a 0.8% chance to come out fine (fine dishes give a longer Well Fed and are
 * better gifts). The cook is whoever last opened the station.
 */
final class Cooking {
    static void register() {
        HearthEvents.TAKEN.register((player, station, taken) -> {
            var dish = HearthApi.dish(taken);
            int tier = dish == null ? 0 : dish.tier();
            Progress.skill(player, Skill.COOKING, Balance.cookXp(tier) * taken.getCount());
        });
        HearthEvents.COOKED.register((level, pos, station, recipe, cook, result) -> {
            if (cook == null) return;
            var dish = HearthApi.dish(result);
            if (dish == null || !dish.dish()) return;
            if (level.getRandom().nextDouble() < Balance.COOK_FINE * Rpg.sheet(cook).skill(Skill.COOKING)) HearthApi.makeFine(result);
        });
        HearthEvents.EATEN.register((player, dish, stack) -> 1 + Balance.COOK_WELL_FED * Rpg.sheet(player).skill(Skill.COOKING));
    }

    private Cooking() {}
}
