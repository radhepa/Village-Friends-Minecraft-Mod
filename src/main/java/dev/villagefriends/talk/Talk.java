package dev.villagefriends.talk;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Chooses what a resident says from what is actually happening: the time and the weather, what part of
 * their day it is, their personality and job, how well they know you, what you're holding and how you
 * look, Market Day, the moon, neighbors nearby, and answers you gave them before. Pure: the world is
 * read into a {@link Context} by {@code TalkWorld}.
 */
public final class Talk {
    /**
     * The moment a line is chosen for. {@code states} describe the player ("hurt", "wet", "diamond"...),
     * {@code extra} the surroundings ("golem", "cat", "trader") and remembered answers ("a:likes:sunrise").
     */
    public record Context(String topic, boolean child, String personality, String job, int level, String period, String weather,
                          String routine, boolean market, String moon, String home, String held, Set<String> states, Set<String> extra,
                          Map<String, String> fill) {
        public boolean night() { return period.equals("night") || period.equals("late"); }
        /** Every tag a question's "when:" can test. */
        public Set<String> tags() {
            var tags = new HashSet<String>();
            tags.add(topic); tags.add(child ? "child" : "adult"); tags.add("personality:" + personality); tags.add("job:" + job);
            tags.add(period); tags.add(night() ? "night" : "day"); tags.add(weather); tags.add("routine:" + routine);
            if (market) tags.add("market");
            tags.add("home:" + home);
            if (!held.isEmpty()) tags.add("held:" + held);
            tags.addAll(states); tags.addAll(extra);
            return tags;
        }
    }
    /** A chosen line, its pool and position (for not repeating it soon). */
    public record Line(String key, int index, String text) {
        public String id() { return key + "#" + index; }
    }

    public static String band(int level) {
        return level <= 0 ? "stranger" : level <= 2 ? "acquaintance" : level <= 4 ? "friend" : level <= 7 ? "close" : "best";
    }
    /** Time of day from the clock (ticks; 0 is 6:00). */
    public static String period(int time) {
        int hour = (Math.floorMod(time, 24000) / 1000 + 6) % 24;
        if (hour >= 5 && hour < 7) return "dawn";
        if (hour < 5) return "late";
        if (hour < 11) return "morning";
        if (hour < 13) return "noon";
        if (hour < 17) return "afternoon";
        if (hour < 20) return "evening";
        return "night";
    }
    public static final String[] MOONS = {"full", "waning_gibbous", "last_quarter", "waning_crescent", "new", "waxing_crescent", "first_quarter", "waxing_gibbous"};
    public static String moonName(String moon) { return moon.replace('_', ' ') + " moon"; }

