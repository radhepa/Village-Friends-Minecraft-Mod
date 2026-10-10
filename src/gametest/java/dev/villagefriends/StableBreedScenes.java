package dev.villagefriends;

import dev.villagefriends.stable.api.Horses;
import dev.villagefriends.stable.bond.BondMath;
import dev.villagefriends.stable.bond.Grooming;
import dev.villagefriends.stable.bond.Whistle;
import dev.villagefriends.stable.breed.Breeds;
import dev.villagefriends.stable.breed.Inheritance;
import dev.villagefriends.stable.client.breed.HorseCoats;
import dev.villagefriends.stable.data.StableItems;
import dev.villagefriends.stable.data.StableTable;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.UUID;
import java.util.function.BooleanSupplier;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.minecraft.client.renderer.entity.state.HorseRenderState;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.animal.equine.Horse;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;

/**
 * {@link StablehandGameTest}'s breeds scene: every coat loads, a new horse takes its biome's breed, a lineup of all
 * eight breeds (adults and foals) for the eye, a destrier x courser foal (breed, stats and its painted foal coat on the
 * client), then the bond: 500 points make a horse Loyal with its bonuses, a carrot from its owner counts, the whistle
 * calls it from 30 blocks (it walks) and from 60 (it is brought behind you), and one brush stroke grows the bond.
 * Written by the breeds package.
 */
@SuppressWarnings("UnstableApiUsage")
final class StableBreedScenes {
    /** The breeds a plains horse can be (the flat test world is plains). */
    private static final Set<String> PLAINS = Set.of("destrier", "palfrey", "courser", "rouncey", "draft");

