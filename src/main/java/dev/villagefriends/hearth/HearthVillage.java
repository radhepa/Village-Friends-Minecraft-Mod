package dev.villagefriends.hearth;

import dev.villagefriends.Emote;
import dev.villagefriends.FriendshipLevels;
import dev.villagefriends.TalkWorld;
import dev.villagefriends.VillageFriends;
import dev.villagefriends.VillageProfessions;
import dev.villagefriends.tavern.Patronage;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import net.fabricmc.fabric.api.attachment.v1.AttachmentRegistry;
import net.fabricmc.fabric.api.attachment.v1.AttachmentTarget;
import net.fabricmc.fabric.api.attachment.v1.AttachmentType;
import net.minecraft.ChatFormatting;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.trading.ItemCost;
import net.minecraft.world.item.trading.MerchantOffer;

/**
 * Where cooking meets the village: every resident's favorite dish (gifts of it are worth the most, and
 * they talk about it), the family recipe a Friend hands over, picnics and gatherings with a dish, the
 * birthday cake, and the tavern keeper selling the cook's dish of the day. Hooks are single calls from
 * {@code VillageFriends}, {@code CompanionController}, {@code Birthdays}, {@code TalkWorld} and a mixin on
 * {@code Villager.setTradingPlayer}.
 */
public final class HearthVillage {
    /** A bonus for bringing a dish to a picnic or a gathering, at most once a day per resident. */
    public static final int PICNIC_BONUS = 4, PICNIC_FAVORITE_BONUS = 8, GUEST_BONUS = 2;
    private static final Map<UUID, String> picnicDishes = new HashMap<>();

    static void register() { java.util.Objects.requireNonNull(SPECIAL); }

    public static Tastes.Eater eater(Villager v) {
        var profile = VillageFriends.profile(v);
        return new Tastes.Eater(profile.id(), profile.personality(), VillageFriends.profession(v), v.isBaby());
    }
    public static Dish favorite(Villager v) { return Tastes.favorite(eater(v), Dishes.all()); }
    public static Dish familyRecipe(Villager v) { return Tastes.familyRecipe(eater(v), Dishes.all()); }
    private static String id(ItemStack stack) { return BuiltInRegistries.ITEM.getKey(stack.getItem()).toString(); }
    private static String name(Dish d) { return HearthItems.stack(d.id(), 1).getHoverName().getString(); }
    public static boolean cake(String item) { var d = Dishes.get(item); return d != null && d.cake(); }

    // -- gifts ---------------------------------------------------------------------------------------

    /** A dish given as a gift: what it's worth, what they say, the status line, the speech bubble and the journal note. */
    public record Gift(int value, boolean favorite, String reply, String status, Emote mood, String memory) {}

    /** Null unless the stack is a dish. */
    public static Gift gift(Villager v, ServerPlayer p, ItemStack stack) {
        var dish = HearthApi.dish(stack);
        if (dish == null || !dish.dish()) return null;
        var fav = favorite(v);
        boolean favorite = fav != null && fav.id().equals(dish.id()), fine = HearthApi.isFine(stack);
        int value = Tastes.giftValue(dish, favorite, fine, v.isBaby());
        String spoken = (fine ? "fine " : "") + dish.spoken();
        var extra = Map.of("gift", spoken);
        String personality = VillageFriends.profile(v).personality();
        String reply = null;
        if (v.isBaby()) reply = TalkWorld.say(v, p, favorite ? "baby.gift.dish.favorite" : "baby.gift.dish", extra);
        else if (favorite && v.getRandom().nextBoolean()) reply = TalkWorld.say(v, p, "gift.dish.favorite." + personality, extra);
        if (reply == null && !v.isBaby()) reply = TalkWorld.say(v, p, favorite ? "gift.dish.favorite" : fine && v.getRandom().nextBoolean() ? "gift.dish.fine" : "gift.dish", extra);
        if (reply == null) reply = favorite ? "My favorite! You remembered." : "That smells wonderful. Thank you!";
        String status = favorite ? "Their favorite dish!" : fine ? "A fine dish: they noticed." : "A home-cooked dish.";
        String memory = favorite ? "You brought me " + spoken + ", my favorite." : "You brought me " + spoken + ".";
        return new Gift(value, favorite, reply, status, favorite ? Emote.HEART : Emote.NOTE, memory);
    }

