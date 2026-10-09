package dev.villagefriends.hearth;

import com.mojang.serialization.Codec;
import dev.villagefriends.tavern.Patronage;
import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;
import net.fabricmc.fabric.api.attachment.v1.AttachmentRegistry;
import net.fabricmc.fabric.api.attachment.v1.AttachmentSyncPredicate;
import net.fabricmc.fabric.api.attachment.v1.AttachmentTarget;
import net.fabricmc.fabric.api.attachment.v1.AttachmentType;
import net.fabricmc.fabric.api.command.v2.CommandRegistrationCallback;
import net.fabricmc.fabric.api.creativetab.v1.CreativeModeTabEvents;
import net.fabricmc.fabric.api.item.v1.DefaultItemComponentEvents;
import net.fabricmc.fabric.api.resource.v1.ResourceLoader;
import net.minecraft.ChatFormatting;
import net.minecraft.commands.Commands;
import net.minecraft.commands.arguments.ResourceArgument;
import net.minecraft.core.Registry;
import net.minecraft.core.component.DataComponentType;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.server.packs.PackType;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.CreativeModeTabs;

/**
 * Hearth & Harvest: cooking for the village. Three stations (a cooking pot over a fire, a clay oven, a prep
 * table), six crops, about sixty dishes from a data table with tiered Well Fed buffs, family recipe cards,
 * and residents who cook, eat at home, have a favorite dish and serve real dishes at the tavern
 * ({@link HearthVillage}). Everything starts from one {@link #register()} call in {@code VillageFriends}.
 * Add-ons hook in through {@link HearthApi} and {@link HearthEvents}.
 */
public final class Hearth {
    public static final String NS = "villagefriends";
    public static Identifier id(String path) { return Identifier.fromNamespaceAndPath(NS, path); }

    /** Set on a dish that was cooked well: a longer Well Fed, a little more as a gift, and "Fine" in its name. */
    public static DataComponentType<Boolean> FINE;
    /** The recipe a recipe card teaches. */
    public static DataComponentType<String> RECIPE;
    /** The family recipes a player has learned. Kept through death, shared only with its owner. */
    public static final AttachmentType<List<String>> COOKBOOK = AttachmentRegistry.create(id("cookbook"), b -> b
            .initializer(List::of).persistent(Codec.STRING.listOf()).copyOnDeath()
            .syncWith(ByteBufCodecs.STRING_UTF8.apply(ByteBufCodecs.list()), AttachmentSyncPredicate.targetOnly()));

    public static void register() {
        var table = Dishes.load();
        WellFed.register();
        FINE = Registry.register(BuiltInRegistries.DATA_COMPONENT_TYPE, id("fine"),
                DataComponentType.<Boolean>builder().persistent(Codec.BOOL).networkSynchronized(ByteBufCodecs.BOOL).build());
        RECIPE = Registry.register(BuiltInRegistries.DATA_COMPONENT_TYPE, id("recipe"),
                DataComponentType.<String>builder().persistent(Codec.STRING).networkSynchronized(ByteBufCodecs.STRING_UTF8).build());
        HearthItems.register(table);
        HearthBlocks.register();
        // Dishes the mod already had keep their items and gain Well Fed.
        DefaultItemComponentEvents.MODIFY.register(context -> {
            for (var d : table.dishes()) {
                if (!d.existing() || !d.dish()) continue;
                var item = BuiltInRegistries.ITEM.getValue(Identifier.parse(d.id()));
                context.modify(item, builder -> builder.set(DataComponents.CONSUMABLE, HearthItems.consumableFor(d, item)));
            }
        });
        // The cook's dish of the day and the tavern's menu come from the dish table.
        Patronage.menu(Tastes.tavernMenu(Dishes.all()), Dishes.all().stream().filter(d -> !d.serve().equals("-"))
                .collect(Collectors.toMap(Dish::id, Dish::serve, (a, b) -> a)));
        ResourceLoader.get(PackType.SERVER_DATA).registerReloadListener(id("hearth_recipes"), new HearthRecipes());
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.FOOD_AND_DRINKS).register(entries -> HearthItems.food().forEach(entries::accept));
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.INGREDIENTS).register(entries -> {
            HearthItems.ingredients().forEach(entries::accept);
            entries.accept(HearthItems.RECIPE_CARD);
        });
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.NATURAL_BLOCKS).register(entries -> HearthItems.farming().forEach(entries::accept));
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.FUNCTIONAL_BLOCKS).register(entries -> HearthBlocks.blocks().forEach(entries::accept));
        CommandRegistrationCallback.EVENT.register((dispatcher, registries, environment) -> dispatcher.register(Commands.literal("hearth")
                .requires(Commands.hasPermission(Commands.LEVEL_GAMEMASTERS))
                .then(Commands.literal("learn").then(Commands.literal("all").executes(c -> {
                    var p = c.getSource().getPlayerOrException();
                    int n = 0;
                    for (var r : Cookbook.all()) if (r.secret() && learn(p, r.id())) n++;
                    int learned = n;
                    c.getSource().sendSuccess(() -> Component.literal("Learned " + learned + " family recipes."), false);
                    return learned;
                })))
                .then(Commands.literal("forget").executes(c -> {
                    target(c.getSource().getPlayerOrException()).setAttached(COOKBOOK, List.of());
                    c.getSource().sendSuccess(() -> Component.literal("Forgot every family recipe."), false);
                    return 1;
                }))
                .then(Commands.literal("recipes").executes(c -> {
                    var counts = new java.util.EnumMap<Station, Integer>(Station.class);
                    for (var r : Cookbook.all()) counts.merge(r.station(), 1, Integer::sum);
                    c.getSource().sendSuccess(() -> Component.literal(Cookbook.all().size() + " recipes: " + counts), false);
                    return Cookbook.all().size();
                }))));
        HearthVillage.register();
        HomeMeals.register();
        HearthFarms.register();
        HearthCompat.register();
    }

    private static AttachmentTarget target(Player p) { return (AttachmentTarget) p; }
    /** The family recipes this player has learned. */
    public static Set<String> known(Player p) { return new LinkedHashSet<>(target(p).getAttachedOrElse(COOKBOOK, List.of())); }
    /** Teaches a player a recipe; false if they already knew it. */
    public static boolean learn(ServerPlayer p, String recipe) {
        var known = known(p);
        if (!known.add(recipe)) return false;
        target(p).setAttached(COOKBOOK, List.copyOf(new ArrayList<>(known)));
        return true;
    }
    public static String stationName(Station s) {
        return switch (s) { case POT -> "cooking pot"; case OVEN -> "clay oven"; case PREP -> "prep table"; };
    }
    static Map<String, String> chat(String text) { return Map.of("text", text); }
    static Component gold(String text) { return Component.literal(text).withStyle(ChatFormatting.GOLD); }

    private Hearth() {}
}
