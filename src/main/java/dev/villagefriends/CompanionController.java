package dev.villagefriends;

import java.util.*;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.Identifier;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.Pose;
import net.minecraft.world.entity.monster.Enemy;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.core.component.DataComponents;
import net.minecraft.world.level.Level;
import static dev.villagefriends.VillageFriends.*;

/** Only loaded residents run social checks. Work AI is suspended only while an owned outing is active. */
public final class CompanionController {
    public static final Set<Villager> loaded = new HashSet<>();
    private static final Map<UUID, Integer> strikes = new HashMap<>();
    private static final Map<UUID, Outing> outings = new HashMap<>();
    private static final Map<UUID, Long> invitations = new HashMap<>();
    public record Outing(String type, long start, double x, double y, double z) {}
    public static boolean hasActivity(Villager v) {
        var s = state(v);
        return outings.containsKey(v.getUUID()) || s.active() && !s.mode().equals("follow") && !s.mode().equals("wait");
    }
    public static void clear() { loaded.clear(); strikes.clear(); outings.clear(); invitations.clear(); }
    public static void unload(Villager v) {
        loaded.remove(v); strikes.remove(v.getUUID());
        if (v.getRemovalReason() != null && v.getRemovalReason().shouldDestroy()) {
            var s = state(v);
            if (s.active()) {
                var p = ((ServerLevel)v.level()).getServer().getPlayerList().getPlayer(UUID.fromString(s.owner()));
                if (p != null && target(p).getAttachedOrElse(PARTY, "").equals(profile(v).id())) target(p).setAttached(PARTY, "");
            }
            outings.remove(v.getUUID());
        }
    }
    public static void resetParty(ServerPlayer p) {
        for (var v : List.copyOf(loaded)) if (state(v).owner().equals(p.getUUID().toString())) returnHome(v, p, true);
        target(p).setAttached(PARTY, "");
    }
    public static CompanionState state(Villager v) { return target(v).getAttachedOrCreate(COMPANION); }
    private static void state(Villager v, CompanionState s) { target(v).setAttached(COMPANION, s); }
    private static FriendshipPayload.Choice c(String id, String label, boolean enabled) { return new FriendshipPayload.Choice(id, label, enabled); }
    private static boolean eligible(Villager v, ServerPlayer p) { return !v.isBaby() && !v.isTrading() && v.level().dimension().equals(Level.OVERWORLD) && bond(v, p).level(VillageFriends.state(v, p)) >= 2 && bond(v, p).chapter() >= 2 && bond(v, p).trust() >= 50; }
    public static List<FriendshipPayload.Choice> choices(Villager v, ServerPlayer p) {
        var s = state(v); boolean owns = s.owner().equals(p.getUUID().toString());
        if (s.downed()) return List.of(c("rescue", "Help them up", true), c("home", "Take them home", owns));
        if (!s.active()) {
            if (GuardController.isGuard(v)) return List.of(c("recruit", "Travel with me", eligible(v, p)), c("equip", "Equip held item", GuardController.canExchange(v, p)), c("talk_tab", "Let's stay here", true));
            return List.of(c("recruit", "Travel with me", eligible(v, p)), c("talk_tab", "Let's stay here", true));
        }
        return List.of(c("follow", "Follow me", owns), c("wait", "Wait here", owns), c("home", "Return home", owns), c("equip", "Equip held item", GuardController.isGuard(v) ? GuardController.canExchange(v,p) : owns));
    }
    public static List<FriendshipPayload.Choice> activityChoices(Villager v, ServerPlayer p) {
        if (outings.containsKey(v.getUUID())) return List.of(c("finish_activity", "Finish our outing", state(v).owner().equals(p.getUUID().toString())), c("home", "End outing and go home", state(v).owner().equals(p.getUUID().toString())));
        boolean available = !v.isBaby() && !state(v).active() && VillageFriends.state(v, p).points() >= 15 && bond(v, p).trust() >= 30 && v.level().dimension().equals(Level.OVERWORLD);
        return List.of(c("walk", "Take a walk", available), c("picnic", "Share a picnic", available), c("explore", "Explore together", available), c("gathering", "Invite the neighbors", available));
    }
    public static boolean handle(ServerPlayer p, Villager v, String action) {
        var s = state(v); boolean owns = s.owner().equals(p.getUUID().toString());
        switch (action) {
            case "companion" -> show(p, v, "companion", s.downed() ? "I need a hand getting up." : s.active() ? "I'm " + s.mode() + " here with my traveling companion. Hold equipment in your main hand if you'd like me to use it."
                    : eligible(v, p) ? "I'd like to see the world with you. We'll watch out for each other." : "Let's get to know each other first. Become friends, help with my story, and build comfortable trust. Adult residents can travel in the Overworld.", "One companion per player.", false);
            case "together" -> show(p, v, "together", "We could take a walk, share a picnic, or explore somewhere new. Bring bread, an apple, or a cookie for a picnic. For a gathering, invite nearby neighbors with bread.", "Close the window to move, then talk again to finish.", false);
            case "recruit" -> {
                if (!eligible(v, p) || s.active() || !claimable(v, p)) return false;
                begin(v, p, "follow");
                saveBond(v, p, bond(v, p).remember(day(v.level()), "We decided to watch out for each other on an adventure."));
                show(p, v, "companion", "I'm ready. Lead the way, and tell me if you'd like to stop or go home.", "Follow / Wait / Return home. Equip held swords or armor.", false);
            }
            case "follow", "wait" -> {
                if (!owns || s.downed()) return false;
                state(v, s.mode(action)); v.getNavigation().stop();
                show(p, v, "companion", action.equals("follow") ? "I'll stay close. Let's take care of each other." : "I'll wait here. You can come back for me or ask me to go home.", action.equals("follow") ? "Following you." : "Waiting here.", false);
            }
            case "home" -> {
                if (!owns) return false;
                returnHome(v, p, true);
                // The actor may now be outside conversation range; avoid leaving the UI waiting.
                p.sendSystemMessage(net.minecraft.network.chat.Component.literal(name(v) + " returned home safely."), true);
            }
            case "rescue" -> {
                if (!s.downed()) return false;
                v.setHealth(Math.max(8, v.getMaxHealth() / 2)); Knockouts.getUp(v); v.clearFire();
                state(v, new CompanionState(s.owner(), "follow", s.x(), s.y(), s.z(), 0, s.originalNoAi(), s.started()));
                var b = bond(v, p);
                if (!b.has("rescue:" + day(v.level()))) {
                    for (String flag : b.flags()) if (flag.startsWith("rescue:")) b = b.unflag(flag);
                    saveBond(v, p, b.trust(5).flag("rescue:" + day(v.level())).remember(day(v.level()), "You helped me up when I couldn't carry on."));
                }
                show(p, v, "companion", "Thank you for staying with me. Let's be careful, or head home if things are too dangerous.", "Recovered. Equipment and memories kept.", false);
            }
            case "equip" -> {
                if (GuardController.isGuard(v)) return GuardController.exchange(p, v);
                if (!owns || s.downed() || outings.containsKey(v.getUUID())) return false;
                var held = p.getMainHandItem();
                if (held.isEmpty()) { show(p, v, "companion", "Hold a sword, axe, or armor piece if you'd like me to use it.", "Equipment is separate from gifts.", false); break; }
                var equippable = held.get(DataComponents.EQUIPPABLE);
                EquipmentSlot slot;
                if (equippable != null && equippable.slot() != EquipmentSlot.BODY && equippable.slot() != EquipmentSlot.SADDLE) slot = equippable.slot();
                else if (held.is(net.minecraft.tags.ItemTags.SWORDS) || held.is(net.minecraft.tags.ItemTags.AXES)) slot = EquipmentSlot.MAINHAND;
                else { show(p, v, "companion", "I can use swords, axes, and ordinary armor. Keep the other supplies for yourself.", "Your item was kept.", false); break; }
                var previous = v.getItemBySlot(slot).copy();
                var replacement = held.copyWithCount(1); held.shrink(1); // Even Creative swaps one physical item: no equipment duplication.
                v.setItemSlot(slot, replacement); v.setDropChance(slot, 1);
                if (!previous.isEmpty() && !p.getInventory().add(previous)) drop(p, previous);
                show(p, v, "companion", "Thank you. I'll take care of it. I've given your previous equipment back.", "Equipped " + replacement.getHoverName().getString() + ".", false);
            }
            case "walk", "picnic", "explore", "gathering" -> {
                if (v.isBaby() || s.active() || !claimable(v, p) || VillageFriends.state(v, p).points() < 15 || bond(v, p).trust() < 30 || !v.level().dimension().equals(Level.OVERWORLD)) return false;
                if (action.equals("picnic") || action.equals("gathering")) {
                    var held = p.getMainHandItem();
                    if (!(held.is(Items.BREAD) || held.is(Items.APPLE) || held.is(Items.COOKIE))) {
                        show(p, v, "together", "Bring bread, an apple, or a cookie so we can share something.", "Hold picnic food in your main hand.", false); break;
                    }
                    if (action.equals("gathering") && loaded.stream().filter(n -> n != v && n.level() == v.level() && n.distanceToSqr(v) < 144 && !n.isBaby() && !state(n).active()).count() < 2) {
                        show(p, v, "together", "Let's invite the neighbors when at least two of them are nearby.", "Gatherings need three adult residents nearby.", false); break;
                    }
                    if (!p.getAbilities().instabuild) held.shrink(1);
                }
                begin(v, p, action);
                outings.put(v.getUUID(), new Outing(action, v.level().getGameTime(), p.getX(), p.getY(), p.getZ()));
                if (action.equals("gathering")) {
                    int invited = 0;
                    for (var neighbor : List.copyOf(loaded)) {
                        if (invited >= 6) break;
                        if (neighbor != v && neighbor.level() == v.level() && neighbor.distanceToSqr(v) < 144 && !neighbor.isBaby() && !state(neighbor).active()) {
                            begin(neighbor, p, "gathering_guest"); invited++;
                        }
                    }
                }
                show(p, v, "together", switch (action) {
                    case "walk" -> "Let's walk together for at least fifteen seconds and go eight blocks from here. Talk to me afterward to finish.";
                    case "explore" -> "Let's explore together for at least thirty seconds and go thirty-two blocks from here. Stay close, then talk to me to finish.";
                    case "gathering" -> "The neighbors are coming over. Let's enjoy their company for twenty seconds, then finish our gathering.";
                    default -> "Let's enjoy our picnic together for fifteen seconds. Stay nearby, then talk to me to finish.";
                }, "Close this window to move around.", false);
            }
            case "finish_activity" -> {
                var outing = outings.get(v.getUUID());
                if (!owns || outing == null || s.downed()) return false;
                double traveled = p.distanceToSqr(outing.x(), outing.y(), outing.z());
                long needed = outing.type.equals("explore") ? 600 : outing.type.equals("gathering") ? 400 : 300;
                double distance = outing.type.equals("explore") ? 1024 : outing.type.equals("walk") ? 64 : 0;
                if (v.level().getGameTime() - outing.start < needed || traveled < distance) {
                    show(p, v, "together", "I'd like a little more time together before we call this finished. Walks need eight blocks; exploration needs thirty-two. Picnics and gatherings just need a little time.", "Keep spending time together, then try again.", false); break;
                }
                finish(v, p, outing.type);
                if (outing.type.equals("gathering")) {
                    for (var guest : List.copyOf(loaded)) if (state(guest).owner().equals(p.getUUID().toString()) && state(guest).mode().equals("gathering_guest")) {
                        finish(guest, p, "gathering"); releaseHere(guest, p);
                    }
                }
                releaseHere(v, p);
                show(p, v, "talk", "I enjoyed that. Thank you for making time for me. I'll remember this when we talk again.", "A shared experience, remembered in your journal.", false);
            }
            default -> { return false; }
        }
        return true;
    }
    private static boolean claimable(Villager v, ServerPlayer p) {
        String party = target(p).getAttachedOrElse(VillageFriends.PARTY, "");
        return party.isEmpty() || party.equals(profile(v).id());
    }
    private static void begin(Villager v, ServerPlayer p, String mode) {
        state(v, new CompanionState(p.getUUID().toString(), mode, v.getX(), v.getY(), v.getZ(), 0, v.isNoAi(), v.level().getGameTime()));
        if (!mode.equals("gathering_guest")) target(p).setAttached(VillageFriends.PARTY, profile(v).id());
        v.setNoAi(false); v.stopSleeping(); v.setTradingPlayer(null);
        if (mode.equals("follow")) saveBond(v, p, bond(v, p).unflag("outing:defense"));
    }
    private static void finish(Villager v, ServerPlayer p, String kind) {
        var b = bond(v, p); long today = day(v.level());
        boolean reward = b.activityDay() != today;
        saveBond(v, p, b.activity(today, kind));
        if (reward) reward(v, p, 8);
    }
    private static void releaseHere(Villager v, ServerPlayer p) {
        GuardController.unload(v);
        var s = state(v); outings.remove(v.getUUID()); v.getNavigation().stop(); v.setNoAi(s.originalNoAi()); state(v, CompanionState.NONE);
        if (target(p).getAttachedOrElse(VillageFriends.PARTY, "").equals(profile(v).id())) target(p).setAttached(VillageFriends.PARTY, "");
    }
    public static void returnHome(Villager v, ServerPlayer p, boolean record) {
        GuardController.unload(v);
        var s = state(v); if (!s.active()) return;
        if (s.downed()) {
            var owner = UUID.fromString(s.owner()); var book = target(v).getAttachedOrCreate(BONDS);
            target(v).setAttached(BONDS, book.with(owner, book.get(owner).remember(day(v.level()), "I recovered at home after our outing ended while I was downed.")));
        }
        var level = (ServerLevel)v.level();
        BlockPos home = BlockPos.containing(s.x(), s.y(), s.z()); level.getChunkAt(home);
        boolean placed = false;
        for (int dy = 0; dy <= 4 && !placed; dy++) for (int dx = -2; dx <= 2 && !placed; dx++) for (int dz = -2; dz <= 2 && !placed; dz++) {
            var pos = home.offset(dx, dy, dz);
            if (level.getBlockState(pos).getCollisionShape(level, pos).isEmpty() && level.getBlockState(pos.above()).getCollisionShape(level, pos.above()).isEmpty()
                    && !level.getBlockState(pos.below()).getCollisionShape(level, pos.below()).isEmpty() && level.getFluidState(pos).isEmpty()) {
                v.teleportTo(pos.getX() + .5, pos.getY(), pos.getZ() + .5); placed = true;
            }
        }
        if (!placed) v.teleportTo(s.x(), s.y(), s.z());
        v.setHealth(Math.max(v.getHealth(), v.getMaxHealth() / 2)); v.clearFire(); Knockouts.getUp(v);
        if (p != null && record && !outings.containsKey(v.getUUID())) {
            var b = bond(v, p); saveBond(v, p, b.flag("adventure_return").remember(day(v.level()), "We returned safely from an adventure together."));
        }
        if (p != null) releaseHere(v, p);
        else { outings.remove(v.getUUID()); v.getNavigation().stop(); v.setNoAi(s.originalNoAi()); state(v, CompanionState.NONE); }
    }
    public static boolean allowDamage(LivingEntity entity, DamageSource source, float amount) {
        if (!(entity instanceof Villager v)) return true;
        if (state(v).downed()) return false;
        if (source.getEntity() instanceof ServerPlayer p && strikes.getOrDefault(v.getUUID(), -100) + 20 <= v.tickCount) {
            strikes.put(v.getUUID(), v.tickCount);
            saveBond(v, p, bond(v, p).trust(-15).flag("hurt").remember(day(v.level()), "You hurt me. I need to feel safe again."));
        }
        return true;
    }
    public static boolean allowDeath(LivingEntity entity, DamageSource source, float amount) {
        if (!(entity instanceof Villager v) || !state(v).active()) return true;
        var s = state(v); v.setHealth(1); v.clearFire(); v.getNavigation().stop();
        state(v, s.downed(v.level().getGameTime() + 1200));
        Knockouts.lieDown(v);
        var p = ((ServerLevel)v.level()).getServer().getPlayerList().getPlayer(UUID.fromString(s.owner()));
        if (p != null) {
            saveBond(v, p, bond(v, p).remember(day(v.level()), "I was badly hurt on our outing. You could help me recover."));
            p.sendSystemMessage(net.minecraft.network.chat.Component.literal(name(v) + " is downed. Right-click to help them up, or take them home."), false);
        }
        return false;
    }
    /** Called from the villager brain hook while recruited; navigation and look controls keep ticking normally. */
    public static void drive(Villager v, ServerLevel level) {
        var s = state(v); if (!s.active()) return;
        var p = level.getServer().getPlayerList().getPlayer(UUID.fromString(s.owner()));
        if (p == null || !p.isAlive() || p.level() != v.level() || !level.dimension().equals(Level.OVERWORLD)) { returnHome(v, p, true); return; }
        if (s.mode().equals("gathering_guest")) {
            if (loaded.stream().noneMatch(host -> state(host).owner().equals(s.owner()) && outings.containsKey(host.getUUID()))) { returnHome(v, p, false); return; }
        } else if (!target(p).getAttachedOrElse(VillageFriends.PARTY, "").equals(profile(v).id())) { returnHome(v, null, false); return; }
        if (s.downed()) {
            v.getNavigation().stop();
            if (!Knockouts.injured(v) || v.getPose() != Pose.SLEEPING) Knockouts.lieDown(v);
            if (level.getGameTime() >= s.until()) returnHome(v, p, false);
            return;
        }
        if (v.getY() < level.getMinY() - 4) { returnHome(v, p, false); return; }
        if (GuardController.isGuard(v) && GuardController.drive(v, level, s.mode().equals("wait"))) return;
        if (!GuardController.isGuard(v) && s.mode().equals("follow") && !outings.containsKey(v.getUUID())) {
            var attacker = p.getLastHurtByMob();
            LivingEntity foe = attacker instanceof Enemy && attacker.isAlive() && attacker.distanceToSqr(p) < 100 ? attacker : null;
            if (foe == null && v.tickCount % 10 == 0) foe = level.getEntitiesOfClass(Mob.class, v.getBoundingBox().inflate(8), m -> m instanceof Enemy && m.isAlive() && (m.getTarget() == v || m.getTarget() == p) && !target(m).hasAttached(PROFILE)).stream().findFirst().orElse(null);
            if (foe != null && v.hasLineOfSight(foe)) {
                v.getLookControl().setLookAt(foe, 30, 30); v.getNavigation().moveTo(foe, .8);
                if (v.distanceToSqr(foe) < 6 && v.tickCount % 20 == 0) {
                    v.swingForAttack(InteractionHand.MAIN_HAND);
                    if (v.doHurtTarget(level, foe) && !bond(v, p).has("outing:defense"))
                        saveBond(v, p, bond(v, p).flag("outing:defense").flag("adventure_defense").remember(day(level), "We defended each other against a " + foe.getName().getString().toLowerCase() + "."));
                }
                return;
            }
        }
        if (s.mode().equals("wait") || s.mode().equals("picnic")) { v.getNavigation().stop(); return; }
        v.getLookControl().setLookAt(p, 30, 30);
        if (v.tickCount % 10 == 0) {
            if (v.distanceToSqr(p) > 9) v.getNavigation().moveTo(p, .7); else v.getNavigation().stop();
        }
    }
    public static void tick(MinecraftServer server) {
        // Restoring interrupted activities is deterministic: they don't award progress after a restart.
        if (server.getTickCount() % 200 != 0) return;
        for (var v : List.copyOf(loaded)) {
            if (!v.isAlive() || v.isRemoved()) { loaded.remove(v); continue; }
            var s = state(v);
            if (s.active() && !s.mode().equals("follow") && !s.mode().equals("wait") && !s.downed() && !s.mode().equals("gathering_guest") && !outings.containsKey(v.getUUID())) {
                var owner = server.getPlayerList().getPlayer(UUID.fromString(s.owner())); returnHome(v, owner, false);
            }
            var neighbors = loaded.stream().filter(n -> n != v && n.isAlive() && n.level() == v.level() && n.distanceToSqr(v) < 256)
                    .sorted(Comparator.comparingDouble(v::distanceToSqr)).limit(4).map(VillageFriends::name).toList();
            if (!neighbors.equals(shared(v).neighbors())) shared(v, shared(v).neighbors(neighbors));
            var company = new HashMap<String, Integer>();
            if (shared(v).socialDay() != day(v.level())) for (var other : loaded) {
                if (other == v || !other.isAlive() || other.level() != v.level() || other.distanceToSqr(v) > 64) continue;
                var self = profile(v); var neighbor = profile(other);
                company.put(neighbor.id(), self.hobby().equals(neighbor.hobby()) || self.value().equals(neighbor.value()) ? 2 : 1);
            }
            if (!company.isEmpty()) shared(v, shared(v).mingle(day(v.level()), company));
            if (!s.active() && !v.isBaby()) for (var p : server.getPlayerList().getPlayers()) {
                if (p.level() != v.level() || p.distanceToSqr(v) > 36) continue;
                var b = bond(v, p);
                if (b.level(VillageFriends.state(v, p)) >= 2 && !b.has("invitation:picnic") && invitations.getOrDefault(p.getUUID(), -1L) != day(v.level())) {
                    invitations.put(p.getUUID(), day(v.level()));
                    saveBond(v, p, b.flag("invitation:picnic").remember(day(v.level()), "I invited you to share a picnic when you have time."));
                    p.sendSystemMessage(net.minecraft.network.chat.Component.literal(name(v) + ": Would you like a picnic sometime? Bring a snack and choose Time when we talk."), false);
                }
            }
        }
    }
    private CompanionController() {}
}
