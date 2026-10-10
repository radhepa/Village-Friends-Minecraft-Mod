package dev.villagefriends;

import static dev.villagefriends.VillageFriends.target;

import dev.villagefriends.stable.api.Horses;
import dev.villagefriends.stable.api.Stables;
import dev.villagefriends.stable.data.HayTroughBlock;
import dev.villagefriends.stable.data.StableBlocks;
import dev.villagefriends.stable.data.StableData;
import dev.villagefriends.stable.data.StableItems;
import dev.villagefriends.stable.data.StableTags;
import dev.villagefriends.stable.yard.Papers;
import dev.villagefriends.stable.yard.Stalls;
import dev.villagefriends.stable.yard.YardFeature;
import java.util.List;
import java.util.UUID;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.entity.animal.equine.Donkey;
import net.minecraft.world.entity.animal.equine.Horse;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.block.Mirror;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.levelgen.structure.templatesystem.JigsawReplacementProcessor;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructurePlaceSettings;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.Vec3;

/**
 * {@link StablehandGameTest}'s yard scene: stalls, troughs, papers and the stable building. Written by the stables package.
 *
 * <ol>
 * <li>Stalls: ride your own horse to a Horse Stall and use it (its stall and vanilla home are set); lead a second horse
 * there (it takes the stall and the first moves out); ride the village's horse there (refused).</li>
 * <li>Troughs: wheat adds a serving, a hay bale fills it; a hurt stalled horse eats from it on the yard tick.</li>
 * <li>Papers: Courser papers bring a tame, grown Courser that is yours; donkey papers a donkey; the papers are used up.</li>
 * <li>The plains stable template: its three horses settle into its stalls as the village's horses of plains breeds,
 * its stablehand trades, and (soft, it needs work hours and a job site) tops up an empty trough.</li>
 * </ol>
 */
