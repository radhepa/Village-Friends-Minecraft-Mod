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
            assertTrue(hair.pieces().stream().anyMatch(p -> { float[] b = bounds(p);
                return b[1] < -8.6F || b[0] < -4.6F || b[3] > 4.6F || b[5] > 4.6F || b[4] > .6F; }), hair.id() + " has volume past the hat layer");
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
        assertFalse(FaceDetails.protectedUv(11, 14));
        assertFalse(FaceDetails.protectedUv(12, 11));
        var swatches = List.of(FaceDetails.BROW_U, FaceDetails.LASH_U, FaceDetails.SHADOW_U, FaceDetails.TINT_U,
            FaceDetails.PUPIL_U, FaceDetails.LIP_U, FaceDetails.ROSE_LIP_U, FaceDetails.BLUSH_U);
        assertEquals(swatches.size(), new HashSet<>(swatches).size());
        // Row 0 of the hair slot's columns, above the hair piece block that starts at y 8.
        for (int u : swatches) assertTrue(u >= 64 && u < 128 && FaceDetails.V < 8);
    }

    @Test void residentsSplitBetweenStarlitAndSoftGlintEyesForLife() {
        int starlit = 0, feminine = 0;
        for (int seed = 0; seed < 20000; seed++) {
            var style = FaceDetails.eyeStyle(seed * 7919);
            assertEquals(style, FaceDetails.eyeStyle(seed * 7919));
            if (style == FaceDetails.EyeStyle.STARLIT) starlit++;
            assertTrue(FaceDetails.feminine(Gender.FEMALE, seed));
            assertFalse(FaceDetails.feminine(Gender.MALE, seed));
            if (FaceDetails.feminine(Gender.NON_BINARY, seed * 7919)) feminine++;
        }
        assertTrue(starlit > 9000 && starlit < 11000, "both eye styles are common: " + starlit);
        assertTrue(feminine > 9000 && feminine < 11000, "non-binary faces mix both: " + feminine);
    }

    @Test void lashesSweepDownToCloseTheEyeAndBrowsKeepAGap() {
        for (var style : FaceDetails.EyeStyle.values()) {
            float top = FaceDetails.eyeTop(style), previous = Float.NEGATIVE_INFINITY;
            assertEquals(top, FaceDetails.lashBottom(style, 0), .0001, "an open eye sits under its lash");
            assertEquals(FaceDetails.EYE_BOTTOM, FaceDetails.lashBottom(style, 1), .0001, "a closed lash reaches the eye's bottom");
            for (float blink = 0; blink <= 1.0001F; blink += .05F) {
                float bottom = FaceDetails.lashBottom(style, blink), lashTop = bottom - FaceDetails.lashHeight(blink);
                assertTrue(bottom >= previous && bottom <= FaceDetails.EYE_BOTTOM + .0001F);
                assertTrue(lashTop >= top - 1.0001F, "lash stays below its resting line");
                previous = bottom;
            }
            float wingBottom = FaceDetails.wingTop(style, 1) + FaceDetails.wingHeight(1);
            assertTrue(wingBottom > FaceDetails.lashBottom(style, 1) - FaceDetails.lashHeight(1), "the wing joins the closed lash");
            assertTrue(FaceDetails.browTop(style) + .55F < top - 1.4F, "brows clear the lashes");
        }
        assertEquals(-4, FaceDetails.eyeTop(FaceDetails.EyeStyle.STARLIT), .0001);
        assertEquals(-3, FaceDetails.eyeTop(FaceDetails.EyeStyle.SOFT_GLINT), .0001);
    }

    @Test void eyeAndMouthColorsComeFromTheResidentsOwnFace() {
        int iris = 0xFF557653, white = 0xFFEDE0CD;
        for (int skin : List.of(0xFFE9C8AF, 0xFFC38B64, 0xFF643F33)) {
            assertTrue(red(FaceDetails.blush(skin)) - green(FaceDetails.blush(skin)) > red(skin) - green(skin), "blush is rosier");
            assertTrue(red(FaceDetails.roseLip(skin)) - green(FaceDetails.roseLip(skin)) > red(FaceDetails.lip(skin)) - green(FaceDetails.lip(skin)), "rose lips are pinker");
            assertTrue(green(FaceDetails.lip(skin)) < green(skin), "lips are darker than skin");
        }
        for (int shift : new int[]{16, 8, 0}) {
            assertTrue(((FaceDetails.tint(iris, white) >>> shift) & 255) > ((iris >>> shift) & 255), "tinted white is lighter than the iris");
            assertEquals(Math.round(((iris >>> shift) & 255) * .5F), (FaceDetails.pupil(iris) >>> shift) & 255);
        }
    }

    private static int red(int argb) { return (argb >>> 16) & 255; }
    private static int green(int argb) { return (argb >>> 8) & 255; }
}
