package dev.villagefriends;

import com.mojang.serialization.Codec;
import dev.villagefriends.quest.Board;
import dev.villagefriends.quest.Notice;
import dev.villagefriends.quest.Postings;
import dev.villagefriends.quest.QuestLog;
import dev.villagefriends.quest.Words;
import dev.villagefriends.social.Calendar;
import dev.villagefriends.talk.DialogueBank;
import dev.villagefriends.talk.Talk;
import java.util.*;
import net.fabricmc.fabric.api.attachment.v1.AttachmentRegistry;
import net.fabricmc.fabric.api.attachment.v1.AttachmentTarget;
import net.fabricmc.fabric.api.attachment.v1.AttachmentType;
import net.fabricmc.fabric.api.entity.event.v1.ServerLivingEntityEvents;
import net.fabricmc.fabric.api.networking.v1.PayloadTypeRegistry;
import net.fabricmc.fabric.api.networking.v1.ServerPlayNetworking;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.ai.gossip.GossipType;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.component.CustomData;
import net.minecraft.world.phys.Vec3;
import static dev.villagefriends.VillageFriends.*;

/**
 * Village notice boards in the world ({@link Postings} decides what goes on them). Right-clicking a board
 * opens it; players take notices down (up to three at a time), hunt monsters anywhere, gather what was
 * asked for, and carry sealed letters between residents. A finished notice is turned in at its board or
 * to the resident who posted it: emeralds, a gift from their trade, their friendship and better prices,
 * and a growing standing in the village (Helping Hand, Good Neighbor, Pillar of the Community, Hero).
 */
public final class VillageQuests {
    private static Identifier id(String path) { return Identifier.fromNamespaceAndPath("villagefriends", path); }
    /** Every village's notice board on a level, keyed by village ID. */
    public static final AttachmentType<Map<String, Board>> BOARDS = AttachmentRegistry.create(id("notice_boards"),
            b -> b.initializer(Map::<String, Board>of).persistent(Codec.unboundedMap(Codec.STRING, Board.CODEC)));
    /** The notices a player has in hand, and thanks residents still owe them. */
    public static final AttachmentType<QuestLog> QUESTS = AttachmentRegistry.create(id("quests"),
            b -> b.initializer(() -> QuestLog.EMPTY).persistent(QuestLog.CODEC).copyOnDeath());
    /** Friendship a poster gives for an answered notice. */
    static final int THANKS = 10;
    private static final Map<UUID, Long> lastAction = new HashMap<>();
    private static final Map<String, String> ICONS = Map.of("zombies", "minecraft:rotten_flesh", "skeletons", "minecraft:bone", "spiders", "minecraft:spider_eye",
            "creepers", "minecraft:gunpowder", "slimes", "minecraft:slime_ball", "witches", "minecraft:glass_bottle", "phantoms", "minecraft:phantom_membrane",
            "pillagers", "minecraft:crossbow");

    public static void register() {
        PayloadTypeRegistry.clientboundPlay().register(NoticeBoardPayload.TYPE, NoticeBoardPayload.CODEC);
        PayloadTypeRegistry.serverboundPlay().register(NoticeActionPayload.TYPE, NoticeActionPayload.CODEC);
        ServerPlayNetworking.registerGlobalReceiver(NoticeActionPayload.TYPE, (payload, context) -> act(context.player(), payload));
        ServerLivingEntityEvents.AFTER_DEATH.register((entity, source) -> {
            if (source.getEntity() instanceof ServerPlayer p && !(entity instanceof Player)) killed(p, entity);
        });
    }
    public static void clear() { lastAction.clear(); }

    // -- boards -------------------------------------------------------------------------------------

