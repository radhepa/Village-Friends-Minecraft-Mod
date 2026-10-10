package dev.villagefriends.stable.api;

import static dev.villagefriends.VillageFriends.target;

import dev.villagefriends.stable.bond.BondMath;
import dev.villagefriends.stable.bond.Bonds;
import dev.villagefriends.stable.breed.Breeds;
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
    public static String pickBreed(ServerLevel level, BlockPos pos, RandomSource random) { return Breeds.pick(level, pos, random); }
    /**
     * Makes a horse this breed: its stats (rolled from the breed's ranges and saved as base values), one of its
     * markings and a coat; it is healed to its new full health. Does nothing for animals that are not horses or for an
     * unknown breed id.
     */
    public static void assignBreed(AbstractHorse horse, String breed, RandomSource random) {
        if (horse instanceof Horse h) Breeds.assign(h, breed, random);
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
    /**
     * Adds bond points from {@code player} (source "groom", "feed", "ride" or "api"; tests and add-ons use "api").
     * The points are added as given (no daily cap, only {@link BondMath#MAX}) and {@code source} is what
     * {@code StablehandEvents.BOND_GAINED} reports. Like every gain, it only counts from the horse's owner, for a
     * horse, donkey or mule, and a different owner than the last partner starts the bond again from 0.
     */
    public static void addBond(AbstractHorse horse, ServerPlayer player, int points, String source) {
        Bonds.gain(horse, player, BondMath.Source.API, points, source == null || source.isBlank() ? "api" : source);
    }
    /** Every breed id, in table order. */
    public static List<String> breeds() { return StableTable.breeds().stream().map(StableTable.Breed::id).toList(); }

    /** A breed's name for players ("Draft Horse"); the id itself for an unknown breed. */
    public static String breedName(String breed) { return Breeds.name(breed); }
    /** Whether a horse, donkey or mule can bond (camels, llamas and undead horses can't). */
    public static boolean bondable(AbstractHorse horse) { return Bonds.bondable(horse); }

    private Horses() {}
}
