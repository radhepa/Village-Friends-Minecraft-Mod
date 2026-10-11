package dev.villagefriends.rpg;

import dev.villagefriends.VillageFriends;
import net.minecraft.ChatFormatting;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;

/**
 * Finding the modpack's places ({@link Atlas}). Once a second the pulse asks which structures reach into the
 * player's chunk; if the player stands inside one the Atlas lists, it's found: the first time pays character
 * experience (more for farther, deadlier places) and fills in its line on the Atlas page, and every visit
 * counts for "Find ..." jobs.
 */
public final class Discoveries {
    private Discoveries() {}

    static void look(ServerPlayer p) {
        if (p.isSpectator() || !(p.level() instanceof ServerLevel level)) return;
        var pos = p.blockPosition();
        var nearby = level.structureManager().getAllStructuresAt(pos);
        if (nearby.isEmpty()) return;
        var registry = level.registryAccess().lookupOrThrow(Registries.STRUCTURE);
        for (var structure : nearby.keySet()) {
            var key = registry.getKey(structure);
            var place = key == null ? null : Atlas.ofStructure(key.toString());
            if (place == null || !wanted(p, place)) continue;
            var start = level.structureManager().getStructureAt(pos, structure);
            if (start != null && start.isValid()) found(p, level, place);
        }
    }
    /** New to the player, or a job asks for it. */
    private static boolean wanted(ServerPlayer p, Atlas.Place place) {
        var s = Rpg.sheet(p);
        if (!s.marks().containsKey(Atlas.mark(place))) return true;
        String target = "place:" + place.id();
        return s.quests().stream().anyMatch(q -> q.kind().equals("explore") && q.target().equals(target) && !q.done());
    }

    private static void found(ServerPlayer p, ServerLevel level, Atlas.Place place) {
        var s = Rpg.sheet(p);
        if (!s.marks().containsKey(Atlas.mark(place))) {
            Rpg.set(p, s.mark(Atlas.mark(place), VillageFriends.day(level) + 1));
            long xp = Balance.discoveryXp(place.tier(), s.level());
            p.sendSystemMessage(Component.literal("Discovered " + place.name() + " (" + Modpack.name(place.mod()) + ")! ").withStyle(ChatFormatting.AQUA)
                    .append(Component.literal("+" + xp + " XP. See your Atlas (K).").withStyle(ChatFormatting.GRAY)));
            level.playSound(null, p.blockPosition(), SoundEvents.UI_TOAST_CHALLENGE_COMPLETE, SoundSource.PLAYERS, place.quest() ? .6F : .3F, 1.2F);
            Progress.xp(p, xp, null);
        }
        Quests.advance(p, "explore", "place:" + place.id(), 1);
    }
}
