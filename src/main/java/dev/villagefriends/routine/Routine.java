package dev.villagefriends.routine;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;

/**
 * A resident's day: when they wake, work, eat, enjoy their hobby, see the neighbors and sleep, and how
 * the weather changes it. Every resident keeps their own hours (early birds, night owls, a tavern keeper
 * who works late, guards on night watch), every seventh day is Market Day, and rain, storms and snow
 * send most people indoors. Pure and unit-tested; {@code ResidentRoutines} applies it to the world.
 *
 * <p>Times are ticks of the Minecraft day: 0 is 6:00, 6000 is noon, 12000 is 18:00, 18000 is midnight.
 */
public final class Routine {
    /** Where a block of the day is spent. */
    public enum Place { HOME, WORK, BELL, TAVERN, HOBBY, VILLAGE }
    /** What the sky is doing where the resident lives. {@code CLEARING} is the hour after rain stops. */
    public enum Weather {
        CLEAR, CLEARING, RAIN, THUNDER, SNOW;
        public String id() { return name().toLowerCase(Locale.ROOT); }
    }
    public enum Chronotype {
        EARLY_BIRD("Early bird", -1000, -1000), REGULAR("Regular hours", 0, 0), NIGHT_OWL("Night owl", 1000, 1500);
        public final String label; final int wake, bed;
        Chronotype(String label, int wake, int bed) { this.label = label; this.wake = wake; this.bed = bed; }
    }
    public enum Block {
        SLEEP("Asleep", Place.HOME, true),
        NAP("Taking a nap", Place.HOME, true),
        WAKE("Just woke up", Place.HOME, false),
        BREAKFAST("Having breakfast", Place.HOME, false),
        PRAYER("At morning prayers", Place.WORK, false),
        WORK("At work", Place.WORK, false),
        LUNCH("On lunch break", Place.BELL, false),
        LUNCH_HOME("Lunch at home", Place.HOME, false),
        LUNCH_TAVERN("Lunch at the tavern", Place.TAVERN, false),
        HOBBY("Enjoying a hobby", Place.HOBBY, false),
        SOCIAL("Catching up with neighbors", Place.BELL, false),
        MARKET("At the market", Place.BELL, false),
        SUPPER("Having supper", Place.HOME, false),
        EVENING("Relaxing at home", Place.HOME, false),
        TAVERN("At the tavern", Place.TAVERN, false),
        PERFORM("Performing at the tavern", Place.TAVERN, false),
        NIGHT_WATCH("On night watch", Place.VILLAGE, false),
        PLAY("Playing", Place.VILLAGE, false),
        LESSONS("At lessons by the bell", Place.BELL, false),
        SHELTER("Sheltering from the rain", Place.HOME, false),
        STORM("Waiting out the storm", Place.HOME, false),
        SNOWED_IN("Keeping warm indoors", Place.HOME, false),
        RAIN_WALK("Enjoying the rain", Place.VILLAGE, false),
        SNOW_PLAY("Playing in the snow", Place.VILLAGE, false),
        /** Guards during a raid: mustered at the bell and out after the raiders instead of hiding. */
        DEFEND("Defending the village", Place.VILLAGE, false);

        public final String label; public final Place place; public final boolean sleep;
        Block(String label, Place place, boolean sleep) { this.label = label; this.place = place; this.sleep = sleep; }
        public String id() { return name().toLowerCase(Locale.ROOT); }
        /** Spent outside under the open sky, unless the place itself has a roof. */
        public boolean outdoors() { return place == Place.BELL || place == Place.HOBBY || place == Place.VILLAGE; }
        public static Block byId(String id) {
            for (var b : values()) if (b.id().equals(id)) return b;
            return null;
        }
    }
    /** One change of activity at a time of day. */
    public record Slot(int start, Block block) {}
    /** A resident's whole day, sorted by start time; the last slot runs on past midnight into the first. */
    public record Day(long number, Chronotype chronotype, boolean marketDay, List<Slot> slots) {
        public Block at(int time) {
            int t = Math.floorMod(time, 24000); Block current = slots.getLast().block();
            for (var slot : slots) { if (slot.start() <= t) current = slot.block(); else break; }
            return current;
        }
        /** When the next change after {@code time} happens. */
        public Slot next(int time) {
            int t = Math.floorMod(time, 24000);
            for (var slot : slots) if (slot.start() > t) return slot;
            return slots.getFirst();
        }
    }
    /** What a resident is doing now: the scheduled block, possibly changed by the weather. */
    public record Plan(Block block, Block scheduled, Weather weather, Day day) {
        public boolean changedByWeather() { return block != scheduled; }
        public String label() {
            if (block == Block.WORK && weather == Weather.RAIN) return "Working in the rain";
            if (block == Block.NIGHT_WATCH && (weather == Weather.RAIN || weather == Weather.THUNDER)) return "Standing guard in the storm";
            return block.label;
        }
    }

