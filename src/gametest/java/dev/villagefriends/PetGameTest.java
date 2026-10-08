package dev.villagefriends;

import dev.villagefriends.client.PetPoser;
import dev.villagefriends.client.PetScreen;
import dev.villagefriends.client.ResidentLife;
import dev.villagefriends.pet.PetKeeping;
import dev.villagefriends.pet.VillagerPets;
import java.util.Random;
import java.util.UUID;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.TamableAnimal;
import net.minecraft.world.entity.animal.feline.Cat;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.phys.Vec3;

/**
 * Residents' pets: befriending a stray dog and a stray cat, playing fetch, belly rubs, string and strokes
 * (with the resident's clips and the pet's tricks on the client, and screenshots of each), the pet card,
 * pets keeping close to their resident, and a pet going back to being a stray when their resident dies.
 * Run with {@code gradlew runClientGameTest -Ptests=PetGameTest}.
 */
@SuppressWarnings("UnstableApiUsage")
public final class PetGameTest implements FabricClientGameTest {
    private static void check(boolean ok, String why) { if (!ok) throw new AssertionError(why); }
    private static Entity entity(TestSingleplayerContext w, UUID id) { return w.getConnection().getServerLevel().getEntity(id); }

    /** A resident whose heart is set on a cat or a dog (residents' wishes are fixed by who they are). */
    private static Villager resident(ServerLevel level, Vec3 at, String wish) {
        var random = new Random(wish.hashCode());
        UUID id;
        do id = new UUID(random.nextLong(), random.nextLong());
        while (!PetKeeping.wish(id, ResidentProfile.generate(id, "").personality(), false).equals(wish));
        var v = new Villager(EntityTypes.VILLAGER, level);
        v.setUUID(id);
        v.setPos(at.x, at.y, at.z);
        level.addFreshEntity(v);
        return v;
    }
    private static TamableAnimal stray(ServerLevel level, Vec3 at, boolean cat) {
        TamableAnimal animal = cat ? EntityTypes.CAT.create(level, EntitySpawnReason.COMMAND) : EntityTypes.WOLF.create(level, EntitySpawnReason.COMMAND);
        animal.snapTo(at.x, at.y, at.z, 0, 0);
        level.addFreshEntity(animal);
        return animal;
    }
    private static String trickOnClient(ClientGameTestContext c, int entityId) {
        return c.computeOnClient(client -> {
            var e = client.level.getEntity(entityId);
            if (!(e instanceof LivingEntity pet)) return "";
            var state = client.getEntityRenderDispatcher().getRenderer(pet).createRenderState(pet, 1);
            var pose = state.getData(PetPoser.POSE);
            return pose == null || pose.trick() == null ? "" : pose.trick().id();
        });
    }
    private static String clipOnClient(ClientGameTestContext c, int villagerId) {
        return c.computeOnClient(client -> client.level.getEntity(villagerId) instanceof Villager v && ResidentLife.of(v).activity() != null
                ? ResidentLife.of(v).activity().id() : "");
    }
    /** Polls from the test thread (never from inside a client or server callback). */
    private static void until(ClientGameTestContext c, java.util.function.BooleanSupplier test, int ticks, String what) {
        until(c, test, ticks, () -> what);
    }
    private static void until(ClientGameTestContext c, java.util.function.BooleanSupplier test, int ticks, java.util.function.Supplier<String> what) {
        for (int i = 0; i < ticks; i++) { if (test.getAsBoolean()) return; c.waitTicks(1); }
        if (!test.getAsBoolean()) throw new AssertionError("Timed out: " + what.get());
    }
    private static boolean onServer(TestSingleplayerContext w, java.util.function.Supplier<Boolean> test) { return w.getServer().computeOnServer(s -> test.get()); }
    private static void finished(ClientGameTestContext c, TestSingleplayerContext w, UUID pet) {
        until(c, () -> onServer(w, () -> VillagerPets.game(entity(w, pet)) == null), 700, "the game ends");
    }
    /** Turns the camera toward an entity. */
    private static void aim(ClientGameTestContext c, int entityId) {
        float[] look = c.computeOnClient(client -> {
            var e = client.level.getEntity(entityId); var p = client.player;
            double dx = e.getX() - p.getX(), dz = e.getZ() - p.getZ(), dy = e.getY() + .4 - p.getEyeY();
            return new float[] {(float) Math.toDegrees(Math.atan2(-dx, dz)), (float) -Math.toDegrees(Math.atan2(dy, Math.sqrt(dx * dx + dz * dz)))};
        });
        c.getInput().lookAt(look[0], look[1]);
    }
    /** Waits for the pet to strike this trick, then takes a picture. */
    private static void snap(ClientGameTestContext c, int petId, String trick, String picture, int within) {
        until(c, () -> trickOnClient(c, petId).equals(trick), within, "the " + trick + " trick");
        c.waitTicks(6);
        c.takeScreenshot(picture);
    }

