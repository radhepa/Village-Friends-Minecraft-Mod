package dev.villagefriends.fishing;

import dev.villagefriends.hearth.HearthSeasons;
import it.unimi.dsi.fastutil.objects.ObjectArrayList;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.IdentityHashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;
import java.util.UUID;
import java.util.WeakHashMap;
import java.util.function.Supplier;
import net.fabricmc.fabric.api.attachment.v1.AttachmentTarget;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.fabricmc.fabric.api.networking.v1.ServerPlayConnectionEvents;
import net.fabricmc.fabric.api.networking.v1.ServerPlayNetworking;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.network.protocol.game.ClientboundSetSubtitleTextPacket;
import net.minecraft.network.protocol.game.ClientboundSetTitleTextPacket;
import net.minecraft.network.protocol.game.ClientboundSetTitlesAnimationPacket;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.BiomeTags;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.projectile.FishingHook;
import net.minecraft.world.item.FishingRodItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.biome.Biomes;
import net.minecraft.world.level.storage.loot.BuiltInLootTables;
import net.minecraft.world.level.storage.loot.LootParams;

/**
 * A fish on the line. When something bites a player's hook ({@code FishingHookMixin}), this decides what it is
 * ({@link Catches}): junk is reeled in the vanilla way, a fish starts the catch-bar minigame on the player's
 * screen while the bobber stays under. The client sends back how it went; a catch is handed to vanilla's own
 * reeling-in (the fish flies to the player, with experience and the "fish caught" statistic) and then logged in
 * the journal, the contest and the RPG add-on ({@link FishingEvents}). With the minigame switched off
 * ({@link FishingConfig}) bites work as in vanilla, but what comes up still comes from the fish table.
 */
public final class Angling {
    /** A fish being played: the hook, what it is, the minigame's seed and setup, when it started, and the hand with the rod. */
    record Fight(FishingHook hook, Fish fish, long seed, Minigame.Tuning tuning, long started, InteractionHand hand, Spot spot, int luck) {}
    /** A landed fish (and any treasure) on its way through vanilla's reeling-in. */
    private record Landed(List<ItemStack> stacks) {}

    private static final Map<UUID, Fight> FIGHTS = new HashMap<>();
    private static final Map<FishingHook, Landed> LANDING = new IdentityHashMap<>();
    /** Hooks whose bite was junk, so reeling in gives junk rather than rolling again. */
    private static final Set<FishingHook> JUNK = Collections.newSetFromMap(new WeakHashMap<>());
    private static final Random RANDOM = new Random();
    /** For {@code /fishing bite <fish>} and tests: the next fish to bite a player's hook. */
    private static final Map<UUID, Fish> NEXT = new HashMap<>();

    static void register() {
        ServerTickEvents.END_SERVER_TICK.register(Angling::tick);
        ServerPlayConnectionEvents.DISCONNECT.register((handler, server) -> FIGHTS.remove(handler.player.getUUID()));
    }
    public static void clear() { FIGHTS.clear(); LANDING.clear(); JUNK.clear(); NEXT.clear(); }
    /** The next bite on this player's hook will be {@code fish} (or anything, if null). */
    public static void next(ServerPlayer p, Fish fish) { if (fish == null) NEXT.remove(p.getUUID()); else NEXT.put(p.getUUID(), fish); }

    /** Whether a minigame is running for this hook (the bobber stays under and vanilla's reeling-in waits). */
    public static boolean fighting(FishingHook hook) {
        var owner = hook.getPlayerOwner();
        var f = owner == null ? null : FIGHTS.get(owner.getUUID());
        return f != null && f.hook() == hook;
    }
    /** Vanilla's reeling-in does nothing while the minigame decides (unless this is the catch being handed out). */
    public static boolean holdsLine(FishingHook hook) { return fighting(hook) && !LANDING.containsKey(hook); }

    // -- the bite -------------------------------------------------------------------------------------

