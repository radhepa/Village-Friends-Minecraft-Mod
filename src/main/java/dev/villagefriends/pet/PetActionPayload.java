package dev.villagefriends.pet;

import java.util.UUID;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.Identifier;

/** A button on a pet's card: {@code pat} or {@code treat}. */
public record PetActionPayload(int entityId, UUID petId, String action) implements CustomPacketPayload {
    public static final Type<PetActionPayload> TYPE = new Type<>(Identifier.fromNamespaceAndPath("villagefriends", "pet_action"));
    public static final StreamCodec<FriendlyByteBuf, PetActionPayload> CODEC = StreamCodec.of(
            (buf, value) -> { buf.writeVarInt(value.entityId); buf.writeUUID(value.petId); buf.writeUtf(value.action, 32); },
            buf -> new PetActionPayload(buf.readVarInt(), buf.readUUID(), buf.readUtf(32)));
    @Override public Type<? extends CustomPacketPayload> type() { return TYPE; }
}
