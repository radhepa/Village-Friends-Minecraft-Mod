package dev.villagefriends.stable.client.yard;

import dev.villagefriends.stable.data.StableComponents;
import dev.villagefriends.stable.data.StableItems;
import net.fabricmc.fabric.api.client.item.v1.ItemTooltipCallback;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;

/**
 * The stables package's client side: Horse Papers say which animal they are for ("Destrier", "Donkey"...) and how
 * to use them. Called once from {@code StablehandClient}.
 */
public final class YardClient {
    public static void register() {
        ItemTooltipCallback.EVENT.register((stack, context, flag, lines) -> {
            if (!stack.is(StableItems.HORSE_PAPERS)) return;
            var papers = stack.get(StableComponents.HORSE_PAPERS);
            if (papers == null) { lines.add(1, Component.literal("Blank").withStyle(ChatFormatting.GRAY)); return; }
            String animal = switch (papers.breed()) { case "donkey" -> "donkey"; case "mule" -> "mule"; default -> "horse"; };
            lines.add(1, Component.translatable("stablehand.breed." + papers.breed()).withStyle(ChatFormatting.GOLD));
            lines.add(2, Component.literal("Use on the ground to meet your " + animal).withStyle(ChatFormatting.GRAY));
        });
    }

    private YardClient() {}
}
