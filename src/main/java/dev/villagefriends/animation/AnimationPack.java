package dev.villagefriends.animation;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import dev.villagefriends.animation.AnimationClip.Bone;
import dev.villagefriends.animation.AnimationClip.Mirror;
import java.util.*;

/**
 * A resource-pack file under {@code assets/<namespace>/resident_animations/}. Packs only describe
 * motion; the resident director decides when each clip plays. See ANIMATION_PACKS.md for the format.
 */
public record AnimationPack(String id, String name, String description, List<AnimationClip> clips, Set<String> disable) {
    public static final int FORMAT = 1;
    /** Situations the director can ask for. Unknown triggers are rejected to catch typos. */
    public static final Set<String> TRIGGERS = Set.of("idle", "greet", "talk", "chat_speak", "chat_listen",
            "laugh", "delighted", "thanks", "decline", "happy", "love", "angry", "nervous", "hurt", "pet");
    private static final float MAX_ROTATION = 400, MAX_OFFSET = 12, MAX_LENGTH = 30;

    public static AnimationPack parse(String id, String json) {
        try { return parse(id, JsonParser.parseString(json).getAsJsonObject()); }
        catch (IllegalArgumentException e) { throw e; }
        catch (RuntimeException e) { throw new IllegalArgumentException("Animation pack " + id + " is not valid JSON: " + e.getMessage(), e); }
    }
    public static AnimationPack parse(String id, JsonObject root) {
        int format = root.has("format") ? root.get("format").getAsInt() : -1;
        if (format != FORMAT) throw new IllegalArgumentException("Animation pack " + id + " needs \"format\": " + FORMAT);
        String name = text(root, "name", id), description = text(root, "description", "");
        var disable = new LinkedHashSet<String>();
        if (root.has("disable")) for (var e : root.getAsJsonArray("disable")) disable.add(e.getAsString());
        var clips = new ArrayList<AnimationClip>(); var ids = new HashSet<String>();
        if (!root.has("clips") || !root.get("clips").isJsonArray()) throw new IllegalArgumentException("Animation pack " + id + " has no clips array");
        for (var element : root.getAsJsonArray("clips")) {
            var clip = clip(id, element.getAsJsonObject());
            if (!ids.add(clip.id())) throw new IllegalArgumentException("Duplicate clip " + clip.id());
            clips.add(clip);
        }
        return new AnimationPack(id, name, description, List.copyOf(clips), Set.copyOf(disable));
    }

