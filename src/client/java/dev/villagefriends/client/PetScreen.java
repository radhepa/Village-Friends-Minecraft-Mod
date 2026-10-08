package dev.villagefriends.client;

import static dev.villagefriends.client.FriendshipScreen.*;

import dev.villagefriends.Emote;
import dev.villagefriends.pet.PetActionPayload;
import dev.villagefriends.pet.PetPayload;
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
 * A resident's cat or dog, on a card in the same cozy style as a resident's conversation window: the
 * pet's portrait rises out of a parchment box where a line about them types out, their name rides on
 * a ribbon, and a name-tag card at the top lists who they belong to, how old they are, their breed,
 * nature and favorite things, and how fond of you they've grown. Pat them or give them a treat from
 * the dock.
 */
public final class PetScreen extends Screen {
    private static final SoundEvent BLIP = SoundEvent.createVariableRangeEvent(Identifier.fromNamespaceAndPath("villagefriends", "ui.blip"));
    private static final SoundEvent POP = SoundEvent.createVariableRangeEvent(Identifier.fromNamespaceAndPath("villagefriends", "ui.pop"));
    private static final int CAT_RIBBON = 0xFFE0975A, DOG_RIBBON = 0xFF7C9CCF, LINE = 10, ROWS = 6;
    private static final float CHARS_PER_SECOND = 40F;

    private PetPayload data;
    private final List<Button> actions = new ArrayList<>();
    private boolean waiting;
    private int waitTicks, ticks, statusAt, emoteAt;
    private Emote emote;
    private int boxX, boxY, boxW, boxH, textX, textW, portraitX, portraitY, portraitW, portraitH, cardX, cardY, cardW, cardH;
    private List<String> lines = List.of();
    private String linesKey = "";
    private int shown, sinceBlip;
    private float budget;
    private long lastFrame;

    public PetScreen(PetPayload data) {
        super(Component.literal("Village Friends - " + data.name()));
        this.data = data;
        emote = Emote.parse(data.emote());
    }
    public boolean matches(PetPayload next) { return data.petId().equals(next.petId()); }
    public int petId() { return data.entityId(); }
    public void update(PetPayload next) {
        if (!next.line().equals(data.line())) { shown = 0; budget = 0; linesKey = ""; }
        if (!next.status().equals(data.status())) statusAt = ticks;
        var mood = Emote.parse(next.emote());
        if (mood != null) { emote = mood; emoteAt = ticks; }
        data = next;
        waiting = false; waitTicks = 0;
        rebuildWidgets();
    }

    // -- layout ------------------------------------------------------------------------------------

