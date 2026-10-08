package dev.villagefriends.client;

import dev.villagefriends.ActionPayload;
import dev.villagefriends.Emote;
import dev.villagefriends.FriendshipLevels;
import dev.villagefriends.FriendshipPayload;
import dev.villagefriends.VillageItems;
import java.util.ArrayList;
import java.util.List;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.components.Tooltip;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.gui.screens.inventory.InventoryScreen;
import net.minecraft.client.input.KeyEvent;
import net.minecraft.client.input.MouseButtonEvent;
import net.minecraft.client.renderer.RenderPipelines;
import net.minecraft.client.resources.sounds.SimpleSoundInstance;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;

/**
 * The conversation window, laid out like a cozy life sim. The resident stays visible in the world,
 * with their mood bubble over their head; a dialogue box with their portrait and name ribbon sits
 * at the bottom; replies float as numbered bubbles on the right; a dock of round buttons switches
 * between talking, their story, time together, travel and the journal; and a friendship card shows
 * your level as ten hearts and what the next level brings.
 */
public final class FriendshipScreen extends Screen {
    static final int INK = 0xFF4E382B, MUTED = 0xFF8B765C, PAPER = 0xFFFFF8E9, PAPER_SHADE = 0xFFF2E4C9, EDGE = 0xFF5B3A29,
            EDGE_LIGHT = 0xFFB98A5E, SAGE = 0xFF55753F, HEART = 0xFFE0567A, HEART_LIGHT = 0xFFFF9DB4, HEART_EMPTY = 0xFFE6D7C0;
    /** Name ribbon colors, one per personality. */
    private static final int[] RIBBONS = {0xFFE88A6E, 0xFF7C9CCF, 0xFFF0B84A, 0xFF5FAE8B, 0xFFB08ACF, 0xFF8DB062,
            0xFF6E8E9E, 0xFFE07FA8, 0xFFB48A5F, 0xFF5DA9C9, 0xFFC96A5A, 0xFFE3A1C0};
    private static final String[] PERSONALITIES = {"Warmhearted", "Thoughtful", "Playful", "Adventurous", "Meticulous", "Steadfast",
            "Reserved", "Imaginative", "Pragmatic", "Curious", "Protective", "Gentle"};
    /** Level badge colors by tier: neighbor, acquaintance, friend, close friend, best friend. */
    static final int[] TIERS = {0xFF9A8F80, 0xFF7FAF6A, 0xFF4FA3A5, 0xFFE0789A, 0xFFE9A93C};
    // Dialogue types out like a farming-sim textbox: a wordless blip every other letter, a pop as each line starts.
    private static final SoundEvent BLIP = SoundEvent.createVariableRangeEvent(Identifier.fromNamespaceAndPath("villagefriends", "ui.blip"));
    private static final SoundEvent POP = SoundEvent.createVariableRangeEvent(Identifier.fromNamespaceAndPath("villagefriends", "ui.pop"));
    private static final float CHARS_PER_SECOND = 36F;
    private static final int SPACE_KEY = 32, KEY_1 = 49; // GLFW keys
    private static final int LINE = 10;

    private FriendshipPayload data;
    private final List<Button> actions = new ArrayList<>();
    private boolean waiting;
    private int waitTicks, ticks;
    // Layout
    private int boxX, boxY, boxW, boxH, textX, textW, portraitX, portraitY, portraitW, portraitH, cardX, cardY, cardW, cardH;
    private int dialogueScroll;
    private String lastDialogue, lastAction;
    // Typing
    private List<String> typeLines = List.of();
    private int[] lineStarts = new int[0];
    private String typeKey = "", typeFlat = "";
    private int shown, sinceBlip;
    private float typeBudget, typePause;
    private long lastFrameNanos;
    private boolean popPending = true;
    // Moments
    private int levelUpAt = -1000, emoteAt = -1000, statusAt;
    private Emote emote;

