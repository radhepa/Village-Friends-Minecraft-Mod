package dev.villagefriends.pet;

import java.util.UUID;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.Identifier;

/**
 * One pet card's worth of state: who the pet is, who they belong to, how old they are, what they
 * love, a line about them and how fond they are of the player looking at them (0 to 100).
 */
public record PetPayload(int entityId, UUID petId, String name, String species, String stage, String breed, String personality,
        String owner, String ownerDetail, String age, String adopted, String game, String treat, String line, String status,
        int fondness, String fondnessLabel, float health, float maxHealth, boolean opening, String emote, String trick)
        implements CustomPacketPayload {
    public static final Type<PetPayload> TYPE = new Type<>(Identifier.fromNamespaceAndPath("villagefriends", "pet_card"));
    public static final StreamCodec<FriendlyByteBuf, PetPayload> CODEC = StreamCodec.of(
            (buf, v) -> {
                buf.writeVarInt(v.entityId); buf.writeUUID(v.petId);
                buf.writeUtf(v.name, 128); buf.writeUtf(v.species, 16); buf.writeUtf(v.stage, 64); buf.writeUtf(v.breed, 64);
                buf.writeUtf(v.personality, 64); buf.writeUtf(v.owner, 128); buf.writeUtf(v.ownerDetail, 256);
                buf.writeUtf(v.age, 64); buf.writeUtf(v.adopted, 128); buf.writeUtf(v.game, 64); buf.writeUtf(v.treat, 64);
                buf.writeUtf(v.line, 1024); buf.writeUtf(v.status, 256);
                buf.writeVarInt(v.fondness); buf.writeUtf(v.fondnessLabel, 64);
                buf.writeFloat(v.health); buf.writeFloat(v.maxHealth); buf.writeBoolean(v.opening);
                buf.writeUtf(v.emote, 16); buf.writeUtf(v.trick, 32);
            },
            buf -> new PetPayload(buf.readVarInt(), buf.readUUID(), buf.readUtf(128), buf.readUtf(16), buf.readUtf(64), buf.readUtf(64),
                    buf.readUtf(64), buf.readUtf(128), buf.readUtf(256), buf.readUtf(64), buf.readUtf(128), buf.readUtf(64), buf.readUtf(64),
                    buf.readUtf(1024), buf.readUtf(256), Math.clamp(buf.readVarInt(), 0, PetKeeping.MAX_FONDNESS), buf.readUtf(64),
                    buf.readFloat(), buf.readFloat(), buf.readBoolean(), buf.readUtf(16), buf.readUtf(32)));
    @Override public Type<? extends CustomPacketPayload> type() { return TYPE; }
    public boolean cat() { return species.equals(PetKeeping.CAT); }
}
