package dev.villagefriends;

import dev.villagefriends.outfit.*;
import java.util.*;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class OutfitEngineTest {
    @Test void everyInputAssemblesACompatibleOutfitWithOnePalette() {
        for (var gender : Gender.values()) for (var job : Profession.values()) for (var palette : PaletteID.values()) {
            var outfit = OutfitFactory.assembleOutfit(gender, job, palette, 42817);
            assertSame(MasterPalettes.get(palette), outfit.palette());
            assertTrue(Wardrobe.compatible(outfit.top(), outfit.bottom()));
            assertEquals(Garment.Kind.HAIR, outfit.hair().kind());
        }
        assertEquals(10, MasterPalettes.ALL.size());
        for (var palette : MasterPalettes.ALL) assertEquals(7, palette.ramps().length);
    }

    @Test void paletteRampsAreImmutableCopies() {
        var palette = MasterPalettes.ALL.getFirst();
        palette.ramps()[0][2] = 0;
        assertNotEquals(0, palette.rgb(ColorPalette.PRIMARY, 2));
        assertThrows(IllegalArgumentException.class, () -> new ColorPalette(PaletteID.ASH_AND_TEAL, "bad", new int[6][5]));
        assertThrows(IllegalArgumentException.class, () -> new HairColor("BAD", "bad", new int[]{1, 2, 3}));
        assertThrows(IllegalArgumentException.class, () -> new Piece("flat", BodyPart.HEAD, Piece.Vec3.ZERO, Piece.Vec3.ZERO,
            Piece.Vec3.ZERO, 4, 4, 0, 0, 0, 0, Piece.Motion.NONE, Piece.Vec3.ONE));
    }

    @Test void seedsRepeatAndJobChangesKeepHairAndPalette() {
        var seen = new HashSet<String>();
        for (int seed = 0; seed < 200; seed++) {
            var a = OutfitFactory.assembleOutfit(Gender.FEMALE, Profession.MERCHANT, PaletteID.SAGE_AND_TERRACOTTA, seed);
            var b = OutfitFactory.assembleOutfit(Gender.FEMALE, Profession.MERCHANT, PaletteID.SAGE_AND_TERRACOTTA, seed);
            assertEquals(a.key(), b.key());
            seen.add(a.key());
            for (var job : Profession.values()) {
                var changed = OutfitFactory.assembleOutfit(Gender.FEMALE, job, a.palette().id(), seed);
                assertSame(a.hair(), changed.hair()); assertSame(a.hairColor(), changed.hairColor());
            }
        }
        assertTrue(seen.size() > 100);
        assertThrows(NullPointerException.class, () -> OutfitFactory.assembleOutfit(null, Profession.NONE, PaletteID.DESERT_SUN));
    }

    @Test void newRecipesRoundTripAndNamesRetainComplexionEligibility() {
        UUID id = UUID.fromString("812ea1a6-1916-4920-8342-2e766d4722d3");
        var look = ResidentLook.generate(id);
        assertEquals(look, ResidentLook.parse(look.recipe())); assertEquals(look, ResidentLook.generate(id));
        assertNotNull(ResidentLook.parse("outfit1:2:MALE:FOREST_AND_HEARTH:81").outfit(Profession.MERCHANT));
        assertNull(ResidentLook.parse("outfit1:99:FEMALE:DESERT_SUN:1"));
        assertNull(ResidentLook.parse("outfit1:0:invalid:DESERT_SUN:1"));
        assertNull(ResidentLook.parse("retired-recipe"));
        for (int i = 0; i < 500; i++) for (int skin = 0; skin < 2; skin++) {
            var light = new ResidentLook(skin, Gender.FEMALE, PaletteID.DESERT_SUN, i);
            assertNotEquals("indian", ResidentNames.pool(new UUID(0, i), light.recipe()).id());
        }
    }
}
