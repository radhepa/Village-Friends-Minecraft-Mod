package dev.villagefriends;

import java.util.UUID;
import java.util.List;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.Identifier;

public record FriendshipPayload(int entityId, UUID villagerId, String name, String profession,
        String personality, int points, int level, int nextThreshold, int giftsLeft,
        boolean talkReady, boolean canTrade, String dialogue, String status, String giftHint, boolean opening,
        String tab, String journal, List<Choice> choices, String trust)
        implements CustomPacketPayload {
    public record Choice(String id, String label, boolean enabled) {}
    public FriendshipPayload(int entityId, UUID villagerId, String name, String profession, String personality,
            int points, int level, int nextThreshold, int giftsLeft, boolean talkReady, boolean canTrade,
            String dialogue, String status, String giftHint, boolean opening) {
        this(entityId, villagerId, name, profession, personality, points, level, nextThreshold, giftsLeft,
                talkReady, canTrade, dialogue, status, giftHint, opening, "talk", "", List.of(
                        new Choice("chat", "How's your day?", true), new Choice("work", "Tell me about work", true),
                        new Choice("adventure", "Talk about adventures", true), new Choice("joke", "Share a joke", true)), "Comfortable");
    }
    public static final Type<FriendshipPayload> TYPE = new Type<>(Identifier.fromNamespaceAndPath("villagefriends", "conversation"));
    public static final StreamCodec<FriendlyByteBuf, FriendshipPayload> CODEC = StreamCodec.of(
            (buf, value) -> {
                buf.writeVarInt(value.entityId); buf.writeUUID(value.villagerId);
                buf.writeUtf(value.name, 256); buf.writeUtf(value.profession, 128); buf.writeUtf(value.personality, 64);
                buf.writeVarInt(value.points); buf.writeVarInt(value.level); buf.writeVarInt(value.nextThreshold);
                buf.writeVarInt(value.giftsLeft); buf.writeBoolean(value.talkReady); buf.writeBoolean(value.canTrade);
                buf.writeUtf(value.dialogue, 8192); buf.writeUtf(value.status, 256); buf.writeUtf(value.giftHint, 512);
                buf.writeBoolean(value.opening);
                buf.writeUtf(value.tab, 32); buf.writeUtf(value.journal, 8192); buf.writeUtf(value.trust, 64);
                buf.writeVarInt(value.choices.size());
                for (var choice : value.choices) { buf.writeUtf(choice.id, 64); buf.writeUtf(choice.label, 64); buf.writeBoolean(choice.enabled); }
            },
            buf -> {
                int entity = buf.readVarInt(); UUID id = buf.readUUID(); String name = buf.readUtf(256), job = buf.readUtf(128), personality = buf.readUtf(64);
                int points = buf.readVarInt(), level = buf.readVarInt(), next = buf.readVarInt(), gifts = buf.readVarInt();
                boolean talk = buf.readBoolean(), trade = buf.readBoolean(); String dialogue = buf.readUtf(8192), status = buf.readUtf(256), hint = buf.readUtf(512);
                boolean opening = buf.readBoolean(); String tab = buf.readUtf(32), journal = buf.readUtf(8192), trust = buf.readUtf(64);
                int count = buf.readVarInt(); if (count < 0 || count > 4) throw new IllegalArgumentException("Invalid choice count");
                var choices = new java.util.ArrayList<Choice>();
                for (int i = 0; i < count; i++) choices.add(new Choice(buf.readUtf(64), buf.readUtf(64), buf.readBoolean()));
                return new FriendshipPayload(entity, id, name, job, personality, points, level, next, gifts, talk, trade, dialogue, status, hint, opening, tab, journal, List.copyOf(choices), trust);
            });
    @Override public Type<? extends CustomPacketPayload> type() { return TYPE; }
}
