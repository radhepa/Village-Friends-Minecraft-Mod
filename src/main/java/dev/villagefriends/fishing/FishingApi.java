package dev.villagefriends.fishing;

import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.Item;

/**
 * For other features and mods. Fish: {@link #registerFish} at mod init (give it an item you register yourself);
 * the tags below; {@link FishingEvents} for the minigame and every catch; {@link #journal} and {@link #land} to read
 * a player's journal or hand them a catch as if they'd reeled it in (logged, contest-scored, RPG experience).
 */
public final class FishingApi {
    /** Every fish in the table, vanilla's four included. */
    public static final TagKey<Item> FISH = tag("fishing/fish");
    /** Fish that are food (no legends, no jellyfish): these join Hearth &amp; Harvest's {@code villagefriends:cooking/fish}. */
    public static final TagKey<Item> EDIBLE = tag("fishing/edible");
    /** Fish that smelt, smoke or campfire-cook into Grilled Fish. */
    public static final TagKey<Item> GRILLABLE = tag("fishing/grillable");
    /** Fish cats and dogs love as treats (also added to minecraft:cat_food and minecraft:wolf_food). */
    public static final TagKey<Item> TREATS = tag("fishing/treats");
    public static final TagKey<Item> LEGENDARY = tag("fishing/legendary");
    /** The vanilla Fishing Rod and ours. */
    public static final TagKey<Item> RODS = tag("fishing/rods");
    public static final TagKey<Item> BAIT = tag("fishing/bait"), TACKLE = tag("fishing/tackle");

    private static TagKey<Item> tag(String path) { return TagKey.create(Registries.ITEM, Identifier.fromNamespaceAndPath(Fishing.NS, path)); }

    /** Adds a fish to the table (call at mod init, after Village Friends; the item must exist). */
    public static void registerFish(Fish fish) { FishTable.put(fish); }
    public static Journal journal(ServerPlayer player) { return Angling.journal(player); }
    /** Gives a player a fish as if they'd landed it: journal, contest, events. Returns the stack to hand over. */
    public static net.minecraft.world.item.ItemStack land(ServerPlayer player, Fish fish, int sizeTenths) { return Angling.caught(player, fish, sizeTenths, false); }

    private FishingApi() {}
}
