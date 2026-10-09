package dev.villagefriends.client;

import dev.villagefriends.hearth.Dishes;
import dev.villagefriends.hearth.Station;
import dev.villagefriends.hearth.StationBlockEntity;
import dev.villagefriends.hearth.StationMenu;
import java.util.ArrayList;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.client.input.MouseButtonEvent;
import net.minecraft.client.renderer.RenderPipelines;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.item.ItemStack;

/**
 * A kitchen station's screen: the grid, the pot's vessel or the oven's fuel, the progress arrow, the fire,
 * and a recipe book beside it. The book lists every recipe for this station (family recipes you haven't
 * learned are sealed cards); hover one for what it needs, click to fill the grid from your inventory
 * (shift-click for as many batches as you can, up to sixteen). Art: {@code tools/hearth/stations.py}.
 */
public final class StationScreen extends AbstractContainerScreen<StationMenu> {
    private static final int BOOK_W = 120, COLUMNS = 5, ROWS = 6, PER_PAGE = COLUMNS * ROWS;
    private static final Identifier BOOK = id("textures/gui/container/hearth_book.png");
    private static final Identifier PROGRESS = id("hearth/progress"), HEAT = id("hearth/heat"), FLAME = id("hearth/flame"),
            BOOK_BUTTON = id("hearth/book"), BOOK_BUTTON_HOVER = id("hearth/book_highlighted"), CELL = id("hearth/recipe"),
            CELL_HOVER = id("hearth/recipe_highlighted"), CELL_MISSING = id("hearth/recipe_missing"), UNKNOWN = id("hearth/unknown");
    private static final Identifier PAGE_FORWARD = Identifier.withDefaultNamespace("recipe_book/page_forward"),
            PAGE_FORWARD_HOVER = Identifier.withDefaultNamespace("recipe_book/page_forward_highlighted"),
            PAGE_BACK = Identifier.withDefaultNamespace("recipe_book/page_backward"),
            PAGE_BACK_HOVER = Identifier.withDefaultNamespace("recipe_book/page_backward_highlighted");
    private static boolean bookOpen = true;
    private final Identifier background;
    private int page;

    private static Identifier id(String path) { return Identifier.fromNamespaceAndPath("villagefriends", path); }

    public StationScreen(StationMenu menu, Inventory inventory, Component title) {
        super(menu, inventory, title, 176, 166);
        background = id("textures/gui/container/hearth_" + menu.station.id() + ".png");
        inventoryLabelY = 72;
    }

    @Override protected void init() {
        super.init();
        // With the book open, the station moves right to make room when the window is wide enough.
        if (bookOpen && width >= imageWidth + 2 * (BOOK_W + 2)) leftPos = (width - imageWidth + BOOK_W + 2) / 2;
        else if (bookOpen) leftPos = Math.max(BOOK_W + 2, leftPos);
    }
    private int bookX() { return leftPos - BOOK_W - 2; }
    private List<StationMenu.BookEntry> book() { return menu.opening.book(); }
    private int pages() { return Math.max(1, (book().size() + PER_PAGE - 1) / PER_PAGE); }

    // -- drawing -----------------------------------------------------------------------------------

