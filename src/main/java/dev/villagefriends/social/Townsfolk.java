package dev.villagefriends.social;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import java.util.HashMap;
import java.util.Map;

/**
 * One resident as their village knows them. Saved with the village, so neighbors can remember and
 * talk about each other even while they are unloaded. {@code kin} maps another resident's ID to what
 * that resident is to this one ("parent", "child", "sibling" or "spouse").
 */
public record Townsfolk(String id, String name, String gender, String job, String personality, boolean adult,
        long joined, long seen, String status, String partner, long partnerSince, boolean married,
        Map<String, String> kin, String household) {
    public static final String HOME = "home", PASSED = "passed", CURSED = "cursed";
    public static final Codec<Townsfolk> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.STRING.fieldOf("id").forGetter(Townsfolk::id),
            Codec.STRING.fieldOf("name").forGetter(Townsfolk::name),
            Codec.STRING.optionalFieldOf("gender", "NON_BINARY").forGetter(Townsfolk::gender),
            Codec.STRING.optionalFieldOf("job", "none").forGetter(Townsfolk::job),
            Codec.STRING.optionalFieldOf("personality", "warmhearted").forGetter(Townsfolk::personality),
            Codec.BOOL.optionalFieldOf("adult", true).forGetter(Townsfolk::adult),
            Codec.LONG.optionalFieldOf("joined", 0L).forGetter(Townsfolk::joined),
            Codec.LONG.optionalFieldOf("seen", 0L).forGetter(Townsfolk::seen),
            Codec.STRING.optionalFieldOf("status", HOME).forGetter(Townsfolk::status),
            Codec.STRING.optionalFieldOf("partner", "").forGetter(Townsfolk::partner),
            Codec.LONG.optionalFieldOf("partner_since", -1L).forGetter(Townsfolk::partnerSince),
            Codec.BOOL.optionalFieldOf("married", false).forGetter(Townsfolk::married),
            Codec.unboundedMap(Codec.STRING, Codec.STRING).optionalFieldOf("kin", Map.of()).forGetter(Townsfolk::kin),
            Codec.STRING.optionalFieldOf("household", "").forGetter(Townsfolk::household)
    ).apply(i, Townsfolk::new));

    public Townsfolk {
        name = name == null || name.isBlank() ? "Neighbor" : name;
        gender = gender == null ? "NON_BINARY" : gender;
        job = job == null ? "none" : job;
        personality = personality == null ? "warmhearted" : personality;
        status = status == null ? HOME : status;
        partner = partner == null ? "" : partner;
        kin = Map.copyOf(kin);
        household = household == null ? "" : household;
    }

    public static Townsfolk newcomer(String id, String name, String gender, String job, String personality, boolean adult, long day) {
        return new Townsfolk(id, name, gender, job, personality, adult, day, day, HOME, "", -1, false, Map.of(), "");
    }

    public boolean living() { return !status.equals(PASSED); }
    public boolean home() { return status.equals(HOME); }
    public boolean single() { return partner.isEmpty(); }
    public String kinOf(String other) { return kin.getOrDefault(other, ""); }

    public Townsfolk seen(String newName, String newJob, boolean nowAdult, long day) {
        return new Townsfolk(id, newName, gender, newJob, personality, nowAdult, joined, Math.max(seen, day), status, partner, partnerSince, married, kin, household);
    }
    public Townsfolk status(String next) {
        return new Townsfolk(id, name, gender, job, personality, adult, joined, seen, next, partner, partnerSince, married, kin, household);
    }
    public Townsfolk partner(String other, long since, boolean wed) {
        return new Townsfolk(id, name, gender, job, personality, adult, joined, seen, status, other, since, wed, kin, household);
    }
    public Townsfolk household(String next) {
        return new Townsfolk(id, name, gender, job, personality, adult, joined, seen, status, partner, partnerSince, married, kin, next);
    }
    public Townsfolk kin(String other, String relation) {
        if (other.equals(id) || relation.equals(kin.get(other))) return this;
        var next = new HashMap<>(kin); next.put(other, relation);
        return new Townsfolk(id, name, gender, job, personality, adult, joined, seen, status, partner, partnerSince, married, next, household);
    }
}
