package dev.villagefriends.client;

import dev.villagefriends.ActionPayload;
import dev.villagefriends.FriendshipPayload;
import dev.villagefriends.FriendshipState;
import java.util.ArrayList;
import java.util.List;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.components.Tooltip;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.gui.screens.inventory.InventoryScreen;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.LivingEntity;

public final class FriendshipScreen extends Screen {
    private static final int INK = 0xFF4E382B;
    private static final int MUTED = 0xFF8B765C;
    private static final int PAPER = 0xFFF6E9CE;
    private static final int HEART = 0xFFC56565;
    private static final int SAGE = 0xFF62734E;
    private FriendshipPayload data;
    private final List<Button> actions = new ArrayList<>();
    private boolean waiting;
    private int waitTicks;
    private int left, top, panelWidth, panelHeight, portraitWidth, textLeft, textWidth, topicsY;
    private int dialogueScroll;
    private String lastDialogue;

    public FriendshipScreen(FriendshipPayload data) {
        super(Component.literal("Village Friends - " + data.name()));
        this.data = data;
        lastDialogue = data.dialogue();
    }
    public boolean matches(FriendshipPayload next) { return data.villagerId().equals(next.villagerId()); }
    public void update(FriendshipPayload next) {
        if (!lastDialogue.equals(next.dialogue())) { dialogueScroll = 0; lastDialogue = next.dialogue(); }
        data = next;
        waiting = false;
        waitTicks = 0;
        rebuildWidgets();
        triggerImmediateNarration(false);
    }
    @Override protected void init() {
        actions.clear();
        panelWidth = Math.min(500, width - 24);
        panelHeight = Math.min(276, height - 24);
        left = (width - panelWidth) / 2;
        top = height - panelHeight - 12;
        portraitWidth = Math.clamp(panelWidth / 4, 82, 112);
        textLeft = left + portraitWidth + 27;
        textWidth = panelWidth - portraitWidth - 44;
        topicsY = top + panelHeight - 108;
        int half = (textWidth - 5) / 2;
        String[] tabs = {"Talk", "Story", "Journal", "Time", "Travel"};
        String[] tabActions = {"talk_tab", "story", "journal", "together", "companion"};
        String[] tabIds = {"talk", "story", "journal", "together", "companion"};
        int tabWidth = (textWidth - 12) / 5;
        for (int i = 0; i < tabs.length; i++) addTab(tabs[i], tabActions[i], textLeft + i * (tabWidth + 3), top + 44, tabWidth, tabIds[i].equals(data.tab()));
        for (int i = 0; i < data.choices().size(); i++) {
            var choice = data.choices().get(i);
            Button button = addAction(choice.label(), choice.id(), textLeft + (i % 2) * (half + 5), topicsY + (i / 2) * 24, half, false);
            button.active = !waiting && choice.enabled();
        }
        int bottomY = top + panelHeight - 33;
        Button gift = addAction("Give gift", "gift", left + 14, bottomY, portraitWidth, true);
        gift.active = !waiting && data.giftsLeft() > 0;
        gift.setTooltip(Tooltip.create(Component.literal("Offer one " + heldName() + " from your main hand. " + data.giftHint())));
        int tradeWidth = (textWidth - 6) / 2;
        Button trade = addAction("Trade", "trade", textLeft, bottomY, tradeWidth, false);
        trade.active = !waiting && data.canTrade();
        addRenderableWidget(new ConversationButton(textLeft + tradeWidth + 6, bottomY,
                textWidth - tradeWidth - 6, 21, "Goodbye", false, button -> onClose()));
    }
    private Button addAction(String label, String action, int x, int y, int w, boolean primary) {
        Button button = new ConversationButton(x, y, w, 21, label, primary, pressed -> send(action));
        button.active = !waiting;
        actions.add(button);
        return addRenderableWidget(button);
    }
    private void addTab(String label, String action, int x, int y, int w, boolean selected) {
        Button button = new ConversationButton(x, y, w, 16, label, selected, pressed -> send(action));
        button.active = !waiting; actions.add(button); addRenderableWidget(button);
    }
    private void send(String action) {
        if (waiting || !ClientPlayNetworking.canSend(ActionPayload.TYPE)) return;
        ClientPlayNetworking.send(new ActionPayload(data.entityId(), data.villagerId(), action));
        if (action.equals("trade") || action.equals("home")) { onClose(); return; }
        waiting = true;
        waitTicks = 0;
        actions.forEach(button -> button.active = false);
    }
    @Override public void tick() {
        if (minecraft.player == null || minecraft.level == null) { onClose(); return; }
        var villager = minecraft.level.getEntity(data.entityId());
        if (villager == null || !villager.isAlive() || !villager.getUUID().equals(data.villagerId())
                || minecraft.player.distanceToSqr(villager) > 36 || !minecraft.player.isAlive()) { onClose(); return; }
        if (waiting && ++waitTicks > 100) { waiting = false; rebuildWidgets(); }
    }
    @Override public boolean isPauseScreen() { return false; }
    @Override public boolean isInGameUi() { return true; }
    @Override public Component getNarrationMessage() {
        return Component.literal(data.name() + ", " + data.profession() + ". " + friendshipTitle()
                + ", " + data.points() + " friendship points. " + data.dialogue() + " " + data.status());
    }
    private String friendshipTitle() { return switch(data.level()) { case 1 -> "Acquaintance"; case 2 -> "Friend"; case 3 -> "Close Friend"; case 4 -> "Best Friend"; default -> "New Neighbor"; }; }
    private String heldName() {
        return minecraft.player == null || minecraft.player.getMainHandItem().isEmpty() ? "empty hand"
                : minecraft.player.getMainHandItem().getHoverName().getString();
    }
    @Override public boolean mouseScrolled(double x, double y, double horizontal, double vertical) {
        if (x >= textLeft && x < textLeft + textWidth && y >= top + 65 && y < topicsY - 6) {
            int lines = font.split(Component.literal(data.dialogue()), textWidth - 8).size();
            int visible = Math.max(1, (topicsY - 6 - (top + 65)) / 11);
            dialogueScroll = Math.clamp(dialogueScroll - (int)Math.signum(vertical), 0, Math.max(0, lines - visible));
            return true;
        }
        return super.mouseScrolled(x, y, horizontal, vertical);
    }
    @Override public void extractRenderState(GuiGraphicsExtractor g, int mouseX, int mouseY, float delta) {
        g.fill(0, 0, width, height, 0x440D1410);
        frame(g, left, top, panelWidth, panelHeight);
        g.fill(left + 8, top + 8, left + panelWidth - 8, top + panelHeight - 8, PAPER);
        g.fill(left + 9, top + 9, left + panelWidth - 9, top + 10, 0xFFFFF5DD);
        // A live portrait uses the exact skin seen in the world, including children.
        int portraitX = left + 14;
        int portraitY = top + 15;
        int portraitHeight = panelHeight - 100;
        g.fill(portraitX, portraitY, portraitX + portraitWidth, portraitY + portraitHeight, 0xFFB99A70);
        g.fillGradient(portraitX + 2, portraitY + 2, portraitX + portraitWidth - 2,
                portraitY + portraitHeight - 2, 0xFFD2DEC0, 0xFFF0E7CB);
        if (minecraft.level != null && minecraft.level.getEntity(data.entityId()) instanceof LivingEntity villager) {
            InventoryScreen.extractEntityInInventoryFollowsMouse(g, portraitX + 2, portraitY + 2,
                    portraitX + portraitWidth - 2, portraitY + portraitHeight - 2,
                    (int)Math.min(portraitWidth * 1.07, portraitHeight * 0.65), 0.36F,
                    portraitX + portraitWidth / 2F - 10, portraitY + portraitHeight / 2F, villager);
        }
        int heartsX = portraitX + (portraitWidth - 79) / 2;
        int heartsY = top + panelHeight - 74;
        for (int i = 0; i < 10; i++) heart(g, heartsX + i * 8, heartsY, data.points() - i * 20);
        g.centeredText(font, friendshipTitle(), portraitX + portraitWidth / 2, heartsY + 12, INK);
        g.centeredText(font, data.giftsLeft() + " gifts left today", portraitX + portraitWidth / 2, heartsY + 24, MUTED);
        // The resident's name leads; metadata is secondary, leaving the reading surface calm.
        var nameLines=font.split(Component.literal(data.name()),textWidth);
        g.text(font,nameLines.getFirst(),textLeft,top+17,INK,false);
        if(nameLines.size()>1)g.text(font,nameLines.get(1),textLeft,top+29,INK,false);
        if(mouseX>=textLeft&&mouseX<textLeft+textWidth&&mouseY>=top+15&&mouseY<top+42)
            g.setTooltipForNextFrame(Component.literal(data.name()+" / "+data.profession()+" / "+data.personality()+" / "+data.trust()),mouseX,mouseY);
        if(nameLines.size()==1)g.text(font, font.plainSubstrByWidth(data.profession() + " / " + data.personality() + " / " + data.trust(), textWidth), textLeft, top + 31, MUTED, false);
        var lines = font.split(Component.literal(data.dialogue()), textWidth - 8);
        int visibleLines = Math.max(1, (topicsY - 6 - (top + 65)) / 11);
        dialogueScroll = Math.clamp(dialogueScroll, 0, Math.max(0, lines.size() - visibleLines));
        g.enableScissor(textLeft, top + 64, textLeft + textWidth, topicsY - 5);
        int y = top + 65;
        for (int line = dialogueScroll; line < Math.min(lines.size(), dialogueScroll + visibleLines); line++) {
            g.text(font, lines.get(line), textLeft, y, INK, false);
            y += 11;
        }
        g.disableScissor();
        if (lines.size() > visibleLines) {
            g.text(font, "+", textLeft + textWidth - 6, topicsY - 15, MUTED, false);
            if (mouseX >= textLeft && mouseX < textLeft + textWidth && mouseY >= top + 64 && mouseY < topicsY - 5)
                g.setTooltipForNextFrame(font, font.split(Component.literal(data.dialogue()), Math.min(330, width - 24)), mouseX, mouseY);
        }
        int statusY = top + panelHeight - 56;
        String status = waiting ? "Listening..." : data.status();
        g.text(font, font.plainSubstrByWidth(status, textWidth), textLeft, statusY, SAGE, false);
        g.text(font, font.plainSubstrByWidth("Offering: " + heldName() + " (one item)", textWidth), textLeft, statusY + 11, MUTED, false);
        if (mouseX >= textLeft && mouseX < textLeft + textWidth && mouseY >= statusY && mouseY < statusY + 10)
            g.setTooltipForNextFrame(Component.literal(status), mouseX, mouseY);
        g.fill(left + 14, top + panelHeight - 38, left + panelWidth - 14, top + panelHeight - 37, 0xFFDAC6A3);
        super.extractRenderState(g, mouseX, mouseY, delta);
    }
    private static void frame(GuiGraphicsExtractor g, int x, int y, int w, int h) {
        g.fill(x + 2, y + 3, x + w + 2, y + h + 3, 0x660D0906);
        g.fill(x, y, x + w, y + h, 0xFF60412D);
        g.fill(x + 2, y + 2, x + w - 2, y + h - 2, 0xFFB88751);
        g.fill(x + 2, y + 2, x + w - 2, y + 4, 0xFFE0B77D);
        g.fill(x + 2, y + 4, x + 4, y + h - 4, 0xFFD5A367);
        g.fill(x + 4, y + h - 4, x + w - 2, y + h - 2, 0xFF8B5B35);
        g.fill(x + w - 4, y + 4, x + w - 2, y + h - 4, 0xFF8B5B35);
        g.fill(x + 6, y + 6, x + w - 6, y + h - 6, 0xFF725036);
        for (int px : new int[]{x + 3, x + w - 5}) for (int py : new int[]{y + 3, y + h - 5})
            g.fill(px, py, px + 2, py + 2, 0xFFF3CF8F);
    }
    private static void heart(GuiGraphicsExtractor g, int x, int y, int progress) {
        int[] masks = {0b0110110, 0b1111111, 0b1111111, 0b0111110, 0b0011100, 0b0001000};
        for (int row = 0; row < masks.length; row++) for (int col = 0; col < 7; col++) {
            if ((masks[row] & (1 << (6 - col))) == 0) continue;
            boolean filled = col < Math.clamp(progress / 20F, 0, 1) * 7;
            int color = filled ? row == 1 ? 0xFFE49A8A : HEART : 0xFFD7C8B0;
            g.fill(x + col, y + row, x + col + 1, y + row + 1, color);
        }
    }
}
