package dev.villagefriends;

import dev.villagefriends.outfit.*;
import java.util.*;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class SurfaceTextureTest {
    @Test void allMaterialsProduceRepeatableHueLockedNoiseWithinFivePercent() {
        int base=0xFF647593;
        for (var material:SurfaceTexture.Material.values()) {
            var colors=new HashSet<Integer>();
            for (int y=0;y<16;y++) for (int x=0;x<16;x++) {
                int pixel=SurfaceTexture.pixel(base,material,x,y,231,0,SurfaceTexture.Face.FRONT);
                assertEquals(pixel,SurfaceTexture.pixel(base,material,x,y,231,0,SurfaceTexture.Face.FRONT));
                colors.add(pixel); assertEquals(255,pixel>>>24);
                assertTrue(Math.abs(value(pixel)/value(base)-1)<=.05+1/147F);
                assertTrue(Math.abs(saturation(pixel)/saturation(base)-1)<.075);
                assertTrue(Math.abs(hue(pixel)-hue(base))<.025);
            }
            assertTrue(colors.size()>12,material.name());
        }
    }
    @Test void protrudingOverlapsDarkenNearbyPixelsByFifteenToTwentyPercent() {
        var shirt=new VoxelBox("shirt",BodyPart.TORSO,0,-4,0,-2,8,12,4,0);
        var belt=new VoxelBox("belt",BodyPart.TORSO,1,-4,5,-2.35F,8,.5F,.2F,0);
        float shadow=SurfaceTexture.occlusion(shirt,SurfaceTexture.Face.FRONT,.5F,.5F,List.of(shirt,belt));
        assertTrue(shadow>=.15F && shadow<=.2F);
        assertEquals(0,SurfaceTexture.occlusion(shirt,SurfaceTexture.Face.FRONT,.5F,.85F,List.of(shirt,belt)));
        int normal=SurfaceTexture.pixel(0xFF889988,SurfaceTexture.Material.WOVEN,3,6,1,0,SurfaceTexture.Face.FRONT);
        int shaded=SurfaceTexture.pixel(0xFF889988,SurfaceTexture.Material.WOVEN,3,6,1,shadow,SurfaceTexture.Face.FRONT);
        assertEquals(1-shadow,value(shaded)/value(normal),.01);
        var leg=new VoxelBox("leg",BodyPart.LEFT_LEG,0,-2,0,-2,4,12,4,0);
        var waist=new VoxelBox("waist",BodyPart.TORSO,1,-4,11.1F,-2.35F,8,.5F,.2F,0);
        assertTrue(SurfaceTexture.occlusion(leg,SurfaceTexture.Face.FRONT,.5F,.04F,List.of(leg,waist))>=.15F);
        var trouser=new VoxelBox("left_trouser",BodyPart.LEFT_LEG,0,-2,0,-2,4,12,4,0);
        assertEquals(.17F,SurfaceTexture.occlusion(trouser,SurfaceTexture.Face.FRONT,.1F,.5F,List.of(trouser)),.001F);
    }
    @Test void allMaleTrimIsConnectedStructuralTrimAndThereIsOnlyOneBuckle() {
        for (var top:MaleTopRegistry.ALL) for (var layer:top.model().layers()) for (var voxel:layer.voxels()) {
            String id=voxel.geometry().id();
            assertFalse(id.contains("belt") || id.contains("patch") || id.contains("knee") || id.contains("shin"));
            if (voxel.mask().weights()[0]==0x0000FF00) assertTrue(id.contains("cuff") || id.contains("collar") || id.contains("lapel") || id.contains("hem"));
        }
        for (var bottom:MaleBottomRegistry.ALL) {
            var boxes=bottom.model().layers().stream().flatMap(l->l.voxels().stream()).toList();
            assertEquals(1,boxes.stream().filter(v->v.geometry().id().equals("belt_buckle")).count());
            for (var v:boxes) {
                assertFalse(v.geometry().id().contains("knee") || v.geometry().id().contains("patch") || v.geometry().id().contains("shin"));
                if (v.mask().weights()[0]==0x0000FF00) assertTrue(v.geometry().id().startsWith("waist_belt_"));
            }
        }
    }
    @Test void steppedHairOverhangsTheForeheadAndBakesAShadow() {
        var face=new VoxelBox("face",BodyPart.HEAD,0,-4,-8,-4,8,8,8,0);
        for (var hair:MaleHairRegistry.ALL) {
            assertTrue(hair.model().voxels().stream().anyMatch(v->v.z()<=-5));
            assertTrue(hair.model().voxels().stream().anyMatch(v->v.x()<=-5 || v.x()+v.width()>=5));
            assertTrue(hair.model().voxels().stream().filter(v->v.id().startsWith("crown_")).count()>4);
            boolean shadow=false;
            for (int y=0;y<4;y++) for (int x=0;x<8;x++) shadow|=SurfaceTexture.occlusion(face,SurfaceTexture.Face.FRONT,
                (x+.5F)/8,(y+.5F)/8,hair.model().voxels())>=.15F;
            assertTrue(shadow,hair.id());
        }
    }
    private static float value(int rgb) { return Math.max((rgb>>>16)&255,Math.max((rgb>>>8)&255,rgb&255)); }
    private static float saturation(int rgb) { float max=value(rgb),min=Math.min((rgb>>>16)&255,Math.min((rgb>>>8)&255,rgb&255));return (max-min)/max; }
    private static float hue(int rgb) {
        float r=(rgb>>>16)&255,g=(rgb>>>8)&255,b=rgb&255,max=value(rgb),min=Math.min(r,Math.min(g,b)),delta=max-min;
        float h=max==r?(g-b)/delta:max==g?2+(b-r)/delta:4+(r-g)/delta;
        return (h+6)%6/6;
    }
}
