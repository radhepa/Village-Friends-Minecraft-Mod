package dev.villagefriends.pet;

import static dev.villagefriends.VillageFriends.*;

import com.mojang.serialization.Codec;
import dev.villagefriends.CompanionController;
import dev.villagefriends.Emote;
import dev.villagefriends.GuardController;
import dev.villagefriends.GuardPatrols;
import dev.villagefriends.Knockouts;
import dev.villagefriends.ResidentRoutines;
import dev.villagefriends.VillageProfessions;
import dev.villagefriends.VillageSettlements;
import dev.villagefriends.VillageSocieties;
import dev.villagefriends.pet.PetPlays.Move;
import dev.villagefriends.pet.PetPlays.Step;
import dev.villagefriends.routine.Routine.Block;
import java.util.ArrayList;
import java.util.EnumSet;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;
import java.util.UUID;
import net.fabricmc.fabric.api.attachment.v1.AttachmentRegistry;
import net.fabricmc.fabric.api.attachment.v1.AttachmentSyncPredicate;
import net.fabricmc.fabric.api.attachment.v1.AttachmentType;
import net.fabricmc.fabric.api.networking.v1.ServerPlayNetworking;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.particles.ItemParticleOption;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.resources.Identifier;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.ItemTags;
import net.minecraft.util.Mth;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.TamableAnimal;
import net.minecraft.world.entity.ai.goal.Goal;
import net.minecraft.world.entity.animal.feline.Cat;
import net.minecraft.world.entity.animal.wolf.Wolf;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.DyeColor;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.component.CustomData;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.phys.Vec3;

/**
 * Residents and their pets. Some residents long for a cat or a dog ({@link PetKeeping#wish}); in their
 * free time they look for a stray nearby (village cats, or a stray who wanders in), walk up, offer a
 * fish or a bone and, sooner or later, take them home. A resident's pet is tamed to them the vanilla
 * way, so it follows them about, guards them and teleports to keep up; it naps by their bed while
 * they sleep and keeps watch beside them if they're knocked out. Now and then the two play together
 * ({@link PetPlays}): the resident acts out their part with a {@code pet} animation clip while this
 * class moves the pet and sets its trick, the pose the pet's model strikes. Players can open a card
 * about any resident's pet to see who they are, pat them and give them treats.
 */
public final class VillagerPets {
    private static Identifier id(String path) { return Identifier.fromNamespaceAndPath("villagefriends", path); }
    /** On a pet: who they are and who they belong to. */
    public static final AttachmentType<PetProfile> PROFILE = AttachmentRegistry.create(id("pet"), b -> b.persistent(PetProfile.CODEC));
    /** On a resident: the pet they keep. */
    public static final AttachmentType<PetLink> LINK = AttachmentRegistry.create(id("pet_link"), b -> b.persistent(PetLink.CODEC));
    /** On a stray who wandered in: the resident who was hoping for them. */
    public static final AttachmentType<String> STRAY_FOR = AttachmentRegistry.create(id("stray_for"), b -> b.persistent(Codec.STRING));
    /** On a pet, shared with clients: "trick@gameTime", the pose they're striking and when it began. */
    public static final AttachmentType<String> TRICK = AttachmentRegistry.create(id("pet_trick"),
            b -> b.syncWith(ByteBufCodecs.STRING_UTF8, AttachmentSyncPredicate.all()));
    /** On a resident, shared with clients: "phase|species|gameTime" while playing with a pet. */
    public static final AttachmentType<String> PLAY = AttachmentRegistry.create(id("pet_play"),
            b -> b.syncWith(ByteBufCodecs.STRING_UTF8, AttachmentSyncPredicate.all()));
    /** On the overworld: "died:<pet>" and "orphan:<pet>" notes for pets and residents who weren't loaded when it happened. */
    public static final AttachmentType<List<String>> LOSSES = AttachmentRegistry.create(id("pet_losses"),
            b -> b.initializer(List::of).persistent(Codec.STRING.listOf()));
    public static final String FETCH_TAG = "villagefriends_fetch", PROP = "villagefriends_prop";
    private static final Set<Block> FREE_TIME = EnumSet.of(Block.HOBBY, Block.SOCIAL, Block.MARKET, Block.EVENING, Block.PLAY,
            Block.SNOW_PLAY, Block.RAIN_WALK, Block.WAKE, Block.BREAKFAST, Block.SUPPER, Block.LUNCH, Block.LUNCH_HOME);
    private static final int CONSIDER_EVERY = 40;

    /** A resident and a pet acting out a script together. */
    static final class Session {
        final Villager villager; final TamableAnimal pet; final String game, species; final boolean taming; final List<Step> steps;
        final long started; final List<Vec3> waypoints = new ArrayList<>();
        int index = -1, waypoint = -1; long stepStart; String phase = "", trick = "";
        Vec3 target; ItemEntity stick; boolean arrived, stuck; float angle;
        Session(Villager villager, TamableAnimal pet, String game, String species, boolean taming, List<Step> steps, long now) {
            this.villager = villager; this.pet = pet; this.game = game; this.species = species; this.taming = taming; this.steps = steps; this.started = now;
        }
        Step step() { return index < 0 || index >= steps.size() ? null : steps.get(index); }
        boolean cat() { return species.equals(PetKeeping.CAT); }
    }
    private record Attention(UUID player, long until) {}
    private static final Map<UUID, Session> byVillager = new HashMap<>(), byPet = new HashMap<>();
    private static final Map<UUID, Long> nextPlay = new HashMap<>(), nextAdopt = new HashMap<>(), nextStray = new HashMap<>();
    /** Tricks a pet does for a player, and when they end. */
    private static final Map<TamableAnimal, Long> trickEnds = new HashMap<>();
    private static final Map<UUID, Integer> attempts = new HashMap<>();
    private static final Map<UUID, Attention> attention = new HashMap<>();

    /** Registers the attachments at startup, before any player joins: synced attachment types are agreed with each client as they connect. */
    public static void register() {}
    public static void clear() {
        byVillager.clear(); byPet.clear(); nextPlay.clear(); nextAdopt.clear(); nextStray.clear(); trickEnds.clear(); attempts.clear(); attention.clear();
    }

    // -- queries -----------------------------------------------------------------------------------

    public static PetProfile profile(Entity pet) { return target(pet).getAttached(PROFILE); }
    public static PetLink link(Villager v) { return target(v).getAttached(LINK); }
    /** A cat or dog that belongs (or once belonged) to a resident. */
    public static boolean residentPet(Entity e) { return (e instanceof Cat || e instanceof Wolf) && target(e).hasAttached(PROFILE); }
    /** "Pet: Biscuit the cat" for a resident's conversation card, or "". */
    public static String petLine(Villager v) { var l = link(v); return l == null ? "" : "Pet: " + l.describe(); }
    public static boolean playing(Villager v) { return byVillager.containsKey(v.getUUID()); }

    // -- loading -----------------------------------------------------------------------------------