    public FriendshipScreen(FriendshipPayload data) {
        super(Component.literal("Village Friends - " + data.name()));
        this.data = data;
        lastDialogue = data.dialogue();
        emote = Emote.parse(data.emote()); emoteAt = 0;
        if (data.opening()) ResidentLife.cue(data.entityId(), "greet");
    }
    public boolean matches(FriendshipPayload next) { return data.villagerId().equals(next.villagerId()); }
    public int residentId() { return data.entityId(); }
    public void update(FriendshipPayload next) {
        if (!lastDialogue.equals(next.dialogue())) { dialogueScroll = 0; lastDialogue = next.dialogue(); restartTyping(); }
        react(lastAction, data, next);
        lastAction = null;
        if (next.levelUp()) { levelUpAt = ticks; playUi(POP, 1.6F, .7F); ResidentLife.cue(next.entityId(), "delighted"); }
        var mood = Emote.parse(next.emote());
        if (mood != null) { emote = mood; emoteAt = ticks; }
        if (!next.status().equals(data.status())) statusAt = ticks;
        data = next;
        waiting = false;
        waitTicks = 0;
        rebuildWidgets();
        triggerImmediateNarration(false);
    }

    // -- typing ------------------------------------------------------------------------------------

    private void restartTyping() { shown = 0; typeBudget = 0; typePause = 0; sinceBlip = 0; popPending = true; }
    private boolean typing() { return shown < typeFlat.length(); }
    private boolean document() { return data.tab().equals("journal"); }
    /** A line in *asterisks* is narration (a downed companion can't speak): shown whole, no blips, no gestures. */
    private boolean narration() { var d = data.dialogue(); return d.length() > 1 && d.startsWith("*") && d.endsWith("*"); }
    private String spoken() { return narration() ? data.dialogue().substring(1, data.dialogue().length() - 1) : data.dialogue(); }
    /** True while the resident's line is still typing out: they gesture as they speak, then listen. */
    public boolean speaking() { return !document() && !narration() && (typing() || typeFlat.isEmpty()); }
    private void finishLine() { if (typing()) { shown = typeFlat.length(); playUi(POP, 1.25F, .35F); } }
    private void playUi(SoundEvent sound, float pitch, float volume) {
        if (minecraft != null) minecraft.getSoundManager().play(SimpleSoundInstance.forUI(sound, pitch, volume));
    }
    private void layoutTyping(int wrapWidth) {
        String key = data.dialogue() + '|' + wrapWidth;
        if (key.equals(typeKey)) return;
        typeKey = key;
        typeLines = font.splitIgnoringLanguage(Component.literal(spoken()), wrapWidth).stream().map(t -> t.getString()).toList();
        lineStarts = new int[typeLines.size()];
        int total = 0;
        for (int i = 0; i < lineStarts.length; i++) { lineStarts[i] = total; total += typeLines.get(i).length(); }
        typeFlat = String.join("", typeLines);
        // Journal pages appear at once; spoken lines type out.
        shown = document() || narration() ? total : Math.min(shown, total);
    }
    private void advanceTyping() {
        long now = System.nanoTime();
        float dt = lastFrameNanos == 0 ? 0F : Math.min(0.1F, (now - lastFrameNanos) / 1.0E9F);
        lastFrameNanos = now;
        if (popPending) { popPending = false; if (!document() && !narration()) playUi(POP, 0.95F + (float) Math.random() * 0.15F, 0.5F); }
        if (!typing()) return;
        typeBudget += dt;
        float cost = 1F / CHARS_PER_SECOND;
        while (typeBudget > 0 && typing()) {
            if (typePause > 0) { float used = Math.min(typePause, typeBudget); typePause -= used; typeBudget -= used; continue; }
            if (typeBudget < cost) break;
            typeBudget -= cost;
            char c = typeFlat.charAt(shown++);
            if (!Character.isWhitespace(c) && ++sinceBlip >= 2) {
                sinceBlip = 0;
                playUi(BLIP, 0.85F + Character.toLowerCase(c) % 11 * 0.045F, 0.3F);
            }
            if (".!?".indexOf(c) >= 0) typePause = 0.18F; else if (",;:".indexOf(c) >= 0) typePause = 0.08F;
        }
    }

    // -- layout ------------------------------------------------------------------------------------

