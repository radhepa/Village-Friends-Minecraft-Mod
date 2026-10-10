package dev.villagefriends;

import static dev.villagefriends.VillageFriends.target;

import dev.villagefriends.stable.api.Horses;
import dev.villagefriends.stable.api.PackAnimals;
import dev.villagefriends.stable.api.StablehandEvents;
import dev.villagefriends.stable.data.HorseBond;
import dev.villagefriends.stable.data.StableData;
import dev.villagefriends.stable.data.StableItems;
import dev.villagefriends.stable.data.StableTable;
import dev.villagefriends.stable.gear.ArcheryMath;
import dev.villagefriends.stable.gear.CombatHooks;
import dev.villagefriends.stable.gear.LanceMath;
import dev.villagefriends.stable.gear.PackHooks;
import dev.villagefriends.stable.gear.Tack;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicReference;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.minecraft.core.BlockPos;
import net.minecraft.core.component.DataComponents;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.ProblemReporter;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.entity.animal.equine.Horse;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.component.DyedItemColor;
import net.minecraft.world.level.storage.TagValueInput;
import net.minecraft.world.level.storage.TagValueOutput;
import net.minecraft.world.phys.Vec3;

/**
 * {@link StablehandGameTest}'s gear scene: tack, barding, pack slots, pack animals and the lance. Written by the gear
 * package. Every outcome is a soft {@code expect}, so one run reports all of them; only "the animal spawned" style
 * preconditions are hard checks. Screenshots: {@code stablehand-gear-lineup}, {@code stablehand-gear-caparison-blue}
 * and {@code stablehand-gear-lance}.
 */
@SuppressWarnings("UnstableApiUsage")
final class StableGearScenes {
    /** The last couched hit Village Friends reported (LANCE_HIT): the damage, or null. Listeners can't be removed, so one is registered once. */
    private static final AtomicReference<Float> LANCE_HIT = new AtomicReference<>();
    private static boolean listening;

    static void run(ClientGameTestContext c, TestSingleplayerContext w, StableTestKit kit) {
        if (!listening) { StablehandEvents.LANCE_HIT.register((p, target, damage, speed) -> LANCE_HIT.set(damage)); listening = true; }
        tackAndBarding(c, w, kit);
        sameTickResize(c, w, kit);
        packAnimals(c, w, kit);
        lineup(c, w, kit);
        lanceAndArchery(c, w, kit);
    }

    private static Item gear(String id) { return StableItems.get(id); }
    private static Vec3 at(StableTestKit kit, int x, int z) { return Vec3.atBottomCenterOf(kit.origin.offset(x, 0, z)); }

    /** Plate barding and saddlebags on one horse: armor, two pack columns, and the pack surviving a save and load. */
    private static void tackAndBarding(ClientGameTestContext c, TestSingleplayerContext w, StableTestKit kit) {
        UUID id = w.getServer().computeOnServer(s -> {
            var horse = kit.horse(kit.level(), at(kit, 3, 0), "destrier", kit.player());
            horse.setItemSlot(EquipmentSlot.BODY, new ItemStack(gear("plate_barding")));
            horse.setItemSlot(EquipmentSlot.SADDLE, new ItemStack(gear("saddlebags")));
            return horse.getUUID();
        });
        c.waitTicks(5);
        kit.expect(kit.onServer(w, () -> kit.entity(w, id) instanceof Horse h && h.getArmorValue() >= 10), "plate barding gives at least 10 armor");
        kit.expect(kit.onServer(w, () -> kit.entity(w, id) instanceof Horse h && h.getInventoryColumns() == 2 && h.isSaddled()),
                "saddlebags give 2 pack columns and count as a saddle");
        String round = w.getServer().computeOnServer(s -> {
            if (!(kit.entity(w, id) instanceof Horse h)) return "the horse is gone";
            var pack = PackHooks.inventory(h);
            if (pack == null || pack.getContainerSize() != 6) return "pack size " + (pack == null ? -1 : pack.getContainerSize());
            pack.setItem(0, new ItemStack(Items.WHEAT, 32));
            pack.setItem(5, new ItemStack(Items.APPLE, 3));
            var level = kit.level();
            var out = TagValueOutput.createWithContext(ProblemReporter.DISCARDING, level.registryAccess());
            h.saveWithoutId(out);
            var copy = EntityTypes.HORSE.create(level, EntitySpawnReason.LOAD);
            if (copy == null) return "no copy";
            copy.load(TagValueInput.create(ProblemReporter.DISCARDING, level.registryAccess(), out.buildResult()));
            var loaded = PackHooks.inventory(copy);
            if (loaded == null || loaded.getContainerSize() != 6) return "loaded pack size " + (loaded == null ? -1 : loaded.getContainerSize());
            boolean ok = loaded.getItem(0).is(Items.WHEAT) && loaded.getItem(0).getCount() == 32 && loaded.getItem(5).is(Items.APPLE) && loaded.getItem(5).getCount() == 3;
            copy.discard();
            return ok ? "" : "loaded " + loaded.getItem(0) + " / " + loaded.getItem(5);
        });
        kit.expect(round.isEmpty(), "the saddlebags' pack survives a save and load: " + round);
    }

