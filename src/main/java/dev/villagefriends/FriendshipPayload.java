package dev.villagefriends;

import java.util.UUID;
import java.util.List;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.Identifier;

/**
 * One conversation screen's worth of state. {@code friendLevel} is the 0-10 friendship level
 * ({@link FriendshipLevels}) and {@code level} the 0-4 tier it belongs to; {@code levelFloor} and
 * {@code nextThreshold} are the points at which the current and next level begin. {@code emote} is
 * the mood bubble the resident shows with this line.
 */
public record FriendshipPayload(int entityId, UUID villagerId, String name, String profession,
        String personality, int points, int level, int nextThreshold, int giftsLeft,
        boolean talkReady, boolean canTrade, String dialogue, String status, String giftHint, boolean opening,
        String tab, String journal, List<Choice> choices, String trust,
        int friendLevel, String levelName, int levelFloor, String goal, boolean levelUp, String emote, String home, String family)
        implements CustomPacketPayload {
    public static final int MAX_CHOICES = 6;
    /** A reply the player can choose; {@code hint} explains a locked one. */
    public record Choice(String id, String label, boolean enabled, String hint) {
        public Choice(String id, String label, boolean enabled) { this(id, label, enabled, ""); }
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
                for (var choice : value.choices) { buf.writeUtf(choice.id, 64); buf.writeUtf(choice.label, 64); buf.writeBoolean(choice.enabled); buf.writeUtf(choice.hint, 128); }
                buf.writeVarInt(value.friendLevel); buf.writeUtf(value.levelName, 64); buf.writeVarInt(value.levelFloor);
                buf.writeUtf(value.goal, 256); buf.writeBoolean(value.levelUp); buf.writeUtf(value.emote, 16);
                buf.writeUtf(value.home, 64); buf.writeUtf(value.family, 512);
            },
            buf -> {
                int entity = buf.readVarInt(); UUID id = buf.readUUID(); String name = buf.readUtf(256), job = buf.readUtf(128), personality = buf.readUtf(64);
                int points = buf.readVarInt(), level = buf.readVarInt(), next = buf.readVarInt(), gifts = buf.readVarInt();
                boolean talk = buf.readBoolean(), trade = buf.readBoolean(); String dialogue = buf.readUtf(8192), status = buf.readUtf(256), hint = buf.readUtf(512);
                boolean opening = buf.readBoolean(); String tab = buf.readUtf(32), journal = buf.readUtf(8192), trust = buf.readUtf(64);
                int count = buf.readVarInt(); if (count < 0 || count > MAX_CHOICES) throw new IllegalArgumentException("Invalid choice count");
                var choices = new java.util.ArrayList<Choice>();
                for (int i = 0; i < count; i++) choices.add(new Choice(buf.readUtf(64), buf.readUtf(64), buf.readBoolean(), buf.readUtf(128)));
                int friendLevel = buf.readVarInt(); String levelName = buf.readUtf(64); int floor = buf.readVarInt();
                String goal = buf.readUtf(256); boolean levelUp = buf.readBoolean(); String emote = buf.readUtf(16);
                String home = buf.readUtf(64), family = buf.readUtf(512);
                return new FriendshipPayload(entity, id, name, job, personality, points, level, next, gifts, talk, trade, dialogue, status, hint, opening, tab, journal,
                        List.copyOf(choices), trust, friendLevel, levelName, floor, goal, levelUp, emote, home, family);
            });
    @Override public Type<? extends CustomPacketPayload> type() { return TYPE; }
}
