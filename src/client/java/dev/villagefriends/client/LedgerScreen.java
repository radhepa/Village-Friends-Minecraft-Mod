package dev.villagefriends.client;

import static dev.villagefriends.client.FriendshipScreen.*;
import dev.villagefriends.FriendshipLevels;
import dev.villagefriends.LedgerPayload;
import dev.villagefriends.LedgerRequestPayload;
import java.util.ArrayList;
import java.util.List;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.gui.screens.inventory.InventoryScreen;
import net.minecraft.client.input.MouseButtonEvent;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.LivingEntity;

/**
 * The Village Ledger: a two-page book listing everyone who lives in a village. The left page lists
 * residents with their job, family or love life and your friendship level; the right page shows the
 * village news, or one resident's story and a meter for how they feel about every neighbor.
 */
public final class LedgerScreen extends Screen {
    private static final int ROW = 22, LINE = 10;
    private static final int[] BADGES = {0xFFE88A6E, 0xFF7C9CCF, 0xFFF0B84A, 0xFF5FAE8B, 0xFFB08ACF, 0xFF8DB062, 0xFF6E8E9E, 0xFFE07FA8};
    private final Screen parent;
    private LedgerPayload data;
    private int x, y, w, h, pageW, listTop, listH, detailX, detailTop, detailH;
    private int listScroll, detailScroll, hovered = -1, hoveredTie = -1;
    private long requested;

    public LedgerScreen(LedgerPayload data, Screen parent) {
        super(Component.literal("Village Ledger - " + data.villageName()));
        this.data = data;
        this.parent = parent;
        scrollToFocus();
    }
    public String village() { return data.village(); }
    public void update(LedgerPayload next) {
        boolean newFocus = !next.focus().equals(data.focus());
        data = next;
        if (newFocus) { detailScroll = 0; scrollToFocus(); rebuildWidgets(); }
    }
    private void scrollToFocus() {
        for (int i = 0; i < data.residents().size(); i++) if (data.residents().get(i).id().equals(data.focus())) listScroll = Math.max(0, i - 2);
    }
    private void focus(String id) {
        long now = System.currentTimeMillis();
        if (now - requested < 150 || !ClientPlayNetworking.canSend(LedgerRequestPayload.TYPE)) return;
        requested = now;
        ClientPlayNetworking.send(new LedgerRequestPayload(data.village(), id));
    }

    @Override protected void init() {
        w = Math.min(470, width - 16); h = Math.min(300, height - 16);
        x = (width - w) / 2; y = (height - h) / 2;
        pageW = (w - 24) / 2;
        listTop = y + 34; listH = h - 34 - 30;
        detailX = x + 14 + pageW + 8; detailTop = y + 34; detailH = h - 34 - 30;
        addRenderableWidget(new ConversationButton(x + w - 74, y + h - 25, 62, 18, parent instanceof FriendshipScreen ? "Back" : "Close", true, b -> onClose()));
        if (!data.focus().isEmpty())
            addRenderableWidget(new ConversationButton(x + w - 74 - 92, y + h - 25, 86, 18, "Village news", false, b -> focus("")));
    }
    @Override public void onClose() { minecraft.gui.setScreen(parent instanceof FriendshipScreen ? parent : null); }
    @Override public boolean isPauseScreen() { return false; }

    // -- input -------------------------------------------------------------------------------------

    @Override public boolean mouseClicked(MouseButtonEvent event, boolean doubleClick) {
        if (hovered >= 0 && hovered < data.residents().size()) {
            var id = data.residents().get(hovered).id();
            if (!id.equals(data.focus())) focus(id);
            return true;
        }
        if (hoveredTie >= 0 && hoveredTie < data.detail().ties().size()) { focus(data.detail().ties().get(hoveredTie).id()); return true; }
        return super.mouseClicked(event, doubleClick);
    }
    @Override public boolean mouseScrolled(double mx, double my, double horizontal, double vertical) {
        int step = (int) -Math.signum(vertical);
        if (mx < detailX) listScroll = Math.clamp(listScroll + step, 0, Math.max(0, data.residents().size() - listH / ROW));
        else detailScroll = Math.clamp(detailScroll + step * 2, 0, Math.max(0, detailLines() - detailH / LINE));
        return true;
    }

    // -- drawing -----------------------------------------------------------------------------------

