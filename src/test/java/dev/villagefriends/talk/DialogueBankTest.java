package dev.villagefriends.talk;

import static org.junit.jupiter.api.Assertions.*;

import dev.villagefriends.routine.Routine;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;
import org.junit.jupiter.api.Test;

class DialogueBankTest {
    static final DialogueBank BANK = DialogueBank.builtin();
    static final List<String> PERSONALITIES = List.of("warmhearted", "thoughtful", "playful", "adventurous", "meticulous", "steadfast",
            "reserved", "imaginative", "pragmatic", "curious", "protective", "gentle");
    static final List<String> JOBS = List.of("farmer", "librarian", "fisherman", "fletcher", "cleric", "cartographer", "armorer", "toolsmith",
            "weaponsmith", "leatherworker", "mason", "shepherd", "butcher", "knight", "archer", "cook", "tavern_keeper", "apothecary", "painter",
            "bard", "tailor", "carpenter", "scholar", "nitwit", "none");
    static final List<String> PERIODS = List.of("dawn", "morning", "noon", "afternoon", "evening", "night", "late");
    static final List<String> HOMES = List.of("plains", "desert", "savanna", "snow", "taiga", "jungle", "swamp");
    static final Set<String> EFFECTS = Set.of("heal", "meal", "shelter", "torch", "cook_held", "mend_held", "directions", "fish", "study",
            "flower", "apple", "bread", "cookie", "seeds", "emerald_tip");

    static final List<String> GOOD_DEEDS = List.of("raid_defended", "raid_won", "revived", "bandaged", "saved_from_monster", "rescued_companion",
            "notice_answered", "birthday_gift", "pet_kindness");
    static final List<String> BAD_DEEDS = List.of("hit_resident", "knocked_out_resident", "killed_resident", "hit_golem", "killed_golem", "hurt_pet",
            "killed_pet", "broke_home", "stole");
    /** Deeds done to or for a resident who lives to talk about it (raids and golems involve nobody; the killed can't speak). */
    static final List<String> SELF_DEEDS = List.of("revived", "bandaged", "saved_from_monster", "rescued_companion", "notice_answered", "birthday_gift",
            "pet_kindness", "hit_resident", "knocked_out_resident", "hurt_pet", "killed_pet", "broke_home", "stole");

    private static void has(String key) { assertTrue(BANK.has(key), "Missing dialogue pool " + key); }

    @Test void thereAreMoreThanFiveThousandPiecesOfDialogue() {
        int lines = 0;
        for (var pool : BANK.pools().values()) lines += pool.size();
        int asks = 0, replies = 0;
        for (var q : BANK.questions()) { asks += q.ask().size(); replies += q.answers().size(); }
        assertTrue(BANK.size() >= 5000, "At least 5,000 pieces of dialogue: " + BANK.size());
        assertTrue(lines + asks + replies >= 5000, "Even without counting answer labels: " + (lines + asks + replies));
        assertTrue(BANK.questions().size() >= 120, "Plenty of questions: " + BANK.questions().size());
    }

    @Test void noLineIsWrittenTwice() {
        var seen = new HashSet<String>();
        for (var pool : BANK.pools().entrySet()) for (var line : pool.getValue()) assertTrue(seen.add(line), "Duplicate line in " + pool.getKey() + ": " + line);
    }

    @Test void everyPersonalityJobAndMomentHasSomethingToSay() {
        for (String p : PERSONALITIES) { has("chat." + p); has("greet.personality." + p); has("adventure." + p); has("joke." + p); }
        for (String job : JOBS) { has("work." + job); has("joke.job." + job); if (!job.equals("nitwit") && !job.equals("none")) has("station." + job); }
        for (var block : Routine.Block.values()) { has("greet.routine." + block.id()); has("routine." + block.id()); }
        for (String w : List.of("clear", "clearing", "rain", "thunder", "snow", "hot")) has("weather." + w);
        for (String w : List.of("clearing", "rain", "thunder", "snow", "hot")) has("greet.weather." + w);
        for (String period : PERIODS) { has("greet." + period); has("time." + period); has("baby.time." + period); }
        for (String band : List.of("stranger", "acquaintance", "friend", "close", "best")) has("greet.band." + band);
        for (String moon : Talk.MOONS) has("moon." + moon);
        for (String home : HOMES) has("home." + home);
        for (String topic : List.of("greet", "chat", "work", "adventure", "joke", "market")) has("baby." + topic);
        for (String key : List.of("chat.general", "chat.new", "chat.friendly", "chat.close", "work.general", "work.on", "work.off",
                "adventure.general", "adventure.place", "joke.general", "day.market", "day.week", "greet.market")) has(key);
    }