    /** Something bit: pick it, and start the minigame for a fish. */
    public static void bite(FishingHook hook) {
        if (!(hook.getPlayerOwner() instanceof ServerPlayer p) || !(hook.level() instanceof ServerLevel level)) return;
        JUNK.remove(hook);
        var hand = rodHand(p);
        if (hand == null) return;
        var rodStack = p.getItemInHand(hand);
        int luck = ((dev.villagefriends.mixin.FishingHookAccess) hook).villagefriends$luck() + (int) p.getLuck();
        var spot = spot(level, hook.blockPosition(), hook.isOpenWaterFishing());
        if (!NEXT.containsKey(p.getUUID()) && FishingCompat.challenger(p, hook, spot, RodItem.bait(rodStack))) return;
        if (!FishingConfig.minigame()) return;
        var forced = NEXT.remove(p.getUUID());
        if (forced == null && Catches.kind(RANDOM, luck, false) == Catches.Kind.JUNK) { JUNK.add(hook); return; }
        var odds = new Catches.Odds(luck, RodItem.bait(rodStack), RodItem.tackle(rodStack), RodItem.rod(rodStack));
        var fish = forced != null ? forced : Catches.pick(FishTable.all(), spot, odds, RANDOM);
        if (fish == null) return;
        double treasureChance = (.15 + .03 * Math.max(0, luck)) * (odds.tackle() == Gear.Tackle.TREASURE_HOOK ? 2 : 1);
        boolean treasure = spot.openWater() && RANDOM.nextDouble() < treasureChance;
        var tuning = FishingEvents.TUNE.invoker().tune(p, fish, Minigame.Tuning.of(odds.rod(), odds.tackle(), treasure));
        long seed = RANDOM.nextLong();
        FIGHTS.put(p.getUUID(), new Fight(hook, fish, seed, tuning, level.getGameTime(), hand, spot, luck));
        ServerPlayNetworking.send(p, new FishingNet.MinigameStart(hook.getId(), fish.behavior().id(), fish.difficulty(), tuning.zone(), tuning.fishSpeed(),
                tuning.gain(), tuning.drain(), treasure, fish.legendary(), seed));
        level.playSound(null, hook.getX(), hook.getY(), hook.getZ(), SoundEvents.FISHING_BOBBER_SPLASH, SoundSource.NEUTRAL, .8F, .9F + RANDOM.nextFloat() * .2F);
    }

    /** What the player's minigame came to. */
    static void result(ServerPlayer p, FishingNet.MinigameResult r) {
        var fight = FIGHTS.remove(p.getUUID());
        if (fight == null) return;
        var hook = fight.hook();
        if (hook.isRemoved() || p.fishing != hook) return;
        var level = (ServerLevel) p.level();
        long elapsed = level.getGameTime() - fight.started();
        boolean won = r.won() && elapsed >= Minigame.quickest(fight.tuning()) - 10;
        var rodStack = p.getItemInHand(fight.hand());
        if (!won || !(rodStack.getItem() instanceof FishingRodItem)) {
            hook.discard();
            p.sendOverlayMessage(Component.literal(fight.fish().legendary() ? "The legend slipped the hook... this time." : "It got away!").withStyle(ChatFormatting.GRAY));
            level.playSound(null, p.blockPosition(), SoundEvents.FISHING_BOBBER_RETRIEVE, SoundSource.NEUTRAL, 1, .6F);
            return;
        }
        int size = Catches.size(fight.fish(), RANDOM, fight.luck(), r.perfect());
        var stacks = new ArrayList<ItemStack>();
        stacks.add(caught(p, fight.fish(), size, r.perfect()));
        if (r.treasure() && fight.tuning().treasure()) stacks.addAll(treasure(p, hook));
        LANDING.put(hook, new Landed(stacks));
        try {
            int damage = hook.retrieve(rodStack);
            rodStack.hurtAndBreak(damage, p, fight.hand().asEquipmentSlot());
        } finally {
            LANDING.remove(hook);
        }
        level.playSound(null, p.getX(), p.getY(), p.getZ(), SoundEvents.FISHING_BOBBER_RETRIEVE, SoundSource.NEUTRAL, 1, .4F / (RANDOM.nextFloat() * .4F + .8F));
        if (r.treasure() && fight.tuning().treasure()) p.sendSystemMessage(Component.literal("You fished up some treasure too!").withStyle(ChatFormatting.GOLD));
        spend(p, rodStack);
    }

