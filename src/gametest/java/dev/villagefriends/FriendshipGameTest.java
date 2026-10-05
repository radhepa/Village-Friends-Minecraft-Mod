package dev.villagefriends;

import dev.villagefriends.client.FriendshipScreen;
import dev.villagefriends.client.ResidentRenderer;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.fabricmc.fabric.api.client.gametest.v1.world.TestWorldSave;
import net.minecraft.network.chat.Component;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.npc.villager.VillagerProfession;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;

@SuppressWarnings("UnstableApiUsage")
public final class FriendshipGameTest implements FabricClientGameTest {
    @Override public void runTest(ClientGameTestContext context) {
        TestWorldSave saved;
        UUID villagerUuid;
        UUID playerUuid;
        List<UUID> neighbors = new ArrayList<>();
        try (TestSingleplayerContext world = context.worldBuilder().create()) {
            world.getConnection().waitForChunksRender();
            world.getServer().runCommand("gamemode survival @a");
            playerUuid = world.getServer().computeOnServer(server -> world.getConnection().getServerPlayer().getUUID());
            villagerUuid = world.getServer().computeOnServer(server -> {
                var player = world.getConnection().getServerPlayer();
                var villager = new Villager(EntityTypes.VILLAGER, player.level());
                villager.setPos(player.getX(), player.getY(), player.getZ() + 2);
                villager.setNoAi(true);
                villager.setCustomName(Component.literal("Rowan Meadow"));
                villager.setVillagerData(villager.getVillagerData().withProfession(server.registryAccess(), VillagerProfession.FARMER));
                world.getConnection().getServerLevel().addFreshEntity(villager);
                check(villager.isCustomNameVisible(), "Existing custom names must be visible");
                player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.EMERALD, 8));
                return villager.getUUID();
            });
            world.getConnection().waitForClientboundEntityUpdates(EntityTypes.VILLAGER);
            int entityId = world.getServer().computeOnServer(server -> world.getConnection().getServerLevel().getEntity(villagerUuid).getId());
            context.runOnClient(client -> {
                var entity = (Villager) client.level.getEntity(entityId);
                check(client.getEntityRenderDispatcher().getRenderer(entity) instanceof ResidentRenderer, "Villagers must use the player-shaped renderer");
                assertSkin(client, entity, 0);
                client.gameMode.interact(client.player, entity, new net.minecraft.world.phys.EntityHitResult(entity), InteractionHand.MAIN_HAND);
            });
            context.waitForScreen(FriendshipScreen.class);
            context.runOnClient(client -> client.gui.toastManager().clear());
            context.takeScreenshot("village-friends-conversation");
            context.clickScreenButton("How's your day?");
            world.getConnection().waitForServerboundPackets();
            world.getConnection().waitForClientboundPackets();
            assertPoints(world, villagerUuid, 4);
            context.clickScreenButton("Share a joke");
            world.getConnection().waitForServerboundPackets();
            world.getConnection().waitForClientboundPackets();
            assertPoints(world, villagerUuid, 4);
            context.clickScreenButton("Give gift");
            world.getConnection().waitForServerboundPackets();
            world.getConnection().waitForClientboundPackets();
            assertPoints(world, villagerUuid, 16);
            world.getServer().runOnServer(server -> {
                var player = world.getConnection().getServerPlayer();
                check(player.getMainHandItem().getCount() == 7, "One gift must consume exactly one emerald");
            });
            context.clickScreenButton("Give gift");
            world.getConnection().waitForServerboundPackets();
            world.getConnection().waitForClientboundPackets();
            context.clickScreenButton("Give gift");
            world.getConnection().waitForServerboundPackets();
            world.getConnection().waitForClientboundPackets();
            assertPoints(world, villagerUuid, 40);
            context.runOnClient(client -> check(client.gui.screen().children().stream()
                    .filter(child -> child instanceof net.minecraft.client.gui.components.Button)
                    .map(child -> (net.minecraft.client.gui.components.Button) child)
                    .anyMatch(button -> button.getMessage().getString().equals("Give gift") && !button.active),
                    "Gift button must disable after the third gift"));
            context.takeScreenshot("village-friends-friendship");
            context.getInput().resizeWindow(1280, 800);
            context.runOnClient(client -> { client.options.guiScale().set(2); client.resizeGui(); });
            context.waitTicks(60);
            context.runOnClient(client -> client.gui.toastManager().clear());
            context.takeScreenshot("village-friends-portrait-large");
            world.getServer().runOnServer(server -> {
                var player = world.getConnection().getServerPlayer();
                check(player.getMainHandItem().getCount() == 5, "Three gifts must consume three emeralds");
            });
            context.clickScreenButton("Goodbye");
            context.waitForScreen(null);
            world.getServer().runOnServer(server -> {
                var player = world.getConnection().getServerPlayer();
                var primary = world.getConnection().getServerLevel().getEntity(villagerUuid);
                primary.setPos(player.getX(), player.getY(), player.getZ() - 3);
                for (int design = 0; design < 5; design++) {
                    var neighbor = new Villager(EntityTypes.VILLAGER, player.level());
                    neighbor.setPos(player.getX() + (design - 2) * 2.0, player.getY(), player.getZ() + 5);
                    neighbor.setNoAi(true);
                    neighbor.setYRot(180);
                    neighbor.yBodyRot = neighbor.yHeadRot = 180;
                    world.getConnection().getServerLevel().addFreshEntity(neighbor);
                    check(neighbor.hasCustomName(), "Every newly spawned villager must get a name before interacting");
                    check(neighbor.isCustomNameVisible(), "Generated names must hover over villagers");
                    check(neighbor.getCustomName().getString().equals(Dialogue.name(neighbor.getUUID(),VillageFriends.profile(neighbor).look())), "Generated name must match stable identity");
                    neighbors.add(neighbor.getUUID());
                }
            });
            world.getConnection().waitForClientboundEntityUpdates(EntityTypes.VILLAGER);
            context.runOnClient(client -> {
                for (int design = 0; design < neighbors.size(); design++) {
                    Villager neighbor = null;
                    for (var candidate : client.level.entitiesForRendering()) {
                        if (candidate.getUUID().equals(neighbors.get(design))) neighbor = (Villager) candidate;
                    }
                    check(neighbor != null, "Each resident must reach the client");
                    assertSkin(client, neighbor, design);
                }
            });
            context.getInput().lookAt(0, 6);
            context.waitTicks(70);
            context.runOnClient(client -> client.gui.toastManager().clear());
            context.takeScreenshot("village-friends-five-residents");
            saved = world.getWorldSave();
        }
        try (TestSingleplayerContext reopened = saved.open()) {
            reopened.getConnection().waitForChunksDownload();
            reopened.getServer().runOnServer(server -> {
                var entity = reopened.getConnection().getServerLevel().getEntity(villagerUuid);
                check(entity instanceof Villager, "Villager must survive a save and reload");
                var book = ((net.fabricmc.fabric.api.attachment.v1.AttachmentTarget) entity).getAttached(VillageFriends.FRIENDSHIPS);
                check(book != null, "Friendship attachment must persist");
                check(book.get(playerUuid).points() == 40, "Saved friendship must remain at 40 points");
                check(book.get(playerUuid).giftsToday() == 3, "Daily gift count must persist");
                check(((Villager) entity).isCustomNameVisible(), "Hover name must remain visible after reload");
                for (int design = 0; design < neighbors.size(); design++) {
                    var neighbor = reopened.getConnection().getServerLevel().getEntity(neighbors.get(design));
                    check(neighbor instanceof Villager && neighbor.hasCustomName(), "Resident name must save with the world");
                }
            });
        }
        VillageFriends.LOGGER.info("GAMEPLAY TEST PASSED: portrait UI, player-shaped renderer, five resident designs, hovering names, conversations, gifts, and persistence after world reload.");
    }

    private static void assertPoints(TestSingleplayerContext world, UUID uuid, int expected) {
        world.getServer().runOnServer(server -> {
            var villager = (Villager) world.getConnection().getServerLevel().getEntity(uuid);
            int actual = VillageFriends.state(villager, world.getConnection().getServerPlayer()).points();
            check(actual == expected, "Expected " + expected + " friendship points, got " + actual);
        });
    }
    private static void assertSkin(net.minecraft.client.Minecraft client, Villager villager, int design) {
        var dispatcher = client.getEntityRenderDispatcher();
        var renderer = (ResidentRenderer) dispatcher.getRenderer(villager);
        var state = renderer.createRenderState(villager, 1.0F);
        check(dispatcher.getRenderer(state) == renderer,
                "World and portrait render states must retain the villager renderer, without falling back to Steve");
        var texture = renderer.getTextureLocation(state);
        check(texture.equals(dev.villagefriends.client.ResidentSkins.texture(((net.fabricmc.fabric.api.attachment.v1.AttachmentTarget)villager).getAttached(VillageFriends.LOOK),VillageFriends.profession(villager))),
                "Synced legacy appearance keeps its identity while wearing the correct job clothes");
        check(texture.getPath().startsWith("generated/")
                ? client.getTextureManager().getTexture(texture) instanceof net.minecraft.client.renderer.texture.DynamicTexture
                : client.getResourceManager().getResource(texture).isPresent(), "Assigned skin must be available to Minecraft");
    }
    private static void check(boolean condition, String message) {
        if (!condition) throw new AssertionError(message);
    }
}

