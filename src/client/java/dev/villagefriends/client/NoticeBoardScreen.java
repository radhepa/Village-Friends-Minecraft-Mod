package dev.villagefriends.client;

import static dev.villagefriends.client.FriendshipScreen.*;
import dev.villagefriends.NoticeActionPayload;
import dev.villagefriends.NoticeBoardPayload;
import java.util.ArrayList;
import java.util.List;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.input.MouseButtonEvent;
import net.minecraft.client.resources.sounds.SimpleSoundInstance;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;

/**
 * A village notice board: a cork board under a little shingle roof with residents' notices pinned to it,
 * each on its own paper (hunts, wanted goods, letters to carry, birthday surprises). Click a notice to read
 * it, take it down, turn it in or pin it back up. With nothing selected, the right-hand page lists the
 * notices you have in hand from any village and the village's upcoming birthdays.
 */
public final class NoticeBoardScreen extends Screen {
    private static final int CORK = 0xFFC48F57, CORK_DARK = 0xFFA87443, CORK_LIGHT = 0xFFD6A469, WOOD = 0xFF6E4527, WOOD_LIGHT = 0xFF8E5D35,
            ROOF = 0xFF7A3B2C, ROOF_DARK = 0xFF5E2B20, GOOD = 0xFF3F8A3A, LINE = 10;
    private NoticeBoardPayload data;
    private String selected = "", message = "";
    private int messageAt, ticks;
    private int x, y, w, h, corkX, corkY, corkW, corkH, pageX, pageY, pageW, pageH, cardW, cardH, page, hovered = -1;
    private long sent;

    public NoticeBoardScreen(NoticeBoardPayload data) {
        super(Component.literal("Notice Board - " + data.villageName()));
        this.data = data;
        this.message = data.message();
    }
    public String village() { return data.village(); }
    /** What the board shows (for tests). */
    public NoticeBoardPayload data() { return data; }
    /** Opens one notice on the right-hand page (for tests). */
    public void select(String id) { selected = card(id) == null ? "" : id; rebuildWidgets(); }
    public void update(NoticeBoardPayload next) {
        data = next;
        if (!next.message().isEmpty()) { message = next.message(); messageAt = ticks; }
        if (card(selected) == null) selected = "";
        rebuildWidgets();
    }
    private NoticeBoardPayload.Card card(String id) {
        for (var c : data.notices()) if (c.id().equals(id)) return c;
        return null;
    }
    private void send(String village, String notice, String action) {
        long now = System.currentTimeMillis();
        if (now - sent < 250 || !ClientPlayNetworking.canSend(NoticeActionPayload.TYPE)) return;
        sent = now;
        ClientPlayNetworking.send(new NoticeActionPayload(village, notice, action, data.pos()));
    }
    private static ItemStack stack(String id) {
        if (id == null || id.isEmpty()) return ItemStack.EMPTY;
        var item = BuiltInRegistries.ITEM.getValue(Identifier.tryParse(id));
        return item == null || item == Items.AIR ? ItemStack.EMPTY : new ItemStack(item);
    }
    private void click() { if (minecraft != null) minecraft.getSoundManager().play(SimpleSoundInstance.forUI(SoundEvents.BOOK_PAGE_TURN, 1.2F, .5F)); }

    // -- layout ------------------------------------------------------------------------------------

