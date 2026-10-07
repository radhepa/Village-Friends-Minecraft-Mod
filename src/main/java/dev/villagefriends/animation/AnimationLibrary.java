package dev.villagefriends.animation;

import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.*;

/** Every loaded pack's clips, indexed by trigger. Later packs replace clips with the same id. */
public final class AnimationLibrary {
    public static final String BUILTIN = "village_life";
    private static volatile AnimationLibrary current = builtin();
    private final List<AnimationPack> packs;
    private final Map<String, AnimationClip> clips;
    private final Map<String, List<AnimationClip>> byTrigger;

    public AnimationLibrary(List<AnimationPack> packs) {
        this.packs = List.copyOf(packs);
        var all = new LinkedHashMap<String, AnimationClip>(); var disabled = new HashSet<String>();
        for (var pack : packs) { for (var clip : pack.clips()) all.put(clip.id(), clip); disabled.addAll(pack.disable()); }
        all.keySet().removeAll(disabled);
        clips = Collections.unmodifiableMap(all);
        var index = new HashMap<String, List<AnimationClip>>();
        for (var clip : all.values()) index.computeIfAbsent(clip.trigger(), t -> new ArrayList<>()).add(clip);
        index.replaceAll((t, list) -> List.copyOf(list));
        byTrigger = Map.copyOf(index);
    }

    public static AnimationLibrary current() { return current; }
    public static void install(AnimationLibrary library) { current = library; }
    public List<AnimationPack> packs() { return packs; }
    public Collection<AnimationClip> clips() { return clips.values(); }
    public AnimationClip clip(String id) { return clips.get(id); }
    public List<AnimationClip> clips(String trigger) { return byTrigger.getOrDefault(trigger, List.of()); }

    /**
     * Weighted choice among the trigger's eligible clips. Recently played clips are strongly
     * discouraged so a resident rarely repeats themselves.
     */
    public AnimationClip pick(String trigger, Set<String> tags, Random random, String... recent) {
        var options = clips(trigger);
        float total = 0;
        for (var clip : options) total += chance(clip, tags, recent);
        if (total <= 0) return null;
        float roll = random.nextFloat() * total;
        for (var clip : options) {
            float w = chance(clip, tags, recent);
            if (w <= 0) continue;
            if ((roll -= w) <= 0) return clip;
        }
        for (int i = options.size() - 1; i >= 0; i--) if (chance(options.get(i), tags, recent) > 0) return options.get(i);
        return null;
    }
    private static float chance(AnimationClip clip, Set<String> tags, String[] recent) {
        if (!clip.eligible(tags)) return 0;
        float w = clip.weightFor(tags);
        for (String id : recent) if (clip.id().equals(id)) w *= .06F;
        return w;
    }

    public static AnimationLibrary builtin() {
        try (InputStream in = AnimationLibrary.class.getResourceAsStream("/assets/villagefriends/resident_animations/" + BUILTIN + ".json")) {
            if (in == null) throw new IllegalStateException("Bundled animation pack missing");
            return new AnimationLibrary(List.of(AnimationPack.parse(BUILTIN, new String(in.readAllBytes(), StandardCharsets.UTF_8))));
        } catch (java.io.IOException e) { throw new IllegalStateException("Cannot read the bundled animation pack", e); }
    }
}
