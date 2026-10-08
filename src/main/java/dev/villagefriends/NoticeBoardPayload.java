package dev.villagefriends;

import java.util.ArrayList;
import java.util.List;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.Identifier;

/**
 * A village notice board as the reading player sees it: the notices pinned on it, the player's own notices
 * in hand (from any village), the village's upcoming birthdays and the player's standing there.
 */
public record NoticeBoardPayload(String village, String villageName, String date, String standing, String standingHint, long pos,
        List<Card> notices, List<Task> tasks, List<String> birthdays, String message) implements CustomPacketPayload {
    public static final int MAX_CARDS = 16, MAX_TASKS = 8, MAX_BIRTHDAYS = 8;
    /**
     * One pinned notice. {@code state} is "open" (up for grabs), "mine" (accepted, not done yet), "ready"
     * (done: turn it in), or "taken" (someone else has it). {@code icon} is an item ID to draw on it.
     */
    public record Card(String id, String kind, String title, String text, String poster, String posterJob, String objective, String reward,
            String icon, String state, int progress, int count, String due) {}
    /** A notice the player has accepted, from this board or another. */
    public record Task(String village, String id, String title, String where, String progress, boolean ready, String icon) {}
    public static final Type<NoticeBoardPayload> TYPE = new Type<>(Identifier.fromNamespaceAndPath("villagefriends", "notice_board"));
    public static final StreamCodec<FriendlyByteBuf, NoticeBoardPayload> CODEC = StreamCodec.of(NoticeBoardPayload::write, NoticeBoardPayload::read);

    private static void write(FriendlyByteBuf buf, NoticeBoardPayload v) {
        buf.writeUtf(v.village, 128); buf.writeUtf(v.villageName, 64); buf.writeUtf(v.date, 96); buf.writeUtf(v.standing, 96); buf.writeUtf(v.standingHint, 160);
        buf.writeLong(v.pos);
        var cards = v.notices.subList(0, Math.min(MAX_CARDS, v.notices.size()));
        buf.writeVarInt(cards.size());
        for (var c : cards) {
            buf.writeUtf(c.id, 32); buf.writeUtf(c.kind, 16); buf.writeUtf(c.title, 96); buf.writeUtf(c.text, 600); buf.writeUtf(c.poster, 128);
            buf.writeUtf(c.posterJob, 64); buf.writeUtf(c.objective, 160); buf.writeUtf(c.reward, 160); buf.writeUtf(c.icon, 96); buf.writeUtf(c.state, 16);
            buf.writeVarInt(c.progress); buf.writeVarInt(c.count); buf.writeUtf(c.due, 64);
        }
        var tasks = v.tasks.subList(0, Math.min(MAX_TASKS, v.tasks.size()));
        buf.writeVarInt(tasks.size());
        for (var t : tasks) {
            buf.writeUtf(t.village, 128); buf.writeUtf(t.id, 32); buf.writeUtf(t.title, 96); buf.writeUtf(t.where, 96); buf.writeUtf(t.progress, 96);
            buf.writeBoolean(t.ready); buf.writeUtf(t.icon, 96);
        }
        var birthdays = v.birthdays.subList(0, Math.min(MAX_BIRTHDAYS, v.birthdays.size()));
        buf.writeVarInt(birthdays.size());
        for (var b : birthdays) buf.writeUtf(b, 128);
        buf.writeUtf(v.message, 256);
    }
    private static NoticeBoardPayload read(FriendlyByteBuf buf) {
        String village = buf.readUtf(128), name = buf.readUtf(64), date = buf.readUtf(96), standing = buf.readUtf(96), hint = buf.readUtf(160);
        long pos = buf.readLong();
        var cards = new ArrayList<Card>();
        for (int i = 0, n = count(buf, MAX_CARDS); i < n; i++)
            cards.add(new Card(buf.readUtf(32), buf.readUtf(16), buf.readUtf(96), buf.readUtf(600), buf.readUtf(128), buf.readUtf(64), buf.readUtf(160),
                    buf.readUtf(160), buf.readUtf(96), buf.readUtf(16), buf.readVarInt(), buf.readVarInt(), buf.readUtf(64)));
        var tasks = new ArrayList<Task>();
        for (int i = 0, n = count(buf, MAX_TASKS); i < n; i++)
            tasks.add(new Task(buf.readUtf(128), buf.readUtf(32), buf.readUtf(96), buf.readUtf(96), buf.readUtf(96), buf.readBoolean(), buf.readUtf(96)));
        var birthdays = new ArrayList<String>();
        for (int i = 0, n = count(buf, MAX_BIRTHDAYS); i < n; i++) birthdays.add(buf.readUtf(128));
        return new NoticeBoardPayload(village, name, date, standing, hint, pos, List.copyOf(cards), List.copyOf(tasks), List.copyOf(birthdays), buf.readUtf(256));
    }
    private static int count(FriendlyByteBuf buf, int max) {
        int n = buf.readVarInt(); if (n < 0 || n > max) throw new IllegalArgumentException("Invalid notice board size"); return n;
    }
    @Override public Type<? extends CustomPacketPayload> type() { return TYPE; }
}
