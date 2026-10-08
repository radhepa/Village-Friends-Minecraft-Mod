package dev.villagefriends.rpg;

import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;

/** Sheet buttons and keys: "spend" (arg = attribute id), "respec", "abandon" (arg = quest id), "ability" (arg = family id). */
public record RpgActionPayload(String action, String arg) implements CustomPacketPayload {
    public static final Type<RpgActionPayload> TYPE = new Type<>(Rpg.id("action"));
    public static final StreamCodec<FriendlyByteBuf, RpgActionPayload> CODEC = StreamCodec.of(
            (buf, p) -> { buf.writeUtf(p.action, 32); buf.writeUtf(p.arg, 128); },
            buf -> new RpgActionPayload(buf.readUtf(32), buf.readUtf(128)));
    @Override public Type<? extends CustomPacketPayload> type() { return TYPE; }
}
