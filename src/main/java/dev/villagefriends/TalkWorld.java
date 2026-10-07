package dev.villagefriends;

import dev.villagefriends.routine.Routine;
import dev.villagefriends.talk.DialogueBank;
import dev.villagefriends.talk.Talk;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Random;
import java.util.Set;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.tags.ItemTags;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.animal.feline.Cat;
import net.minecraft.world.entity.animal.golem.IronGolem;
import net.minecraft.world.entity.npc.wanderingtrader.WanderingTrader;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.crafting.RecipeType;
import net.minecraft.world.item.crafting.SingleRecipeInput;
import static dev.villagefriends.VillageFriends.*;

/**
 * Reads the world into a {@link Talk.Context}, says the chosen line, and carries out what residents
 * offer: patching you up, a bite to eat, cooking or mending what you hold, directions home.
 *
 * <p>Bond flags: {@code asking:<id>} is the question on the table, {@code q:<id>} one you've answered,
 * {@code offer:<id>:<day>} an offer made today, {@code a:<flag>} something they remember about you.
 */
public final class TalkWorld {
    private static final Random RANDOM = new Random();

    // -- reading the moment ------------------------------------------------------------------------

    static Talk.Context context(Villager v, ServerPlayer p, String topic) {
        var level = v.level(); var profile = profile(v); var b = bond(v, p);
        int friendLevel = FriendshipLevels.level(state(v, p), b);
        int time = ResidentRoutines.timeOfDay(level); long today = day(level);
        var plan = ResidentRoutines.plan(v);
        String weather = plan.weather().id();
        var biome = level.getBiome(v.blockPosition());
        if (weather.equals("clear") && biome.value().getBaseTemperature() >= 1.5F && Talk.period(time).matches("noon|afternoon")) weather = "hot";
        String home = v.getVillagerData().type().unwrapKey().map(k -> k.identifier().getPath()).orElse("plains");
        var held = held(p.getMainHandItem());
        var states = states(p, level, time);
        var extra = new HashSet<String>();
        if (!level.getEntitiesOfClass(IronGolem.class, v.getBoundingBox().inflate(16), g -> g.isAlive()).isEmpty()) extra.add("golem");
        if (!level.getEntitiesOfClass(Cat.class, v.getBoundingBox().inflate(10), g -> g.isAlive()).isEmpty()) extra.add("cat");
        if (!level.getEntitiesOfClass(WanderingTrader.class, v.getBoundingBox().inflate(32), g -> g.isAlive()).isEmpty()) extra.add("trader");
        if (!level.getEntitiesOfClass(Villager.class, v.getBoundingBox().inflate(12), o -> o != v && o.isBaby()).isEmpty()) extra.add("children");
        // A couple of things they remember about you, for callbacks.
        var remembered = new ArrayList<String>();
        for (var flag : b.flags()) if (flag.startsWith("a:")) remembered.add(flag);
        java.util.Collections.shuffle(remembered, RANDOM);
        extra.addAll(remembered.subList(0, Math.min(2, remembered.size())));
        extra.add(friendLevel >= 3 ? "friends" : "newcomers");

        var fill = new HashMap<String, String>();
        fill.put("name", first(name(v))); fill.put("player", p.getName().getString());
        var town = VillageSettlements.home(v); fill.put("village", town == null ? "the village" : town.name());
        String job = profession(v);
        fill.put("job", job.equals("none") ? "neighbor" : job.equals("nitwit") ? "free spirit" : VillageProfessions.label(job).toLowerCase(Locale.ROOT));
        fill.put("hobby", profile.hobby()); fill.put("love", itemName(profile.love()));
        fill.put("time", Routine.clock(time)); fill.put("day", Long.toString(today + 1));
        fill.put("weekday", Routine.weekday(today));
        long toMarket = Math.floorMod(Routine.MARKET_EVERY - 1 - today, Routine.MARKET_EVERY);
        fill.put("market", toMarket == 0 ? "today" : toMarket == 1 ? "tomorrow" : "in " + toMarket + " days");
        String moon = Talk.MOONS[(int) Math.floorMod(today, 8L)];
        fill.put("moon", Talk.moonName(moon));
        fill.put("biome", switch (home) { case "snow" -> "the snowy plains"; case "taiga" -> "the taiga"; case "desert" -> "the desert"; case "savanna" -> "the savanna";
            case "jungle" -> "the jungle"; case "swamp" -> "the swamp"; default -> "the plains"; });
        if (!p.getMainHandItem().isEmpty()) fill.put("item", p.getMainHandItem().getHoverName().getString().toLowerCase(Locale.ROOT));
        var society = VillageSocieties.of(v);
        if (society != null && society.has(profile.id())) {
            var self = society.get(profile.id());
            if (!self.partner().isEmpty()) fill.put("partner", first(society.nameOf(self.partner())));
            String friend = society.bestFriend(profile.id(), today), rival = society.rival(profile.id(), today);
            if (!friend.isEmpty()) fill.put("friend", first(society.nameOf(friend)));
            if (!rival.isEmpty()) fill.put("rival", first(society.nameOf(rival)));
            var others = society.living().stream().filter(t -> !t.id().equals(profile.id())).toList();
            if (!others.isEmpty()) fill.put("neighbor", first(others.get(RANDOM.nextInt(others.size())).name()));
        }
        return new Talk.Context(topic, v.isBaby(), profile.personality(), job, friendLevel, Talk.period(time), weather,
                plan.block().id(), Routine.marketDay(today), moon, home, held, states, extra, fill);
    }
    private static String first(String name) { int space = name.indexOf(' '); return space > 0 ? name.substring(0, space) : name; }

