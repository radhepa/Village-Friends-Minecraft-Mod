package dev.villagefriends.rpg;

/**
 * Every number the RPG runs on, in one place. Pure: no Minecraft types, so it can be unit tested.
 *
 * <p>The shape: a new character is half as strong as vanilla (5 hearts, 50% hungrier, half melee and
 * projectile damage, half block-breaking speed) and earns its way back to vanilla by level 30. After that
 * it keeps growing slowly to level 100: 15 hearts before Vitality and perks (a full-Vitality, fully
 * mastered tank tops out near 25), and 14% more base damage and breaking speed. Attribute points
 * (317 by level 100) can't max all ten attributes (500), so every character is a build. Against
 * bosses only half of any damage bonus counts, and the bonus on one hit can't pass a small share
 * of the boss's health, so even a maxed character fights the Warden and the dragon for real.
 */
public final class Balance {
    private Balance() {}
    public static final int MAX_LEVEL = 100, ATTR_CAP = 50, SKILL_CAP = 50;

    // Tunable from config/villagefriends_rpg.json (see RpgConfig); these are the defaults.
    public static double xpRate = 1, skillXpRate = 1, deathPenalty = .25, bossBonusShare = .5, bossHitCap = .04;
    public static boolean hardStart = true;

    // -- character level -------------------------------------------------------------------------
    /** Character experience needed to go from {@code level} to the next one. */
    public static long need(int level) { return 60 + Math.round(12 * Math.pow(level, 1.6)); }
    /** Total experience from level 1 to {@code level}. */
    public static long total(int level) { long t = 0; for (int l = 1; l < level; l++) t += need(l); return t; }
    /** Attribute points for reaching {@code level}: 3, or 5 on every tenth level. */
    public static int pointsAt(int level) { return level % 10 == 0 ? 5 : 3; }
    public static int pointsThrough(int level) { int p = 0; for (int l = 2; l <= level; l++) p += pointsAt(l); return p; }
    public static int maxQuests(int level) { return 3 + (level >= 30 ? 1 : 0) + (level >= 60 ? 1 : 0); }
    public static String title(int level) {
        return level >= 100 ? "Mythic" : level >= 90 ? "Legend" : level >= 70 ? "Paragon" : level >= 50 ? "Hero"
                : level >= 35 ? "Champion" : level >= 20 ? "Veteran" : level >= 10 ? "Adventurer" : "Wanderer";
    }

    // -- the weak start, earned back by level 30, then slow growth to 100 ------------------------------
    /** How strong a level 1 character is (damage, block breaking), its health, and the level where it matches vanilla. */
    public static final double START_POWER = .5;
    public static final int START_HEALTH = 10, VANILLA_LEVEL = 30;
    /** Base damage and breaking speed gained per level past {@link #VANILLA_LEVEL} (+14% by level 100). */
    public static final double LATE_GROWTH = .002;
    /** 0 at level 1, rising evenly to 1 at {@link #VANILLA_LEVEL}. */
    static double startShare(int level) { return Math.clamp((level - 1) / (double) (VANILLA_LEVEL - 1), 0, 1); }
    /** Levels past {@link #VANILLA_LEVEL}, never below 0. */
    static int past(int level) { return Math.max(0, level - VANILLA_LEVEL); }
    /**
     * Base max health: 10 (5 hearts) at level 1, a heart every 6 levels to vanilla's 20 at level 30, then a
     * heart every 14 levels to 30 (15 hearts) at level 100.
     */
    public static double baseHealth(int level) {
        int late = 20 + 2 * (past(level) / 14);
        return hardStart && level < VANILLA_LEVEL ? START_HEALTH + 2 * (level / 6) : late;
    }
    /** Hunger drain multiplier: 1.5 at level 1, 1.0 at 30, 0.85 at 100. */
    public static double hungerRate(int level) {
        if (level <= VANILLA_LEVEL) return hardStart ? 1.5 - .5 * startShare(level) : 1;
        return 1 - .15 * past(level) / (double) (MAX_LEVEL - VANILLA_LEVEL);
    }
    /** The level multiplier on damage and block breaking: 0.5 at level 1, 1.0 at 30, 1.14 at 100. */
    public static double startPower(int level) {
        double start = hardStart ? START_POWER + (1 - START_POWER) * startShare(level) : 1;
        return start + LATE_GROWTH * past(level);
    }
    /** Melee damage before bonuses: 0.5 at level 1, 1.0 at 30, 1.14 at 100. */
    public static double meleeBase(int level) { return startPower(level); }
    /** Projectile damage (bows, crossbows, tridents) before bonuses: 0.5 at level 1, 1.0 at 30, 1.14 at 100. */
    public static double rangedBase(int level) { return startPower(level); }
    /** Block breaking speed before skills: 0.5 at level 1, 1.0 at 30, 1.14 at 100. */
    public static double mineBase(int level) { return startPower(level); }

