package dev.villagefriends.rpg;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Monster masteries. Kills of a family climb five tiers (Novice, Hunter, Slayer, Bane, Legend).
 * Every tier adds +2% damage against the family and -2% damage taken from it; Slayer (tier 3) and
 * Legend (tier 5) each unlock a named passive tied to that monster; Legend also unlocks an active
 * ability used with the ability key. Pure data, no Minecraft types.
 */
public final class Bestiary {
    private Bestiary() {}
    public enum Rarity {
        COMMON(25, 100, 300, 750, 1500), UNCOMMON(15, 60, 180, 450, 900), RARE(5, 20, 60, 150, 300), BOSS(1, 2, 3, 5, 8);
        public final int[] tiers;
        Rarity(int... tiers) { this.tiers = tiers; }
    }
    /**
     * One ability. Kinds: immune (key = effect ids, comma separated), resist (key = damage group,
     * amount = share removed), damage (key = scope, amount = bonus), drop (key = item, amount = chance,
     * count), attr (key = attribute, amount), mine (amount = speed bonus), special (key = ability id),
     * active (amount = cooldown seconds, count = hunger cost).
     */
    public record Perk(int tier, String name, String desc, String kind, String key, double amount, int count) {}
    public record Family(String id, String label, Rarity rarity, List<String> mobs, List<Perk> perks) {
        public int tier(int kills) { int t = 0; while (t < 5 && kills >= rarity.tiers[t]) t++; return t; }
        /** Kills needed for the next tier, or -1 at Legend. */
        public int next(int kills) { int t = tier(kills); return t >= 5 ? -1 : rarity.tiers[t]; }
        public boolean boss() { return rarity == Rarity.BOSS; }
        /** The Legend ability used with the ability key. */
        public Perk active() { return perks.get(2); }
    }
    public static final double TIER_DAMAGE = .02, TIER_RESIST = .02;

    private static Perk p(int tier, String name, String desc, String kind, String key, double amount) { return new Perk(tier, name, desc, kind, key, amount, 1); }
    private static Perk drop(int tier, String name, String desc, String item, double chance, int count) { return new Perk(tier, name, desc, "drop", item, chance, count); }
    private static Perk act(String name, String desc, int cooldown, int hunger) {
        return new Perk(5, name, desc + " (" + cooldown + "s cooldown" + (hunger > 0 ? ", " + hunger + " hunger" : "") + ")", "active", "", cooldown, hunger);
    }
    /** Legend abilities, used with the ability key (amount = cooldown in seconds, count = hunger cost). See {@link Abilities}. */
    private static final Map<String, Perk> ACTIVES = Map.ofEntries(
            Map.entry("zombie", act("Undead Vigor", "Regeneration II for 6s", 90, 3)),
            Map.entry("skeleton", act("Hunter's Sight", "Monsters within 32 blocks glow for 10s", 45, 1)),
            Map.entry("spider", act("Web Shot", "The monster you look at is webbed (Slowness IV, 4s)", 30, 1)),
            Map.entry("creeper", act("Controlled Blast", "Up to 8 damage to monsters within 4 blocks, no block damage; costs you 1 heart", 60, 2)),
            Map.entry("vermin", act("Burrow Rush", "Haste II for 20s", 120, 2)),
            Map.entry("slime", act("Bounce", "Spring about 6 blocks up; no fall damage for 8s", 20, 1)),
            Map.entry("enderman", act("Ender Blink", "Teleport to the block you look at, up to 24 blocks, no pearl needed", 20, 2)),
            Map.entry("blaze", act("Fire Bolt", "Shoot a blaze fireball", 8, 1)),
            Map.entry("witch", act("Witch's Draught", "Heal 2 hearts and shake off harmful effects", 120, 2)),
            Map.entry("drowned", act("Riptide", "Launch forward like a Riptide trident, in water or rain", 15, 1)),
            Map.entry("piglin", act("War Cry", "Strength I for 10s", 90, 2)),
            Map.entry("illager", act("Evoker Fangs", "A line of fangs bites up to 11 blocks ahead", 30, 2)),
            Map.entry("guardian", act("Tidal Sight", "Conduit Power for 60s", 180, 1)),
            Map.entry("wither_skeleton", act("Withering Strike", "Your next melee hit within 10s withers (Wither II, 5s)", 30, 1)),
            Map.entry("ghast", act("Ghast Fireball", "Shoot an exploding ghast fireball", 30, 2)),
            Map.entry("phantom", act("Night Glide", "Slow Falling for 15s and a push forward", 45, 1)),
            Map.entry("shulker", act("Shulker Bolt", "The monster you look at levitates for 4s", 25, 1)),
            Map.entry("breeze", act("Wind Burst", "Blow monsters within 5 blocks away and hop up", 15, 1)),
            Map.entry("warden", act("Sonic Boom", "10 damage through armor to the monster you look at, up to 15 blocks", 60, 4)),
            Map.entry("wither", act("Wither Skull", "Shoot a wither skull", 20, 2)),
            Map.entry("dragon", act("Dragon Roar", "3 hearts of damage to monsters within 8 blocks, knocking them back", 90, 3)),
            Map.entry("elder_guardian", act("Abyssal Ward", "Resistance II for 8s", 120, 2)));
    private static Family f(String id, String label, Rarity r, List<String> mobs, Perk slayer, Perk legend) { return new Family(id, label, r, mobs, List.of(slayer, legend, ACTIVES.get(id))); }