    @Override public void runTest(ClientGameTestContext c) {
        try (var w = c.worldBuilder().create()) {
            w.getConnection().waitForChunksRender();
            w.getServer().runCommand("gamemode survival @a"); w.getServer().runCommand("difficulty peaceful");
            w.getServer().runCommand("gamerule advance_time false"); w.getServer().runCommand("gamerule spawn_mobs false");
            w.getServer().runCommand("time set 6000");
            Vec3 base = w.getServer().computeOnServer(s -> {
                var p = w.getConnection().getServerPlayer(); var level = w.getConnection().getServerLevel();
                var origin = p.blockPosition().above(4);
                for (int x = -30; x <= 30; x++) for (int z = -30; z <= 30; z++) {
                    level.setBlock(origin.offset(x, -1, z), Blocks.GRASS_BLOCK.defaultBlockState(), 3);
                    for (int y = 0; y < 5; y++) level.setBlock(origin.offset(x, y, z), Blocks.AIR.defaultBlockState(), 3);
                }
                p.teleportTo(origin.getX() + .5, origin.getY(), origin.getZ() - 4.5);
                p.addEffect(new MobEffectInstance(MobEffects.RESISTANCE, 100000, 4, false, false));
                return Vec3.atBottomCenterOf(origin);
            });
            c.getInput().lookAt(0, 25);

            // --- A resident who wants a dog befriends a stray.
            UUID[] ids = w.getServer().computeOnServer(s -> {
                var level = w.getConnection().getServerLevel();
                var v = resident(level, base.add(0, 0, 2), PetKeeping.DOG);
                var wolf = stray(level, base.add(4, 0, 4), false);
                return new UUID[] {v.getUUID(), wolf.getUUID()};
            });
            c.waitTicks(10);
            w.getServer().runOnServer(s -> VillagerPets.befriend((Villager) entity(w, ids[0]), (TamableAnimal) entity(w, ids[1]), true));
            int villagerId = w.getServer().computeOnServer(s -> entity(w, ids[0]).getId());
            int dogId = w.getServer().computeOnServer(s -> entity(w, ids[1]).getId());
            until(c, () -> clipOnClient(c, villagerId).endsWith("pet_coax"), 400, () -> "the resident coaxing the stray ("
                    + w.getServer().computeOnServer(s -> VillagerPets.describe((Villager) entity(w, ids[0]))) + "; client clip " + clipOnClient(c, villagerId)
                    + ", play " + c.computeOnClient(client -> String.valueOf(((net.fabricmc.fabric.api.attachment.v1.AttachmentTarget) client.level.getEntity(villagerId)).getAttached(VillagerPets.PLAY))) + ")");
            c.waitTicks(20); c.takeScreenshot("pets-coax-dog");
            until(c, () -> onServer(w, () -> ((TamableAnimal) entity(w, ids[1])).isTame()), 200, "the dog is tamed");
            w.getServer().runOnServer(s -> {
                var v = (Villager) entity(w, ids[0]); var dog = (TamableAnimal) entity(w, ids[1]);
                check(dog.getOwner() == v, "The dog belongs to the resident the vanilla way");
                var profile = VillagerPets.profile(dog);
                check(profile != null && profile.owned() && profile.species().equals("dog"), "The dog has a profile");
                check(dog.hasCustomName() && dog.getCustomName().getString().equals(profile.name()), "The resident named the dog");
                check(VillagerPets.link(v) != null && VillagerPets.link(v).pet().equals(dog.getUUID().toString()), "The resident remembers their dog");
                check(VillagerPets.petLine(v).startsWith("Pet: " + profile.name()), "Their conversation card mentions the dog");
            });
            c.waitTicks(40);

            // --- Fetch: the resident throws, the dog brings the stick back in its mouth.
            w.getServer().runOnServer(s -> w.getConnection().getServerPlayer().teleportTo(base.x + 6, base.y, base.z - 3));
            c.getInput().lookAt(45, 30);
            w.getServer().runOnServer(s -> VillagerPets.play((Villager) entity(w, ids[0]), (TamableAnimal) entity(w, ids[1]), "fetch"));
            snap(c, dogId, "play_bow", "pets-fetch-ready", 100);
            until(c, () -> clipOnClient(c, villagerId).endsWith("pet_throw") || clipOnClient(c, villagerId).endsWith("pet_watch"), 100, "the throw");
            c.takeScreenshot("pets-fetch-throw");
            until(c, () -> trickOnClient(c, dogId).equals("carry"), 300, "the dog carrying the stick back");
            w.getServer().runOnServer(s -> { var dog = entity(w, ids[1]); w.getConnection().getServerPlayer().teleportTo(dog.getX() + 2.5, dog.getY(), dog.getZ() + 2.5); });
            c.waitTicks(3); aim(c, dogId); c.waitTicks(3);
            check(c.computeOnClient(client -> { var dog = (LivingEntity) client.level.getEntity(dogId);
                var item = client.getEntityRenderDispatcher().getRenderer(dog).createRenderState(dog, 1).getData(PetPoser.CARRIED);
                return item != null && !item.isEmpty(); }), "The dog has the stick in its mouth");
            c.takeScreenshot("pets-fetch-carry");
            finished(c, w, ids[1]);

            // --- Belly rubs and a paw to shake.
            w.getServer().runOnServer(s -> VillagerPets.play((Villager) entity(w, ids[0]), (TamableAnimal) entity(w, ids[1]), "belly_rub"));
            snap(c, dogId, "belly_up", "pets-belly-rub", 200);
            c.waitTicks(30); c.takeScreenshot("pets-belly-rub-2");
            finished(c, w, ids[1]);
            w.getServer().runOnServer(s -> VillagerPets.play((Villager) entity(w, ids[0]), (TamableAnimal) entity(w, ids[1]), "shake_paw"));
            snap(c, dogId, "paw", "pets-shake-paw", 200);
            finished(c, w, ids[1]);

            // --- The pet card.
            w.getServer().runOnServer(s -> w.getConnection().getServerPlayer().teleportTo(base.x + 2, base.y, base.z - 1));
            c.waitTicks(10);
            c.runOnClient(client -> { var e = client.level.getEntity(dogId); client.gameMode.interact(client.player, e, new net.minecraft.world.phys.EntityHitResult(e), InteractionHand.MAIN_HAND); });
            c.waitFor(client -> client.gui.screen() instanceof PetScreen, 60);
            c.waitTicks(40); c.takeScreenshot("pets-card-dog");
            c.runOnClient(client -> { if (client.gui.screen() != null) client.gui.screen().onClose(); });
            c.waitTicks(5);

            // --- A resident who wants a cat befriends one too, and they play.
            UUID[] cats = w.getServer().computeOnServer(s -> {
                var level = w.getConnection().getServerLevel();
                var v = resident(level, base.add(-5, 0, 3), PetKeeping.CAT);
                var cat = stray(level, base.add(-8, 0, 6), true);
                return new UUID[] {v.getUUID(), cat.getUUID()};
            });
            c.waitTicks(10);
            w.getServer().runOnServer(s -> VillagerPets.befriend((Villager) entity(w, cats[0]), (TamableAnimal) entity(w, cats[1]), true));
            int catId = w.getServer().computeOnServer(s -> entity(w, cats[1]).getId());
            // Watch the cat scene from the side, out of everyone's way.
            w.getServer().runOnServer(s -> w.getConnection().getServerPlayer().teleportTo(base.x - 12, base.y, base.z + 4.5));
            c.getInput().lookAt(-90, 25);
            until(c, () -> onServer(w, () -> ((TamableAnimal) entity(w, cats[1])).isTame()), 500, "the cat is tamed");
            c.waitTicks(40);
            w.getServer().runOnServer(s -> VillagerPets.play((Villager) entity(w, cats[0]), (TamableAnimal) entity(w, cats[1]), "string"));
            snap(c, catId, "bat", "pets-cat-string", 200);
            finished(c, w, cats[1]);
            w.getServer().runOnServer(s -> VillagerPets.play((Villager) entity(w, cats[0]), (TamableAnimal) entity(w, cats[1]), "stroke"));
            until(c, () -> c.computeOnClient(client -> client.level.getEntity(catId) instanceof Cat cat && cat.isLying()), 200, "the cat lies down");
            c.waitTicks(30); c.takeScreenshot("pets-cat-stroke");
            finished(c, w, cats[1]);
            w.getServer().runOnServer(s -> VillagerPets.play((Villager) entity(w, cats[0]), (TamableAnimal) entity(w, cats[1]), "feather"));
            snap(c, catId, "pounce", "pets-cat-pounce", 300);
            finished(c, w, cats[1]);

            // --- Pets keep close: a dog left behind catches up with their resident.
            w.getServer().runOnServer(s -> entity(w, ids[0]).teleportTo(base.x + 11, base.y, base.z + 2));
            c.waitTicks(120);
            w.getServer().runOnServer(s -> check(entity(w, ids[1]).distanceTo(entity(w, ids[0])) < 6, "The dog caught up with their resident"));

            // --- A pet whose resident dies is a stray again, remembering them.
            w.getServer().runOnServer(s -> entity(w, cats[0]).kill(w.getConnection().getServerLevel()));
            c.waitTicks(5);
            w.getServer().runOnServer(s -> {
                var cat = (TamableAnimal) entity(w, cats[1]); var profile = VillagerPets.profile(cat);
                check(!cat.isTame() && profile != null && !profile.owned() && !profile.former().isEmpty(), "The cat is a stray again and remembers their resident");
            });
        }
    }
}
