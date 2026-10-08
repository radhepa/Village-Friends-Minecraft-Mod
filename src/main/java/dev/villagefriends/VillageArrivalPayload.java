package dev.villagefriends;

import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.Identifier;

/** Shows the large arrival title card when a player walks into a village. */
public record VillageArrivalPayload(String village, int variant) implements CustomPacketPayload {
    public static final Type<VillageArrivalPayload> TYPE = new Type<>(Identifier.fromNamespaceAndPath("villagefriends", "village_arrival"));
    public static final StreamCodec<FriendlyByteBuf, VillageArrivalPayload> CODEC = StreamCodec.of(
            (buf, value) -> { buf.writeUtf(value.village, 64); buf.writeVarInt(value.variant); },
            buf -> new VillageArrivalPayload(buf.readUtf(64), Math.floorMod(buf.readVarInt(), VillageArrival.VARIANTS)));
    @Override public Type<? extends CustomPacketPayload> type() { return TYPE; }
}