    /** What kind of thing the player is holding, as residents see it. */
    static String held(ItemStack s) {
        if (s.isEmpty()) return "";
        if (s.is(ItemTags.SWORDS)) return "sword";
        if (s.is(ItemTags.AXES)) return "axe";
        if (s.is(ItemTags.PICKAXES)) return "pickaxe";
        if (s.is(ItemTags.SHOVELS)) return "shovel";
        if (s.is(ItemTags.HOES)) return "hoe";
        if (s.is(Items.BOW) || s.is(Items.CROSSBOW)) return "bow";
        if (s.is(Items.TRIDENT) || s.is(Items.MACE)) return "trident";
        if (s.is(Items.SHIELD)) return "shield";
        if (s.is(Items.FISHING_ROD)) return "fishing_rod";
        if (s.is(Items.MAP) || s.is(Items.FILLED_MAP)) return "map";
        if (s.is(Items.COMPASS) || s.is(Items.RECOVERY_COMPASS) || s.is(Items.CLOCK) || s.is(Items.SPYGLASS)) return "compass";
        if (s.is(Items.BOOK) || s.is(Items.WRITABLE_BOOK) || s.is(Items.WRITTEN_BOOK) || s.is(Items.ENCHANTED_BOOK) || s.is(VillageItems.get("field_journal"))) return "book";
        if (s.is(net.minecraft.tags.BlockItemTags.FLOWERS.item())) return "flower";
        if (s.is(Items.EMERALD) || s.is(Items.EMERALD_BLOCK)) return "emerald";
        if (s.is(Items.DIAMOND) || s.is(Items.DIAMOND_BLOCK) || s.is(Items.NETHERITE_INGOT)) return "diamond";
        if (s.is(Items.GOLD_INGOT) || s.is(Items.GOLD_NUGGET) || s.is(Items.GOLD_BLOCK) || s.is(Items.RAW_GOLD)) return "gold";
        if (s.is(Items.TORCH) || s.is(Items.LANTERN) || s.is(Items.SOUL_TORCH) || s.is(Items.SOUL_LANTERN)) return "torch";
        if (s.is(Items.BUCKET) || s.is(Items.WATER_BUCKET) || s.is(Items.LAVA_BUCKET) || s.is(Items.MILK_BUCKET) || s.is(Items.POWDER_SNOW_BUCKET)) return "bucket";
        if (s.is(Items.WHEAT_SEEDS) || s.is(Items.WHEAT) || s.is(Items.CARROT) || s.is(Items.POTATO) || s.is(Items.BEETROOT) || s.is(Items.BEETROOT_SEEDS)
                || s.is(Items.PUMPKIN_SEEDS) || s.is(Items.MELON_SEEDS) || s.is(ItemTags.SAPLINGS)) return "crops";
        if (s.is(ItemTags.EGGS)) return "egg";
        if (s.is(Items.TOTEM_OF_UNDYING)) return "totem";
        if (s.is(Items.ELYTRA)) return "elytra";
        if (s.is(Items.TNT) || s.is(Items.FLINT_AND_STEEL) || s.is(Items.FIRE_CHARGE)) return "tnt";
        if (s.is(Items.POTION) || s.is(Items.SPLASH_POTION) || s.is(Items.LINGERING_POTION)) return "potion";
        if (s.is(Items.CAKE) || s.is(Items.COOKIE) || s.is(Items.PUMPKIN_PIE) || s.is(Items.HONEY_BOTTLE) || s.is(Items.SWEET_BERRIES)) return "treat";
        if (s.has(DataComponents.FOOD)) return raw(s) ? "raw_food" : "food";
        if (s.is(Items.BELL) || s.is(Items.NOTE_BLOCK) || s.is(Items.JUKEBOX) || s.is(VillageItems.get("lute")) || s.is(Items.GOAT_HORN)) return "music";
        if (s.is(Items.NAME_TAG) || s.is(Items.LEAD) || s.is(Items.SADDLE)) return "pet";
        if (s.is(Items.SHEARS) || s.is(net.minecraft.tags.ItemTags.WOOL)) return "wool";
        if (s.is(ItemTags.LOGS) || s.is(ItemTags.PLANKS)) return "wood";
        if (s.is(Items.IRON_INGOT) || s.is(Items.COPPER_INGOT) || s.is(Items.RAW_IRON) || s.is(Items.COAL)) return "ore";
        if (s.is(VillageItems.get("paintbrush")) || s.is(net.minecraft.tags.ItemTags.DYES)) return "paint";
        return "";
    }
    private static boolean raw(ItemStack s) {
        return s.is(Items.BEEF) || s.is(Items.PORKCHOP) || s.is(Items.CHICKEN) || s.is(Items.MUTTON) || s.is(Items.RABBIT) || s.is(Items.COD) || s.is(Items.SALMON)
                || s.is(Items.POTATO) || s.is(Items.KELP);
    }
    /** How the player looks right now. */
    static Set<String> states(ServerPlayer p, net.minecraft.world.level.Level level, int time) {
        var states = new HashSet<String>();
        if (p.getHealth() < p.getMaxHealth() * .5F) states.add("hurt");
        if (p.getFoodData().getFoodLevel() <= 8) states.add("hungry");
        if (p.isInWaterOrRain() && !p.isInWater()) states.add("wet");
        if (p.isOnFire()) states.add("fire");
        if (p.isPassenger()) states.add("riding");
        if (p.getMainHandItem().isDamaged()) states.add("damaged");
        var head = p.getItemBySlot(EquipmentSlot.HEAD); var chest = p.getItemBySlot(EquipmentSlot.CHEST);
        if (head.is(Items.CARVED_PUMPKIN)) states.add("pumpkin");
        if (chest.is(Items.ELYTRA)) states.add("elytra");
        else if (chest.is(Items.DIAMOND_CHESTPLATE) || chest.is(Items.NETHERITE_CHESTPLATE)) states.add("diamond");
        else if (chest.is(Items.GOLDEN_CHESTPLATE)) states.add("golden");
        else if (chest.is(Items.LEATHER_CHESTPLATE)) states.add("leather");
        else if (chest.isEmpty() && head.isEmpty() && p.getItemBySlot(EquipmentSlot.LEGS).isEmpty()) states.add("unarmored");
        String period = Talk.period(time);
        if ((period.equals("night") || period.equals("late")) && level.canSeeSky(p.blockPosition())) states.add("dark");
        return states;
    }