    public static final List<Family> FAMILIES = List.of(
            f("zombie", "Zombies", Rarity.COMMON, List.of("zombie", "zombie_villager", "husk"),
                    p(3, "Strong Stomach", "Immune to Hunger (rotten flesh is safe)", "immune", "hunger", 0),
                    p(5, "Grave Resolve", "Once every 20 minutes a killing blow leaves you at 4 health", "special", "cheat_death", 0)),
            f("skeleton", "Skeletons", Rarity.COMMON, List.of("skeleton", "stray", "bogged", "parched"),
                    p(3, "Bone Archer", "+15% projectile damage", "damage", "projectile", .15),
                    p(5, "Deadeye", "+20% more projectile damage", "damage", "projectile", .20)),
            f("spider", "Spiders", Rarity.COMMON, List.of("spider", "cave_spider"),
                    p(3, "Venom Ward", "Immune to Poison", "immune", "poison", 0),
                    p(5, "Night Eyes", "Night Vision whenever you're underground", "special", "night_eyes", 0)),
            f("creeper", "Creepers", Rarity.COMMON, List.of("creeper"),
                    p(3, "Blast Hardened", "Explosions hurt 30% less", "resist", "explosion", .30),
                    p(5, "Defuser", "Explosions hurt 60% less in total", "resist", "explosion", .30)),
            f("vermin", "Vermin", Rarity.COMMON, List.of("silverfish", "endermite"),
                    p(3, "Quick Hands", "+10% block breaking speed", "mine", "", .10),
                    p(5, "Tunnel Rat", "+20% block breaking speed in total", "mine", "", .10)),
            f("slime", "Slimes", Rarity.UNCOMMON, List.of("slime", "magma_cube"),
                    p(3, "Bouncy", "Fall damage 40% lower", "resist", "fall", .40),
                    p(5, "Gel Body", "+25% knockback resistance", "attr", "knockback_resistance", .25)),
            f("enderman", "Endermen", Rarity.UNCOMMON, List.of("enderman"),
                    p(3, "Pearl Thrift", "Ender pearls no longer hurt when you land", "resist", "pearl", 1),
                    p(5, "Steady Gaze", "Endermen don't mind you looking at them", "special", "steady_gaze", 0)),
            f("blaze", "Blazes", Rarity.UNCOMMON, List.of("blaze"),
                    p(3, "Fire Ward", "Fire hurts 30% less", "resist", "fire", .30),
                    p(5, "Flame Soul", "Fire hurts 60% less in total", "resist", "fire", .30)),
            f("witch", "Witches", Rarity.UNCOMMON, List.of("witch"),
                    p(3, "Hex Ward", "Magic hurts 35% less", "resist", "magic", .35),
                    p(5, "Alchemist's Blood", "Immune to Weakness and Slowness", "immune", "weakness,slowness", 0)),
            f("drowned", "Drowned", Rarity.UNCOMMON, List.of("drowned"),
                    p(3, "Gills", "+2 breath", "attr", "oxygen_bonus", 2),
                    p(5, "Tidecaller", "+25% trident damage", "damage", "trident", .25)),
            f("piglin", "Piglins and Hoglins", Rarity.UNCOMMON, List.of("piglin", "piglin_brute", "zombified_piglin", "hoglin", "zoglin"),
                    p(3, "Gilded Guile", "Piglins treat you as if you wore gold", "special", "gilded_guile", 0),
                    p(5, "Hellbound", "+15% damage in the Nether", "damage", "nether", .15)),
            f("illager", "Illagers", Rarity.UNCOMMON, List.of("pillager", "vindicator", "evoker", "illusioner", "ravager", "vex"),
                    p(3, "Raid Veteran", "+15% damage during raids", "damage", "raid", .15),
                    p(5, "Village Hero", "Always counted a Hero of the Village", "special", "village_hero", 0)),
            f("guardian", "Guardians", Rarity.RARE, List.of("guardian"),
                    p(3, "Deep Lungs", "+2 breath", "attr", "oxygen_bonus", 2),
                    p(5, "Fatigue Ward", "Immune to Mining Fatigue", "immune", "mining_fatigue", 0)),
            f("wither_skeleton", "Wither Skeletons", Rarity.RARE, List.of("wither_skeleton"),
                    p(3, "Decay Ward", "Immune to Wither", "immune", "wither", 0),
                    drop(5, "Skull Hunter", "+5% chance of a wither skeleton skull", "minecraft:wither_skeleton_skull", .05, 1)),
            f("ghast", "Ghasts", Rarity.RARE, List.of("ghast"),
                    p(3, "Sky Hunter", "+20% damage to flying monsters", "damage", "flying", .20),
                    drop(5, "Tear Collector", "Ghasts always drop an extra tear", "minecraft:ghast_tear", 1, 1)),
            f("phantom", "Phantoms", Rarity.RARE, List.of("phantom"),
                    drop(3, "Membrane Harvest", "Phantoms always drop an extra membrane", "minecraft:phantom_membrane", 1, 1),
                    p(5, "Insomnia Ward", "Phantoms stop coming for you", "special", "no_phantoms", 0)),
            f("shulker", "Shulkers", Rarity.RARE, List.of("shulker"),
                    p(3, "Levitation Ward", "Immune to Levitation", "immune", "levitation", 0),
                    drop(5, "Shell Collector", "+50% chance of an extra shulker shell", "minecraft:shulker_shell", .5, 1)),
            f("breeze", "Breezes", Rarity.RARE, List.of("breeze"),
                    p(3, "Steady Feet", "+20% knockback resistance", "attr", "knockback_resistance", .20),
                    p(5, "Updraft", "+3 safe fall distance", "attr", "safe_fall_distance", 3)),
            f("warden", "The Warden", Rarity.BOSS, List.of("warden"),
                    p(3, "Echo Ward", "Sonic booms hurt 30% less", "resist", "sonic", .30),
                    p(5, "Calm of the Deep", "Immune to Darkness", "immune", "darkness", 0)),
            f("wither", "The Wither", Rarity.BOSS, List.of("wither"),
                    p(3, "Starforged", "+10% damage to bosses", "damage", "boss", .10),
                    p(5, "Star Heart", "+4 max health", "attr", "max_health", 4)),
            f("dragon", "The Ender Dragon", Rarity.BOSS, List.of("ender_dragon"),
                    p(3, "Dragon Hide", "The dragon and its breath hurt 40% less", "resist", "dragon", .40),
                    p(5, "Dragonslayer", "+10% damage to bosses", "damage", "boss", .10)),
            f("elder_guardian", "Elder Guardians", Rarity.BOSS, List.of("elder_guardian"),
                    p(3, "Abyssal Lungs", "+3 breath", "attr", "oxygen_bonus", 3),
                    p(5, "Tidebreaker", "+0.3 water movement", "attr", "water_movement_efficiency", .3)));

    private static final Map<String, Family> BY_MOB = new HashMap<>(), BY_ID = new HashMap<>();
    static { for (var f : FAMILIES) { BY_ID.put(f.id(), f); for (var m : f.mobs()) BY_MOB.put(m, f); } }
    /** The family of a mob, by entity type path (e.g. "zombie"), or null. */
    public static Family ofMob(String path) { return BY_MOB.get(path); }
    public static Family byId(String id) { return BY_ID.get(id); }
}
