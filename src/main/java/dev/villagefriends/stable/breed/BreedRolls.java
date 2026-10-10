package dev.villagefriends.stable.breed;

import dev.villagefriends.stable.data.StableTable;
import java.util.random.RandomGenerator;

/**
 * A new horse's stats from its breed's ranges, pure so it can be unit tested. Each stat is the average of two
 * uniform rolls across the range, so most horses sit near the middle of their breed and the ends are rare (a soft
 * middle, like vanilla's own sum of rolls). Health is rounded to whole hit points, as vanilla's wild horses have.
 */
public final class BreedRolls {
    /** A horse's three bred stats, in vanilla attribute units: max health, movement speed and jump strength. */
    public record Stats(double health, double speed, double jump) {}

    public static Stats roll(StableTable.Breed breed, RandomGenerator random) {
        return new Stats(Math.round(soft(breed.health(), random)), soft(breed.speed(), random), soft(breed.jump(), random));
    }

    static double soft(StableTable.Range range, RandomGenerator random) {
        return range.min() + range.width() * (random.nextDouble() + random.nextDouble()) / 2;
    }

    private BreedRolls() {}
}
