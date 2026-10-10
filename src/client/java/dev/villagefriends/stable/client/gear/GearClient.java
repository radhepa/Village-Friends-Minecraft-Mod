package dev.villagefriends.stable.client.gear;

import dev.villagefriends.stable.data.StableItems;
import dev.villagefriends.stable.data.StableTable;
import dev.villagefriends.stable.gear.GearText;
import dev.villagefriends.stable.gear.Tack;
import java.util.List;
import net.fabricmc.fabric.api.client.item.v1.ItemTooltipCallback;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;

/**
 * The gear package's client side: plain-words tooltips for tack, barding and the lance, built from the gear table
 * ({@link GearText}), so they always match the numbers the game uses. Rendering needs no code here: vanilla draws
 * barding through its {@code horse_body} layer and tack through the saddle layers, from the equipment assets
 * {@code tools/stablehand/gear.py} writes. Called once from {@code StablehandClient}.
 */
public final class GearClient {
    public static void register() {
        ItemTooltipCallback.EVENT.register((stack, context, flag, lines) -> {
            List<String> extra = Tack.row(stack).map(GearText::lines)
                    .orElseGet(() -> StableItems.JOUSTING_LANCE != null && stack.is(StableItems.JOUSTING_LANCE) ? GearText.lance(StableTable.lance()) : List.of());
            int at = Math.min(1, lines.size());
            for (var line : extra) lines.add(at++, Component.literal(line).withStyle(ChatFormatting.GRAY));
        });
    }

    private GearClient() {}
}
