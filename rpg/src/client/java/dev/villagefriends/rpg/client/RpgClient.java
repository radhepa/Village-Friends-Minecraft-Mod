package dev.villagefriends.rpg.client;

import com.mojang.blaze3d.platform.InputConstants;
import dev.villagefriends.rpg.Balance;
import dev.villagefriends.rpg.Bestiary;
import dev.villagefriends.rpg.Rpg;
import dev.villagefriends.rpg.RpgActionPayload;
import dev.villagefriends.rpg.Sheet;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.keymapping.v1.KeyMappingHelper;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;
import net.fabricmc.fabric.api.client.rendering.v1.hud.HudElementRegistry;
import net.fabricmc.fabric.api.client.rendering.v1.hud.VanillaHudElements;
import net.minecraft.client.DeltaTracker;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.network.chat.Component;

import java.util.List;

/**
 * Keys: K opens the character sheet, R uses the selected Legend ability, G switches between unlocked
 * abilities. A small badge in the corner shows level, experience and the selected ability's cooldown.
 */
public final class RpgClient implements ClientModInitializer {
    static final KeyMapping.Category CATEGORY = KeyMapping.Category.register(Rpg.id("rpg"));
    static KeyMapping open, use, cycle;
    /** The selected ability's family id; kept for the session. */
    static String selected = "";

    @Override public void onInitializeClient() {
        open = KeyMappingHelper.registerKeyMapping(new KeyMapping("key.villagefriends_rpg.character", InputConstants.Type.KEYBOARD, InputConstants.KEY_K, CATEGORY));
        use = KeyMappingHelper.registerKeyMapping(new KeyMapping("key.villagefriends_rpg.ability", InputConstants.Type.KEYBOARD, InputConstants.KEY_R, CATEGORY));
        cycle = KeyMappingHelper.registerKeyMapping(new KeyMapping("key.villagefriends_rpg.next_ability", InputConstants.Type.KEYBOARD, InputConstants.KEY_G, CATEGORY));
        ClientTickEvents.END_CLIENT_TICK.register(client -> {
            while (open.consumeClick()) if (client.player != null && client.gui.screen() == null) client.gui.setScreen(new CharacterScreen());
            while (cycle.consumeClick()) if (client.player != null) {
                var all = unlocked(Rpg.sheet(client.player));
                if (all.isEmpty()) { client.player.sendOverlayMessage(Component.literal("Reach Legend against a monster family to unlock an ability.")); continue; }
                selected = all.get((all.indexOf(current(all)) + 1) % all.size()).id();
                client.player.sendOverlayMessage(Component.literal("Ability: " + Bestiary.byId(selected).active().name()));
            }
            while (use.consumeClick()) if (client.player != null) {
                var f = current(unlocked(Rpg.sheet(client.player)));
                if (f != null && ClientPlayNetworking.canSend(RpgActionPayload.TYPE)) ClientPlayNetworking.send(new RpgActionPayload("ability", f.id()));
            }
        });
        HudElementRegistry.attachElementBefore(VanillaHudElements.TITLE_AND_SUBTITLE, Rpg.id("level_badge"), RpgClient::badge);
    }
    static List<Bestiary.Family> unlocked(Sheet s) { return Bestiary.FAMILIES.stream().filter(f -> s.tier(f) >= 5).toList(); }
    static Bestiary.Family current(List<Bestiary.Family> all) {
        return all.stream().filter(f -> f.id().equals(selected)).findFirst().orElse(all.isEmpty() ? null : all.getFirst());
    }

    private static void badge(GuiGraphicsExtractor g, DeltaTracker delta) {
        var mc = Minecraft.getInstance();
        if (mc.player == null || mc.level == null || mc.gui.screen() != null && !(mc.gui.screen() instanceof net.minecraft.client.gui.screens.ChatScreen)) return;
        var s = Rpg.sheet(mc.player);
        String text = "Lv " + s.level() + (s.points() > 0 ? "  +" + s.points() : "");
        var ability = current(unlocked(s));
        String line = "";
        if (ability != null) {
            long left = s.mark("cd:" + ability.id()) - mc.level.getGameTime();
            line = "[" + use.getTranslatedKeyMessage().getString() + "] " + ability.active().name() + (left > 0 ? " " + (left + 19) / 20 + "s" : "");
        }
        int w = Math.max(54, Math.max(mc.font.width(text), mc.font.width(line)) + 8), x = 4, y = 4;
        g.fill(x, y, x + w, y + (line.isEmpty() ? 15 : 26), 0x99000000);
        g.text(mc.font, "Lv " + s.level(), x + 4, y + 2, 0xFFF4E6C3, true);
        if (s.points() > 0) g.text(mc.font, "+" + s.points(), x + 4 + mc.font.width("Lv " + s.level() + "  "), y + 2, 0xFF7FD36B, true);
        double f = s.level() >= Balance.MAX_LEVEL ? 1 : s.xp() / (double) Balance.need(s.level());
        g.fill(x + 2, y + 11, x + w - 2, y + 13, 0xFF3A2E1E);
        g.fill(x + 2, y + 11, x + 2 + (int) Math.round((w - 4) * f), y + 13, 0xFFE0B04A);
        if (!line.isEmpty()) g.text(mc.font, line, x + 4, y + 16, line.endsWith("s") && Character.isDigit(line.charAt(line.length() - 2)) ? 0xFF9C8B6A : 0xFFC28BF0, true);
    }
}
