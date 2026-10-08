package dev.villagefriends.pet;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import dev.villagefriends.animation.AnimationTrack;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;

/**
 * One pose a pet strikes while playing (a play bow, rolling onto its back, batting at string), keyed
 * like resident clips: rotations in degrees and positions in model pixels, added to the cat or dog
 * model's own pose. The root turns about the middle of the body, so a dog can roll over or spin on
 * the spot. Looping tricks repeat until the pet's next trick; the others hold their last key.
 * Tricks are client resources in {@code assets/<namespace>/pet_tricks/*.json}, authored in Python
 * under {@code tools/pets/}.
 */
public record PetTrick(String id, String species, float length, boolean loop, float blendIn, float blendOut,
        AnimationTrack[] rotations, AnimationTrack[] positions) {
    public static final int FORMAT = 1;
    private static final float MAX_ROTATION = 400, MAX_OFFSET = 16, MAX_LENGTH = 20;

    public enum Bone {
        ROOT, HEAD, BODY, UPPER_BODY, TAIL, TAIL_TIP, RIGHT_FRONT_LEG, LEFT_FRONT_LEG, RIGHT_HIND_LEG, LEFT_HIND_LEG;
        public static final Bone[] ALL = values();
    }

    /** Where the trick is at {@code seconds} after it began. */
    public float time(float seconds) { return loop ? seconds % length : Math.min(seconds, length); }
    /** How strongly the trick shows: fading in at the start (and out at the end of a one-shot trick). */
    public float envelope(float seconds) {
        float in = blendIn <= 0 ? 1 : dev.villagefriends.animation.AnimationClip.smooth(seconds / blendIn);
        if (loop) return in;
        float out = blendOut <= 0 ? 1 : dev.villagefriends.animation.AnimationClip.smooth((length - seconds) / blendOut);
        return seconds >= length ? 0 : Math.min(in, out);
    }

    /** Parses a trick file; tricks are keyed {@code species:id}. */
    public static Map<String, PetTrick> parse(String file, String json) {
        JsonObject root;
        try { root = JsonParser.parseString(json).getAsJsonObject(); }
        catch (RuntimeException e) { throw new IllegalArgumentException("Pet tricks " + file + " is not valid JSON: " + e.getMessage(), e); }
        if (!root.has("format") || root.get("format").getAsInt() != FORMAT) throw new IllegalArgumentException("Pet tricks " + file + " needs \"format\": " + FORMAT);
        var tricks = new HashMap<String, PetTrick>();
        for (var element : root.getAsJsonArray("tricks")) {
            var trick = trick(element.getAsJsonObject());
            if (tricks.put(trick.species() + ":" + trick.id(), trick) != null) throw new IllegalArgumentException("Duplicate pet trick " + trick.species() + ":" + trick.id());
        }
        return Map.copyOf(tricks);
    }
    private static PetTrick trick(JsonObject o) {
        String id = o.get("id").getAsString(), species = o.get("species").getAsString(), where = "Pet trick " + species + ":" + id;
        if (!id.matches("[a-z0-9_]+")) throw new IllegalArgumentException(where + " needs a lowercase id");
        if (!species.equals(PetKeeping.CAT) && !species.equals(PetKeeping.DOG)) throw new IllegalArgumentException(where + " is for a cat or a dog");
        float length = o.get("length").getAsFloat();
        if (!(length > 0 && length <= MAX_LENGTH)) throw new IllegalArgumentException(where + " needs a length up to " + MAX_LENGTH + " seconds");
        boolean loop = o.has("loop") && o.get("loop").getAsBoolean();
        float in = .2F, out = .3F;
        if (o.has("blend")) { var b = o.getAsJsonArray("blend"); in = b.get(0).getAsFloat(); out = b.get(1).getAsFloat(); }
        var rotations = new AnimationTrack[Bone.ALL.length]; var positions = new AnimationTrack[Bone.ALL.length];
        for (var entry : o.getAsJsonObject("tracks").entrySet()) {
            String key = entry.getKey(); int dot = key.indexOf('.');
            if (dot < 0) throw new IllegalArgumentException(where + " track " + key + " must end in .rot or .pos");
            Bone bone;
            try { bone = Bone.valueOf(key.substring(0, dot).toUpperCase(Locale.ROOT)); }
            catch (IllegalArgumentException e) { throw new IllegalArgumentException(where + " has unknown bone " + key); }
            boolean rotation = key.endsWith(".rot");
            if (!rotation && !key.endsWith(".pos")) throw new IllegalArgumentException(where + " track " + key + " must end in .rot or .pos");
            var track = track(where, key, entry.getValue().getAsJsonArray(), rotation ? MAX_ROTATION : MAX_OFFSET);
            if (track.end() > length + 1e-4F) throw new IllegalArgumentException(where + " has keys after its length");
            (rotation ? rotations : positions)[bone.ordinal()] = track;
        }
        return new PetTrick(id, species, length, loop, in, out, rotations, positions);
    }
    private static AnimationTrack track(String where, String key, JsonArray keys, float limit) {
        if (keys.isEmpty()) throw new IllegalArgumentException(where + " track " + key + " is empty");
        float[] times = new float[keys.size()], values = new float[keys.size() * 3];
        for (int i = 0; i < keys.size(); i++) {
            var k = keys.get(i).getAsJsonArray();
            if (k.size() != 4) throw new IllegalArgumentException(where + " track " + key + " needs [time, x, y, z] keys");
            times[i] = k.get(0).getAsFloat();
            if (times[i] < 0 || i > 0 && times[i] <= times[i - 1]) throw new IllegalArgumentException(where + " track " + key + " times must increase from 0");
            for (int c = 0; c < 3; c++) {
                float v = k.get(c + 1).getAsFloat();
                if (!Float.isFinite(v) || Math.abs(v) > limit) throw new IllegalArgumentException(where + " track " + key + " value out of range: " + v);
                values[i * 3 + c] = v;
            }
        }
        return new AnimationTrack(times, values);
    }
}