    @Override protected void init() {
        actions.clear();
        int dockH = 20, bottom = height - 8 - dockH - 5;
        boxW = Math.min(430, width - 16);
        boxX = (width - boxW) / 2;
        portraitW = 64;
        textX = boxX + portraitW + 18;
        textW = boxX + boxW - 12 - textX;
        // Replies float above the box on the right: one column when there's room, otherwise two.
        int count = data.choices().size(), row = 18, baseH = 64;
        int columns = count * row > bottom - baseH - 30 ? 2 : 1;
        int rows = (count + columns - 1) / columns;
        int replyW = columns == 1 ? Math.clamp(width * 2 / 5, 130, 186) : Math.clamp((boxW - 12) / 2 - 2, 100, 170);
        boxH = document() ? Math.clamp(bottom - 10 - rows * row - 26, baseH, 200) : baseH;
        boxY = bottom - boxH;
        portraitH = Math.min(boxH + 30, 118);
        portraitX = boxX + 7;
        portraitY = boxY + boxH - 7 - portraitH;
        cardX = 8; cardY = 8; cardW = Math.min(170, width / 2 - 12); cardH = 50;
        // On wide screens they hug the right edge, leaving the resident in the middle in view.
        int replyRight = Math.max(boxX + boxW, width - 10), replyBottom = boxY - 18;
        for (int i = 0; i < count; i++) {
            var choice = data.choices().get(i);
            int column = columns == 1 ? 0 : i % 2, r = columns == 1 ? i : i / 2;
            int x = replyRight - (columns - column) * (replyW + 4) + 4, y = replyBottom - (rows - r) * row;
            var button = new ReplyButton(x, y, replyW, row - 3, i + 1, choice.label(), pressed -> send(choice.id()));
            button.active = !waiting && choice.enabled();
            if (!choice.enabled() && !choice.hint().isEmpty()) button.setTooltip(Tooltip.create(Component.literal(choice.hint())));
            actions.add(button); addRenderableWidget(button);
        }
        // The dock: conversation tabs, then gift, trade and the ledger, then goodbye.
        var player = Minecraft.getInstance().player;
        ItemStack held = player == null ? ItemStack.EMPTY : player.getMainHandItem();
        String[] labels = {"Talk", "Story", "Time", "Travel", "Journal", "Give gift", "Trade", "Village", "Goodbye"};
        String[] ids = {"talk_tab", "story", "together", "companion", "journal", "gift", "trade", "ledger", "goodbye"};
        String[] tabs = {"talk", "story", "together", "companion", "journal"};
        ItemStack[] icons = {ItemStack.EMPTY, new ItemStack(Items.BOOK), new ItemStack(Items.CAKE), new ItemStack(Items.COMPASS), new ItemStack(Items.WRITABLE_BOOK),
                held.isEmpty() ? new ItemStack(Items.POPPY) : held.copyWithCount(1), new ItemStack(Items.EMERALD), new ItemStack(VillageItems.get("village_ledger")), new ItemStack(Items.OAK_DOOR)};
        boolean wide = width >= 620;
        int each = wide ? 64 : 20, gap = 3, groupGap = 8;
        int total = 9 * each + 8 * gap + 2 * groupGap, x = (width - total) / 2, y = height - 8 - dockH;
        for (int i = 0; i < 9; i++) {
            if (i == 5 || i == 8) x += groupGap;
            String id = ids[i];
            boolean selected = i < 5 && tabs[i].equals(data.tab());
            var button = new DockButton(x, y, each, dockH, labels[i], icons[i], i == 0, selected, wide,
                    id.equals("gift") ? data.giftsLeft() : -1, pressed -> { if (id.equals("goodbye")) onClose(); else send(id); });
            button.setTooltip(Tooltip.create(Component.literal(tooltip(id, held))));
            if (id.equals("gift")) button.active = !waiting && data.giftsLeft() > 0;
            else if (id.equals("trade")) button.active = !waiting && data.canTrade();
            else if (!id.equals("goodbye")) button.active = !waiting;
            if (!id.equals("goodbye")) actions.add(button);
            addRenderableWidget(button);
            x += each + gap;
        }
    }
    private String tooltip(String id, ItemStack held) {
        return switch (id) {
            case "talk_tab" -> "Talk: everyday chat, news and heart-to-hearts";
            case "story" -> "Story: their personal four-chapter story";
            case "together" -> "Time: walks, picnics, exploring and gatherings";
            case "companion" -> "Travel: adventure together";
            case "journal" -> "Journal: memories, about them and story notes";
            case "gift" -> "Give gift: offer one " + (held.isEmpty() ? "item (hold one in your main hand)" : held.getHoverName().getString())
                    + ". " + data.giftsLeft() + " left today. " + data.giftHint();
            case "trade" -> data.canTrade() ? "Trade" : "This resident has nothing to trade";
            case "ledger" -> "Village: open the Village Ledger at their page";
            default -> "Goodbye (Esc)";
        };
    }
    private void send(String action) {
        if (waiting || !ClientPlayNetworking.canSend(ActionPayload.TYPE)) return;
        lastAction = action;
        ClientPlayNetworking.send(new ActionPayload(data.entityId(), data.villagerId(), action));
        if (action.equals("trade") || action.equals("home")) { onClose(); return; }
        if (action.equals("ledger")) return; // The ledger opens over this window.
        waiting = true;
        waitTicks = 0;
        emote = Emote.DOTS; emoteAt = ticks;
        actions.forEach(button -> button.active = false);
    }
    /** The resident's body language answers what just happened in the conversation. */
    private static void react(String action, FriendshipPayload before, FriendshipPayload after) {
        if (action == null) return;
        String trigger = switch (action) {
            case "joke" -> "laugh";
            case "gift" -> after.points() > before.points()
                    ? after.dialogue().startsWith("You remembered!") ? "delighted" : "thanks"
                    : after.status().contains("declined") || after.status().contains("kept") ? "decline" : null;
            default -> null;
        };
        if (trigger != null) ResidentLife.cue(after.entityId(), trigger);
    }