    /** Which pools a topic draws from now, and how likely each is. */
    public static Map<String, Integer> pools(Context c) {
        var w = new LinkedHashMap<String, Integer>();
        boolean weather = !c.weather.equals("clear");
        // Homestead folk (the pariah, the shepherd...) live out in the wild: they talk from their own pools.
        String dweller = c.fill.get("dweller");
        if (dweller != null && !c.child) return dweller(dweller, c, weather);
        if (c.child) {
            String t = c.topic.equals("greet") ? "greet" : c.topic;
            w.put("baby." + t, 6);
            if (weather) w.put("baby.weather." + c.weather, c.topic.equals("greet") || c.topic.equals("chat") ? 4 : 1);
            if (c.topic.equals("chat") || c.topic.equals("greet")) {
                w.put("baby.routine." + c.routine, 2); w.put("baby.time." + c.period, 1);
                if (c.market) w.put("baby.market", 2);
                if (c.topic.equals("chat")) w.put("baby.chat.food", 1);
                if (c.fill.containsKey("meal")) w.put("meal.eating", 6);
                if (c.topic.equals("chat") && c.fill.containsKey("legend") && !c.fill.containsKey("tale_caught")) w.put("baby.tale.legend", 1);
                // A child whose family is short of room talks about the bigger house they asked for.
                String home = c.fill.get("home_talk");
                if ("crowded".equals(home) || "homeless".equals(home)) w.put("baby.notice.house", 2);
                else if (home != null) w.put("baby.home." + home, "new".equals(home) ? 3 : 1);
                held(w, c, 1);
            }
            return w;
        }
        switch (c.topic) {
            case "greet" -> {
                w.put("greet." + c.period, 3); w.put("greet.band." + band(c.level), 3); w.put("greet.personality." + c.personality, 2);
                w.put("greet.routine." + c.routine, 3);
                if (weather) w.put("greet.weather." + c.weather, 5);
                if (c.market) w.put("greet.market", 4);
                home(w, c);
                held(w, c, 2); states(w, c, 4);
            }
            case "chat" -> {
                w.put("chat." + c.personality, 6); w.put("chat.general", 3); w.put("routine." + c.routine, 3); w.put("time." + c.period, 2);
                // Hearth & Harvest: food talk, the meal in their hands, the tavern's dish of the day.
                if (c.fill.containsKey("dish")) w.put("chat.food", 2);
                if (c.fill.containsKey("meal")) w.put("meal.eating", 8);
                if (c.routine.equals("lunch_tavern") || c.routine.equals("supper_tavern") || c.job.equals("tavern_keeper") || c.job.equals("cook")) w.put("tavern.special", 3);
                fishing(w, c);
                w.put(c.level >= 6 ? "chat.close" : c.level <= 1 ? "chat.new" : "chat.friendly", 2);
                w.put("weather." + c.weather, weather ? 4 : 1);
                if (c.night()) w.put("moon." + c.moon, 2);
                if (c.market) w.put("day.market", 3); else w.put("day.week", 1);
                w.put("home." + c.home, 1);
                home(w, c);
                held(w, c, 2); states(w, c, 3);
                for (var tag : c.extra) {
                    if (tag.startsWith("a:")) w.put("remember." + tag.substring(2).replace(':', '_'), 3);
                    else w.put("village." + tag, 2);
                }
            }
            case "work" -> {
                w.put("work." + c.job, 7); w.put("station." + c.job, 2); w.put("work.general", 1);
                if (c.job.equals("fisherman")) { w.put("fishmonger.work", 4); w.put("fishing.chat", 2); }
                w.put(c.routine.equals("work") ? "work.on" : "work.off", 2);
                if (weather) w.put("work.weather." + c.weather, 1);
            }
            case "adventure" -> {
                w.put("adventure." + c.personality, 4); w.put("adventure.general", 3); w.put("adventure.place", 3);
                if (c.night()) w.put("adventure.night", 1);
                held(w, c, 1);
            }
            case "joke" -> {
                w.put("joke.general", 5); w.put("joke." + c.personality, 2); w.put("joke.job." + c.job, 2);
                if (weather) w.put("joke.weather", 1);
            }
            default -> w.put("chat.general", 1);
        }
        return w;
    }
    /**
     * Tall Tales Fishing: tall tales of legendary fish (more from fishermen and anglers), what they make of a
     * legend the player has landed, the season's contest and who won it, fishing talk, and the dock.
     */
    private static void fishing(Map<String, Integer> w, Context c) {
        boolean angler = c.job.equals("fisherman") || "fishing".equals(c.fill.get("hobby"));
        if (c.fill.containsKey("legend")) {
            if (c.fill.containsKey("tale_caught")) w.put("tale.caught", 3);
            else {
                w.put("tale.legend", angler ? 3 : 1); w.put("tale.legend." + c.personality, 1);
                if (c.job.equals("fisherman")) w.put("tale.legend.fisherman", 3);
            }
        }
        String contest = c.fill.get("contest_when");
        if (contest != null) w.put(contest.equals("today") ? "contest.today" : "contest.soon", angler ? 4 : 2);
        String won = c.fill.get("contest_won");
        if (won != null) w.put(won.equals("player") ? "contest.won.player" : "contest.won.resident", 3);
        if (angler) w.put("fishing.chat", 3);
        if (c.fill.containsKey("angling")) w.put("fishing.dock", 8);
        if (c.fill.containsKey("landed")) w.put("fishing.catch", 5);
    }
    /**
     * A homestead resident's pools, all under their role ({@code pariah.chat}, {@code shepherd.greet.night}...):
     * greetings by how well they know you and the time of day, weather, the life they lead and the one they left,
     * late-night thoughts, their work (and their own trade, {@code homesteader.work.farmer}), and reactions to you.
     */
    private static Map<String, Integer> dweller(String role, Context c, boolean weather) {
        var w = new LinkedHashMap<String, Integer>();
        String r = role + ".";
        switch (c.topic) {
            case "greet" -> {
                w.put(r + "greet", 6);
                w.put(r + "greet." + (c.level >= 3 ? "friend" : "stranger"), 4);
                String time = dev.villagefriends.homestead.Dwelling.greetingTime(c.period);
                if (time != null) w.put(r + "greet." + time, 3);
                if (weather) w.put(r + "weather." + c.weather, 5);
                if (!c.held.isEmpty()) w.put(r + "held." + c.held, 2);
                for (var s : c.states) w.put(r + "player." + s, 3);
            }
            case "chat" -> {
                w.put(r + "chat", 8);
                if (c.level <= 1) w.put(r + "chat.new", 3);
                if (c.level >= 6) w.put(r + "chat.close", 4);
                w.put(r + "past", c.level >= 3 ? 3 : 2);
                if (c.night()) w.put(r + "night", 3);
                if (weather) w.put(r + "weather." + c.weather, 3);
                if (!c.held.isEmpty()) w.put(r + "held." + c.held, 2);
                for (var s : c.states) w.put(r + "player." + s, 2);
            }
            case "work" -> { w.put(r + "work", 6); w.put(r + "work." + c.job, 8); }
            case "adventure", "joke", "news", "heart" -> w.put(r + c.topic, 8);
            default -> w.put(r + "chat", 1);
        }
        return w;
    }
    /** Their own house: "home.mine", "home.crowded", "home.new"... (TalkWorld puts which one fits into {@code home_talk}). */
    private static void home(Map<String, Integer> w, Context c) {
        if (c.fill.containsKey("home_talk")) w.put("home." + c.fill.get("home_talk"), 2);
        // Supper or the evening, and still far from their own house: off home they go.
        if (c.fill.containsKey("home_far") && (c.routine.equals("supper") || c.routine.equals("evening"))) w.put("home.bedtime", 4);
    }
    private static void held(Map<String, Integer> w, Context c, int weight) { if (!c.held.isEmpty()) w.put("held." + c.held, weight); }
    private static void states(Map<String, Integer> w, Context c, int weight) { for (var s : c.states) w.put("player." + s, weight); }

