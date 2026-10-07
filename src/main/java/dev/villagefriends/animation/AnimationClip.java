package dev.villagefriends.animation;

import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * One authored resident animation. Rotations are degrees added to the resident's live pose;
 * positions are model pixels. {@link #require} entries are any-of groups ({@code "job:farmer|job:fisherman"})
 * that must all match the resident's situation; {@link #avoid} tags rule the clip out; {@link #boost}
 * multiplies the weight for each matching tag.
 */
public record AnimationClip(String id, String name, String trigger, float length, float weight,
        List<Set<String>> require, Set<String> avoid, Map<String, Float> boost,
        float blendIn, float blendOut, Mirror mirror, boolean overrideItems,
        AnimationTrack[] rotations, AnimationTrack[] positions, AnimationTrack lid, AnimationTrack look) {

    public enum Bone {
        ROOT, WAIST, BODY, HEAD, RIGHT_ARM, LEFT_ARM, RIGHT_LEG, LEFT_LEG;
        public static final Bone[] ALL = values();
        public Bone mirrored() {
            return switch (this) {
                case RIGHT_ARM -> LEFT_ARM; case LEFT_ARM -> RIGHT_ARM;
                case RIGHT_LEG -> LEFT_LEG; case LEFT_LEG -> RIGHT_LEG;
                default -> this;
            };
        }
    }
    /** HAND follows the resident's handedness; FREE may also be mirrored at random for variety. */
    public enum Mirror { HAND, FREE, NEVER }

    public boolean eligible(Set<String> tags) {
        for (var group : require) {
            boolean any = false;
            for (String tag : group) if (tags.contains(tag)) { any = true; break; }
            if (!any) return false;
        }
        for (String tag : avoid) if (tags.contains(tag)) return false;
        return true;
    }
    public float weightFor(Set<String> tags) {
        float w = weight;
        for (var entry : boost.entrySet()) if (tags.contains(entry.getKey())) w *= entry.getValue();
        return w;
    }
    /** Fades the clip in and out so interrupted or overlapping clips never pop. */
    public float envelope(float t) {
        if (t < 0 || t > length) return 0;
        float in = blendIn <= 0 ? 1 : smooth(t / blendIn), out = blendOut <= 0 ? 1 : smooth((length - t) / blendOut);
        return Math.min(in, out);
    }
    public boolean uses(Bone bone) { return rotations[bone.ordinal()] != null || positions[bone.ordinal()] != null; }

    public static float smooth(float value) {
        float t = Math.max(0, Math.min(1, value)); return t * t * (3 - 2 * t);
    }
}