    // -- input -------------------------------------------------------------------------------------

    @Override public boolean keyPressed(KeyEvent event) {
        if (event.key() == SPACE_KEY && typing()) { finishLine(); return true; }
        int index = event.key() - KEY_1;
        if (index >= 0 && index < data.choices().size() && !waiting) {
            var choice = data.choices().get(index);
            if (choice.enabled()) { playUi(POP, 1.1F, .4F); send(choice.id()); return true; }
        }
        return super.keyPressed(event);
    }
    @Override public boolean mouseClicked(MouseButtonEvent event, boolean doubleClick) {
        if (typing() && event.x() >= boxX && event.x() < boxX + boxW && event.y() >= boxY && event.y() < boxY + boxH) { finishLine(); return true; }
        return super.mouseClicked(event, doubleClick);
    }
    @Override public boolean mouseScrolled(double x, double y, double horizontal, double vertical) {
        if (x >= boxX && x < boxX + boxW && y >= boxY && y < boxY + boxH) {
            dialogueScroll = Math.clamp(dialogueScroll - (int) Math.signum(vertical), 0, Math.max(0, typeLines.size() - visibleLines()));
            return true;
        }
        return super.mouseScrolled(x, y, horizontal, vertical);
    }
    @Override public void tick() {
        ticks++;
        if (minecraft.player == null || minecraft.level == null) { onClose(); return; }
        var villager = minecraft.level.getEntity(data.entityId());
        if (villager == null || !villager.isAlive() || !villager.getUUID().equals(data.villagerId())
                || minecraft.player.distanceToSqr(villager) > 36 || !minecraft.player.isAlive()) { onClose(); return; }
        if (waiting && ++waitTicks > 100) { waiting = false; rebuildWidgets(); }
    }
    @Override public boolean isPauseScreen() { return false; }
    @Override public boolean isInGameUi() { return true; }
    @Override public Component getNarrationMessage() {
        return Component.literal(data.name() + ", " + data.profession() + ". Friendship level " + data.friendLevel() + ", " + data.levelName()
                + ". " + data.dialogue() + " " + data.status());
    }

    // -- drawing -----------------------------------------------------------------------------------

    /** No blur: the resident and their mood bubble stay visible in the world; a soft shade lifts the text. */
    @Override public void extractBackground(GuiGraphicsExtractor g, int mouseX, int mouseY, float delta) {
        g.fillGradient(0, height / 2, width, height, 0x00000000, 0x660D0906);
    }
    private int visibleLines() { return Math.max(1, (boxH - 24) / LINE); }