    static Map<String, Board> boards(ServerLevel level) { return ((AttachmentTarget) level).getAttachedOrCreate(BOARDS); }
    static void put(ServerLevel level, Board board) {
        var next = new HashMap<>(boards(level)); next.put(board.village(), board);
        ((AttachmentTarget) level).setAttached(BOARDS, Map.copyOf(next));
    }
    /** A village's board, freshly pinned for today. */
    static Board board(ServerLevel level, VillageRecord record) {
        var old = boards(level).getOrDefault(record.id(), Board.create(record.id()));
        var society = VillageSocieties.society(level, record.id());
        if (society == null || society.living().isEmpty()) return old;
        var next = Postings.refresh(old, society, day(level), writer(record.name()), dev.villagefriends.home.Homes.needs(level, record.id()));
        if (next != old) put(level, next);
        return next;
    }
    /** How many notes to draw on a board block (0-3): the notices up for grabs in its village. */
    public static int pinned(ServerLevel level, BlockPos pos) {
        var record = VillageSettlements.book(level).at(pos);
        return record == null ? 0 : Math.min(3, board(level, record).open(day(level)).size());
    }
    static Postings.Writer writer(String villageName) {
        return new Postings.Writer() {
            @Override public String write(String pool, Map<String, String> fill, Random random) {
                var lines = DialogueBank.current().pool(pool);
                if (lines.isEmpty()) return null;
                var values = new HashMap<>(fill); values.put("village", villageName);
                int start = random.nextInt(lines.size());
                for (int n = 0; n < lines.size(); n++) { String text = Talk.fill(lines.get((start + n) % lines.size()), values); if (text != null) return text; }
                return null;
            }
            @Override public String itemName(String item) { return VillageQuests.itemLabel(item); }
            @Override public String loved(String residentId) {
                try { return ResidentProfile.generate(UUID.fromString(residentId), "").love(); } catch (RuntimeException e) { return ""; }
            }
        };
    }
    /** "iron ingot" for "minecraft:iron_ingot", as the game names it. */
    static String itemLabel(String item) {
        var it = BuiltInRegistries.ITEM.getValue(Identifier.parse(item));
        if (it == null || it == Items.AIR) return itemName(item);
        String name = new ItemStack(it).getHoverName().getString();
        return name.isBlank() || name.contains(".") ? itemName(item) : name.toLowerCase(Locale.ROOT);
    }

    // -- players ------------------------------------------------------------------------------------

    static QuestLog log(ServerPlayer p) { return target(p).getAttachedOrCreate(QUESTS); }
    static void log(ServerPlayer p, QuestLog log) { target(p).setAttached(QUESTS, log); }
    private static String me(ServerPlayer p) { return p.getUUID().toString(); }
    private static String first(String name) { return TalkWorld.firstName(name); }
    private static ServerLevel origin(ServerPlayer p, QuestLog.Quest q) {
        var level = p.level().getServer().getLevel(ResourceKey.create(Registries.DIMENSION, Identifier.parse(q.dimension())));
        return level == null ? (ServerLevel) p.level() : level;
    }
    /** A resident, if they are loaded on that level. */
    static Villager resident(ServerLevel level, String residentId) {
        for (var v : CompanionController.loaded) if (v.isAlive() && v.level() == level && VillageSocieties.id(v).equals(residentId)) return v;
        return null;
    }
    static int count(ServerPlayer p, String item) {
        var inventory = p.getInventory(); int n = 0;
        for (int i = 0; i < inventory.getContainerSize(); i++) {
            var stack = inventory.getItem(i);
            if (!stack.isEmpty() && BuiltInRegistries.ITEM.getKey(stack.getItem()).toString().equals(item)) n += stack.getCount();
        }
        return n;
    }
    private static void remove(ServerPlayer p, String item, int amount) {
        var inventory = p.getInventory();
        for (int i = 0; i < inventory.getContainerSize() && amount > 0; i++) {
            var stack = inventory.getItem(i);
            if (stack.isEmpty() || !BuiltInRegistries.ITEM.getKey(stack.getItem()).toString().equals(item)) continue;
            int used = Math.min(amount, stack.getCount());
            stack.shrink(used); amount -= used;
        }
        // Residents keep the milk or lava, not your bucket.
        if (item.endsWith("_bucket")) giveItem(p, "minecraft:bucket", 1);
        inventory.setChanged();
    }
    /** Finished and ready to turn in: the monsters are defeated, or what was asked for is in the player's pack. */
    static boolean ready(ServerPlayer p, QuestLog.Quest q) {
        var n = q.notice();
        return switch (n.kind()) {
            case Notice.HUNT -> q.hunted();
            case Notice.FETCH, Notice.BIRTHDAY -> count(p, n.target()) >= n.count();
            case Notice.HOUSE -> dev.villagefriends.home.Homes.housed(origin(p, q), q.village(), n.poster());
            default -> false;
        };
    }

