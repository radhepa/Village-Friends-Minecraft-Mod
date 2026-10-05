package dev.villagefriends;

import dev.villagefriends.outfit.*;
import java.util.*;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class HandcraftedFaceTest {
    @Test void fiveIdsMatchTheRequestedHandcraftedStyles() {
        assertEquals(List.of(MaleHairRegistry.Geometry.MESSY_PARTED,MaleHairRegistry.Geometry.SPIKY_LAYERED,
            MaleHairRegistry.Geometry.LOW_PONYTAIL,MaleHairRegistry.Geometry.SHAGGY_CROP,MaleHairRegistry.Geometry.UNDERCUT_SWEEP),
            MaleHairRegistry.ALL.stream().map(MaleHairRegistry.Entry::geometry).toList());
        for (var entry:MaleHairRegistry.ALL) {
            assertSame(entry.model(),MaleHairModels.get(entry.id()));
            assertEquals(2,entry.strandLayerDepth());
            assertThrows(UnsupportedOperationException.class,()->entry.model().voxels().clear());
        }
        assertThrows(IllegalArgumentException.class,()->MaleHairModels.get("m_hair_06"));
    }
    @Test void DrapesNeverObstructTheAnimatedEyeFramesOrEyebrows() {
        for (var hair:MaleHairRegistry.ALL) for (var v:hair.model().voxels()) {
            if (v.z()-v.inflation()>=-4.1F) continue;
            for (float eyeX:new float[]{-3,1}) {
                assertFalse(overlap(v.x()-v.inflation(),v.x()+v.width()+v.inflation(),eyeX,eyeX+2)
                    && overlap(v.y()-v.inflation(),v.y()+v.height()+v.inflation(),-4,-3),hair.id()+":"+v.id()+" blocks eyes");
                assertFalse(overlap(v.x()-v.inflation(),v.x()+v.width()+v.inflation(),eyeX,eyeX+2)
                    && overlap(v.y()-v.inflation(),v.y()+v.height()+v.inflation(),-7,-6),hair.id()+":"+v.id()+" blocks brows");
            }
        }
    }
    private static boolean overlap(float min,float max,float start,float end) { return min<end && max>start; }
    @Test void PonytailHasActualRearLengthAndSeparateCheekFramingStrands() {
        var model=MaleHairModels.get("m_hair_03");
        assertTrue(model.voxels().stream().anyMatch(v->v.id().equals("ponytail_lower") && v.z()>4 && v.y()+v.height()>3));
        assertTrue(model.voxels().stream().anyMatch(v->v.id().equals("cheek_left_front") && v.y()+v.height()<-1 && v.y()+v.height()>-2));
        assertTrue(model.voxels().stream().anyMatch(v->v.id().equals("cheek_right_front") && v.z()<-5));
    }
    @Test void BrowsUseExactlyTwentyPercentDarkerNaturalHairAndShadowsTenPercentDarkerSkin() {
        for (int color:OutfitCatalog.HAIR_COLORS) for (int shift:new int[]{16,8,0}) {
            assertEquals(Math.round(((color>>>shift)&255)*.8F),(FaceDetails.brow(color)>>>shift)&255);
            assertTrue(((FaceDetails.lash(color)>>>shift)&255)<=((FaceDetails.brow(color)>>>shift)&255));
        }
        for (int skin:List.of(0xFFD6B494,0xFFAC8061,0xFF765136)) for (int shift:new int[]{16,8,0})
            assertEquals(Math.round(((skin>>>shift)&255)*.9F),(FaceDetails.shadow(skin)>>>shift)&255);
    }
    @Test void EyeSamplingGridIsProtectedAndFaceSwatchesAreOutsideTheBodyAtlas() {
        for (int x=8;x<16;x++) assertTrue(FaceDetails.protectedUv(x,12));
        assertTrue(FaceDetails.protectedUv(11,14));
        assertFalse(FaceDetails.protectedUv(12,11));
        for (int u:List.of(FaceDetails.BROW_U,FaceDetails.LASH_U,FaceDetails.SOCKET_U,FaceDetails.CHIN_U)) assertTrue(u>=64);
        assertEquals(1,(FaceDetails.LASH_Y-.5F)-(FaceDetails.BROW_Y+.5F),.0001);
    }
}