    @Test void everyDeedHasReactionsForEveryWayOfKnowingAndEveryPersonality() {
        for (String kind : GOOD_DEEDS) { has("deed." + kind + ".seen"); has("deed." + kind + ".heard"); }
        for (String kind : BAD_DEEDS) { has("deed." + kind + ".seen"); has("deed." + kind + ".heard"); }
        for (String kind : SELF_DEEDS) { has("deed." + kind + ".self"); has("deed." + kind + ".family"); }
        has("deed.killed_resident.family");
        for (String sort : List.of("good", "bad")) for (String how : List.of("seen", "heard")) {
            for (String p : PERSONALITIES) has("deed." + sort + "." + how + "." + p);
            has("baby.deed." + sort + "." + how);
        }
        for (String sort : List.of("good", "bad")) has("baby.deed." + sort + ".family");
        for (String kind : List.of("saved_from_monster", "revived", "bandaged", "birthday_gift", "pet_kindness", "hit_resident")) has("baby.deed." + kind + ".self");
        for (String key : List.of("deed.apology.accept", "deed.apology.cool", "deed.apology.accept.child", "deed.apology.cool.child",
                "deed.apology.remembered")) has(key);
        for (String kind : List.of("revived", "saved_from_monster", "rescued_companion")) { has("deed.kept." + kind + ".self"); has("deed.kept." + kind + ".family"); }
        has("greet.unwelcome"); has("baby.greet.unwelcome"); has("chat.unwelcome"); has("notice.unwelcome");
        for (String p : PERSONALITIES) has("greet.unwelcome." + p);
    }

    @Test void deedReactionsNeverDependOnlyOnOptionalDetails() {
        // {kin}, {teller} and {house} aren't always known; {victim} always is for a deed with someone involved, and raids and
        // golems involve nobody. Every reaction pool keeps lines that need no more than that.
        var always = new java.util.HashMap<>(Map.of("name", "Mira", "player", "Alex", "village", "Thistlewick"));
        var withVictim = new java.util.HashMap<>(always); withVictim.put("victim", "Liora");
        for (var pool : BANK.pools().entrySet()) {
            String key = pool.getKey();
            if (!key.startsWith("deed.") && !key.startsWith("baby.deed.")) continue;
            boolean nobody = key.contains("raid_") || key.contains("_golem") || key.startsWith("deed.good.") || key.startsWith("deed.bad.")
                    || key.startsWith("deed.apology.") || key.startsWith("baby.deed.good.") || key.startsWith("baby.deed.bad.");
            var values = nobody ? always : withVictim;
            long ok = pool.getValue().stream().filter(line -> Talk.fill(line, values) != null).count();
            assertTrue(ok >= 2, key + " has at least two lines that always fill: " + ok);
        }
        for (String kind : List.of("raid_defended", "raid_won", "hit_golem", "killed_golem"))
            for (String how : List.of("seen", "heard")) for (var line : BANK.pool("deed." + kind + "." + how))
                assertFalse(line.contains("{victim}") || line.contains("{kin}"), "Nobody is involved in " + kind + ": " + line);
    }

    @Test void homesHaveSomethingToSay() {
        for (String key : List.of("home.mine", "home.shared", "home.homeless", "home.crowded", "home.new", "home.new.player", "home.newborn_bed",
                "home.partner_moved", "home.vacant", "home.bedtime", "home.carried", "home.carried.cot", "baby.home.mine", "baby.home.new",
                "home.plaque.lived", "home.plaque.empty", "home.plaque.private", "notice.house", "notice.house.homeless", "notice.house.crowded",
                "notice.house.newborn", "notice.thanks.house", "baby.notice.house")) has(key);
        var always = Map.of("name", "Mira", "player", "Alex", "village", "Thistlewick");
        for (var pool : BANK.pools().entrySet()) {
            if (!pool.getKey().startsWith("home.") && !pool.getKey().startsWith("baby.home.") && !pool.getKey().contains(".house")) continue;
            assertTrue(pool.getValue().stream().anyMatch(line -> Talk.fill(line, always) != null), pool.getKey() + " can speak without a house name");
        }
    }