    // -- the board screen ---------------------------------------------------------------------------

    public static void open(ServerPlayer p, BlockPos pos) { send(p, pos, ""); }
    static void send(ServerPlayer p, BlockPos pos, String message) {
        if (!ServerPlayNetworking.canSend(p, NoticeBoardPayload.TYPE)) return;
        var level = (ServerLevel) p.level();
        var record = VillageSettlements.discover(level, pos);
        if (record == null) { p.sendSystemMessage(Component.literal("Nobody reads this board yet. Put it up in a village, or claim the place with a Village Marker."), true); return; }
        var board = board(level, record);
        long today = day(level);
        var society = VillageSocieties.society(level, record.id());
        var log = log(p);
        var cards = new ArrayList<NoticeBoardPayload.Card>();
        for (var n : board.notices()) {
            String state; int progress = 0;
            var mine = n.taker().equals(me(p)) ? log.find(record.id(), n.id()) : null;
            if (n.taken() && mine == null) state = "taken";
            else if (mine != null) { state = ready(p, mine) ? "ready" : "mine"; progress = progress(p, mine); }
            else if (n.open(today)) state = "open";
            else continue;
            String poster = society != null && society.has(n.poster()) ? society.nameOf(n.poster()) : n.posterName();
            cards.add(new NoticeBoardPayload.Card(n.id(), n.kind(), n.title(), n.text(), poster, job(n.posterJob()), objective(n), rewardText(n), icon(n), state,
                    progress, n.count(), due(n, today, state)));
        }
        var tasks = new ArrayList<NoticeBoardPayload.Task>();
        for (var q : log.quests())
            tasks.add(new NoticeBoardPayload.Task(q.village(), q.id(), q.notice().title(), q.village().equals(record.id()) ? "This board" : q.villageName(),
                    progressText(p, q), ready(p, q), icon(q.notice())));
        var birthdays = new ArrayList<String>();
        if (society != null) for (var t : society.birthdays(today, 6)) {
            int until = Calendar.daysUntil(t.birthday(), today);
            birthdays.add((until == 0 ? "Today! " : Calendar.birthdayDate(t.birthday()) + " · ") + t.name() + (until > 0 && until <= 7 ? " (" + Calendar.when(until) + ")" : ""));
        }
        int favors = board.favors(me(p)), tier = Board.standing(favors);
        String hint = tier + 1 < Board.STANDING.length ? (Board.STANDING[tier + 1] - favors) + " more to become " + Board.title(tier + 1, record.name())
                : "Everyone here knows your name. Trades are cheaper all over the village.";
        ServerPlayNetworking.send(p, new NoticeBoardPayload(record.id(), record.name(), Calendar.longDate(today),
                Board.title(tier, record.name()) + " · " + favors + (favors == 1 ? " notice" : " notices") + " answered", hint, pos.asLong(),
                cards, tasks, birthdays, message == null ? "" : message));
    }
    private static String job(String job) {
        return job.equals("none") ? "Neighbor" : job.equals("nitwit") ? "Free Spirit" : VillageProfessions.label(job);
    }
    private static int progress(ServerPlayer p, QuestLog.Quest q) {
        var n = q.notice();
        return switch (n.kind()) {
            case Notice.HUNT -> q.progress();
            case Notice.FETCH, Notice.BIRTHDAY -> Math.min(n.count(), count(p, n.target()));
            default -> 0;
        };
    }
    static String objective(Notice n) {
        return switch (n.kind()) {
            case Notice.HUNT -> "Defeat " + Words.mobs(n.count(), n.target()) + (n.target().equals("zombies") ? " (husks and drowned count)" : n.target().equals("skeletons") ? " (strays count)" : "");
            case Notice.FETCH -> "Bring " + Words.count(n.count(), itemLabel(n.target())) + " to " + first(n.posterName()) + " or this board";
            case Notice.LETTER -> "Carry a sealed letter to " + n.who();
            case Notice.BIRTHDAY -> "Bring " + Words.count(n.count(), itemLabel(n.target())) + " for " + first(n.who()) + "'s birthday";
            case Notice.HOUSE -> "Build a house with " + n.count() + " beds in the village and put up a House Plaque for " + first(n.posterName()) + "'s family";
            default -> n.title();
        };
    }
    static String rewardText(Notice n) {
        var r = n.reward(); var parts = new ArrayList<String>();
        if (r.emeralds() > 0) parts.add(r.emeralds() + (r.emeralds() == 1 ? " emerald" : " emeralds"));
        if (!r.item().isEmpty() && r.count() > 0) parts.add(Words.count(r.count(), itemLabel(r.item())));
        parts.add("friendship with " + first(n.posterName()));
        return String.join(" · ", parts);
    }
    static String icon(Notice n) {
        return switch (n.kind()) {
            case Notice.HUNT -> ICONS.getOrDefault(n.target(), "minecraft:iron_sword");
            case Notice.LETTER -> "villagefriends:sealed_letter";
            case Notice.HOUSE -> "villagefriends:house_plaque";
            default -> n.target();
        };
    }
    private static String due(Notice n, long today, String state) {
        return switch (state) {
            case "ready" -> "Ready to turn in!";
            case "mine" -> "In hand";
            case "taken" -> "Someone took this one";
            default -> n.expires() - today <= 1 ? "Comes down tomorrow" : "Up for " + (n.expires() - today) + " more days";
        };
    }
    private static String progressText(ServerPlayer p, QuestLog.Quest q) {
        var n = q.notice();
        return switch (n.kind()) {
            case Notice.HUNT -> q.progress() + "/" + n.count() + " " + Words.plural(Words.mobs(1, n.target()).substring(Words.mobs(1, n.target()).indexOf(' ') + 1));
            case Notice.FETCH, Notice.BIRTHDAY -> "Have " + Math.min(n.count(), count(p, n.target())) + "/" + n.count() + " " + Words.plural(itemLabel(n.target()));
            case Notice.LETTER -> "Deliver to " + first(n.who());
            case Notice.HOUSE -> ready(p, q) ? first(n.posterName()) + " has moved in!" : "A house with " + n.count() + " beds and a plaque";
            default -> "";
        };
    }