    @Override public void extractRenderState(GuiGraphicsExtractor g, int mouseX, int mouseY, float delta) {
        float now = ticks + delta;
        drawCard(g, mouseX, mouseY);
        // Portrait window rising out of the dialogue box.
        panel(g, boxX, boxY, boxW, boxH, PAPER);
        frame(g, portraitX - 2, portraitY - 2, portraitW + 4, portraitH + 4);
        g.fillGradient(portraitX, portraitY, portraitX + portraitW, portraitY + portraitH, 0xFFCFE3C2, 0xFFF4EBCF);
        if (minecraft.level != null && minecraft.level.getEntity(data.entityId()) instanceof LivingEntity villager) {
            ResidentRenderer.portrait = true;
            try {
                InventoryScreen.extractEntityInInventoryFollowsMouse(g, portraitX, portraitY, portraitX + portraitW, portraitY + portraitH,
                        (int) Math.min(portraitW * 1.12, portraitH * 0.7), 0.36F, portraitX + portraitW / 2F - 10, portraitY + portraitH / 2F, villager);
            } finally { ResidentRenderer.portrait = false; }
        }
        drawEmote(g, portraitX + portraitW - 8, portraitY - 6, now);
        drawRibbon(g, mouseX, mouseY);
        // Dialogue.
        layoutTyping(textW);
        advanceTyping();
        int visible = visibleLines();
        if (typing()) {
            int lastLine = 0;
            for (int i = 0; i < lineStarts.length; i++) if (lineStarts[i] < shown) lastLine = i;
            dialogueScroll = Math.max(dialogueScroll, lastLine - visible + 1);
        }
        dialogueScroll = Math.clamp(dialogueScroll, 0, Math.max(0, typeLines.size() - visible));
        int top = boxY + 9;
        g.enableScissor(textX, top - 1, textX + textW, top + visible * LINE);
        for (int line = dialogueScroll, y = top; line < Math.min(typeLines.size(), dialogueScroll + visible); line++, y += LINE) {
            int chars = Math.min(typeLines.get(line).length(), shown - lineStarts[line]);
            if (chars <= 0) break;
            g.text(font, typeLines.get(line).substring(0, chars), textX, y, INK, false);
        }
        g.disableScissor();
        if (typeLines.size() > visible) scrollbar(g, top, visible);
        // Status along the bottom of the box, and a bouncing arrow once the line has finished.
        int statusY = boxY + boxH - 13;
        g.fill(textX, statusY - 3, textX + textW, statusY - 2, PAPER_SHADE);
        String status = waiting ? "Listening..." : data.status();
        int statusColor = now - statusAt < 40 ? 0xFF2F8F3A : SAGE;
        g.text(font, font.plainSubstrByWidth(status, textW - 12), textX, statusY, statusColor, false);
        if (mouseX >= textX && mouseX < textX + textW && mouseY >= statusY - 2 && mouseY < statusY + 9 && font.width(status) > textW - 12)
            g.setTooltipForNextFrame(Component.literal(status), mouseX, mouseY);
        if (!typing() && !waiting && !document()) {
            int bounce = (int) (Math.abs(Mth.sin(now * .25F)) * 2);
            int ax = boxX + boxW - 14, ay = statusY + 1 + bounce;
            for (int i = 0; i < 4; i++) g.fill(ax + i, ay + i, ax + 7 - i, ay + i + 1, EDGE_LIGHT);
        }
        super.extractRenderState(g, mouseX, mouseY, delta);
        drawLevelUp(g, now);
    }

