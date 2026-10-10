package dev.villagefriends.stable.data;

import com.mojang.serialization.Codec;
import dev.villagefriends.VillageBlocks;
import java.util.Objects;
import net.fabricmc.fabric.api.attachment.v1.AttachmentRegistry;
import net.fabricmc.fabric.api.attachment.v1.AttachmentSyncPredicate;
import net.fabricmc.fabric.api.attachment.v1.AttachmentType;

/**
 * Everything Stablehand saves on entities, as Fabric attachments (read and write them through
 * {@code VillageFriends.target(entity)}):
 * <ul>
 * <li>{@link #BREED} on a {@code Horse}: its breed and coat, synced to every client for the coat render hook.</li>
 * <li>{@link #BOND} on any {@code AbstractHorse}: the bond with its owner.</li>
 * <li>{@link #STALL} on any {@code AbstractHorse}: its stall, keeper and theft flags.</li>
 * <li>{@link #MOUNT_ORDER} on a {@code Villager}: why a resident is riding ("patrol", "companion" or "caravan").</li>
 * </ul>
 */
public final class StableData {
    public static final AttachmentType<HorseBreed> BREED = AttachmentRegistry.create(VillageBlocks.id("horse_breed"),
            b -> b.persistent(HorseBreed.CODEC).syncWith(HorseBreed.STREAM_CODEC, AttachmentSyncPredicate.all()));
    public static final AttachmentType<HorseBond> BOND = AttachmentRegistry.create(VillageBlocks.id("horse_bond"), b -> b.persistent(HorseBond.CODEC));
    public static final AttachmentType<StallHome> STALL = AttachmentRegistry.create(VillageBlocks.id("horse_stall"), b -> b.persistent(StallHome.CODEC));
    public static final AttachmentType<String> MOUNT_ORDER = AttachmentRegistry.create(VillageBlocks.id("mount_order"), b -> b.persistent(Codec.STRING));

    /**
     * Touches every attachment during mod initialization: a synced attachment type has to exist before a
     * player joins, or the client never learns about it (the same reason {@code Homesteads.register} does this).
     */
    public static void register() {
        Objects.requireNonNull(BREED); Objects.requireNonNull(BOND); Objects.requireNonNull(STALL); Objects.requireNonNull(MOUNT_ORDER);
    }

    private StableData() {}
}
