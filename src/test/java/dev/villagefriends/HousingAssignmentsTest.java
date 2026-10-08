package dev.villagefriends;

import static org.junit.jupiter.api.Assertions.*;

import com.mojang.serialization.JsonOps;
import dev.villagefriends.home.Assignments;
import dev.villagefriends.home.House;
import dev.villagefriends.home.HousingBook;
import dev.villagefriends.home.HousingIndex;
import dev.villagefriends.social.Townsfolk;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Random;
import java.util.Set;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.level.levelgen.structure.BoundingBox;
import org.junit.jupiter.api.Test;

class HousingAssignmentsTest {
    // -- a little village to assign beds in ---------------------------------------------------------

    private static House.Bed bed(int x, int z, int room) { return bed(x, 64, z, Direction.NORTH, room); }
    private static House.Bed bed(int x, int y, int z, Direction facing, int room) {
        var foot = new BlockPos(x, y, z);
        return new House.Bed(foot.relative(facing), foot, facing, room, true);
    }
    private static House house(String id, House.Use use, List<House.Workstation> stations, House.Bed... beds) {
        var rooms = new ArrayList<House.Room>();
        int maxRoom = 0;
        for (var b : beds) maxRoom = Math.max(maxRoom, b.room());
        for (int r = 0; r <= maxRoom; r++) rooms.add(new House.Room("room" + r, new BoundingBox(0, 64, 0, 1, 65, 1)));
        return new House(id, House.Kind.GENERATED, "villagefriends:village/" + id, use, new BoundingBox(0, 60, 0, 10, 70, 10), rooms, List.of(beds),
                List.of(), stations, Optional.empty(), "", false, true, 1);
    }
    private static House home(String id, int at, int beds) {
        var list = new House.Bed[beds];
        for (int i = 0; i < beds; i++) list[i] = bed(at + i * 4, at, 0);
        return house(id, House.Use.HOME, List.of(), list);
    }
    private static House player(String id, int at, int beds, boolean closed) {
        var h = home(id, at, beds);
        return new House(id, House.Kind.PLAYER, "", House.Use.HOME, h.box(), h.rooms(), h.beds(), List.of(), List.of(), Optional.of(new BlockPos(at, 64, at)), "", closed, true, 1);
    }
    private static Townsfolk adult(String id, String job) { return person(id, job, true, "", Map.of(), "", -1, 0); }
    private static Townsfolk person(String id, String job, boolean adult, String partner, Map<String, String> kin, String household, int born, long joined) {
        return new Townsfolk(id, "Neighbor " + id.toUpperCase(), "FEMALE", job, "warmhearted", adult, joined, joined, Townsfolk.HOME, partner, partner.isEmpty() ? -1 : 0,
                false, kin, household, born);
    }
    /** Two partners and (optionally) their children. */
    private static List<Townsfolk> family(String a, String b, String... children) {
        var kinA = new HashMap<String, String>(); var kinB = new HashMap<String, String>(); var out = new ArrayList<Townsfolk>();
        for (String c : children) { kinA.put(c, "child"); kinB.put(c, "child"); }
        out.add(person(a, "farmer", true, b, kinA, a, -1, 0));
        out.add(person(b, "fisherman", true, a, kinB, a, -1, 0));
        for (String c : children) out.add(person(c, "none", false, "", Map.of(a, "parent", b, "parent"), a, -1, 1));
        return out;
    }
    private static HousingIndex index(House... houses) {
        return new HousingIndex("natural:0:0", List.of(houses), Map.of(), List.of(), Map.of(), List.of(), Map.of(), Map.of(), 0, true);
    }
    private static HousingIndex assign(HousingIndex index, List<Townsfolk> folk) { return assign(index, folk, 10); }
    private static HousingIndex assign(HousingIndex index, List<Townsfolk> folk, long day) { return Assignments.assign(index, folk, Map.of(), Set.of(), day); }

    // -- households ---------------------------------------------------------------------------------

    @Test void partnersTakeTheClosestPairInOneRoom() {
        var h = house("cottage", House.Use.HOME, List.of(), bed(0, 0, 0), bed(9, 9, 1), bed(2, 0, 0));
        var result = assign(index(h), family("a", "b"));
        var a = result.bedOf("a").orElseThrow(); var b = result.bedOf("b").orElseThrow();
        assertEquals(0, a.room()); assertEquals(0, b.room());
        assertTrue(a.beside(b), "Partners sleep side by side");
        assertTrue(result.needs().isEmpty() && result.homeless().isEmpty());
    }