    private void drawCard(GuiGraphicsExtractor g, int mouseX, int mouseY) {
        panel(g, cardX, cardY, cardW, cardH, PAPER);
        int tier = TIERS[Math.clamp(data.level(), 0, 4)];
        String badge = "Lv. " + data.friendLevel();
        int badgeW = font.width(badge) + 10;
        pill(g, cardX + 6, cardY + 6, badgeW, 12, tier);
        g.text(font, badge, cardX + 11, cardY + 8, 0xFFFFFFFF, true);
        g.text(font, font.plainSubstrByWidth(data.levelName(), cardW - badgeW - 18), cardX + badgeW + 11, cardY + 8, INK, false);
        // Ten hearts, one per level; the next one fills as you get closer.
        int floor = data.levelFloor(), next = Math.max(floor + 1, data.nextThreshold());
        float progress = data.friendLevel() >= 10 ? 0 : Math.clamp((data.points() - floor) / (float) (next - floor), 0, 1);
        int hx = cardX + 7, hy = cardY + 23;
        for (int i = 0; i < 10; i++) heart(g, hx + i * 9, hy, i < data.friendLevel() ? 1 : i == data.friendLevel() ? progress : 0);
        String goal = data.goal(), shortGoal = font.width(goal) > cardW - 12 && goal.contains(":") ? goal.substring(0, goal.indexOf(':')) : goal;
        g.text(font, font.plainSubstrByWidth(shortGoal, cardW - 12), cardX + 6, cardY + 35, MUTED, false);
        if (mouseX >= cardX && mouseX < cardX + cardW && mouseY >= cardY && mouseY < cardY + cardH) {
            var lines = new ArrayList<Component>();
            lines.add(Component.literal("Friendship Lv. " + data.friendLevel() + ": " + data.levelName()));
            lines.add(Component.literal(data.points() + " friendship points · Trust: " + data.trust()));
            lines.add(Component.literal(goal));
            if (!data.family().isEmpty()) lines.add(Component.literal(data.family()));
            g.setComponentTooltipForNextFrame(font, lines, mouseX, mouseY);
        }
    }
    private void drawRibbon(GuiGraphicsExtractor g, int mouseX, int mouseY) {
        int color = RIBBONS[Math.floorMod(java.util.Arrays.asList(PERSONALITIES).indexOf(data.personality()), RIBBONS.length)];
        String name = font.plainSubstrByWidth(data.name(), boxW - portraitW - 40);
        int w = font.width(name) + 14, x = textX - 4, y = boxY - 12;
        g.fill(x + 1, y + 1, x + w + 1, y + 14, 0x55000000);
        g.fill(x, y, x + w, y + 13, color);
        g.fill(x, y + 11, x + w, y + 13, darker(color));
        g.fill(x - 1, y + 1, x, y + 12, darker(color)); g.fill(x + w, y + 1, x + w + 1, y + 12, darker(color));
        g.text(font, name, x + 7, y + 3, 0xFFFFFFFF, true);
        boolean named = data.home().isEmpty() || data.name().endsWith(" of " + data.home());
        String subtitle = data.profession() + " · " + data.personality() + (named ? "" : " · " + data.home());
        int room = boxX + boxW - (x + w + 6) - 6;
        if (room > 40) g.text(font, font.plainSubstrByWidth(subtitle, room), x + w + 6, y + 3, 0xFFF4E9D6, true);
        if (mouseX >= x && mouseX < x + w && mouseY >= y && mouseY < y + 13)
            g.setTooltipForNextFrame(Component.literal(subtitle + (data.family().isEmpty() ? "" : "\n" + data.family())), mouseX, mouseY);
    }
    /** The resident's current mood bubble, popping in beside their portrait. */
    private void drawEmote(GuiGraphicsExtractor g, int x, int y, float now) {
        if (emote == null) return;
        float age = (now - emoteAt) * 1;
        float life = EmoteBubbles.length(emote) + 40;
        if (age > life && !waiting) return;
        var bubble = new EmoteBubbles.Bubble(emote, 0, (int) life);
        float scale = waiting ? Math.min(1, age / 5F) : EmoteBubbles.scale(bubble, age);
        if (scale <= .01F) return;
        var pose = g.pose();
        pose.pushMatrix();
        pose.translate(x + 12, y + 22 + EmoteBubbles.bob(age));
        pose.scale(scale, scale);
        g.blit(RenderPipelines.GUI_TEXTURED, EmoteBubbles.SHEET, -12, -24, EmoteBubbles.shape(emote) * 32, 0, 24, 24, 32, 32, 128, 128);
        float[] motion = EmoteBubbles.symbolMotion(emote, age);
        int symbol = EmoteBubbles.symbol(emote, age);
        pose.translate(motion[0] * .75F, -14.5F + motion[1] * .75F);
        pose.rotate(motion[3] * Mth.DEG_TO_RAD);
        pose.scale(motion[2], motion[2]);
        g.blit(RenderPipelines.GUI_TEXTURED, EmoteBubbles.SHEET, -6, -6, symbol % 8 * 16, 32 + symbol / 8 * 16, 12, 12, 16, 16, 128, 128);
        pose.popMatrix();
    }
    /** A banner that drops in when your friendship reaches a new level. */
    private void drawLevelUp(GuiGraphicsExtractor g, float now) {
        float age = now - levelUpAt;
        if (age < 0 || age > 80) return;
        float drop = age < 8 ? 1 - (float) Math.pow(1 - age / 8, 3) : age > 70 ? 1 - (age - 70) / 10 : 1;
        String title = "Friendship Lv. " + data.friendLevel() + "!";
        String perk = data.levelName() + " · " + FriendshipLevels.perk(data.friendLevel());
        int w = Math.max(font.width(title), font.width(perk)) + 40, h = 30, x = (width - w) / 2, y = (int) (-h + (h + 10) * drop);
        panel(g, x, y, w, h, 0xFFFFF1F4);
        g.centeredText(font, title, width / 2, y + 6, HEART);
        g.centeredText(font, perk, width / 2, y + 17, INK);
        for (int i = 0; i < 6; i++) {
            float a = age * .12F + i * 1.047F;
            int sx = (int) (width / 2 + Mth.cos(a) * (w / 2F + 6)), sy = (int) (y + h / 2 + Mth.sin(a) * (h / 2F + 5));
            heart(g, sx - 3, sy - 3, 1);
        }
    }
    private void scrollbar(GuiGraphicsExtractor g, int top, int visible) {
        int trackX = boxX + boxW - 6, trackH = visible * LINE;
        g.fill(trackX, top, trackX + 2, top + trackH, PAPER_SHADE);
        int thumb = Math.max(6, trackH * visible / typeLines.size());
        int offset = (trackH - thumb) * dialogueScroll / Math.max(1, typeLines.size() - visible);
        g.fill(trackX, top + offset, trackX + 2, top + offset + thumb, EDGE_LIGHT);
    }

