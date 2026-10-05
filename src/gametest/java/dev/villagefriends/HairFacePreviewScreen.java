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

/** Native close-up review: the existing blink animator receives sampled times, never replaced eyelid poses. */
final class HairFacePreviewScreen extends Screen {
    private final List<Villager> residents;
    private final int frame;
    HairFacePreviewScreen(List<Villager> residents,int frame) {
        super(Component.literal("Handcrafted male hair / Living Eyes"));this.residents=List.copyOf(residents);this.frame=frame;
    }
    @Override public boolean isPauseScreen() { return false; }
    static float blinkAge(int seed,float target) {
        for (float age=0;age<400;age+=.025F) if (Math.abs(ResidentMotion.blink(age,seed)-target)<.015F) return age;
        throw new AssertionError("Blink sample unavailable");
    }
    @Override public void extractRenderState(GuiGraphicsExtractor g,int mx,int my,float delta) {
        g.fill(0,0,width,height,0xFFF1E4CB);
        g.text(font,"FIVE HANDCRAFTED MALE HEADS  /  LIVING EYES",18,14,0xFF4E382B,false);
        g.text(font,"1px brows and lashes / protected eye UVs / explicit 3D hair",18,29,0xFF77674F,false);
        int rows=frame<0?3:1,cellW=(width-36)/5,cellH=(height-60)/rows;
        for (int row=0;row<rows;row++) for (int i=0;i<residents.size();i++) {
            int x=18+i*cellW,y=48+row*cellH;
            g.fillGradient(x+3,y+3,x+cellW-5,y+cellH-5,0xFFD0DEC7,0xFFE9DFC5);
            var renderer=(ResidentRenderer)minecraft.getEntityRenderDispatcher().getRenderer(residents.get(i));
            var state=renderer.createRenderState(residents.get(i),1);
            state.shadowPieces.clear();state.nameTag=null;state.outlineColor=0;
            state.bodyRot=row==1?150:175;state.yRot=0;state.xRot=0;state.onGround=true;
            state.walkAnimationPos=0;state.walkAnimationSpeed=0;state.attention=1;state.eyeLookY=0;state.scale=1;
            float full=blinkAge(state.motionSeed,1);
            state.ageInTicks=frame<0?blinkAge(state.motionSeed,row==0?0:row==1?.5F:1):full-3+frame*.55F;
            state.eyeLookX=frame<0?(row==0?-.2F:row==1?.2F:0):(float)Math.sin(frame*.4F)*.22F;
            int size=Math.min((int)(cellW*1.38F),(int)((cellH-36)*1.72F));
            g.entity(state,size,new Vector3f(0,1.57F,0),new Quaternionf().rotateZ((float)Math.PI),new Quaternionf(),
                x+7,y+5,x+cellW-9,y+cellH-33);
            String id=state.outfit.hair().id();
            String name=MaleHairRegistry.ALL.stream().filter(e->e.id().equals(id)).findFirst().orElseThrow().name();
            g.centeredText(font,id,x+cellW/2,y+cellH-26,0xFF4E382B);
            g.centeredText(font,frame<0?List.of("Open / glance left","Half blink / glance right","Closed / sleeping pose").get(row):name,
                x+cellW/2,y+cellH-14,0xFF77674F);
        }
    }
}
