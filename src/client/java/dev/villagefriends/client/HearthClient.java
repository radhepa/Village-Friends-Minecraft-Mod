package dev.villagefriends.client;

import dev.villagefriends.hearth.Dishes;
import dev.villagefriends.hearth.Hearth;
import dev.villagefriends.hearth.HearthApi;
import dev.villagefriends.hearth.HearthBlocks;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.item.v1.ItemTooltipCallback;
import net.minecraft.ChatFormatting;
import net.minecraft.client.gui.screens.MenuScreens;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;

/**
 * Hearth & Harvest on the client: the kitchen station screen, and dish tooltips (Well Fed tier and time,
 * fine, family recipe cards). A separate client entrypoint so it stays apart from the rest of the client code.
 */
public final class HearthClient implements ClientModInitializer {
    @Override public void onInitializeClient() {
        MenuScreens.register(HearthBlocks.MENU, StationScreen::new);
        ItemTooltipCallback.EVENT.register((stack, context, flag, lines) -> {
            var dish = Dishes.get(BuiltInRegistries.ITEM.getKey(stack.getItem()).toString());
            if (dish != null && dish.dish()) {
                int seconds = (int) Math.round(dish.buff() * (HearthApi.isFine(stack) ? 1.5 : 1));
                lines.add(1, Component.literal("Well Fed " + "I".repeat(dish.tier()) + " · " + seconds / 60 + ":" + (seconds % 60 < 10 ? "0" : "") + seconds % 60)
                        .withStyle(ChatFormatting.GOLD));
                if (HearthApi.isFine(stack)) lines.add(2, Component.literal("Fine: Well Fed lasts longer").withStyle(ChatFormatting.LIGHT_PURPLE));
            }
            String recipe = stack.get(Hearth.RECIPE);
            if (recipe != null) lines.add(1, Component.literal("Use to learn this family recipe").withStyle(ChatFormatting.GRAY));
        });
    }
}
