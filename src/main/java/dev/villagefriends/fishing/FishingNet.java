package dev.villagefriends.fishing;

import java.util.List;
import net.fabricmc.fabric.api.networking.v1.PayloadTypeRegistry;
import net.fabricmc.fabric.api.networking.v1.ServerPlayNetworking;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.server.level.ServerPlayer;

/** Tall Tales Fishing's packets: the minigame (start, end, the player's result), the journal and the contest board. */
public final class FishingNet {
    /** A fish is on: play the minigame. The fish itself stays a surprise; only how it fights is sent. */
    public record MinigameStart(int hook, String behavior, int difficulty, float zone, float fishSpeed, float gain, float drain,
                                boolean treasure, boolean legendary, long seed) implements CustomPacketPayload {
        public static final Type<MinigameStart> TYPE = new Type<>(Fishing.id("minigame_start"));
        public static final StreamCodec<FriendlyByteBuf, MinigameStart> CODEC = StreamCodec.of((buf, v) -> {
            buf.writeVarInt(v.hook); buf.writeUtf(v.behavior, 16); buf.writeVarInt(v.difficulty);
            buf.writeFloat(v.zone); buf.writeFloat(v.fishSpeed); buf.writeFloat(v.gain); buf.writeFloat(v.drain);
            buf.writeBoolean(v.treasure); buf.writeBoolean(v.legendary); buf.writeLong(v.seed);
        }, buf -> new MinigameStart(buf.readVarInt(), buf.readUtf(16), buf.readVarInt(), buf.readFloat(), buf.readFloat(), buf.readFloat(),
                buf.readFloat(), buf.readBoolean(), buf.readBoolean(), buf.readLong()));
        @Override public Type<? extends CustomPacketPayload> type() { return TYPE; }
        public Minigame.Tuning tuning() { return new Minigame.Tuning(zone, fishSpeed, gain, drain, treasure); }
    }
    /** The line went slack (the rod was put away, the hook is gone): stop the minigame. */
    public record MinigameEnd() implements CustomPacketPayload {
        public static final Type<MinigameEnd> TYPE = new Type<>(Fishing.id("minigame_end"));
        public static final StreamCodec<FriendlyByteBuf, MinigameEnd> CODEC = StreamCodec.unit(new MinigameEnd());
        @Override public Type<? extends CustomPacketPayload> type() { return TYPE; }
    }
    /** How the minigame went: caught or not, perfect (never out of the zone), the treasure collected. */
    public record MinigameResult(boolean won, boolean perfect, boolean treasure) implements CustomPacketPayload {
        public static final Type<MinigameResult> TYPE = new Type<>(Fishing.id("minigame_result"));
        public static final StreamCodec<FriendlyByteBuf, MinigameResult> CODEC = StreamCodec.composite(
                ByteBufCodecs.BOOL, MinigameResult::won, ByteBufCodecs.BOOL, MinigameResult::perfect, ByteBufCodecs.BOOL, MinigameResult::treasure,
                MinigameResult::new);
        @Override public Type<? extends CustomPacketPayload> type() { return TYPE; }
    }
    /** Open the angler's journal (its contents are the player's synced {@link Fishing#JOURNAL}). */
    public record OpenJournal() implements CustomPacketPayload {
        public static final Type<OpenJournal> TYPE = new Type<>(Fishing.id("open_journal"));
        public static final StreamCodec<FriendlyByteBuf, OpenJournal> CODEC = StreamCodec.unit(new OpenJournal());
        @Override public Type<? extends CustomPacketPayload> type() { return TYPE; }
    }
    /**
     * The contest board in the corner of the screen while a player is at a village on contest day: the
     * village, what's happening ("Fishing until 16:30", "Weigh-in at the tavern at 17:00"), the top five and
     * the player's own place. {@code show} false hides it.
     */
    public record ContestBoard(boolean show, String village, String status, List<Contest.Entry> top, int place, String best) implements CustomPacketPayload {
        public static final Type<ContestBoard> TYPE = new Type<>(Fishing.id("contest_board"));
        public static final StreamCodec<RegistryFriendlyByteBuf, ContestBoard> CODEC = StreamCodec.composite(
                ByteBufCodecs.BOOL, ContestBoard::show, ByteBufCodecs.STRING_UTF8, ContestBoard::village, ByteBufCodecs.STRING_UTF8, ContestBoard::status,
                Contest.Entry.STREAM_CODEC.apply(ByteBufCodecs.list(8)), ContestBoard::top, ByteBufCodecs.VAR_INT, ContestBoard::place,
                ByteBufCodecs.STRING_UTF8, ContestBoard::best, ContestBoard::new);
        public static final ContestBoard HIDDEN = new ContestBoard(false, "", "", List.of(), 0, "");
        @Override public Type<? extends CustomPacketPayload> type() { return TYPE; }
    }

    static void register() {
        PayloadTypeRegistry.clientboundPlay().register(MinigameStart.TYPE, MinigameStart.CODEC);
        PayloadTypeRegistry.clientboundPlay().register(MinigameEnd.TYPE, MinigameEnd.CODEC);
        PayloadTypeRegistry.clientboundPlay().register(OpenJournal.TYPE, OpenJournal.CODEC);
        PayloadTypeRegistry.clientboundPlay().register(ContestBoard.TYPE, ContestBoard.CODEC);
        PayloadTypeRegistry.serverboundPlay().register(MinigameResult.TYPE, MinigameResult.CODEC);
        ServerPlayNetworking.registerGlobalReceiver(MinigameResult.TYPE, (payload, context) -> Angling.result(context.player(), payload));
    }

    public static void openJournal(ServerPlayer p) { ServerPlayNetworking.send(p, new OpenJournal()); }

    private FishingNet() {}
}
