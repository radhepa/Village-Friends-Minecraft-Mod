package dev.villagefriends.client;

import dev.villagefriends.fishing.Catches;
import dev.villagefriends.fishing.Fish;
import dev.villagefriends.fishing.FishTable;
import dev.villagefriends.fishing.Fishing;
import dev.villagefriends.fishing.FishingItems;
import dev.villagefriends.fishing.Journal;
import dev.villagefriends.fishing.Tales;
import dev.villagefriends.social.Calendar;
import java.util.List;
import net.fabricmc.fabric.api.attachment.v1.AttachmentTarget;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.input.KeyEvent;
import net.minecraft.client.input.MouseButtonEvent;
import net.minecraft.client.renderer.RenderPipelines;
import net.minecraft.client.resources.sounds.SimpleSoundInstance;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.item.ItemStack;

/**
 * The Angler's Journal: an open book. The left page holds every fish in the table, thirty to a page; a fish
 * you haven't caught is a dark silhouette. The right page tells you about the one you point at: its name,
 * rarity, how many you've caught, your record and when you first landed one, where and when it bites, and the
 * journal note; an uncaught fish is "???", unless it's a legend whose tall tale you've heard.
 */
public final class JournalScreen extends Screen {
    private static final Identifier BOOK = FishingClient.id("textures/gui/fishing/journal.png");
    private static final Identifier SLOT = FishingClient.id("fishing/journal/slot"), SLOT_SELECTED = FishingClient.id("fishing/journal/slot_selected"),
            STAR = FishingClient.id("fishing/journal/star"), STAR_EMPTY = FishingClient.id("fishing/journal/star_empty");
    private static final Identifier PAGE_FORWARD = Identifier.withDefaultNamespace("recipe_book/page_forward"),
            PAGE_FORWARD_HOVER = Identifier.withDefaultNamespace("recipe_book/page_forward_highlighted"),
            PAGE_BACK = Identifier.withDefaultNamespace("recipe_book/page_backward"),
            PAGE_BACK_HOVER = Identifier.withDefaultNamespace("recipe_book/page_backward_highlighted");
    static final int W = 280, H = 180, COLUMNS = 5, ROWS = 6, PER_PAGE = COLUMNS * ROWS, PITCH = 22;
    private static final int INK = 0xFF3B2A1A, FADED = 0xFF7A6448, GOLD = 0xFF9A6A10;
    private static int page, selected;
    private final List<Fish> fish = List.copyOf(FishTable.all());
    private int hovered = -1;

    public JournalScreen() { super(Component.literal("Angler's Journal")); }

    private int left() { return (width - W) / 2; }
    private int top() { return (height - H) / 2; }
    private int pages() { return Math.max(1, (fish.size() + PER_PAGE - 1) / PER_PAGE); }
    private Journal journal() {
        var player = minecraft == null ? null : minecraft.player;
        return player == null ? Journal.EMPTY : ((AttachmentTarget) player).getAttachedOrElse(Fishing.JOURNAL, Journal.EMPTY);
    }
    @Override public boolean isPauseScreen() { return false; }

    @Override public void extractRenderState(GuiGraphicsExtractor g, int mouseX, int mouseY, float delta) {
        super.extractRenderState(g, mouseX, mouseY, delta);
        int x = left(), y = top();
        page = Math.clamp(page, 0, pages() - 1);
        g.blit(RenderPipelines.GUI_TEXTURED, BOOK, x, y, 0, 0, W, H, 512, 256);
        var journal = journal();
        // Left page: the fish.
        g.text(font, "Angler's Journal", x + 18, y + 16, INK, false);
        String count = journal.species() + "/" + fish.size();
        g.text(font, count, x + 130 - font.width(count), y + 16, FADED, false);
        hovered = -1;
        for (int n = 0; n < PER_PAGE; n++) {
            int index = page * PER_PAGE + n;
            if (index >= fish.size()) break;
            int cx = x + 19 + (n % COLUMNS) * PITCH, cy = y + 29 + (n / COLUMNS) * PITCH;
            boolean over = mouseX >= cx && mouseX < cx + 20 && mouseY >= cy && mouseY < cy + 20;
            if (over) hovered = index;
            g.blitSprite(RenderPipelines.GUI_TEXTURED, index == selected || over ? SLOT_SELECTED : SLOT, cx, cy, 20, 20);
            var f = fish.get(index);
            if (journal.caught(f.id())) g.item(FishingItems.stack(f.item(), 1), cx + 2, cy + 2);
            else g.blitSprite(RenderPipelines.GUI_TEXTURED, silhouette(f), cx + 2, cy + 2, 16, 16);
        }
        // Right page: the one pointed at.
        detail(g, x + 148, y + 16, fish.get(Math.clamp(hovered >= 0 ? hovered : selected, 0, fish.size() - 1)), journal);
        if (pages() > 1) {
            int by = y + 150;
            if (page > 0) g.blitSprite(RenderPipelines.GUI_TEXTURED, over(mouseX, mouseY, x + 150, by, 12, 17) ? PAGE_BACK_HOVER : PAGE_BACK, x + 150, by, 12, 17);
            if (page < pages() - 1) g.blitSprite(RenderPipelines.GUI_TEXTURED, over(mouseX, mouseY, x + 252, by, 12, 17) ? PAGE_FORWARD_HOVER : PAGE_FORWARD, x + 252, by, 12, 17);
            String p = (page + 1) + " / " + pages();
            g.text(font, p, x + 207 - font.width(p) / 2, by + 5, FADED, false);
        }
    }
    static Identifier silhouette(Fish f) { return FishingClient.id("fishing/silhouette/" + f.id()); }