    // -- saying things -----------------------------------------------------------------------------

    /** A line for a topic ("greet", "chat", "work", "adventure", "joke"), remembered so it isn't repeated soon; null if none. */
    public static String line(Villager v, ServerPlayer p, String topic) {
        var bank = DialogueBank.current(); var c = context(v, p, topic); var b = bond(v, p);
        var recent = new HashSet<String>();
        for (var id : b.recentLines()) if (id.startsWith("t:")) recent.add(id.substring(2));
        var line = Talk.pick(bank, c, RANDOM, recent);
        if (line == null) return null;
        saveBond(v, p, bond(v, p).line("t:" + line.id()));
        return line.text();
    }

    /** Sometimes, on "How's your day?", a resident asks you something or offers to help instead. */
    public static DialogueBank.Question ask(Villager v, ServerPlayer p) {
        var bank = DialogueBank.current(); var c = context(v, p, "chat"); var b = bond(v, p);
        long today = day(v.level());
        var done = new HashSet<String>();
        for (var flag : b.flags()) {
            if (flag.startsWith("q:")) done.add(flag.substring(2));
            if (flag.startsWith("offer:") && flag.endsWith(":" + today)) done.add(flag.substring(6, flag.lastIndexOf(':')));
        }
        DialogueBank.Question q = null;
        // Children ask questions, but only grown-ups make offers.
        if (!v.isBaby() && RANDOM.nextFloat() < .7F) q = Talk.question(bank, c, done, true, RANDOM);
        if (q == null && RANDOM.nextFloat() < .24F) q = Talk.question(bank, c, done, false, RANDOM);
        if (q == null) return null;
        var next = b;
        for (var flag : b.flags()) if (flag.startsWith("asking:")) next = next.unflag(flag);
        saveBond(v, p, next.flag("asking:" + q.id()));
        return q;
    }
    public static String askText(Villager v, ServerPlayer p, DialogueBank.Question q) {
        var c = context(v, p, "chat");
        var options = new ArrayList<String>();
        for (var a : q.ask()) { var t = Talk.fill(a, c.fill()); if (t != null) options.add(t); }
        return options.isEmpty() ? q.ask().getFirst() : options.get(RANDOM.nextInt(options.size()));
    }
    static DialogueBank.Question asking(Villager v, ServerPlayer p) {
        for (var flag : bond(v, p).flags()) if (flag.startsWith("asking:")) return DialogueBank.current().question(flag.substring(7));
        return null;
    }
    /** Your possible answers to the question on the table. */
    public static List<FriendshipPayload.Choice> choices(Villager v, ServerPlayer p) {
        var q = asking(v, p); var out = new ArrayList<FriendshipPayload.Choice>();
        if (q == null) return List.of(new FriendshipPayload.Choice("talk_tab", "Let's talk", true));
        for (int i = 0; i < q.answers().size() && i < FriendshipPayload.MAX_CHOICES - 1; i++)
            out.add(new FriendshipPayload.Choice("answer:" + q.id() + ":" + i, q.answers().get(i).label(), true));
        out.add(new FriendshipPayload.Choice("skip_question", "Let's talk about something else", true));
        return out;
    }
    /** You chose an answer: they reply, remember it, and do what they offered. */
    public static boolean answer(ServerPlayer p, Villager v, String action) {
        if (action.equals("skip_question")) {
            var b = bond(v, p);
            for (var flag : b.flags()) if (flag.startsWith("asking:")) b = b.unflag(flag);
            saveBond(v, p, b);
            show(p, v, "talk", pickOr(v, p, "Another time, then. What's on your mind?"), "No pressure.", false, Emote.DOTS);
            return true;
        }
        var q = asking(v, p);
        if (q == null) return false;
        int index = Talk.answerIndex(action, q.id());
        if (index < 0 || index >= q.answers().size()) return false;
        var a = q.answers().get(index); long today = day(v.level());
        var b = bond(v, p).unflag("asking:" + q.id());
        b = q.offer() ? b.flag("offer:" + q.id() + ":" + today) : b.flag("q:" + q.id());
        if (a.flag() != null && !a.flag().isEmpty()) b = b.flag("a:" + a.flag());
        // Offers made on earlier days don't need remembering.
        for (var flag : List.copyOf(b.flags())) if (flag.startsWith("offer:") && !flag.endsWith(":" + today)) b = b.unflag(flag);
        saveBond(v, p, b);
        String status = q.offer() ? "" : "They'll remember that.";
        if (a.points() > 0) { reward(v, p, a.points()); status = "+" + a.points() + " friendship." + (q.offer() ? "" : " They'll remember that."); }
        if (a.effect() != null && !a.effect().isEmpty()) status = effect(a.effect(), p, v);
        var c = context(v, p, "chat");
        String reply = Talk.fill(a.reply(), c.fill());
        Emote mood = null;
        if (a.mood() != null) try { mood = Emote.valueOf(a.mood()); } catch (IllegalArgumentException ignored) {}
        show(p, v, "talk", reply == null ? a.reply().replaceAll("\\{[a-z_]+}", "you") : reply, status.isEmpty() ? "Happy to help." : status, false, mood == null ? Emote.NOTE : mood);
        return true;
    }
    private static String pickOr(Villager v, ServerPlayer p, String fallback) { var line = line(v, p, "chat"); return line == null ? fallback : line; }

