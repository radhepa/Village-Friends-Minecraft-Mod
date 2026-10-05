package dev.villagefriends;

import dev.villagefriends.outfit.*;
import java.util.*;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class HandcraftedFaceTest {
    /** Bone-local AABB of a rotated piece (Minecraft ZYX rotation about the pivot). */
    private static float[] bounds(Piece p) {
        double ax = Math.toRadians(p.rotation().x()), ay = Math.toRadians(p.rotation().y()), az = Math.toRadians(p.rotation().z());
        float[] lo = {Float.MAX_VALUE, Float.MAX_VALUE, Float.MAX_VALUE}, hi = {-Float.MAX_VALUE, -Float.MAX_VALUE, -Float.MAX_VALUE};
        float g = p.inflate();
        for (float cx : new float[]{p.origin().x() - g, p.origin().x() + p.width() + g})
            for (float cy : new float[]{p.origin().y() - g, p.origin().y() + p.height() + g})
                for (float cz : new float[]{p.origin().z() - g, p.origin().z() + p.depth() + g}) {
                    double x = cx * p.scale().x(), y = cy * p.scale().y(), z = cz * p.scale().z();
                    double y1 = y * Math.cos(ax) - z * Math.sin(ax), z1 = y * Math.sin(ax) + z * Math.cos(ax);
                    double x2 = x * Math.cos(ay) + z1 * Math.sin(ay), z2 = -x * Math.sin(ay) + z1 * Math.cos(ay);
                    double x3 = x2 * Math.cos(az) - y1 * Math.sin(az), y3 = x2 * Math.sin(az) + y1 * Math.cos(az);
                    float[] v = {(float)x3 + p.pivot().x(), (float)y3 + p.pivot().y(), (float)z2 + p.pivot().z()};
                    for (int i = 0; i < 3; i++) { lo[i] = Math.min(lo[i], v[i]); hi[i] = Math.max(hi[i], v[i]); }
                }
        return new float[]{lo[0], lo[1], lo[2], hi[0], hi[1], hi[2]};
    }

    @Test void hairPiecesNeverHangOverTheAnimatedEyesNoseOrMouth() {
        for (var hair : Wardrobe.HAIR) for (var piece : hair.pieces()) {
            float[] b = bounds(piece);
            boolean inFront = b[2] < -4.1F, overFace = b[0] < 3 && b[3] > -3, belowLashes = b[4] > -5.02F && b[1] < 0;
            assertFalse(inFront && overFace && belowLashes, hair.id() + ":" + piece.id() + " covers the eyes");
        }
    }

    @Test void everyHairstyleHasVolumeBeyondTheHatLayer() {
        for (var hair : Wardrobe.HAIR) {
            assertTrue(hair.pieces().stream().anyMatch(p -> { float[] b = bounds(p); return b[1] < -8.6F; }), hair.id() + " rises past the hat layer");
        }
    }

    @Test void BrowsUseExactlyTwentyPercentDarkerNaturalHairAndShadowsTenPercentDarkerSkin() {
        for (var color : Wardrobe.HAIR_COLORS) for (int shift : new int[]{16, 8, 0}) {
            int base = color.base();
            assertEquals(Math.round(((base >>> shift) & 255) * .8F), (FaceDetails.brow(base) >>> shift) & 255);
            assertTrue(((FaceDetails.lash(base) >>> shift) & 255) <= ((FaceDetails.brow(base) >>> shift) & 255));
        }
        for (int skin : List.of(0xFFD6B494, 0xFFAC8061, 0xFF765136)) for (int shift : new int[]{16, 8, 0})
            assertEquals(Math.round(((skin >>> shift) & 255) * .9F), (FaceDetails.shadow(skin) >>> shift) & 255);
    }

    @Test void EyeSamplingGridIsProtectedAndFaceSwatchesAreOutsideTheBodyAtlas() {
        for (int x = 8; x < 16; x++) assertTrue(FaceDetails.protectedUv(x, 12));
        assertTrue(FaceDetails.protectedUv(11, 14));
        assertFalse(FaceDetails.protectedUv(12, 11));
        for (int u : List.of(FaceDetails.BROW_U, FaceDetails.LASH_U, FaceDetails.SOCKET_U, FaceDetails.CHIN_U)) assertTrue(u >= 64);
        assertEquals(1, (FaceDetails.LASH_Y - .5F) - (FaceDetails.BROW_Y + .5F), .0001);
    }
}
