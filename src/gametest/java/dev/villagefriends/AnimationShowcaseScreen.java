package dev.villagefriends;

import dev.villagefriends.animation.AnimationClip;
import dev.villagefriends.client.*;
import java.util.List;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.npc.villager.Villager;
import org.joml.Quaternionf;
import org.joml.Vector3f;

/**
 * Test-only gallery: real residents rendered by the real renderer, each playing one animation pack
 * clip on a loop. The test sets {@link #seconds} before every capture, so frames are exact.
 */
final class AnimationShowcaseScreen extends Screen {
    record Cell(Villager resident, AnimationClip clip, boolean mirror, String caption) {}
    private final String heading, subheading;
    private final List<Cell> cells;
    private final int cols;
    /** Showcase clock. With {@code freeze} set, every clip is held at that fraction of its length. */
    float seconds, freeze = -1;

    AnimationShowcaseScreen(String heading, String subheading, List<Cell> cells, int cols) {
        super(Component.literal("Village Friends animation showcase"));
        this.heading = heading; this.subheading = subheading; this.cells = cells; this.cols = cols;
    }
    @Override public boolean isPauseScreen() { return false; }
    @Override public void extractRenderState(GuiGraphicsExtractor g, int mx, int my, float delta) {
        g.fillGradient(0, 0, width, height, 0xFFF4E8CF, 0xFFE9D9B8);
        g.fill(0, 0, width, 44, 0xFF5A3D29);
        g.fill(0, 44, width, 46, 0xFFB98A55);
        g.text(font, heading, 18, 10, 0xFFF8E7C3, false);
        g.text(font, subheading, 18, 26, 0xFFD9BE8E, false);
        int rows = (cells.size() + cols - 1) / cols;
        int cellW = (width - 24) / cols, cellH = (height - 56) / Math.max(1, rows);
        for (int i = 0; i < cells.size(); i++) {
            var cell = cells.get(i);
            int x = 12 + i % cols * cellW, y = 52 + i / cols * cellH;
            g.fillGradient(x + 3, y + 3, x + cellW - 3, y + cellH - 3, 0xFFCFE0C4, 0xFFEFE4C8);
            g.fill(x + 3, y + cellH - 24, x + cellW - 3, y + cellH - 3, 0x22000000);
            var renderer = (ResidentRenderer) minecraft.getEntityRenderDispatcher().getRenderer(cell.resident());
            var s = renderer.createRenderState(cell.resident(), 1);
            s.shadowPieces.clear(); s.outlineColor = 0; s.nameTag = null;
            s.bodyRot = 162; s.yRot = 0; s.xRot = 0; s.onGround = true;
            s.walkAnimationPos = 0; s.walkAnimationSpeed = 0;
            s.attention = 1; s.eyeLookX = s.eyeLookY = 0; s.turnWeight = 0;
            s.ageInTicks = seconds * 20 + i * 37;
            var clip = cell.clip();
            float period = clip.length() + .8F;
            float t = freeze >= 0 ? clip.length() * freeze : (seconds + i * .23F) % period;
            float weight = freeze >= 0 ? 1 : clip.envelope(t);
            s.layers[1].clear();
            if (t <= clip.length() && weight > 0) s.layers[0].set(clip, t, weight, cell.mirror(), 1);
            else s.layers[0].clear();
            s.scale = 1;
            int size = (int) ((cellH - 34) * (s.isBaby ? .64F : .43F));
            g.entity(s, size, new Vector3f(0, s.boundingBoxHeight / 2 + (s.isBaby ? .05F : .12F), 0),
                    new Quaternionf().rotateZ((float) Math.PI), new Quaternionf(), x + 4, y + 4, x + cellW - 4, y + cellH - 26);
            g.centeredText(font, clip.name(), x + cellW / 2, y + cellH - 19, 0xFF4E382B);
            if (cell.caption() != null) g.centeredText(font, cell.caption(), x + cellW / 2, y + cellH - 10, 0xFF8B765C);
        }
    }
}
