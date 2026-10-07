package dev.villagefriends.client;

import dev.villagefriends.animation.AnimationClip;

/** One clip sampled for this frame: the director fills it, both resident and armor models read it. */
public final class AnimationLayer {
    public AnimationClip clip;
    /** Seconds into the clip. */
    public float time;
    /** Blend weight for the whole clip. */
    public float weight;
    /** Extra weight for root, waist and legs: walking keeps its own feet. */
    public float lowerBody = 1;
    public boolean mirror;

    public void set(AnimationClip clip, float time, float weight, boolean mirror, float lowerBody) {
        this.clip = clip; this.time = time; this.weight = weight; this.mirror = mirror; this.lowerBody = lowerBody;
    }
    public void clear() { clip = null; weight = 0; time = 0; lowerBody = 1; mirror = false; }
    public boolean active() { return clip != null && weight > 0; }
}