    /** Saddling and filling in one server task, then swapping to a plain saddle spills the pack at once. */
    private static void sameTickResize(ClientGameTestContext c, TestSingleplayerContext w, StableTestKit kit) {
        var result = new ArrayList<String>();
        UUID id = w.getServer().computeOnServer(s -> {
            var h = kit.horse(kit.level(), at(kit, -3, 0), "palfrey", kit.player());
            h.setItemSlot(EquipmentSlot.SADDLE, new ItemStack(gear("saddlebags")));
            var pack = PackHooks.inventory(h);
            try {
                pack.setItem(0, new ItemStack(Items.BREAD, 4));
                pack.setItem(5, new ItemStack(Items.CARROT, 7));
            } catch (RuntimeException e) { result.add("filling threw " + e); }
            if (pack.getContainerSize() != 6 || !pack.getItem(0).is(Items.BREAD) || !pack.getItem(5).is(Items.CARROT)) result.add("not stored, size " + pack.getContainerSize());
            h.setItemSlot(EquipmentSlot.SADDLE, new ItemStack(Items.SADDLE));
            if (PackHooks.inventory(h).getContainerSize() != 0) result.add("a plain saddle left " + PackHooks.inventory(h).getContainerSize() + " slots");
            return h.getUUID();
        });
        kit.expect(result.isEmpty(), "same-tick resize: " + result);
        c.waitTicks(3);
        kit.expect(kit.onServer(w, () -> {
            var h = kit.entity(w, id);
            if (h == null) return false;
            var drops = kit.level().getEntitiesOfClass(ItemEntity.class, h.getBoundingBox().inflate(3));
            return drops.stream().anyMatch(e -> e.getItem().is(Items.BREAD) && e.getItem().getCount() == 4)
                    && drops.stream().anyMatch(e -> e.getItem().is(Items.CARROT) && e.getItem().getCount() == 7);
        }), "the spilled bread and carrots lie at the horse's feet");
    }