    @Override public void extractBackground(GuiGraphicsExtractor g, int mouseX, int mouseY, float delta) {
        super.extractBackground(g, mouseX, mouseY, delta);
        g.blit(RenderPipelines.GUI_TEXTURED, background, leftPos, topPos, 0, 0, imageWidth, imageHeight, 256, 256);
        int progress = menu.data(StationBlockEntity.DATA_PROGRESS), total = menu.data(StationBlockEntity.DATA_TOTAL);
        if (total > 0 && progress > 0) {
            int w = Math.min(24, (int) Math.ceil(24.0 * progress / total));
            g.blitSprite(RenderPipelines.GUI_TEXTURED, PROGRESS, 24, 17, 0, 0, leftPos + 89, topPos + 34, w, 17);
        }
        if (menu.station == Station.POT && menu.data(StationBlockEntity.DATA_HEAT) == 1)
            g.blitSprite(RenderPipelines.GUI_TEXTURED, HEAT, leftPos + 31, topPos + 56, 14, 14);
        if (menu.station == Station.OVEN) {
            int burn = menu.data(StationBlockEntity.DATA_BURN), most = Math.max(1, menu.data(StationBlockEntity.DATA_BURN_TOTAL));
            if (burn > 0) {
                int h = Math.max(1, (int) Math.ceil(14.0 * burn / most));
                g.blitSprite(RenderPipelines.GUI_TEXTURED, FLAME, 14, 14, 0, 14 - h, leftPos + 31, topPos + 56 + 14 - h, 14, h);
            }
        }
        boolean overButton = over(mouseX, mouseY, leftPos + 5, topPos + 34, 20, 18);
        g.blitSprite(RenderPipelines.GUI_TEXTURED, overButton ? BOOK_BUTTON_HOVER : BOOK_BUTTON, leftPos + 5, topPos + 34, 20, 18);
        if (bookOpen) drawBook(g, mouseX, mouseY);
    }
    private void drawBook(GuiGraphicsExtractor g, int mouseX, int mouseY) {
        int x = bookX(), y = topPos;
        g.blit(RenderPipelines.GUI_TEXTURED, BOOK, x, y, 0, 0, BOOK_W, 166, 256, 256);
        g.text(font, Component.literal("Recipes"), x + 10, y + 8, 0xFF4A2E14, false);
        int current = menu.data(StationBlockEntity.DATA_RECIPE);
        var entries = book();
        for (int n = 0; n < PER_PAGE; n++) {
            int index = page * PER_PAGE + n;
            if (index >= entries.size()) break;
            var e = entries.get(index);
            int cx = x + 10 + (n % COLUMNS) * 20, cy = y + 22 + (n / COLUMNS) * 20;
            boolean hover = over(mouseX, mouseY, cx, cy, 20, 20);
            boolean hidden = e.secret() && !e.known();
            var cell = hidden ? CELL : hover || index == current ? CELL_HOVER : menu.canMake(minecraft.player, e) ? CELL : CELL_MISSING;
            g.blitSprite(RenderPipelines.GUI_TEXTURED, cell, cx, cy, 20, 20);
            if (hidden) g.blitSprite(RenderPipelines.GUI_TEXTURED, UNKNOWN, cx + 2, cy + 2, 16, 16);
            else g.item(e.result(), cx + 2, cy + 2);
            if (hover) g.setComponentTooltipForNextFrame(font, tooltip(e), mouseX, mouseY);
        }
        if (pages() > 1) {
            if (page > 0) g.blitSprite(RenderPipelines.GUI_TEXTURED, over(mouseX, mouseY, x + 24, y + 146, 12, 17) ? PAGE_BACK_HOVER : PAGE_BACK, x + 24, y + 146, 12, 17);
            if (page < pages() - 1) g.blitSprite(RenderPipelines.GUI_TEXTURED, over(mouseX, mouseY, x + 84, y + 146, 12, 17) ? PAGE_FORWARD_HOVER : PAGE_FORWARD, x + 84, y + 146, 12, 17);
            g.centeredText(font, Component.literal((page + 1) + "/" + pages()), x + 60, y + 151, 0xFF4A2E14);
        }
    }
    private List<Component> tooltip(StationMenu.BookEntry e) {
        var lines = new ArrayList<Component>();
        if (e.secret() && !e.known()) {
            lines.add(Component.literal("A family recipe").withStyle(ChatFormatting.GOLD));
            lines.add(Component.literal("Become a Friend of a villager and they").withStyle(ChatFormatting.GRAY));
            lines.add(Component.literal("may share theirs on a recipe card.").withStyle(ChatFormatting.GRAY));
            return lines;
        }
        lines.add(e.result().getHoverName().copy().withStyle(ChatFormatting.WHITE));
        var dish = Dishes.get(BuiltInRegistries.ITEM.getKey(e.result().getItem()).toString());
        if (dish != null && dish.dish()) lines.add(Component.literal("Well Fed " + "I".repeat(dish.tier()) + " · " + clock(dish.buff())).withStyle(ChatFormatting.GOLD));
        if (e.secret()) lines.add(Component.literal("Family recipe").withStyle(ChatFormatting.LIGHT_PURPLE));
        var needs = new ArrayList<String>();
        var counted = new java.util.LinkedHashMap<String, Integer>();
        for (var options : e.ingredients()) {
            var shown = options.isEmpty() ? ItemStack.EMPTY : options.get((int) (System.currentTimeMillis() / 1000 % options.size()));
            String name = options.size() > 1 ? "any " + ingredientWord(options) : shown.getHoverName().getString();
            counted.merge(name, 1, Integer::sum);
        }
        counted.forEach((name, n) -> needs.add(n > 1 ? name + " x" + n : name));
        if (!e.vessel().isEmpty()) needs.add("in a " + e.vessel().getHoverName().getString().toLowerCase(java.util.Locale.ROOT));
        lines.add(Component.literal(String.join(", ", needs)).withStyle(ChatFormatting.GRAY));
        lines.add(Component.literal(e.time() / 20 + "s" + (e.result().getCount() > 1 ? " · makes " + e.result().getCount() : "")).withStyle(ChatFormatting.DARK_GRAY));
        lines.add(Component.literal(menu.canMake(minecraft.player, e) ? "Click to fill · Shift: up to 16" : "You're missing something").withStyle(ChatFormatting.DARK_AQUA));
        return lines;
    }
    private static String ingredientWord(List<ItemStack> options) {
        for (var o : options) if (o.is(net.minecraft.world.item.Items.COD) || o.is(net.minecraft.world.item.Items.SALMON)) return "fish";
        return options.getFirst().getHoverName().getString();
    }
    private static String clock(int seconds) { return seconds / 60 + ":" + (seconds % 60 < 10 ? "0" : "") + seconds % 60; }
    private static boolean over(double mx, double my, int x, int y, int w, int h) { return mx >= x && my >= y && mx < x + w && my < y + h; }

