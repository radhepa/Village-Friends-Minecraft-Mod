package dev.villagefriends.stable;

import static org.junit.jupiter.api.Assertions.*;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import dev.villagefriends.stable.data.StableTable;
import dev.villagefriends.stable.gear.ArcheryMath;
import dev.villagefriends.stable.gear.GearText;
import dev.villagefriends.stable.gear.LanceMath;
import dev.villagefriends.stable.gear.PackCapacity;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Map;
import java.util.Random;
import org.junit.jupiter.api.Test;

/** Pack slots, the couched lance and mounted archery (the gear package's pure logic), and the gear assets the table promises. */
class StableGearTest {
    private static final double IRON_SPEAR_MULTIPLIER = 0.95;
    private static final Map<String, String> SADDLE_LAYERS = Map.of("horse", "horse_saddle", "donkey", "donkey_saddle", "mule", "mule_saddle");

    private static StableTable.Gear gear(String id) { return StableTable.gear(id).orElseThrow(); }
    private static int columns(String animal, boolean chest, String tack) {
        return PackCapacity.columns(animal, chest, tack == null ? 0 : PackCapacity.tackColumns(gear(tack), animal));
    }

    @Test void saddlebagsGiveAHorseTwoColumnsAndNothingElseDoes() {
        assertEquals(2, columns("horse", false, "saddlebags"));
        assertEquals(6, PackCapacity.slots(columns("horse", false, "saddlebags")), "six extra slots");
        assertEquals(0, columns("horse", false, null), "a bare horse has no pack");
        assertEquals(0, columns("horse", false, "bridle"), "a bridle carries nothing");
        assertEquals(0, columns("horse", false, "pack_saddle"), "a pack saddle is not for horses");
        assertEquals(0, columns("horse", true, null), "horses have no chest to count");
        assertEquals(PackCapacity.HORSE_COLUMNS, PackCapacity.columns("horse", false, 5), "bags never make a horse a pack frame");
    }

    @Test void aPackSaddleOrAChestGivesDonkeysAndMulesAFullPack() {
        for (var animal : List.of("donkey", "mule")) {
            assertEquals(5, columns(animal, false, "pack_saddle"), animal + " with a pack saddle");
            assertEquals(5, columns(animal, true, null), animal + " with a chest (vanilla)");
            assertEquals(5, columns(animal, true, "pack_saddle"), animal + " with both still fits the screen");
            assertEquals(0, columns(animal, false, null), animal + " bare");
            assertEquals(0, columns(animal, false, "bridle"), animal + " in a bridle");
            assertEquals(5, columns(animal, true, "bridle"), animal + " in a bridle keeps its chest");
            assertEquals(0, columns(animal, false, "saddlebags"), "saddlebags are for horses only");
            assertEquals(15, PackCapacity.slots(columns(animal, false, "pack_saddle")));
        }
    }

    @Test void otherAnimalsKeepVanillaAndNothingPassesTheScreen() {
        for (var other : new String[]{"llama", "camel", "zombie_horse", "", null}) assertEquals(PackCapacity.KEEP, PackCapacity.columns(other, true, 5), "" + other);
        var r = new Random(7);
        for (int i = 0; i < 10_000; i++) {
            String animal = List.of("horse", "donkey", "mule").get(r.nextInt(3));
            int c = PackCapacity.columns(animal, r.nextBoolean(), r.nextInt(20) - 5);
            assertTrue(c >= 0 && c <= PackCapacity.MAX_COLUMNS, animal + " got " + c);
        }
        assertEquals(0, PackCapacity.tackColumns(null, "horse"));
        assertEquals(0, PackCapacity.tackColumns(gear("plate_barding"), "horse"), "barding is not tack");
        assertEquals(0, PackCapacity.slots(-3));
    }