    /** What a resident does for you when you accept an offer. */
    static String effect(String effect, ServerPlayer p, Villager v) {
        var level = (ServerLevel) v.level(); String who = first(name(v));
        switch (effect) {
            case "heal" -> {
                p.heal(6); p.addEffect(new MobEffectInstance(MobEffects.REGENERATION, 100, 0));
                return who + " patched you up. (+3 hearts)";
            }
            case "meal" -> {
                String job = profession(v);
                var food = switch (job) {
                    case "cook" -> new ItemStack(VillageItems.get("fresh_village_bread"));
                    case "tavern_keeper" -> new ItemStack(VillageItems.get("mug_of_cider"));
                    case "fisherman" -> new ItemStack(Items.COOKED_COD, 2);
                    case "butcher" -> new ItemStack(Items.COOKED_PORKCHOP);
                    case "farmer" -> new ItemStack(Items.BREAD, 2);
                    default -> new ItemStack(Items.BREAD);
                };
                giveStack(p, food);
                return who + " shared " + food.getHoverName().getString().toLowerCase(Locale.ROOT) + " with you.";
            }
            case "shelter" -> { reward(v, p, 3); saveBond(v, p, bond(v, p).remember(day(level), "We waited out the rain together.")); return "+3 friendship. You waited out the rain together."; }
            case "torch" -> { giveStack(p, new ItemStack(Items.TORCH, 3)); return who + " gave you three torches."; }
            case "apple" -> { giveStack(p, new ItemStack(Items.APPLE)); return who + " gave you an apple."; }
            case "bread" -> { giveStack(p, new ItemStack(Items.BREAD)); return who + " gave you some bread."; }
            case "cookie" -> { giveStack(p, new ItemStack(Items.COOKIE, 2)); return who + " gave you two cookies."; }
            case "seeds" -> { giveStack(p, new ItemStack(Items.WHEAT_SEEDS, 4)); return who + " gave you a handful of seeds."; }
            case "flower" -> {
                var flowers = List.of(Items.POPPY, Items.DANDELION, Items.CORNFLOWER, Items.OXEYE_DAISY, Items.ALLIUM, Items.AZURE_BLUET);
                giveStack(p, new ItemStack(flowers.get(RANDOM.nextInt(flowers.size())))); return who + " gave you a flower.";
            }
            case "fish" -> { giveStack(p, new ItemStack(Items.COOKED_COD)); return who + " gave you a cooked cod."; }
            case "study" -> { p.giveExperiencePoints(5); return "You learned something. (+5 experience)"; }
            case "emerald_tip" -> { giveStack(p, new ItemStack(Items.EMERALD)); return who + " pressed an emerald into your hand."; }
            case "cook_held" -> {
                var held = p.getMainHandItem(); var input = new SingleRecipeInput(held);
                var recipe = level.recipeAccess().getRecipeFor(RecipeType.CAMPFIRE_COOKING, input, level);
                if (recipe.isEmpty()) return "There was nothing to cook after all.";
                int n = Math.min(8, held.getCount());
                var cooked = recipe.get().value().assemble(input).copyWithCount(n);
                held.shrink(n); giveStack(p, cooked);
                return who + " cooked " + n + " for you.";
            }
            case "mend_held" -> {
                var held = p.getMainHandItem();
                if (!held.isDamaged()) return "It didn't need much after all.";
                held.setDamageValue(Math.max(0, held.getDamageValue() - Math.max(1, held.getMaxDamage() * 3 / 10)));
                return who + " mended your " + held.getHoverName().getString().toLowerCase(Locale.ROOT) + ".";
            }
            case "directions" -> {
                var town = VillageSettlements.home(v);
                if (town == null) return "They point vaguely toward the horizon.";
                p.sendSystemMessage(Component.literal("✉ " + town.name() + ": the heart of the village is at " + town.x() + ", " + town.z() + "."), false);
                return "Directions noted in your chat.";
            }
            default -> { return ""; }
        }
    }
    private static void giveStack(ServerPlayer p, ItemStack stack) { if (!p.getInventory().add(stack)) drop(p, stack); }
    static String itemId(ItemStack s) { return BuiltInRegistries.ITEM.getKey(s.getItem()).toString(); }
    private TalkWorld() {}
}