    public static void loaded(Entity entity) {
        if (entity instanceof ItemEntity item && item.entityTags().contains(FETCH_TAG)) { item.discard(); return; }
        if (entity instanceof Villager v) { clearProp(v); return; }
        if (!(entity instanceof Cat || entity instanceof Wolf)) return;
        var pet = (TamableAnimal) entity;
        var accessor = (dev.villagefriends.mixin.MobGoalsAccessor) pet;
        var goals = accessor.villagefriends$goals();
        if (goals.getAvailableGoals().stream().noneMatch(g -> g.getGoal() instanceof PetGoal)) goals.addGoal(1, new PetGoal(pet));
        // A stray who wandered in to find a home doesn't go after the village's sheep while it waits.
        if (target(pet).hasAttached(STRAY_FOR)) accessor.villagefriends$targets().removeAllGoals(g -> g instanceof net.minecraft.world.entity.ai.goal.target.NonTameRandomTargetGoal<?>);
        var profile = profile(pet);
        if (profile != null && profile.owned() && pet.level() instanceof ServerLevel level && takeLoss(level, "orphan:" + pet.getUUID())) release(pet, profile);
    }
    public static void unloaded(Entity entity) {
        var s = entity instanceof Villager ? byVillager.get(entity.getUUID()) : byPet.get(entity.getUUID());
        if (s != null) end(s, false);
        attention.remove(entity.getUUID());
    }

    // -- the world ticking -------------------------------------------------------------------------

    public static void tick(MinecraftServer server) {
        tickSessions();
        int tick = server.getTickCount();
        for (var v : List.copyOf(CompanionController.loaded)) {
            if (Math.floorMod(tick + v.getId(), CONSIDER_EVERY) != 0 || !(v.level() instanceof ServerLevel level)) continue;
            consider(v, level, level.getGameTime());
        }
        if (tick % 10 == 0) {
            trickEnds.entrySet().removeIf(e -> {
                var pet = e.getKey();
                if (pet.isRemoved()) return true;
                if (pet.level().getGameTime() < e.getValue()) return false;
                if (!byPet.containsKey(pet.getUUID())) target(pet).removeAttached(TRICK);
                return true;
            });
            attention.entrySet().removeIf(e -> server.overworld().getGameTime() > e.getValue().until());
        }
    }

    private static void consider(Villager v, ServerLevel level, long now) {
        if (byVillager.containsKey(v.getUUID()) || !v.isAlive() || v.isRemoved()) return;
        var link = link(v);
        if (link != null) { lookAfter(v, link, level, now); return; }
        var profile = dev.villagefriends.VillageFriends.profile(v);
        String wish = PetKeeping.wish(UUID.fromString(profile.id()), profile.personality(), v.isBaby());
        if (wish.isEmpty() || !free(v) || !level.isBrightOutside()) return;
        adopt(v, wish, level, now);
    }

    /** Awake, unhurt, not busy with a player, a fight, a raid or a trade, and in a free part of their day. */
    private static boolean free(Villager v) {
        if (v.isSleeping() || v.isNoAi() || v.isPassenger() || !v.onGround() || v.isInWater() || Knockouts.injured(v) || v.isTrading()
                || CompanionController.state(v).active() || CompanionController.hasActivity(v) || GuardController.fighting(v) || GuardPatrols.defending(v)) return false;
        var block = ResidentRoutines.plan(v).block();
        if (FREE_TIME.contains(block)) return true;
        String job = profession(v);
        return block == Block.WORK && (v.isBaby() || job.equals("none") || job.equals("nitwit"));
    }

    // -- a resident and their pet ------------------------------------------------------------------

    private static void lookAfter(Villager v, PetLink link, ServerLevel level, long now) {
        var entity = level.getEntity(UUID.fromString(link.pet()));
        if (!(entity instanceof TamableAnimal pet) || !pet.isAlive()) {
            if (takeLoss(level, "died:" + link.pet())) forget(v);
            return;
        }
        keep(v, pet, link);
        if (now < nextPlay.computeIfAbsent(v.getUUID(), k -> now + 200 + v.getRandom().nextInt(1000))) return;
        if (!free(v) || !v.getNavigation().isDone() || pet.distanceToSqr(v) > 100 || pet.isLeashed() || pet.isPassenger() || pet.isOrderedToSit()
                || pet.isInWater() || !pet.onGround() || byPet.containsKey(pet.getUUID())) return;
        var profile = profile(pet);
        if (profile == null) return;
        boolean wet = level.isRainingAt(v.blockPosition().above());
        if (wet && profile.cat()) { nextPlay.put(v.getUUID(), now + 600); return; }
        var random = new Random(now * 31 + v.getUUID().hashCode());
        var possible = new ArrayList<>(PetKeeping.games(profile.species()));
        List<Vec3> waypoints = List.of();
        if (wet || landing(level, v, pet, 5) == null) possible.remove("fetch");
        if (possible.contains("chase")) { waypoints = waypoints(level, v, random); if (waypoints.size() < 3) possible.remove("chase"); }
        String game = PetKeeping.pickGame(random, profile, possible);
        int rounds = game.equals("fetch") && (profile.game().equals("fetch") || profile.personality().equals("zoomy") || random.nextBoolean()) ? 2 : 1;
        var s = new Session(v, pet, game, profile.species(), false, PetPlays.game(game, profile.treat(), rounds), now);
        if (game.equals("chase")) s.waypoints.addAll(waypoints);
        begin(s);
    }

    /** Keeps the vanilla ownership pointing at this resident (a cured resident is a new entity) and the names current. */
    private static void keep(Villager v, TamableAnimal pet, PetLink link) {
        if (!pet.isTame()) pet.setTame(true, true);
        var owner = pet.getOwnerReference();
        if (owner == null || !owner.getUUID().equals(v.getUUID())) pet.setOwner(v);
        var profile = profile(pet);
        if (profile == null) return;
        String petName = pet.hasCustomName() ? pet.getCustomName().getString() : profile.name();
        var next = profile.ownerName(name(v)).renamed(petName);
        if (next != profile) target(pet).setAttached(PROFILE, next);
        if (!petName.equals(link.name())) target(v).setAttached(LINK, new PetLink(link.pet(), link.species(), petName, link.since()));
    }

    // -- adopting a stray --------------------------------------------------------------------------