    @Override protected void init() {
        w = Math.min(500, width - 12); h = Math.min(310, height - 12);
        x = (width - w) / 2; y = (height - h) / 2;
        int top = y + 38, bottom = y + h - 30;
        corkX = x + 10; corkY = top; corkW = (w - 26) * 3 / 5; corkH = bottom - top;
        pageX = corkX + corkW + 6; pageY = top; pageW = x + w - 10 - pageX; pageH = corkH;
        cardW = (corkW - 16) / 3; cardH = Math.min(78, (corkH - 22) / 2);
        page = Math.clamp(page, 0, pages() - 1);
        addRenderableWidget(new ConversationButton(x + w - 66, y + h - 24, 56, 18, "Close", true, b -> onClose()));
        addRenderableWidget(new ConversationButton(x + w - 66 - 98, y + h - 24, 92, 18, "Village Ledger", false, b -> send(data.village(), "", "ledger")));
        if (pages() > 1) {
            addRenderableWidget(new ConversationButton(corkX + corkW - 46, corkY + corkH - 16, 20, 14, "<", false, b -> { page = Math.max(0, page - 1); rebuildWidgets(); }));
            addRenderableWidget(new ConversationButton(corkX + corkW - 24, corkY + corkH - 16, 20, 14, ">", false, b -> { page = Math.min(pages() - 1, page + 1); rebuildWidgets(); }));
        }
        var card = card(selected);
        if (card != null) {
            int by = pageY + pageH - 22, bw = (pageW - 18) / 2;
            switch (card.state()) {
                case "open" -> addRenderableWidget(new ConversationButton(pageX + 6, by, pageW - 12, 18, card.kind().equals("letter") ? "Take the letter" : "Take this notice", true,
                        b -> { click(); send(data.village(), card.id(), "accept"); }));
                case "ready" -> {
                    if (!card.kind().equals("letter")) addRenderableWidget(new ConversationButton(pageX + 6, by, bw, 18, "Turn it in", true, b -> send(data.village(), card.id(), "claim")));
                    addRenderableWidget(new ConversationButton(pageX + 12 + bw, by, bw, 18, "Pin it back", false, b -> send(data.village(), card.id(), "abandon")));
                }
                case "mine" -> addRenderableWidget(new ConversationButton(pageX + 6, by, pageW - 12, 18, "Pin it back up", false, b -> { click(); send(data.village(), card.id(), "abandon"); }));
                default -> {}
            }
            addRenderableWidget(new ConversationButton(pageX + pageW - 46, pageY + 4, 40, 14, "Back", false, b -> { selected = ""; rebuildWidgets(); }));
        } else {
            // Drop a notice from any village from the overview.
            int row = 0;
            for (var task : data.tasks()) {
                int ty = pageY + 20 + row * 30;
                if (ty + 26 > pageY + pageH / 2 + 30) break;
                var drop = new ConversationButton(pageX + pageW - 22, ty + 4, 14, 12, "x", false, b -> send(task.village(), task.id(), "abandon"));
                drop.setTooltip(net.minecraft.client.gui.components.Tooltip.create(Component.literal("Pin it back up")));
                addRenderableWidget(drop);
                row++;
            }
        }
    }
    private int perPage() { return 6; }
    private int pages() { return Math.max(1, (data.notices().size() + perPage() - 1) / perPage()); }
    @Override public boolean isPauseScreen() { return false; }
    @Override public void tick() {
        ticks++;
        var player = minecraft.player;
        if (player == null || !player.isAlive() || player.distanceToSqr(net.minecraft.world.phys.Vec3.atCenterOf(BlockPos.of(data.pos()))) > 10 * 10) onClose();
    }

    // -- input -------------------------------------------------------------------------------------

    @Override public boolean mouseClicked(MouseButtonEvent event, boolean doubleClick) {
        if (hovered >= 0 && hovered < data.notices().size()) {
            var id = data.notices().get(hovered).id();
            selected = id.equals(selected) ? "" : id;
            click(); rebuildWidgets();
            return true;
        }
        return super.mouseClicked(event, doubleClick);
    }

    // -- drawing -----------------------------------------------------------------------------------

