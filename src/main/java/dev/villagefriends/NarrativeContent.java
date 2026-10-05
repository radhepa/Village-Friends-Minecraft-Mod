package dev.villagefriends;

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

/** Declarative story packs: no scripts or external chat service. Invalid reloads retain the working pack. */
public final class NarrativeContent {
    public record Personality(String id, String label, String hobby, String value, List<String> loves,
            List<String> dislikes, Map<String, List<String>> lines) {}
    public record Request(String id, String title, String item, int count, String prompt, String thanks) {}
    public record Conditions(int confessionVisits, int endingVisits, int endingTrust, boolean requireSharedExperience) {
        public static final Conditions DEFAULT = new Conditions(3, 5, 60, true);
    }
    public record Story(String id, String title, String intro, String confide, String encourage,
            String practical, String gift, List<Request> requests, Conditions conditions) {
        public Story { if (conditions == null) conditions = Conditions.DEFAULT; }
        public Story(String id, String title, String intro, String confide, String encourage, String practical, String gift, List<Request> requests) {
            this(id,title,intro,confide,encourage,practical,gift,requests,Conditions.DEFAULT);
        }
    }
    public record Data(int version, List<Personality> personalities, List<Story> stories) {
        public Personality personality(String id) { return personalities.stream().filter(p -> p.id.equals(id)).findFirst().orElse(personalities.getFirst()); }
        public Story story(String id) { return stories.stream().filter(p -> p.id.equals(id)).findFirst().orElse(null); }
    }
    private static final Gson GSON = new Gson();
    private static volatile Data current = builtin();
    public static Data current() { return current; }
    private static Data builtin() {
        try (var stream = NarrativeContent.class.getResourceAsStream("/data/villagefriends/villagefriends/content.json")) {
            if (stream == null) throw new IllegalStateException("Bundled story pack missing");
            return validate(GSON.fromJson(new InputStreamReader(stream, StandardCharsets.UTF_8), Data.class));
        } catch (Exception e) { throw new IllegalStateException("Cannot read bundled stories", e); }
    }
    public static Data parse(String json) { return validate(GSON.fromJson(json, Data.class)); }
    public static Data validate(Data data) {
        if (data == null || data.version != 1 || data.personalities == null || data.personalities.isEmpty()
                || data.stories == null || data.stories.isEmpty()) throw new IllegalArgumentException("Story pack needs version 1, personalities, and stories");
        var ids = new HashSet<String>();
        for (var p : data.personalities) {
            id(p.id); if (!ids.add(p.id)) throw new IllegalArgumentException("Duplicate personality " + p.id);
            shortText(p.label, 64); shortText(p.hobby, 100); shortText(p.value, 100);
            if (p.loves == null || p.loves.isEmpty() || p.dislikes == null || p.dislikes.isEmpty() || p.lines == null) throw new IllegalArgumentException("Missing preferences or dialogue");
            p.loves.forEach(NarrativeContent::item); p.dislikes.forEach(NarrativeContent::item);
            if (p.loves.stream().anyMatch(p.dislikes::contains)) throw new IllegalArgumentException("Loved and disliked items overlap");
            for (String topic : List.of("chat", "work", "adventure", "joke")) {
                var lines = p.lines.get(topic); if (lines == null || lines.isEmpty()) throw new IllegalArgumentException("Missing topic " + topic);
                lines.forEach(NarrativeContent::text);
            }
        }
        ids.clear();
        for (var s : data.stories) {
            id(s.id); if (!ids.add(s.id)) throw new IllegalArgumentException("Duplicate story " + s.id);
            shortText(s.title, 100); text(s.intro); text(s.confide); text(s.encourage); text(s.practical); item(s.gift);
            var gate = s.conditions;
            if (gate.confessionVisits < 1 || gate.endingVisits < gate.confessionVisits || gate.endingVisits > 100 || gate.endingTrust < 0 || gate.endingTrust > 100)
                throw new IllegalArgumentException("Invalid story conditions");
            if (s.requests == null || s.requests.size() != 3) throw new IllegalArgumentException("Each story needs three requests");
            var requests = new HashSet<String>();
            for (var r : s.requests) {
                id(r.id); if (!requests.add(r.id)) throw new IllegalArgumentException("Duplicate request");
                shortText(r.title, 100); item(r.item); text(r.prompt); text(r.thanks);
                if (r.count < 1 || r.count > 64) throw new IllegalArgumentException("Invalid request count");
            }
        }
        return data;
    }
    private static void id(String s) { if (s == null || !s.matches("[a-z0-9_]{1,48}")) throw new IllegalArgumentException("Invalid content ID"); }
    private static void item(String s) { if (s == null || !s.matches("[a-z0-9_.-]+:[a-z0-9_/.-]+")) throw new IllegalArgumentException("Invalid item ID"); }
    private static void text(String s) { if (s == null || s.isBlank() || s.length() > 1800) throw new IllegalArgumentException("Missing or oversized story text"); }
    private static void shortText(String s, int limit) { text(s); if (s.length() > limit) throw new IllegalArgumentException("Oversized content label"); }
    public static void register() {
        ResourceLoader.get(PackType.SERVER_DATA).registerReloadListener(Identifier.fromNamespaceAndPath("villagefriends", "stories"),
                new SimplePreparableReloadListener<Data>() {
                    @Override protected Data prepare(ResourceManager resources, ProfilerFiller profiler) {
                        var resource = resources.getResource(Identifier.fromNamespaceAndPath("villagefriends", "villagefriends/content.json"));
                        if (resource.isEmpty()) return builtin();
                        try (var reader = resource.get().openAsReader()) {
                            var data = validate(GSON.fromJson(reader, Data.class));
                            var items = new HashSet<String>();
                            for (var p : data.personalities) { items.addAll(p.loves); items.addAll(p.dislikes); }
                            for (var s : data.stories) { items.add(s.gift); for (var r : s.requests) items.add(r.item); }
                            for (var item : items) if (!net.minecraft.core.registries.BuiltInRegistries.ITEM.containsKey(Identifier.parse(item)))
                                throw new IllegalArgumentException("Unknown item " + item);
                            return data;
                        }
                        catch (Exception e) { VillageFriends.LOGGER.error("Story pack rejected; keeping working content: {}", e.getMessage()); return current; }
                    }
                    @Override protected void apply(Data data, ResourceManager resources, ProfilerFiller profiler) { current = data; }
                });
    }
    private NarrativeContent() {}
}