    /** A line for this moment that hasn't been said lately, with its placeholders filled; null if nothing fits. */
    public static Line pick(DialogueBank bank, Context c, Random random, Collection<String> recent) {
        var weights = new LinkedHashMap<String, Integer>();
        for (var e : pools(c).entrySet()) if (bank.has(e.getKey())) weights.put(e.getKey(), e.getValue());
        for (int attempt = 0; attempt < 10 && !weights.isEmpty(); attempt++) {
            String key = weighted(weights, random);
            var lines = bank.pool(key);
            int start = random.nextInt(lines.size());
            for (int n = 0; n < lines.size(); n++) {
                int index = (start + n) % lines.size();
                if (recent.contains(key + "#" + index)) continue;
                String text = fill(lines.get(index), c.fill);
                if (text != null) return new Line(key, index, text);
            }
            weights.remove(key); // Everything here was said lately or can't be filled.
        }
        return null;
    }
    private static String weighted(Map<String, Integer> weights, Random random) {
        int total = 0;
        for (int v : weights.values()) total += v;
        int roll = random.nextInt(total);
        for (var e : weights.entrySet()) { roll -= e.getValue(); if (roll < 0) return e.getKey(); }
        return weights.keySet().iterator().next();
    }

    private static final Pattern SLOT = Pattern.compile("\\{([a-z_]+)}");
    /** Fills {placeholders}; null when one of them has no value here. */
    public static String fill(String line, Map<String, String> values) {
        Matcher m = SLOT.matcher(line);
        var out = new StringBuilder();
        while (m.find()) {
            String value = values.get(m.group(1));
            if (value == null || value.isBlank()) return null;
            m.appendReplacement(out, Matcher.quoteReplacement(value));
        }
        m.appendTail(out);
        String text = out.toString();
        return text.isEmpty() ? text : Character.toUpperCase(text.charAt(0)) + text.substring(1);
    }

    /** Whether a question's conditions hold: tags must all be present, "!tag" absent, "level:N" reached. */
    public static boolean eligible(DialogueBank.Question q, Set<String> tags, int level) {
        if (q.when() == null) return true;
        for (String cond : q.when()) {
            if (cond.startsWith("level:")) { if (level < Integer.parseInt(cond.substring(6))) return false; }
            else if (cond.startsWith("!")) { if (tags.contains(cond.substring(1))) return false; }
            else if (cond.contains("|")) {
                boolean any = false;
                for (String option : cond.split("\\|")) any |= tags.contains(option);
                if (!any) return false;
            }
            else if (!tags.contains(cond)) return false;
        }
        return true;
    }
    /** Questions about village life, which nobody living out in the wild would ask. */
    private static final Pattern VILLAGE_TALK = Pattern.compile("(?i)village|tavern|market|bell|neighbo|square");
    static boolean aboutVillageLife(DialogueBank.Question q) {
        for (var ask : q.ask()) if (VILLAGE_TALK.matcher(ask).find()) return true;
        for (var a : q.answers()) if (VILLAGE_TALK.matcher(a.reply()).find() || VILLAGE_TALK.matcher(a.label()).find()) return true;
        return false;
    }
    /** A question to ask (or an offer to make) now, avoiding ones already done; null if none fit. */
    public static DialogueBank.Question question(DialogueBank bank, Context c, Set<String> done, boolean offers, Random random) {
        var tags = c.tags(); var fit = new ArrayList<DialogueBank.Question>();
        boolean wild = c.fill.containsKey("dweller");
        for (var q : bank.questions()) {
            if (q.offer() != offers || done.contains(q.id()) || !eligible(q, tags, c.level)) continue;
            if (wild && aboutVillageLife(q)) continue;
            boolean fillable = true;
            for (var ask : q.ask()) if (fill(ask, c.fill) == null) fillable = false;
            if (fillable) fit.add(q);
        }
        return fit.isEmpty() ? null : fit.get(random.nextInt(fit.size()));
    }
    /** The 0-based answer from an action like "answer:sunrise:2", or -1. */
    public static int answerIndex(String action, String questionId) {
        String prefix = "answer:" + questionId + ":";
        if (!action.startsWith(prefix)) return -1;
        try { return Integer.parseInt(action.substring(prefix.length())); } catch (NumberFormatException e) { return -1; }
    }
    private Talk() {}
}