    private static void adopt(Villager v, String wish, ServerLevel level, long now) {
        UUID id = v.getUUID();
        if (now < nextAdopt.getOrDefault(id, 0L)) return;
        var random = new Random(now ^ id.getLeastSignificantBits());
        nextAdopt.put(id, now + 300 + random.nextInt(400));
        String resident = dev.villagefriends.VillageFriends.profile(v).id();
        var type = wish.equals(PetKeeping.CAT) ? EntityTypes.CAT : EntityTypes.WOLF;
        var stray = level.getEntitiesOfClass(TamableAnimal.class, v.getBoundingBox().inflate(16, 4, 16), a -> a.getType() == type && a.isAlive()
                        && !a.isTame() && !byPet.containsKey(a.getUUID()) && !a.isLeashed() && !a.isPassenger() && !(a instanceof Wolf w && w.isAngry()))
                .stream().min((a, b) -> Double.compare(rank(a, v, resident), rank(b, v, resident))).orElse(null);
        if (stray != null) {
            boolean expected = resident.equals(target(stray).getAttached(STRAY_FOR));
            int tries = attempts.getOrDefault(id, 0);
            boolean success = random.nextDouble() < .4 + .2 * tries + (expected ? .25 : 0);
            begin(new Session(v, stray, "taming", wish, true, PetPlays.taming(wish, success), now));
            return;
        }
        // Nobody around to befriend: before long, a stray wanders into the village.
        long arrival = nextStray.computeIfAbsent(id, k -> now + 1200 + random.nextInt(6000));
        if (now < arrival) return;
        nextStray.put(id, now + 12000 + random.nextInt(12000));
        long strays = level.getEntitiesOfClass(TamableAnimal.class, v.getBoundingBox().inflate(48, 16, 48), a -> target(a).hasAttached(STRAY_FOR) && !a.isTame()).size();
        if (strays < 2) spawnStray(v, wish, resident, level, random);
    }
    private static double rank(TamableAnimal stray, Villager v, String resident) {
        return stray.distanceToSqr(v) - (resident.equals(target(stray).getAttached(STRAY_FOR)) ? 400 : 0);
    }
    private static void spawnStray(Villager v, String species, String resident, ServerLevel level, Random random) {
        for (int i = 0; i < 24; i++) {
            double angle = random.nextDouble() * Math.PI * 2, distance = 10 + random.nextDouble() * 8;
            int x = Mth.floor(v.getX() + Math.cos(angle) * distance), z = Mth.floor(v.getZ() + Math.sin(angle) * distance);
            var pos = new BlockPos(x, level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, x, z), z);
            if (!level.isLoaded(pos) || Math.abs(pos.getY() - v.getY()) > 6 || !standable(level, pos)) continue;
            if (level.getNearestPlayer(pos.getX() + .5, pos.getY(), pos.getZ() + .5, 10, false) != null) continue;
            TamableAnimal animal = species.equals(PetKeeping.CAT) ? EntityTypes.CAT.create(level, EntitySpawnReason.EVENT) : EntityTypes.WOLF.create(level, EntitySpawnReason.EVENT);
            if (animal == null) return;
            animal.snapTo(pos.getX() + .5, pos.getY(), pos.getZ() + .5, random.nextFloat() * 360, 0);
            animal.finalizeSpawn(level, level.getCurrentDifficultyAt(pos), EntitySpawnReason.EVENT, null);
            if (animal instanceof Cat cat) randomVariant(level, cat, Registries.CAT_VARIANT, DataComponents.CAT_VARIANT, random);
            else randomVariant(level, animal, Registries.WOLF_VARIANT, DataComponents.WOLF_VARIANT, random);
            if (random.nextDouble() < (species.equals(PetKeeping.CAT) ? .3 : .35)) animal.setAge(-24000);
            target(animal).setAttached(STRAY_FOR, resident);
            level.addFreshEntity(animal);
            return;
        }
    }
    private static <T> void randomVariant(ServerLevel level, Entity animal, net.minecraft.resources.ResourceKey<? extends net.minecraft.core.Registry<T>> registry,
            net.minecraft.core.component.DataComponentType<net.minecraft.core.Holder<T>> component, Random random) {
        var variants = level.registryAccess().lookupOrThrow(registry).listElements().toList();
        if (!variants.isEmpty()) animal.setComponent(component, variants.get(random.nextInt(variants.size())));
    }

    private static void tame(Session s, ServerLevel level, long now) {
        var pet = s.pet; var v = s.villager;
        pet.setTame(true, true); pet.setOwner(v); pet.setOrderedToSit(false); pet.setPersistenceRequired(); pet.setTarget(null);
        var resident = dev.villagefriends.VillageFriends.profile(v);
        var random = new Random(pet.getUUID().getLeastSignificantBits() ^ now);
        // A pet whose resident died keeps their name and nature when someone new takes them in.
        var before = profile(pet);
        var profile = before != null ? before.adoptedBy(resident.id(), name(v), day(level))
                : PetKeeping.newProfile(random, s.species, resident.id(), name(v), day(level), pet.isBaby());
        if (pet.hasCustomName()) profile = profile.renamed(pet.getCustomName().getString());
        else pet.setCustomName(Component.literal(profile.name()));
        target(pet).setAttached(PROFILE, profile);
        target(pet).removeAttached(STRAY_FOR);
        var collar = DyeColor.byName(PetKeeping.collar(random, resident.personality()), DyeColor.RED);
        pet.setComponent(s.cat() ? DataComponents.CAT_COLLAR : DataComponents.WOLF_COLLAR, collar);
        target(v).setAttached(LINK, new PetLink(pet.getUUID().toString(), s.species, profile.name(), day(level)));
        attempts.remove(v.getUUID()); nextStray.remove(v.getUUID());
        nextPlay.put(v.getUUID(), now + 1200);
        VillageSocieties.emote(v, Emote.HEART, 0);
        var line = Component.literal(name(v) + " adopted a stray " + (pet.isBaby() ? s.cat() ? "kitten" : "puppy" : s.species) + " and named it " + profile.name() + ".");
        for (var p : level.players()) if (p.distanceToSqr(v) < 48 * 48) p.sendSystemMessage(line, false);
    }

    // -- losing each other -------------------------------------------------------------------------

    /** A resident or a resident's pet died. */
    public static void died(LivingEntity entity) {
        if (!(entity.level() instanceof ServerLevel level)) return;
        if (entity instanceof Villager v) {
            var link = link(v);
            if (link == null) return;
            var pet = level.getEntity(UUID.fromString(link.pet()));
            if (pet instanceof TamableAnimal t && profile(t) != null) release(t, profile(t));
            else addLoss(level, "orphan:" + link.pet());
            return;
        }
        var profile = profile(entity);
        if (profile == null || !profile.owned() || !(entity instanceof TamableAnimal pet)) return;
        if (pet.getOwner() instanceof Villager owner) {
            if (link(owner) != null && link(owner).pet().equals(pet.getUUID().toString())) forget(owner);
        } else addLoss(level, "died:" + pet.getUUID());
        var line = Component.literal(profile.name() + ", " + profile.ownerName() + "'s " + profile.species() + ", has died.");
        for (var p : level.players()) if (p.distanceToSqr(pet) < 48 * 48) p.sendSystemMessage(line, false);
    }
    private static void forget(Villager v) {
        target(v).removeAttached(LINK);
        nextPlay.remove(v.getUUID());
        VillageSocieties.emote(v, Emote.GLOOM, 0);
    }
    /** Their resident is gone: the pet is a stray again (remembering who they belonged to), and someone else may take them in. */
    private static void release(TamableAnimal pet, PetProfile profile) {
        var s = byPet.get(pet.getUUID());
        if (s != null) end(s, false);
        target(pet).setAttached(PROFILE, profile.released());
        pet.setOwnerReference(null); pet.setTame(false, true); pet.setInSittingPose(false); pet.setOrderedToSit(false);
    }
    private static void addLoss(ServerLevel level, String note) {
        var overworld = level.getServer().overworld();
        var list = new ArrayList<>(overworld.getAttachedOrCreate(LOSSES));
        list.add(note);
        while (list.size() > 256) list.removeFirst();
        overworld.setAttached(LOSSES, List.copyOf(list));
    }
    private static boolean takeLoss(ServerLevel level, String note) {
        var overworld = level.getServer().overworld();
        var list = overworld.getAttachedOrCreate(LOSSES);
        if (!list.contains(note)) return false;
        var next = new ArrayList<>(list); next.remove(note);
        overworld.setAttached(LOSSES, List.copyOf(next));
        return true;
    }

    // -- sessions ----------------------------------------------------------------------------------

    /** Starts a resident befriending this stray right away, ending however it was told to (for tests). */
    public static void befriend(Villager v, TamableAnimal stray, boolean success) {
        String species = stray instanceof Cat ? PetKeeping.CAT : PetKeeping.DOG;
        cancel(v, stray);
        begin(new Session(v, stray, "taming", species, true, PetPlays.taming(species, success), v.level().getGameTime()));
    }
    /** Starts a resident and their pet playing this game right away (for tests). */
    public static void play(Villager v, TamableAnimal pet, String game) {
        var profile = profile(pet);
        cancel(v, pet);
        var s = new Session(v, pet, game, profile.species(), false, PetPlays.game(game, profile.treat(), 1), v.level().getGameTime());
        if (game.equals("chase") && v.level() instanceof ServerLevel level) s.waypoints.addAll(waypoints(level, v, new Random(1)));
        begin(s);
    }
    private static final Map<UUID, String> lastEnded = new HashMap<>();
    /** Where a resident's session is, or why their last one ended (for tests and debugging). */
    public static String describe(Villager v) {
        var s = byVillager.get(v.getUUID());
        if (s == null) return "no session; last ended: " + lastEnded.getOrDefault(v.getUUID(), "never");
        var step = s.step();
        return s.game + " step " + s.index + "/" + s.steps.size() + (step == null ? "" : " " + step.move() + " phase=" + step.phase() + " trick=" + step.trick())
                + " distance=" + String.format(java.util.Locale.ROOT, "%.1f", Math.sqrt(v.distanceToSqr(s.pet))) + " navDone=" + v.getNavigation().isDone();
    }
    /** The game a pet is playing (or "taming"), or null. */
    public static String game(Entity pet) { var s = byPet.get(pet.getUUID()); return s == null ? null : s.game; }
    private static void cancel(Villager v, TamableAnimal pet) {
        var a = byVillager.get(v.getUUID()); if (a != null) end(a, false);
        var b = byPet.get(pet.getUUID()); if (b != null) end(b, false);
    }

    private static void begin(Session s) {
        byVillager.put(s.villager.getUUID(), s); byPet.put(s.pet.getUUID(), s);
        s.villager.getBrain().eraseMemory(net.minecraft.world.entity.ai.memory.MemoryModuleType.WALK_TARGET);
        s.pet.getNavigation().stop();
    }
    private static void tickSessions() {
        for (var s : List.copyOf(byVillager.values())) {
            if (!(s.villager.level() instanceof ServerLevel level)) { end(s, false); continue; }
            long now = level.getGameTime();
            String why = invalid(s, now);
            if (why != null) { lastEnded.put(s.villager.getUUID(), why); end(s, false); continue; }
            if (s.index < 0) { advance(s, level, now); continue; }
            var step = s.step();
            boolean done = arrived(s, step);
            if (now - s.stepStart >= step.ticks() || step.until() && done) {
                // A resident who couldn't reach the stray gives up.
                if (step.move() == Move.APPROACH && !done) { lastEnded.put(s.villager.getUUID(), "couldn't reach the stray"); end(s, false); continue; }
                if (s.index + 1 >= s.steps.size()) { lastEnded.put(s.villager.getUUID(), "finished " + s.game); end(s, true); } else advance(s, level, now);
            }
        }
    }
    /** Why a session can't go on, or null while it can. */
    private static String invalid(Session s, long now) {
        var v = s.villager; var pet = s.pet;
        if (!v.isAlive() || v.isRemoved() || !pet.isAlive() || pet.isRemoved() || v.level() != pet.level()) return "gone";
        if (v.distanceToSqr(pet) > 24 * 24) return "too far apart";
        if (v.isSleeping() || Knockouts.injured(v)) return "asleep or hurt";
        if (v.isTrading() || CompanionController.state(v).active() || CompanionController.hasActivity(v)) return "busy with a player";
        if (v.hurtTime > 0 || pet.hurtTime > 0) return "hurt";
        if (GuardController.fighting(v) || GuardPatrols.defending(v)) return "fighting";
        if (pet.isLeashed() || pet.isPassenger()) return "pet leashed";
        if (now - s.started > 2400) return "took too long";
        if (s.taming) return !pet.isTame() || pet.getOwner() == v ? null : "someone else tamed it";
        return pet.isTame() && pet.getOwner() == v ? null : "not their pet";
    }
    private static boolean arrived(Session s, Step step) {
        return switch (step.move()) {
            case FETCH -> s.stick == null || !s.stick.isAlive() ? s.target == null || s.pet.position().distanceToSqr(s.target) < 1.3 * 1.3
                    : s.stick.onGround() && s.pet.position().distanceToSqr(s.stick.position()) < 1.3 * 1.3;
            case RETURN -> s.arrived || s.stuck;
            case CHASE -> s.waypoint >= 0 && s.waypoint < s.waypoints.size() && s.villager.position().distanceToSqr(s.waypoints.get(s.waypoint)) < 1.4 * 1.4;
            case APPROACH -> s.villager.distanceToSqr(s.pet) < 2.3 * 2.3;
            default -> false;
        };
    }
    private static void advance(Session s, ServerLevel level, long now) {
        s.index++; s.stepStart = now; s.arrived = false; s.stuck = false;
        var step = s.step();
        if (!step.phase().equals(s.phase)) {
            s.phase = step.phase();
            if (s.phase.isEmpty()) target(s.villager).removeAttached(PLAY);
            else target(s.villager).setAttached(PLAY, s.phase + "|" + s.species + "|" + now);
        }
        if (!step.trick().equals(s.trick)) {
            s.trick = step.trick();
            if (s.trick.isEmpty()) target(s.pet).removeAttached(TRICK);
            else target(s.pet).setAttached(TRICK, s.trick + "@" + now);
        }
        boolean sits = step.move() == Move.SIT || step.move() == Move.COAX && !s.cat();
        if (!sits) s.pet.setInSittingPose(false);
        if (step.move() != Move.LIE && s.pet instanceof Cat cat) cat.setLying(false);
        if (step.move() == Move.CHASE) s.waypoint++;
        if (step.move() == Move.FLEE) s.target = null;
        for (String event : step.eventList()) fire(s, event, level, now);
    }
    private static void end(Session s, boolean finished) {
        byVillager.remove(s.villager.getUUID()); byPet.remove(s.pet.getUUID());
        target(s.villager).removeAttached(PLAY);
        target(s.pet).removeAttached(TRICK);
        clearProp(s.villager);
        if (s.stick != null) { s.stick.discard(); s.stick = null; }
        s.pet.setInSittingPose(false);
        if (s.pet instanceof Cat cat) cat.setLying(false);
        if (s.pet instanceof Wolf wolf) wolf.setIsInterested(false);
        s.pet.getNavigation().stop(); s.villager.getNavigation().stop();
        long now = s.villager.level().getGameTime();
        var random = new Random(now ^ s.villager.getUUID().getMostSignificantBits());
        if (s.taming) {
            if (!s.pet.isTame()) nextAdopt.put(s.villager.getUUID(), now + 1200 + random.nextInt(1200));
            return;
        }
        var profile = profile(s.pet);
        nextPlay.put(s.villager.getUUID(), now + (profile == null ? 2400 : PetKeeping.playPause(random,
                profile, dev.villagefriends.VillageFriends.profile(s.villager).personality())));
        if (finished && random.nextInt(5) < 2) VillageSocieties.emote(s.villager, random.nextBoolean() ? Emote.HEART : Emote.NOTE, 0);
    }

    // -- events ------------------------------------------------------------------------------------

    private static void fire(Session s, String event, ServerLevel level, long now) {
        var pet = s.pet; var v = s.villager;
        if (event.startsWith("prop:")) { holdProp(v, event.substring(5)); return; }
        switch (event) {
            case "clear_prop" -> clearProp(v);
            case "throw" -> throwStick(s, level);
            case "pickup" -> { if (s.stick != null) { s.stick.discard(); s.stick = null; } }
            case "hop" -> { if (pet.onGround()) pet.getJumpControl().jump(); }
            case "pounce" -> {
                var dir = horizontal(v.position().subtract(pet.position()));
                if (pet.onGround()) pet.setDeltaMovement(dir.x * .3, .36, dir.z * .3);
            }
            case "bark", "meow" -> pet.playAmbientSound();
            case "purr" -> sound(pet, purr(pet), .7F);
            case "eat" -> {
                pet.playSound(SoundEvents.GENERIC_EAT.value(), .6F, 1.2F);
                var food = v.getMainHandItem().isEmpty() ? new ItemStack(s.cat() ? Items.COD : Items.COOKED_BEEF) : v.getMainHandItem().copyWithCount(1);
                level.sendParticles(new ItemParticleOption(ParticleTypes.ITEM, food.getItem()), pet.getX(), pet.getY() + pet.getBbHeight() * .7, pet.getZ(), 6, .12, .08, .12, .05);
            }
            case "hearts" -> level.broadcastEntityEvent(pet, (byte) 7);
            case "interested" -> { if (pet instanceof Wolf wolf) wolf.setIsInterested(true); }
            case "tame" -> tame(s, level, now);
            case "refuse" -> {
                level.broadcastEntityEvent(pet, (byte) 6);
                attempts.merge(v.getUUID(), 1, Integer::sum);
                VillageSocieties.emote(v, Emote.SWEAT, 0);
            }
            default -> {}
        }
    }
    private static net.minecraft.sounds.SoundEvent purr(TamableAnimal pet) {
        if (pet instanceof Cat cat) {
            var variant = cat.get(DataComponents.CAT_SOUND_VARIANT);
            if (variant != null) return (cat.isBaby() ? variant.value().babySounds() : variant.value().adultSounds()).purrSound().value();
        }
        if (pet instanceof Wolf wolf) {
            var variant = wolf.get(DataComponents.WOLF_SOUND_VARIANT);
            if (variant != null) return (wolf.isBaby() ? variant.value().babySounds() : variant.value().adultSounds()).pantSound().value();
        }
        return null;
    }
    private static void sound(Entity e, net.minecraft.sounds.SoundEvent sound, float volume) {
        if (sound != null) e.playSound(sound, volume, .9F + e.level().getRandom().nextFloat() * .2F);
    }
    private static void whine(TamableAnimal pet) {
        if (pet instanceof Wolf wolf) {
            var variant = wolf.get(DataComponents.WOLF_SOUND_VARIANT);
            if (variant != null) sound(pet, (wolf.isBaby() ? variant.value().babySounds() : variant.value().adultSounds()).whineSound().value(), .7F);
        } else sound(pet, purr(pet), .5F);
    }

    // -- fetch -------------------------------------------------------------------------------------

    private static void throwStick(Session s, ServerLevel level) {
        var v = s.villager;
        var landing = landing(level, v, s.pet, 4);
        var dir = horizontal(s.pet.position().subtract(v.position()));
        if (dir.lengthSqr() < 1e-4) dir = horizontal(v.getLookAngle());
        if (landing == null) landing = s.pet.position().add(dir.scale(2));
        s.target = landing;
        double distance = Math.sqrt(horizontal(landing.subtract(v.position())).lengthSqr());
        var hand = v.position().add(0, v.getEyeHeight() * .85, 0).add(dir.scale(.3));
        var stick = new ItemEntity(level, hand.x, hand.y, hand.z, new ItemStack(Items.STICK), dir.x * distance / 16.5, .3, dir.z * distance / 16.5);
        stick.setNeverPickUp();
        stick.addTag(FETCH_TAG);
        level.addFreshEntity(stick);
        s.stick = stick;
    }
    /** Somewhere 5 to 7 blocks past the pet, on open level ground in sight, where a stick can land; null if there's no room. */
    private static Vec3 landing(ServerLevel level, Villager v, TamableAnimal pet, int minimum) {
        var dir = horizontal(pet.position().subtract(v.position()));
        if (dir.lengthSqr() < 1e-4) dir = horizontal(v.getLookAngle());
        for (int d = 7; d >= minimum; d--) {
            var spot = v.position().add(dir.scale(d));
            var pos = BlockPos.containing(spot);
            for (int dy = 0; dy <= 1; dy++) {
                var p = pos.below(dy);
                if (Math.abs(p.getY() - v.getBlockY()) <= 1 && standable(level, p) && level.clip(new net.minecraft.world.level.ClipContext(v.getEyePosition(),
                        Vec3.atCenterOf(p).add(0, .5, 0), net.minecraft.world.level.ClipContext.Block.COLLIDER, net.minecraft.world.level.ClipContext.Fluid.ANY, v)).getType()
                        == net.minecraft.world.phys.HitResult.Type.MISS)
                    return new Vec3(p.getX() + .5, p.getY(), p.getZ() + .5);
            }
        }
        return null;
    }
    /** Where the dog runs: where the stick will land while it's in the air, then the stick itself. */
    private static Vec3 fetchTarget(Session s) {
        if (s.stick != null && s.stick.isAlive() && (s.stick.onGround() || s.target == null)) return s.stick.position();
        return s.target == null ? s.pet.position() : s.target;
    }

    /** Three open spots around a resident to run between for a game of chase. */
    private static List<Vec3> waypoints(ServerLevel level, Villager v, Random random) {
        var points = new ArrayList<Vec3>();
        double start = random.nextDouble() * Math.PI * 2;
        for (int i = 0; i < 6 && points.size() < 3; i++) {
            double angle = start + i * Math.PI * 2 / 3 + (i >= 3 ? Math.PI / 3 : 0);
            var pos = BlockPos.containing(v.getX() + Math.cos(angle) * 4.5, v.getY(), v.getZ() + Math.sin(angle) * 4.5);
            for (int dy : new int[] {0, 1, -1}) {
                if (standable(level, pos.above(dy))) { points.add(Vec3.atBottomCenterOf(pos.above(dy))); break; }
            }
        }
        return points;
    }
    private static boolean standable(Level level, BlockPos pos) {
        return level.getBlockState(pos).getCollisionShape(level, pos).isEmpty() && level.getBlockState(pos.above()).getCollisionShape(level, pos.above()).isEmpty()
                && level.getFluidState(pos).isEmpty() && level.getBlockState(pos.below()).isFaceSturdy(level, pos.below(), Direction.UP);
    }
    private static Vec3 horizontal(Vec3 v) { var flat = new Vec3(v.x, 0, v.z); return flat.lengthSqr() < 1e-6 ? Vec3.ZERO : flat.normalize(); }

    // -- props: what a resident holds while playing -------------------------------------------------

    private static void holdProp(Villager v, String item) {
        var held = v.getMainHandItem();
        if (!held.isEmpty() && !isProp(held)) return; // a guard keeps their sword
        var value = BuiltInRegistries.ITEM.getValue(Identifier.parse(item));
        if (value == null || value == Items.AIR) return;
        var stack = new ItemStack(value);
        CustomData.update(DataComponents.CUSTOM_DATA, stack, tag -> tag.putBoolean(PROP, true));
        v.setItemSlot(EquipmentSlot.MAINHAND, stack);
        v.setDropChance(EquipmentSlot.MAINHAND, 0);
    }
    public static void clearProp(Villager v) {
        if (!isProp(v.getMainHandItem())) return;
        v.setItemSlot(EquipmentSlot.MAINHAND, ItemStack.EMPTY);
        v.setDropChance(EquipmentSlot.MAINHAND, .085F);
    }
    private static boolean isProp(ItemStack stack) {
        var data = stack.get(DataComponents.CUSTOM_DATA);
        return data != null && data.copyTag().getBooleanOr(PROP, false);
    }

    // -- moving: called every tick from the pet's goal and the resident's AI step -------------------

    /**
     * The pet's goal runs while it's playing, being befriended, looking at a player, minding a sleeping or
     * hurt resident, or trotting to catch up with them (from seven blocks away until within three).
     */
    static boolean wanted(TamableAnimal pet, boolean running) {
        if (byPet.containsKey(pet.getUUID()) || attention.containsKey(pet.getUUID())) return true;
        if (!pet.isTame() || pet.isOrderedToSit() || pet.isLeashed() || pet.isPassenger() || !(pet.getOwner() instanceof Villager owner) || owner.level() != pet.level()) return false;
        double d = pet.distanceToSqr(owner);
        if (d > 48 * 48) return false;
        return owner.isSleeping() || Knockouts.injured(owner) || d > (running ? 3 * 3 : 7 * 7);
    }
    static void steer(TamableAnimal pet) {
        var s = byPet.get(pet.getUUID());
        if (s != null) { steerPlay(s); return; }
        var look = attention.get(pet.getUUID());
        if (look != null && pet.level() instanceof ServerLevel level && level.getPlayerByUUID(look.player()) instanceof Player p) {
            pet.getNavigation().stop(); pet.getLookControl().setLookAt(p, 30, 30); face(pet, p.position(), 10); return;
        }
        if (!(pet.getOwner() instanceof Villager owner)) return;
        if (owner.isSleeping() || Knockouts.injured(owner)) { rest(pet, owner); return; }
        // Catching up with their resident.
        pet.setInSittingPose(false);
        if (pet instanceof Cat cat) cat.setLying(false);
        if (pet.distanceToSqr(owner) > 144) { pet.tryToTeleportToOwner(); return; }
        pet.getLookControl().setLookAt(owner, 10, pet.getMaxHeadXRot());
        if (pet.tickCount % 10 == 0 || pet.getNavigation().isDone()) pet.getNavigation().moveTo(owner, pet instanceof Cat ? 1.0 : 1.1);
    }
    static void stopped(TamableAnimal pet) {
        if (byPet.containsKey(pet.getUUID())) return;
        pet.setInSittingPose(false);
        if (pet instanceof Cat cat) cat.setLying(false);
    }
    /** Beside a sleeping resident: a cat curls up, a dog lies watch. Beside a knocked-out one, a dog whines now and then. */
    private static void rest(TamableAnimal pet, Villager owner) {
        var nav = pet.getNavigation();
        double d = pet.distanceToSqr(owner);
        if (d > 144) { pet.tryToTeleportToOwner(); return; }
        if (d > 2.4 * 2.4) {
            pet.setInSittingPose(false);
            if (pet instanceof Cat cat) cat.setLying(false);
            if ((pet.tickCount % 10 == 0 || nav.isDone()) && !nav.moveTo(owner, 1.0)) settle(pet, owner);
            return;
        }
        nav.stop();
        settle(pet, owner);
        if (Knockouts.injured(owner) && pet.tickCount % 200 == 0) whine(pet);
    }
    private static void settle(TamableAnimal pet, Villager owner) {
        pet.getLookControl().setLookAt(owner, 20, 20);
        if (pet instanceof Cat cat) cat.setLying(true); else pet.setInSittingPose(true);
    }
    private static void steerPlay(Session s) {
        var step = s.step();
        var pet = s.pet; var v = s.villager; var nav = pet.getNavigation();
        if (step == null) { nav.stop(); return; }
        switch (step.move()) {
            case STAY, APPROACH -> { nav.stop(); pet.getLookControl().setLookAt(v, 30, 30); face(pet, v.position(), 8); }
            case FRONT, SIT, LIE, COAX, RETURN -> {
                var spot = front(s, step.move());
                double d = Math.sqrt(horizontal2(pet.position(), spot));
                double tolerance = s.arrived ? .9 : step.move() == Move.RETURN ? .6 : .4;
                // Somewhere it can't reach (behind a fence, against a wall): it settles where it is.
                if (d > tolerance && !s.stuck) {
                    s.arrived = false;
                    pet.setInSittingPose(false);
                    if (pet instanceof Cat cat) cat.setLying(false);
                    if ((pet.tickCount % 8 == 0 || nav.isDone()) && !nav.moveTo(spot.x, spot.y, spot.z, speed(s, step.move()))) s.stuck = true;
                    if (step.move() == Move.RETURN) pet.getLookControl().setLookAt(v, 30, 30);
                } else {
                    s.arrived = true;
                    nav.stop();
                    pet.getLookControl().setLookAt(v, 30, 30); face(pet, v.position(), 12);
                    if (step.move() == Move.SIT || step.move() == Move.COAX && !s.cat()) pet.setInSittingPose(true);
                    if (step.move() == Move.LIE && pet instanceof Cat cat) cat.setLying(true);
                }
            }
            case FETCH -> {
                var t = fetchTarget(s);
                if (pet.tickCount % 5 == 0 || nav.isDone()) nav.moveTo(t.x, t.y, t.z, 1.5);
                pet.getLookControl().setLookAt(t.x, t.y, t.z, 30, 30);
            }
            case CIRCLE, WEAVE -> {
                boolean weave = step.move() == Move.WEAVE;
                s.angle += weave ? 4.5F : 9F;
                double r = weave ? .9 : 1.8, a = Math.toRadians(s.angle);
                var spot = v.position().add(Math.cos(a) * r, 0, Math.sin(a) * r);
                if (pet.tickCount % 4 == 0 || nav.isDone()) nav.moveTo(spot.x, spot.y, spot.z, weave ? .8 : s.cat() ? 1.33 : 1.3);
            }
            case CHASE -> {
                if (pet.tickCount % 5 == 0 || nav.isDone()) nav.moveTo(v, 1.35);
                pet.getLookControl().setLookAt(v, 30, 30);
            }
            case FLEE -> {
                if (s.target == null) s.target = pet.position().add(horizontal(pet.position().subtract(v.position())).scale(5));
                if (pet.tickCount % 10 == 0 || nav.isDone()) nav.moveTo(s.target.x, s.target.y, s.target.z, 1.1);
            }
        }
    }
    private static double speed(Session s, Move move) {
        if (s.cat()) return move == Move.COAX ? .6 : .8;
        return move == Move.RETURN ? 1.3 : 1.0;
    }
    /** Just in front of the resident, on the side the pet is coming from. */
    private static Vec3 front(Session s, Move move) {
        double distance = s.cat() ? move == Move.LIE ? .85 : move == Move.COAX ? .8 : 1.0 : move == Move.SIT || move == Move.COAX ? 1.25 : 1.4;
        if (s.pet.isBaby()) distance -= .2;
        var dir = horizontal(s.pet.position().subtract(s.villager.position()));
        if (dir.lengthSqr() < 1e-4) dir = horizontal(s.villager.getLookAngle());
        return s.villager.position().add(dir.scale(distance));
    }
    private static double horizontal2(Vec3 a, Vec3 b) { double dx = a.x - b.x, dz = a.z - b.z; return dx * dx + dz * dz; }
    private static void face(LivingEntity e, Vec3 target, float step) {
        double dx = target.x - e.getX(), dz = target.z - e.getZ();
        if (dx * dx + dz * dz < 1e-4) return;
        float yaw = (float) (Mth.atan2(dz, dx) * Mth.RAD_TO_DEG) - 90F;
        float next = Mth.approachDegrees(e.getYRot(), yaw, step);
        e.setYRot(next); e.setYBodyRot(next);
    }

    /** Runs in place of the resident's brain while they play or befriend a stray. */
    public static boolean drive(Villager v, ServerLevel level) {
        var s = byVillager.get(v.getUUID());
        if (s == null) return false;
        var step = s.step(); var nav = v.getNavigation();
        if (step == null) { nav.stop(); return true; }
        switch (step.move()) {
            case APPROACH -> {
                if (v.tickCount % 10 == 0 || nav.isDone()) nav.moveTo(s.pet, .55);
                v.getLookControl().setLookAt(s.pet, 30, 30);
            }
            case CHASE -> {
                var wp = s.waypoints.get(Math.clamp(s.waypoint, 0, s.waypoints.size() - 1));
                if (v.tickCount % 10 == 0 || nav.isDone()) nav.moveTo(wp.x, wp.y, wp.z, .7);
            }
            default -> {
                nav.stop();
                v.getLookControl().setLookAt(s.pet, 30, 30);
                if (step.move() != Move.FETCH) face(v, s.pet.position(), 12);
            }
        }
        return true;
    }

    // -- players and pets --------------------------------------------------------------------------

    /** Right-clicking a resident's pet opens their card (sneak, a name tag or a lead still work the vanilla way). */
    public static InteractionResult interact(Player player, Level world, InteractionHand hand, Entity entity) {
        if (!(entity instanceof Cat || entity instanceof Wolf) || hand != InteractionHand.MAIN_HAND || player.isSpectator() || player.isShiftKeyDown()) return InteractionResult.PASS;
        var held = player.getMainHandItem();
        if (held.is(Items.NAME_TAG) || held.is(Items.LEAD)) return InteractionResult.PASS;
        var pet = (TamableAnimal) entity;
        if (world.isClientSide()) return pet.isTame() && pet.getOwner() instanceof Villager ? InteractionResult.SUCCESS : InteractionResult.PASS;
        var profile = profile(pet);
        if (profile == null || !(player instanceof ServerPlayer sp) || !ServerPlayNetworking.canSend(sp, PetPayload.TYPE)) return InteractionResult.PASS;
        if (!valid(sp, pet)) return InteractionResult.PASS;
        look(pet, sp, 100);
        show(sp, pet, PetKeeping.greeting(new Random(pet.getUUID().hashCode() * 31L + world.getGameTime() / 200), profile), status(pet, profile), true, null);
        return InteractionResult.SUCCESS_SERVER;
    }
    private static boolean valid(ServerPlayer p, Entity pet) { return p.isAlive() && !p.isSpectator() && pet.isAlive() && p.level() == pet.level() && p.distanceToSqr(pet) <= 36 && p.hasLineOfSight(pet); }
    private static void look(TamableAnimal pet, ServerPlayer p, int ticks) { attention.put(pet.getUUID(), new Attention(p.getUUID(), pet.level().getGameTime() + ticks)); }

    public static void handleAction(ServerPlayer player, PetActionPayload action) {
        var entity = player.level().getEntity(action.entityId());
        if (!(entity instanceof TamableAnimal pet) || !pet.getUUID().equals(action.petId()) || !valid(player, pet) || profile(pet) == null) {
            player.sendSystemMessage(Component.literal("Move a little closer to the pet."), true); return;
        }
        var level = (ServerLevel) player.level();
        var profile = profile(pet); long today = day(level);
        var fondness = profile.fondness(player.getUUID());
        var random = new Random(level.getGameTime() ^ pet.getUUID().getMostSignificantBits());
        look(pet, player, 100);
        switch (action.action()) {
            case "pat" -> {
                boolean first = fondness.patDay() != today;
                var next = first ? fondness.add(6).patted(today) : fondness;
                target(pet).setAttached(PROFILE, profile.fondness(player.getUUID(), next));
                react(pet, profile.cat() ? "lean" : random.nextInt(3) == 0 && !pet.isBaby() ? "belly_up" : "happy", 50);
                level.broadcastEntityEvent(pet, (byte) 7);
                if (profile.cat()) sound(pet, purr(pet), .8F); else if (random.nextBoolean()) pet.playAmbientSound();
                show(player, pet, PetKeeping.patLine(random, profile, first), first ? "+6 fondness. Come back tomorrow for more." : "Pats are always welcome.", false, Emote.HEART);
            }
            case "treat" -> {
                var held = player.getMainHandItem();
                boolean food = held.is(profile.cat() ? ItemTags.CAT_FOOD : ItemTags.WOLF_FOOD);
                if (!food) {
                    show(player, pet, PetKeeping.refusedLine(profile, held.isEmpty()), held.isEmpty() ? "Hold a treat in your main hand." : "Your item was kept.", false, Emote.QUESTION);
                    return;
                }
                String item = BuiltInRegistries.ITEM.getKey(held.getItem()).toString();
                boolean first = fondness.treatDay() != today;
                int gain = !first ? 0 : item.equals(profile.treat()) ? 15 : 10;
                var eaten = held.getItem();
                if (!player.getAbilities().instabuild) held.shrink(1);
                pet.heal(4);
                pet.playSound(SoundEvents.GENERIC_EAT.value(), .7F, 1.15F);
                level.sendParticles(new ItemParticleOption(ParticleTypes.ITEM, eaten),
                        pet.getX(), pet.getY() + pet.getBbHeight() * .7, pet.getZ(), 6, .12, .08, .12, .05);
                target(pet).setAttached(PROFILE, profile.fondness(player.getUUID(), first ? fondness.add(gain).treated(today) : fondness));
                react(pet, profile.cat() ? "tail_up" : "catch", 30);
                show(player, pet, PetKeeping.treatLine(profile, item, first), first ? "+" + gain + " fondness." : "Treat fondness returns tomorrow.", false,
                        item.equals(profile.treat()) ? Emote.SPARKLE : Emote.NOTE);
            }
            default -> show(player, pet, PetKeeping.greeting(random, profile), status(pet, profile), false, null);
        }
    }
    /** A short trick in answer to a player (only when the pet isn't busy playing). */
    private static void react(TamableAnimal pet, String trick, int ticks) {
        if (byPet.containsKey(pet.getUUID())) return;
        long now = pet.level().getGameTime();
        target(pet).setAttached(TRICK, trick + "@" + now);
        trickEnds.put(pet, now + ticks);
        if (trick.equals("catch") && pet.onGround()) pet.getJumpControl().jump();
    }

    /** What the pet is up to, for the bottom of their card. */
    private static String status(TamableAnimal pet, PetProfile profile) {
        var s = byPet.get(pet.getUUID());
        if (!profile.owned()) return s != null && s.taming ? "Being won over by " + name(s.villager) + "." : "Looking for a home.";
        String owner = profile.ownerName();
        if (s != null) return "Playing " + PetKeeping.gameLabel(s.game).toLowerCase(java.util.Locale.ROOT) + " with " + owner + ".";
        if (pet.getOwner() instanceof Villager v) {
            if (Knockouts.injured(v)) return "Keeping watch over " + owner + ".";
            if (v.isSleeping()) return "Napping by " + owner + "'s bed.";
            return pet.distanceToSqr(v) < 16 * 16 ? "Following " + owner + " around." : "Off exploring. " + owner + " is nearby.";
        }
        return "Waiting for " + owner + " to come back.";
    }

    static void show(ServerPlayer p, TamableAnimal pet, String line, String status, boolean opening, Emote emote) {
        if (p.connection == null || !ServerPlayNetworking.canSend(p, PetPayload.TYPE)) return;
        var profile = profile(pet);
        var level = (ServerLevel) pet.level();
        long today = day(level), age = Math.max(0, today - profile.born());
        String variant = pet instanceof Cat cat ? cat.getVariant().unwrapKey().map(k -> k.identifier().toString()).orElse("")
                : pet.get(DataComponents.WOLF_VARIANT) instanceof net.minecraft.core.Holder<?> h ? h.unwrapKey().map(k -> k.identifier().toString()).orElse("") : "";
        String owner, detail;
        if (profile.owned()) {
            owner = profile.ownerName();
            if (pet.getOwner() instanceof Villager v) {
                String job = profession(v);
                String label = v.isBaby() ? "Young villager" : job.equals("none") ? "Neighbor" : job.equals("nitwit") ? "Free spirit" : VillageProfessions.label(job);
                var town = VillageSettlements.home(v);
                detail = label + (town == null ? "" : " of " + town.name());
            } else detail = "";
        } else {
            owner = "No one yet";
            detail = profile.former().isEmpty() ? "A stray looking for a home" : "Once " + profile.former() + "'s " + profile.species();
        }
        long home = today - profile.adopted();
        String adopted = !profile.owned() ? "" : home <= 0 ? "Came home today" : home == 1 ? "Came home yesterday" : "Came home " + home + " days ago";
        int fondness = profile.fondness(p.getUUID()).points();
        ServerPlayNetworking.send(p, new PetPayload(pet.getId(), pet.getUUID(), profile.name(), profile.species(),
                PetKeeping.stage(profile.species(), pet.isBaby(), age), PetKeeping.breed(variant), PetKeeping.nature(profile.species(), profile.personality()).label(),
                owner, detail, PetKeeping.age(age), adopted, PetKeeping.gameLabel(profile.game()), PetKeeping.treatLabel(profile.treat()),
                line, status, fondness, PetKeeping.fondnessLabel(fondness), pet.getHealth(), pet.getMaxHealth(), opening,
                emote == null ? "" : emote.name(), ""));
    }

    /** Added to every cat and wolf: takes over movement while the pet plays, is befriended, greets a player or minds its resident. */
    static final class PetGoal extends Goal {
        private final TamableAnimal pet;
        PetGoal(TamableAnimal pet) { this.pet = pet; setFlags(EnumSet.of(Goal.Flag.MOVE, Goal.Flag.LOOK, Goal.Flag.JUMP)); }
        @Override public boolean canUse() { return !pet.level().isClientSide() && wanted(pet, false); }
        @Override public boolean canContinueToUse() { return wanted(pet, true); }
        @Override public boolean requiresUpdateEveryTick() { return true; }
        @Override public void tick() { steer(pet); }
        @Override public void stop() { stopped(pet); }
    }
    private VillagerPets() {}
}
