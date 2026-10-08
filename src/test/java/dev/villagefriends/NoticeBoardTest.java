package dev.villagefriends;

import static org.junit.jupiter.api.Assertions.*;
import com.mojang.serialization.JsonOps;
import dev.villagefriends.quest.*;
import dev.villagefriends.social.*;
import dev.villagefriends.social.Calendar;
import dev.villagefriends.talk.DialogueBank;
import dev.villagefriends.talk.Talk;
import java.util.*;
import org.junit.jupiter.api.Test;

class NoticeBoardTest {
    private static final DialogueBank BANK = DialogueBank.builtin();
    private static final String[] JOBS = {"farmer", "librarian", "fisherman", "knight", "cook", "tavern_keeper", "apothecary", "carpenter", "cleric", "archer", "nitwit", "none"};
    /** Notices written from the real dialogue bank. */
    static final Postings.Writer WRITER = new Postings.Writer() {
        @Override public String write(String pool, Map<String, String> fill, Random random) {
            var lines = BANK.pool(pool);
            if (lines.isEmpty()) return null;
            var values = new HashMap<>(fill); values.put("village", "Thistlewick");
            int start = random.nextInt(lines.size());
            for (int n = 0; n < lines.size(); n++) { String text = Talk.fill(lines.get((start + n) % lines.size()), values); if (text != null) return text; }
            return null;
        }
        @Override public String itemName(String item) { return item.substring(item.indexOf(':') + 1).replace('_', ' '); }
        @Override public String loved(String residentId) { return "minecraft:honey_bottle"; }
    };
    private static Society village(int adults, int children) {
        var s = Society.create("natural:0:0", 0);
        for (int n = 0; n < adults + children; n++)
            s = s.register(Townsfolk.newcomer("resident-" + n, "Resident" + n + " Ash", n % 2 == 0 ? "MALE" : "FEMALE", JOBS[n % JOBS.length], "warmhearted", n < adults, 0));
        return s.advance(60);
    }

    @Test void boardsFillUpEachMorningAndStaleNoticesComeDown() {
        var s = village(14, 3);
        var board = Postings.refresh(Board.create(s.village()), s, 60, WRITER);
        assertEquals(Postings.MAX_OPEN - 1, board.open(60).size(), "a new board starts with four notices");
        assertSame(board, Postings.refresh(board, s, 60, WRITER), "once a day");
        for (long day = 61; day < 160; day++) {
            board = Postings.refresh(board, s, day, WRITER);
            int open = board.open(day).size();
            assertTrue(open >= Postings.MIN_OPEN && open <= Postings.MAX_OPEN, "between three and five notices up on day " + day + ": " + open);
            var posters = new HashSet<String>();
            for (var n : board.open(day)) {
                assertTrue(posters.add(n.poster()), "one open notice per resident");
                assertTrue(day < n.expires() && n.expires() - n.posted() <= Postings.LIFETIME);
                assertFalse(n.text().contains("{") || n.text().isBlank(), "filled text: " + n.text());
                assertTrue(s.has(n.poster()) && s.get(n.poster()).living());
            }
        }
    }

    @Test void everyKindOfNoticeGoesUpAndMakesSense() {
        var s = village(16, 4);
        var kinds = new HashMap<String, Integer>();
        var board = Board.create(s.village());
        var groups = new HashSet<String>();
        for (long day = 60; day < 460; day++) {
            board = Postings.refresh(board, s, day, WRITER);
            for (var n : board.notices()) if (n.posted() == day) {
                kinds.merge(n.kind(), 1, Integer::sum);
                switch (n.kind()) {
                    case Notice.HUNT -> {
                        var hunt = Postings.hunt(n.target());
                        assertNotNull(hunt); groups.add(n.target());
                        assertTrue(n.count() >= hunt.min() && n.count() <= hunt.max());
                        assertTrue(s.get(n.poster()).adult());
                        assertTrue(n.reward().emeralds() >= 2 && n.reward().emeralds() <= 16);
                    }
                    case Notice.FETCH -> {
                        var wants = s.get(n.poster()).adult() ? Postings.WANTS.get(s.get(n.poster()).job()) : Postings.CHILD_WANTS;
                        assertTrue(wants.stream().anyMatch(w -> w.item().equals(n.target())), n.target() + " for " + s.get(n.poster()).job());
                        assertTrue(n.title().startsWith("Wanted: "));
                    }
                    case Notice.LETTER -> {
                        assertTrue(s.has(n.target()) && !n.target().equals(n.poster()));
                        assertTrue(List.of("friend", "family", "crush", "partner", "apology").contains(n.about()));
                        assertEquals(s.nameOf(n.target()), n.who());
                    }
                    case Notice.BIRTHDAY -> {
                        int until = Calendar.daysUntil(s.get(n.about()).birthday(), day);
                        assertTrue(until >= 1 && until <= 4, "planned a few days ahead: " + until);
                        assertTrue(n.target().equals("minecraft:cake") || n.target().equals("minecraft:honey_bottle"));
                        assertTrue(n.expires() <= day + until + 1, "comes down by the birthday");
                    }
                    default -> fail("unknown kind " + n.kind());
                }
                assertFalse(n.reward().item().isEmpty());
            }
            // Take some notices so the board keeps turning over.
            for (var n : board.open(day)) if ((n.id().hashCode() & 3) == 0) board = board.take(n.id(), "player").remove(n.id());
        }
        for (var kind : List.of(Notice.HUNT, Notice.FETCH, Notice.LETTER, Notice.BIRTHDAY)) assertTrue(kinds.getOrDefault(kind, 0) > 0, "posted " + kind + ": " + kinds);
        assertTrue(kinds.get(Notice.FETCH) > kinds.get(Notice.LETTER), kinds.toString());
        assertTrue(groups.containsAll(List.of("zombies", "skeletons", "spiders", "creepers")), groups.toString());
    }

