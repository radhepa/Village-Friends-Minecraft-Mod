package dev.villagefriends.rpg;

import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.network.protocol.game.ClientboundSetSubtitleTextPacket;
import net.minecraft.network.protocol.game.ClientboundSetTitleTextPacket;
import net.minecraft.network.protocol.game.ClientboundSetTitlesAnimationPacket;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;

/** Hands out character and skill experience, and celebrates level-ups, skill-ups and new mastery tiers. */
public final class Progress {
    private Progress() {}

    /** Whole points from a fractional amount, rounding the remainder up by chance so small gains still add up. */
    static long roll(ServerPlayer p, double v) { long whole = (long) Math.floor(v); return whole + (p.getRandom().nextDouble() < v - whole ? 1 : 0); }

    /** Character experience; Wisdom and the config rate apply. {@code why} shows on the action bar when given. */
    public static void xp(ServerPlayer p, double raw, String why) {
        var s = Rpg.sheet(p);
        if (s.level() >= Balance.MAX_LEVEL) return;
        long amount = roll(p, raw * Balance.xpRate * (1 + Balance.WIS_XP * s.attr(Attr.WISDOM)));
        if (amount <= 0) return;
        var next = s.gain(amount);
        Rpg.set(p, next);
        if (why != null) p.sendSystemMessage(Component.literal("+" + amount + " XP " + why).withStyle(ChatFormatting.GREEN), true);
        if (next.level() > s.level()) levelUp(p, s.level(), next);
    }

    private static void levelUp(ServerPlayer p, int from, Sheet s) {
        Life.apply(p);
        if (p.connection == null) return;
        int gained = Balance.pointsThrough(s.level()) - Balance.pointsThrough(from);
        p.connection.send(new ClientboundSetTitlesAnimationPacket(8, 50, 20));
        p.connection.send(new ClientboundSetTitleTextPacket(Component.literal("Level " + s.level()).withStyle(ChatFormatting.GOLD)));
        p.connection.send(new ClientboundSetSubtitleTextPacket(Component.literal("+" + gained + " attribute points - press K")));
        p.level().playSound(null, p.blockPosition(), SoundEvents.PLAYER_LEVELUP, SoundSource.PLAYERS, 1, .8F);
        if (p.level() instanceof ServerLevel level) level.sendParticles(ParticleTypes.TOTEM_OF_UNDYING, p.getX(), p.getY() + 1, p.getZ(), 40, .5, .8, .5, .3);
        if (!Balance.title(from).equals(Balance.title(s.level())))
            p.sendSystemMessage(Component.literal("You are now known as a " + Balance.title(s.level()) + ".").withStyle(ChatFormatting.GOLD));
        if (s.level() == 30 || s.level() == 60) p.sendSystemMessage(Component.literal("You can now take on " + Balance.maxQuests(s.level()) + " jobs at once.").withStyle(ChatFormatting.YELLOW));
    }

    /** Skill experience; Wisdom and the config rate apply. */
    public static void skill(ServerPlayer p, Skill skill, double raw) {
        var s = Rpg.sheet(p);
        if (s.skill(skill) >= Balance.SKILL_CAP) return;
        long amount = roll(p, raw * Balance.skillXpRate * (1 + Balance.WIS_XP * s.attr(Attr.WISDOM)));
        if (amount <= 0) return;
        var next = s.skillGain(skill, amount);
        Rpg.set(p, next);
        int before = s.skill(skill), after = next.skill(skill);
        if (after > before) {
            Life.apply(p);
            p.sendSystemMessage(Component.literal(skill.label + " " + after + ": " + skill.effect(after)).withStyle(ChatFormatting.AQUA), true);
            p.level().playSound(null, p.blockPosition(), SoundEvents.EXPERIENCE_ORB_PICKUP, SoundSource.PLAYERS, .6F, .7F + after * .02F);
        }
    }

    /** A new mastery tier against a monster family. */
    static void mastery(ServerPlayer p, Bestiary.Family f, int tier) {
        if (p.connection == null) return;
        String rank = Balance.tierName(tier);
        p.connection.send(new ClientboundSetTitlesAnimationPacket(8, 50, 20));
        p.connection.send(new ClientboundSetTitleTextPacket(Component.literal(rank).withStyle(ChatFormatting.LIGHT_PURPLE)));
        String unlock = f.perks().stream().filter(k -> k.tier() == tier).map(k -> k.name() + ": " + k.desc()).findFirst().orElse("");
        p.connection.send(new ClientboundSetSubtitleTextPacket(Component.literal(f.label() + (unlock.isEmpty() ? " - +2% damage, -2% damage taken" : " - " + unlock.substring(0, unlock.indexOf(':'))))));
        p.sendSystemMessage(Component.literal(f.label() + " mastery: " + rank + ". +2% damage to them, -2% damage from them"
                + (unlock.isEmpty() ? "." : ". Unlocked " + unlock + ".")).withStyle(ChatFormatting.LIGHT_PURPLE));
        p.level().playSound(null, p.blockPosition(), SoundEvents.UI_TOAST_CHALLENGE_COMPLETE, SoundSource.PLAYERS, .7F, 1);
    }
}