    private static AnimationClip clip(String pack, JsonObject o) {
        String local = text(o, "id", null);
        if (local == null || !local.matches("[a-z0-9_]+")) throw new IllegalArgumentException("Clip ids in " + pack + " must be lowercase words: " + local);
        String id = pack + ":" + local, where = "Clip " + id;
        String trigger = text(o, "trigger", "idle");
        if (!TRIGGERS.contains(trigger)) throw new IllegalArgumentException(where + " has unknown trigger " + trigger);
        float length = number(o, "length", -1);
        if (!(length > 0 && length <= MAX_LENGTH)) throw new IllegalArgumentException(where + " needs a length between 0 and " + MAX_LENGTH + " seconds");
        float weight = number(o, "weight", 1);
        if (!(weight > 0)) throw new IllegalArgumentException(where + " needs a positive weight");
        var require = new ArrayList<Set<String>>();
        if (o.has("require")) for (var e : o.getAsJsonArray("require")) require.add(Set.of(e.getAsString().split("\\|")));
        var avoid = new HashSet<String>();
        if (o.has("avoid")) for (var e : o.getAsJsonArray("avoid")) avoid.add(e.getAsString());
        var boost = new LinkedHashMap<String, Float>();
        if (o.has("boost")) for (var e : o.getAsJsonObject("boost").entrySet()) {
            float b = e.getValue().getAsFloat();
            if (!(b >= 0)) throw new IllegalArgumentException(where + " has a negative boost");
            boost.put(e.getKey(), b);
        }
        float blendIn = .25F, blendOut = .35F;
        if (o.has("blend")) { var b = o.getAsJsonArray("blend"); blendIn = b.get(0).getAsFloat(); blendOut = b.get(1).getAsFloat(); }
        if (blendIn < 0 || blendOut < 0 || blendIn + blendOut > length + 1e-4F) throw new IllegalArgumentException(where + " blends longer than the clip");
        Mirror mirror = switch (text(o, "mirror", "hand")) {
            case "hand" -> Mirror.HAND; case "free" -> Mirror.FREE; case "never" -> Mirror.NEVER;
            default -> throw new IllegalArgumentException(where + " mirror must be hand, free or never");
        };
        boolean overrideItems = "override".equals(text(o, "items", "keep"));
        var rotations = new AnimationTrack[Bone.ALL.length]; var positions = new AnimationTrack[Bone.ALL.length];
        AnimationTrack lid = null, look = null;
        if (!o.has("tracks")) throw new IllegalArgumentException(where + " has no tracks");
        for (var entry : o.getAsJsonObject("tracks").entrySet()) {
            String key = entry.getKey(); int dot = key.indexOf('.');
            String bone = dot < 0 ? key : key.substring(0, dot), channel = dot < 0 ? "" : key.substring(dot + 1);
            if (bone.equals("eyes")) {
                switch (channel) {
                    case "lid" -> lid = track(where, key, entry.getValue(), 1, 0, 1);
                    case "look" -> look = track(where, key, entry.getValue(), 2, -1, 1);
                    default -> throw new IllegalArgumentException(where + " has unknown eye channel " + key);
                }
                continue;
            }
            Bone b;
            try { b = Bone.valueOf(bone.toUpperCase(Locale.ROOT)); }
            catch (IllegalArgumentException e) { throw new IllegalArgumentException(where + " has unknown bone " + bone); }
            switch (channel) {
                case "rot" -> rotations[b.ordinal()] = track(where, key, entry.getValue(), 3, -MAX_ROTATION, MAX_ROTATION);
                case "pos" -> {
                    if (b == Bone.WAIST) throw new IllegalArgumentException(where + ": the waist only rotates");
                    positions[b.ordinal()] = track(where, key, entry.getValue(), 3, -MAX_OFFSET, MAX_OFFSET);
                }
                default -> throw new IllegalArgumentException(where + " channel " + key + " must end in .rot or .pos");
            }
        }
        for (var t : rotations) if (t != null && t.end() > length + 1e-4F) throw new IllegalArgumentException(where + " has keys after its length");
        for (var t : positions) if (t != null && t.end() > length + 1e-4F) throw new IllegalArgumentException(where + " has keys after its length");
        if (lid != null && lid.end() > length + 1e-4F || look != null && look.end() > length + 1e-4F) throw new IllegalArgumentException(where + " has eye keys after its length");
        return new AnimationClip(id, text(o, "name", local), trigger, length, weight, List.copyOf(require), Set.copyOf(avoid),
                Collections.unmodifiableMap(boost), blendIn, blendOut, mirror, overrideItems, rotations, positions, lid, look);
    }

    /** Keys are {@code [time, x, y, z]} (fewer components for eye channels). */
    private static AnimationTrack track(String where, String key, JsonElement element, int width, float min, float max) {
        JsonArray keys = element.getAsJsonArray();
        if (keys.isEmpty()) throw new IllegalArgumentException(where + " track " + key + " is empty");
        float[] times = new float[keys.size()], values = new float[keys.size() * 3];
        for (int i = 0; i < keys.size(); i++) {
            var k = keys.get(i).getAsJsonArray();
            if (k.size() != width + 1) throw new IllegalArgumentException(where + " track " + key + " needs " + (width + 1) + " numbers per key");
            times[i] = k.get(0).getAsFloat();
            if (times[i] < 0 || i > 0 && times[i] <= times[i - 1]) throw new IllegalArgumentException(where + " track " + key + " times must increase from 0");
            for (int c = 0; c < width; c++) {
                float v = k.get(c + 1).getAsFloat();
                if (!Float.isFinite(v) || v < min || v > max) throw new IllegalArgumentException(where + " track " + key + " value out of range: " + v);
                values[i * 3 + c] = v;
            }
        }
        return new AnimationTrack(times, values);
    }
    private static String text(JsonObject o, String key, String fallback) { return o.has(key) ? o.get(key).getAsString() : fallback; }
    private static float number(JsonObject o, String key, float fallback) { return o.has(key) ? o.get(key).getAsFloat() : fallback; }
}
