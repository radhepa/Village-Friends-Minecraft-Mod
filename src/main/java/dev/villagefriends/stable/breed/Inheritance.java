package dev.villagefriends.stable.breed;

import dev.villagefriends.stable.data.StableTable;
import java.util.random.RandomGenerator;

/**
 * A foal's breed, coat and stats from its parents, pure so it can be unit tested.
 *
 * <p>The foal takes one parent's breed, 50/50 (two parents of one breed always give that breed). Its coat is the
 * matching parent's when both parents share the breed, otherwise a random coat of its breed. Each stat uses
 * vanilla's offspring formula, {@code mid + (|a - b| + 0.3 * width) * (average of three rolls - 0.5)}, with the
 * width of the foal's breed, then is kept inside that breed's range widened by 10% of its width on each side:
 * careful breeding can edge a little past the wild range, never far, and a draft parent can't make a courser foal
 * as heavy as a draft horse.
 */
public final class Inheritance {
    /** How far past its breed's wild range a bred stat may go, as a fraction of the range's width. */
    public static final double EDGE = 0.1;

    public record Foal(String breed, int coat, BreedRolls.Stats stats) {}

    public static Foal foal(StableTable.Breed a, BreedRolls.Stats sa, int coatA, StableTable.Breed b, BreedRolls.Stats sb, int coatB, RandomGenerator r) {
        boolean same = a.id().equals(b.id());
        boolean first = r.nextBoolean();
        var breed = first || same ? a : b;
        int coats = Math.max(1, breed.coats());
        int parentCoat = first ? coatA : coatB;
        int coat = same && parentCoat >= 0 && parentCoat < coats ? parentCoat : r.nextInt(coats);
        var stats = new BreedRolls.Stats(blend(sa.health(), sb.health(), breed.health(), r), blend(sa.speed(), sb.speed(), breed.speed(), r),
                blend(sa.jump(), sb.jump(), breed.jump(), r));
        return new Foal(breed.id(), coat, stats);
    }

    /** One stat of a foal: between its parents, spread like vanilla, inside the widened range. */
    static double blend(double a, double b, StableTable.Range range, RandomGenerator r) {
        double quality = (r.nextDouble() + r.nextDouble() + r.nextDouble()) / 3 - 0.5;
        double value = (a + b) / 2 + (Math.abs(a - b) + 0.3 * range.width()) * quality;
        var limits = widened(range);
        return Math.clamp(value, limits.min(), limits.max());
    }

    /** A breed's range widened by {@link #EDGE} of its width on both sides: where bred stats are allowed to land. */
    public static StableTable.Range widened(StableTable.Range range) {
        double edge = EDGE * range.width();
        return new StableTable.Range(range.min() - edge, range.max() + edge);
    }

    private Inheritance() {}
}