    @Test void homesteadFolkHaveSomethingToSayOnEveryTopic() {
        var always = Map.of("name", "Mira", "player", "Alex", "village", "the village", "place", "Blackthorn House", "item", "iron sword",
                "time", "8:30", "weekday", "Bellday", "season", "Summer", "moon", "full moon");
        for (var role : dev.villagefriends.homestead.Dwelling.Role.values()) {
            String r = role.id() + ".";
            for (String key : List.of("greet", "greet.stranger", "greet.friend", "greet.morning", "greet.evening", "greet.night", "weather.rain",
                    "weather.thunder", "weather.snow", "weather.clearing", "weather.hot", "chat", "chat.new", "chat.close", "past", "night", "work",
                    "adventure", "joke", "news", "heart", "player.hurt", "held.sword", "held.flower")) has(r + key);
            assertTrue(BANK.pool(r + "chat").size() >= 35, role + " has plenty to chat about: " + BANK.pool(r + "chat").size());
            // A widowed homesteader (no {partner}, no {spouse}) still has something to say in every pool.
            for (var pool : BANK.pools().entrySet()) if (pool.getKey().startsWith(r))
                assertTrue(pool.getValue().stream().anyMatch(line -> Talk.fill(line, always) != null), pool.getKey() + " can speak without a spouse");
        }
        has("homesteader.work.farmer"); has("homesteader.work.cook");
    }

    @Test void questionsAreWellFormedAndAnswersAreRemembered() {
        var ids = new HashSet<String>();
        for (var q : BANK.questions()) {
            assertTrue(ids.add(q.id()), "Unique id " + q.id());
            assertTrue(q.answers().size() >= 2 && q.answers().size() <= 4, q.id());
            for (var a : q.answers()) {
                assertTrue(a.label().length() <= 30, "Short label: " + a.label());
                if (a.effect() != null) assertTrue(EFFECTS.contains(a.effect()), "Known effect " + a.effect());
                if (a.flag() != null) has("remember." + a.flag().replace(':', '_'));
            }
            if (q.offer()) assertTrue(q.answers().stream().anyMatch(a -> a.effect() != null || a.points() > 0), "Offer " + q.id() + " does something");
        }
    }

    @Test void placeholdersCanBeFilled() {
        Map<String, String> all = Map.ofEntries(Map.entry("name", "Mira"), Map.entry("player", "Alex"), Map.entry("village", "Thistlewick"),
                Map.entry("job", "farmer"), Map.entry("hobby", "baking"), Map.entry("love", "cookie"), Map.entry("friend", "Pell"),
                Map.entry("partner", "Rowan"), Map.entry("rival", "Gus"), Map.entry("time", "8:30"), Map.entry("day", "12"), Map.entry("item", "iron sword"),
                Map.entry("biome", "the plains"), Map.entry("moon", "full moon"), Map.entry("market", "tomorrow"), Map.entry("neighbor", "Tamsin"),
                Map.entry("weekday", "Bellday"), Map.entry("celebrant", "Mira"), Map.entry("birthday", "Summer 12"), Map.entry("when", "in 3 days"),
                Map.entry("mobs", "5 zombies"), Map.entry("wanted", "12 wheat"), Map.entry("recipient", "Tobin"), Map.entry("sender", "Mira"),
                Map.entry("season", "Summer"), Map.entry("victim", "Liora"), Map.entry("kin", "sister"), Map.entry("teller", "Pell"),
                Map.entry("house", "The Ashford House"), Map.entry("place", "Blackthorn House"), Map.entry("spouse", "wife"),
                Map.entry("dish", "onion pottage"), Map.entry("meal", "beef stew"), Map.entry("special", "mutton pie"), Map.entry("gift", "honey cake"));
        for (var pool : BANK.pools().entrySet()) for (var line : pool.getValue()) {
            String filled = Talk.fill(line, all);
            assertNotNull(filled, "Fillable: " + line);
            assertFalse(filled.contains("{"), "No leftover braces: " + filled);
        }
    }

    @Test void aWholeConversationRarelyRepeats() {
        var context = new Talk.Context("chat", false, "playful", "farmer", 4, "afternoon", "rain", "hobby", false, "full", "plains", "",
                Set.of(), Set.of(), Map.of("name", "Mira", "player", "Alex", "village", "Thistlewick", "hobby", "music", "time", "15:00", "weekday", "Bellday", "market", "in 2 days", "biome", "the plains", "moon", "full moon"));
        var recent = new java.util.ArrayDeque<String>(); var said = new HashSet<String>(); var random = new Random(7);
        for (int i = 0; i < 60; i++) {
            var line = Talk.pick(BANK, context, random, recent);
            assertNotNull(line);
            assertFalse(recent.contains(line.id()), "Not one of the last twelve lines");
            said.add(line.text());
            recent.addLast(line.id()); if (recent.size() > 12) recent.removeFirst();
        }
        assertTrue(said.size() >= 55, "Sixty chats, nearly all different: " + said.size());
    }
}
