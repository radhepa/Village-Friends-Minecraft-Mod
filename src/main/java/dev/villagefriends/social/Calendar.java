package dev.villagefriends.social;

import dev.villagefriends.routine.Routine;

/**
 * The village calendar: four seasons of 28 days (four village weeks each, so every season starts on
 * a Moonday and every Market Day falls on the 7th, 14th, 21st and 28th), 112 days to a year. Day 0
 * of the world is Spring 1 of Year 1. Every resident has a birthday on it; babies born in a village
 * have theirs on the day they were born.
 */
public final class Calendar {
    public static final int SEASON_DAYS = 28, SEASONS = 4, YEAR = SEASON_DAYS * SEASONS;
    private static final String[] NAMES = {"Spring", "Summer", "Autumn", "Winter"};

    /** The day of the year, 0 (Spring 1) to 111 (Winter 28). */
    public static int dayOfYear(long day) { return (int) Math.floorMod(day, (long) YEAR); }
    public static int year(long day) { return (int) Math.floorDiv(day, (long) YEAR) + 1; }
    public static String season(long day) { return NAMES[dayOfYear(day) / SEASON_DAYS]; }
    /** 1 to 28. */
    public static int dayOfSeason(long day) { return dayOfYear(day) % SEASON_DAYS + 1; }
    /** "Summer 12". */
    public static String date(long day) { return season(day) + " " + dayOfSeason(day); }
    /** "Hayday, Summer 12, Year 2". */
    public static String longDate(long day) { return Routine.weekday(day) + ", " + date(day) + ", Year " + year(day); }
    /** A day of the year as a date: {@code birthdayDate(40)} is "Summer 13". */
    public static String birthdayDate(int dayOfYear) { return date(Math.floorMod(dayOfYear, YEAR)); }

    /** A resident's birthday (day of the year) for those not born in the village: stable for their ID. */
    public static int birthday(String residentId) {
        long h = 0xB17D4A7L;
        for (int i = 0; i < residentId.length(); i++) h = (h ^ residentId.charAt(i)) * 0x100000001B3L;
        h ^= h >>> 29; h *= 0xBF58476D1CE4E5B9L; h ^= h >>> 32;
        return (int) Math.floorMod(h, (long) YEAR);
    }
    /** Days from {@code today} until the next birthday on {@code dayOfYear}: 0 on the day itself. */
    public static int daysUntil(int dayOfYear, long today) { return Math.floorMod(dayOfYear - dayOfYear(today), YEAR); }
    public static boolean isBirthday(int dayOfYear, long today) { return daysUntil(dayOfYear, today) == 0; }
    /** "today", "tomorrow", "in 3 days". */
    public static String when(int days) { return days == 0 ? "today" : days == 1 ? "tomorrow" : "in " + days + " days"; }

    private Calendar() {}
}
