package dev.villagefriends;

import dev.villagefriends.outfit.*;
import java.awt.image.BufferedImage;
import java.util.*;
import javax.imageio.ImageIO;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class WardrobeTest {
    private static BufferedImage texture(Garment garment) throws Exception {
        try (var input = WardrobeTest.class.getResourceAsStream("/assets/villagefriends/wardrobe/" + garment.texture())) {
            assertNotNull(input, garment.texture());
            return ImageIO.read(input);
        }
    }

    @Test void tenHairstylesTenTopsTenBottomsAndTenOutfits() {
        assertEquals(10, Wardrobe.HAIR.size()); assertEquals(10, Wardrobe.TOPS.size()); assertEquals(10, Wardrobe.BOTTOMS.size());
        assertEquals(10, Wardrobe.OUTFITS.size()); assertEquals(10, MasterPalettes.ALL.size()); assertEquals(10, Wardrobe.HAIR_COLORS.size());
        assertEquals(30, Wardrobe.ALL.stream().map(Garment::id).distinct().count());
        assertEquals(10, Wardrobe.OUTFITS.stream().map(t -> t.top()).distinct().count(), "each outfit has its own top");
        assertEquals(10, Wardrobe.OUTFITS.stream().map(t -> t.bottom()).distinct().count(), "each outfit has its own bottom");
        assertThrows(UnsupportedOperationException.class, () -> Wardrobe.HAIR.clear());
        assertThrows(IllegalArgumentException.class, () -> Wardrobe.get("missing"));
    }

    @Test void everyTextureIsKeyColorPixelArtOfTheDeclaredSize() throws Exception {
        for (var garment : Wardrobe.ALL) {
            var image = texture(garment);
            assertEquals(64, image.getWidth(), garment.id()); assertEquals(64 + garment.extrasHeight(), image.getHeight(), garment.id());
            int painted = 0;
            for (int y = 0; y < image.getHeight(); y++) for (int x = 0; x < 64; x++) {
                int code = Wardrobe.code(image.getRGB(x, y));
                if (code == Wardrobe.TRANSPARENT) continue;
                painted++;
                boolean hairKey = !Wardrobe.shadow(code) && code / Wardrobe.SHADES == Wardrobe.HAIR_ROLE;
                if (garment.kind() != Garment.Kind.HAIR) assertFalse(hairKey, "garments never use natural hair keys: " + garment.id());
            }
            assertTrue(painted > 150, garment.id());
            for (var piece : garment.pieces()) for (int y = piece.v(); y < piece.v() + piece.netHeight(); y++)
                for (int x = piece.u(); x < piece.u() + piece.netWidth(); x++) {
                    boolean net = y - piece.v() >= piece.depth()
                        || (x - piece.u() >= piece.depth() && x - piece.u() < piece.depth() + 2 * piece.width());
                    if (net) assertNotEquals(Wardrobe.TRANSPARENT, Wardrobe.code(image.getRGB(x, 64 + y)), garment.id() + ":" + piece.id());
                }
        }
        assertThrows(IllegalArgumentException.class, () -> Wardrobe.code(0xFF123456));
    }

    @Test void hairNeverPaintsTheLivingEyesRowOrHangsOverTheEyes() throws Exception {
        for (var hair : Wardrobe.HAIR) {
            var image = texture(hair);
            for (int x = 8; x < 16; x++) assertEquals(Wardrobe.TRANSPARENT, Wardrobe.code(image.getRGB(x, 12)), hair.id());
            assertEquals(Wardrobe.TRANSPARENT, Wardrobe.code(image.getRGB(11, 14)), hair.id());
            for (int y = 11; y < 16; y++) for (int x = 41; x <= 46; x++)
                assertEquals(Wardrobe.TRANSPARENT, Wardrobe.code(image.getRGB(x, y)), "hat layer over the eyes: " + hair.id());
            assertTrue(hair.pieces().size() >= 5, "volumetric hair: " + hair.id());
            for (var piece : hair.pieces()) assertEquals(BodyPart.HEAD, piece.bone());
        }
    }

    @Test void topsAndBottomsMixFreelyExceptArmorAndHose() {
        for (var top : Wardrobe.TOPS) {
            int partners = Wardrobe.bottomsFor(top).size();
            assertTrue(partners >= (top.tags().contains("armor") ? 4 : 7), top.id() + " pairs with " + partners);
        }
        int pairs = 0;
        for (var top : Wardrobe.TOPS) for (var bottom : Wardrobe.BOTTOMS) if (Wardrobe.compatible(top, bottom)) pairs++;
        assertTrue(pairs >= 75, "most tops and bottoms combine: " + pairs);
        var brigandine = Wardrobe.get("t01_squires_brigandine"); var hose = Wardrobe.get("b09_minstrel_hose");
        var greaves = Wardrobe.get("b01_plated_greaves"); var waistcoat = Wardrobe.get("t05_merchants_waistcoat");
        assertFalse(Wardrobe.compatible(brigandine, hose), "armor needs sturdy legwear");
        assertFalse(Wardrobe.compatible(waistcoat, greaves), "plate legs need a martial top");
        assertFalse(Wardrobe.compatible(hose, brigandine), "kinds are not interchangeable");
        for (var template : Wardrobe.OUTFITS) assertTrue(Wardrobe.compatible(template.top(), template.bottom()), template.id());
    }

    @Test void everyResolvedTexelComesFromTheOnePaletteOrTheHairRamp() throws Exception {
        for (var palette : MasterPalettes.ALL) {
            var allowed = new HashSet<Integer>();
            for (var ramp : palette.ramps()) for (int rgb : ramp) allowed.add(rgb);
            for (var hairColor : Wardrobe.HAIR_COLORS) {
                var hairRamp = new HashSet<Integer>(); for (int rgb : hairColor.ramp()) hairRamp.add(rgb);
                for (var garment : Wardrobe.ALL) {
                    var image = texture(garment);
                    for (int y = 0; y < image.getHeight(); y++) for (int x = 0; x < 64; x++) {
                        int code = Wardrobe.code(image.getRGB(x, y));
                        if (code == Wardrobe.TRANSPARENT || Wardrobe.shadow(code)) continue;
                        int role = code / Wardrobe.SHADES, shade = code % Wardrobe.SHADES;
                        int rgb = role == Wardrobe.HAIR_ROLE ? hairColor.shade(shade) : palette.rgb(role, shade);
                        assertTrue(role == Wardrobe.HAIR_ROLE ? hairRamp.contains(rgb) : allowed.contains(rgb));
                    }
                }
            }
        }
    }

    @Test void paletteRampsRunDarkToLight() {
        for (var palette : MasterPalettes.ALL) for (var ramp : palette.ramps()) for (int i = 1; i < 5; i++)
            assertTrue(luma(ramp[i]) >= luma(ramp[i - 1]) - 1, palette.name());
        for (var color : Wardrobe.HAIR_COLORS) for (int i = 1; i < 5; i++) assertTrue(luma(color.shade(i)) > luma(color.shade(i - 1)), color.name());
    }
    private static float luma(int rgb) { return .299F * (rgb >>> 16 & 255) + .587F * (rgb >>> 8 & 255) + .114F * (rgb & 255); }

    @Test void professionsPickTheirTemplateAndHairNeverChangesWithTheJob() {
        var seenTops = new HashSet<Garment>(); var seenBottoms = new HashSet<Garment>(); var seenHair = new HashSet<Garment>();
        int mixed = 0;
        for (long seed = 0; seed < 600; seed++) {
            var base = OutfitFactory.assembleOutfit(Gender.MALE, Profession.NONE, PaletteID.FOREST_AND_HEARTH, seed);
            assertSame(base.top(), OutfitFactory.assembleOutfit(Gender.MALE, Profession.NONE, PaletteID.FOREST_AND_HEARTH, seed).top());
            for (var job : Profession.values()) {
                var outfit = OutfitFactory.assembleOutfit(Gender.MALE, job, PaletteID.FOREST_AND_HEARTH, seed);
                assertSame(base.hair(), outfit.hair()); assertSame(base.hairColor(), outfit.hairColor());
                assertTrue(Wardrobe.templates(job).contains(outfit.template()));
                assertSame(outfit.template().top(), outfit.top());
                assertTrue(Wardrobe.compatible(outfit.top(), outfit.bottom()));
                if (outfit.bottom() != outfit.template().bottom()) mixed++;
                seenTops.add(outfit.top()); seenBottoms.add(outfit.bottom()); seenHair.add(outfit.hair());
            }
        }
        assertEquals(10, seenTops.size()); assertEquals(10, seenBottoms.size()); assertEquals(10, seenHair.size());
        assertTrue(mixed > 1000, "bottoms are sometimes swapped for compatible ones");
        assertEquals("knight_errant", Wardrobe.templates(Profession.KNIGHT).getFirst().id());
        assertEquals("arcanist", Wardrobe.templates(Profession.MAGE).getFirst().id());
        assertSame(Wardrobe.templates(Profession.NONE), Wardrobe.templates(Profession.fromId("othermod:juggler")));
    }

    @Test void outfitsOwnOnePaletteAndRecolorKeepsTheirPieces() {
        var outfit = OutfitFactory.assembleOutfit(Gender.MALE, Profession.MERCHANT, PaletteID.ROYAL_VELVET, 81);
        var changed = outfit.recolor(PaletteID.DESERT_SUN);
        assertSame(outfit.top(), changed.top()); assertSame(outfit.bottom(), changed.bottom()); assertSame(outfit.hair(), changed.hair());
        assertSame(MasterPalettes.get(PaletteID.DESERT_SUN), changed.palette());
        assertNotEquals(outfit.key(), changed.key());
        var tucked = new Outfit(Gender.MALE, Profession.FARMER, outfit.palette(), outfit.hair(), outfit.hairColor(),
            Wardrobe.get("t04_farmhand_flannel"), Wardrobe.get("b04_patched_workpants"), Wardrobe.template("farmhand"));
        assertEquals(List.of(tucked.top(), tucked.bottom(), tucked.hair()), tucked.layers(), "a tucked shirt sits under the waistband");
        var coat = OutfitFactory.assembleOutfit(Gender.MALE, Profession.MAGE, PaletteID.SCHOLARLY_PLUM, 3);
        assertEquals(List.of(coat.bottom(), coat.top(), coat.hair()), coat.layers());
        var belt = coat.bottom().pieces().stream().filter(p -> p.id().startsWith("waist")).findFirst();
        belt.ifPresent(p -> assertFalse(coat.shows(coat.bottom(), p), "a sashed coat hides the bottom's belt"));
        assertThrows(IllegalArgumentException.class, () -> new Outfit(Gender.MALE, Profession.NONE, outfit.palette(), outfit.hair(),
            outfit.hairColor(), Wardrobe.get("t01_squires_brigandine"), Wardrobe.get("b09_minstrel_hose"), Wardrobe.OUTFITS.getFirst()));
    }
}
