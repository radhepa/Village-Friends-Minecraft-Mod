package dev.villagefriends;

import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.Identifier;

/** Something done at a notice board: "accept", "abandon" or "claim" a notice, or open the "ledger". */
public record NoticeActionPayload(String village, String notice, String action, long pos) implements CustomPacketPayload {
    public static final Type<NoticeActionPayload> TYPE = new Type<>(Identifier.fromNamespaceAndPath("villagefriends", "notice_action"));
    public static final StreamCodec<FriendlyByteBuf, NoticeActionPayload> CODEC = StreamCodec.of(
            (buf, value) -> { buf.writeUtf(value.village, 128); buf.writeUtf(value.notice, 32); buf.writeUtf(value.action, 16); buf.writeLong(value.pos); },
            buf -> new NoticeActionPayload(buf.readUtf(128), buf.readUtf(32), buf.readUtf(16), buf.readLong()));
    @Override public Type<? extends CustomPacketPayload> type() { return TYPE; }
}