    // -- input -------------------------------------------------------------------------------------

    @Override public boolean mouseClicked(MouseButtonEvent event, boolean doubleClick) {
        double mx = event.x(), my = event.y();
        if (over(mx, my, leftPos + 5, topPos + 34, 20, 18)) {
            bookOpen = !bookOpen; click(); init(); return true;
        }
        if (bookOpen) {
            int x = bookX(), y = topPos;
            if (pages() > 1 && page > 0 && over(mx, my, x + 24, y + 146, 12, 17)) { page--; click(); return true; }
            if (pages() > 1 && page < pages() - 1 && over(mx, my, x + 84, y + 146, 12, 17)) { page++; click(); return true; }
            for (int n = 0; n < PER_PAGE; n++) {
                int index = page * PER_PAGE + n;
                if (index >= book().size()) break;
                int cx = x + 10 + (n % COLUMNS) * 20, cy = y + 22 + (n / COLUMNS) * 20;
                if (!over(mx, my, cx, cy, 20, 20)) continue;
                var e = book().get(index);
                if (e.secret() && !e.known()) return true;
                minecraft.gameMode.handleInventoryButtonClick(menu.containerId, index + (event.hasShiftDown() ? StationMenu.MANY : 0));
                click();
                return true;
            }
        }
        return super.mouseClicked(event, doubleClick);
    }
    @Override protected boolean hasClickedOutside(double mx, double my, int left, int top) {
        return super.hasClickedOutside(mx, my, left, top) && !(bookOpen && over(mx, my, bookX(), topPos, BOOK_W, 166));
    }
    private void click() {
        minecraft.getSoundManager().play(net.minecraft.client.resources.sounds.SimpleSoundInstance.forUI(SoundEvents.UI_BUTTON_CLICK, 1F));
    }
}