    // -- shared drawing helpers --------------------------------------------------------------------

    /** A rounded parchment panel with an oak edge and a soft drop shadow. */
    static void panel(GuiGraphicsExtractor g, int x, int y, int w, int h, int paper) {
        g.fill(x + 1, y + h, x + w - 1, y + h + 2, 0x55000000);
        g.fill(x + 1, y, x + w - 1, y + h, EDGE); g.fill(x, y + 1, x + w, y + h - 1, EDGE);
        g.fill(x + 2, y + 1, x + w - 2, y + h - 1, paper); g.fill(x + 1, y + 2, x + w - 1, y + h - 2, paper);
        g.fill(x + 2, y + h - 3, x + w - 2, y + h - 2, PAPER_SHADE);
        g.fill(x + 2, y + 2, x + w - 2, y + 3, 0xFFFFFFFF);
    }
    static void frame(GuiGraphicsExtractor g, int x, int y, int w, int h) {
        g.fill(x + 1, y + h, x + w + 1, y + h + 2, 0x55000000);
        g.fill(x, y, x + w, y + h, EDGE);
        g.fill(x + 1, y + 1, x + w - 1, y + h - 1, EDGE_LIGHT);
    }
    static void pill(GuiGraphicsExtractor g, int x, int y, int w, int h, int color) {
        g.fill(x + 1, y, x + w - 1, y + h, color); g.fill(x, y + 1, x + w, y + h - 1, color);
        g.fill(x + 1, y + h - 2, x + w - 1, y + h - 1, darker(color));
    }
    static int darker(int color) {
        int r = (color >> 16 & 255) * 3 / 4, gr = (color >> 8 & 255) * 3 / 4, b = (color & 255) * 3 / 4;
        return 0xFF000000 | r << 16 | gr << 8 | b;
    }
    /** A 7x6 pixel heart, filled from the left by {@code fill} (0 to 1). */
    static void heart(GuiGraphicsExtractor g, int x, int y, float fill) {
        int[] masks = {0b0110110, 0b1111111, 0b1111111, 0b0111110, 0b0011100, 0b0001000};
        for (int row = 0; row < masks.length; row++) for (int col = 0; col < 7; col++) {
            if ((masks[row] & (1 << (6 - col))) == 0) continue;
            boolean filled = col < Math.round(Math.clamp(fill, 0, 1) * 7);
            int color = filled ? row <= 1 && col < 3 ? HEART_LIGHT : HEART : HEART_EMPTY;
            g.fill(x + col, y + row, x + col + 1, y + row + 1, color);
        }
    }

