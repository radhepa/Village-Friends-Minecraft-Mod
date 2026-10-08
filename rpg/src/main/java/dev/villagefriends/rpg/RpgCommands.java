package dev.villagefriends.rpg;

import com.mojang.brigadier.CommandDispatcher;
import com.mojang.brigadier.arguments.IntegerArgumentType;
import com.mojang.brigadier.arguments.StringArgumentType;
import com.mojang.brigadier.context.CommandContext;
import com.mojang.brigadier.exceptions.CommandSyntaxException;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.commands.Commands;
import net.minecraft.commands.arguments.EntityArgument;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;

import java.util.function.UnaryOperator;

/** /rpg shows your character in chat; /rpg admin ... edits a player's sheet (operators only, for testing). */
public final class RpgCommands {
    private RpgCommands() {}
    static void register(CommandDispatcher<CommandSourceStack> d) {
        d.register(Commands.literal("rpg")
                .executes(c -> { summary(c.getSource(), c.getSource().getPlayerOrException()); return 1; })
                .then(Commands.literal("admin").requires(Commands.hasPermission(Commands.LEVEL_GAMEMASTERS))
                        .then(Commands.argument("player", EntityArgument.player())
                                .then(Commands.literal("level").then(Commands.argument("level", IntegerArgumentType.integer(1, Balance.MAX_LEVEL))
                                        .executes(c -> edit(c, s -> s.withLevel(IntegerArgumentType.getInteger(c, "level"))))))
                                .then(Commands.literal("xp").then(Commands.argument("amount", IntegerArgumentType.integer(1))
                                        .executes(c -> { Progress.xp(target(c), IntegerArgumentType.getInteger(c, "amount") / Balance.xpRate, "(admin)"); return 1; })))
                                .then(Commands.literal("skill").then(Commands.argument("skill", StringArgumentType.word())
                                        .then(Commands.argument("level", IntegerArgumentType.integer(0, Balance.SKILL_CAP)).executes(c -> {
                                            var sk = skill(StringArgumentType.getString(c, "skill")); int l = IntegerArgumentType.getInteger(c, "level");
                                            return sk == null ? 0 : edit(c, s -> s.withSkillXp(sk, xpFor(l)));
                                        }))))
                                .then(Commands.literal("kills").then(Commands.argument("family", StringArgumentType.word())
                                        .then(Commands.argument("count", IntegerArgumentType.integer(0)).executes(c -> {
                                            var f = Bestiary.byId(StringArgumentType.getString(c, "family")); int n = IntegerArgumentType.getInteger(c, "count");
                                            return f == null ? 0 : edit(c, s -> s.kill(f.id(), n - s.kills(f.id())));
                                        }))))
                                .then(Commands.literal("reset").executes(c -> edit(c, s -> Sheet.NEW))))));
    }
    private static ServerPlayer target(CommandContext<CommandSourceStack> c) throws CommandSyntaxException { return EntityArgument.getPlayer(c, "player"); }
    private static int edit(CommandContext<CommandSourceStack> c, UnaryOperator<Sheet> fn) throws CommandSyntaxException {
        var p = target(c); Rpg.set(p, fn.apply(Rpg.sheet(p))); Life.apply(p);
        c.getSource().sendSuccess(() -> Component.literal("Updated " + p.getName().getString() + "'s character."), true);
        return 1;
    }
    private static Skill skill(String id) { for (var s : Skill.values()) if (s.id().equals(id)) return s; return null; }
    private static long xpFor(int level) { long t = 0; for (int s = 0; s < level; s++) t += Balance.skillNeed(s); return t; }
    private static void summary(CommandSourceStack src, ServerPlayer p) {
        var s = Rpg.sheet(p);
        src.sendSystemMessage(Component.literal("Level " + s.level() + " " + Balance.title(s.level()) + " - " + s.xp() + "/" + Balance.need(s.level()) + " XP, "
                + s.points() + " unspent points, " + s.quests().size() + " jobs, " + s.masteries() + " Legend masteries. Press K for the full sheet."));
    }
}
