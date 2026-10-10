package dev.villagefriends.fishing;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import dev.villagefriends.social.Calendar;
import io.netty.buffer.ByteBuf;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Comparator;
import java.util.List;
import java.util.Random;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;

/**
 * The village fishing contest: once a season, on the 12th, every village holds one. Fishing runs from 6:00 to
 * 16:30 (anything caught in or near the village counts, by players and by the residents who enter); at 17:00 the
 * tavern keeper reads out the results at the tavern and hands out the prizes. The biggest single fish wins.
 * Pure: the calendar, the hours, the standings and the prizes.
 */
public final class Contest {
    public static final int DAY_OF_SEASON = 12, OPENS = 0, CLOSES = 10500, RESULTS = 11000;

    public enum Phase { NONE, OPEN, WEIGH_IN, OVER }

    public static boolean contestDay(long day) { return Calendar.dayOfSeason(day) == DAY_OF_SEASON; }
    /** Days until the next contest: 0 on the day itself. */
    public static int daysUntil(long day) { return Math.floorMod(DAY_OF_SEASON - Calendar.dayOfSeason(day), Calendar.SEASON_DAYS); }
    /** Where the day is, for a contest: {@code time} in ticks (0 = 6:00). */
    public static Phase phase(long day, int time) {
        if (!contestDay(day)) return Phase.NONE;
        int t = Math.floorMod(time, 24000);
        return t < CLOSES ? Phase.OPEN : t < RESULTS ? Phase.WEIGH_IN : Phase.OVER;
    }
    /** "Summer 12", the next contest's date. */
    public static String nextDate(long day) { return Calendar.date(day + daysUntil(day)); }

    /** One entrant's best fish: {@code key} is a player's UUID or a resident's id. */
    public record Entry(String key, String name, boolean player, String fish, int size) {
        public static final Codec<Entry> CODEC = RecordCodecBuilder.create(i -> i.group(
                Codec.STRING.fieldOf("key").forGetter(Entry::key), Codec.STRING.fieldOf("name").forGetter(Entry::name),
                Codec.BOOL.fieldOf("player").forGetter(Entry::player), Codec.STRING.fieldOf("fish").forGetter(Entry::fish),
                Codec.INT.fieldOf("size").forGetter(Entry::size)).apply(i, Entry::new));
        public static final StreamCodec<ByteBuf, Entry> STREAM_CODEC = StreamCodec.composite(
                ByteBufCodecs.STRING_UTF8, Entry::key, ByteBufCodecs.STRING_UTF8, Entry::name, ByteBufCodecs.BOOL, Entry::player,
                ByteBufCodecs.STRING_UTF8, Entry::fish, ByteBufCodecs.VAR_INT, Entry::size, Entry::new);
    }

    /** Biggest first; ties go to whoever landed theirs first. */
    public static List<Entry> add(List<Entry> standings, Entry entry) {
        var out = new ArrayList<Entry>();
        boolean replaced = false, kept = false;
        for (var e : standings) {
            if (!e.key().equals(entry.key())) { out.add(e); continue; }
            if (entry.size() > e.size()) { replaced = true; } else { out.add(e); kept = true; }
        }
        if (replaced || !kept) out.add(entry);
        out.sort(Comparator.comparingInt(Entry::size).reversed());
        return List.copyOf(out);
    }
    /** 1 for the winner; 0 if they haven't entered. */
    public static int place(List<Entry> standings, String key) {
        for (int i = 0; i < standings.size(); i++) if (standings.get(i).key().equals(key)) return i + 1;
        return 0;
    }

    /** A prize: an item id and how many. */
    public record Prize(String item, int count) {}
    public static List<Prize> prizes(int place) {
        return switch (place) {
            case 1 -> List.of(new Prize("villagefriends:anglers_rod", 1), new Prize("minecraft:emerald", 8));
            case 2 -> List.of(new Prize("minecraft:emerald", 6), new Prize("villagefriends:legend_lure", 1));
            case 3 -> List.of(new Prize("minecraft:emerald", 3), new Prize("villagefriends:glow_bait", 8));
            default -> List.of();
        };
    }
    public static String ordinal(int place) {
        return switch (place) { case 1 -> "1st"; case 2 -> "2nd"; case 3 -> "3rd"; default -> place + "th"; };
    }

    /**
     * A resident's catch for the contest: the best of a few casts at the village's water, with a little
     * skill ({@code luck}) for fishermen.
     */
    public static Entry residentCatch(String id, String name, Collection<Fish> table, Spot spot, int luck, Random random) {
        Fish best = null; int bestSize = 0;
        var odds = new Catches.Odds(luck, null, null, Gear.Rod.PLAIN);
        for (int i = 0; i < 3; i++) {
            var f = Catches.pick(table, spot, odds, random);
            if (f == null || f.legendary()) continue;
            int size = Catches.size(f, random, luck, false);
            if (size > bestSize) { best = f; bestSize = size; }
        }
        return best == null ? null : new Entry(id, name, false, best.id(), bestSize);
    }

    private Contest() {}
}