    @Test void takingDroppingAndStanding() {
        var s = village(8, 0);
        var board = Postings.refresh(Board.create(s.village()), s, 60, WRITER);
        var n = board.open(60).getFirst();
        board = board.take(n.id(), "p1");
        assertTrue(board.find(n.id()).taken());
        assertFalse(board.open(60).contains(board.find(n.id())));
        assertEquals(n.release(), board.release(n.id(), 60).find(n.id()));
        assertNull(board.release(n.id(), n.expires()).find(n.id()), "dropped after its time comes down");
        // Taken notices survive the morning; untaken ones expire.
        var later = Postings.refresh(board, s, n.expires() + 5, WRITER);
        assertNotNull(later.find(n.id()));
        assertTrue(later.notices().stream().filter(x -> !x.taken()).allMatch(x -> x.expires() > n.expires() + 5));
        for (int i = 0; i < 20; i++) board = board.favor("p1");
        assertEquals(20, board.favors("p1"));
        assertEquals(0, Board.standing(0)); assertEquals(1, Board.standing(1)); assertEquals(2, Board.standing(4)); assertEquals(3, Board.standing(12));
        assertEquals("Hero of Thistlewick", Board.title(Board.standing(board.favors("p1")), "Thistlewick"));
        // Saved with the level.
        var json = Board.CODEC.encodeStart(JsonOps.INSTANCE, board).getOrThrow();
        assertEquals(board, Board.CODEC.parse(JsonOps.INSTANCE, json).getOrThrow());
    }

    @Test void huntsCountTheRightMonsters() {
        assertEquals("zombies", Postings.group("minecraft:husk"));
        assertEquals("skeletons", Postings.group("minecraft:stray"));
        assertEquals("pillagers", Postings.group("minecraft:vindicator"));
        assertEquals("", Postings.group("minecraft:cow"));
        var hunt = new Notice("n1", Notice.HUNT, "r", "Mira Ash", "knight", "zombies", 3, "", "", Notice.Reward.NONE, "Zombie trouble", "", 0, 3, "p");
        var log = QuestLog.EMPTY.add(new QuestLog.Quest("v", "Thistlewick", "minecraft:overworld", hunt, 0, 0));
        assertEquals(1, log.hunting("zombies").size()); assertTrue(log.hunting("skeletons").isEmpty());
        for (int i = 0; i < 5; i++) for (var q : log.hunting("zombies")) log = log.replace(q.progress(q.progress() + 1));
        assertTrue(log.find("v", "n1").hunted());
        assertEquals(3, log.find("v", "n1").progress(), "progress stops at the goal");
        log = log.done("v", "n1", "r", 10);
        assertTrue(log.quests().isEmpty()); assertEquals(1, log.answered()); assertEquals(10, log.thanks().get("r"));
        assertTrue(log.thanked("r").thanks().isEmpty());
        var json = QuestLog.CODEC.encodeStart(JsonOps.INSTANCE, log).getOrThrow();
        assertEquals(log, QuestLog.CODEC.parse(JsonOps.INSTANCE, json).getOrThrow());
    }

    @Test void noticesReadNaturally() {
        assertEquals("12 wheat", Words.count(12, "Wheat"));
        assertEquals("3 iron ingots", Words.count(3, "Iron Ingot"));
        assertEquals("a cake", Words.count(1, "cake"));
        assertEquals("an apple", Words.count(1, "apple"));
        assertEquals("some sugar", Words.count(1, "sugar"));
        assertEquals("4 sweet berries", Words.count(4, "sweet berries"));
        assertEquals("2 glass bottles", Words.count(2, "glass bottle"));
        assertEquals("5 zombies", Words.mobs(5, "zombies"));
        assertEquals("a witch", Words.mobs(1, "witches"));
        assertEquals("2 witches", Words.mobs(2, "witches"));
        for (var job : Postings.WANTS.keySet()) { assertTrue(Postings.GIFTS.containsKey(job), job); assertTrue(Postings.RARE.containsKey(job), job); }
    }
}
