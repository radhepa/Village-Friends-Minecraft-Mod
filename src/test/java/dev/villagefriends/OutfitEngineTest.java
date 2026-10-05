package dev.villagefriends;

import dev.villagefriends.outfit.*;
import java.util.*;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class OutfitEngineTest {
    @Test void everyInputAssemblesCompatibleLayersWithOnePalette() {
        for (var gender : Gender.values()) for (var job : Profession.values()) for (var palette : PaletteID.values()) {
            var outfit = OutfitFactory.assembleOutfit(gender, job, palette, 42817);
            assertSame(MasterPalettes.get(palette), outfit.palette());
            assertEquals(job.preferredStyle(), outfit.top().style());
            assertTrue(outfit.bottom().compatibleStyles().contains(outfit.top().style()));
            for (var layer : outfit.layers()) {
                assertSame(outfit.palette(), layer.palette());
                for (var voxel : layer.model().voxels()) assertEquals(voxel.mask().resolve(outfit.palette())[0], layer.resolve(voxel)[0]);
            }
        }
        assertEquals(10, MasterPalettes.ALL.size());
        assertEquals(60, ColorRole.ROLE_PRIMARY.textilePercent());
        assertEquals(30, ColorRole.ROLE_SECONDARY.textilePercent());
        assertEquals(10, ColorRole.ROLE_ACCENT.textilePercent());
    }

    @Test void fourRoleChannelsResolveAndHardwareIsIndependentOfOpacity() {
        var palette = new ColorPalette(PaletteID.ASH_AND_TEAL, "test", 0xFF0000, 0x00FF00, 0x0000FF, 0x123456);
        for (var role : ColorRole.values()) assertEquals(0xFF000000 | palette.rgb(role), RoleMask.solid(role).argb(0, 0, palette));
        var hardware = new RoleMask(1, 1, new int[]{0x000000FF}, new byte[]{64}, new byte[]{0});
        assertEquals(0x40123456, hardware.argb(0, 0, palette));
        var mixed = new RoleMask(1, 1, new int[]{0x994D1900}, new byte[]{(byte)255}, new byte[]{0});
        assertEquals(0xFF994D19, mixed.argb(0, 0, palette));
        var empty = new RoleMask(1, 1, new int[]{0}, new byte[]{0}, new byte[]{0});
        assertEquals(0, empty.argb(0, 0, palette));
        assertThrows(IllegalArgumentException.class, () -> new RoleMask(1, 1, new int[]{0xFFFFFFFF}, new byte[]{-1}, new byte[]{0}));
        assertThrows(IllegalArgumentException.class, () -> new RoleMask(1, 1, new int[]{0}, new byte[]{-1}, new byte[]{0}));
        assertThrows(IndexOutOfBoundsException.class, () -> hardware.argb(1, 0, palette));
    }

    @Test void maskArraysAndModelCollectionsCannotMutateEquippedClothes() {
        int[] weights = {0xFF000000}; byte[] opacity = {-1}, shade = {0};
        var mask = new RoleMask(1, 1, weights, opacity, shade);
        weights[0] = 255; opacity[0] = 0; shade[0] = 50; mask.weights()[0] = 0;
        assertEquals(0xFF000000 | MasterPalettes.ALL.getFirst().primary(), mask.argb(0, 0, MasterPalettes.ALL.getFirst()));
        var outfit = OutfitFactory.assembleOutfit(Gender.FEMALE, Profession.MERCHANT, PaletteID.ROYAL_VELVET, 88);
        assertThrows(UnsupportedOperationException.class, () -> outfit.layers().clear());
        assertThrows(UnsupportedOperationException.class, () -> outfit.hair().voxels().clear());
        var changed = outfit.recolor(PaletteID.DESERT_SUN);
        assertSame(outfit.top(), changed.top()); assertSame(outfit.bottom(), changed.bottom()); assertSame(outfit.hair(), changed.hair());
        assertEquals(outfit.hairRgb(), changed.hairRgb());
        for (var layer : changed.layers()) assertSame(changed.palette(), layer.palette());
        for (var layer : outfit.layers()) assertSame(MasterPalettes.get(PaletteID.ROYAL_VELVET), layer.palette());
    }

    @Test void hairHasOuterLayerVolumeAndRejectsPlanes() {
        assertEquals(10, OutfitCatalog.HAIR.size());
        for (var hair : OutfitCatalog.HAIR) {
            assertTrue(hair.voxels().stream().anyMatch(v -> v.depthLayer() > 0 && v.outsideHead()));
            for (var voxel : hair.voxels()) {
                assertTrue(voxel.width() > 0 && voxel.height() > 0 && voxel.depth() > 0);
                assertEquals(BodyPart.HEAD, voxel.bone());
            }
        }
        assertThrows(IllegalArgumentException.class, () -> new VoxelBox("flat", BodyPart.HEAD, 1, 0, 0, 0, 4, 4, 0, 0));
        assertThrows(IllegalArgumentException.class, () -> new VoxelBox("bad", BodyPart.HEAD, 1, Float.NaN, 0, 0, 1, 1, 1, 0));
        var inside = new VoxelBox("inside", BodyPart.HEAD, 0, -4, -8, -4, 8, 8, 8, 0);
        assertThrows(IllegalArgumentException.class, () -> new HairModel("flat_hair", Set.of(Gender.MALE), List.of(inside), List.of()));
    }

    @Test void seedsRepeatAndJobChangesKeepHairAndPalette() {
        var seen = new HashSet<String>();
        for (int seed = 0; seed < 200; seed++) {
            var a = OutfitFactory.assembleOutfit(Gender.FEMALE, Profession.MERCHANT, PaletteID.SAGE_AND_TERRACOTTA, seed);
            var b = OutfitFactory.assembleOutfit(Gender.FEMALE, Profession.MERCHANT, PaletteID.SAGE_AND_TERRACOTTA, seed);
            assertSame(a.top(), b.top()); assertSame(a.bottom(), b.bottom()); assertSame(a.hair(), b.hair());
            assertEquals(a.hairRgb(), b.hairRgb());
            seen.add(a.top().id() + ":" + a.bottom().id() + ":" + a.hair().id() + ":" + a.hairRgb());
            for (var job : Profession.values()) {
                var changed = OutfitFactory.assembleOutfit(Gender.FEMALE, job, a.palette().id(), seed);
                assertSame(a.hair(), changed.hair()); assertEquals(a.hairRgb(), changed.hairRgb());
            }
        }
        assertTrue(seen.size() > 100);
        assertThrows(NullPointerException.class, () -> OutfitFactory.assembleOutfit(null, Profession.NONE, PaletteID.DESERT_SUN));
    }

    @Test void newRecipesRoundTripAndNamesRetainComplexionEligibility() {
        UUID id = UUID.fromString("812ea1a6-1916-4920-8342-2e766d4722d3");
        var look = ResidentLook.generate(id);
        assertEquals(look, ResidentLook.parse(look.recipe())); assertEquals(look, ResidentLook.generate(id));
        assertNull(ResidentLook.parse("outfit1:99:FEMALE:DESERT_SUN:1"));
        assertNull(ResidentLook.parse("outfit1:0:invalid:DESERT_SUN:1"));
        assertNull(ResidentLook.parse("retired-recipe"));
        for (int i = 0; i < 500; i++) for (int skin = 0; skin < 2; skin++) {
            var light = new ResidentLook(skin, Gender.FEMALE, PaletteID.DESERT_SUN, i);
            assertNotEquals("indian", ResidentNames.pool(new UUID(0, i), light.recipe()).id());
        }
    }
}
