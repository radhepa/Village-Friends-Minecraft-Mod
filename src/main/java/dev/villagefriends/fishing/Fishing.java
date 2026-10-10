package dev.villagefriends.fishing;

import com.mojang.brigadier.arguments.StringArgumentType;
import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import io.netty.buffer.ByteBuf;
import net.fabricmc.fabric.api.attachment.v1.AttachmentRegistry;
import net.fabricmc.fabric.api.attachment.v1.AttachmentSyncPredicate;
import net.fabricmc.fabric.api.attachment.v1.AttachmentTarget;
import net.fabricmc.fabric.api.attachment.v1.AttachmentType;
import net.fabricmc.fabric.api.command.v2.CommandRegistrationCallback;
import net.fabricmc.fabric.api.creativetab.v1.CreativeModeTabEvents;
import net.minecraft.ChatFormatting;
import net.minecraft.commands.Commands;
import net.minecraft.core.Registry;
import net.minecraft.core.component.DataComponentType;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.item.CreativeModeTabs;

/**
 * Tall Tales Fishing: fishing with stories behind it. A catch-bar minigame when a fish bites ({@link Angling},
 * {@link Minigame}; switch it off in {@link FishingConfig}), 84 fish from a data table ({@link FishTable}) that bite
 * by water, region, time, weather and season, nine legends, treasure, rods, bait and tackle ({@link Gear}), the
 * Angler's Journal, a Trophy Mount, docks and fishermen in villages ({@link Docks}, {@link DockAnglers}), a fishing
 * contest every season ({@link Contests}), tall tales ({@link FishingVillage}) and fish for Hearth &amp; Harvest's
 * kitchen. Everything starts from one {@link #register()} call in {@code VillageFriends}; add-ons use
 * {@link FishingApi} and {@link FishingEvents}.
 */
public final class Fishing {
    public static final String NS = "villagefriends";
    public static Identifier id(String path) { return Identifier.fromNamespaceAndPath(NS, path); }

    /** Bait or tackle loaded on a rod: the item, and how many (bait) or how many fish it has left (tackle). */
    public record Loaded(String item, int count) {
        static final Codec<Loaded> CODEC = RecordCodecBuilder.create(i -> i.group(
                Codec.STRING.fieldOf("item").forGetter(Loaded::item), Codec.INT.fieldOf("count").forGetter(Loaded::count)).apply(i, Loaded::new));
        static final StreamCodec<ByteBuf, Loaded> STREAM_CODEC = StreamCodec.composite(
                ByteBufCodecs.STRING_UTF8, Loaded::item, ByteBufCodecs.VAR_INT, Loaded::count, Loaded::new);
    }
    /** On a record catch or a legend: its length in tenths of a centimetre, who caught it, and the day. */
    public record Trophy(int size, String catcher, long day) {
        static final Codec<Trophy> CODEC = RecordCodecBuilder.create(i -> i.group(
                Codec.INT.fieldOf("size").forGetter(Trophy::size), Codec.STRING.fieldOf("catcher").forGetter(Trophy::catcher),
                Codec.LONG.fieldOf("day").forGetter(Trophy::day)).apply(i, Trophy::new));
        static final StreamCodec<ByteBuf, Trophy> STREAM_CODEC = StreamCodec.composite(
                ByteBufCodecs.VAR_INT, Trophy::size, ByteBufCodecs.STRING_UTF8, Trophy::catcher, ByteBufCodecs.VAR_LONG, Trophy::day, Trophy::new);
    }

    public static DataComponentType<Loaded> BAIT, TACKLE;
    public static DataComponentType<Trophy> TROPHY;
    /** A player's angler's journal. Kept through death, shared only with its owner (the journal screen reads it). */
    public static final AttachmentType<Journal> JOURNAL = AttachmentRegistry.create(id("fish_journal"), b -> b
            .initializer(() -> Journal.EMPTY).persistent(Journal.CODEC).copyOnDeath()
            .syncWith(Journal.STREAM_CODEC, AttachmentSyncPredicate.targetOnly()));

