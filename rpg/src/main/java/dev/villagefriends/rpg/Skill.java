package dev.villagefriends.rpg;

/** Skills rise by doing: each levels 0 to {@link Balance#SKILL_CAP} on its own experience curve. */
public enum Skill {
    SWORDS("Swordsmanship", "Hit and kill with swords"),
    AXES("Axe Mastery", "Hit and kill with axes"),
    ARCHERY("Archery", "Hit and kill with bows, crossbows and tridents"),
    DEFENSE("Defense", "Take hits in armor, block with a shield"),
    MINING("Mining", "Break stone and ore with a pickaxe"),
    WOODCUTTING("Woodcutting", "Chop logs with an axe"),
    EXCAVATION("Excavation", "Dig dirt, sand and gravel with a shovel"),
    FARMING("Farming", "Harvest ripe crops"),
    FISHING("Fishing", "Catch fish (rarer fish and perfect catches teach more)"),
    HUSBANDRY("Husbandry", "Breed animals and hunt livestock"),
    ATHLETICS("Athletics", "Sprint"),
    SWIMMING("Swimming", "Swim"),
    ACROBATICS("Acrobatics", "Survive falls"),
    ARCANA("Arcana", "Enchant, brew, use anvils, gather experience"),
    BARTERING("Bartering", "Trade with villagers and finish their jobs"),
    COOKING("Cooking", "Cook dishes at a cooking pot, clay oven or prep table"),
    RIDING("Riding", "Ride horses, groom them, and charge with a lance");

    public final String label, howToTrain;
    Skill(String label, String howToTrain) { this.label = label; this.howToTrain = howToTrain; }
    public String id() { return name().toLowerCase(); }

    /** What this skill gives at level {@code s}, in words. */
    public String effect(int s) {
        return switch (this) {
            case SWORDS -> pct(Balance.SWORD_DAMAGE * s) + " sword damage, +" + num(Balance.SWORD_SWEEP * s) + " sweep";
            case AXES -> pct(Balance.AXE_DAMAGE * s) + " axe damage";
            case ARCHERY -> pct(Balance.ARCHERY_DAMAGE * s) + " projectile damage";
            case DEFENSE -> "+" + num(Balance.DEFENSE_TOUGHNESS * s) + " armor toughness, " + pct(Balance.DEFENSE_KNOCKBACK * s) + " knockback resist";
            case MINING -> pct(Balance.TOOL_SPEED * s) + " pickaxe speed, " + chance(Balance.MINING_DOUBLE * s) + " double ore";
            case WOODCUTTING -> pct(Balance.TOOL_SPEED * s) + " axe speed, " + chance(Balance.WOOD_DOUBLE * s) + " double log";
            case EXCAVATION -> pct(Balance.TOOL_SPEED * s) + " shovel speed, " + chance(Balance.DIG_FIND * s) + " buried find";
            case FARMING -> chance(Balance.FARM_EXTRA * s) + " extra harvest";
            case FISHING -> "+" + num(Balance.FISH_LUCK * s) + " luck, " + pct(Balance.FISH_REEL * s) + " reel speed";
            case HUSBANDRY -> chance(Balance.HUSBANDRY_EXTRA * s) + " extra meat, hide or wool";
            case ATHLETICS -> pct(Balance.ATHLETICS_SPEED * s) + " move speed, " + pct(-Balance.ATHLETICS_HUNGER * s) + " sprint hunger";
            case SWIMMING -> "+" + num(Balance.SWIM_EFFICIENCY * s) + " water speed, +" + num(Balance.SWIM_BREATH * s) + " breath";
            case ACROBATICS -> "+" + num(Balance.ACRO_SAFE_FALL * s) + " safe fall, " + pct(-Balance.ACRO_FALL_DAMAGE * s) + " fall damage";
            case ARCANA -> pct(Balance.ARCANA_XP * s) + " vanilla experience";
            case BARTERING -> pct(Balance.BARTER_REWARD * s) + " quest rewards";
            case COOKING -> pct(Balance.COOK_WELL_FED * s) + " Well Fed time, " + chance(Balance.COOK_FINE * s) + " fine dish";
            case RIDING -> pct(Balance.RIDING_SPEED * s) + " horse speed, " + pct(Balance.RIDING_BOND * s) + " bond growth, "
                    + pct(Balance.RIDING_LANCE * s) + " lance damage, " + pct(Balance.RIDING_AIM * s) + " steadier mounted aim";
        };
    }
    static String pct(double v) { return (v >= 0 ? "+" : "") + Math.round(v * 1000) / 10.0 + "%"; }
    static String chance(double v) { return Math.round(v * 1000) / 10.0 + "%"; }
    static String num(double v) { return String.valueOf(Math.round(v * 100) / 100.0); }
}