    // -- actions ------------------------------------------------------------------------------------

    static void act(ServerPlayer p, NoticeActionPayload a) {
        long now = p.level().getGameTime();
        if (lastAction.getOrDefault(p.getUUID(), -10L) + 4 > now) return;
        lastAction.put(p.getUUID(), now);
        var level = (ServerLevel) p.level(); var pos = BlockPos.of(a.pos());
        if (!level.getBlockState(pos).is(VillageBlocks.get("notice_board")) || p.distanceToSqr(Vec3.atCenterOf(pos)) > 8 * 8 || p.isSpectator()) return;
        var record = VillageSettlements.discover(level, pos);
        if (record == null) return;
        String message = switch (a.action()) {
            case "accept" -> record.id().equals(a.village()) ? accept(p, level, record, a.notice()) : "";
            case "claim" -> record.id().equals(a.village()) ? claimAtBoard(p, a.village(), a.notice()) : "";
            case "abandon" -> abandon(p, a.village(), a.notice());
            case "ledger" -> { VillageLedger.openAt(p, pos); yield null; }
            default -> "";
        };
        if (message != null) send(p, pos, message);
    }
    static String accept(ServerPlayer p, ServerLevel level, VillageRecord record, String id) {
        var board = board(level, record); var n = board.find(id); long today = day(level);
        if (n == null || !n.open(today)) return "Someone else got to that notice first.";
        var log = log(p);
        if (log.full()) return "You already have " + QuestLog.MAX + " notices in hand. Finish or drop one first.";
        put(level, board.take(id, me(p)));
        var taken = n.take(me(p));
        log(p, log.add(new QuestLog.Quest(record.id(), record.name(), level.dimension().identifier().toString(), taken, 0, today)));
        if (n.kind().equals(Notice.LETTER)) giveStack(p, letter(taken, record.id()));
        p.level().playSound(null, p.blockPosition(), SoundEvents.BOOK_PAGE_TURN, SoundSource.PLAYERS, 1F, 1F);
        return n.kind().equals(Notice.LETTER) ? "You took " + first(n.posterName()) + "'s sealed letter for " + first(n.who()) + "."
                : "You took down " + first(n.posterName()) + "'s notice: " + n.title() + ".";
    }
    static String abandon(ServerPlayer p, String village, String id) {
        var log = log(p); var q = log.find(village, id);
        if (q == null) return "";
        log(p, log.drop(village, id));
        var origin = origin(p, q); var board = boards(origin).get(village);
        if (board != null) put(origin, board.release(id, day(origin)));
        if (q.notice().kind().equals(Notice.LETTER)) {
            int slot = letterSlot(p, l -> l.getStringOr("quest", "").equals(id) && l.getStringOr("village", "").equals(village));
            if (slot >= 0) p.getInventory().getItem(slot).shrink(1);
        }
        return "You pinned " + first(q.notice().posterName()) + "'s notice back up.";
    }
    static String claimAtBoard(ServerPlayer p, String village, String id) {
        var q = log(p).find(village, id);
        if (q == null) return "";
        String missing = gather(p, q);
        if (missing != null) return missing;
        return "Notice answered! " + complete(p, q, null);
    }
    /** Takes what a finished notice needs from the player; null when done, otherwise what is still missing. */
    private static String gather(ServerPlayer p, QuestLog.Quest q) {
        var n = q.notice();
        switch (n.kind()) {
            case Notice.HUNT -> { return q.hunted() ? null : "Defeat " + (n.count() - q.progress()) + " more first."; }
            case Notice.HOUSE -> { return ready(p, q) ? null : "Build a house with " + n.count() + " beds, put up a House Plaque, and wait for " + first(n.posterName()) + "'s family to move in."; }
            case Notice.FETCH, Notice.BIRTHDAY -> {
                int have = count(p, n.target());
                if (have < n.count()) return "You need " + Words.count(n.count(), itemLabel(n.target())) + " (you have " + have + ").";
                remove(p, n.target(), n.count());
                return null;
            }
            default -> { return "Hand the letter to " + first(n.who()) + " in person."; }
        }
    }
    /**
     * Pays out a finished notice: emeralds and a gift, the poster's thanks (now if they're nearby, next time
     * you talk if not), a line in the village news, and one more notice toward the player's standing.
     */
    static String complete(ServerPlayer p, QuestLog.Quest q, Villager poster) {
        var n = q.notice(); var origin = origin(p, q); long today = day(origin);
        var r = n.reward();
        if (r.emeralds() > 0) giveItem(p, "minecraft:emerald", r.emeralds());
        if (!r.item().isEmpty() && r.count() > 0) giveItem(p, r.item(), r.count());
        p.giveExperiencePoints(3 + r.emeralds());
        var board = boards(origin).get(q.village());
        int before = board == null ? 0 : board.favors(me(p));
        if (board != null) put(origin, board.remove(n.id()).favor(me(p)));
        var society = VillageSocieties.society(origin, q.village());
        if (society != null) VillageSocieties.put(origin, society.helped(n.poster(), p.getName().getString(), today));
        if (poster == null) poster = resident(origin, n.poster());
        if (poster != null) thank(poster, p, n, today);
        if (n.kind().equals(Notice.BIRTHDAY)) {
            var celebrant = resident(origin, n.about());
            if (celebrant != null) { reward(celebrant, p, 8); saveBond(celebrant, p, bond(celebrant, p).remember(today, "You helped make my birthday special.")); }
        }
        log(p, log(p).done(q.village(), n.id(), poster == null ? n.poster() : "", THANKS));
        standing(p, q.village(), q.villageName(), before, before + 1);
        p.level().playSound(null, p.blockPosition(), SoundEvents.PLAYER_LEVELUP, SoundSource.PLAYERS, .5F, 1.6F);
        var parts = new ArrayList<String>();
        if (r.emeralds() > 0) parts.add("+" + r.emeralds() + (r.emeralds() == 1 ? " emerald" : " emeralds"));
        if (!r.item().isEmpty() && r.count() > 0) parts.add(Words.count(r.count(), itemLabel(r.item())));
        parts.add(poster != null ? "+" + THANKS + " friendship with " + first(name(poster)) : first(n.posterName()) + " will thank you in person");
        String summary = String.join(", ", parts) + ".";
        // The status line may be busy with a friendship level-up, so the rewards go in chat too.
        p.sendSystemMessage(Component.literal("✔ " + n.title() + " answered: " + summary).withStyle(ChatFormatting.GREEN), false);
        return summary;
    }
    private static void thank(Villager poster, ServerPlayer p, Notice n, long today) {
        reward(poster, p, THANKS);
        saveBond(poster, p, bond(poster, p).trust(2).remember(today, "You answered my notice: " + n.title().toLowerCase(Locale.ROOT) + "."));
        // Word gets around: the poster gives you better prices.
        poster.getGossips().add(p.getUUID(), GossipType.MINOR_POSITIVE, 15);
    }
    /** A new standing in the village: a message, better prices from everyone there, and for its hero, Hero of the Village. */
    private static void standing(ServerPlayer p, String village, String villageName, int before, int after) {
        int was = Board.standing(before), now = Board.standing(after);
        if (now <= was) return;
        p.sendSystemMessage(Component.literal("★ " + villageName + ": you are now " + (now == Board.STANDING.length - 1 ? "the " : "a ") + Board.title(now, villageName) + "!")
                .withStyle(ChatFormatting.GOLD), false);
        int gossip = switch (now) { case 2 -> 5; case 3 -> 10; case 4 -> 20; default -> 0; };
        if (gossip > 0) for (var v : CompanionController.loaded) {
            var home = target(v).getAttached(HOME);
            if (home != null && home.village().equals(village) && v.isAlive()) v.getGossips().add(p.getUUID(), GossipType.MAJOR_POSITIVE, gossip);
        }
        if (now == 3) giveItem(p, "minecraft:emerald", 8);
        if (now == 4) p.addEffect(new MobEffectInstance(MobEffects.HERO_OF_THE_VILLAGE, 48000, 0));
    }

