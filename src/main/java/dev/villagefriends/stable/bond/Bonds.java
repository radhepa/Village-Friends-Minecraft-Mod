package dev.villagefriends.stable.bond;

import static dev.villagefriends.VillageFriends.target;

import dev.villagefriends.VillageBlocks;
import dev.villagefriends.VillageFriends;
import dev.villagefriends.stable.api.Horses;
import dev.villagefriends.stable.api.StablehandEvents;
import dev.villagefriends.stable.breed.Breeds;
import dev.villagefriends.stable.data.HorseBond;
import dev.villagefriends.stable.data.StableData;
import dev.villagefriends.stable.data.StableTable;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.UUID;
import net.minecraft.core.Holder;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.Attribute;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.entity.animal.equine.Donkey;
import net.minecraft.world.entity.animal.equine.Horse;
import net.minecraft.world.entity.animal.equine.Mule;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;
import org.jspecify.annotations.Nullable;

/**
 * The bond in the world: who may grow it, applying a gain (with the riding multiplier, the tier-up feedback and
 * {@link StablehandEvents#BOND_GAINED}), the tier's small speed, jump and health bonuses, and riding, measured once a
 * second. The numbers are {@link BondMath}'s. Bonds belong to horses, donkeys and mules, and only grow from the
 * horse's owner: a horse that changes hands starts again with its new owner at the next gain.
 */
public final class Bonds {
    private static final Identifier SPEED = VillageBlocks.id("bond_speed"), JUMP = VillageBlocks.id("bond_jump"),
            HEALTH = VillageBlocks.id("bond_health"), RIDER = VillageBlocks.id("rider_speed");
    /** More than this many blocks between two samples a second apart is a teleport, not riding. */
    private static final double MOST_IN_A_SECOND = 30;
    /** Who is riding which horse, and where the horse was at the last sample. */
    private static final Map<UUID, Ride> RIDES = new HashMap<>();
    private record Ride(UUID horse, ResourceKey<Level> dimension, Vec3 at) {}

    /** Horses, donkeys and mules bond; camels, llamas and undead horses don't. */
    public static boolean bondable(@Nullable Entity entity) { return entity instanceof Horse || entity instanceof Donkey || entity instanceof Mule; }
    /** Whether the player owns this (tamed) horse. */
    public static boolean owns(Player player, AbstractHorse horse) {
        var owner = horse.getOwnerReference();
        return horse.isTamed() && owner != null && owner.getUUID().equals(player.getUUID());
    }
    public static HorseBond bond(AbstractHorse horse) { return target(horse).getAttachedOrElse(StableData.BOND, HorseBond.NONE); }

    /** "Destrier", "Draft Horse", "Donkey", "Mule": what kind of horse this is, for messages. */
    public static String kind(AbstractHorse horse) {
        if (horse instanceof Donkey) return "Donkey";
        if (horse instanceof Mule) return "Mule";
        return Horses.breed(horse).map(Breeds::name).orElse("Horse");
    }
    /** The horse's own name, or null when it has none. */
    public static @Nullable String customName(AbstractHorse horse) { return horse.hasCustomName() ? horse.getCustomName().getString() : null; }

    /**
     * One gain from {@code player} (who must own the horse): {@code amount} is blocks ridden or API points. Reports
     * {@code label} (or the source's own label) to {@link StablehandEvents#BOND_GAINED}. Returns the points added.
     */
    public static int gain(AbstractHorse horse, ServerPlayer player, BondMath.Source source, double amount, @Nullable String label) {
        if (!bondable(horse) || !owns(player, horse) || !(horse.level() instanceof ServerLevel level)) return 0;
        var before = bond(horse);
        String partner = player.getStringUUID();
        double multiplier = BondMath.multiplier(source, source == BondMath.Source.RIDE_BLOCKS ? bondRide(horse) : 1,
                StablehandEvents.ridingBonus(player, StablehandEvents.Aspect.BOND_GAIN));
        var after = BondMath.gain(before, partner, source, VillageFriends.day(level), multiplier, amount);
        if (after.equals(before)) return 0;
        target(horse).setAttached(StableData.BOND, after);
        int gained = BondMath.gained(before, after), was = BondMath.tierBefore(before, partner), now = BondMath.tier(after.points());
        if (BondMath.tier(before.points()) != now) refresh(horse);
        if (gained > 0) StablehandEvents.BOND_GAINED.invoker().onBondGained(player, horse, label == null ? source.label() : label, gained, was, now);
        if (now > was) closer(horse, player, level, was, now);
        return gained;
    }

    /** The tier went up: a line on the action bar, hearts and the horse's own voice; at Loyal, word of the whistle. */
    private static void closer(AbstractHorse horse, ServerPlayer player, ServerLevel level, int was, int now) {
        String name = customName(horse), kind = kind(horse);
        player.sendSystemMessage(Component.literal(BondMath.trustLine(name, kind, now)), true);
        if (was < BondMath.WHISTLE_TIER && now >= BondMath.WHISTLE_TIER) player.sendSystemMessage(Component.literal(BondMath.whistleLine(name, kind)));
        level.sendParticles(ParticleTypes.HEART, horse.getX(), horse.getY() + horse.getBbHeight(), horse.getZ(), 5, .5, .3, .5, 0);
        horse.playAmbientSound();
    }

