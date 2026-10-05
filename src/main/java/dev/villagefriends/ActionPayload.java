package dev.villagefriends;

import java.util.UUID;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.Identifier;

public record ActionPayload(int entityId, UUID villagerId, String action) implements CustomPacketPayload {
    public static final Type<ActionPayload> TYPE = new Type<>(Identifier.fromNamespaceAndPath("villagefriends", "action"));
    public static final StreamCodec<FriendlyByteBuf, ActionPayload> CODEC = StreamCodec.of(
            (buf, value) -> { buf.writeVarInt(value.entityId); buf.writeUUID(value.villagerId); buf.writeUtf(value.action, 64); },
            buf -> new ActionPayload(buf.readVarInt(), buf.readUUID(), buf.readUtf(64)));
    @Override public Type<? extends CustomPacketPayload> type() { return TYPE; }
}