    @Test void childrenLiveWithTheirParentsInAnotherRoom() {
        var family = house("family_house", House.Use.HOME, List.of(), bed(0, 0, 0), bed(2, 0, 0), bed(8, 8, 1));
        var small = home("hut", 40, 2);
        var result = assign(index(family, small), family("a", "b", "c"));
        assertEquals("family_house", result.houseOf("c").id(), "The child lives with their parents");
        assertEquals(1, result.bedOf("c").orElseThrow().room(), "The child has the other room");
        assertEquals(0, result.bedOf("a").orElseThrow().room());
        assertTrue(result.needs().isEmpty());
    }

    @Test void aNewbornGetsABedOrTheFamilyNeedsOne() {
        var folk = new ArrayList<>(family("a", "b"));
        var withBaby = new ArrayList<>(family("a", "b", "baby"));
        // The baby was born in the village.
        withBaby.set(2, person("baby", "none", false, "", Map.of("a", "parent", "b", "parent"), "a", 100, 5));
        var cramped = assign(index(home("pair", 0, 2)), folk);
        var after = assign(cramped, withBaby);
        assertTrue(after.bedOf("a").isPresent() && after.bedOf("b").isPresent(), "The parents keep their beds");
        assertTrue(after.bedOf("baby").isEmpty() && after.homeless().contains("baby"));
        assertEquals(HousingIndex.NEWBORN, after.needOf("baby").kind(), "The family is waiting for a bed for the baby");
        // With a spare bed in their house the baby gets it.
        var roomy = assign(index(home("trio", 0, 3)), withBaby);
        assertEquals("trio", roomy.houseOf("baby").id());
        assertNull(roomy.needOf("baby"));
    }

    @Test void quartersBarracksAndTheInnTakeTheirOwnAndTheOverflow() {
        var inn = house("tavern", House.Use.INN, List.of(new House.Workstation(new BlockPos(1, 64, 1), "villagefriends:cook")), bed(100, 0, 0), bed(102, 0, 0));
        var barracks = house("garrison", House.Use.BARRACKS, List.of(new House.Workstation(new BlockPos(1, 64, 1), "villagefriends:knight")), bed(200, 0, 0));
        var apothecary = house("apothecary", House.Use.QUARTERS, List.of(new House.Workstation(new BlockPos(1, 64, 1), "villagefriends:apothecary")), bed(300, 0, 0));
        var cottage = home("cottage", 0, 1);
        var folk = List.of(adult("cook", "cook"), adult("knight", "knight"), adult("healer", "apothecary"), adult("farmer", "farmer"), adult("fisher", "fisherman"));
        var result = assign(index(inn, barracks, apothecary, cottage), folk);
        assertEquals("tavern", result.houseOf("cook").id(), "The cook sleeps at the inn");
        assertEquals("garrison", result.houseOf("knight").id(), "The knight sleeps in the barracks");
        assertEquals("apothecary", result.houseOf("healer").id(), "The apothecary sleeps over the shop");
        assertEquals("cottage", result.houseOf("farmer").id(), "Family homes go to everyone else first");
        assertEquals("tavern", result.houseOf("fisher").id(), "Whoever is left over lodges at the inn");
        assertEquals(HousingIndex.CROWDED, result.needOf("fisher").kind(), "Lodging at the inn means they need a home");
        assertNull(result.needOf("cook"), "The cook belongs at the inn");
    }

    @Test void homelessHouseholdsMoveIntoPlayerHousesUnlessPrivate() {
        var folk = new ArrayList<>(family("a", "b")); folk.add(adult("c", "mason"));
        var none = assign(index(home("hut", 0, 1)), folk);
        assertEquals(HousingIndex.HOMELESS, none.needOf("a").kind());
        assertEquals(List.of("a", "b"), none.needOf("a").members());
        var closed = assign(index(home("hut", 0, 1), player("p:5,64,5", 50, 2, true)), folk);
        assertNull(closed.houseOf("a"), "Nobody moves into a private house");
        var open = assign(index(home("hut", 0, 1), player("p:5,64,5", 50, 2, false)), folk);
        assertEquals("p:5,64,5", open.houseOf("a").id(), "A homeless household moves into the house a player built");
        assertEquals("p:5,64,5", open.houseOf("b").id());
        assertNull(open.needOf("a"));
        // Those who asked on the notice board move in first.
        var asked = Assignments.assign(index(player("p:5,64,5", 50, 1, false)), List.of(adult("x", "mason"), adult("y", "mason")), Map.of(), Set.of("y"), 10);
        assertEquals("p:5,64,5", asked.houseOf("y").id());
    }