    @Override public void extractBackground(GuiGraphicsExtractor g, int mouseX, int mouseY, float delta) {
        g.fill(0, 0, width, height, 0xD0100C08);
    }
    @Override public void extractRenderState(GuiGraphicsExtractor g, int mouseX, int mouseY, float delta) {
        // A leather-bound book with two parchment pages.
        g.fill(x + 2, y + 3, x + w + 2, y + h + 3, 0x66000000);
        g.fill(x, y, x + w, y + h, 0xFF5A2E1E); g.fill(x + 2, y + 2, x + w - 2, y + h - 2, 0xFF7A3A26);
        panel(g, x + 8, y + 8, pageW + 4, h - 16, PAPER);
        panel(g, x + 12 + pageW, y + 8, pageW + 4, h - 16, PAPER);
        g.fill(x + w / 2 - 1, y + 10, x + w / 2 + 1, y + h - 10, 0x33000000);
        long living = data.residents().stream().filter(e -> !e.status().equals("passed")).count();
        g.text(font, font.plainSubstrByWidth(data.villageName(), pageW - 10), x + 16, y + 14, INK, false);
        g.text(font, living + " residents · day " + (data.day() + 1), x + 16, y + 23, MUTED, false);
        drawList(g, mouseX, mouseY);
        if (data.focus().isEmpty()) drawNews(g); else drawDetail(g, mouseX, mouseY);
        super.extractRenderState(g, mouseX, mouseY, delta);
    }
    private void drawList(GuiGraphicsExtractor g, int mouseX, int mouseY) {
        hovered = -1;
        int left = x + 14, rows = listH / ROW;
        listScroll = Math.clamp(listScroll, 0, Math.max(0, data.residents().size() - rows));
        g.enableScissor(left - 2, listTop - 2, left + pageW, listTop + listH);
        for (int i = listScroll, row = 0; i < data.residents().size() && row < rows; i++, row++) {
            var e = data.residents().get(i);
            int ry = listTop + row * ROW;
            boolean hover = mouseX >= left && mouseX < left + pageW - 4 && mouseY >= ry && mouseY < ry + ROW - 2;
            if (hover) hovered = i;
            boolean focused = e.id().equals(data.focus());
            if (focused || hover) g.fill(left - 1, ry - 1, left + pageW - 5, ry + ROW - 2, focused ? 0xFFFBE3B2 : 0xFFF6ECD8);
            boolean gone = e.status().equals("passed");
            int badge = gone ? 0xFFA79C8D : BADGES[Math.floorMod(e.job().hashCode(), BADGES.length)];
            pill(g, left + 1, ry + 1, 16, 16, badge);
            g.centeredText(font, e.name().isEmpty() ? "?" : e.name().substring(0, 1), left + 9, ry + 5, 0xFFFFFFFF);
            int textW = pageW - 56;
            g.text(font, font.plainSubstrByWidth(e.name(), textW), left + 21, ry + 1, gone ? MUTED : INK, false);
            String sub = e.job() + " · " + e.note();
            g.text(font, font.plainSubstrByWidth(sub, textW), left + 21, ry + 11, e.status().equals("cursed") ? 0xFF4F8A3A : MUTED, false);
            if (e.level() >= 0) {
                heart(g, left + pageW - 30, ry + 3, 1);
                g.text(font, String.valueOf(e.level()), left + pageW - 21, ry + 3, TIERS[FriendshipLevels.tier(e.level())], false);
            }
            if (hover) g.setTooltipForNextFrame(Component.literal(e.name() + "\n" + sub + "\n" + (e.level() < 0 ? "You haven't met yet" : "Your friendship: Lv. " + e.level() + " " + FriendshipLevels.name(e.level()))), mouseX, mouseY);
        }
        g.disableScissor();
        if (data.residents().isEmpty()) g.text(font, "Nobody has been counted here yet.", left, listTop, MUTED, false);
        if (data.residents().size() > rows) {
            int trackX = left + pageW - 3, thumb = Math.max(8, listH * rows / data.residents().size());
            int offset = (listH - thumb) * listScroll / Math.max(1, data.residents().size() - rows);
            g.fill(trackX, listTop, trackX + 2, listTop + listH, PAPER_SHADE);
            g.fill(trackX, listTop + offset, trackX + 2, listTop + offset + thumb, EDGE_LIGHT);
        }
    }
    private void drawNews(GuiGraphicsExtractor g) {
        hoveredTie = -1;
        int left = detailX + 4;
        g.text(font, "Village news", left, y + 14, INK, false);
        g.text(font, "Click a resident to read their page.", left, y + 23, MUTED, false);
        var lines = new ArrayList<String>();
        for (String item : data.news()) { lines.addAll(wrap("• " + item, pageW - 12)); lines.add(""); }
        drawLines(g, lines, left, detailTop, INK);
    }
    private int detailLines() {
        return data.focus().isEmpty() ? data.news().size() * 3 : aboutLines().size() + 2 + data.detail().ties().size() * 2;
    }
    private List<String> aboutLines() {
        var lines = new ArrayList<String>();
        for (String line : data.detail().about()) lines.addAll(wrap(line, pageW - 14));
        return lines;
    }
    private void drawDetail(GuiGraphicsExtractor g, int mouseX, int mouseY) {
        hoveredTie = -1;
        var entry = data.residents().stream().filter(e -> e.id().equals(data.focus())).findFirst().orElse(null);
        if (entry == null) return;
        int left = detailX + 4, portrait = 0;
        if (entry.entityId() >= 0 && minecraft.level != null && minecraft.level.getEntity(entry.entityId()) instanceof LivingEntity living) {
            portrait = 30;
            frame(g, left - 1, y + 11, 26, 26);
            g.fillGradient(left, y + 12, left + 24, y + 36, 0xFFCFE3C2, 0xFFF4EBCF);
            ResidentRenderer.portrait = true;
            try { InventoryScreen.extractEntityInInventoryFollowsMouse(g, left, y + 12, left + 24, y + 36, 30, 0.6F, left + 12, y + 18, living); }
            finally { ResidentRenderer.portrait = false; }
        }
        g.text(font, font.plainSubstrByWidth(entry.name(), pageW - 10 - portrait), left + portrait, y + 14, INK, false);
        g.text(font, font.plainSubstrByWidth(entry.job() + (entry.adult() ? "" : " · young"), pageW - 10 - portrait), left + portrait, y + 23, MUTED, false);
        // About, then a meter for every neighbor: family first, then from fondest to frostiest.
        int top = detailTop + 4, bottom = detailTop + detailH, row = -detailScroll;
        g.enableScissor(left - 2, top - 1, left + pageW, bottom);
        for (String line : aboutLines()) { if (row >= 0) g.text(font, line, left, top + row * LINE, INK, false); row++; }
        row++;
        if (row >= 0) g.text(font, "How they feel about everyone", left, top + row * LINE, SAGE, false);
        row++;
        var ties = data.detail().ties();
        for (int i = 0; i < ties.size(); i++) {
            var tie = ties.get(i);
            int ty = top + row * LINE;
            if (row >= 0 && ty < bottom) {
                boolean hover = mouseX >= left && mouseX < left + pageW - 6 && mouseY >= ty && mouseY < ty + LINE * 2 && mouseY < bottom;
                if (hover) { hoveredTie = i; g.fill(left - 1, ty - 1, left + pageW - 6, ty + LINE * 2 - 1, 0xFFF6ECD8); }
                g.text(font, font.plainSubstrByWidth(tie.name(), pageW / 2 - 4), left, ty, INK, false);
                String label = tie.label();
                g.text(font, label, left + pageW - 10 - font.width(label), ty, tie.family() ? HEART : MUTED, false);
                meter(g, left, ty + LINE + 1, pageW - 12, tie.affinity(), tie.family());
            }
            row += 2;
        }
        g.disableScissor();
    }
    /** A relationship meter from -100 to 100, filling right (green to pink) or left (red) from the middle. */
    private static void meter(GuiGraphicsExtractor g, int x, int y, int w, int value, boolean family) {
        int mid = x + w / 2;
        g.fill(x, y, x + w, y + 4, 0xFFE3D6C0);
        g.fill(mid, y - 1, mid + 1, y + 5, 0xFFB8A58A);
        int span = (int) (w / 2F * Math.min(100, Math.abs(value)) / 100F);
        int color = value < 0 ? 0xFFD9534A : family ? HEART : value >= 65 ? 0xFFE3789E : value >= 40 ? 0xFF6DB56A : 0xFF9DBF7C;
        if (value >= 0) g.fill(mid + 1, y, mid + 1 + span, y + 4, color); else g.fill(mid - span, y, mid, y + 4, color);
    }
    private void drawLines(GuiGraphicsExtractor g, List<String> lines, int left, int top, int color) {
        int visible = detailH / LINE;
        detailScroll = Math.clamp(detailScroll, 0, Math.max(0, lines.size() - visible));
        for (int i = detailScroll, row = 0; i < lines.size() && row < visible; i++, row++)
            g.text(font, lines.get(i), left, top + row * LINE, color, false);
    }
    private List<String> wrap(String text, int width) {
        return font.splitIgnoringLanguage(Component.literal(text), width).stream().map(t -> t.getString()).toList();
    }
}
