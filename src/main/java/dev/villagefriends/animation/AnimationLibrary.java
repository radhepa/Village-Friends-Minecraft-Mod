package dev.villagefriends.animation;

import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.*;

/** Every loaded pack's clips, indexed by trigger. Later packs replace clips with the same id. */
public final class AnimationLibrary {
    public static final String BUILTIN = "village_life";
    /** The tag for residents sitting down, and the triggers that only ever use clips written for sitting. */
    public static final String SEATED = "seated";
    private static final Set<String> SEATED_ONLY = Set.of("idle", "chat_speak", "chat_listen", "talk");
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
        // Sitting at a table: idles and chats come only from seated clips; reactions use one if any fits.
        if (tags.contains(SEATED)) {
            var seated = new ArrayList<AnimationClip>();
            for (var clip : options) if (clip.seated() && chance(clip, tags, recent) > 0) seated.add(clip);
            if (!seated.isEmpty() || SEATED_ONLY.contains(trigger)) options = seated;
        }
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

    /** The packs that ship with the mod, in load order. */
    public static List<String> bundled() { return List.of(BUILTIN, "tavern"); }
    public static AnimationLibrary builtin() {
        var packs = new ArrayList<AnimationPack>();
        for (String id : bundled()) {
            try (InputStream in = AnimationLibrary.class.getResourceAsStream("/assets/villagefriends/resident_animations/" + id + ".json")) {
                if (in == null) { if (id.equals(BUILTIN)) throw new IllegalStateException("Bundled animation pack missing"); continue; }
                packs.add(AnimationPack.parse(id, new String(in.readAllBytes(), StandardCharsets.UTF_8)));
            } catch (java.io.IOException e) { throw new IllegalStateException("Cannot read the bundled animation pack " + id, e); }
        }
        return new AnimationLibrary(packs);
    }
}
