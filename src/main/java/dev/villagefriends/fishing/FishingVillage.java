package dev.villagefriends.fishing;

import dev.villagefriends.VillageSettlements;
import java.util.ArrayList;
import java.util.Map;
import java.util.Random;
import net.fabricmc.fabric.api.attachment.v1.AttachmentTarget;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.npc.villager.Villager;

/**
 * Fishing in village life. Residents tell tall tales of legendary fish (true ones: the hints come from the
 * fish table through {@link Tales}), and a tale you've heard goes into your angler's journal; they marvel at the
 * legends you've landed, look forward to the season's contest and gossip about who won it, fishermen talk shop
 * and the fisherman cries his wares. Messages in bottles hold tales too. One {@link #talk} call from
 * {@code TalkWorld} fills the dialogue placeholders; {@link #heard} logs a tale once it's been told.
 */
public final class FishingVillage {
    private static final Random RANDOM = new Random();

    /** Fills {legend}, {legend_where}, {legend_when}, {contest_when}, {winner}, {catch} for this resident and player. */
    public static void talk(Villager v, ServerPlayer p, Map<String, String> fill) {
        if (!(v.level() instanceof ServerLevel level)) return;
        var journal = Angling.journal(p);
        // A legend the player has landed is the talk of the village; otherwise a tall tale, of one they haven't caught.
        var caught = new ArrayList<Fish>();
        for (var f : FishTable.all()) if (f.legendary() && journal.caught(f.id())) caught.add(f);
        Fish legend;
        if (!caught.isEmpty() && RANDOM.nextInt(3) == 0) { legend = caught.get(RANDOM.nextInt(caught.size())); fill.put("tale_caught", "1"); }
        else {
            var known = new java.util.HashSet<String>();
            for (var f : caught) known.add(f.id());
            legend = Tales.legend(FishTable.all(), Angling.region(level, v.blockPosition()), known, RANDOM);
        }
        if (legend != null) {
            fill.put("legend", legend.name().startsWith("The ") ? "the " + legend.name().substring(4) : legend.name());
            fill.put("legend_where", Tales.where(legend));
            fill.put("legend_when", Tales.when(legend));
            fill.put("legend_id", legend.id());
        }
        var village = VillageSettlements.home(v);
        if (village != null) {
            long today = dev.villagefriends.VillageFriends.day(level);
            int until = Contest.daysUntil(today);
            if (until == 0 && Contest.phase(today, dev.villagefriends.ResidentRoutines.timeOfDay(level)) != Contest.Phase.OVER) fill.put("contest_when", "today");
            else if (until > 0 && until <= 5) fill.put("contest_when", dev.villagefriends.social.Calendar.when(until));
            var won = Contests.recentWinner(level, village.id(), today);
            if (won != null) {
                if (won.player()) { if (won.key().equals(p.getUUID().toString())) fill.put("contest_won", "player"); }
                else if (DockAnglers.lastCatch(v) == null) { // {catch} is their own fresh catch otherwise
                    fill.put("contest_won", "resident");
                    fill.put("winner", first(won.name()));
                    var f = FishTable.get(won.fish());
                    if (f != null) fill.put("catch", f.name().toLowerCase(java.util.Locale.ROOT));
                }
            }
        }
        var landed = DockAnglers.lastCatch(v);
        if (landed != null) { fill.put("catch", landed.name().toLowerCase(java.util.Locale.ROOT)); fill.put("landed", "1"); }
        if (DockAnglers.angling(v)) fill.put("angling", "1");
    }
    private static String first(String name) { int space = name.indexOf(' '); return space > 0 ? name.substring(0, space) : name; }

    /** After a resident told a tall tale: it goes in the player's journal (with a note the first time). */
    public static void heard(ServerPlayer p, String legend) {
        if (legend == null) return;
        var journal = Angling.journal(p);
        if (journal.heard(legend) || FishTable.get(legend) == null) return;
        ((AttachmentTarget) p).setAttached(Fishing.JOURNAL, journal.hear(legend));
        p.sendOverlayMessage(Component.literal("Noted in your angler's journal: the tale of " + FishTable.get(legend).name() + ".").withStyle(ChatFormatting.AQUA));
    }

    /** A message in a bottle: an old angler's note about a legend, noted in the journal. */
    static void readBottle(ServerPlayer p) {
        var journal = Angling.journal(p);
        var level = (ServerLevel) p.level();
        // A note is worth finding: it tells of a legend the player hasn't heard of yet, while there are any.
        var unheard = FishTable.all().stream().filter(f -> f.legendary() && !journal.heard(f.id())).toList();
        var legend = unheard.isEmpty() ? Tales.legend(FishTable.all(), Angling.region(level, p.blockPosition()), journal.tales(), RANDOM)
                : unheard.get(RANDOM.nextInt(unheard.size()));
        if (legend == null) return;
        String[] openings = {"To whoever finds this: ", "My last cast, set down so it isn't lost: ", "Never believed it till I saw it. ", "For my grandchildren: "};
        p.sendSystemMessage(Component.literal("The note reads: \"" + openings[RANDOM.nextInt(openings.length)] + legend.name() + " lives in " + Tales.where(legend)
                + " and bites " + Tales.when(legend) + ".\"").withStyle(ChatFormatting.ITALIC, ChatFormatting.GRAY));
        heard(p, legend.id());
    }

    /** A player landed a legend: residents near by cheer. */
    static void legendCaught(ServerPlayer p, Fish fish) {
        var level = (ServerLevel) p.level();
        for (var v : level.getEntitiesOfClass(Villager.class, p.getBoundingBox().inflate(16), Villager::isAlive))
            dev.villagefriends.VillageSocieties.emote(v, dev.villagefriends.Emote.EXCLAIM, v.getRandom().nextInt(20));
    }

    /** Which village type's look a village's dock and water have: from the biome at its centre. */
    public static String villageType(ServerLevel level, BlockPos center) {
        var key = level.getBiome(center).unwrapKey().map(k -> k.identifier().getPath()).orElse("plains");
        return switch (key) {
            case "desert" -> "desert";
            case "savanna", "savanna_plateau", "windswept_savanna" -> "savanna";
            case "snowy_plains", "ice_spikes", "snowy_taiga", "snowy_slopes" -> "snowy";
            case "taiga", "old_growth_pine_taiga", "old_growth_spruce_taiga" -> "taiga";
            default -> "plains";
        };
    }

    private FishingVillage() {}
}
