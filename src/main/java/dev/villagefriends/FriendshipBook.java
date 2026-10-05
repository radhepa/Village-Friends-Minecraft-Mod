package dev.villagefriends;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

public record FriendshipBook(Map<String, FriendshipState> relationships) {
    public static final Codec<FriendshipState> STATE_CODEC = RecordCodecBuilder.create(instance -> instance.group(
            Codec.INT.fieldOf("points").forGetter(FriendshipState::points),
            Codec.LONG.optionalFieldOf("talk_day", -1L).forGetter(FriendshipState::talkDay),
            Codec.LONG.optionalFieldOf("gift_day", -1L).forGetter(FriendshipState::giftDay),
            Codec.INT.optionalFieldOf("gifts_today", 0).forGetter(FriendshipState::giftsToday),
            Codec.STRING.optionalFieldOf("last_gift", "").forGetter(FriendshipState::lastGift)
    ).apply(instance, FriendshipState::new));
    public static final Codec<FriendshipBook> CODEC = Codec.unboundedMap(Codec.STRING, STATE_CODEC)
            .xmap(FriendshipBook::new, FriendshipBook::relationships);

    public FriendshipBook { relationships = Map.copyOf(relationships); }
    public static FriendshipBook empty() { return new FriendshipBook(Map.of()); }
    public FriendshipState get(UUID player) { return relationships.getOrDefault(player.toString(), FriendshipState.NEW); }

    public FriendshipBook with(UUID player, FriendshipState state) {
        var updated = new HashMap<>(relationships);
        updated.put(player.toString(), state);
        return new FriendshipBook(updated);
    }
}
