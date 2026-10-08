package dev.villagefriends.rpg.client;

import com.mojang.blaze3d.platform.InputConstants;
import dev.villagefriends.rpg.Balance;
import dev.villagefriends.rpg.Rpg;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.keymapping.v1.KeyMappingHelper;
import net.fabricmc.fabric.api.client.rendering.v1.hud.HudElementRegistry;
import net.fabricmc.fabric.api.client.rendering.v1.hud.VanillaHudElements;
import net.minecraft.client.DeltaTracker;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphicsExtractor;

/** The K key for the character sheet, and a small level badge with an experience bar in the corner. */
public final class RpgClient implements ClientModInitializer {
    static final KeyMapping.Category CATEGORY = KeyMapping.Category.register(Rpg.id("rpg"));
    static KeyMapping open;

    @Override public void onInitializeClient() {
        open = KeyMappingHelper.registerKeyMapping(new KeyMapping("key.villagefriends_rpg.character", InputConstants.Type.KEYBOARD, InputConstants.KEY_K, CATEGORY));
        ClientTickEvents.END_CLIENT_TICK.register(client -> {
            while (open.consumeClick()) if (client.player != null && client.gui.screen() == null) client.gui.setScreen(new CharacterScreen());
        });
        HudElementRegistry.attachElementBefore(VanillaHudElements.TITLE_AND_SUBTITLE, Rpg.id("level_badge"), RpgClient::badge);
    }

    private static void badge(GuiGraphicsExtractor g, DeltaTracker delta) {
        var mc = Minecraft.getInstance();
        if (mc.player == null || mc.gui.screen() != null && !(mc.gui.screen() instanceof net.minecraft.client.gui.screens.ChatScreen)) return;
        var s = Rpg.sheet(mc.player);
        String text = "Lv " + s.level() + (s.points() > 0 ? "  +" + s.points() : "");
        int w = Math.max(54, mc.font.width(text) + 8), x = 4, y = 4;
        g.fill(x, y, x + w, y + 15, 0x99000000);
        g.text(mc.font, "Lv " + s.level(), x + 4, y + 2, 0xFFF4E6C3, true);
        if (s.points() > 0) g.text(mc.font, "+" + s.points(), x + 4 + mc.font.width("Lv " + s.level() + "  "), y + 2, 0xFF7FD36B, true);
        double f = s.level() >= Balance.MAX_LEVEL ? 1 : s.xp() / (double) Balance.need(s.level());
        g.fill(x + 2, y + 11, x + w - 2, y + 13, 0xFF3A2E1E);
        g.fill(x + 2, y + 11, x + 2 + (int) Math.round((w - 4) * f), y + 13, 0xFFE0B04A);
    }
}