    @Override protected void init() {
        actions.clear();
        int dockH = 20, bottom = height - 8 - dockH - 5;
        boxW = Math.min(400, width - 16);
        boxX = (width - boxW) / 2;
        boxH = 58;
        boxY = bottom - boxH;
        portraitW = 70; portraitH = Math.min(boxH + 34, 96);
        portraitX = boxX + 7; portraitY = boxY + boxH - 7 - portraitH;
        textX = boxX + portraitW + 18; textW = boxX + boxW - 12 - textX;
        cardX = 8; cardY = 8; cardW = Math.min(214, width - 16); cardH = 40 + ROWS * LINE;
        var player = Minecraft.getInstance().player;
        ItemStack held = player == null ? ItemStack.EMPTY : player.getMainHandItem();
        boolean cat = data.cat();
        String[] labels = {"Pat", "Give treat", "Goodbye"};
        String[] ids = {"pat", "treat", "goodbye"};
        ItemStack[] icons = {new ItemStack(cat ? Items.STRING : Items.BONE), held.isEmpty() ? new ItemStack(cat ? Items.COD : Items.COOKED_BEEF) : held.copyWithCount(1),
                new ItemStack(Items.OAK_DOOR)};
        boolean wide = width >= 420;
        int each = wide ? 78 : 20, gap = 4, total = 3 * each + 2 * gap + 8, x = (width - total) / 2, y = height - 8 - dockH;
        for (int i = 0; i < 3; i++) {
            if (i == 2) x += 8;
            String id = ids[i];
            var button = new DockButton(x, y, each, dockH, labels[i], icons[i], false, false, wide, -1,
                    pressed -> { if (id.equals("goodbye")) onClose(); else send(id); });
            button.setTooltip(Tooltip.create(Component.literal(switch (id) {
                case "pat" -> "Pat " + data.name() + (cat ? ". Cats like chin scratches." : ". Good dog!");
                case "treat" -> "Give a treat from your hand: " + (cat ? "cod or salmon" : "meat") + ". " + data.name() + " loves " + data.treat().toLowerCase() + ".";
                default -> "Goodbye (Esc)";
            })));
            if (!id.equals("goodbye")) { button.active = !waiting; actions.add(button); }
            addRenderableWidget(button);
            x += each + gap;
        }
    }
    private void send(String action) {
        if (waiting || !ClientPlayNetworking.canSend(PetActionPayload.TYPE)) return;
        ClientPlayNetworking.send(new PetActionPayload(data.entityId(), data.petId(), action));
        waiting = true; waitTicks = 0;
        emote = Emote.DOTS; emoteAt = ticks;
        actions.forEach(b -> b.active = false);
    }

    // -- input -------------------------------------------------------------------------------------

    @Override public boolean keyPressed(KeyEvent event) {
        if (event.key() == 32 && typing()) { shown = flat().length(); return true; }
        return super.keyPressed(event);
    }
    @Override public boolean mouseClicked(MouseButtonEvent event, boolean doubleClick) {
        if (typing() && event.x() >= boxX && event.x() < boxX + boxW && event.y() >= boxY && event.y() < boxY + boxH) { shown = flat().length(); return true; }
        return super.mouseClicked(event, doubleClick);
    }
    @Override public void tick() {
        ticks++;
        if (minecraft.player == null || minecraft.level == null) { onClose(); return; }
        var pet = minecraft.level.getEntity(data.entityId());
        if (pet == null || !pet.isAlive() || !pet.getUUID().equals(data.petId()) || minecraft.player.distanceToSqr(pet) > 64 || !minecraft.player.isAlive()) { onClose(); return; }
        if (waiting && ++waitTicks > 100) { waiting = false; rebuildWidgets(); }
    }
    @Override public boolean isPauseScreen() { return false; }
    @Override public boolean isInGameUi() { return true; }
    @Override public Component getNarrationMessage() {
        return Component.literal(data.name() + ", " + data.stage() + ". " + (data.owner().isEmpty() ? "" : "Belongs to " + data.owner() + ". ") + data.line());
    }

    // -- typing ------------------------------------------------------------------------------------

    private String flat() { return String.join("", lines); }
    private boolean typing() { return shown < flat().length(); }
    private void layout() {
        String key = data.line() + '|' + textW;
        if (key.equals(linesKey)) return;
        linesKey = key;
        lines = font.splitIgnoringLanguage(Component.literal(data.line()), textW).stream().map(t -> t.getString()).toList();
    }
    private void advance() {
        long now = System.nanoTime();
        float dt = lastFrame == 0 ? 0 : Math.min(.1F, (now - lastFrame) / 1.0E9F);
        lastFrame = now;
        String all = flat();
        if (shown == 0 && budget == 0 && !all.isEmpty()) play(POP, 1.15F, .45F);
        budget += dt;
        while (shown < all.length() && budget >= 1 / CHARS_PER_SECOND) {
            budget -= 1 / CHARS_PER_SECOND;
            char c = all.charAt(shown++);
            // A higher, quicker blip than a resident's voice: the narrator describing the pet.
            if (!Character.isWhitespace(c) && ++sinceBlip >= 3) { sinceBlip = 0; play(BLIP, 1.35F + Character.toLowerCase(c) % 7 * .04F, .22F); }
        }
    }
    private void play(SoundEvent sound, float pitch, float volume) { if (minecraft != null) minecraft.getSoundManager().play(SimpleSoundInstance.forUI(sound, pitch, volume)); }

