package dev.villagefriends.client;

import dev.villagefriends.FriendshipPayload;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;
import net.fabricmc.fabric.api.client.rendering.v1.EntityRendererRegistry;
import net.minecraft.world.entity.EntityTypes;

public final class VillageFriendsClient implements ClientModInitializer {
    @Override public void onInitializeClient() {
        ResidentSkins.register();
        EntityRendererRegistry.register(EntityTypes.VILLAGER, ResidentRenderer::new);
        ClientPlayNetworking.registerGlobalReceiver(FriendshipPayload.TYPE, (payload, context) -> {
            var client = context.client();
            if (client.gui.screen() instanceof FriendshipScreen screen && screen.matches(payload)) {
                screen.update(payload);
            } else if (payload.opening() && client.player != null) {
                client.gui.setScreen(new FriendshipScreen(payload));
            }
        });
    }
}