    public static final int MARKET_EVERY = 7;
    private static final String[] WEEK = {"Moonday", "Bellday", "Hearthday", "Wellday", "Lanternday", "Hayday", "Market Day"};
    /** The village week: six working days and Market Day. */
    public static String weekday(long day) { return WEEK[(int) Math.floorMod(day, 7L)]; }
    public static boolean marketDay(long day) { return Math.floorMod(day, MARKET_EVERY) == MARKET_EVERY - 1; }
    /** Clock time in ticks: {@code at(8, 30)} is 8:30 in the morning. */
    public static int at(int hour, int minute) { return Math.floorMod((hour - 6) * 1000 + minute * 1000 / 60, 24000); }
    public static String clock(int time) {
        int t = Math.floorMod(time, 24000), hour = (t / 1000 + 6) % 24, minute = t % 1000 * 60 / 1000;
        return hour + ":" + (minute < 10 ? "0" : "") + minute;
    }

    public static Chronotype chronotype(int seed, String personality, String job, boolean child) {
        if (child) return Chronotype.REGULAR;
        if (job.equals("tavern_keeper") || job.equals("bard")) return Chronotype.NIGHT_OWL;
        if (job.equals("farmer") || job.equals("fisherman") || job.equals("cook") || job.equals("butcher") || job.equals("cleric")) return Chronotype.EARLY_BIRD;
        int roll = Math.floorMod(mix(seed ^ 0x51ED), 100);
        int early = switch (personality) { case "steadfast", "protective", "meticulous", "pragmatic" -> 55; case "thoughtful", "curious", "imaginative" -> 15; default -> 30; };
        int owl = switch (personality) { case "thoughtful", "curious", "imaginative" -> 50; case "steadfast", "protective", "meticulous" -> 10; default -> 22; };
        return roll < early ? Chronotype.EARLY_BIRD : roll < early + owl ? Chronotype.NIGHT_OWL : Chronotype.REGULAR;
    }
    /** About half of all guards keep the night watch; they sleep through the morning. */
    public static boolean nightWatch(int seed, String job) {
        return (job.equals("knight") || job.equals("archer")) && Math.floorMod(mix(seed ^ 0x6A7D), 2) == 0;
    }
    /** Some residents love being out in the rain; children more than most. */
    public static boolean likesRain(int seed, String personality, boolean child) {
        int roll = Math.floorMod(mix(seed ^ 0x7A1B), 100);
        int chance = switch (personality) { case "playful", "adventurous" -> 40; case "curious", "imaginative" -> 25; case "reserved", "meticulous" -> 3; default -> 10; };
        return roll < (child ? chance + 25 : chance);
    }
    public static boolean likesSnow(int seed, String personality, boolean child) {
        int roll = Math.floorMod(mix(seed ^ 0x5A0F), 100);
        int chance = switch (personality) { case "playful", "adventurous", "steadfast" -> 55; case "warmhearted", "protective" -> 30; case "reserved", "gentle" -> 10; default -> 20; };
        return roll < (child ? 85 : chance);
    }
    /** Outdoor trades keep going through ordinary rain. */
    public static boolean hardy(String job) {
        return switch (job) { case "farmer", "shepherd", "fisherman", "knight", "archer", "mason" -> true; default -> false; };
    }

