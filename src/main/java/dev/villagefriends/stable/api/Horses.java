package dev.villagefriends.stable.api;

import static dev.villagefriends.VillageFriends.target;

import dev.villagefriends.stable.bond.BondMath;
import dev.villagefriends.stable.data.HorseBond;
import dev.villagefriends.stable.data.HorseBreed;
import dev.villagefriends.stable.data.StableData;
import dev.villagefriends.stable.data.StableTable;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.entity.animal.equine.Horse;

/**
 * Breeds and bonds, for the rest of Stablehand and for add-ons (server side). Breeds belong to horses only
 * (not donkeys, mules, camels or undead horses); bonds to horses, donkeys and mules.
 * Owned by the breeds package; the signatures are frozen.
 */
public final class Horses {
    /** The horse's breed id, if it has one. */
    public static Optional<String> breed(AbstractHorse horse) {
        return Optional.ofNullable(target(horse).getAttached(StableData.BREED)).map(HorseBreed::breed);
    }
    /** The breed a horse born or found here would be (by the biome at {@code pos}). */
    public static String pickBreed(ServerLevel level, BlockPos pos, RandomSource random) { return "rouncey"; }
    /** Makes a horse this breed: its stats, markings and coat. Does nothing for animals that are not horses. */
    public static void assignBreed(AbstractHorse horse, String breed, RandomSource random) {
        if (horse instanceof Horse) target(horse).setAttached(StableData.BREED, new HorseBreed(breed, 0));
    }
    /** Bond points with its partner, 0 to {@link BondMath#MAX}. */
    public static int bondPoints(AbstractHorse horse) { return target(horse).getAttachedOrElse(StableData.BOND, HorseBond.NONE).points(); }
    /** Bond tier, 0 (Wary) to 4 (Devoted). */
    public static int bondTier(AbstractHorse horse) { return BondMath.tier(bondPoints(horse)); }
    /** The player the horse is bonded with, if any. */
    public static Optional<UUID> bondPartner(AbstractHorse horse) {
        String partner = target(horse).getAttachedOrElse(StableData.BOND, HorseBond.NONE).partner();
        try { return partner.isEmpty() ? Optional.empty() : Optional.of(UUID.fromString(partner)); }
        catch (IllegalArgumentException e) { return Optional.empty(); }
    }
    /** Adds bond points from {@code player} (source "groom", "feed", "ride" or "api"; tests and add-ons use "api"). */
    public static void addBond(AbstractHorse horse, ServerPlayer player, int points, String source) {}
    /** Every breed id, in table order. */
    public static List<String> breeds() { return StableTable.breeds().stream().map(StableTable.Breed::id).toList(); }

    private Horses() {}
}