    /** Fights whose hook is gone (the player put the rod away, walked off) end; the player's screen is told. */
    private static void tick(MinecraftServer server) {
        if (FIGHTS.isEmpty()) return;
        var it = FIGHTS.entrySet().iterator();
        while (it.hasNext()) {
            var e = it.next(); var f = e.getValue();
            var p = server.getPlayerList().getPlayer(e.getKey());
            boolean over = p == null || f.hook().isRemoved() || p.fishing != f.hook()
                    || p.level().getGameTime() - f.started() > Minigame.MAX_TICKS + 200;
            if (!over) continue;
            it.remove();
            if (p != null) ServerPlayNetworking.send(p, new FishingNet.MinigameEnd());
        }
    }

    // -- vanilla's reeling-in -----------------------------------------------------------------------------

    /**
     * What vanilla's reeling-in gives: the landed fish when the minigame just ended in a catch; otherwise
     * (the minigame is off, or the bite was junk) a catch rolled here from the fish table, junk or treasure.
     */
    public static ObjectArrayList<ItemStack> loot(FishingHook hook, LootParams params, Supplier<ObjectArrayList<ItemStack>> vanilla) {
        var landed = LANDING.get(hook);
        if (landed != null) return new ObjectArrayList<>(landed.stacks());
        if (!(hook.getPlayerOwner() instanceof ServerPlayer p) || !(hook.level() instanceof ServerLevel level)) return vanilla.get();
        int luck = ((dev.villagefriends.mixin.FishingHookAccess) hook).villagefriends$luck() + (int) p.getLuck();
        var server = level.getServer();
        if (JUNK.remove(hook)) return server.reloadableRegistries().getLootTable(BuiltInLootTables.FISHING_JUNK).getRandomItems(params);
        var forced = NEXT.remove(p.getUUID());
        var kind = forced != null ? Catches.Kind.FISH : Catches.kind(RANDOM, luck, hook.isOpenWaterFishing());
        if (kind == Catches.Kind.JUNK) return server.reloadableRegistries().getLootTable(BuiltInLootTables.FISHING_JUNK).getRandomItems(params);
        if (kind == Catches.Kind.TREASURE) return new ObjectArrayList<>(treasure(p, hook));
        var hand = rodHand(p);
        var rodStack = hand == null ? ItemStack.EMPTY : p.getItemInHand(hand);
        var odds = new Catches.Odds(luck, RodItem.bait(rodStack), RodItem.tackle(rodStack), RodItem.rod(rodStack));
        var fish = forced != null ? forced : Catches.pick(FishTable.all(), spot(level, hook.blockPosition(), hook.isOpenWaterFishing()), odds, RANDOM);
        if (fish == null) return vanilla.get();
        var out = new ObjectArrayList<ItemStack>();
        out.add(caught(p, fish, Catches.size(fish, RANDOM, luck, false), false));
        if (!rodStack.isEmpty()) spend(p, rodStack);
        return out;
    }