    static void run(ClientGameTestContext c, TestSingleplayerContext w, StableTestKit kit) {
        var o = kit.origin;
        var server = w.getServer();

        // Every breed's coat is loaded on the client, adult and foal.
        var missing = c.computeOnClient(client -> {
            var out = new ArrayList<String>();
            for (var b : StableTable.breeds()) for (boolean baby : new boolean[]{false, true}) {
                var id = VillageBlocks.id(HorseCoats.path(b.id(), 0, baby));
                if (!HorseCoats.has(id)) out.add(id.toString());
            }
            return out;
        });
        kit.expect(missing.isEmpty(), "coat textures missing on the client: " + missing);

        // A horse that loads without a breed takes its biome's.
        UUID wild = server.computeOnServer(s -> {
            var horse = EntityTypes.HORSE.create(kit.level(), EntitySpawnReason.COMMAND);
            kit.check(horse != null, "a horse could be created");
            horse.snapTo(o.getX() - 6.5, o.getY(), o.getZ() + 6.5, 0, 0);
            kit.level().addFreshEntity(horse);
            return horse.getUUID();
        });
        kit.expect(soon(c, () -> kit.onServer(w, () -> kit.entity(w, wild) instanceof Horse h && Horses.breed(h).isPresent()), 40),
                "a new horse got a breed when it loaded");
        String wildBreed = server.computeOnServer(s -> kit.entity(w, wild) instanceof Horse h ? Horses.breed(h).orElse("none") : "gone");
        kit.expect(PLAINS.contains(wildBreed), "a plains horse is a plains breed, not " + wildBreed);

        // All eight breeds, adult and foal, standing still for a picture.
        List<UUID> lineup = server.computeOnServer(s -> {
            var ids = new ArrayList<UUID>();
            int x = -11;
            for (var b : StableTable.breeds()) {
                for (boolean baby : new boolean[]{false, true}) {
                    var horse = kit.horse(kit.level(), new Vec3(o.getX() + x + .5, o.getY(), o.getZ() + (baby ? 7.5 : 10.5)), b.id(), null);
                    if (baby) horse.setBaby(true);
                    horse.setNoAi(true);
                    horse.setYRot(90);
                    horse.setYHeadRot(90);
                    ids.add(horse.getUUID());
                }
                x += 3;
            }
            return ids;
        });
        kit.view(c, w, new Vec3(o.getX() + .5, o.getY() + 2.5, o.getZ() - 4), 0, 15, "breeds-lineup");
        server.runOnServer(s -> lineup.forEach(id -> { var e = kit.entity(w, id); if (e != null) e.discard(); }));
        server.runCommand("tp @a " + (o.getX() + .5) + " " + o.getY() + " " + (o.getZ() + .5));

        // A destrier and a courser of the player's, both in love: their foal is one of the two, bred inside its range.
        UUID[] parents = server.computeOnServer(s -> {
            var p = kit.player();
            var d = kit.horse(kit.level(), new Vec3(o.getX() + 3.5, o.getY(), o.getZ() + 4.5), "destrier", p);
            var cr = kit.horse(kit.level(), new Vec3(o.getX() + 5.5, o.getY(), o.getZ() + 4.5), "courser", p);
            d.setInLove(p);
            cr.setInLove(p);
            return new UUID[]{d.getUUID(), cr.getUUID()};
        });
        kit.until(c, () -> kit.onServer(w, () -> foal(kit) != null), 900, "the destrier and the courser had a foal");
        int foalId = server.computeOnServer(s -> {
            var foal = foal(kit);
            String breed = Horses.breed(foal).orElse("none");
            kit.expect(breed.equals("destrier") || breed.equals("courser"), "the foal is a destrier or a courser, not " + breed);
            var row = StableTable.breed(breed);
            if (row.isPresent()) {
                var stats = Breeds.stats(foal);
                kit.expect(inside(stats.health(), Inheritance.widened(row.get().health())), "foal health " + stats.health() + " fits a " + breed);
                kit.expect(inside(stats.speed(), Inheritance.widened(row.get().speed())), "foal speed " + stats.speed() + " fits a " + breed);
                kit.expect(inside(stats.jump(), Inheritance.widened(row.get().jump())), "foal jump " + stats.jump() + " fits a " + breed);
            }
            return foal.getId();
        });
        c.waitTicks(10);
        String coat = c.computeOnClient(client -> {
            if (!(client.level.getEntity(foalId) instanceof Horse foal)) return "no foal on the client";
            var state = client.getEntityRenderDispatcher().getRenderer(foal).createRenderState(foal, 1);
            if (!(state instanceof HorseRenderState horseState) || horseState.getData(HorseCoats.COAT) == null) return "no breed in the render state";
            var texture = HorseCoats.texture(horseState);
            return texture == null ? "no coat texture" : texture.toString();
        });
        kit.expect(coat.endsWith("_baby.png"), "the foal wears a painted foal coat: " + coat);
        kit.view(c, w, new Vec3(o.getX() + 4.5, o.getY() + 1.8, o.getZ() - 1.5), 0, 20, "breeds-foal");
        server.runCommand("tp @a " + (o.getX() + .5) + " " + o.getY() + " " + (o.getZ() + .5));

        // 500 bond points make the destrier Loyal, with its tier's bonuses.
        var destrier = parents[0];
        boolean loyal = server.computeOnServer(s -> {
            var d = (Horse) kit.entity(w, destrier);
            Horses.addBond(d, kit.player(), 500, "api");
            return Horses.bondTier(d) == BondMath.WHISTLE_TIER && d.getAttributeValue(Attributes.MOVEMENT_SPEED) > d.getAttributeBaseValue(Attributes.MOVEMENT_SPEED)
                    && Horses.bondPartner(d).filter(kit.player().getUUID()::equals).isPresent();
        });
        kit.expect(loyal, "500 bond points make a horse Loyal, faster and bonded to its owner");

        // A carrot from its owner counts when the horse really eats it (it is hungry for health here).
        int fed = server.computeOnServer(s -> {
            var p = kit.player();
            var palfrey = kit.horse(kit.level(), new Vec3(o.getX() - 3.5, o.getY(), o.getZ() + 3.5), "palfrey", p);
            palfrey.setHealth(palfrey.getMaxHealth() - 5);
            p.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.CARROT, 4));
            palfrey.mobInteract(p, InteractionHand.MAIN_HAND);
            int points = Horses.bondPoints(palfrey);
            palfrey.discard();
            return points;
        });
        kit.expect(fed == BondMath.FEED, "a carrot from its owner is worth " + BondMath.FEED + " bond points, got " + fed);

        // The whistle: from 30 blocks the destrier walks over; from 60 it is brought to a spot behind the player.
        server.runOnServer(s -> {
            var p = kit.player();
            kit.entity(w, destrier).teleportTo(p.getX() + 20, p.getY(), p.getZ() + 22);
        });
        c.waitTicks(5);
        boolean answered = server.computeOnServer(s -> {
            var p = kit.player();
            p.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(StableItems.HORSE_WHISTLE));
            var horse = Whistle.blow(p, p.getMainHandItem());
            return horse != null && horse.getUUID().equals(destrier) && Whistle.called(horse);
        });
        kit.expect(answered, "the Loyal destrier answers the whistle and sets off");
        kit.expect(soon(c, () -> kit.onServer(w, () -> kit.entity(w, destrier) != null && kit.entity(w, destrier).distanceTo(kit.player()) < 4), 500),
                "the whistled destrier came within 4 blocks");
        boolean fetched = server.computeOnServer(s -> {
            var p = kit.player();
            var d = kit.entity(w, destrier);
            d.teleportTo(p.getX() + 50, p.getY(), p.getZ() + 30);
            p.getCooldowns().removeCooldown(p.getCooldowns().getCooldownGroup(p.getMainHandItem()));
            return Whistle.blow(p, p.getMainHandItem()) != null && d.distanceTo(p) < 7.5;
        });
        kit.expect(fetched, "from 60 blocks away the destrier is brought to a spot behind the player");

        // One brush stroke grows the bond.
        int[] brushed = server.computeOnServer(s -> {
            var p = kit.player();
            var d = (Horse) kit.entity(w, destrier);
            p.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(StableItems.GROOMING_BRUSH));
            int before = Horses.bondPoints(d);
            Grooming.groom(p, d, InteractionHand.MAIN_HAND);
            return new int[]{before, Horses.bondPoints(d), p.getMainHandItem().getDamageValue()};
        });
        kit.expect(brushed[1] == brushed[0] + BondMath.GROOM_FIRST, "the day's first groom adds " + BondMath.GROOM_FIRST + ": " + brushed[0] + " -> " + brushed[1]);
        kit.expect(brushed[2] == 1, "the brush wears by one use");
        server.runOnServer(s -> kit.player().setItemInHand(InteractionHand.MAIN_HAND, ItemStack.EMPTY));
    }

    /** The first foal near the pad, on the server thread. */
    private static Horse foal(StableTestKit kit) {
        var foals = kit.level().getEntitiesOfClass(Horse.class, new AABB(kit.origin).inflate(StableTestKit.PAD, 8, StableTestKit.PAD), Horse::isBaby);
        return foals.isEmpty() ? null : foals.getFirst();
    }

    private static boolean inside(double v, StableTable.Range r) { return v >= r.min() - 1e-6 && v <= r.max() + 1e-6; }

    /** Polls a condition for up to {@code ticks}; false when it never came true (a soft wait, unlike {@code kit.until}). */
    private static boolean soon(ClientGameTestContext c, BooleanSupplier condition, int ticks) {
        for (int i = 0; i < ticks; i++) { if (condition.getAsBoolean()) return true; c.waitTicks(1); }
        return condition.getAsBoolean();
    }

    private StableBreedScenes() {}
}
