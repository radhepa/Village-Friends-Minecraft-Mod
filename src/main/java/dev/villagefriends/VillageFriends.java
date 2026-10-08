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
    /** The resident's personality id, shared with clients so body language matches who they are. */
    public static final AttachmentType<String> TEMPERAMENT = AttachmentRegistry.create(id("temperament"),
            b -> b.syncWith(ByteBufCodecs.STRING_UTF8, AttachmentSyncPredicate.all()));
    public static final AttachmentType<BondBook> BONDS = AttachmentRegistry.create(id("bonds"), b -> b.initializer(BondBook::empty).persistent(BondBook.CODEC));
    public static final AttachmentType<SharedHistory> SHARED = AttachmentRegistry.create(id("shared_history"), b -> b.initializer(() -> SharedHistory.EMPTY).persistent(SharedHistory.CODEC));
    public static final AttachmentType<CompanionState> COMPANION = AttachmentRegistry.create(id("companion"), b -> b.initializer(() -> CompanionState.NONE).persistent(CompanionState.CODEC));
    public static final AttachmentType<String> PARTY = AttachmentRegistry.create(id("party"), b -> b.initializer(() -> "").persistent(Codec.STRING));
    public static final AttachmentType<VillageBook> VILLAGES = AttachmentRegistry.create(id("villages"), b -> b.initializer(() -> VillageBook.EMPTY).persistent(VillageBook.CODEC));
    public static final AttachmentType<ResidentHome> HOME = AttachmentRegistry.create(id("home_village"), b -> b.persistent(ResidentHome.CODEC));
    public static final AttachmentType<String> HOME_LABEL = AttachmentRegistry.create(id("home_label"), b -> b.persistent(Codec.STRING));
    public static final AttachmentType<Boolean> GUARD_EQUIPPED = AttachmentRegistry.create(id("guard_equipped"), b -> b.persistent(Codec.BOOL));
    public static final AttachmentType<String> GUARD_ARROW_TARGET = AttachmentRegistry.create(id("guard_arrow_target"), b -> b.persistent(Codec.STRING));
    public static final AttachmentType<GuardProgress> GUARD_PROGRESS = AttachmentRegistry.create(id("guard_progress"), b -> b.persistent(GuardProgress.CODEC));
    public static final AttachmentType<Boolean> GUARD_OBSERVED = AttachmentRegistry.create(id("guard_observed"), b -> b.persistent(Codec.BOOL));
    public static final AttachmentType<Integer> GUARD_ARROW_LEVEL = AttachmentRegistry.create(id("guard_arrow_level"), b -> b.persistent(Codec.INT));
    /** Every village's residents, families and relationships, kept on the level that records the village. */
    public static final AttachmentType<dev.villagefriends.social.SocietyBook> SOCIETIES = AttachmentRegistry.create(id("societies"),
            b -> b.initializer(() -> dev.villagefriends.social.SocietyBook.EMPTY).persistent(dev.villagefriends.social.SocietyBook.CODEC));
    /** "parentId|parentId" for a baby until it joins its village. */
    public static final AttachmentType<String> PARENTS = AttachmentRegistry.create(id("parents"), b -> b.persistent(Codec.STRING));
    /** A player's last known friendship level with each resident they have talked to, for the Village Ledger. */
    public static final AttachmentType<java.util.Map<String, Integer>> ACQUAINTANCES = AttachmentRegistry.create(id("acquaintances"),
            b -> b.initializer(java.util.Map::<String, Integer>of).persistent(Codec.unboundedMap(Codec.STRING, Codec.INT)).copyOnDeath());
    /** What a resident is doing in their day ("work", "lunch", "shelter"...), shared with clients for body language. */
    public static final AttachmentType<String> ROUTINE = AttachmentRegistry.create(id("routine"),
            b -> b.syncWith(ByteBufCodecs.STRING_UTF8, AttachmentSyncPredicate.all()));
    /** A knocked-out resident's clock: revive them before {@code until} (game time) or they die. Absent while conscious. */
    public static final AttachmentType<KnockoutState> KNOCKOUT = AttachmentRegistry.create(id("knockout"), b -> b.persistent(KnockoutState.CODEC));
    /** Lying hurt on the ground (knocked out, or a downed companion): shared with clients for the pose and hitbox. */
    public static final AttachmentType<Boolean> INJURED = AttachmentRegistry.create(id("injured"),
            b -> b.syncWith(ByteBufCodecs.BOOL, AttachmentSyncPredicate.all()));
    private static final Set<String> TOPICS = Set.of("chat", "work", "adventure", "joke", "news", "heart");
    public static AttachmentTarget target(Entity entity) { return (AttachmentTarget) entity; }

    @Override public void onInitialize() {
        VillageMarkerBlock.register();
        VillageStructure.register();
        VillageFoundation.register();
        dev.villagefriends.tavern.Taverns.register();
        dev.villagefriends.play.Playground.register();
        NarrativeContent.register();
        dev.villagefriends.talk.DialogueBank.register();
        ResidentNames.register();
        Birthdays.register();
        VillageQuests.register();
        dev.villagefriends.pet.VillagerPets.register();
        net.fabricmc.fabric.api.object.builder.v1.entity.FabricDefaultAttributeRegistry.register(net.minecraft.world.entity.EntityTypes.VILLAGER,
                Villager.createAttributes().add(net.minecraft.world.entity.ai.attributes.Attributes.ATTACK_DAMAGE, 1).add(net.minecraft.world.entity.ai.attributes.Attributes.ATTACK_KNOCKBACK, 0));
        ServerEntityEvents.ENTITY_LOAD.register((entity, level) -> dev.villagefriends.pet.VillagerPets.loaded(entity));
        ServerEntityEvents.ENTITY_LOAD.register((entity, level) -> {
            if (entity instanceof Villager villager) { GuardProgression.loaded(villager); ensureIdentity(villager); CompanionController.loaded.add(villager); VillageSettlements.identify(villager,false); GuardController.initializeEquipment(villager); if (Knockouts.knockedOut(villager)) Knockouts.lieDown(villager); }
        });
        ServerEntityEvents.ENTITY_UNLOAD.register((entity, level) -> { GuardProgression.unload(entity); dev.villagefriends.pet.VillagerPets.unloaded(entity); if (entity instanceof Villager v) { CompanionController.unload(v); GuardController.unload(v); ResidentRoutines.unload(v); Knockouts.unload(v); GuardPatrols.unload(v); } });
        ServerPlayConnectionEvents.JOIN.register((handler, sender, server) -> CompanionController.resetParty(handler.getPlayer()));
        ServerPlayConnectionEvents.DISCONNECT.register((handler, server) -> CompanionController.resetParty(handler.getPlayer()));
        ServerLifecycleEvents.SERVER_STOPPED.register(server -> { CompanionController.clear(); VillageSettlements.clear(); GuardController.clear(); GuardProgression.clear(); VillageSocieties.clear(); VillageLedger.clear(); ResidentRoutines.clear(); Workstations.clear(); Knockouts.clear(); GuardPatrols.clear(); Birthdays.clear(); VillageQuests.clear(); dev.villagefriends.pet.VillagerPets.clear(); });
        ServerTickEvents.END_SERVER_TICK.register(CompanionController::tick);
        ServerTickEvents.END_SERVER_TICK.register(VillageSettlements::tick);
        ServerTickEvents.END_SERVER_TICK.register(GuardController::tick);
        ServerTickEvents.END_SERVER_TICK.register(VillageSocieties::tick);
        ServerTickEvents.END_SERVER_TICK.register(ResidentRoutines::tick);
        ServerTickEvents.END_SERVER_TICK.register(GuardPatrols::tick);
        ServerTickEvents.END_SERVER_TICK.register(Workstations::tick);
        ServerTickEvents.END_SERVER_TICK.register(dev.villagefriends.pet.VillagerPets::tick);
        // Striking the training dummy measures the hit instead of breaking it.
        net.fabricmc.fabric.api.event.player.AttackBlockCallback.EVENT.register(Workstations::attack);
        ServerLivingEntityEvents.MOB_CONVERSION.register((before, after, params) -> transferIdentity(before, after));
        ServerLivingEntityEvents.ALLOW_DAMAGE.register(GuardController::allowDamage);
        ServerLivingEntityEvents.AFTER_DAMAGE.register(GuardController::afterDamage);
        ServerLivingEntityEvents.ALLOW_DEATH.register(GuardController::allowDeath);
        ServerLivingEntityEvents.AFTER_DEATH.register(GuardController::afterDeath);
        ServerLivingEntityEvents.AFTER_DEATH.register((entity, source) -> { if (entity instanceof Villager v) VillageSocieties.died(v); });
        ServerLivingEntityEvents.AFTER_DEATH.register((entity, source) -> dev.villagefriends.pet.VillagerPets.died(entity));
        PayloadTypeRegistry.clientboundPlay().register(FriendshipPayload.TYPE, FriendshipPayload.CODEC);
        PayloadTypeRegistry.clientboundPlay().register(EmotePayload.TYPE, EmotePayload.CODEC);
        PayloadTypeRegistry.clientboundPlay().register(LedgerPayload.TYPE, LedgerPayload.CODEC);
        PayloadTypeRegistry.clientboundPlay().register(VillageArrivalPayload.TYPE, VillageArrivalPayload.CODEC);
        PayloadTypeRegistry.serverboundPlay().register(ActionPayload.TYPE, ActionPayload.CODEC);
        PayloadTypeRegistry.serverboundPlay().register(LedgerRequestPayload.TYPE, LedgerRequestPayload.CODEC);
        PayloadTypeRegistry.clientboundPlay().register(dev.villagefriends.pet.PetPayload.TYPE, dev.villagefriends.pet.PetPayload.CODEC);
        PayloadTypeRegistry.serverboundPlay().register(dev.villagefriends.pet.PetActionPayload.TYPE, dev.villagefriends.pet.PetActionPayload.CODEC);
        ServerPlayNetworking.registerGlobalReceiver(dev.villagefriends.pet.PetActionPayload.TYPE, (payload, context) -> dev.villagefriends.pet.VillagerPets.handleAction(context.player(), payload));
        ServerPlayNetworking.registerGlobalReceiver(ActionPayload.TYPE, (payload, context) -> handleAction(context.player(), payload));
        ServerPlayNetworking.registerGlobalReceiver(LedgerRequestPayload.TYPE, (payload, context) -> VillageLedger.request(context.player(), payload));
        // A resident's cat or dog opens their pet card.
        UseEntityCallback.EVENT.register((player, world, hand, entity, hit) -> dev.villagefriends.pet.VillagerPets.interact(player, world, hand, entity));
        UseEntityCallback.EVENT.register((player, world, hand, entity, hit) -> {
            if (!(entity instanceof Villager villager) || hand != InteractionHand.MAIN_HAND || player.isSpectator()) return InteractionResult.PASS;
            var held = player.getMainHandItem();
            // Someone knocked out can be treated or checked on, but not traded with or talked to.
            if (Knockouts.injured(villager) && !CompanionController.state(villager).downed()) {
                if (held.is(Items.NAME_TAG)) return InteractionResult.PASS;
                if (world.isClientSide()) return InteractionResult.SUCCESS;
                if (player instanceof ServerPlayer sp && Knockouts.knockedOut(villager)) Knockouts.interact(sp, villager);
                return InteractionResult.SUCCESS_SERVER;
            }
            if (player.isShiftKeyDown()) return InteractionResult.PASS;
            if (held.is(Items.NAME_TAG) || held.getItem() instanceof SpawnEggItem) return InteractionResult.PASS;
            if (world.isClientSide() || !(player instanceof ServerPlayer sp) || !ServerPlayNetworking.canSend(sp, FriendshipPayload.TYPE) || !validTarget(sp, villager)) return InteractionResult.PASS;
            if (villager.isSleeping()) { sp.sendSystemMessage(Component.literal("Your neighbor is sleeping. Visit again in the morning!"), true); return InteractionResult.SUCCESS_SERVER; }
            ensureIdentity(villager);
            VillageSettlements.identify(villager,true);
            saveBond(villager, sp, bond(villager, sp).visit(day(world)));
            villager.getLookControl().setLookAt(player, 30, 30);
            show(sp, villager, "talk", NarrativeEngine.greeting(villager, sp), ResidentRoutines.doing(villager) + " · " + dev.villagefriends.routine.Routine.clock(ResidentRoutines.timeOfDay(world))
                    + (dev.villagefriends.routine.Routine.marketDay(day(world)) ? " · Market Day" : "") + Birthdays.status(villager), true);
            return InteractionResult.SUCCESS_SERVER;
        });
        // A notice board shows its village's notices, birthdays and a way into the ledger.
        net.fabricmc.fabric.api.event.player.UseBlockCallback.EVENT.register((player, world, hand, hit) -> {
            if (hand != InteractionHand.MAIN_HAND || player.isShiftKeyDown() || player.isSpectator()
                    || !world.getBlockState(hit.getBlockPos()).is(VillageBlocks.get("notice_board"))) return InteractionResult.PASS;
            if (player instanceof ServerPlayer sp) VillageQuests.open(sp, hit.getBlockPos());
            return InteractionResult.SUCCESS;
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
        else if (!t.hasAttached(HOME)) {
            // Names generated before 2.18.0 could ignore gender; settled residents are fixed in identify().
            String fixed = ResidentNames.corrected(v.getUUID(), look, v.getCustomName().getString());
            if (fixed != null) v.setCustomName(Component.literal(fixed));
        }
        v.setCustomNameVisible(true);
        if (!look.equals(t.getAttached(LOOK))) t.setAttached(LOOK, look);
        if (!profile.personality().equals(t.getAttached(TEMPERAMENT))) t.setAttached(TEMPERAMENT, profile.personality());
    }
    private static <T> void copy(Entity before, Entity after, AttachmentType<T> type) {
        T data = target(before).getAttached(type); if (data != null) target(after).setAttached(type, data);
    }
    public static void transferIdentity(Entity before, Entity after) {
        if (!target(before).hasAttached(PROFILE)) return;
        if (before instanceof Villager v) { CompanionController.unload(v); GuardController.unload(v); }
        copy(before, after, PROFILE); copy(before, after, LOOK);
        copy(before, after, FRIENDSHIPS); copy(before, after, BONDS); copy(before, after, SHARED);
        copy(before, after, HOME); copy(before, after, HOME_LABEL);
        copy(before, after, GUARD_EQUIPPED);
        copy(before, after, GUARD_PROGRESS); copy(before, after, GUARD_OBSERVED); copy(before, after, dev.villagefriends.pet.VillagerPets.LINK);
        GuardProgression.converted(after);
        VillageSocieties.converted(before, after);
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
            int friendLevel = FriendshipLevels.level(state(v, player), bond(v, player));
            if (a.equals("news") && friendLevel < FriendshipLevels.NEWS || a.equals("heart") && friendLevel < FriendshipLevels.HEART_TO_HEART) {
                show(player, v, "talk", NarrativeEngine.greeting(v, player), "Get to know each other a little better first.", false); return;
            }
            var old = state(v, player); long today = day(v.level()); var next = old.talk(today); save(v, player, next);
            saveBond(v, player, bond(v, player).visit(today));
            // Sometimes "How's your day?" turns into a question for you, or an offer to help.
            var question = a.equals("chat") && !bond(v, player).has("hurt") ? TalkWorld.ask(v, player) : null;
            String reply = question != null ? TalkWorld.askText(v, player, question) : NarrativeEngine.conversation(v, player, a);
            celebrate(v, old, next);
            String status = old.canTalk(today) ? "+4 friendship - thanks for visiting!" : "Happy to keep talking. Friendship rewards return tomorrow.";
            if (old.canTalk(today) && friendLevel >= FriendshipLevels.DAILY_GIFT && !v.isBaby()) {
                var gift = dailyGift(profile(v).personality());
                giveItem(player, gift, 2);
                status = "+4 friendship. They slipped you " + itemName(gift) + ", just because.";
            }
            if (question != null) { show(player, v, "question", reply, question.offer() ? status : "They're asking you. " + status, false, question.offer() ? Emote.IDEA : Emote.QUESTION); return; }
            show(player, v, "talk", reply, status, false, NarrativeEngine.mood(v, player, a)); return;
        }
        if (a.equals("ledger")) { VillageLedger.open(player, v); return; }
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
            show(p, v, "talk", reply, "Gift declined. Your item and gift allowance were kept.", false, stack.isEmpty() ? Emote.QUESTION : Emote.SWEAT); return;
        }
        int value = item.equals(profile.love()) ? 14 : GiftPreferences.value(profession(v), v.isBaby(), item);
        // Birthdays: presents count double, and cake or a birthday card are everyone's favorite.
        var birthday = Birthdays.gift(v, p, item, value, item.equals(profile.love()));
        if (birthday != null) value = birthday.value();
        if (value == 0) { show(p, v, "talk", "That's thoughtful, but perhaps a flower, treat, or something for my hobby?", "Your item was kept.", false, Emote.QUESTION); return; }
        var next = old.gift(today, item, value); if (!p.getAbilities().instabuild) stack.shrink(1); save(v, p, next);
        saveBond(v, p, bond(v, p).trust(item.equals(profile.love()) || birthday != null ? 2 : 1).remember(today, birthday != null ? birthday.memory() : "You gave me " + itemName(item) + "."));
        celebrate(v, old, next);
        if (birthday != null) { show(p, v, "talk", birthday.reply(), "+" + (next.points() - old.points()) + " friendship. " + birthday.status(), false, birthday.mood()); return; }
        show(p, v, "talk", item.equals(profile.love()) ? "You remembered! " + itemName(item) + " is one of my favorites. Thank you for paying attention."
                : "What a lovely surprise. Thank you for thinking of me!", "+" + (next.points() - old.points()) + " friendship. Gifts help; shared experiences deepen our bond.", false,
                item.equals(profile.love()) ? Emote.HEART : Emote.NOTE);
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
        show(p, v, tab, dialogue, status, opening, opening ? NarrativeEngine.greetingMood(v, p) : null);
    }
    public static void show(ServerPlayer p, Villager v, String tab, String dialogue, String status, boolean opening, Emote emote) {
        if (p.connection == null || !ServerPlayNetworking.canSend(p, FriendshipPayload.TYPE)) return;
        var affinity = state(v, p); var b = bond(v, p); var profile = profile(v); String job = profession(v);
        String label = v.isBaby() ? "Young Villager" : job.equals("none") ? "Neighbor" : job.equals("nitwit") ? "Free Spirit" : VillageProfessions.label(job);
        if (GuardController.isGuard(v) && GuardProgression.progress(v) != null) label += " · Level " + GuardProgression.progress(v).level();
        String personality = NarrativeContent.current().personality(profile.personality()).label();
        String journal = GuardProgression.journal(v) + NarrativeEngine.journal(v, p);
        // Friendship levels: remember the last level this player saw, so a rise is celebrated once.
        int friendLevel = FriendshipLevels.level(affinity, b);
        int seen = b.flags().stream().filter(f -> f.startsWith("seen_level:")).mapToInt(f -> Integer.parseInt(f.substring(11))).findFirst().orElse(-1);
        boolean levelUp = seen >= 0 && friendLevel > seen;
        if (seen != friendLevel) { b = b.unflag("seen_level:" + seen).flag("seen_level:" + friendLevel); saveBond(v, p, b); }
        if (levelUp) { status = "Friendship Lv. " + friendLevel + "! " + FriendshipLevels.perk(friendLevel); emote = Emote.SPARKLE; }
        var known = target(p).getAttachedOrCreate(ACQUAINTANCES);
        if (known.getOrDefault(profile.id(), -1) != friendLevel) {
            var next = new java.util.HashMap<>(known); next.put(profile.id(), friendLevel); target(p).setAttached(ACQUAINTANCES, java.util.Map.copyOf(next));
        }
        var town = VillageSettlements.home(v); var society = VillageSocieties.of(v);
        String family = society == null || !society.has(profile.id()) ? "" : String.join(" · ", dev.villagefriends.social.Gossip.about(society, profile.id(), day(v.level())).stream().limit(2).toList());
        String pet = dev.villagefriends.pet.VillagerPets.petLine(v);
        if (!pet.isEmpty()) family = family.isEmpty() ? pet : family + " · " + pet;
        if (emote != null) VillageSocieties.emote(v, emote, 0);
        ServerPlayNetworking.send(p, new FriendshipPayload(v.getId(), v.getUUID(), name(v), label, personality,
                affinity.points(), b.level(affinity), FriendshipLevels.threshold(Math.min(FriendshipLevels.MAX, friendLevel + 1)), affinity.giftsLeft(day(v.level())), affinity.canTalk(day(v.level())),
                !v.isBaby() && !job.equals("none") && !job.equals("nitwit"), dialogue, status,
                "Hobby: " + profile.hobby() + ". Loves " + itemName(profile.love()) + "; dislikes " + itemName(profile.dislike()) + ". " + GiftPreferences.hint(job, v.isBaby()),
                opening, tab, journal, NarrativeEngine.choices(v, p, tab), b.trustLabel(),
                friendLevel, FriendshipLevels.name(friendLevel), FriendshipLevels.threshold(friendLevel), FriendshipLevels.goal(affinity, b), levelUp,
                emote == null ? "" : emote.name(), town == null ? "" : town.name(), family));
    }
    /** A small present a Kindred Spirit saves for you, matching their hobby. */
    static String dailyGift(String personality) {
        return switch (personality) {
            case "warmhearted" -> "minecraft:cookie";
            case "thoughtful" -> "minecraft:paper";
            case "playful" -> "minecraft:sweet_berries";
            case "adventurous" -> "minecraft:apple";
            case "meticulous" -> "minecraft:honeycomb";
            case "steadfast" -> "minecraft:bone_meal";
            case "reserved" -> "minecraft:cooked_cod";
            case "imaginative" -> "minecraft:pink_dye";
            case "pragmatic" -> "minecraft:candle";
            case "curious" -> "minecraft:glowstone_dust";
            case "protective" -> "minecraft:bread";
            default -> "minecraft:allium";
        };
    }
}