    // -- letters ------------------------------------------------------------------------------------

    private static ItemStack letter(Notice n, String village) {
        var stack = new ItemStack(VillageItems.get("sealed_letter"));
        stack.set(DataComponents.ITEM_NAME, Component.literal("Letter for " + n.who()));
        var tag = new CompoundTag();
        tag.putString("quest", n.id()); tag.putString("village", village); tag.putString("to", n.target());
        tag.putString("from", n.poster()); tag.putString("about", n.about()); tag.putString("sender", first(n.posterName()));
        CustomData.set(DataComponents.CUSTOM_DATA, stack, tag);
        return stack;
    }
    private static int letterSlot(ServerPlayer p, java.util.function.Predicate<CompoundTag> test) {
        var inventory = p.getInventory(); var item = VillageItems.get("sealed_letter");
        for (int i = 0; i < inventory.getContainerSize(); i++) {
            var stack = inventory.getItem(i);
            if (!stack.is(item)) continue;
            var data = stack.get(DataComponents.CUSTOM_DATA);
            if (data != null && test.test(data.copyTag())) return i;
        }
        return -1;
    }
    private static void giveStack(ServerPlayer p, ItemStack stack) { if (!p.getInventory().add(stack)) drop(p, stack); }
    private static void deliver(ServerPlayer p, Villager v) {
        String id = VillageSocieties.id(v);
        int slot = letterSlot(p, tag -> tag.getStringOr("to", "").equals(id));
        if (slot < 0) { show(p, v, "talk", "A letter? I don't see one. Maybe it's still at the bottom of your pack.", "No letter for them in your pack.", false, Emote.QUESTION); return; }
        var tag = p.getInventory().getItem(slot).get(DataComponents.CUSTOM_DATA).copyTag();
        p.getInventory().getItem(slot).shrink(1);
        String about = tag.getStringOr("about", "friend"), sender = tag.getStringOr("sender", "a friend"), from = tag.getStringOr("from", "");
        long today = day(v.level());
        String line = TalkWorld.say(v, p, "letter.read." + about, Map.of("sender", sender));
        reward(v, p, 6);
        saveBond(v, p, bond(v, p).remember(today, "You brought me a letter from " + sender + "."));
        var society = VillageSocieties.of(v); var origin = VillageSocieties.origin(v);
        if (society != null && origin != null) VillageSocieties.put(origin, society.letter(from, id, today, about.equals("apology")));
        var q = log(p).find(tag.getStringOr("village", ""), tag.getStringOr("quest", ""));
        String status = "+6 friendship with " + first(name(v)) + ".";
        if (q != null) status = complete(p, q, null) + " +6 friendship with " + first(name(v)) + ".";
        var mood = switch (about) { case "crush" -> Emote.BLUSH; case "partner" -> Emote.HEART; case "apology" -> Emote.SPARKLE; default -> Emote.NOTE; };
        show(p, v, "talk", line != null ? line : "A letter from " + sender + "? For me? I'll read it somewhere quiet. Thank you for carrying it.", status, false, mood);
    }