    public static void register() {
        FishTable.load();
        FishingConfig.load();
        BAIT = component("bait", Loaded.CODEC, Loaded.STREAM_CODEC);
        TACKLE = component("tackle", Loaded.CODEC, Loaded.STREAM_CODEC);
        TROPHY = component("trophy", Trophy.CODEC, Trophy.STREAM_CODEC);
        FishingItems.register();
        TrophyMount.register();
        FishingNet.register();
        Angling.register();
        Docks.register();
        DockAnglers.register();
        Contests.register();
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.FOOD_AND_DRINKS).register(entries -> {
            FishingItems.fish().forEach(entries::accept);
            entries.accept(FishingItems.GRILLED_FISH);
        });
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.TOOLS_AND_UTILITIES).register(entries -> FishingItems.gear().forEach(entries::accept));
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.FUNCTIONAL_BLOCKS).register(entries -> entries.accept(TrophyMount.BLOCK));
        CommandRegistrationCallback.EVENT.register((dispatcher, registries, environment) -> dispatcher.register(Commands.literal("fishing")
                .requires(Commands.hasPermission(Commands.LEVEL_GAMEMASTERS))
                .then(Commands.literal("minigame")
                        .then(Commands.literal("on").executes(c -> { FishingConfig.minigame(true); c.getSource().sendSuccess(() -> Component.literal("The fishing minigame is on."), true); return 1; }))
                        .then(Commands.literal("off").executes(c -> { FishingConfig.minigame(false); c.getSource().sendSuccess(() -> Component.literal("The fishing minigame is off: vanilla fishing."), true); return 1; })))
                .then(Commands.literal("journal")
                        .then(Commands.literal("fill").executes(c -> {
                            var p = c.getSource().getPlayerOrException();
                            var j = Angling.journal(p); long day = dev.villagefriends.VillageFriends.day(p.level());
                            for (var f : FishTable.all()) j = j.record(f.id(), f.maxSize() * 10, day).journal().hear(f.id());
                            ((AttachmentTarget) p).setAttached(JOURNAL, j);
                            c.getSource().sendSuccess(() -> Component.literal("Every fish is in your journal."), false);
                            return FishTable.all().size();
                        }))
                        .then(Commands.literal("clear").executes(c -> {
                            ((AttachmentTarget) c.getSource().getPlayerOrException()).setAttached(JOURNAL, Journal.EMPTY);
                            c.getSource().sendSuccess(() -> Component.literal("Your journal is blank again."), false);
                            return 1;
                        })))
                .then(Commands.literal("catch").then(Commands.argument("fish", StringArgumentType.word())
                        .suggests((c, b) -> { FishTable.all().forEach(f -> b.suggest(f.id())); return b.buildFuture(); })
                        .executes(c -> {
                            var p = c.getSource().getPlayerOrException();
                            var f = FishTable.get(StringArgumentType.getString(c, "fish"));
                            if (f == null) { c.getSource().sendFailure(Component.literal("No such fish.")); return 0; }
                            var stack = Angling.caught(p, f, Catches.size(f, new java.util.Random(), 0, false), false);
                            if (!p.getInventory().add(stack)) dev.villagefriends.VillageFriends.drop(p, stack);
                            return 1;
                        })))
                .then(Commands.literal("contest")
                        .then(Commands.literal("start").executes(c -> {
                            var p = c.getSource().getPlayerOrException();
                            var village = Contests.start((ServerLevel) p.level(), p.blockPosition());
                            if (village == null) { c.getSource().sendFailure(Component.literal("Stand in a village to start its contest.")); return 0; }
                            c.getSource().sendSuccess(() -> Component.literal("The " + village.name() + " fishing contest is on until you end it.").withStyle(ChatFormatting.AQUA), true);
                            return 1;
                        }))
                        .then(Commands.literal("end").executes(c -> {
                            var p = c.getSource().getPlayerOrException();
                            boolean done = Contests.finish((ServerLevel) p.level(), p.blockPosition());
                            if (!done) { c.getSource().sendFailure(Component.literal("There's no contest on here.")); return 0; }
                            return 1;
                        }))
                        .then(Commands.literal("next").executes(c -> {
                            long day = dev.villagefriends.VillageFriends.day(c.getSource().getLevel());
                            c.getSource().sendSuccess(() -> Component.literal("The next fishing contest is on " + Contests.next(day) + "."), false);
                            return 1;
                        })))
                .then(Commands.literal("dock")
                        .then(Commands.literal("build").executes(c -> {
                            var p = c.getSource().getPlayerOrException();
                            var dock = Docks.buildNear((ServerLevel) p.level(), p.blockPosition());
                            if (dock == null || !dock.built()) { c.getSource().sendFailure(Component.literal("No shore with open water within 32 blocks.")); return 0; }
                            var at = net.minecraft.core.BlockPos.of(dock.origin());
                            c.getSource().sendSuccess(() -> Component.literal("Built a dock at " + at.toShortString() + "."), false);
                            return 1;
                        })))
                .then(Commands.literal("bite").executes(c -> bite(c.getSource().getPlayerOrException(), null))
                        .then(Commands.argument("fish", StringArgumentType.word())
                                .suggests((c, b) -> { FishTable.all().forEach(f -> b.suggest(f.id())); return b.buildFuture(); })
                                .executes(c -> bite(c.getSource().getPlayerOrException(), FishTable.get(StringArgumentType.getString(c, "fish"))))))));
    }
    /** Forgets everything kept in memory (fights, anglers' places, the contest board) when a world closes. */
    public static void clear() { Angling.clear(); DockAnglers.clear(); Contests.clear(); }
    /** {@code /fishing bite [fish]}: something bites the player's hook straight away (that fish, if given). */
    private static int bite(net.minecraft.server.level.ServerPlayer p, Fish fish) {
        if (p.fishing == null) { p.sendSystemMessage(Component.literal("Cast your line into water first.")); return 0; }
        Angling.next(p, fish);
        ((dev.villagefriends.mixin.FishingHookAccess) p.fishing).villagefriends$setTimeUntilLured(1);
        return 1;
    }
    private static <T> DataComponentType<T> component(String name, Codec<T> codec, StreamCodec<ByteBuf, T> stream) {
        return Registry.register(BuiltInRegistries.DATA_COMPONENT_TYPE, id(name), DataComponentType.<T>builder().persistent(codec).networkSynchronized(stream).build());
    }

    private Fishing() {}
}