    @Test void housesNobodyHasCheckedYetStillTakeTheirFamilies() {
        // Only the houses near the player are loaded and checked when beds are first handed out.
        var near = home("near", 0, 2);
        var far = home("far", 50, 2);
        var unchecked = new House(far.id(), far.kind(), far.template(), far.use(), far.box(), far.rooms(), far.beds(), far.doors(), far.workstations(),
                far.plaque(), "", false, false, 0);
        var folk = new ArrayList<>(family("a", "b")); folk.addAll(family("c", "d"));
        var result = assign(index(near, unchecked), folk);
        assertTrue(result.needs().isEmpty(), "Both families have a whole house, the unchecked one from its catalog beds: " + result.needs());
        assertEquals(result.houseOf("a").id(), result.houseOf("b").id());
        assertEquals(result.houseOf("c").id(), result.houseOf("d").id());
        assertNotEquals(result.houseOf("a").id(), result.houseOf("c").id(), "Nobody is crammed into the loaded house");
        // A player's house is only lived in once its plaque has looked it over.
        var p = player("p:5,64,5", 80, 2, false);
        var unflooded = new House(p.id(), p.kind(), p.template(), p.use(), p.box(), p.rooms(), p.beds(), p.doors(), p.workstations(), p.plaque(), "", false, false, 0);
        assertNull(assign(index(unflooded), family("a", "b")).houseOf("a"));
    }

    @Test void aLodgerGivesWayWhenTheFamilyItLodgesWithNeedsTheBed() {
        // A single newcomer with nowhere else to go takes the spare bed in the Ashfords' home.
        var folk = new ArrayList<>(family("a", "b")); folk.add(adult("s", "mason"));
        var before = assign(index(home("ashford", 0, 3)), folk);
        assertEquals("ashford", before.houseOf("s").id(), "The newcomer lodges in the spare bed");
        var again = assign(before, folk, 11);
        assertEquals(before.beds(), again.beds(), "Nothing changes while the family has room");
        // The Ashfords have a baby: the bed goes to the baby, and the lodger has to find somewhere else.
        var withBaby = new ArrayList<>(family("a", "b", "baby"));
        withBaby.set(2, person("baby", "none", false, "", Map.of("a", "parent", "b", "parent"), "a", 100, 5));
        withBaby.add(adult("s", "mason"));
        var after = assign(again, withBaby, 12);
        assertEquals("ashford", after.houseOf("baby").id(), "The baby gets the bed in their family's home");
        assertEquals(before.beds().get("a"), after.beds().get("a"), "The parents keep their beds");
        assertNull(after.needOf("a"), "The family has room");
        assertNull(after.houseOf("s"), "The lodger moved out");
    }

    // -- stability and determinism ------------------------------------------------------------------

    private static List<Townsfolk> village() {
        var folk = new ArrayList<Townsfolk>();
        folk.addAll(family("a", "b", "c"));
        folk.addAll(family("d", "e"));
        for (String id : List.of("f", "g", "h", "i")) folk.add(adult(id, id.equals("g") ? "knight" : "farmer"));
        return folk;
    }
    private static House[] houses() {
        return new House[]{house("family", House.Use.HOME, List.of(), bed(0, 0, 0), bed(2, 0, 0), bed(6, 6, 1)), home("cottage", 20, 2), home("hut", 40, 1),
                house("garrison", House.Use.BARRACKS, List.of(new House.Workstation(new BlockPos(0, 64, 0), "villagefriends:knight")), bed(60, 0, 0), bed(62, 0, 0)),
                house("tavern", House.Use.INN, List.of(), bed(80, 0, 0), bed(82, 0, 0))};
    }

    @Test void theSameVillageAlwaysGetsTheSameBeds() {
        var first = assign(index(houses()), village());
        var random = new Random(7);
        for (int i = 0; i < 5; i++) {
            var folk = new ArrayList<>(village()); Collections.shuffle(folk, random);
            var list = new ArrayList<>(List.of(houses())); Collections.shuffle(list, random);
            var again = assign(index(list.toArray(House[]::new)), folk);
            assertEquals(first.beds(), again.beds(), "Shuffled inputs give the same beds");
            assertEquals(first.needs(), again.needs());
        }
    }

