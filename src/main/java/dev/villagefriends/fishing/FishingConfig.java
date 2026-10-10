package dev.villagefriends.fishing;

import com.google.gson.GsonBuilder;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import net.fabricmc.loader.api.FabricLoader;

/**
 * {@code config/villagefriends-fishing.json}: {@code "minigame": true} plays the catch-bar minigame when a fish
 * bites; {@code false} goes back to vanilla fishing (reel in when the bobber dips). Either way the catch comes
 * from the fish table. {@code /fishing minigame on|off} changes it and saves the file.
 */
public final class FishingConfig {
    private static boolean minigame = true;
    private static Path path() { return FabricLoader.getInstance().getConfigDir().resolve("villagefriends-fishing.json"); }

    public static boolean minigame() { return minigame; }

    public static void load() {
        var file = path();
        try {
            if (Files.exists(file)) {
                JsonObject o = JsonParser.parseString(Files.readString(file, StandardCharsets.UTF_8)).getAsJsonObject();
                if (o.has("minigame")) minigame = o.get("minigame").getAsBoolean();
            } else save();
        } catch (IOException | RuntimeException e) {
            minigame = true;
        }
    }
    public static void minigame(boolean on) { minigame = on; save(); }
    private static void save() {
        var o = new JsonObject();
        o.addProperty("minigame", minigame);
        try {
            Files.createDirectories(path().getParent());
            Files.writeString(path(), new GsonBuilder().setPrettyPrinting().create().toJson(o) + "\n", StandardCharsets.UTF_8);
        } catch (IOException ignored) {
            // A read-only config folder just means the setting isn't remembered.
        }
    }

    private FishingConfig() {}
}
