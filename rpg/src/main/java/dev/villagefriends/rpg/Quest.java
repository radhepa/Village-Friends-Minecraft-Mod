package dev.villagefriends.rpg;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;

/**
 * A job a villager gave the player. Kinds: slay (target = bestiary family), gather (item id, handed
 * over on turn-in), mine (ores|stone|logs|dirt), harvest, fish, breed, enchant, trade, explore
 * ("biome:&lt;id&gt;" or "dim:&lt;id&gt;"). Rewards are fixed when the job is offered.
 */
public record Quest(String id, String kind, String target, int need, int have, String giver, String giverName,
                    String job, int xp, int emeralds, int friendship, String label) {
    public static final Codec<Quest> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.STRING.fieldOf("id").forGetter(Quest::id),
            Codec.STRING.fieldOf("kind").forGetter(Quest::kind),
            Codec.STRING.optionalFieldOf("target", "").forGetter(Quest::target),
            Codec.INT.fieldOf("need").forGetter(Quest::need),
            Codec.INT.optionalFieldOf("have", 0).forGetter(Quest::have),
            Codec.STRING.fieldOf("giver").forGetter(Quest::giver),
            Codec.STRING.optionalFieldOf("giver_name", "").forGetter(Quest::giverName),
            Codec.STRING.optionalFieldOf("job", "").forGetter(Quest::job),
            Codec.INT.optionalFieldOf("xp", 0).forGetter(Quest::xp),
            Codec.INT.optionalFieldOf("emeralds", 0).forGetter(Quest::emeralds),
            Codec.INT.optionalFieldOf("friendship", 0).forGetter(Quest::friendship),
            Codec.STRING.optionalFieldOf("label", "").forGetter(Quest::label)
    ).apply(i, Quest::new));

    public boolean done() { return have >= need; }
    public Quest withHave(int n) { n = Math.clamp(n, 0, need); return n == have ? this : new Quest(id, kind, target, need, n, giver, giverName, job, xp, emeralds, friendship, label); }
    public Quest progress(int n) { return withHave(have + n); }
}
