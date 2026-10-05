package dev.villagefriends;

import java.util.List;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.ItemStack;

/** Test-only gallery of the models actually baked by Minecraft. */
final class FoundationPreviewScreen extends Screen {
    private final List<ItemStack> items;
    FoundationPreviewScreen(List<ItemStack> items) { super(Component.literal("Village Friends foundation")); this.items = items; }
    @Override public boolean isPauseScreen() { return false; }
    @Override public void extractRenderState(GuiGraphicsExtractor g, int mx, int my, float delta) {
        g.fill(0,0,width,height,0xFFF1E4CB);
        g.text(font,"VILLAGE FRIENDS / PHASE 1",16,12,0xFF4E382B,false);
        int cellWidth=(width-32)/7, cellHeight=(height-40)/((items.size()+6)/7);
        for (int n=0; n<items.size(); n++) {
            int x=16+n%7*cellWidth, y=36+n/7*cellHeight;
            g.fill(x+1,y+1,x+cellWidth-3,y+cellHeight-3,0xFFE2D6BC);
            g.item(items.get(n),x+cellWidth/2-8,y+5);
            var lines=font.split(items.get(n).getHoverName(),cellWidth-6);
            for (int line=0; line<Math.min(2,lines.size()); line++)
                g.text(font,lines.get(line),x+3,y+25+line*10,0xFF4E382B,false);
        }
    }
}
