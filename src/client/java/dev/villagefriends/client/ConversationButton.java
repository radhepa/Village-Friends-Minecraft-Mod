package dev.villagefriends.client;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.components.Button;
import net.minecraft.network.chat.Component;

/** Native button behavior and narration, with a quiet parchment-and-oak treatment. */
public final class ConversationButton extends Button {
    private final boolean primary;
    public ConversationButton(int x, int y, int width, int height, String label, boolean primary, OnPress action) {
        super(x, y, width, height, Component.literal(label), action, DEFAULT_NARRATION);
        this.primary = primary;
    }
    @Override protected void extractContents(GuiGraphicsExtractor g, int mouseX, int mouseY, float delta) {
        boolean selected = active && isHoveredOrFocused();
        int border = selected ? 0xFFAA7447 : 0xFFC8AC83;
        int paper = !active ? 0xFFE0D4BE : selected ? 0xFFFFF6DF : primary ? 0xFFE5EACF : 0xFFF2E4CB;
        int ink = !active ? 0xFF9F947E : primary ? 0xFF43583D : 0xFF5C4635;
        g.fill(getX(), getY() + 1, getX() + getWidth(), getY() + getHeight() + 1, 0xFFB69A71);
        g.fill(getX(), getY(), getX() + getWidth(), getY() + getHeight(), border);
        g.fill(getX() + 1, getY() + 1, getX() + getWidth() - 1, getY() + getHeight() - 1, paper);
        if (selected) g.fill(getX() + 2, getY() + 3, getX() + 4, getY() + getHeight() - 3, 0xFFAA7447);
        var font = Minecraft.getInstance().font;
        String label = font.plainSubstrByWidth(getMessage().getString(), getWidth() - 12);
        g.centeredText(font, label, getX() + getWidth() / 2, getY() + (getHeight() - 8) / 2, ink);
    }
}
