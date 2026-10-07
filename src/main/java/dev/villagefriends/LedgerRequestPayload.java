package dev.villagefriends;

import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.Identifier;

/** Asks for a Village Ledger page about one resident ({@code focus}) of a village on the player's level. */
public record LedgerRequestPayload(String village, String focus) implements CustomPacketPayload {
    public static final Type<LedgerRequestPayload> TYPE = new Type<>(Identifier.fromNamespaceAndPath("villagefriends", "ledger_request"));
    public static final StreamCodec<FriendlyByteBuf, LedgerRequestPayload> CODEC = StreamCodec.of(
            (buf, value) -> { buf.writeUtf(value.village, 128); buf.writeUtf(value.focus, 64); },
            buf -> new LedgerRequestPayload(buf.readUtf(128), buf.readUtf(64)));
    @Override public Type<? extends CustomPacketPayload> type() { return TYPE; }
}
