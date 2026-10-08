package dev.villagefriends.client;

import dev.villagefriends.NoticeBoardPayload;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;

/** Opens village notice boards (and keeps an open one current as notices are taken and turned in). */
public final class NoticeBoardClient implements ClientModInitializer {
    @Override public void onInitializeClient() {
        ClientPlayNetworking.registerGlobalReceiver(NoticeBoardPayload.TYPE, (payload, context) -> {
            var client = context.client();
            if (client.gui.screen() instanceof NoticeBoardScreen board && board.village().equals(payload.village())) board.update(payload);
            else client.gui.setScreen(new NoticeBoardScreen(payload));
        });
    }
}