    // -- drawing -----------------------------------------------------------------------------------

    @Override public void extractBackground(GuiGraphicsExtractor g, int mouseX, int mouseY, float delta) {
        g.fillGradient(0, height / 2, width, height, 0x00000000, 0x660D0906);
    }
    @Override public void extractRenderState(GuiGraphicsExtractor g, int mouseX, int mouseY, float delta) {
        float now = ticks + delta;
        drawCard(g, mouseX, mouseY);
        panel(g, boxX, boxY, boxW, boxH, PAPER);
        frame(g, portraitX - 2, portraitY - 2, portraitW + 4, portraitH + 4);
        g.fillGradient(portraitX, portraitY, portraitX + portraitW, portraitY + portraitH, data.cat() ? 0xFFF3DCC2 : 0xFFD3E2EE, 0xFFF4EBCF);
        if (minecraft.level != null && minecraft.level.getEntity(data.entityId()) instanceof LivingEntity pet) {
            float size = Math.max(pet.getBbHeight(), pet.getBbWidth() * 1.35F);
            int scale = (int) Math.min(portraitW * .62F / size, 140);
            InventoryScreen.extractEntityInInventoryFollowsMouse(g, portraitX, portraitY + 6, portraitX + portraitW, portraitY + portraitH - 4,
                    scale, .1F, mouseX, mouseY, pet);
        }
        drawEmote(g, portraitX + portraitW - 8, portraitY - 6, now);
        drawRibbon(g, mouseX, mouseY);
        layout(); advance();
        int y = boxY + 9;
        int left = shown;
        for (int i = 0; i < Math.min(lines.size(), 3); i++, y += LINE) {
            String line = lines.get(i);
            int chars = Math.min(line.length(), left);
            if (chars <= 0) break;
            g.text(font, line.substring(0, chars), textX, y, INK, false);
            left -= line.length();
        }
        int statusY = boxY + boxH - 13;
        g.fill(textX, statusY - 3, textX + textW, statusY - 2, PAPER_SHADE);
        String status = waiting ? "..." : data.status();
        g.text(font, font.plainSubstrByWidth(status, textW - 12), textX, statusY, now - statusAt < 40 ? 0xFF2F8F3A : SAGE, false);
        if (mouseX >= textX && mouseX < textX + textW && mouseY >= statusY - 2 && mouseY < statusY + 9 && font.width(status) > textW - 12)
            g.setTooltipForNextFrame(Component.literal(status), mouseX, mouseY);
        if (!typing() && !waiting) {
            int bounce = (int) (Math.abs(Mth.sin(now * .25F)) * 2), ax = boxX + boxW - 14, ay = statusY + 1 + bounce;
            for (int i = 0; i < 4; i++) g.fill(ax + i, ay + i, ax + 7 - i, ay + i + 1, EDGE_LIGHT);
        }
        super.extractRenderState(g, mouseX, mouseY, delta);
    }

