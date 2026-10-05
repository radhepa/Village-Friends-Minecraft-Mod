package dev.villagefriends;

import java.util.List;
import java.util.UUID;
import java.util.Set;
import com.mojang.serialization.Codec;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.attachment.v1.*;
import net.fabricmc.fabric.api.entity.event.v1.ServerLivingEntityEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerEntityEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.fabricmc.fabric.api.event.player.UseEntityCallback;
import net.fabricmc.fabric.api.networking.v1.*;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.SpawnEggItem;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public final class VillageFriends implements ModInitializer {
    public static final Logger LOGGER = LoggerFactory.getLogger("VillageFriends");
    private static Identifier id(String path) { return Identifier.fromNamespaceAndPath("villagefriends", path); }
    public static final AttachmentType<FriendshipBook> FRIENDSHIPS = AttachmentRegistry.create(id("friendships"),
            b -> b.initializer(FriendshipBook::empty).persistent(FriendshipBook.CODEC));
    public static final AttachmentType<String> LOOK = AttachmentRegistry.create(id("look"),
            b -> b.persistent(Codec.STRING).syncWith(ByteBufCodecs.STRING_UTF8, AttachmentSyncPredicate.all()));
    public static final AttachmentType<ResidentProfile> PROFILE = AttachmentRegistry.create(id("resident"), b -> b.persistent(ResidentProfile.CODEC));
    public static final AttachmentType<BondBook> BONDS = AttachmentRegistry.create(id("bonds"), b -> b.initializer(BondBook::empty).persistent(BondBook.CODEC));
    public static final AttachmentType<SharedHistory> SHARED = AttachmentRegistry.create(id("shared_history"), b -> b.initializer(() -> SharedHistory.EMPTY).persistent(SharedHistory.CODEC));
    public static final AttachmentType<CompanionState> COMPANION = AttachmentRegistry.create(id("companion"), b -> b.initializer(() -> CompanionState.NONE).persistent(CompanionState.CODEC));
    public static final AttachmentType<String> PARTY = AttachmentRegistry.create(id("party"), b -> b.initializer(() -> "").persistent(Codec.STRING));
    public static final AttachmentType<VillageBook> VILLAGES = AttachmentRegistry.create(id("villages"), b -> b.initializer(() -> VillageBook.EMPTY).persistent(VillageBook.CODEC));
    public static final AttachmentType<ResidentHome> HOME = AttachmentRegistry.create(id("home_village"), b -> b.persistent(ResidentHome.CODEC));
    public static final AttachmentType<String> HOME_LABEL = AttachmentRegistry.create(id("home_label"), b -> b.persistent(Codec.STRING));
    private static final Set<String> TOPICS = Set.of("chat", "work", "adventure", "joke");
    public static AttachmentTarget target(Entity entity) { return (AttachmentTarget) entity; }

    @Override public void onInitialize() {
        VillageMarkerBlock.register();
        VillageFoundation.register();
        NarrativeContent.register();
        ResidentNames.register();
        net.fabricmc.fabric.api.object.builder.v1.entity.FabricDefaultAttributeRegistry.register(net.minecraft.world.entity.EntityTypes.VILLAGER,
                Villager.createAttributes().add(net.minecraft.world.entity.ai.attributes.Attributes.ATTACK_DAMAGE, 1).add(net.minecraft.world.entity.ai.attributes.Attributes.ATTACK_KNOCKBACK, 0));
        ServerEntityEvents.ENTITY_LOAD.register((entity, level) -> {
            if (entity instanceof Villager villager) { ensureIdentity(villager); CompanionController.loaded.add(villager); VillageSettlements.identify(villager,false); }
        });
        ServerEntityEvents.ENTITY_UNLOAD.register((entity, level) -> { if (entity instanceof Villager v) CompanionController.unload(v); });
        ServerPlayConnectionEvents.JOIN.register((handler, sender, server) -> CompanionController.resetParty(handler.getPlayer()));
        ServerPlayConnectionEvents.DISCONNECT.register((handler, server) -> CompanionController.resetParty(handler.getPlayer()));
        ServerLifecycleEvents.SERVER_STOPPED.register(server -> { CompanionController.clear(); VillageSettlements.clear(); });
        ServerTickEvents.END_SERVER_TICK.register(CompanionController::tick);
        ServerTickEvents.END_SERVER_TICK.register(VillageSettlements::tick);
        ServerLivingEntityEvents.MOB_CONVERSION.register((before, after, params) -> transferIdentity(before, after));
        ServerLivingEntityEvents.ALLOW_DAMAGE.register(CompanionController::allowDamage);
        ServerLivingEntityEvents.ALLOW_DEATH.register(CompanionController::allowDeath);
        PayloadTypeRegistry.clientboundPlay().register(FriendshipPayload.TYPE, FriendshipPayload.CODEC);
        PayloadTypeRegistry.serverboundPlay().register(ActionPayload.TYPE, ActionPayload.CODEC);
        ServerPlayNetworking.registerGlobalReceiver(ActionPayload.TYPE, (payload, context) -> handleAction(context.player(), payload));
        UseEntityCallback.EVENT.register((player, world, hand, entity, hit) -> {
            if (!(entity instanceof Villager villager) || hand != InteractionHand.MAIN_HAND || player.isSpectator() || player.isShiftKeyDown()) return InteractionResult.PASS;
            var held = player.getMainHandItem();
            if (held.is(Items.NAME_TAG) || held.getItem() instanceof SpawnEggItem) return InteractionResult.PASS;
            if (world.isClientSide() || !(player instanceof ServerPlayer sp) || !ServerPlayNetworking.canSend(sp, FriendshipPayload.TYPE) || !validTarget(sp, villager)) return InteractionResult.PASS;
            if (villager.isSleeping()) { sp.sendSystemMessage(Component.literal("Your neighbor is sleeping. Visit again in the morning!"), true); return InteractionResult.SUCCESS_SERVER; }
            ensureIdentity(villager);
            VillageSettlements.identify(villager,true);
            saveBond(villager, sp, bond(villager, sp).visit(day(world)));
            villager.getLookControl().setLookAt(player, 30, 30);
            show(sp, villager, "talk", NarrativeEngine.greeting(villager, sp), "Welcome, neighbor!", true);
            return InteractionResult.SUCCESS_SERVER;
        });
        LOGGER.info("Village Friends ready: persistent residents, written stories, adventures, and modular appearances.");
    }
    public static void ensureIdentity(Villager v) {
        var t = target(v);
        if (!t.hasAttached(PROFILE)) {
            t.setAttached(PROFILE, ResidentProfile.generate(v.getUUID(), ""));
            var old = t.getAttached(FRIENDSHIPS);
            if (old != null && !t.hasAttached(BONDS)) {
                BondBook migrated = BondBook.empty();
                for (var e : old.relationships().entrySet()) {
                    try { migrated = migrated.with(UUID.fromString(e.getKey()), BondState.migrated(e.getValue().level())); }
                    catch (IllegalArgumentException ignored) { LOGGER.warn("Skipping malformed legacy player ID"); }
                }
                t.setAttached(BONDS, migrated);
            }
        }
        var profile = t.getAttached(PROFILE);
        if (dev.villagefriends.outfit.ResidentLook.parse(profile.look()) == null) {
            // Reset only appearance when retiring the previous wardrobe; preserve resident history.
            profile = new ResidentProfile(profile.id(), profile.personality(), profile.hobby(), profile.value(),
                profile.love(), profile.dislike(), profile.story(), ResidentAppearance.generate(UUID.fromString(profile.id())));
            t.setAttached(PROFILE, profile);
        }
        String look = profile.look();
        if (!v.hasCustomName()) v.setCustomName(Component.literal(Dialogue.name(v.getUUID(),look)));
        v.setCustomNameVisible(true);
        if (!look.equals(t.getAttached(LOOK))) t.setAttached(LOOK, look);
    }
    private static <T> void copy(Entity before, Entity after, AttachmentType<T> type) {
        T data = target(before).getAttached(type); if (data != null) target(after).setAttached(type, data);
    }
    public static void transferIdentity(Entity before, Entity after) {
        if (!target(before).hasAttached(PROFILE)) return;
        if (before instanceof Villager v) CompanionController.unload(v);
        copy(before, after, PROFILE); copy(before, after, LOOK);
        copy(before, after, FRIENDSHIPS); copy(before, after, BONDS); copy(before, after, SHARED);
        copy(before, after, HOME); copy(before, after, HOME_LABEL);
        target(after).setAttached(COMPANION, CompanionState.NONE);
        if (before.hasCustomName()) after.setCustomName(before.getCustomName());
        after.setCustomNameVisible(true);
        if (after instanceof Villager v) ensureIdentity(v);
    }
    public static ResidentProfile profile(Villager v) { ensureIdentity(v); return target(v).getAttached(PROFILE); }
    public static FriendshipState state(Villager v, ServerPlayer p) { return target(v).getAttachedOrCreate(FRIENDSHIPS).get(p.getUUID()); }
    public static void save(Villager v, ServerPlayer p, FriendshipState s) { target(v).setAttached(FRIENDSHIPS, target(v).getAttachedOrCreate(FRIENDSHIPS).with(p.getUUID(), s)); }
    public static BondState bond(Villager v, ServerPlayer p) { return target(v).getAttachedOrCreate(BONDS).get(p.getUUID()); }
    public static void saveBond(Villager v, ServerPlayer p, BondState b) { target(v).setAttached(BONDS, target(v).getAttachedOrCreate(BONDS).with(p.getUUID(), b)); }
    public static SharedHistory shared(Villager v) { return target(v).getAttachedOrCreate(SHARED); }
    public static void shared(Villager v, SharedHistory s) { target(v).setAttached(SHARED, s); }
    public static void reward(Villager v, ServerPlayer p, int points) {
        var old = state(v, p);
        var next = new FriendshipState(old.points() + points, old.talkDay(), old.giftDay(), old.giftsToday(), old.lastGift());
        save(v, p, next); celebrate(v, old, next);
    }
    public static boolean validTarget(ServerPlayer p, Villager v) { return p.isAlive() && !p.isSpectator() && v.isAlive() && p.level() == v.level() && p.distanceToSqr(v) <= 36 && p.hasLineOfSight(v); }
    public static void handleAction(ServerPlayer player, ActionPayload action) {
        Entity entity = player.level().getEntity(action.entityId());
        if (!(entity instanceof Villager v) || !v.getUUID().equals(action.villagerId()) || !validTarget(player, v) || v.isSleeping()) {
            player.sendSystemMessage(Component.literal("Move closer to an awake villager to keep talking."), true); return;
        }
        String a = action.action();
        if (a.equals("trade")) { if (!v.isBaby() && !v.isTrading() && !CompanionController.state(v).downed()) v.mobInteract(player, InteractionHand.MAIN_HAND); return; }
        if (TOPICS.contains(a)) {
            var old = state(v, player); var next = old.talk(day(v.level())); save(v, player, next);
            saveBond(v, player, bond(v, player).visit(day(v.level())));
            String reply = NarrativeEngine.conversation(v, player, a);
            celebrate(v, old, next);
            show(player, v, "talk", reply, old.canTalk(day(v.level())) ? "+4 friendship - thanks for visiting!" : "Happy to keep talking. Friendship rewards return tomorrow.", false); return;
        }
        if (a.equals("gift")) { giveGift(player, v); return; }
        if (!NarrativeEngine.handle(player, v, a) && !CompanionController.handle(player, v, a))
            show(player, v, "talk", NarrativeEngine.greeting(v, player), "That choice is no longer available.", false);
    }
    private static void giveGift(ServerPlayer p, Villager v) {
        var old = state(v, p); long today = day(v.level());
        if (old.giftsLeft(today) == 0) { show(p, v, "talk", "You've been so generous today. Save your next gift for tomorrow!", "Your item was kept.", false); return; }
        var stack = p.getMainHandItem(); String item = BuiltInRegistries.ITEM.getKey(stack.getItem()).toString();
        var profile = profile(v); var b = bond(v, p);
        if (stack.isEmpty() || item.equals(profile.dislike())) {
            String reply = stack.isEmpty() ? "Hold something in your main hand before offering it." : "Thank you for thinking of me, but " + itemName(item) + " isn't something I enjoy. I'd rather you keep it.";
            show(p, v, "talk", reply, "Gift declined. Your item and gift allowance were kept.", false); return;
        }
        int value = item.equals(profile.love()) ? 14 : GiftPreferences.value(profession(v), v.isBaby(), item);
        if (value == 0) { show(p, v, "talk", "That's thoughtful, but perhaps a flower, treat, or something for my hobby?", "Your item was kept.", false); return; }
        var next = old.gift(today, item, value); if (!p.getAbilities().instabuild) stack.shrink(1); save(v, p, next);
        saveBond(v, p, b.trust(item.equals(profile.love()) ? 2 : 1).remember(today, "You gave me " + itemName(item) + "."));
        celebrate(v, old, next);
        show(p, v, "talk", item.equals(profile.love()) ? "You remembered! " + itemName(item) + " is one of my favorites. Thank you for paying attention."
                : "What a lovely surprise. Thank you for thinking of me!", "+" + (next.points() - old.points()) + " friendship. Gifts help; shared experiences deepen our bond.", false);
    }
    public static void giveItem(ServerPlayer p, String id, int count) {
        var item = BuiltInRegistries.ITEM.getValue(Identifier.parse(id));
        if (item == null || item == Items.AIR) return;
        var stack = new ItemStack(item, count); if (!p.getInventory().add(stack)) drop(p, stack);
    }
    public static void drop(ServerPlayer p, ItemStack stack) {
        var entity = new net.minecraft.world.entity.item.ItemEntity(p.level(), p.getX(), p.getY() + .5, p.getZ(), stack);
        entity.setDefaultPickUpDelay(); p.level().addFreshEntity(entity);
    }
    public static String itemName(String id) { return id.substring(id.indexOf(':') + 1).replace('_', ' '); }
    private static void celebrate(Villager v, FriendshipState old, FriendshipState next) {
        if (next.points() <= old.points()) return;
        ((ServerLevel)v.level()).sendParticles(ParticleTypes.HEART, v.getX(), v.getY() + 1.5, v.getZ(), 3, .3, .2, .3, .01);
        v.playSound(SoundEvents.VILLAGER_YES, .6F, 1.15F);
    }
    public static String profession(Villager v) { return v.getVillagerData().profession().unwrapKey().map(k -> k.identifier().getPath()).orElse("none"); }
    public static String name(Villager v) { return v.hasCustomName() ? v.getCustomName().getString() : Dialogue.name(v.getUUID(),profile(v).look()); }
    public static long day(net.minecraft.world.level.Level level) { return Math.floorDiv(level.getOverworldClockTime(), 24000L); }
    public static void show(ServerPlayer p, Villager v, String tab, String dialogue, String status, boolean opening) {
        if (p.connection == null || !ServerPlayNetworking.canSend(p, FriendshipPayload.TYPE)) return;
        var affinity = state(v, p); var b = bond(v, p); var profile = profile(v); String job = profession(v);
        String label = v.isBaby() ? "Young Villager" : job.equals("none") ? "Neighbor" : job.equals("nitwit") ? "Free Spirit" : VillageProfessions.label(job);
        String personality = NarrativeContent.current().personality(profile.personality()).label();
        String journal = NarrativeEngine.journal(v, p);
        ServerPlayNetworking.send(p, new FriendshipPayload(v.getId(), v.getUUID(), name(v), label, personality,
                affinity.points(), b.level(affinity), affinity.nextThreshold(), affinity.giftsLeft(day(v.level())), affinity.canTalk(day(v.level())),
                !v.isBaby() && !job.equals("none") && !job.equals("nitwit"), dialogue, status,
                "Hobby: " + profile.hobby() + ". Loves " + itemName(profile.love()) + "; dislikes " + itemName(profile.dislike()) + ". " + GiftPreferences.hint(job, v.isBaby()),
                opening, tab, journal, NarrativeEngine.choices(v, p, tab), b.trustLabel()));
    }
}
