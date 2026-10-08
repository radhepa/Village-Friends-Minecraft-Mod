package dev.villagefriends.quest;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;

/**
 * One notice pinned on a village board by a resident ({@code poster}).
 *
 * <ul>
 * <li>{@code hunt}: defeat {@code count} monsters of the group {@code target} ("zombies", "skeletons"...).</li>
 * <li>{@code fetch}: bring {@code count} of the item {@code target}.</li>
 * <li>{@code letter}: carry a sealed letter to the resident {@code target} ({@code who} by name); {@code about}
 *     is how they know each other ("friend", "family", "crush", "partner", "apology").</li>
 * <li>{@code birthday}: bring {@code count} of {@code target} for the birthday of resident {@code about} ({@code who}).</li>
 * </ul>
 *
 * {@code taker} is the UUID of the player who accepted it, or "" while it is up for grabs. Notices nobody
 * takes come down on day {@code expires}.
 */
public record Notice(String id, String kind, String poster, String posterName, String posterJob, String target, int count,
        String about, String who, Reward reward, String title, String text, long posted, long expires, String taker) {
    public static final String HUNT = "hunt", FETCH = "fetch", LETTER = "letter", BIRTHDAY = "birthday";
    /** What answering the notice earns: emeralds and a little something from the poster's trade. */
    public record Reward(int emeralds, String item, int count) {
        public static final Reward NONE = new Reward(0, "", 0);
        public static final Codec<Reward> CODEC = RecordCodecBuilder.create(i -> i.group(
                Codec.INT.optionalFieldOf("emeralds", 0).forGetter(Reward::emeralds),
                Codec.STRING.optionalFieldOf("item", "").forGetter(Reward::item),
                Codec.INT.optionalFieldOf("count", 0).forGetter(Reward::count)
        ).apply(i, Reward::new));
    }
    public static final Codec<Notice> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.STRING.fieldOf("id").forGetter(Notice::id),
            Codec.STRING.fieldOf("kind").forGetter(Notice::kind),
            Codec.STRING.fieldOf("poster").forGetter(Notice::poster),
            Codec.STRING.optionalFieldOf("poster_name", "").forGetter(Notice::posterName),
            Codec.STRING.optionalFieldOf("poster_job", "none").forGetter(Notice::posterJob),
            Codec.STRING.fieldOf("target").forGetter(Notice::target),
            Codec.INT.optionalFieldOf("count", 1).forGetter(Notice::count),
            Codec.STRING.optionalFieldOf("about", "").forGetter(Notice::about),
            Codec.STRING.optionalFieldOf("who", "").forGetter(Notice::who),
            Reward.CODEC.optionalFieldOf("reward", Reward.NONE).forGetter(Notice::reward),
            Codec.STRING.optionalFieldOf("title", "").forGetter(Notice::title),
            Codec.STRING.optionalFieldOf("text", "").forGetter(Notice::text),
            Codec.LONG.optionalFieldOf("posted", 0L).forGetter(Notice::posted),
            Codec.LONG.optionalFieldOf("expires", 0L).forGetter(Notice::expires),
            Codec.STRING.optionalFieldOf("taker", "").forGetter(Notice::taker)
    ).apply(i, Notice::new));

    public Notice {
        count = Math.max(1, count);
        taker = taker == null ? "" : taker;
        about = about == null ? "" : about;
        who = who == null ? "" : who;
    }
    public boolean taken() { return !taker.isEmpty(); }
    /** Still pinned up for anyone to take on {@code today}. */
    public boolean open(long today) { return !taken() && today < expires; }
    public Notice take(String player) { return with(player); }
    public Notice release() { return with(""); }
    private Notice with(String nextTaker) {
        return new Notice(id, kind, poster, posterName, posterJob, target, count, about, who, reward, title, text, posted, expires, nextTaker);
    }
}