    /** How much faster riding grows the bond with the tack in the horse's saddle slot (a Bridle 1.5, anything else 1). */
    public static double bondRide(AbstractHorse horse) {
        var saddle = horse.getItemBySlot(EquipmentSlot.SADDLE);
        if (saddle.isEmpty()) return 1;
        var id = BuiltInRegistries.ITEM.getKey(saddle.getItem());
        return id.getNamespace().equals("villagefriends") ? StableTable.gear(id.getPath()).map(StableTable.Gear::bondRide).orElse(1.0) : 1;
    }

    // -- tier bonuses ----------------------------------------------------------------------------------------

    /** Puts the tier's speed, jump and health bonuses on the horse (transient: refreshed whenever it loads). */
    public static void refresh(AbstractHorse horse) {
        if (!bondable(horse)) return;
        int tier = BondMath.tier(bond(horse).points());
        modifier(horse, Attributes.MOVEMENT_SPEED, SPEED, BondMath.speedBonus(tier), AttributeModifier.Operation.ADD_MULTIPLIED_BASE);
        modifier(horse, Attributes.JUMP_STRENGTH, JUMP, BondMath.jumpBonus(tier), AttributeModifier.Operation.ADD_MULTIPLIED_BASE);
        modifier(horse, Attributes.MAX_HEALTH, HEALTH, BondMath.healthBonus(tier), AttributeModifier.Operation.ADD_VALUE);
    }
    /**
     * A bonded horse loaded: its tier's bonuses go back on. They are transient, so vanilla clamped the saved health to the
     * maximum without them; a horse that loads exactly at that maximum was at least that healthy when it was saved, so it
     * is filled up to the bonus again (otherwise a Devoted horse would lose its bonus hearts every time it reloads).
     */
    public static void loaded(Entity entity) {
        if (!(entity instanceof AbstractHorse horse) || !bondable(horse) || bond(horse).points() <= 0) return;
        boolean full = horse.getHealth() >= horse.getMaxHealth();
        refresh(horse);
        if (full && horse.isAlive()) horse.setHealth(horse.getMaxHealth());
    }

    private static void modifier(LivingEntity entity, Holder<Attribute> attribute, Identifier id, double amount, AttributeModifier.Operation operation) {
        var instance = entity.getAttribute(attribute);
        if (instance == null) return;
        if (amount == 0) instance.removeModifier(id);
        else instance.addOrUpdateTransientModifier(new AttributeModifier(id, amount, operation));
    }

    // -- riding ------------------------------------------------------------------------------------------------

    /**
     * Once a second: every player steering a horse grows its bond by the distance it covered (if they own it), and the
     * Riding skill's speed bonus (an add-on's {@code RIDING_BONUS}) rides along as a modifier that leaves with them.
     */
    public static void tick(MinecraftServer server) {
        if (server.getTickCount() % 20 != 0) return;
        var riding = new HashSet<UUID>();
        for (var player : server.getPlayerList().getPlayers()) {
            if (!(player.getVehicle() instanceof AbstractHorse horse) || horse.getControllingPassenger() != player) continue;
            riding.add(player.getUUID());
            var last = RIDES.get(player.getUUID());
            if (last != null && !last.horse().equals(horse.getUUID())) unseat(server, last);
            modifier(horse, Attributes.MOVEMENT_SPEED, RIDER, StablehandEvents.ridingBonus(player, StablehandEvents.Aspect.HORSE_SPEED),
                    AttributeModifier.Operation.ADD_MULTIPLIED_BASE);
            if (last != null && last.horse().equals(horse.getUUID()) && last.dimension() == horse.level().dimension()) {
                double moved = horse.position().subtract(last.at()).horizontalDistance();
                if (moved > 0 && moved <= MOST_IN_A_SECOND) gain(horse, player, BondMath.Source.RIDE_BLOCKS, moved, null);
            }
            RIDES.put(player.getUUID(), new Ride(horse.getUUID(), horse.level().dimension(), horse.position()));
        }
        RIDES.entrySet().removeIf(e -> {
            if (riding.contains(e.getKey())) return false;
            unseat(server, e.getValue());
            return true;
        });
    }

    /** The rider left the horse: its rider modifier goes with them. */
    private static void unseat(MinecraftServer server, Ride ride) {
        var level = server.getLevel(ride.dimension());
        if (level != null && level.getEntity(ride.horse()) instanceof AbstractHorse horse) modifier(horse, Attributes.MOVEMENT_SPEED, RIDER, 0, AttributeModifier.Operation.ADD_MULTIPLIED_BASE);
    }

    public static void left(ServerPlayer player, MinecraftServer server) {
        var ride = RIDES.remove(player.getUUID());
        if (ride != null) unseat(server, ride);
    }

    public static void clear() { RIDES.clear(); }

    private Bonds() {}
}