    @Override public void extractBackground(GuiGraphicsExtractor g, int mouseX, int mouseY, float delta) { g.fill(0, 0, width, height, 0xC0100C08); }
    @Override public void extractRenderState(GuiGraphicsExtractor g, int mouseX, int mouseY, float delta) {
        drawFrame(g);
        drawCork(g, mouseX, mouseY);
        if (card(selected) != null) drawNotice(g, card(selected)); else drawOverview(g, mouseX, mouseY);
        // Standing in the village, and what just happened.
        int footY = y + h - 21;
        g.text(font, font.plainSubstrByWidth(data.standing(), w - 190), x + 12, footY - 4, 0xFFFFE6B0, false);
        g.text(font, font.plainSubstrByWidth(data.standingHint(), w - 190), x + 12, footY + 6, 0xFFE0C79A, false);
        if (!message.isEmpty() && ticks - messageAt < 160) {
            int mw = Math.min(w - 40, font.width(message) + 12), mx = x + (w - mw) / 2, my = corkY + corkH - 14;
            g.fill(mx, my - 2, mx + mw, my + 10, 0xE0FFF8E9); g.fill(mx, my + 10, mx + mw, my + 11, 0x66000000);
            g.centeredText(font, font.plainSubstrByWidth(message, mw - 8), mx + mw / 2, my, 0xFF2F6B2A);
        }
        super.extractRenderState(g, mouseX, mouseY, delta);
    }
    private void drawFrame(GuiGraphicsExtractor g) {
        // Posts, a plank frame and a little shingle roof with the village's name carved under it.
        g.fill(x + 2, y + 4, x + w + 2, y + h + 4, 0x66000000);
        g.fill(x, y + 8, x + w, y + h, WOOD); g.fill(x + 2, y + 10, x + w - 2, y + h - 2, WOOD_LIGHT);
        for (int i = 0; i < 8; i++) g.fill(x - 4 + i, y + 8 - i, x + w + 4 - i, y + 9 - i, i % 3 == 0 ? ROOF_DARK : ROOF);
        for (int sx = x + 2; sx < x + w - 2; sx += 9) g.fill(sx, y + 1, sx + 1, y + 8, ROOF_DARK);
        String title = data.villageName() + " Notice Board";
        int tw = Math.min(w - 40, Math.max(font.width(title), font.width(data.date())) + 20), tx = x + (w - tw) / 2;
        panel(g, tx, y + 10, tw, 25, 0xFFF3DFB8);
        g.centeredText(font, font.plainSubstrByWidth(title, tw - 8), x + w / 2, y + 13, INK);
        g.centeredText(font, font.plainSubstrByWidth(data.date(), tw - 8), x + w / 2, y + 23, MUTED);
        g.fill(x + 4, y + h - 28, x + w - 4, y + h - 27, 0x55000000);
    }
    private void drawCork(GuiGraphicsExtractor g, int mouseX, int mouseY) {
        g.fill(corkX - 2, corkY - 2, corkX + corkW + 2, corkY + corkH + 2, WOOD);
        g.fill(corkX, corkY, corkX + corkW, corkY + corkH, CORK);
        // Speckles, the same every frame.
        for (int i = 0; i < corkW * corkH / 40; i++) {
            int sx = corkX + Math.floorMod(i * 73 + i * i * 31, corkW - 1), sy = corkY + Math.floorMod(i * 151 + i * i * 7, corkH - 1);
            g.fill(sx, sy, sx + 1, sy + 1, i % 3 == 0 ? CORK_LIGHT : CORK_DARK);
        }
        hovered = -1;
        var cards = data.notices();
        if (cards.isEmpty()) {
            g.centeredText(font, "Nothing pinned up today.", corkX + corkW / 2, corkY + corkH / 2 - 8, 0xFFFFF3DA);
            g.centeredText(font, "Check back tomorrow morning.", corkX + corkW / 2, corkY + corkH / 2 + 4, 0xFFF3DEB8);
            return;
        }
        int start = page * perPage();
        for (int i = start; i < Math.min(cards.size(), start + perPage()); i++) {
            int slot = i - start, col = slot % 3, row = slot / 3;
            int cx = corkX + 4 + col * (cardW + 4), cy = corkY + 6 + row * (cardH + 6) + (int) (Math.floorMod(cards.get(i).id().hashCode() + slot, 3) - 1);
            boolean hover = mouseX >= cx && mouseX < cx + cardW && mouseY >= cy && mouseY < cy + cardH;
            if (hover) hovered = i;
            drawCard(g, cards.get(i), cx, cy - (hover ? 1 : 0), hover, cards.get(i).id().equals(selected));
        }
        if (pages() > 1) g.text(font, (page + 1) + "/" + pages(), corkX + corkW - 70, corkY + corkH - 13, 0xFFFFF3DA, false);
    }
    private static int paper(String kind) {
        return switch (kind) { case "hunt" -> 0xFFF7E1CF; case "letter" -> 0xFFDDEBF4; case "birthday" -> 0xFFFADCE7; default -> 0xFFFFF5DC; };
    }
    private static int pin(String kind) {
        return switch (kind) { case "hunt" -> 0xFFC8423A; case "letter" -> 0xFF4E9A5A; case "birthday" -> 0xFFE7B33C; default -> 0xFF4A74B8; };
    }
    private void drawCard(GuiGraphicsExtractor g, NoticeBoardPayload.Card c, int cx, int cy, boolean hover, boolean picked) {
        int paper = paper(c.kind());
        g.fill(cx + 2, cy + cardH, cx + cardW, cy + cardH + 2, 0x44000000);
        g.fill(cx, cy, cx + cardW, cy + cardH, picked ? 0xFF8A5528 : 0xFFB89A74);
        g.fill(cx + 1, cy + 1, cx + cardW - 1, cy + cardH - 1, hover ? 0xFFFFFFFF : paper);
        // A torn bottom edge and the pin.
        for (int i = cx + 1; i < cx + cardW - 1; i += 4) g.fill(i, cy + cardH - 2, i + 2, cy + cardH - 1, 0xFFE8D9C0);
        int px = cx + cardW / 2 - 2;
        g.fill(px, cy - 2, px + 5, cy + 3, darker(pin(c.kind()))); g.fill(px + 1, cy - 1, px + 4, cy + 2, pin(c.kind())); g.fill(px + 1, cy - 1, px + 2, cy, 0xFFFFFFFF);
        var icon = stack(c.icon());
        if (!icon.isEmpty()) g.item(icon, cx + 3, cy + 5);
        int textX = cx + 21, textW = cardW - 24;
        var lines = wrap(c.title(), textW);
        for (int l = 0; l < Math.min(2, lines.size()); l++) g.text(font, lines.get(l), textX, cy + 5 + l * 9, INK, false);
        g.text(font, font.plainSubstrByWidth(c.poster(), cardW - 8), cx + 4, cy + 25, MUTED, false);
        if (cardH >= 60) {
            var body = wrap(c.text(), cardW - 8);
            for (int l = 0; l < Math.min((cardH - 50) / 9, body.size()); l++) g.text(font, body.get(l), cx + 4, cy + 35 + l * 9, 0xFF6F5A45, false);
        }
        int footY = cy + cardH - 13;
        switch (c.state()) {
            case "taken" -> { g.fill(cx + 1, cy + 1, cx + cardW - 1, cy + cardH - 1, 0x88B7AA94); stamp(g, "Taken", cx + cardW / 2, footY, 0xFF7E7262); }
            case "mine" -> stamp(g, c.count() > 1 && !c.kind().equals("letter") ? "In hand " + c.progress() + "/" + c.count() : "In hand", cx + cardW / 2, footY, 0xFF4A74B8);
            case "ready" -> stamp(g, "Ready!", cx + cardW / 2, footY, GOOD);
            default -> {
                g.item(new ItemStack(Items.EMERALD), cx + 3, footY - 4);
                g.text(font, font.plainSubstrByWidth(c.reward().split(" · ")[0], cardW - 24), cx + 21, footY, SAGE, false);
            }
        }
    }
    private void stamp(GuiGraphicsExtractor g, String text, int cx, int cy, int color) {
        int tw = font.width(text) + 8;
        g.fill(cx - tw / 2, cy - 2, cx + tw / 2, cy + 9, color); g.fill(cx - tw / 2 + 1, cy - 1, cx + tw / 2 - 1, cy + 8, 0xFFFFFBF0);
        g.centeredText(font, text, cx, cy, color);
    }
    private void drawNotice(GuiGraphicsExtractor g, NoticeBoardPayload.Card c) {
        panel(g, pageX, pageY, pageW, pageH, paper(c.kind()));
        int left = pageX + 8, textW = pageW - 16, yy = pageY + 7;
        var icon = stack(c.icon());
        if (!icon.isEmpty()) g.item(icon, left, yy);
        for (var line : wrap(c.title(), textW - 66)) { g.text(font, line, left + 20, yy + 1, INK, false); yy += 9; }
        yy = Math.max(yy, pageY + 25) + 2;
        g.text(font, font.plainSubstrByWidth(c.poster() + " · " + c.posterJob(), textW), left, yy, MUTED, false); yy += 13;
        var objective = wrap(c.objective(), textW); var reward = wrap("Reward: " + c.reward(), textW);
        int footer = objective.size() * LINE + reward.size() * LINE + 38;
        int bottom = pageY + pageH - footer - 4;
        for (var line : wrap("“" + c.text() + "”", textW)) { if (yy > bottom) break; g.text(font, line, left, yy, 0xFF5E4A38, false); yy += LINE; }
        yy = Math.max(yy + 4, pageY + pageH - footer);
        g.fill(left, yy - 3, left + textW, yy - 2, 0x33000000);
        for (var line : objective) { g.text(font, line, left, yy, INK, false); yy += LINE; }
        yy += 1;
        if (!c.state().equals("open") && !c.state().equals("taken") && c.count() > 1 && !c.kind().equals("letter")) {
            g.fill(left, yy, left + textW, yy + 4, 0xFFE3D6C0);
            g.fill(left, yy, left + textW * Math.min(c.progress(), c.count()) / c.count(), yy + 4, c.state().equals("ready") ? GOOD : 0xFF6DB56A);
            yy += 7;
        }
        for (var line : reward) { g.text(font, line, left, yy, SAGE, false); yy += LINE; }
        g.text(font, font.plainSubstrByWidth(c.due(), textW), left, yy, c.state().equals("ready") ? GOOD : MUTED, false);
    }
    private void drawOverview(GuiGraphicsExtractor g, int mouseX, int mouseY) {
        panel(g, pageX, pageY, pageW, pageH, PAPER);
        int left = pageX + 8, textW = pageW - 16, yy = pageY + 7;
        g.text(font, "Your notices (" + data.tasks().size() + "/3)", left, yy, INK, false); yy += 13;
        if (data.tasks().isEmpty()) { g.text(font, font.plainSubstrByWidth("Click a notice to read it.", textW), left, yy + 4, MUTED, false); yy += 30; }
        int half = pageY + pageH / 2 + 30;
        for (var task : data.tasks()) {
            if (yy + 26 > half) break;
            var icon = stack(task.icon());
            if (!icon.isEmpty()) g.item(icon, left, yy + 2);
            g.text(font, font.plainSubstrByWidth(task.title(), textW - 40), left + 19, yy + 1, INK, false);
            g.text(font, font.plainSubstrByWidth((task.ready() ? "Ready! " : "") + task.progress() + " · " + task.where(), textW - 40), left + 19, yy + 11, task.ready() ? GOOD : MUTED, false);
            yy += 30;
        }
        yy = Math.max(yy, half - 30) + 4;
        g.fill(left, yy - 4, left + textW, yy - 3, 0x33000000);
        g.text(font, "Birthdays", left, yy, HEART, false); yy += 12;
        if (data.birthdays().isEmpty()) g.text(font, "Nobody has told the board yet.", left, yy, MUTED, false);
        for (var line : data.birthdays()) {
            if (yy > pageY + pageH - 12) break;
            boolean today = line.startsWith("Today");
            g.text(font, font.plainSubstrByWidth(line, textW), left, yy, today ? HEART : INK, false);
            yy += 10;
        }
    }
    private List<String> wrap(String text, int width) {
        return new ArrayList<>(font.splitIgnoringLanguage(Component.literal(text), Math.max(20, width)).stream().map(t -> t.getString()).toList());
    }
}
