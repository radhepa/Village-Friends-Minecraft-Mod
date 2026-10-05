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

/** Test-only gallery: actual resident renderer, full body, no overlapping world nameplates. */
final class OutfitPreviewScreen extends Screen {
    private final List<Villager> residents;
    private final String title;
    OutfitPreviewScreen(List<Villager> residents,String title) {
        super(Component.literal(title)); this.residents=List.copyOf(residents); this.title=title;
    }
    @Override public boolean isPauseScreen() { return false; }
    @Override public void extractRenderState(GuiGraphicsExtractor g,int mx,int my,float delta) {
        g.fill(0,0,width,height,0xFFF1E4CB);
        g.text(font,title,18,14,0xFF4E382B,false);
        g.text(font,"Woven cloth / leather grain / overlap shadows / layered hair",18,29,0xFF77674F,false);
        int columns=5, rows=(residents.size()+4)/5, cellW=(width-36)/columns, cellH=(height-60)/rows;
        for (int i=0;i<residents.size();i++) {
            int x=18+i%columns*cellW, y=48+i/columns*cellH;
            g.fillGradient(x+3,y+3,x+cellW-5,y+cellH-5,0xFFD0DEC7,0xFFE9DFC5);
            var v=residents.get(i); var renderer=(ResidentRenderer)minecraft.getEntityRenderDispatcher().getRenderer(v);
            var state=renderer.createRenderState(v,1);
            state.shadowPieces.clear(); state.nameTag=null; state.outlineColor=0;
            state.bodyRot=145; state.yRot=10; state.xRot=0; state.onGround=true;
            state.ageInTicks=30; state.walkAnimationPos=0; state.walkAnimationSpeed=0;
            for (int age=0;age<300;age++) if (ResidentMotion.blink(age,state.motionSeed)==0) { state.ageInTicks=age;break; }
            state.attention=1; state.eyeLookX=0; state.eyeLookY=0; state.scale=1;
            int size=Math.min((int)((cellH-60)*.43F),(int)(cellW*1.25F));
            g.entity(state,size,new Vector3f(0,state.boundingBoxHeight/2,0),
                new Quaternionf().rotateZ((float)Math.PI),new Quaternionf(),x+6,y+8,x+cellW-8,y+cellH-47);
            g.centeredText(font,state.outfit.profession().name().replace('_',' '),x+cellW/2,y+cellH-36,0xFF4E382B);
            String palette=state.outfit.palette().name();
            g.centeredText(font,palette,x+cellW/2,y+cellH-23,0xFF77674F);
        }
    }
}
