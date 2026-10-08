package dev.villagefriends;

import static org.junit.jupiter.api.Assertions.*;

import dev.villagefriends.home.House;
import dev.villagefriends.home.HouseCatalog;
import dev.villagefriends.home.HouseNames;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.levelgen.structure.BoundingBox;
import org.junit.jupiter.api.Test;

class HouseCatalogTest {
    private static final HouseCatalog CATALOG = HouseCatalog.builtin();

    @Test void everyVillageTypeHasHousesWithBeds() {
        for (String type : List.of("plains", "desert", "savanna", "snowy", "taiga")) {
            java.util.function.Predicate<HouseCatalog.Template> ofType = t -> type.equals("plains") ? !t.name().contains("/") : t.name().startsWith(type + "/");
            long homes = CATALOG.templates().stream().filter(t -> t.use() == House.Use.HOME && ofType.test(t)).count();
            assertTrue(homes >= 8, "Every village type has family homes: " + type + " has " + homes);
            for (var use : List.of(House.Use.INN, House.Use.BARRACKS, House.Use.QUARTERS))
                assertTrue(CATALOG.templates().stream().anyMatch(t -> t.use() == use && ofType.test(t)), type + " has " + use);
        }
    }

    @Test void everyBedHasItsFacingAndRoom() {
        for (var t : CATALOG.templates()) {
            assertEquals(t.bedFeet().size(), t.bedFacing().size(), t.id() + " has a facing for every bed");
            assertEquals(t.bedFeet().size(), t.bedRoom().size(), t.id() + " has a room for every bed");
            assertFalse(t.rooms().isEmpty(), t.id() + " has bedrooms");
            for (int n = 0; n < t.bedFeet().size(); n++) {
                int room = t.bedRoom().get(n);
                assertTrue(room >= 0 && room < t.rooms().size(), t.id() + " bed " + n + " belongs to a room");
                assertTrue(t.bedFacing().get(n).getAxis().isHorizontal());
            }
        }
    }

    @Test void everyBedIsInsideItsRoom() {
        for (var t : CATALOG.templates()) for (int n = 0; n < t.bedFeet().size(); n++) {
            var room = t.rooms().get(t.bedRoom().get(n));
            var box = BoundingBox.fromCorners(room.min(), room.max());
            var foot = t.bedFeet().get(n); var head = foot.relative(t.bedFacing().get(n));
            assertTrue(box.isInside(foot) && box.isInside(head), t.id() + " bed " + n + " at " + foot + " lies in " + room.name() + " " + box);
        }
    }

    @Test void everyHomeHasAPlaque() {
        var missing = new ArrayList<String>();
        for (var t : CATALOG.templates()) if (t.use() == House.Use.HOME && t.plaque().isEmpty()) missing.add(t.id());
        assertTrue(missing.isEmpty(), "Homes without a House Plaque: " + missing);
    }

    @Test void quartersKnowWhoseTheyAre() {
        for (var t : CATALOG.templates()) {
            if (t.use() == House.Use.BARRACKS) assertTrue(t.jobs().contains("knight") || t.jobs().contains("archer"), t.id());
            if (t.use() == House.Use.INN) assertTrue(t.jobs().contains("tavern_keeper"), t.id());
            if (t.use() == House.Use.QUARTERS) assertFalse(t.jobs().isEmpty(), t.id() + " has a workstation that says whose rooms they are");
        }
    }

    @Test void templatesTurnTheWayTheJigsawPlacesThem() {
        var local = new BlockPos(3, 1, 5); var origin = new BlockPos(100, 64, 200);
        var expected = Map.of(Rotation.NONE, new BlockPos(103, 65, 205), Rotation.CLOCKWISE_90, new BlockPos(95, 65, 203),
                Rotation.CLOCKWISE_180, new BlockPos(97, 65, 195), Rotation.COUNTERCLOCKWISE_90, new BlockPos(105, 65, 197));
        for (var e : expected.entrySet()) assertEquals(e.getValue(), HouseCatalog.place(local, e.getKey(), origin), e.getKey().name());
        // A bed facing north in the template faces east once its piece is turned clockwise; its head is a step that way.
        var t = CATALOG.template("villagefriends:village/cottage_oak");
        assertNotNull(t);
        for (var rotation : Rotation.values()) {
            var house = HouseCatalog.house(t, rotation, origin, new BoundingBox(origin));
            for (int n = 0; n < t.bedFeet().size(); n++) {
                var foot = HouseCatalog.place(t.bedFeet().get(n), rotation, origin);
                var bed = house.beds().stream().filter(b -> b.foot().equals(foot)).findFirst().orElseThrow();
                assertEquals(rotation.rotate(t.bedFacing().get(n)), bed.facing());
                assertEquals(bed.foot().relative(bed.facing()), bed.head());
                assertEquals(t.bedRoom().get(n), bed.room());
            }
            assertEquals(House.Use.HOME, house.use());
            assertTrue(house.plaque().isPresent());
        }
        assertEquals(Direction.EAST, Rotation.CLOCKWISE_90.rotate(Direction.NORTH));
    }

    @Test void housesHaveFriendlyNames() {
        assertEquals("Oak Cottage", HouseNames.label("villagefriends:village/cottage_oak"));
        assertEquals("Tall Brick House", HouseNames.label("villagefriends:village/house_tall_brick"));
        assertEquals("Adobe House", HouseNames.label("villagefriends:village/desert/adobe_house"));
        assertEquals("A-Frame", HouseNames.label("villagefriends:village/snowy/a_frame"));
        var t = CATALOG.template("villagefriends:village/cottage_oak");
        var house = HouseCatalog.house(t, Rotation.NONE, BlockPos.ZERO, new BoundingBox(BlockPos.ZERO));
        var mira = new dev.villagefriends.social.Townsfolk("m", "Mira Ashford", "FEMALE", "farmer", "warmhearted", true, 0, 0, "home", "", -1, false, Map.of(), "", -1);
        var pip = new dev.villagefriends.social.Townsfolk("p", "Pip Reed", "MALE", "none", "playful", false, 5, 5, "home", "", -1, false, Map.of(), "", -1);
        Map<String, dev.villagefriends.social.Townsfolk> folk = Map.of("m", mira, "p", pip);
        assertEquals("The Ashford House", HouseNames.name(house, List.of("p", "m"), folk::get), "Named after the grown-up who has lived there longest");
        assertEquals("Oak Cottage", HouseNames.name(house, List.of(), folk::get), "An empty house is named for what it is");
        assertEquals("The Reed Place", HouseNames.name(house.named("The Reed Place"), List.of("m"), folk::get), "A plaque's own name wins");
        var garrison = HouseCatalog.house(CATALOG.template("villagefriends:village/garrison"), Rotation.NONE, BlockPos.ZERO, new BoundingBox(BlockPos.ZERO));
        assertEquals("The Garrison", HouseNames.name(garrison, List.of("m"), folk::get));
        var apothecary = HouseCatalog.house(CATALOG.template("villagefriends:village/apothecary"), Rotation.NONE, BlockPos.ZERO, new BoundingBox(BlockPos.ZERO));
        assertEquals("The Apothecary's Rooms", HouseNames.name(apothecary, List.of("m"), folk::get));
    }
}
