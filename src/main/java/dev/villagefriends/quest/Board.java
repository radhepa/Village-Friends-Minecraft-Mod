package dev.villagefriends.quest;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import java.util.*;

/**
 * One village's notice board: the notices pinned on it, the day it was last refreshed, and how many
 * notices each player (by UUID) has answered for this village, which earns them a standing there.
 */
public record Board(String village, List<Notice> notices, long day, int serial, Map<String, Integer> favors) {
    public static final Codec<Board> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.STRING.fieldOf("village").forGetter(Board::village),
            Notice.CODEC.listOf().optionalFieldOf("notices", List.of()).forGetter(Board::notices),
            Codec.LONG.optionalFieldOf("day", -1L).forGetter(Board::day),
            Codec.INT.optionalFieldOf("serial", 0).forGetter(Board::serial),
            Codec.unboundedMap(Codec.STRING, Codec.INT).optionalFieldOf("favors", Map.of()).forGetter(Board::favors)
    ).apply(i, Board::new));
    /** Standings in a village by notices answered: the last one is "Hero of the village". */
    public static final int[] STANDING = {0, 1, 4, 10, 20};
    private static final String[] TITLES = {"Newcomer", "Helping Hand", "Good Neighbor", "Pillar of the Community", "Hero of "};

    public Board {
        notices = List.copyOf(notices); favors = Map.copyOf(favors);
    }
    public static Board create(String village) { return new Board(village, List.of(), -1, 0, Map.of()); }

    public Notice find(String id) {
        for (var n : notices) if (n.id().equals(id)) return n;
        return null;
    }
    public List<Notice> open(long today) { return notices.stream().filter(n -> n.open(today)).toList(); }
    public int favors(String player) { return favors.getOrDefault(player, 0); }

    public Board take(String id, String player) { return replace(id, n -> n.take(player)); }
    /** Back on the board for someone else, unless its time is up. */
    public Board release(String id, long today) { return replace(id, n -> today < n.expires() ? n.release() : null); }
    public Board remove(String id) { return replace(id, n -> null); }
    private Board replace(String id, java.util.function.UnaryOperator<Notice> change) {
        var next = new ArrayList<Notice>(); boolean changed = false;
        for (var n : notices) {
            if (!n.id().equals(id)) { next.add(n); continue; }
            var updated = change.apply(n); changed = true;
            if (updated != null) next.add(updated);
        }
        return changed ? new Board(village, next, day, serial, favors) : this;
    }
    /** One more notice answered by {@code player}. */
    public Board favor(String player) {
        var next = new HashMap<>(favors); next.merge(player, 1, Integer::sum);
        return new Board(village, notices, day, serial, next);
    }

    /** 0 to 4: Newcomer, Helping Hand, Good Neighbor, Pillar of the Community, Hero of the village. */
    public static int standing(int favors) {
        int tier = 0;
        for (int i = 0; i < STANDING.length; i++) if (favors >= STANDING[i]) tier = i;
        return tier;
    }
    public static String title(int tier, String villageName) { return tier == TITLES.length - 1 ? TITLES[tier] + villageName : TITLES[tier]; }
}
