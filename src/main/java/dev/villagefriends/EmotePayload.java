package dev.villagefriends;

import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.Identifier;

/** Pops an emote bubble above a resident after {@code delay} ticks. */
public record EmotePayload(int entityId, String emote, int delay) implements CustomPacketPayload {
    public static final Type<EmotePayload> TYPE = new Type<>(Identifier.fromNamespaceAndPath("villagefriends", "emote"));
    public static final StreamCodec<FriendlyByteBuf, EmotePayload> CODEC = StreamCodec.of(
            (buf, value) -> { buf.writeVarInt(value.entityId); buf.writeUtf(value.emote, 16); buf.writeVarInt(value.delay); },
            buf -> new EmotePayload(buf.readVarInt(), buf.readUtf(16), Math.clamp(buf.readVarInt(), 0, 200)));
    @Override public Type<? extends CustomPacketPayload> type() { return TYPE; }
}