    private void detail(GuiGraphicsExtractor g, int x, int y, Fish f, Journal journal) {
        var entry = journal.entry(f.id());
        boolean caught = entry != null, tale = f.legendary() && journal.heard(f.id());
        g.pose().pushMatrix();
        g.pose().translate(x, y);
        g.pose().scale(2, 2);
        if (caught) g.item(FishingItems.stack(f.item(), 1), 0, 0);
        else g.blitSprite(RenderPipelines.GUI_TEXTURED, silhouette(f), 0, 0, 16, 16);
        g.pose().popMatrix();
        String name = caught || tale ? f.name() : "???";
        g.text(font, font.plainSubstrByWidth(name, 82), x + 36, y + 4, caught ? INK : FADED, false);
        for (int i = 0; i < 5; i++)
            g.blitSprite(RenderPipelines.GUI_TEXTURED, i < f.rarity().stars() ? STAR : STAR_EMPTY, x + 36 + i * 8, y + 16, 7, 7);
        g.text(font, f.rarity().label, x + 36, y + 25, f.legendary() ? GOLD : FADED, false);
        int ty = y + 39;
        if (caught) {
            ty = line(g, "Caught: " + entry.count(), x, ty, INK);
            ty = line(g, "Record: " + Catches.cm(entry.best()), x, ty, INK);
            ty = line(g, "First: " + Calendar.date(entry.first()) + ", Year " + Calendar.year(entry.first()), x, ty, INK);
            ty += 3;
            ty = wrap(g, "Lives in " + Tales.where(f) + (f.time().isEmpty() && f.weather().equals("any") && f.season().isEmpty() ? "." : ", and bites " + Tales.when(f) + "."), x, ty, FADED);
            ty += 3;
            wrap(g, f.text(), x, ty, INK);
        } else if (tale) {
            ty = wrap(g, "A tall tale: " + f.name() + " lives in " + Tales.where(f) + " and bites " + Tales.when(f) + ".", x, ty, FADED);
            wrap(g, "Not caught yet.", x, ty + 3, FADED);
        } else wrap(g, f.legendary() ? "A legend. Listen for tall tales about it in the villages." : "Not caught yet.", x, ty, FADED);
    }
    private int line(GuiGraphicsExtractor g, String text, int x, int y, int color) {
        g.text(font, font.plainSubstrByWidth(text, 118), x, y, color, false);
        return y + 10;
    }
    private int wrap(GuiGraphicsExtractor g, String text, int x, int y, int color) {
        for (var seq : font.split(Component.literal(text), 118)) {
            if (y > top() + 146) break;
            g.text(font, seq, x, y, color, false);
            y += 9;
        }
        return y;
    }
    private static boolean over(double mx, double my, int x, int y, int w, int h) { return mx >= x && mx < x + w && my >= y && my < y + h; }

    @Override public boolean mouseClicked(MouseButtonEvent event, boolean doubleClick) {
        int x = left(), y = top();
        if (pages() > 1 && page > 0 && over(event.x(), event.y(), x + 150, y + 150, 12, 17)) { page--; click(); return true; }
        if (pages() > 1 && page < pages() - 1 && over(event.x(), event.y(), x + 252, y + 150, 12, 17)) { page++; click(); return true; }
        if (hovered >= 0) { selected = hovered; click(); return true; }
        return super.mouseClicked(event, doubleClick);
    }
    @Override public boolean keyPressed(KeyEvent event) {
        if (event.input() == 262 && page < pages() - 1) { page++; return true; }  // right arrow
        if (event.input() == 263 && page > 0) { page--; return true; }           // left arrow
        return super.keyPressed(event);
    }
    private void click() {
        minecraft.getSoundManager().play(SimpleSoundInstance.forUI(SoundEvents.BOOK_PAGE_TURN, 1));
    }
    /** For tests and previews. */
    public static void show(int pageIndex, String fishId) {
        page = pageIndex;
        var all = List.copyOf(FishTable.all());
        for (int i = 0; i < all.size(); i++) if (all.get(i).id().equals(fishId)) selected = i;
    }
    static ItemStack icon(Fish f) { return FishingItems.stack(f.item(), 1); }
}
