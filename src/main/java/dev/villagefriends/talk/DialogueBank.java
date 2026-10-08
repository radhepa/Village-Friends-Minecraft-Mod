package dev.villagefriends.talk;

import com.google.gson.Gson;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import net.fabricmc.fabric.api.resource.v1.ResourceLoader;
import net.minecraft.resources.Identifier;
import net.minecraft.server.packs.PackType;
import net.minecraft.server.packs.resources.ResourceManager;
import net.minecraft.server.packs.resources.SimplePreparableReloadListener;
import net.minecraft.util.profiling.ProfilerFiller;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Everything residents can say: pools of handwritten lines keyed by situation ("work.farmer",
 * "weather.rain", "routine.lunch"...) and questions they ask you, with your possible answers. Compiled
 * from tools/dialogue by dialogue.py into a data pack file, so a data pack can add or replace lines.
 * An invalid reload keeps the working bank.
 */
public record DialogueBank(int format, Map<String, List<String>> pools, List<Question> questions) {
    public record Answer(String label, String reply, String flag, String effect, int points, String mood) {}
    /** {@code offer}s are situational and can come up once a day; ordinary questions are asked once. */
    public record Question(String id, boolean offer, List<String> when, List<String> ask, List<Answer> answers) {}

    private static final Logger LOGGER = LoggerFactory.getLogger("VillageFriends");
    private static final Gson GSON = new Gson();
    private static final String PATH = "villagefriends/dialogue.json";
    private static volatile DialogueBank current;

    public static DialogueBank current() {
        var bank = current;
        if (bank == null) current = bank = builtin();
        return bank;
    }
    public List<String> pool(String key) { return pools.getOrDefault(key, List.of()); }
    public boolean has(String key) { return !pool(key).isEmpty(); }
    public Question question(String id) {
        for (var q : questions) if (q.id().equals(id)) return q;
        return null;
    }
    /** Lines, questions and answers (label and reply each), the way the authoring tool counts them. */
    public int size() {
        int n = 0;
        for (var lines : pools.values()) n += lines.size();
        for (var q : questions) n += q.ask().size() + q.answers().size() * 2;
        return n;
    }

    static DialogueBank builtin() {
        try (var stream = DialogueBank.class.getResourceAsStream("/data/villagefriends/" + PATH)) {
            if (stream == null) throw new IllegalStateException("Bundled dialogue missing");
            return validate(GSON.fromJson(new InputStreamReader(stream, StandardCharsets.UTF_8), DialogueBank.class));
        } catch (Exception e) { throw new IllegalStateException("Cannot read bundled dialogue", e); }
    }
    public static DialogueBank parse(String json) { return validate(GSON.fromJson(json, DialogueBank.class)); }
    public static DialogueBank validate(DialogueBank bank) {
        if (bank == null || bank.format != 1 || bank.pools == null || bank.pools.isEmpty() || bank.questions == null)
            throw new IllegalArgumentException("Dialogue needs format 1, pools and questions");
        for (var e : bank.pools.entrySet()) {
            if (!e.getKey().matches("[a-z0-9_.]+")) throw new IllegalArgumentException("Bad pool key " + e.getKey());
            for (var line : e.getValue()) if (line == null || line.isBlank() || line.length() > 300) throw new IllegalArgumentException("Bad line in " + e.getKey());
        }
        var ids = new HashSet<String>();
        for (var q : bank.questions) {
            if (q.id == null || !q.id.matches("[a-z0-9_]{2,40}") || !ids.add(q.id)) throw new IllegalArgumentException("Bad question id " + q.id);
            if (q.ask == null || q.ask.isEmpty() || q.answers == null || q.answers.size() < 2 || q.answers.size() > 4) throw new IllegalArgumentException("Question " + q.id + " needs a question and 2-4 answers");
            for (var a : q.answers) if (a.label == null || a.label.isBlank() || a.label.length() > 30 || a.reply == null || a.reply.isBlank())
                throw new IllegalArgumentException("Bad answer in " + q.id);
        }
        return bank;
    }
    public static void register() {
        ResourceLoader.get(PackType.SERVER_DATA).registerReloadListener(Identifier.fromNamespaceAndPath("villagefriends", "dialogue"),
                new SimplePreparableReloadListener<DialogueBank>() {
                    @Override protected DialogueBank prepare(ResourceManager resources, ProfilerFiller profiler) {
                        var resource = resources.getResource(Identifier.fromNamespaceAndPath("villagefriends", PATH));
                        if (resource.isEmpty()) return builtin();
                        try (var reader = resource.get().openAsReader()) { return validate(GSON.fromJson(reader, DialogueBank.class)); }
                        catch (Exception e) { LOGGER.error("Dialogue rejected; keeping working dialogue: {}", e.getMessage()); return current(); }
                    }
                    @Override protected void apply(DialogueBank bank, ResourceManager resources, ProfilerFiller profiler) { current = bank; }
                });
    }
}
