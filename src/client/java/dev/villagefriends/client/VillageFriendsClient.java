package dev.villagefriends.client;

import dev.villagefriends.Emote;
import dev.villagefriends.EmotePayload;
import dev.villagefriends.FriendshipPayload;
import dev.villagefriends.LedgerPayload;
import dev.villagefriends.VillageArrivalPayload;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;
import net.fabricmc.fabric.api.client.rendering.v1.EntityRendererRegistry;
import net.minecraft.world.entity.EntityTypes;

public final class VillageFriendsClient implements ClientModInitializer {
    @Override public void onInitializeClient() {
        ResidentSkins.register();
        AnimationPacks.register();
        ArrivalBanner.register();
        net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents.END_CLIENT_TICK.register(ResidentLife::tickAll);
        net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents.END_CLIENT_TICK.register(EmoteBubbles::tick);
        net.fabricmc.fabric.api.client.networking.v1.ClientPlayConnectionEvents.DISCONNECT.register((handler, client) -> client.execute(() -> { ResidentLife.clear(); EmoteBubbles.clear(); ArrivalBanner.clear(); }));
        ClientPlayNetworking.registerGlobalReceiver(EmotePayload.TYPE, (payload, context) ->
                EmoteBubbles.show(payload.entityId(), Emote.parse(payload.emote()), payload.delay()));
        ClientPlayNetworking.registerGlobalReceiver(LedgerPayload.TYPE, (payload, context) -> {
            var client = context.client();
            if (client.gui.screen() instanceof LedgerScreen ledger && ledger.village().equals(payload.village())) ledger.update(payload);
            else client.gui.setScreen(new LedgerScreen(payload, client.gui.screen()));
        });
        ClientPlayNetworking.registerGlobalReceiver(VillageArrivalPayload.TYPE, (payload, context) ->
                ArrivalBanner.show(payload.village(), payload.variant()));
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