    /** A pack-saddled donkey, a mule fitted and loaded in the same call, the spawners, and a pack saved without a chest. */
    private static void packAnimals(ClientGameTestContext c, TestSingleplayerContext w, StableTestKit kit) {
        var problems = w.getServer().computeOnServer(s -> {
            var out = new ArrayList<String>();
            ServerLevel level = kit.level();
            var donkey = EntityTypes.DONKEY.create(level, EntitySpawnReason.COMMAND);
            kit.check(donkey != null, "a donkey could be created");
            donkey.snapTo(at(kit, 6, 4).x, at(kit, 6, 4).y, at(kit, 6, 4).z, 0, 0);
            donkey.setTamed(true);
            level.addFreshEntity(donkey);
            donkey.setItemSlot(EquipmentSlot.SADDLE, new ItemStack(gear("pack_saddle")));
            if (donkey.getInventoryColumns() != 5 || PackAnimals.capacity(donkey) != 15 || !PackAnimals.canCarry(donkey)) out.add("donkey columns " + donkey.getInventoryColumns());
            var goods = List.of(new ItemStack(Items.WHEAT, 64), new ItemStack(Items.WHEAT, 10), new ItemStack(Items.IRON_INGOT, 20));
            if (!PackAnimals.load(donkey, goods).isEmpty()) out.add("donkey refused goods");
            if (goods.get(0).getCount() != 64) out.add("load changed the caller's stacks");
            var inside = PackAnimals.contents(donkey);
            if (count(inside, Items.WHEAT) != 74 || count(inside, Items.IRON_INGOT) != 20) out.add("donkey holds " + inside);
            var unloaded = PackAnimals.unload(donkey);
            if (count(unloaded, Items.WHEAT) != 74 || !PackAnimals.contents(donkey).isEmpty()) out.add("unload gave " + unloaded);

            var mule = EntityTypes.MULE.create(level, EntitySpawnReason.COMMAND);
            kit.check(mule != null, "a mule could be created");
            mule.snapTo(at(kit, 9, 4).x, at(kit, 9, 4).y, at(kit, 9, 4).z, 0, 0);
            level.addFreshEntity(mule);
            var many = new ArrayList<ItemStack>();
            for (var item : List.of(Items.WHEAT, Items.CARROT, Items.POTATO, Items.BEETROOT, Items.APPLE, Items.BREAD, Items.COAL, Items.IRON_INGOT,
                    Items.GOLD_INGOT, Items.COPPER_INGOT, Items.LEATHER, Items.STRING, Items.FEATHER, Items.FLINT, Items.PAPER, Items.BOOK))
                many.add(new ItemStack(item, 16));
            boolean fitted = PackAnimals.fitPackSaddle(mule);
            var left = PackAnimals.load(mule, many);
            if (!fitted || !mule.isTamed() || !Tack.wears(mule, "pack_saddle")) out.add("the mule was not fitted");
            if (left.size() != 1 || !left.getFirst().is(Items.BOOK)) out.add("16 kinds into 15 slots left " + left);
            var saved = TagValueOutput.createWithContext(ProblemReporter.DISCARDING, level.registryAccess());
            mule.saveWithoutId(saved);
            var copy = EntityTypes.MULE.create(level, EntitySpawnReason.LOAD);
            copy.load(TagValueInput.create(ProblemReporter.DISCARDING, level.registryAccess(), saved.buildResult()));
            if (PackAnimals.contents(copy).size() != 15) out.add("a chestless mule's pack after a reload: " + PackAnimals.contents(copy).size());
            copy.discard();

            var spawned = PackAnimals.spawnPackAnimal(level, kit.origin.offset(12, 0, 4), "mule");
            if (spawned == null || !Tack.wears(spawned, "pack_saddle") || PackAnimals.capacity(spawned) != 15 || !PackAnimals.canCarry(spawned) || spawned.isBaby())
                out.add("spawnPackAnimal gave " + spawned);
            if (PackAnimals.spawnPackAnimal(level, kit.origin, "camel") != null) out.add("spawnPackAnimal made a camel");
            var horse = PackAnimals.spawnHorse(level, kit.origin.offset(12, 0, -4), "courser");
            if (horse == null || !horse.isTamed() || !horse.isSaddled() || horse.isBaby() || !Horses.breed(horse).orElse("").equals("courser"))
                out.add("spawnHorse gave " + horse);
            if (horse != null && PackAnimals.canCarry(horse)) out.add("a plain-saddled horse has no pack");
            return out;
        });
        kit.expect(problems.isEmpty(), "pack animals: " + problems);
    }

    /** Every barding tier and every piece of tack side by side, and a caparison dyed blue, for the screenshots. */
    private static void lineup(ClientGameTestContext c, TestSingleplayerContext w, StableTestKit kit) {
        w.getServer().runOnServer(s -> {
            var level = kit.level();
            String[][] row = {{"caparison", "saddlebags"}, {"leather_barding", "bridle"}, {"mail_barding", "saddlebags"}, {"plate_barding", ""}};
            for (int i = 0; i < row.length; i++) {
                var h = kit.horse(level, at(kit, -9 + i * 4, -10), "destrier", kit.player());
                h.setItemSlot(EquipmentSlot.BODY, new ItemStack(gear(row[i][0])));
                if (!row[i][1].isEmpty()) h.setItemSlot(EquipmentSlot.SADDLE, new ItemStack(gear(row[i][1])));
            }
            var blue = new ItemStack(gear("caparison"));
            blue.set(DataComponents.DYED_COLOR, new DyedItemColor(0x3C44AA));
            kit.horse(level, at(kit, 7, -10), "courser", kit.player()).setItemSlot(EquipmentSlot.BODY, blue);
            var pack = PackAnimals.spawnPackAnimal(level, kit.origin.offset(11, 0, -10), "donkey");
            if (pack != null) pack.setNoAi(true);
            for (var h : level.getEntitiesOfClass(AbstractHorse.class, new net.minecraft.world.phys.AABB(kit.origin).inflate(20))) {
                h.setNoAi(true); h.setYRot(90); h.setYBodyRot(90); h.setYHeadRot(90);
            }
        });
        c.waitTicks(10);
        kit.view(c, w, at(kit, 0, -2), 180, 15, "gear-lineup");
        kit.view(c, w, at(kit, 7, -6), 180, 25, "gear-caparison-blue");
        kit.expect(kit.onServer(w, () -> kit.level().getEntitiesOfClass(Horse.class, new net.minecraft.world.phys.AABB(kit.origin).inflate(20),
                h -> h.getBodyArmorItem().has(DataComponents.DYED_COLOR)).size() == 1), "the blue caparison is on its horse");
    }

