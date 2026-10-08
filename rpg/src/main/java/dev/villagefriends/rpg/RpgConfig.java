package dev.villagefriends.rpg;

import com.google.gson.GsonBuilder;
import net.fabricmc.loader.api.FabricLoader;

import java.nio.file.Files;

/** config/villagefriends_rpg.json: a few global knobs over {@link Balance}. Written with defaults on first run. */
public final class RpgConfig {
    private RpgConfig() {}
    /** Field names are the JSON keys. */
    static final class Values {
        double xpRate = 1, skillXpRate = 1, deathPenalty = .25, bossBonusShare = .5, bossHitCap = .04;
        boolean hardStart = true;
        String _help = "xpRate/skillXpRate scale experience; deathPenalty is the share of level progress lost on death; "
                + "bossBonusShare is how much of your damage bonus counts against bosses; bossHitCap caps that bonus per hit "
                + "as a share of the boss's max health; hardStart starts you at 6 hearts and hungrier.";
    }

    public static void load() {
        var gson = new GsonBuilder().setPrettyPrinting().create();
        var file = FabricLoader.getInstance().getConfigDir().resolve("villagefriends_rpg.json");
        var v = new Values();
        try {
            if (Files.exists(file)) { var read = gson.fromJson(Files.readString(file), Values.class); if (read != null) v = read; }
            Files.writeString(file, gson.toJson(v));
        } catch (Exception e) { Rpg.LOGGER.warn("Couldn't read {}, using defaults: {}", file, e.toString()); }
        Balance.xpRate = Math.max(0, v.xpRate); Balance.skillXpRate = Math.max(0, v.skillXpRate);
        Balance.deathPenalty = Math.clamp(v.deathPenalty, 0, 1); Balance.bossBonusShare = Math.clamp(v.bossBonusShare, 0, 1);
        Balance.bossHitCap = Math.clamp(v.bossHitCap, 0, 1); Balance.hardStart = v.hardStart;
    }
}