    /** The name-tag card: species and nature, fondness hearts, and the facts about them. */
    private void drawCard(GuiGraphicsExtractor g, int mouseX, int mouseY) {
        panel(g, cardX, cardY, cardW, cardH, PAPER);
        int color = data.cat() ? CAT_RIBBON : DOG_RIBBON;
        String badge = data.stage();
        int badgeW = font.width(badge) + 10;
        pill(g, cardX + 6, cardY + 6, badgeW, 12, color);
        g.text(font, badge, cardX + 11, cardY + 8, 0xFFFFFFFF, true);
        g.text(font, font.plainSubstrByWidth(data.personality(), cardW - badgeW - 18), cardX + badgeW + 11, cardY + 8, INK, false);
        int hx = cardX + 7, hy = cardY + 23;
        for (int i = 0; i < 10; i++) heart(g, hx + i * 9, hy, Math.clamp((data.fondness() - i * 10) / 10F, 0, 1));
        g.text(font, font.plainSubstrByWidth(data.fondnessLabel(), cardW - 104), hx + 96, hy - 1, MUTED, false);
        String[][] rows = {
                {"Owner", data.owner() + (data.ownerDetail().isEmpty() ? "" : " · " + data.ownerDetail())},
                {"Age", data.age().isEmpty() ? data.stage() : data.age()},
                {"Breed", data.breed().isEmpty() ? "Mixed" : data.breed()},
                {"Loves", data.game() + " · " + data.treat()},
                {"Home", data.adopted().isEmpty() ? "Looking for one" : data.adopted()},
                {"Health", health()}};
        int labelW = 0;
        for (var row : rows) labelW = Math.max(labelW, font.width(row[0]));
        int y = cardY + 36;
        for (var row : rows) {
            g.text(font, row[0], cardX + 7, y, MUTED, false);
            int vx = cardX + 13 + labelW, room = cardX + cardW - 7 - vx;
            g.text(font, font.plainSubstrByWidth(row[1], room), vx, y, INK, false);
            if (mouseX >= vx && mouseX < vx + room && mouseY >= y - 1 && mouseY < y + 9 && font.width(row[1]) > room)
                g.setTooltipForNextFrame(Component.literal(row[1]), mouseX, mouseY);
            y += LINE;
        }
        if (mouseX >= hx && mouseX < hx + 90 && mouseY >= hy - 1 && mouseY < hy + 7)
            g.setTooltipForNextFrame(Component.literal(data.fondness() + " fondness: " + data.fondnessLabel() + ". Pat them and bring treats to win them over."), mouseX, mouseY);
    }
    private String health() {
        int hearts = Math.round(data.health() / 2), max = Math.round(data.maxHealth() / 2);
        if (data.health() >= data.maxHealth()) return "Healthy (" + hearts + " hearts)";
        return hearts + " of " + max + " hearts" + (data.health() < data.maxHealth() / 2 ? ". A treat would help." : "");
    }
    private void drawRibbon(GuiGraphicsExtractor g, int mouseX, int mouseY) {
        int color = data.cat() ? CAT_RIBBON : DOG_RIBBON;
        String name = font.plainSubstrByWidth(data.name(), boxW - portraitW - 40);
        int w = font.width(name) + 14, x = textX - 4, y = boxY - 12;
        g.fill(x + 1, y + 1, x + w + 1, y + 14, 0x55000000);
        g.fill(x, y, x + w, y + 13, color);
        g.fill(x, y + 11, x + w, y + 13, darker(color));
        g.fill(x - 1, y + 1, x, y + 12, darker(color)); g.fill(x + w, y + 1, x + w + 1, y + 12, darker(color));
        g.text(font, name, x + 7, y + 3, 0xFFFFFFFF, true);
        String whose = data.owner().isEmpty() || data.owner().equals("No one yet") ? "Stray " + data.species() : data.owner() + "'s " + data.species();
        String subtitle = whose + (data.breed().isEmpty() ? "" : " · " + data.breed());
        int room = boxX + boxW - (x + w + 6) - 6;
        if (room > 40) g.text(font, font.plainSubstrByWidth(subtitle, room), x + w + 6, y + 3, 0xFFF4E9D6, true);
        if (mouseX >= x && mouseX < x + w && mouseY >= y && mouseY < y + 13) g.setTooltipForNextFrame(Component.literal(subtitle), mouseX, mouseY);
    }
    private void drawEmote(GuiGraphicsExtractor g, int x, int y, float now) {
        if (emote == null) return;
        float age = now - emoteAt, life = EmoteBubbles.length(emote) + 40;
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
}