    @Test void lanceMathReproducesVanillasKineticFormula() {
        assertEquals(20, LanceMath.vanilla(1, 12, 1.6), "1 + floor(19.2)");
        assertEquals(12, LanceMath.vanilla(1, 12, IRON_SPEAR_MULTIPLIER), "the iron spear at the same speed");
        assertEquals(1, LanceMath.vanilla(1, 0.5, 1.6), "rounded down");
        assertEquals(1, LanceMath.vanilla(1, -4, 1.6), "moving away deals only the base");
        assertEquals(10, LanceMath.blocksPerSecond(0.3, 0.4), 1e-9);
        assertEquals(12.648, LanceMath.horseSpeed(0.3), 1e-9);
    }

    @Test void theBondAndRidingBonusRaiseALanceHit() {
        assertEquals(20f, LanceMath.mounted(20, 0, 0));
        assertEquals(21f, LanceMath.mounted(20, 2, 0), 1e-5);
        assertEquals(22f, LanceMath.mounted(20, 4, 0), 1e-5, "Devoted adds 10%");
        assertEquals(22f, LanceMath.mounted(20, 9, 0), 1e-5, "tiers stop at Devoted");
        assertEquals(20f, LanceMath.mounted(20, -1, -0.5), 1e-5, "nothing ever lowers it");
        var r = new Random(7);
        for (int i = 0; i < 2_000; i++) {
            float damage = 1 + r.nextInt(30); int tier = r.nextInt(4); double bonus = r.nextDouble() * 0.5;
            assertTrue(LanceMath.mounted(damage, tier + 1, bonus) > LanceMath.mounted(damage, tier, bonus), "a higher tier hits harder");
            assertTrue(LanceMath.mounted(damage, tier, bonus + 0.05) > LanceMath.mounted(damage, tier, bonus), "a bigger bonus hits harder");
        }
    }

    @Test void aGallopBeatsTheIronSpearAndASprintCannotCouch() {
        var l = StableTable.lance();
        double gallop = LanceMath.vanilla(1, 12, l.damageMultiplier());
        assertTrue(gallop > LanceMath.vanilla(1, 12, IRON_SPEAR_MULTIPLIER), "lance " + gallop);
        assertFalse(LanceMath.couched(LanceMath.SPRINT, l.damageThreshold()), "a sprinting player can't land it");
        assertTrue(LanceMath.couched(12, l.damageThreshold()), "a gallop can");
        assertTrue(LanceMath.couched(l.damageThreshold(), l.damageThreshold()), "the threshold itself counts");
        var courser = StableTable.breed("courser").orElseThrow();
        assertTrue(LanceMath.horseSpeed(courser.speed().min()) > l.damageThreshold(), "even a slow courser charges fast enough");
        assertTrue(LanceMath.mounted((float) LanceMath.vanilla(1, 12, l.damageMultiplier()), 2, 0) > gallop, "a Trusting horse adds to it");
    }

    @Test void mountedArcheryIsSteadierWithTheBondAndCapped() {
        assertEquals(0.9f, ArcheryMath.uncertainty(1, 0, 0), 1e-6, "any rider gets a little help");
        assertEquals(0.5f, ArcheryMath.uncertainty(1, 4, 0), 1e-6);
        assertEquals(0.25f, ArcheryMath.uncertainty(1, 4, 5), 1e-6, "never steadier than a quarter of the spread");
        assertEquals(0.5, ArcheryMath.damping(0, 0), 1e-9);
        assertEquals(0.9, ArcheryMath.damping(4, 5), 1e-9, "an arrow always keeps some of the horse's speed");
        var r = new Random(7);
        for (int i = 0; i < 5_000; i++) {
            float base = r.nextFloat() * 14; int tier = r.nextInt(4); double bonus = r.nextDouble() * 0.6;
            assertTrue(ArcheryMath.uncertainty(base, tier + 1, bonus) <= ArcheryMath.uncertainty(base, tier, bonus), "tier never makes it worse");
            assertTrue(ArcheryMath.uncertainty(base, tier, bonus + .1) <= ArcheryMath.uncertainty(base, tier, bonus), "bonus never makes it worse");
            assertTrue(ArcheryMath.uncertainty(base, tier, bonus) >= base * (1 - ArcheryMath.MAX_STEADY) - 1e-5);
            assertTrue(ArcheryMath.damping(tier + 1, bonus) >= ArcheryMath.damping(tier, bonus));
            assertTrue(ArcheryMath.damping(tier, bonus) <= ArcheryMath.MAX_DAMPING && ArcheryMath.damping(tier, bonus) >= 0.5);
        }
    }

