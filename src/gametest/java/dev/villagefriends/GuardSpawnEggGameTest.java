package dev.villagefriends;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.fabricmc.fabric.api.client.gametest.v1.world.TestWorldSave;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.SpawnEggItem;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.DispenserBlock;
import net.minecraft.world.level.block.entity.DispenserBlockEntity;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.Vec3;

/** Exercise the real spawn-egg and dispenser paths with the existing villager type. */
@SuppressWarnings("UnstableApiUsage")
public final class GuardSpawnEggGameTest implements FabricClientGameTest {
    private static void check(boolean ok, String reason) { if (!ok) throw new AssertionError(reason); }
    private static Villager at(TestSingleplayerContext world, BlockPos pos) {
        var found = world.getConnection().getServerLevel().getEntitiesOfClass(Villager.class, new AABB(pos).inflate(.5));
        check(found.size() == 1, "One ordinary villager spawned at " + pos);
        return found.getFirst();
    }
    private static void guard(Villager v, String job) {
        check(v.getType() == EntityTypes.VILLAGER && !v.isBaby() && !v.isNoAi(), "Egg makes an ordinary adult villager with AI");
        check(v.getVillagerData().profession().is(VillageProfessions.key(job)), "Egg chooses the full registered " + job + " profession");
        var progress = GuardProgression.progress(v);
        check(progress != null && progress.level() >= 15 && progress.level() <= 30 && progress.origin().equals("generated"), "Egg guard receives generated veteran levels");
        check(progress.xp() == 0 && progress.lockedProfession().isEmpty(), "Combat XP and first-kill lock remain separate");
        check(v.getHealth() == v.getMaxHealth() && v.getMaxHealth() > 20, "Generated guard begins at its full leveled health");
        check(v.getMainHandItem().is(job.equals("knight") ? Items.IRON_SWORD : Items.BOW), "Egg guard has its role weapon");
        int iron = 0, chain = 0;
        for (var slot : List.of(EquipmentSlot.HEAD, EquipmentSlot.CHEST, EquipmentSlot.LEGS, EquipmentSlot.FEET)) {
            var id = net.minecraft.core.registries.BuiltInRegistries.ITEM.getKey(v.getItemBySlot(slot).getItem()).getPath();
            if (id.startsWith("iron_")) iron++;
            if (id.startsWith("chainmail_")) chain++;
        }
        check(iron == 2 && chain == 2, "Egg guard receives the existing mixed armor policy");
    }
    @Override public void runTest(ClientGameTestContext context) {
        var ids = new ArrayList<UUID>();
        var levels = new ArrayList<Integer>();
        TestWorldSave saved;
        try (var world = context.worldBuilder().create()) {
            world.getConnection().waitForChunksDownload();
            world.getServer().runCommand("time set 2000");
            var origin = world.getServer().computeOnServer(server -> {
                var level = world.getConnection().getServerLevel();
                var p = world.getConnection().getServerPlayer();
                var base = p.blockPosition().above(4);
                for (int x = -12; x <= 12; x++) for (int z = -12; z <= 12; z++) {
                    level.setBlock(base.offset(x, -1, z), Blocks.STONE.defaultBlockState(), 3);
                    for (int y = 0; y < 3; y++) level.setBlock(base.offset(x, y, z), Blocks.AIR.defaultBlockState(), 3);
                }
                p.teleportTo(base.getX() + .5, base.getY(), base.getZ() + .5);
                return base;
            });
            for (int n = 0; n < 2; n++) {
                String job = n == 0 ? "knight" : "archer";
                boolean creative = n == 1;
                var pos = origin.offset(n * 12 - 6, 0, -4);
                world.getServer().runCommand("gamemode " + (creative ? "creative" : "survival") + " @a");
                world.getServer().runOnServer(server -> {
                    var p = world.getConnection().getServerPlayer();
                    var egg = new ItemStack(VillageItems.get(job + "_spawn_egg"), 2);
                    check(egg.getItem() instanceof SpawnEggItem && SpawnEggItem.spawnsEntity(egg, EntityTypes.VILLAGER), "Egg uses native villager spawning");
                    p.setItemInHand(InteractionHand.MAIN_HAND, egg);
                    var hit = new BlockHitResult(Vec3.atCenterOf(pos.below()).add(0, .5, 0), Direction.UP, pos.below(), false);
                    check(egg.useOn(new UseOnContext(p, InteractionHand.MAIN_HAND, hit)).consumesAction(), "Guard egg use succeeds");
                    check(egg.getCount() == (creative ? 2 : 1), "Native Creative/Survival egg accounting");
                    var v = at(world, pos); guard(v, job); ids.add(v.getUUID()); levels.add(GuardProgression.progress(v).level());
                    p.setItemInHand(InteractionHand.MAIN_HAND, ItemStack.EMPTY);
                });
            }
            for (int n = 0; n < 2; n++) {
                String job = n == 0 ? "knight" : "archer";
                var dispenser = origin.offset(n * 12 - 7, 0, 4);
                world.getServer().runOnServer(server -> {
                    var level = world.getConnection().getServerLevel();
                    level.setBlock(dispenser, Blocks.DISPENSER.defaultBlockState().setValue(DispenserBlock.FACING, Direction.EAST), 3);
                    ((DispenserBlockEntity)level.getBlockEntity(dispenser)).setItem(0, new ItemStack(VillageItems.get(job + "_spawn_egg"), 2));
                    level.setBlock(dispenser.below(), Blocks.REDSTONE_BLOCK.defaultBlockState(), 3);
                });
                context.waitTicks(5);
                world.getServer().runOnServer(server -> {
                    var level = world.getConnection().getServerLevel();
                    check(((DispenserBlockEntity)level.getBlockEntity(dispenser)).getItem(0).getCount() == 1, "Dispenser consumes exactly one guard egg");
                    var v = at(world, dispenser.relative(Direction.EAST)); guard(v, job);
                    ids.add(v.getUUID()); levels.add(GuardProgression.progress(v).level());
                    level.removeBlock(dispenser, false); level.setBlock(dispenser.below(), Blocks.STONE.defaultBlockState(), 3);
                });
            }
            context.waitTicks(200);
            world.getServer().runOnServer(server -> {
                for (int n = 0; n < ids.size(); n++) {
                    var v = (Villager)world.getConnection().getServerLevel().getEntity(ids.get(n));
                    check(v != null && v.getVillagerData().profession().is(VillageProfessions.key(n % 2 == 0 ? "knight" : "archer")), "Egg guard keeps its profession without a workstation");
                    v.setNoAi(true);
                }
            });
            saved = world.getWorldSave();
        }
        try (var world = saved.open()) {
            world.getConnection().waitForChunksDownload();
            world.getServer().runOnServer(server -> {
                for (int n = 0; n < ids.size(); n++) {
                    var v = (Villager)world.getConnection().getServerLevel().getEntity(ids.get(n));
                    check(v != null && v.getVillagerData().profession().is(VillageProfessions.key(n % 2 == 0 ? "knight" : "archer")), "Spawned guard profession survives reload");
                    check(GuardProgression.progress(v).level() == levels.get(n), "Spawned guard level never rerolls");
                    check(v.getMainHandItem().is(n % 2 == 0 ? Items.IRON_SWORD : Items.BOW), "Spawned guard weapon survives reload");
                }
            });
        }
        VillageFriends.LOGGER.info("GUARD SPAWN EGGS PASSED: ordinary adult villagers, full profession keys, veteran levels, equipment, Creative/Survival accounting, powered dispensers, jobs without workstations and reload.");
    }
}
