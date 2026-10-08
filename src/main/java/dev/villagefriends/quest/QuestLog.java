package dev.villagefriends.quest;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import java.util.*;

/**
 * A player's notices in hand (at most {@link #MAX}), thanks owed to them by residents who weren't around
 * when a notice was turned in at the board, and how many notices they have answered in all.
 */
public record QuestLog(List<Quest> quests, Map<String, Integer> thanks, int answered) {
    public static final int MAX = 3;
    public static final QuestLog EMPTY = new QuestLog(List.of(), Map.of(), 0);
    /** An accepted notice: which village's board it came from, and how far along it is (monsters defeated). */
    public record Quest(String village, String villageName, String dimension, Notice notice, int progress, long accepted) {
        public static final Codec<Quest> CODEC = RecordCodecBuilder.create(i -> i.group(
                Codec.STRING.fieldOf("village").forGetter(Quest::village),
                Codec.STRING.optionalFieldOf("village_name", "").forGetter(Quest::villageName),
                Codec.STRING.optionalFieldOf("dimension", "minecraft:overworld").forGetter(Quest::dimension),
                Notice.CODEC.fieldOf("notice").forGetter(Quest::notice),
                Codec.INT.optionalFieldOf("progress", 0).forGetter(Quest::progress),
                Codec.LONG.optionalFieldOf("accepted", 0L).forGetter(Quest::accepted)
        ).apply(i, Quest::new));
        public String id() { return notice.id(); }
        public boolean hunted() { return notice.kind().equals(Notice.HUNT) && progress >= notice.count(); }
        public Quest progress(int next) { return new Quest(village, villageName, dimension, notice, Math.min(next, notice.count()), accepted); }
        public boolean is(String villageId, String noticeId) { return village.equals(villageId) && notice.id().equals(noticeId); }
    }
    public static final Codec<QuestLog> CODEC = RecordCodecBuilder.create(i -> i.group(
            Quest.CODEC.listOf().optionalFieldOf("quests", List.of()).forGetter(QuestLog::quests),
            Codec.unboundedMap(Codec.STRING, Codec.INT).optionalFieldOf("thanks", Map.of()).forGetter(QuestLog::thanks),
            Codec.INT.optionalFieldOf("answered", 0).forGetter(QuestLog::answered)
    ).apply(i, QuestLog::new));

    public QuestLog { quests = List.copyOf(quests); thanks = Map.copyOf(thanks); }

    public boolean full() { return quests.size() >= MAX; }
    public Quest find(String village, String id) {
        for (var q : quests) if (q.is(village, id)) return q;
        return null;
    }
    public QuestLog add(Quest q) {
        if (find(q.village(), q.id()) != null) return this;
        var next = new ArrayList<>(quests); next.add(q);
        return new QuestLog(next, thanks, answered);
    }
    public QuestLog replace(Quest q) {
        var next = new ArrayList<Quest>();
        for (var o : quests) next.add(o.is(q.village(), q.id()) ? q : o);
        return new QuestLog(next, thanks, answered);
    }
    public QuestLog drop(String village, String id) {
        var next = new ArrayList<>(quests); next.removeIf(q -> q.is(village, id));
        return new QuestLog(next, thanks, answered);
    }
    /** A notice answered: it leaves the log, and the poster owes thanks if they weren't there to give it. */
    public QuestLog done(String village, String id, String owedBy, int points) {
        var next = drop(village, id);
        var owed = new HashMap<>(thanks);
        if (owedBy != null && !owedBy.isEmpty() && points > 0) owed.merge(owedBy, points, Integer::sum);
        return new QuestLog(next.quests, owed, answered + 1);
    }
    public QuestLog thanked(String resident) {
        if (!thanks.containsKey(resident)) return this;
        var owed = new HashMap<>(thanks); owed.remove(resident);
        return new QuestLog(quests, owed, answered);
    }
    /** A monster of {@code group} defeated: every hunt for it moves along. Returns the quests that changed. */
    public List<Quest> hunting(String group) {
        return quests.stream().filter(q -> q.notice().kind().equals(Notice.HUNT) && q.notice().target().equals(group) && q.progress() < q.notice().count()).toList();
    }
}