    @Test void bedsStayPutWhenAnUnrelatedHouseIsAdded() {
        var enough = new ArrayList<>(List.of(houses())); enough.add(home("cottage_two", 120, 2));
        var before = assign(index(enough.toArray(House[]::new)), village());
        assertTrue(before.needs().isEmpty(), "Everyone has a home of their own: " + before.needs());
        var more = new ArrayList<>(before.houses()); more.add(home("new_cottage", 100, 4));
        var after = assign(before.withHouses(more), village(), 11);
        assertEquals(before.beds(), after.beds(), "Nobody moves because a new house went up");
    }

    @Test void aDeathFreesTheBedAndIsRemembered() {
        var before = assign(index(houses()), village());
        var bed = before.beds().get("f");
        var folk = new ArrayList<Townsfolk>();
        for (var t : village()) folk.add(t.id().equals("f") ? t.status(Townsfolk.PASSED) : t);
        var after = assign(before, folk, 12);
        assertFalse(after.beds().containsKey("f"));
        assertEquals("h", after.owner(bed.head()), "Their bed is freed, and a neighbor lodging at the inn moves in");
        assertNull(after.needOf("h"));
        var vacancy = after.vacated().getLast();
        assertEquals("f", vacancy.resident()); assertEquals("passed", vacancy.why()); assertEquals(12, vacancy.day());
        assertEquals(bed.head(), vacancy.bed());
    }

    @Test void aCursedResidentsBedWaitsAWeek() {
        var before = assign(index(houses()), village());
        var bed = before.beds().get("h");
        var folk = new ArrayList<Townsfolk>();
        for (var t : village()) folk.add(t.id().equals("h") ? t.status(Townsfolk.CURSED) : t);
        var cursed = assign(before, folk, 20);
        assertEquals(bed, cursed.beds().get("h"), "Their bed is kept for them");
        assertEquals(20L, cursed.cursed().get("h"));
        var sixDays = assign(cursed, folk, 26);
        assertEquals(bed, sixDays.beds().get("h"));
        var week = assign(sixDays, folk, 27);
        assertFalse(week.beds().containsKey("h"), "After a week the bed is freed");
        assertEquals("cursed", week.vacated().getLast().why());
        // Cured, they find a bed again.
        var cured = assign(week, village(), 28);
        assertTrue(cured.beds().containsKey("h"));
    }

    @Test void aBrokenBedIsGivenUp() {
        var before = assign(index(home("cottage", 0, 2), home("spare", 50, 1)), List.of(adult("a", "farmer"), adult("b", "farmer")));
        var key = before.beds().get("a"); var h = before.house(key.house());
        var beds = new ArrayList<House.Bed>();
        for (var b : h.beds()) beds.add(b.head().equals(key.head()) ? b.present(false) : b);
        var after = assign(before.withHouse(h.withBeds(beds)), List.of(adult("a", "farmer"), adult("b", "farmer")), 11);
        assertNotEquals(key, after.beds().get("a"), "They sleep somewhere else now");
        assertTrue(after.beds().containsKey("a"));
        assertEquals(before.beds().get("b"), after.beds().get("b"), "Their housemate keeps their bed");
    }

    // -- saving -------------------------------------------------------------------------------------

    @Test void theBookSavesAndLoads() {
        var assigned = assign(index(houses()), village());
        var book = HousingBook.EMPTY.put(assigned);
        var json = HousingBook.CODEC.encodeStart(JsonOps.INSTANCE, book).getOrThrow();
        var back = HousingBook.CODEC.parse(JsonOps.INSTANCE, json).getOrThrow();
        assertEquals(book, back, "The housing book round-trips");
        assertEquals(HousingIndex.empty("nowhere"), HousingBook.EMPTY.get("nowhere"), "A village nobody surveyed has an empty index");
        var empty = HousingBook.CODEC.parse(JsonOps.INSTANCE, new com.google.gson.JsonObject()).getOrThrow();
        assertEquals(HousingBook.FORMAT, empty.format());
        assertTrue(empty.villages().isEmpty(), "An absent attachment is an empty book");
        var future = json.deepCopy().getAsJsonObject(); future.addProperty("format", HousingBook.FORMAT + 1);
        assertTrue(HousingBook.CODEC.parse(JsonOps.INSTANCE, future).isError(), "A book from a newer version is refused, not misread");
    }
}
