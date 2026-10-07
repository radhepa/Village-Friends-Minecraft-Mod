package dev.villagefriends;

import java.util.ArrayList;
import java.util.List;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.Identifier;

/**
 * A page of the Village Ledger: everyone who lives in a village, the latest news, and (when one
 * resident is in focus) their story and how they feel about each neighbor.
 */
public record LedgerPayload(String village, String villageName, long day, String focus, List<Entry> residents, List<String> news, Detail detail)
        implements CustomPacketPayload {
    public static final int MAX_RESIDENTS = 256, MAX_LINES = 32;
    /** One resident's line: {@code level} is the reader's friendship level with them, or -1 if they haven't met. */
    public record Entry(String id, String name, String job, String status, boolean adult, int level, String note, int entityId, String gender) {}
    /** How the focused resident feels about one neighbor. */
    public record Tie(String id, String name, int affinity, String label, boolean family) {}
    public record Detail(String id, List<String> about, List<Tie> ties) {
        public static final Detail NONE = new Detail("", List.of(), List.of());
    }
    public static final Type<LedgerPayload> TYPE = new Type<>(Identifier.fromNamespaceAndPath("villagefriends", "ledger"));
    public static final StreamCodec<FriendlyByteBuf, LedgerPayload> CODEC = StreamCodec.of(LedgerPayload::write, LedgerPayload::read);

    private static void write(FriendlyByteBuf buf, LedgerPayload value) {
        buf.writeUtf(value.village, 128); buf.writeUtf(value.villageName, 64); buf.writeVarLong(value.day); buf.writeUtf(value.focus, 64);
        buf.writeVarInt(Math.min(MAX_RESIDENTS, value.residents.size()));
        for (var e : value.residents.subList(0, Math.min(MAX_RESIDENTS, value.residents.size()))) {
            buf.writeUtf(e.id, 64); buf.writeUtf(e.name, 128); buf.writeUtf(e.job, 64); buf.writeUtf(e.status, 16); buf.writeBoolean(e.adult);
            buf.writeVarInt(e.level + 1); buf.writeUtf(e.note, 160); buf.writeVarInt(e.entityId + 1); buf.writeUtf(e.gender, 16);
        }
        lines(buf, value.news);
        buf.writeUtf(value.detail.id, 64); lines(buf, value.detail.about);
        buf.writeVarInt(Math.min(MAX_RESIDENTS, value.detail.ties.size()));
        for (var t : value.detail.ties.subList(0, Math.min(MAX_RESIDENTS, value.detail.ties.size()))) {
            buf.writeUtf(t.id, 64); buf.writeUtf(t.name, 128); buf.writeVarInt(t.affinity + 100); buf.writeUtf(t.label, 64); buf.writeBoolean(t.family);
        }
    }
    private static LedgerPayload read(FriendlyByteBuf buf) {
        String village = buf.readUtf(128), name = buf.readUtf(64); long day = buf.readVarLong(); String focus = buf.readUtf(64);
        var residents = new ArrayList<Entry>();
        for (int i = 0, n = count(buf, MAX_RESIDENTS); i < n; i++)
            residents.add(new Entry(buf.readUtf(64), buf.readUtf(128), buf.readUtf(64), buf.readUtf(16), buf.readBoolean(), buf.readVarInt() - 1, buf.readUtf(160), buf.readVarInt() - 1, buf.readUtf(16)));
        var news = readLines(buf);
        String id = buf.readUtf(64); var about = readLines(buf);
        var ties = new ArrayList<Tie>();
        for (int i = 0, n = count(buf, MAX_RESIDENTS); i < n; i++)
            ties.add(new Tie(buf.readUtf(64), buf.readUtf(128), buf.readVarInt() - 100, buf.readUtf(64), buf.readBoolean()));
        return new LedgerPayload(village, name, day, focus, List.copyOf(residents), news, new Detail(id, about, List.copyOf(ties)));
    }
    private static void lines(FriendlyByteBuf buf, List<String> lines) {
        buf.writeVarInt(Math.min(MAX_LINES, lines.size()));
        for (var line : lines.subList(0, Math.min(MAX_LINES, lines.size()))) buf.writeUtf(line, 256);
    }
    private static List<String> readLines(FriendlyByteBuf buf) {
        var lines = new ArrayList<String>();
        for (int i = 0, n = count(buf, MAX_LINES); i < n; i++) lines.add(buf.readUtf(256));
        return List.copyOf(lines);
    }
    private static int count(FriendlyByteBuf buf, int max) {
        int n = buf.readVarInt(); if (n < 0 || n > max) throw new IllegalArgumentException("Invalid ledger size"); return n;
    }
    @Override public Type<? extends CustomPacketPayload> type() { return TYPE; }
}