    /** Treasure: now and then one of ours (a message in a bottle, a lure, tackle), otherwise vanilla's treasure. */
    private static List<ItemStack> treasure(ServerPlayer p, FishingHook hook) {
        double roll = RANDOM.nextDouble();
        if (roll < .14) return List.of(new ItemStack(FishingItems.BOTTLE));
        if (roll < .19) return List.of(new ItemStack(FishingItems.get("legend_lure")));
        if (roll < .25) return List.of(new ItemStack(FishingItems.get(Gear.Tackle.values()[RANDOM.nextInt(Gear.Tackle.values().length)].id())));
        if (roll < .32) return List.of(new ItemStack(FishingItems.get("glow_bait"), 4 + RANDOM.nextInt(5)));
        var level = (ServerLevel) hook.level();
        var params = new LootParams.Builder(level)
                .withParameter(net.minecraft.world.level.storage.loot.parameters.LootContextParams.ORIGIN, hook.position())
                .withParameter(net.minecraft.world.level.storage.loot.parameters.LootContextParams.TOOL, p.getMainHandItem())
                .withParameter(net.minecraft.world.level.storage.loot.parameters.LootContextParams.THIS_ENTITY, hook)
                .withLuck(p.getLuck()).create(net.minecraft.world.level.storage.loot.parameters.LootContextParamSets.FISHING);
        return level.getServer().reloadableRegistries().getLootTable(BuiltInLootTables.FISHING_TREASURE).getRandomItems(params);
    }

    // -- after a catch ----------------------------------------------------------------------------------

    /**
     * Logs a catch and makes its stack: the journal (first catch, new record), a title for a legend, the contest,
     * the RPG add-on. A record or a legend is a trophy (it carries its size and won't stack with others).
     */
    public static ItemStack caught(ServerPlayer p, Fish fish, int size, boolean perfect) {
        var level = (ServerLevel) p.level();
        long day = dev.villagefriends.VillageFriends.day(level);
        var result = journal(p).record(fish.id(), size, day);
        ((AttachmentTarget) p).setAttached(Fishing.JOURNAL, result.journal());
        var stack = FishingItems.stack(fish.item(), 1);
        if (fish.legendary() || result.record() && !result.first())
            stack.set(Fishing.TROPHY, new Fishing.Trophy(size, p.getName().getString(), day));
        String name = fish.name() + " · " + Catches.cm(size);
        String note = result.first() ? "  New in your journal!" : result.record() ? "  New record! (was " + Catches.cm(result.previousBest()) + ")" : "";
        p.sendOverlayMessage(Component.literal(name).withStyle(FishingItems.rarityColor(fish.rarity()))
                .append(Component.literal(note).withStyle(ChatFormatting.YELLOW))
                .append(Component.literal(perfect ? "  Perfect!" : "").withStyle(ChatFormatting.AQUA)));
        if (fish.legendary()) {
            p.connection.send(new ClientboundSetTitlesAnimationPacket(10, 60, 20));
            p.connection.send(new ClientboundSetTitleTextPacket(Component.literal(fish.name()).withStyle(ChatFormatting.GOLD)));
            p.connection.send(new ClientboundSetSubtitleTextPacket(Component.literal("A legend, " + Catches.cm(size) + "!").withStyle(ChatFormatting.YELLOW)));
            level.playSound(null, p.blockPosition(), SoundEvents.UI_TOAST_CHALLENGE_COMPLETE, SoundSource.PLAYERS, .8F, 1);
            for (var other : level.players()) if (other != p && other.distanceToSqr(p) < 96 * 96)
                other.sendSystemMessage(Component.literal(p.getName().getString() + " landed " + fish.name() + ", " + Catches.cm(size) + "!").withStyle(ChatFormatting.GOLD));
            FishingVillage.legendCaught(p, fish);
        } else if (result.first() && fish.rarity().ordinal() >= Fish.Rarity.RARE.ordinal())
            level.playSound(null, p.blockPosition(), SoundEvents.PLAYER_LEVELUP, SoundSource.PLAYERS, .5F, 1.4F);
        Contests.caught(p, fish, size);
        FishingEvents.CAUGHT.invoker().caught(p, fish, size, perfect);
        return stack;
    }
    /** One bait used and the tackle a fish more worn. */
    private static void spend(ServerPlayer p, ItemStack rod) {
        if (p.getAbilities().instabuild) return;
        var bait = rod.get(Fishing.BAIT);
        if (bait != null && bait.count() > 0) {
            if (bait.count() <= 1) { rod.remove(Fishing.BAIT); p.sendOverlayMessage(Component.literal("You're out of bait.").withStyle(ChatFormatting.GRAY)); }
            else rod.set(Fishing.BAIT, new Fishing.Loaded(bait.item(), bait.count() - 1));
        }
        var tackle = rod.get(Fishing.TACKLE);
        if (tackle != null && tackle.count() > 0) {
            if (tackle.count() <= 1) {
                rod.remove(Fishing.TACKLE);
                var name = BuiltInRegistries.ITEM.getValue(net.minecraft.resources.Identifier.parse(tackle.item())).getDefaultInstance().getHoverName();
                p.sendSystemMessage(Component.literal("Your ").append(name).append(" wore out.").withStyle(ChatFormatting.GRAY));
            } else rod.set(Fishing.TACKLE, new Fishing.Loaded(tackle.item(), tackle.count() - 1));
        }
    }

