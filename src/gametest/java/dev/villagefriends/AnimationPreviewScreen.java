package dev.villagefriends;

import dev.villagefriends.client.*;
import java.util.List;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.npc.villager.Villager;
import org.joml.Quaternionf;
import org.joml.Vector3f;

/** Test-only art review with actual Minecraft rendering at consistent animation samples. */
final class AnimationPreviewScreen extends Screen {
    private final List<Villager> residents;
    private final boolean faces;
    private final float sample;
    AnimationPreviewScreen(List<Villager> residents,boolean faces,float sample) {
        super(Component.literal("Village Friends animation review"));this.residents=residents;this.faces=faces;this.sample=sample;
    }
    @Override public boolean isPauseScreen(){return false;}
    @Override public void extractRenderState(GuiGraphicsExtractor g,int mx,int my,float delta) {
        g.fill(0,0,width,height,0xFFF1E4CB);
        g.text(font,faces?"VILLAGE FRIENDS  /  LIVING EYES":"VILLAGE FRIENDS  /  SIX INDIVIDUAL WALKS",18,14,0xFF4E382B,false);
        g.text(font,faces?"Original eye colors, quick blinks, gentle glances and children":"Soft steps, shoulder swing and restrained weight shifts",18,28,0xFF77674F,false);
        int cols=faces?4:3,cellW=(width-36)/cols,cellH=(height-55)/2;
        for(int i=0;i<residents.size();i++) {
            int x=18+i%cols*cellW,y=46+i/cols*cellH;
            g.fillGradient(x+3,y+3,x+cellW-5,y+cellH-5,0xFFD0DEC7,0xFFE9DFC5);
            var v=residents.get(i);var renderer=(ResidentRenderer)minecraft.getEntityRenderDispatcher().getRenderer(v);
            var s=renderer.createRenderState(v,1);
            s.shadowPieces.clear();s.outlineColor=0;s.nameTag=null;s.bodyRot=faces?180:155;s.yRot=faces?0:10;s.xRot=0;s.onGround=true;
            s.ageInTicks=sample;s.walkAnimationPos=sample*.46F;s.walkAnimationSpeed=faces?0:.46F;
            s.attention=1;s.eyeLookX=faces?(i%2==0?-.22F:.22F):0;s.eyeLookY=0;
            if(faces && i==2) for(float a=0;a<300;a+=.025F)if(Math.abs(ResidentMotion.blink(a,s.motionSeed)-.55F)<.025F){s.ageInTicks=a;break;}
            if(faces && i==3)for(float a=0;a<300;a+=.05F)if(ResidentMotion.blink(a,s.motionSeed)==1){s.ageInTicks=a;break;}
            s.scale=1;
            int size=faces?(int)(cellW*1.4F):(int)((cellH-30)*.48F);
            g.entity(s,size,new Vector3f(0,faces?(s.isBaby?.86F:1.56F):s.boundingBoxHeight/2,0),
                    new Quaternionf().rotateZ((float)Math.PI),new Quaternionf(),x+6,y+6,x+cellW-8,y+cellH-24);
            String label=faces?List.of("Glance left","Glance right","Mid-blink","Closed eyes","Glasses","Child","Legacy face","Beard").get(i):ResidentMotion.gait(s.motionSeed).label;
            g.centeredText(font,label,x+cellW/2,y+cellH-17,0xFF4E382B);
        }
    }
}