    // -- recipe cards --------------------------------------------------------------------------------

    /**
     * The first time a resident who is at least a Friend talks to you, they hand you their family recipe.
     * Returns the line they say, or null. Called when the conversation window opens.
     */
    public static String familyRecipeFor(ServerPlayer p, Villager v, int friendLevel) {
        var dweller = dev.villagefriends.homestead.Homesteads.dweller(v);
        if (v.isBaby() || friendLevel < Tastes.RECIPE_LEVEL || dweller != null && dweller.role().equals("pariah")) return null;
        var b = VillageFriends.bond(v, p);
        if (b.has("family_recipe")) return null;
        var dish = familyRecipe(v);
        if (dish == null) return null;
        var recipe = Cookbook.making(dish.id());
        if (recipe == null) return null;
        VillageFriends.saveBond(v, p, b.flag("family_recipe").remember(VillageFriends.day(v.level()), "I gave you our family recipe for " + dish.spoken() + "."));
        var card = RecipeCardItem.of(recipe.id());
        if (!p.getInventory().add(card)) VillageFriends.drop(p, card);
        var extra = Map.of("gift", dish.spoken());
        String personality = VillageFriends.profile(v).personality();
        String line = v.getRandom().nextBoolean() ? TalkWorld.say(v, p, "recipe.card." + personality, extra) : null;
        if (line == null) line = TalkWorld.say(v, p, "recipe.card", extra);
        p.sendSystemMessage(Component.literal(VillageFriends.name(v) + " gave you a recipe card: " + name(dish) + ". Use it to learn the recipe.").withStyle(ChatFormatting.GOLD), false);
        return line != null ? line : "Here. My family's recipe for " + dish.spoken() + ". Don't tell anyone where you got it.";
    }

    // -- talk -----------------------------------------------------------------------------------------

    /** Placeholders for dialogue: {dish} (their favorite), {meal} (eating now), {special} (the tavern's dish of the day). */
    public static void talk(Villager v, Map<String, String> fill) {
        var fav = favorite(v);
        if (fav != null) fill.put("dish", fav.spoken());
        String now = HomeMeals.eatingNow(v);
        if (now != null) fill.put("meal", now);
        var special = Dishes.get(Patronage.dishOfTheDay(VillageFriends.day(v.level())));
        fill.put("special", special != null ? special.spoken() : VillageFriends.itemName(Patronage.dishOfTheDay(VillageFriends.day(v.level()))));
    }
    /** What the player holds, as a resident sees it: "favorite_dish", "dish", or null when it isn't a dish. */
    public static String held(Villager v, ItemStack stack) {
        var dish = HearthApi.dish(stack);
        if (dish == null || !dish.dish()) return null;
        var fav = favorite(v);
        return fav != null && fav.id().equals(dish.id()) ? "favorite_dish" : "dish";
    }
    /** "Favorite dish: Onion Pottage", for the Ledger and the conversation window's hints. */
    public static String favoriteLabel(Villager v) {
        var fav = favorite(v);
        return fav == null ? "" : "Favorite dish: " + name(fav);
    }

    // -- picnics and gatherings ----------------------------------------------------------------------