    /** A resident's day: their personal hours, their job's hours, and Market Day. */
    public static Day day(int seed, String job, String personality, boolean child, long number) {
        var type = chronotype(seed, personality, job, child);
        boolean market = marketDay(number);
        int jitter = Math.floorMod(mix(seed ^ (int) number * 31), 401) - 200; // up to 12 minutes either way
        var keys = new ArrayList<Slot>();
        int wake = at(6, 0) + type.wake + jitter, bed = at(20, 30) + type.bed + jitter;
        if (child) {
            wake = at(7, 0) + jitter; bed = at(19, 30) + jitter;
            add(keys, wake, Block.WAKE); add(keys, wake + 300, Block.BREAKFAST);
            add(keys, at(8, 0), Block.PLAY);
            if (!market) { add(keys, at(10, 0), Block.LESSONS); add(keys, at(11, 30), Block.LUNCH_HOME); add(keys, at(12, 30), Block.PLAY); }
            else add(keys, at(11, 30), Block.MARKET);
            add(keys, at(17, 0), Block.SUPPER); add(keys, at(18, 0), Block.EVENING); add(keys, bed, Block.SLEEP);
            return sorted(number, type, market, keys);
        }
        int lunch = Math.floorMod(mix(seed ^ 0x1C4), 3);
        Block lunchBlock = lunch == 0 ? Block.LUNCH : lunch == 1 ? Block.LUNCH_HOME : Block.LUNCH_TAVERN;
        boolean tavernNight = Math.floorMod(mix(seed ^ (int) number * 7919), 3) == 0;
        Block evening = tavernNight ? Block.TAVERN : Block.EVENING;
        switch (job) {
            case "knight", "archer" -> {
                if (nightWatch(seed, job)) {
                    add(keys, at(8, 0), Block.SLEEP); add(keys, at(15, 0), Block.WAKE); add(keys, at(15, 20), Block.BREAKFAST);
                    add(keys, at(16, 0), Block.SOCIAL); add(keys, at(17, 15), Block.SUPPER); add(keys, at(18, 0), Block.NIGHT_WATCH);
                    return sorted(number, type, market, keys);
                }
                add(keys, wake, Block.WAKE); add(keys, wake + 300, Block.BREAKFAST); add(keys, at(7, 30), Block.WORK);
                add(keys, at(11, 30), lunchBlock); add(keys, at(12, 30), Block.WORK); add(keys, at(16, 30), Block.SOCIAL);
                add(keys, at(17, 30), Block.SUPPER); add(keys, at(18, 30), evening); add(keys, bed, Block.SLEEP);
                return sorted(number, type, market, keys);
            }
            case "tavern_keeper" -> {
                add(keys, wake, Block.WAKE); add(keys, wake + 400, Block.BREAKFAST); add(keys, at(9, 30), Block.HOBBY);
                add(keys, at(11, 0), Block.WORK); add(keys, at(19, 45), Block.EVENING); add(keys, bed, Block.SLEEP);
                return sorted(number, type, market, keys);
            }
            case "bard" -> {
                add(keys, wake, Block.WAKE); add(keys, wake + 400, Block.BREAKFAST);
                add(keys, at(9, 0), market ? Block.MARKET : Block.WORK); add(keys, at(11, 30), Block.LUNCH_TAVERN);
                add(keys, at(12, 30), Block.HOBBY); add(keys, at(15, 0), Block.SOCIAL); add(keys, at(17, 0), Block.SUPPER);
                add(keys, at(18, 0), Block.PERFORM); add(keys, at(19, 45), Block.EVENING); add(keys, bed, Block.SLEEP);
                return sorted(number, type, market, keys);
            }
            case "nitwit" -> {
                wake = at(8, 30) + jitter; bed = at(21, 30) + jitter;
                add(keys, wake, Block.WAKE); add(keys, wake + 500, Block.BREAKFAST); add(keys, at(10, 0), Block.HOBBY);
                add(keys, at(11, 30), lunchBlock); add(keys, at(12, 30), Block.NAP); add(keys, at(14, 0), Block.HOBBY);
                add(keys, at(15, 30), market ? Block.MARKET : Block.SOCIAL); add(keys, at(17, 30), Block.SUPPER);
                add(keys, at(18, 15), Block.TAVERN); add(keys, at(19, 45), Block.EVENING); add(keys, bed, Block.SLEEP);
                return sorted(number, type, market, keys);
            }
            default -> {}
        }
        // The cook keeps the kitchen going on Market Day; everyone else takes the day off.
        boolean works = !market || job.equals("cook");
        // Residents without a job spend working hours on their hobby (and looking for a workstation).
        Block work = job.equals("none") ? Block.HOBBY : Block.WORK;
        int start = switch (job) { case "farmer", "fisherman" -> at(6, 30); case "cook", "butcher" -> at(6, 15); case "painter", "scholar" -> at(9, 0); default -> at(8, 0); };
        int stop = switch (job) { case "farmer", "fisherman" -> at(14, 0); case "cook" -> at(13, 0); case "painter" -> at(16, 0); case "scholar" -> at(17, 0); default -> at(15, 0); };
        add(keys, wake, Block.WAKE); add(keys, wake + 300, Block.BREAKFAST);
        if (job.equals("cleric")) add(keys, wake + 600, Block.PRAYER);
        if (works) {
            if (!job.equals("cleric") && wake + 1300 < start && type == Chronotype.EARLY_BIRD) add(keys, wake + 900, Block.HOBBY);
            add(keys, start, work);
            if (!job.equals("cook")) { add(keys, at(11, 30), lunchBlock); add(keys, at(12, 30), work); }
            add(keys, stop, Block.HOBBY);
        } else {
            add(keys, at(9, 0), Block.MARKET); add(keys, at(12, 0), lunchBlock); add(keys, at(13, 0), Block.HOBBY);
        }
        add(keys, at(16, 30), Block.SOCIAL); add(keys, at(17, 30), Block.SUPPER);
        add(keys, at(18, 30), market ? Block.TAVERN : evening); add(keys, bed, Block.SLEEP);
        return sorted(number, type, market, keys);
    }
    private static void add(List<Slot> keys, int time, Block block) { keys.add(new Slot(Math.floorMod(time, 24000), block)); }
    private static Day sorted(long number, Chronotype type, boolean market, List<Slot> keys) {
        keys.sort(Comparator.comparingInt(Slot::start));
        var merged = new ArrayList<Slot>();
        for (var k : keys) {
            if (!merged.isEmpty() && merged.getLast().start() == k.start()) merged.removeLast();
            if (merged.isEmpty() || merged.getLast().block() != k.block()) merged.add(k);
        }
        return new Day(number, type, market, List.copyOf(merged));
    }

