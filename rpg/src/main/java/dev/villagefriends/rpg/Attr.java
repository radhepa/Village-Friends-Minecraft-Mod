package dev.villagefriends.rpg;

/** The ten character attributes. Points come from levels, each attribute caps at {@link Balance#ATTR_CAP}. */
public enum Attr {
    VITALITY("Vitality", "+0.3 max health"),
    STRENGTH("Strength", "+1% melee damage"),
    DEXTERITY("Dexterity", "+0.8% attack speed"),
    AGILITY("Agility", "+0.2% speed, +0.2% jump, +0.06 safe fall"),
    ENDURANCE("Endurance", "-0.8% hunger drain, +0.04 breath"),
    TOUGHNESS("Toughness", "+0.12 armor, +0.05 armor toughness"),
    PRECISION("Precision", "+0.4% crit chance, +0.6% projectile damage"),
    LUCK("Luck", "+0.04 luck, +0.5% bonus loot chance"),
    WISDOM("Wisdom", "+1% character and skill experience"),
    RECOVERY("Recovery", "Heal slowly out of combat; faster per point");

    public final String label, perPoint;
    Attr(String label, String perPoint) { this.label = label; this.perPoint = perPoint; }
    public String id() { return name().toLowerCase(); }
    public static Attr byId(String id) {
        for (var a : values()) if (a.id().equals(id)) return a;
        return null;
    }
}