    /** Food that can start a picnic or a gathering: bread, an apple, a cookie, or any dish. */
    public static boolean picnicFood(ItemStack stack) {
        if (stack.is(Items.BREAD) || stack.is(Items.APPLE) || stack.is(Items.COOKIE)) return true;
        var dish = HearthApi.dish(stack);
        return dish != null && dish.dish();
    }
    /** Remembers which dish was brought, before it's eaten. */
    public static void brought(Villager v, ItemStack stack) {
        var dish = HearthApi.dish(stack);
        if (dish != null && dish.dish()) picnicDishes.put(v.getUUID(), dish.id()); else picnicDishes.remove(v.getUUID());
    }
    /**
     * At the end of a picnic or gathering someone brought a dish to: a little extra friendship (more for their
     * favorite, and some for every guest), once a day. Returns what they say, or null for an ordinary outing.
     */
    public static String finished(Villager v, ServerPlayer p, String kind, List<Villager> guests) {
        String item = picnicDishes.remove(v.getUUID());
        if (item == null || !(kind.equals("picnic") || kind.equals("gathering"))) return null;
        var dish = Dishes.get(item);
        if (dish == null) return null;
        long today = VillageFriends.day(v.level());
        var b = VillageFriends.bond(v, p);
        var fav = favorite(v);
        boolean favorite = fav != null && fav.id().equals(item);
        if (!b.has("picnic_dish:" + today)) {
            VillageFriends.saveBond(v, p, b.flag("picnic_dish:" + today).remember(today, "We shared " + dish.spoken() + " at a " + kind + "."));
            VillageFriends.reward(v, p, favorite ? PICNIC_FAVORITE_BONUS : PICNIC_BONUS);
            for (var guest : guests) VillageFriends.reward(guest, p, GUEST_BONUS);
        }
        String line = TalkWorld.say(v, p, favorite ? "picnic.dish.favorite" : "picnic.dish", Map.of("gift", dish.spoken()));
        return line != null ? line : "That " + dish.spoken() + " was perfect for a " + kind + ". Thank you for bringing it.";
    }

    // -- birthday cake -------------------------------------------------------------------------------

    /** The cake at this resident's birthday party. */
    public static Dish partyCake(Villager host) { return Tastes.partyCake(eater(host), Dishes.all()); }
    /** Cake time: the guest of honor and every guest eat a slice. Returns the cake's item id for the players' slices. */
    public static String serveCake(Villager host, List<Villager> guests) {
        var cake = partyCake(host);
        String item = cake != null ? cake.id() : "villagefriends:birthday_cake_slice";
        String key = "party|" + VillageFriends.day(host.level());
        HomeMeals.eat(host, item, 22, key);
        for (var g : guests) HomeMeals.eat(g, item, 16 + g.getRandom().nextInt(10), key);
        return item;
    }

    // -- the tavern keeper's dish of the day ---------------------------------------------------------

    /** The day and dish the tavern keeper last put on sale ("12|villagefriends:onion_pottage"). */
    public static final AttachmentType<String> SPECIAL = AttachmentRegistry.create(Hearth.id("dish_of_the_day"), b -> b.persistent(com.mojang.serialization.Codec.STRING));
    public static final int SPECIAL_USES = 8;

    /**
     * Before a player trades with the tavern keeper, today's dish of the day goes on sale (and yesterday's comes
     * off): one emerald plus one per Well Fed tier a helping, eight helpings a day. Called from
     * {@code Villager.setTradingPlayer}.
     */
    public static void stockKeeper(Villager v) {
        if (!(v.level() instanceof net.minecraft.server.level.ServerLevel level) || v.isBaby()) return;
        if (!VillageFriends.profession(v).equals("tavern_keeper")) return;
        String dish = Patronage.dishOfTheDay(VillageFriends.day(level));
        var item = BuiltInRegistries.ITEM.getValue(Identifier.parse(dish));
        if (item == null || item == Items.AIR) return;
        var target = (AttachmentTarget) v;
        String want = VillageFriends.day(level) + "|" + dish, stored = target.getAttached(SPECIAL);
        var offers = v.getOffers();
        if (want.equals(stored) && offers.stream().anyMatch(o -> o.getResult().is(item))) return;
        if (stored != null) {
            var old = BuiltInRegistries.ITEM.getValue(Identifier.parse(stored.substring(stored.indexOf('|') + 1)));
            offers.removeIf(o -> o.getResult().is(old) && o.getMaxUses() == SPECIAL_USES && o.getCostA().is(Items.EMERALD));
        }
        var row = Dishes.get(dish);
        offers.add(0, new MerchantOffer(new ItemCost(Items.EMERALD, row == null ? 2 : 1 + row.tier()), new ItemStack(item), SPECIAL_USES, 2, .05F));
        target.setAttached(SPECIAL, want);
    }

    /** The tavern keeper's label in messages. */
    static String keeper() { return VillageProfessions.label("tavern_keeper"); }

    private HearthVillage() {}
}
