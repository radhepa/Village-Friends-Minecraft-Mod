package dev.villagefriends.social;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;

/**
 * A village event residents talk about. Names are resolved when shown, so renamed residents stay correct.
 * A player's big deed is {@code "deed:<kind>"} with {@code a} the resident it happened to, {@code b} a pet's
 * name and {@code c} the player's name.
 */
public record News(long day, String kind, String a, String b, String c) {
    public static final Codec<News> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.LONG.fieldOf("day").forGetter(News::day),
            Codec.STRING.fieldOf("kind").forGetter(News::kind),
            Codec.STRING.optionalFieldOf("a", "").forGetter(News::a),
            Codec.STRING.optionalFieldOf("b", "").forGetter(News::b),
            Codec.STRING.optionalFieldOf("c", "").forGetter(News::c)
    ).apply(i, News::new));

    public boolean involves(String id) { return a.equals(id) || b.equals(id) || c.equals(id); }

    /** A short headline for the ledger, such as "Mira Ash and Tobin Reed fell in love!". */
    public String headline(Society society) {
        String x = society.nameOf(a), y = society.nameOf(b), z = society.nameOf(c);
        return switch (kind) {
            case "arrived" -> x + " settled in the village.";
            case "family" -> x + " came to the village with family: " + y + ".";
            case "born" -> x + " was born to " + y + (c.isEmpty() ? "" : " and " + z) + ".";
            case "grew_up" -> x + " is all grown up.";
            case "sweethearts" -> x + " and " + y + " fell in love!";
            case "married" -> x + " and " + y + " got married!";
            case "passed" -> x + " passed away. They are dearly missed.";
            case "cursed" -> x + " was turned into a zombie villager.";
            case "cured" -> x + " was cured and came home.";
            case "friends" -> x + " and " + y + " became good friends.";
            case "best_friends" -> x + " and " + y + " are now best friends.";
            case "quarrel" -> x + " and " + y + " had a quarrel.";
            case "birthday" -> "It's " + x + "'s birthday! Party by the bell this evening.";
            case "helped" -> c + " answered a notice from " + x + ".";
            case "deed:raid_won" -> c + " helped beat back the raid. The village is safe!";
            case "deed:revived" -> c + " revived " + x + " after " + x + " was knocked out.";
            case "deed:knocked_out_resident" -> c + " knocked " + x + " out cold.";
            case "deed:killed_resident" -> x + " died of the injuries " + c + " gave them.";
            case "deed:killed_golem" -> c + " killed the village's iron golem.";
            case "deed:killed_pet" -> c + " killed " + (b.isEmpty() ? "a pet" : b) + (a.isEmpty() ? "." : ", " + x + "'s pet.");
            default -> x + " has news.";
        };
    }
}