    /**
     * What a resident does right now. Ordinary rain sends most people indoors (rain lovers stay out,
     * hardy trades keep working); a thunderstorm sends everyone in except the guards on duty; falling
     * snow keeps the cold-averse at home while children and snow lovers play in it.
     *
     * @param workIndoors whether their workstation has a roof over it
     */
    public static Plan plan(Day day, int time, Weather weather, int seed, String job, String personality, boolean child, boolean workIndoors) {
        Block scheduled = day.at(time), block = scheduled;
        boolean guard = job.equals("knight") || job.equals("archer");
        boolean outside = scheduled.outdoors() || scheduled == Block.WORK && !workIndoors || scheduled == Block.PRAYER && !workIndoors;
        if (outside) switch (weather) {
            case THUNDER -> {
                if (!(guard && (scheduled == Block.WORK || scheduled == Block.NIGHT_WATCH))) block = Block.STORM;
            }
            case RAIN -> {
                if (guard && (scheduled == Block.WORK || scheduled == Block.NIGHT_WATCH)) break;
                if (scheduled == Block.WORK && hardy(job)) break;
                block = likesRain(seed, personality, child) && scheduled != Block.WORK && scheduled != Block.PRAYER ? Block.RAIN_WALK : Block.SHELTER;
            }
            case SNOW -> {
                if (scheduled == Block.WORK || scheduled == Block.NIGHT_WATCH || scheduled == Block.PRAYER) break;
                if (likesSnow(seed, personality, child)) { if (child || scheduled == Block.PLAY) block = Block.SNOW_PLAY; }
                else block = Block.SNOWED_IN;
            }
            default -> {}
        }
        return new Plan(block, scheduled, weather, day);
    }

    /** "6:00 wake · 8:00 work · 11:30 lunch at the bell · ... · 20:30 bed" for the Village Ledger. */
    public static String summary(Day day) {
        var parts = new ArrayList<String>();
        for (var slot : day.slots()) parts.add(clock(slot.start()) + " " + brief(slot.block()));
        int bed = parts.size();
        // Read the day from waking up, not from midnight.
        int first = 0;
        for (int i = 0; i < day.slots().size(); i++) if (day.slots().get(i).block() == Block.WAKE) { first = i; break; }
        var ordered = new ArrayList<String>(parts.subList(first, bed)); ordered.addAll(parts.subList(0, first));
        return String.join(" · ", ordered);
    }
    public static String brief(Block block) {
        return switch (block) {
            case SLEEP -> "bed"; case NAP -> "nap"; case WAKE -> "up"; case BREAKFAST -> "breakfast"; case PRAYER -> "prayers";
            case WORK -> "work"; case LUNCH -> "lunch at the bell"; case LUNCH_HOME -> "lunch at home"; case LUNCH_TAVERN -> "lunch at the tavern";
            case HOBBY -> "hobby"; case SOCIAL -> "neighbors"; case MARKET -> "market"; case SUPPER -> "supper"; case EVENING -> "home";
            case TAVERN -> "tavern"; case PERFORM -> "performs"; case NIGHT_WATCH -> "night watch"; case PLAY -> "play"; case LESSONS -> "lessons";
            default -> block.label.toLowerCase(Locale.ROOT);
        };
    }

    public static int mix(int value) {
        value ^= value >>> 16; value *= 0x7feb352d; value ^= value >>> 15; value *= 0x846ca68b;
        return value ^ (value >>> 16);
    }
    private Routine() {}
}