    // -- reading the water -----------------------------------------------------------------------------

    public static Journal journal(ServerPlayer p) { return ((AttachmentTarget) p).getAttachedOrElse(Fishing.JOURNAL, Journal.EMPTY); }

    /** The hand holding a fishing rod (main first), or null. */
    public static InteractionHand rodHand(ServerPlayer p) {
        if (p.getMainHandItem().getItem() instanceof FishingRodItem) return InteractionHand.MAIN_HAND;
        if (p.getOffhandItem().getItem() instanceof FishingRodItem) return InteractionHand.OFF_HAND;
        return null;
    }

    /** The water at {@code pos} and the moment, as the fish table sees them. */
    public static Spot spot(ServerLevel level, BlockPos pos, boolean openWater) {
        var biome = level.getBiome(pos);
        boolean underground = !level.canSeeSky(pos.above()) && pos.getY() < level.getSeaLevel() - 8;
        boolean ocean = biome.is(BiomeTags.IS_OCEAN) || biome.is(BiomeTags.IS_DEEP_OCEAN);
        String water = ocean ? "ocean" : biome.is(BiomeTags.IS_RIVER) ? "river"
                : biome.is(Biomes.SWAMP) || biome.is(Biomes.MANGROVE_SWAMP) ? "swamp" : "lake";
        boolean warm = biome.is(Biomes.WARM_OCEAN) || biome.is(Biomes.LUKEWARM_OCEAN) || biome.is(Biomes.DEEP_LUKEWARM_OCEAN);
        boolean cold = biome.is(Biomes.COLD_OCEAN) || biome.is(Biomes.FROZEN_OCEAN) || biome.is(Biomes.DEEP_COLD_OCEAN) || biome.is(Biomes.DEEP_FROZEN_OCEAN);
        var waters = Spot.waters(underground, pos.getY(), water, warm, cold, biome.is(BiomeTags.IS_DEEP_OCEAN));
        return new Spot(waters, region(level, pos), Spot.times(dev.villagefriends.ResidentRoutines.timeOfDay(level)),
                level.isRaining(), level.isThundering(), HearthSeasons.season(level), openWater);
    }
    /** The land around: the commonest region among the biomes at the spot and eight points 24 blocks out. */
    public static String region(ServerLevel level, BlockPos pos) {
        var counts = new HashMap<String, Integer>();
        for (int i = -1; i < 8; i++) {
            var at = i < 0 ? pos : pos.offset((int) Math.round(Math.cos(i * Math.PI / 4) * 24), 0, (int) Math.round(Math.sin(i * Math.PI / 4) * 24));
            var key = level.getBiome(at).unwrapKey();
            if (key.isEmpty()) continue;
            var region = FishTable.region(key.get().identifier().toString());
            if (region != null) counts.merge(region, i < 0 ? 2 : 1, Integer::sum);
        }
        return counts.entrySet().stream().max(Map.Entry.comparingByValue()).map(Map.Entry::getKey).orElse("open");
    }

    private Angling() {}
}