    // -- attributes, per point ----------------------------------------------------------------------
    public static final double VIT_HEALTH = .2, STR_MELEE = .01, DEX_SPEED = .008, AGI_SPEED = .002, AGI_JUMP = .002,
            AGI_SAFE_FALL = .06, END_HUNGER = .008, END_BREATH = .04, TOU_ARMOR = .12, TOU_TOUGHNESS = .05,
            PRE_CRIT = .004, PRE_PROJECTILE = .006, LUCK_LUCK = .04, LUCK_LOOT = .005, WIS_XP = .01;
    /** Ticks between half-hearts of Recovery healing; 0 means none. */
    public static int recoveryInterval(int points) { return points <= 0 ? 0 : 240 - 3 * points; }
    public static final double CRIT_BONUS = .5;

    // -- skills, per level --------------------------------------------------------------------------
    public static final double SWORD_DAMAGE = .004, SWORD_SWEEP = .01, AXE_DAMAGE = .004, ARCHERY_DAMAGE = .006,
            DEFENSE_TOUGHNESS = .06, DEFENSE_KNOCKBACK = .004, TOOL_SPEED = .01, MINING_DOUBLE = .004, WOOD_DOUBLE = .006,
            DIG_FIND = .003, FARM_EXTRA = .01, FISH_LUCK = .03, HUSBANDRY_EXTRA = .01, ATHLETICS_SPEED = .002,
            ATHLETICS_HUNGER = .008, SWIM_EFFICIENCY = .008, SWIM_BREATH = .03, ACRO_SAFE_FALL = .05,
            ACRO_FALL_DAMAGE = .006, ARCANA_XP = .01, BARTER_REWARD = .01;
    /** Cooking (Hearth & Harvest): longer Well Fed from food you eat, and a chance your dishes come out fine. */
    public static final double COOK_WELL_FED = .01, COOK_FINE = .008;
    /** Riding (Stablehand): horse speed, bond growth, couched lance damage and steadier aim from horseback, per level. */
    public static final double RIDING_SPEED = .002, RIDING_BOND = .01, RIDING_LANCE = .004, RIDING_AIM = .006;
    /** Cooking experience per item taken from a station: a little for flour and butter, more for better dishes. */
    public static double cookXp(int tier) { return tier <= 0 ? 1 : 4 + 4 * tier; }
    /** Fishing (Tall Tales Fishing's minigame): catch-zone pixels (of a 568-pixel track) and reel speed per level. */
    public static final double FISH_ZONE = 1.2, FISH_REEL = .006;
    /** Extra Fishing experience for landing a fish of this rarity (0 common to 4 legendary), on top of the usual 15. */
    public static double fishXp(int rarity, boolean perfect) {
        double xp = switch (rarity) { case 0 -> 0; case 1 -> 10; case 2 -> 25; case 3 -> 50; default -> 150; };
        return perfect ? xp * 1.25 + 5 : xp;
    }
    /** Skill experience to go from skill level {@code s} to the next. */
    public static long skillNeed(int s) { return 20 + Math.round(6 * Math.pow(s, 1.5)); }
    public static int skillLevel(long xp) {
        int s = 0;
        while (s < SKILL_CAP && xp >= skillNeed(s)) xp -= skillNeed(s++);
        return s;
    }
    /** Experience already earned toward the next skill level, and how much that level needs. */
    public static long[] skillProgress(long xp) {
        int s = 0;
        while (s < SKILL_CAP && xp >= skillNeed(s)) xp -= skillNeed(s++);
        return s >= SKILL_CAP ? new long[]{1, 1} : new long[]{xp, skillNeed(s)};
    }