    @Test void tooltipsSayWhatEachRowDoes() {
        assertTrue(GearText.lines(gear("saddlebags")).contains("6 pack slots"));
        assertTrue(GearText.lines(gear("pack_saddle")).contains("15 pack slots, no chest needed"));
        assertTrue(GearText.lines(gear("pack_saddle")).contains("For donkeys and mules"));
        var bridle = GearText.lines(gear("bridle"));
        assertTrue(bridle.contains("Bond grows 1.5x faster while riding"), bridle.toString());
        assertTrue(bridle.contains("Keeps the animal calmer near monsters"));
        assertTrue(bridle.contains("For horses, donkeys and mules"));
        assertTrue(GearText.lines(gear("caparison")).stream().anyMatch(s -> s.startsWith("Dye it")));
        assertTrue(GearText.lines(gear("plate_barding")).equals(List.of("For horses")), "armor numbers are vanilla's lines");
        assertTrue(GearText.lance(StableTable.lance()).contains("Lands only above 7 blocks a second"));
    }

    @Test void everyGearRowHasItsEquipmentLayersItemAndTextures() throws Exception {
        for (var g : StableTable.gear()) {
            var equipment = json("/assets/villagefriends/equipment/" + g.id() + ".json").getAsJsonObject("layers");
            var layers = g.barding() ? List.of("horse_body") : g.animals().stream().map(SADDLE_LAYERS::get).toList();
            assertEquals(layers.size(), equipment.size(), g.id() + " layers " + equipment.keySet());
            for (var layer : layers) {
                var first = equipment.getAsJsonArray(layer).get(0).getAsJsonObject();
                String texture = first.get("texture").getAsString().replace("villagefriends:", "");
                assertNotNull(getClass().getResource("/assets/villagefriends/textures/entity/equipment/" + layer + "/" + texture + ".png"), g.id() + " " + layer);
                assertEquals(g.dyeable(), first.has("dyeable"), g.id() + " dyeable layer");
                if (g.dyeable()) assertEquals(g.undyed(), first.getAsJsonObject("dyeable").get("color_when_undyed").getAsInt());
            }
            assertNotNull(getClass().getResource("/assets/villagefriends/items/" + g.id() + ".json"), g.id() + " item definition");
            assertNotNull(getClass().getResource("/assets/villagefriends/textures/item/" + g.id() + ".png"), g.id() + " sprite");
            assertNotNull(getClass().getResource("/data/villagefriends/recipe/" + g.id() + ".json"), g.id() + " recipe");
        }
        var dye = json("/data/villagefriends/recipe/caparison_dyed.json");
        assertEquals("minecraft:crafting_dye", dye.get("type").getAsString());
        assertTrue(json("/data/minecraft/tags/item/cauldron_can_remove_dye.json").getAsJsonArray("values").toString().contains("villagefriends:caparison"));
        assertNotNull(getClass().getResource("/assets/villagefriends/textures/item/jousting_lance_in_hand.png"), "the lance held in hand");
    }

    private JsonObject json(String path) throws Exception {
        try (var in = getClass().getResourceAsStream(path)) {
            assertNotNull(in, path);
            return JsonParser.parseReader(new InputStreamReader(in, StandardCharsets.UTF_8)).getAsJsonObject();
        }
    }
}