    /** A numbered reply bubble. Its message is the plain reply, for narration and tests. */
    static final class ReplyButton extends Button {
        private final int number;
        ReplyButton(int x, int y, int w, int h, int number, String label, OnPress action) {
            super(x, y, w, h, Component.literal(label), action, DEFAULT_NARRATION);
            this.number = number;
        }
        @Override protected void extractContents(GuiGraphicsExtractor g, int mouseX, int mouseY, float delta) {
            boolean hover = active && isHoveredOrFocused();
            int x = getX() + (hover ? -2 : 0), y = getY(), w = getWidth(), h = getHeight();
            int paper = !active ? 0xFFE7DCC8 : hover ? 0xFFFFFFFF : 0xFFFFF6E3;
            g.fill(x + 2, y + h, x + w - 2, y + h + 1, 0x44000000);
            g.fill(x + 2, y, x + w - 2, y + h, active ? EDGE : 0xFFA89A86); g.fill(x + 1, y + 1, x + w - 1, y + h - 1, active ? EDGE : 0xFFA89A86);
            g.fill(x + 2, y + 1, x + w - 2, y + h - 1, paper); g.fill(x + 1, y + 2, x + w - 1, y + h - 2, paper);
            int badge = active ? hover ? HEART : EDGE_LIGHT : 0xFFB9AD99;
            g.fill(x + 3, y + 2, x + 12, y + h - 2, badge);
            var font = Minecraft.getInstance().font;
            g.centeredText(font, String.valueOf(number), x + 8, y + (h - 8) / 2, 0xFFFFFFFF);
            String label = font.plainSubstrByWidth(getMessage().getString(), w - 20);
            g.text(font, label, x + 16, y + (h - 8) / 2, active ? INK : 0xFF9F947E, false);
        }
    }

    /** A round dock button with an item icon (and its name, on wide screens). */
    static final class DockButton extends Button {
        private final ItemStack icon;
        private final boolean talk, selected, labeled;
        private final int badge;
        DockButton(int x, int y, int w, int h, String label, ItemStack icon, boolean talk, boolean selected, boolean labeled, int badge, OnPress action) {
            super(x, y, w, h, Component.literal(label), action, DEFAULT_NARRATION);
            this.icon = icon; this.talk = talk; this.selected = selected; this.labeled = labeled; this.badge = badge;
        }
        @Override protected void extractContents(GuiGraphicsExtractor g, int mouseX, int mouseY, float delta) {
            boolean hover = active && isHoveredOrFocused();
            int x = getX(), y = getY() - (hover ? 1 : 0), w = getWidth(), h = getHeight();
            int fill = !active ? 0xFFD9CDB8 : selected ? 0xFFFFE3A6 : hover ? 0xFFFFFFFF : 0xFFF6EAD2;
            int edge = selected ? 0xFFC77B2E : !active ? 0xFFA89A86 : EDGE;
            g.fill(x + 2, y + h, x + w - 2, y + h + 2, 0x44000000);
            g.fill(x + 2, y, x + w - 2, y + h, edge); g.fill(x, y + 2, x + w, y + h - 2, edge); g.fill(x + 1, y + 1, x + w - 1, y + h - 1, edge);
            g.fill(x + 2, y + 1, x + w - 2, y + h - 1, fill); g.fill(x + 1, y + 2, x + w - 1, y + h - 2, fill);
            int iconX = labeled ? x + 3 : x + (w - 16) / 2, iconY = y + (h - 16) / 2;
            if (talk) g.blit(RenderPipelines.GUI_TEXTURED, EmoteBubbles.SHEET, iconX, iconY, 0, 0, 16, 16, 32, 32, 128, 128);
            if (talk) g.blit(RenderPipelines.GUI_TEXTURED, EmoteBubbles.SHEET, iconX + 4, iconY + 2, 0, 48, 8, 8, 16, 16, 128, 128);
            if (!talk && !icon.isEmpty()) g.item(icon, iconX, iconY);
            var font = Minecraft.getInstance().font;
            String caption = getMessage().getString().equals("Give gift") ? "Gift" : getMessage().getString();
            if (labeled) g.text(font, font.plainSubstrByWidth(caption, w - 22), x + 20, y + (h - 8) / 2, active ? INK : 0xFF9F947E, false);
            if (badge >= 0) {
                String text = String.valueOf(badge);
                int bx = x + w - 7, by = y - 3;
                g.fill(bx - 1, by, bx + 7, by + 8, badge > 0 ? HEART : 0xFF9A8F80);
                g.centeredText(font, text, bx + 3, by, 0xFFFFFFFF);
            }
            if (!active) g.fill(x + 2, y + 2, x + w - 2, y + h - 2, 0x66E7DCC8);
        }
    }
}
