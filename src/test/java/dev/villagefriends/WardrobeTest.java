package dev.villagefriends;

import dev.villagefriends.outfit.*;
import java.awt.image.BufferedImage;
import java.util.*;
import javax.imageio.ImageIO;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class WardrobeTest {
    private static final List<Gender> SETS = List.of(Gender.MALE, Gender.FEMALE);
    private static final Map<String, BufferedImage> TEXTURES = new HashMap<>();

    private static BufferedImage texture(Garment garment) throws Exception {
        var cached = TEXTURES.get(garment.id());
        if (cached != null) return cached;
        try (var input = WardrobeTest.class.getResourceAsStream("/assets/villagefriends/wardrobe/" + garment.texture())) {
            assertNotNull(input, garment.texture());
            var image = ImageIO.read(input);
            TEXTURES.put(garment.id(), image);
            return image;
        }
    }
    private static long count(List<Garment> garments, Garment.Fit fit) { return garments.stream().filter(g -> g.fit() == fit).count(); }

    @Test void menAndWomenEachHaveTheirOwnWardrobe() {
        assertEquals(80, count(Wardrobe.HAIR, Garment.Fit.MALE)); assertEquals(50, count(Wardrobe.HAIR, Garment.Fit.FEMALE));
        assertEquals(120, count(Wardrobe.TOPS, Garment.Fit.MALE)); assertEquals(60, count(Wardrobe.TOPS, Garment.Fit.FEMALE));
        assertEquals(120, count(Wardrobe.BOTTOMS, Garment.Fit.MALE)); assertEquals(60, count(Wardrobe.BOTTOMS, Garment.Fit.FEMALE));
        assertEquals(10, MasterPalettes.ALL.size()); assertEquals(10, Wardrobe.HAIR_COLORS.size());
        assertEquals(Wardrobe.ALL.size(), Wardrobe.ALL.stream().map(Garment::id).distinct().count());
        assertEquals(Wardrobe.OUTFITS.size(), Wardrobe.OUTFITS.stream().map(Wardrobe.OutfitTemplate::id).distinct().count());
        for (var gender : SETS) {
            var hair = Wardrobe.hair(gender); var tops = Wardrobe.tops(gender); var bottoms = Wardrobe.bottoms(gender);
            assertTrue(hair.stream().allMatch(g -> g.fits(gender)) && tops.stream().allMatch(g -> g.fits(gender))
                && bottoms.stream().allMatch(g -> g.fits(gender)), gender + " set holds only its own pieces");
        }
        assertEquals(Wardrobe.HAIR, Wardrobe.hair(Gender.NON_BINARY), "non-binary residents wear every hairstyle");
        assertEquals(Wardrobe.TOPS, Wardrobe.tops(Gender.NON_BINARY));
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

    @Test void topsAndBottomsMixFreelyWithinASetExceptArmorHoseAndLockedSets() {
        for (var gender : SETS) {
            int free = 0, pairs = 0, locked = 0;
            for (var top : Wardrobe.tops(gender)) {
                var partners = Wardrobe.bottomsFor(top, gender);
                if (top.locked()) {
                    locked++;
                    assertEquals(List.of(Wardrobe.get(top.lockedTo())), partners, "a locked set only pairs with its partner: " + top.id());
                    continue;
                }
                assertTrue(partners.size() >= (top.tags().contains("armor") ? 4 : 7), top.id() + " pairs with " + partners.size());
                assertTrue(partners.stream().noneMatch(Garment::locked), "free tops never take a locked bottom: " + top.id());
                for (var bottom : Wardrobe.bottoms(gender)) if (!bottom.locked()) { free++; if (Wardrobe.compatible(top, bottom)) pairs++; }
            }
            assertTrue(pairs >= free * 3 / 4, gender + ": most free tops and bottoms combine (" + pairs + " of " + free + ")");
            assertTrue(locked > 0 && locked * 4 < Wardrobe.tops(gender).size(), gender + ": a few locked sets, most pieces free (" + locked + ")");
        }
        var brigandine = Wardrobe.get("t01_squires_brigandine"); var hose = Wardrobe.get("b09_minstrel_hose");
        var greaves = Wardrobe.get("b01_plated_greaves"); var waistcoat = Wardrobe.get("t05_merchants_waistcoat");
        assertFalse(Wardrobe.compatible(brigandine, hose), "armor needs sturdy legwear");
        assertFalse(Wardrobe.compatible(waistcoat, greaves), "plate legs need a martial top");
        assertFalse(Wardrobe.compatible(hose, brigandine), "kinds are not interchangeable");
        for (var garment : Wardrobe.ALL) if (garment.locked()) {
            var partner = Wardrobe.get(garment.lockedTo());
            assertEquals(garment.id(), partner.lockedTo(), "locked sets name each other");
            assertEquals(garment.fit(), partner.fit(), "locked sets share a gender");
        }
        for (var template : Wardrobe.OUTFITS) {
            assertTrue(Wardrobe.compatible(template.top(), template.bottom()), template.id());
            assertTrue(template.fits(Gender.MALE) || template.fits(Gender.FEMALE), template.id());
        }
    }

    @Test void everyResolvedTexelComesFromTheOnePaletteOrTheHairRamp() throws Exception {
        // Collect the key codes each garment uses once, then resolve them through every palette and hair color.
        var used = new TreeSet<Integer>();
        for (var garment : Wardrobe.ALL) {
            var image = texture(garment);
            for (int y = 0; y < image.getHeight(); y++) for (int x = 0; x < 64; x++) {
                int code = Wardrobe.code(image.getRGB(x, y));
                if (code != Wardrobe.TRANSPARENT && !Wardrobe.shadow(code)) used.add(code);
            }
        }
        for (var palette : MasterPalettes.ALL) {
            var allowed = new HashSet<Integer>();
            for (var ramp : palette.ramps()) for (int rgb : ramp) allowed.add(rgb);
            for (var hairColor : Wardrobe.HAIR_COLORS) {
                var hairRamp = new HashSet<Integer>(); for (int rgb : hairColor.ramp()) hairRamp.add(rgb);
                for (int code : used) {
                    int role = code / Wardrobe.SHADES, shade = code % Wardrobe.SHADES;
                    int rgb = role == Wardrobe.HAIR_ROLE ? hairColor.shade(shade) : palette.rgb(role, shade);
                    assertTrue(role == Wardrobe.HAIR_ROLE ? hairRamp.contains(rgb) : allowed.contains(rgb));
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

    @Test void everyProfessionDressesBothSetsAndEveryTopIsWorn() {
        for (var gender : SETS) {
            var worn = new HashSet<Garment>();
            for (var job : Profession.values()) {
                var templates = Wardrobe.templates(job, gender);
                assertFalse(templates.isEmpty(), gender + " " + job);
                for (var template : templates) { assertTrue(template.fits(gender), template.id()); worn.add(template.top()); }
            }
            assertEquals(new HashSet<>(Wardrobe.tops(gender)), worn, gender + ": every top is some profession's outfit");
        }
        assertEquals(Wardrobe.templates(Profession.KNIGHT), Wardrobe.templates(Profession.KNIGHT, Gender.NON_BINARY));
        assertEquals("knight_errant", Wardrobe.templates(Profession.KNIGHT, Gender.MALE).getFirst().id());
        assertEquals("arcanist", Wardrobe.templates(Profession.MAGE, Gender.MALE).getFirst().id());
        assertSame(Wardrobe.templates(Profession.NONE, Gender.FEMALE), Wardrobe.templates(Profession.fromId("othermod:juggler"), Gender.FEMALE));
    }

    @Test void residentsDressFromTheirOwnSetAndHairNeverChangesWithTheJob() {
        for (var gender : SETS) {
            var seenTops = new HashSet<Garment>(); var seenBottoms = new HashSet<Garment>(); var seenHair = new HashSet<Garment>();
            int mixed = 0, outfits = 0;
            for (long seed = 0; seed < 3000; seed++) {
                var base = OutfitFactory.assembleOutfit(gender, Profession.NONE, PaletteID.FOREST_AND_HEARTH, seed);
                seenHair.add(base.hair());
                if (seed >= 1000) continue;
                for (var job : Profession.values()) {
                    var outfit = OutfitFactory.assembleOutfit(gender, job, PaletteID.FOREST_AND_HEARTH, seed);
                    outfits++;
                    assertSame(base.hair(), outfit.hair()); assertSame(base.hairColor(), outfit.hairColor());
                    assertTrue(Wardrobe.templates(job, gender).contains(outfit.template()));
                    assertSame(outfit.template().top(), outfit.top());
                    for (var garment : outfit.garments()) assertTrue(garment.fits(gender), gender + " wears " + garment.id());
                    assertTrue(Wardrobe.compatible(outfit.top(), outfit.bottom()));
                    if (outfit.top().locked()) assertSame(outfit.template().bottom(), outfit.bottom(), "locked sets are worn whole");
                    if (outfit.bottom() != outfit.template().bottom()) mixed++;
                    seenTops.add(outfit.top()); seenBottoms.add(outfit.bottom());
                }
            }
            assertEquals(Wardrobe.hair(gender).size(), seenHair.size(), gender + ": every hairstyle is worn");
            assertEquals(Wardrobe.tops(gender).size(), seenTops.size(), gender + ": every top is worn");
            assertTrue(seenBottoms.size() > Wardrobe.bottoms(gender).size() * 9 / 10, gender + ": bottoms " + seenBottoms.size());
            assertTrue(mixed > outfits / 4, gender + ": bottoms are often swapped for compatible ones (" + mixed + ")");
        }
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
        var coat = new Outfit(Gender.MALE, Profession.MAGE, MasterPalettes.get(PaletteID.SCHOLARLY_PLUM), outfit.hair(), outfit.hairColor(),
            Wardrobe.get("t03_arcanist_longcoat"), Wardrobe.get("b03_scholars_slacks"), Wardrobe.template("arcanist"));
        assertEquals(List.of(coat.bottom(), coat.top(), coat.hair()), coat.layers());
        var belt = coat.bottom().pieces().stream().filter(p -> p.id().startsWith("waist")).findFirst();
        belt.ifPresent(p -> assertFalse(coat.shows(coat.bottom(), p), "a sashed coat hides the bottom's belt"));
        assertThrows(IllegalArgumentException.class, () -> new Outfit(Gender.MALE, Profession.NONE, outfit.palette(), outfit.hair(),
            outfit.hairColor(), Wardrobe.get("t01_squires_brigandine"), Wardrobe.get("b09_minstrel_hose"), Wardrobe.OUTFITS.getFirst()));
        var set = Wardrobe.TOPS.stream().filter(Garment::locked).findFirst().orElseThrow();
        var stranger = Wardrobe.bottoms(Gender.NON_BINARY).stream().filter(b -> !b.id().equals(set.lockedTo())).findFirst().orElseThrow();
        assertThrows(IllegalArgumentException.class, () -> new Outfit(Gender.FEMALE, Profession.NONE, outfit.palette(), outfit.hair(),
            outfit.hairColor(), set, stranger, Wardrobe.OUTFITS.getFirst()), "a locked top never mixes");
    }
}