    /**
     * The lance: first the hook on its own (a player on a Trusting horse, using the lance, gets exactly
     * {@code LanceMath.mounted}; on foot or not using it, nothing changes), and the bow hook for the same rider; then a
     * live charge at a gallop into a still husk, which may miss on a slow machine, so it is soft.
     */
    private static void lanceAndArchery(ClientGameTestContext c, TestSingleplayerContext w, StableTestKit kit) {
        kit.pad(w); // a clear run: the lineup and pack animals would stand in the lane
        var lance = StableTable.lance();
        float base = (float) LanceMath.vanilla(1, 12, lance.damageMultiplier());
        UUID horseId = w.getServer().computeOnServer(s -> {
            var p = kit.player();
            var h = kit.horse(kit.level(), at(kit, 0, -18), "courser", p);
            h.setItemSlot(EquipmentSlot.SADDLE, new ItemStack(Items.SADDLE));
            target(h).setAttached(StableData.BOND, new HorseBond(p.getUUID().toString(), 300, -1, 0, 0, 0, 0));
            p.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(StableItems.JOUSTING_LANCE));
            kit.check(p.startRiding(h), "the player mounted the courser");
            return h.getUUID();
        });
        c.waitTicks(5);
        String hooks = w.getServer().computeOnServer(s -> {
            var p = kit.player();
            var out = new ArrayList<String>();
            if (CombatHooks.stab(p, base) != base) out.add("a mounted stab without using the lance changed");
            p.startUsingItem(InteractionHand.MAIN_HAND);
            float want = LanceMath.mounted(base, 2, StablehandEvents.ridingBonus(p, StablehandEvents.Aspect.LANCE_DAMAGE));
            float got = CombatHooks.stab(p, base);
            if (Math.abs(got - want) > 1e-4) out.add("couched stab " + got + ", wanted " + want);
            var arrow = EntityTypes.ARROW.create(kit.level(), EntitySpawnReason.COMMAND);
            if (arrow != null) {
                arrow.setOwner(p);
                float aim = CombatHooks.aim(arrow, 1);
                if (Math.abs(aim - ArcheryMath.uncertainty(1, 2, StablehandEvents.ridingBonus(p, StablehandEvents.Aspect.MOUNTED_AIM))) > 1e-5) out.add("mounted aim " + aim);
                arrow.discard();
            }
            p.stopUsingItem();
            return String.join("; ", out);
        });
        kit.expect(hooks.isEmpty(), "lance and bow hooks: " + hooks);

        // The live charge: a still husk 20 blocks ahead, the rider holds forward and use.
        UUID huskId = w.getServer().computeOnServer(s -> {
            var husk = EntityTypes.HUSK.create(kit.level(), EntitySpawnReason.COMMAND);
            kit.check(husk != null, "a husk could be created");
            var spot = at(kit, 0, 2);
            husk.snapTo(spot.x, spot.y, spot.z, 180, 0);
            husk.setNoAi(true); husk.setPersistenceRequired();
            kit.level().addFreshEntity(husk);
            return husk.getUUID();
        });
        LANCE_HIT.set(null);
        c.getInput().lookAt(0, 5);
        c.getInput().holdKey(o -> o.keyUse);
        c.getInput().holdKey(o -> o.keyUp);
        float least = (float) LanceMath.vanilla(1, lance.damageThreshold(), lance.damageMultiplier());
        boolean hit = false;
        for (int t = 0; t < 140 && !hit; t++) {
            c.waitTicks(1);
            hit = kit.onServer(w, () -> !(kit.entity(w, huskId) instanceof LivingEntity husk) || husk.getHealth() <= husk.getMaxHealth() - least);
        }
        kit.view(c, w, "gear-lance");
        c.getInput().releaseKey(o -> o.keyUp);
        c.getInput().releaseKey(o -> o.keyUse);
        kit.expect(hit, "a galloping lance charge took at least " + least + " health off the husk");
        kit.expect(LANCE_HIT.get() != null, "LANCE_HIT fired for the charge");
        w.getServer().runOnServer(s -> { kit.player().stopRiding(); if (kit.entity(w, horseId) != null) kit.entity(w, horseId).discard(); });
    }

    private static int count(List<ItemStack> stacks, Item item) { return stacks.stream().filter(st -> st.is(item)).mapToInt(ItemStack::getCount).sum(); }

    private StableGearScenes() {}
}