    // -- combat ------------------------------------------------------------------------------------
    /** Hunger multiplier never drops below this, however good the build. */
    public static final double MIN_HUNGER = .4, MAX_REDUCTION = .75;
    /**
     * Damage after the RPG multiplier. Against a boss only {@link #bossBonusShare} of the bonus counts,
     * capped at {@link #bossHitCap} of the boss's max health. Penalties (multiplier below 1) always apply.
     */
    public static float outgoing(float vanilla, double multiplier, boolean boss, float bossMaxHealth) {
        if (!boss || multiplier <= 1) return (float) (vanilla * multiplier);
        double bonus = vanilla * (multiplier - 1) * bossBonusShare;
        return (float) (vanilla + Math.min(bonus, bossMaxHealth * bossHitCap));
    }
    public static float incoming(float amount, double reduction) { return (float) (amount * (1 - Math.clamp(reduction, 0, MAX_REDUCTION))); }

    /** Character experience for a kill, from the mob's max health and how rare its kind is. */
    public static int killXp(float maxHealth, boolean hostile, Bestiary.Rarity rarity) {
        if (!hostile) return 1;
        double mult = rarity == null ? 1 : switch (rarity) { case COMMON -> 1; case UNCOMMON -> 1.3; case RARE -> 1.6; case ELITE -> 3; case BOSS -> 6; };
        return (int) Math.clamp(Math.round(maxHealth * .6 * mult), 1, 4000);
    }
    /**
     * Character experience for discovering a modpack place ({@link Atlas}) of tier 1-5: 10% of the current
     * level's need for a tier 1 place, up to 30% for a tier 5 one, so it's worth the trip at any level.
     */
    public static long discoveryXp(int tier, int level) { return Math.round(need(level) * (.05 + .05 * Math.clamp(tier, 1, 5))); }
    /** Taming an animal: Husbandry and character experience. */
    public static final double TAME_SKILL = 15, TAME_XP = 5;
    /** Seconds between kills of one kind that still count as "in a row", and the window for a mass kill. */
    public static final int STREAK_SECONDS = 30, BURST_SECONDS = 4;
    /**
     * Kill experience share. {@code streak} is this kill's place in a run of the same kind of mob, each
     * within {@link #STREAK_SECONDS} of the last: the first is full, the 2nd to 10th give half, and past
     * 10 it keeps dropping (x0.8 per kill, down to 5%). {@code burst} is how many kills of anything landed
     * in the last {@link #BURST_SECONDS}: 5 or more is a mass kill (x0.25), 10 or more a farm (x0.1).
     */
    public static double fatigue(int streak, int burst) {
        double m = streak <= 1 ? 1 : streak <= 10 ? .5 : Math.max(.05, .5 * Math.pow(.8, streak - 10));
        return m * (burst >= 10 ? .1 : burst >= 5 ? .25 : 1);
    }
    /** Character experience for breaking an ore block, by block id path. */
    public static int oreXp(String path) {
        if (path.contains("ancient_debris")) return 25;
        if (path.contains("diamond") || path.contains("emerald")) return 15;
        if (path.contains("gold")) return path.contains("nether") ? 3 : 6;
        if (path.contains("lapis") || path.contains("iron")) return 4;
        if (path.contains("redstone")) return 3;
        return 2;
    }
    public static String tierName(int tier) {
        return switch (tier) { case 1 -> "Novice"; case 2 -> "Hunter"; case 3 -> "Slayer"; case 4 -> "Bane"; case 5 -> "Legend"; default -> "Untested"; };
    }
}