    // -- conversation -------------------------------------------------------------------------------

    /** "I have a letter for you" and "About your notice..." when the player has something for this resident. */
    static List<FriendshipPayload.Choice> choices(Villager v, ServerPlayer p) {
        var out = new ArrayList<FriendshipPayload.Choice>(); String id = VillageSocieties.id(v);
        if (letterSlot(p, tag -> tag.getStringOr("to", "").equals(id)) >= 0) out.add(new FriendshipPayload.Choice("deliver_letter", "I have a letter for you", true));
        for (var q : log(p).quests())
            if (q.notice().poster().equals(id) && !q.notice().kind().equals(Notice.LETTER) && ready(p, q)) { out.add(new FriendshipPayload.Choice("notice_turn_in", "About your notice...", true)); break; }
        return out;
    }
    static boolean handle(ServerPlayer p, Villager v, String action) {
        switch (action) {
            case "deliver_letter" -> deliver(p, v);
            case "notice_turn_in" -> {
                String id = VillageSocieties.id(v);
                var q = log(p).quests().stream().filter(x -> x.notice().poster().equals(id) && ready(p, x)).findFirst().orElse(null);
                String missing = q == null ? "Nothing to turn in yet." : gather(p, q);
                if (missing != null) { show(p, v, "talk", NarrativeEngine.greeting(v, p), missing, false); return true; }
                String status = complete(p, q, v);
                String line = TalkWorld.say(v, p, v.isBaby() ? "baby.notice.thanks" : "notice.thanks." + q.notice().kind(), Map.of());
                show(p, v, "talk", line != null ? line : "You did it! Thank you. I'll be telling everyone at the well.", status, false, Emote.HEART);
            }
            default -> { return false; }
        }
        return true;
    }
    /** A thank-you owed from a notice turned in at the board while they were away; null if none. */
    static String thanks(Villager v, ServerPlayer p) {
        var log = log(p); String id = VillageSocieties.id(v);
        int points = log.thanks().getOrDefault(id, 0);
        if (points <= 0) return null;
        log(p, log.thanked(id));
        long today = day(v.level());
        reward(v, p, points);
        saveBond(v, p, bond(v, p).trust(2).remember(today, "You answered my notice on the board."));
        v.getGossips().add(p.getUUID(), GossipType.MINOR_POSITIVE, 15);
        String line = TalkWorld.say(v, p, v.isBaby() ? "baby.notice.thanks.later" : "notice.thanks.later", Map.of());
        return line != null ? line : "I saw my notice came down from the board. That was you, wasn't it? Thank you!";
    }

    // -- hunting ------------------------------------------------------------------------------------

    static void killed(ServerPlayer p, Entity entity) {
        String group = Postings.group(BuiltInRegistries.ENTITY_TYPE.getKey(entity.getType()).toString());
        if (group.isEmpty()) return;
        var log = log(p); var hunting = log.hunting(group);
        if (hunting.isEmpty()) return;
        for (var q : hunting) {
            var next = q.progress(q.progress() + 1);
            log = log.replace(next);
            var n = next.notice();
            if (next.hunted()) {
                p.sendSystemMessage(Component.literal("✔ " + n.title() + " - done! Tell " + first(n.posterName()) + ", or turn it in at the " + next.villageName() + " notice board.")
                        .withStyle(ChatFormatting.GREEN), false);
                p.level().playSound(null, p.blockPosition(), SoundEvents.NOTE_BLOCK_CHIME.value(), SoundSource.PLAYERS, .8F, 1.4F);
            } else p.sendSystemMessage(Component.literal(n.title() + ": " + next.progress() + "/" + n.count()), true);
        }
        log(p, log);
    }

    private VillageQuests() {}
}