@SuppressWarnings("UnstableApiUsage")
final class StableYardScenes {
    static void run(ClientGameTestContext c, TestSingleplayerContext w, StableTestKit kit) {
        var o = kit.origin;
        BlockPos stall = o.offset(4, 0, -6), villageStall = o.offset(9, 0, -6), trough = o.offset(5, 0, -6);
        UUID[] ids = new UUID[3];
        w.getServer().runOnServer(s -> {
            var level = kit.level(); var p = kit.player();
            level.setBlock(stall, StableBlocks.HORSE_STALL.defaultBlockState(), 3);
            level.setBlock(villageStall, StableBlocks.HORSE_STALL.defaultBlockState(), 3);
            level.setBlock(trough, StableBlocks.HAY_TROUGH.defaultBlockState(), 3);
            ids[0] = kit.horse(level, Vec3.atBottomCenterOf(o.offset(2, 0, -2)), "destrier", p).getUUID();
            ids[1] = kit.horse(level, Vec3.atBottomCenterOf(o.offset(-2, 0, -2)), "palfrey", p).getUUID();
            var village = kit.horse(level, Vec3.atBottomCenterOf(o.offset(9, 0, -4)), "rouncey", null);
            Stables.stall(village, villageStall, "", "village");
            ids[2] = village.getUUID();
        });
        kit.check(kit.onServer(w, () -> kit.entity(w, ids[0]) instanceof Horse && kit.entity(w, ids[1]) instanceof Horse && kit.entity(w, ids[2]) instanceof Horse),
                "the three horses spawned");

        // -- 1. Ride your horse to the stall.
        kit.expect(kit.onServer(w, () -> {
            var p = kit.player(); var a = (AbstractHorse) kit.entity(w, ids[0]);
            p.startRiding(a, true, true);
            Stalls.use(p, kit.level(), stall);
            p.stopRiding();
            var home = Stables.stallOf(a).orElse(null);
            return home != null && home.stall().equals(stall) && home.keeper().equals(Stalls.keeper(p)) && a.hasHome() && a.getHomePosition().equals(stall);
        }), "riding your own horse to a stall stables it there, keeper player:<you>, vanilla home = the stall");

        // -- 2. Lead a second horse there: it takes the stall and the first moves out.
        kit.expect(kit.onServer(w, () -> {
            var p = kit.player(); var a = (AbstractHorse) kit.entity(w, ids[0]); var b = (AbstractHorse) kit.entity(w, ids[1]);
            b.setLeashedTo(p, true);
            Stalls.use(p, kit.level(), stall);
            b.dropLeash();
            return Stables.stallOf(b).map(h -> h.stall().equals(stall)).orElse(false) && Stables.stallOf(a).isEmpty() && !a.hasHome();
        }), "a led horse takes the stall and the horse living there moves out");

        // -- 3. The village's horse can't be re-stalled by a player.
        kit.expect(kit.onServer(w, () -> {
            var p = kit.player(); var v = (AbstractHorse) kit.entity(w, ids[2]); var b = (AbstractHorse) kit.entity(w, ids[1]);
            p.startRiding(v, true, true);
            Stalls.use(p, kit.level(), stall);
            p.stopRiding();
            return Stables.stallOf(v).map(h -> h.stall().equals(villageStall) && h.residentOwned()).orElse(false)
                    && Stables.stallOf(b).map(h -> h.stall().equals(stall)).orElse(false);
        }), "riding the village's horse to your stall changes nothing");

        // -- 4. Troughs: wheat, a hay bale, and a hurt horse eating on the yard tick.
        kit.expect(kit.onServer(w, () -> {
            var p = kit.player(); var level = kit.level();
            var hit = new BlockHitResult(Vec3.atCenterOf(trough).add(0, .4, 0), Direction.UP, trough, false);
            p.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.WHEAT, 3));
            level.getBlockState(trough).useItemOn(p.getMainHandItem(), level, p, InteractionHand.MAIN_HAND, hit);
            boolean one = level.getBlockState(trough).getValue(HayTroughBlock.HAY) == 1 && p.getMainHandItem().getCount() == 2;
            p.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.HAY_BLOCK));
            level.getBlockState(trough).useItemOn(p.getMainHandItem(), level, p, InteractionHand.MAIN_HAND, hit);
            p.setItemInHand(InteractionHand.MAIN_HAND, ItemStack.EMPTY);
            return one && level.getBlockState(trough).getValue(HayTroughBlock.HAY) == 4;
        }), "wheat adds one serving to the trough and a hay bale fills it to four");
        float[] health = new float[2];
        w.getServer().runOnServer(s -> {
            var b = (AbstractHorse) kit.entity(w, ids[1]);
            b.setHealth(b.getMaxHealth() - 6);
            health[0] = b.getHealth();
            YardFeature.yardTick(kit.level());
            health[1] = b.getHealth();
        });
        kit.expect(health[1] >= health[0] + 2, "a hurt stalled horse eats from the trough beside its stall: " + health[0] + " -> " + health[1]);
        kit.expect(kit.onServer(w, () -> kit.level().getBlockState(trough).getValue(HayTroughBlock.HAY) >= 3), "one meal takes at most one serving");

        // -- 5. Horse Papers.
        BlockPos ground = o.offset(-8, -1, 4), ground2 = o.offset(-12, -1, 4);
        kit.expect(kit.onServer(w, () -> {
            var p = kit.player(); var level = kit.level();
            p.setItemInHand(InteractionHand.MAIN_HAND, StableItems.papers("courser"));
            var used = Papers.use(p, level, new BlockHitResult(Vec3.atCenterOf(ground).add(0, .5, 0), Direction.UP, ground, false), p.getMainHandItem());
            var horses = level.getEntitiesOfClass(Horse.class, new AABB(ground.above()).inflate(2));
            return used.consumesAction() && p.getMainHandItem().isEmpty() && horses.size() == 1 && horses.getFirst().isTamed() && !horses.getFirst().isBaby()
                    && horses.getFirst().getOwnerReference() != null && horses.getFirst().getOwnerReference().getUUID().equals(p.getUUID())
                    && Horses.breed(horses.getFirst()).orElse("").equals("courser");
        }), "Courser papers bring one tame, grown Courser that is yours, and are used up");
        kit.expect(kit.onServer(w, () -> {
            var p = kit.player(); var level = kit.level();
            p.setItemInHand(InteractionHand.MAIN_HAND, StableItems.papers("donkey"));
            Papers.use(p, level, new BlockHitResult(Vec3.atCenterOf(ground2).add(0, .5, 0), Direction.UP, ground2, false), p.getMainHandItem());
            p.setItemInHand(InteractionHand.MAIN_HAND, ItemStack.EMPTY);
            return level.getEntitiesOfClass(Donkey.class, new AABB(ground2.above()).inflate(2), d -> d.isTamed()).size() == 1;
        }), "donkey papers bring a tame donkey");
        kit.view(c, w, Vec3.atBottomCenterOf(o.offset(-2, 0, -12)), 0, 20, "yard-stalls");

        // -- 6. The plains stable: horses settle, the stablehand trades.
        BlockPos corner = o.offset(-7, -1, 6);
        int[] size = w.getServer().computeOnServer(s -> {
            var level = kit.level();
            var template = level.getStructureTemplateManager().get(VillageBlocks.id("village/stable")).orElseThrow();
            template.placeInWorld(level, corner, corner, new StructurePlaceSettings().setRotation(Rotation.NONE).setMirror(Mirror.NONE)
                    .setIgnoreEntities(false).setFinalizeEntities(true).setKnownShape(true).addProcessor(JigsawReplacementProcessor.INSTANCE), level.getRandom(), 18);
            return new int[]{template.getSize().getX(), template.getSize().getY(), template.getSize().getZ()};
        });
        var box = new AABB(Vec3.atLowerCornerOf(corner), Vec3.atLowerCornerOf(corner.offset(size[0], size[1], size[2])));
        kit.until(c, () -> kit.onServer(w, () -> settled(kit.level(), box).size() == 3), 200,
                () -> "the stable's three horses settle: " + kit.onServer(w, () -> { describe(kit.level(), box); return true; }));
        kit.expect(kit.onServer(w, () -> settled(kit.level(), box).stream().allMatch(h -> {
            var home = Stables.stallOf(h).orElseThrow();
            return home.keeper().equals("village") && h.isTamed() && !h.entityTags().contains(StableTags.STABLE_HORSE)
                    && kit.level().getBlockState(home.stall()).is(StableBlocks.HORSE_STALL)
                    && Horses.breed(h).map(b -> List.of("destrier", "palfrey", "courser", "rouncey", "draft").contains(b)).orElse(false);
        })), "each stable horse is the village's, tame, untagged, in its own Horse Stall, and a plains breed");
        kit.expect(kit.onServer(w, () -> settled(kit.level(), box).stream().map(h -> Stables.stallOf(h).orElseThrow().stall()).distinct().count() == 3),
                "the three horses took three different stalls");
        kit.expect(kit.onServer(w, () -> {
            var hands = kit.level().getEntitiesOfClass(Villager.class, box, v -> VillageFriends.profession(v).equals("stablehand"));
            return hands.size() == 1 && !hands.getFirst().getOffers().isEmpty() && hands.getFirst().getOffers().stream().noneMatch(offer -> offer.getResult().isEmpty());
        }), "the stable has a stablehand with real trades");
        kit.view(c, w, Vec3.atBottomCenterOf(corner.offset(7, 1, -8)), 0, 15, "yard-stable");

        // -- 7. The stablehand's work (soft: it needs work hours, a working day and the rack as their job site).
        BlockPos[] empty = new BlockPos[1];
        w.getServer().runOnServer(s -> {
            var level = kit.level();
            for (var p : BlockPos.betweenClosed(corner, corner.offset(size[0], size[1], size[2])))
                if (empty[0] == null && level.getBlockState(p).is(StableBlocks.HAY_TROUGH)) {
                    empty[0] = p.immutable();
                    level.setBlock(p, level.getBlockState(p).setValue(HayTroughBlock.HAY, 0), 3);
                }
        });
        kit.check(empty[0] != null, "the stable has hay troughs");
        w.getServer().runCommand("time set 8000");
        boolean refilled = false;
        for (int i = 0; i < 40 && !refilled; i++) {
            c.waitTicks(20);
            refilled = kit.onServer(w, () -> kit.level().getBlockState(empty[0]).getValue(HayTroughBlock.HAY) == 4);
        }
        kit.expect(refilled, "the stablehand tops up an empty trough during work hours");
        w.getServer().runCommand("time set 6000");
    }

    /** Settled stable horses inside the template's box. */
    private static List<AbstractHorse> settled(ServerLevel level, AABB box) {
        return level.getEntitiesOfClass(AbstractHorse.class, box.inflate(4), h -> h.isAlive() && target(h).hasAttached(StableData.STALL));
    }
    private static void describe(ServerLevel level, AABB box) {
        for (var h : level.getEntitiesOfClass(AbstractHorse.class, box.inflate(4)))
            System.out.println("[stablehand] " + h.getUUID() + " tags=" + h.entityTags() + " stall=" + target(h).getAttached(StableData.STALL));
    }

    private StableYardScenes() {}
}
