package dev.villagefriends;

import dev.villagefriends.client.*;
import dev.villagefriends.outfit.*;
import java.util.List;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.npc.villager.Villager;
import org.joml.Quaternionf;
import org.joml.Vector3f;

/**
 * Test-only wardrobe gallery: the actual resident renderer and model, dressed with explicit
 * outfits, full body or head close-ups, from the front or the back.
 */
final class OutfitPreviewScreen extends Screen {
    record Cell(Outfit outfit, int complexion, String title, String subtitle, String detail) {
        Cell(Outfit outfit, int complexion, String title, String subtitle) { this(outfit, complexion, title, subtitle, ""); }
    }
    enum View { FRONT, BACK, HEAD, HEAD_BACK, WALK }
    private final Villager model;
    private final List<Cell> cells;
    private final String title, subtitle;
    private final int columns;
    private final View view;

    OutfitPreviewScreen(Villager model, List<Cell> cells, int columns, View view, String title, String subtitle) {
        super(Component.literal(title));
        this.model = model; this.cells = List.copyOf(cells); this.columns = columns; this.view = view;
        this.title = title; this.subtitle = subtitle;
    }
    @Override public boolean isPauseScreen() { return false; }
    @Override public void extractRenderState(GuiGraphicsExtractor g, int mx, int my, float delta) {
        g.fill(0, 0, width, height, 0xFFF1E4CB);
        g.text(font, title, 18, 12, 0xFF4E382B, false);
        g.text(font, subtitle, 18, 25, 0xFF77674F, false);
        int rows = (cells.size() + columns - 1) / columns, cellW = (width - 36) / columns, cellH = (height - 44) / rows;
        boolean head = view == View.HEAD || view == View.HEAD_BACK;
        var renderer = (ResidentRenderer)minecraft.getEntityRenderDispatcher().getRenderer(model);
        for (int i = 0; i < cells.size(); i++) {
            var cell = cells.get(i);
            int x = 18 + i % columns * cellW, y = 38 + i / columns * cellH;
            g.fillGradient(x + 3, y + 3, x + cellW - 3, y + cellH - 3, 0xFFD5E0CB, 0xFFEBE1C8);
            var state = renderer.createRenderState(model, 1);
            state.outfit = cell.outfit(); state.texture = ResidentSkins.texture(cell.outfit(), cell.complexion());
            state.shadowPieces.clear(); state.nameTag = null; state.outlineColor = 0;
            boolean back = view == View.BACK || view == View.HEAD_BACK;
            state.bodyRot = back ? -32 : view == View.WALK ? 118 : 148; state.yRot = head ? (back ? 0 : 6) : 8; state.xRot = 0; state.onGround = true;
            state.walkAnimationPos = view == View.WALK ? 2.2F : 0; state.walkAnimationSpeed = view == View.WALK ? .75F : 0;
            state.ageInTicks = 30;
            for (int age = 0; age < 300; age++) if (ResidentMotion.blink(age, state.motionSeed) == 0) { state.ageInTicks = age; break; }
            state.attention = 1; state.eyeLookX = 0; state.eyeLookY = 0; state.scale = 1;
            int labels = cell.subtitle().isEmpty() ? 16 : cell.detail().isEmpty() ? 28 : 40;
            if (head) {
                int size = Math.min((int)(cellW * 1.0F), (int)((cellH - labels) * 1.02F));
                g.entity(state, size, new Vector3f(0, 1.80F, 0), new Quaternionf().rotateZ((float)Math.PI), new Quaternionf(),
                    x + 6, y + 6, x + cellW - 6, y + cellH - labels - 2);
            } else {
                int size = Math.min((int)((cellH - labels - 10) * .44F), (int)(cellW * .85F));
                g.entity(state, size, new Vector3f(0, state.boundingBoxHeight / 2 + .02F, 0), new Quaternionf().rotateZ((float)Math.PI),
                    new Quaternionf(), x + 6, y + 8, x + cellW - 6, y + cellH - labels - 2);
            }
            g.centeredText(font, cell.title(), x + cellW / 2, y + cellH - labels + 2, 0xFF4E382B);
            if (!cell.subtitle().isEmpty()) g.centeredText(font, cell.subtitle(), x + cellW / 2, y + cellH - labels + 14, 0xFF77674F);
            if (!cell.detail().isEmpty()) g.centeredText(font, cell.detail(), x + cellW / 2, y + cellH - 14, 0xFF77674F);
        }
    }
}
