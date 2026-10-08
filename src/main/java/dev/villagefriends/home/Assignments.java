package dev.villagefriends.home;

import dev.villagefriends.home.HousingIndex.BedKey;
import dev.villagefriends.home.HousingIndex.Need;
import dev.villagefriends.home.HousingIndex.Vacancy;
import dev.villagefriends.social.Townsfolk;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;
import net.minecraft.core.BlockPos;

/**
 * Who sleeps in which bed. Pure and deterministic: the same houses and residents always give the same
 * beds, whatever order they come in, and a bed someone already has stays theirs while it still makes sense.
 *
 * <p>Residents are grouped into households: partners, their young children, and children who share a
 * household with them. Each household keeps the beds it has in the house that holds most of it (a smaller
 * household lodging in a bigger family's home gives its beds up when that family needs them); the rest
 * are placed together in one house: the one they already live in, the house of the bed they used to sleep
 * in, their parents' house (a grown child living alone), their own quarters (the apothecary over the shop,
 * guards in the barracks, the tavern keeper and cook at the inn), then the smallest family home with room
 * for all of them. Households that fit nowhere move into a house a player built, if one isn't private.
 * Whoever still has no bed takes any free one (the inn, the barracks, then anyone's spare bed), and the
 * household is recorded as homeless, crowded, or waiting for a bed for their new baby.
 *
 * <p>Partners take the two closest beds in one room; children take a bed in another room when there is
 * one. Residents who passed away or left free their beds, which are remembered as {@link Vacancy vacancies};
 * a resident turned into a zombie villager keeps their bed for {@link #CURSED_DAYS} days in case they are cured.
 */
public final class Assignments {
    /** How long a bed waits for a resident who was turned into a zombie villager. */
    public static final int CURSED_DAYS = 7;

    /** A household: its members (by id) in a stable order, and whether each is a minor or a baby born here. */
    record Unit(List<Townsfolk> members) {
        String key() { return members.getFirst().id(); }
        int size() { return members.size(); }
        boolean has(String id) { for (var t : members) if (t.id().equals(id)) return true; return false; }
    }

    /**
     * Assigns beds for one village.
     *
     * @param previous the village's index: its houses and who had which bed until now
     * @param folk everyone the village knows (living, passed and cursed)
     * @param anchors each resident's current vanilla home bed (its head), used to keep residents near where they already sleep
     * @param noticed residents whose household has an open "we need a bigger house" notice: they move into player houses first
     * @param today the village's day
     * @return the index with new beds, homeless, needs, vacancies, move-in days and cursed reservations
     */
    public static HousingIndex assign(HousingIndex previous, Collection<Townsfolk> folk, Map<String, BlockPos> anchors, Set<String> noticed, long today) {
        var byId = new TreeMap<String, Townsfolk>();
        for (var t : folk) byId.put(t.id(), t);
        var houses = new ArrayList<>(previous.houses());
        houses.sort(Comparator.comparing(House::id));
        var houseById = new HashMap<String, House>();
        for (var h : houses) houseById.put(h.id(), h);

        var beds = new LinkedHashMap<String, BedKey>();
        var vacated = new ArrayList<>(previous.vacated());
        var cursed = new TreeMap<String, Long>();
        var taken = new HashMap<BedKey, String>();

        // Residents who passed away or left free their beds; the cursed keep theirs for a week.
        for (var e : new TreeMap<>(previous.beds()).entrySet()) {
            String id = e.getKey(); var key = e.getValue(); var t = byId.get(id);
            String why = t == null ? "moved" : !t.living() ? "passed" : null;
            if (why == null && t.status().equals(Townsfolk.CURSED)) {
                long since = previous.cursed().getOrDefault(id, today);
                if (today - since >= CURSED_DAYS) why = "cursed";
                else { cursed.put(id, since); if (usable(houseById, key, false)) { beds.put(id, key); taken.put(key, id); } continue; }
            }
            if (why != null) vacated.add(new Vacancy(id, t == null ? "" : t.name(), key.house(), key.head(), today, why));
        }
        for (var t : byId.values()) if (t.status().equals(Townsfolk.CURSED) && !cursed.containsKey(t.id())) cursed.put(t.id(), previous.cursed().getOrDefault(t.id(), today));

        var units = units(byId);
        // The biggest household sleeping in each house, to tell a family from the lodgers in its home.
        var biggest = new HashMap<String, Integer>();
        for (var unit : units) for (var t : unit.members()) {
            var key = previous.beds().get(t.id());
            if (key != null && usable(houseById, key, false)) biggest.merge(key.house(), unit.size(), Math::max);
        }
        // Keep what still makes sense: each household's beds in the house that holds most of it.
        var kept = new HashMap<String, String>(); // unit key -> house it keeps
        var lodgers = new HashSet<String>();
        for (var unit : units) {
            var count = new TreeMap<String, Integer>();
            for (var t : unit.members()) {
                var key = previous.beds().get(t.id());
                if (key != null && usable(houseById, key, false) && !taken.containsKey(key)) count.merge(key.house(), 1, Integer::sum);
            }
            if (count.isEmpty()) continue;
            String best = null;
            for (var e : count.entrySet()) if (best == null || e.getValue() > count.get(best)) best = e.getKey();
            kept.put(unit.key(), best);
            // Lodging in a bigger family's home: they take their beds back below, once that family has what it needs.
            if (houseById.get(best).use() == House.Use.HOME && biggest.getOrDefault(best, 0) > unit.size()) { lodgers.add(unit.key()); continue; }
            for (var t : unit.members()) {
                var key = previous.beds().get(t.id());
                if (key != null && key.house().equals(best) && usable(houseById, key, false) && !taken.containsKey(key)) { beds.put(t.id(), key); taken.put(key, t.id()); }
            }
        }

        // Place everyone else, whole households first; households split between houses or lodging at the inn try to move together.
        var unplaced = new ArrayList<Unit>();
        for (var unit : units) {
            if (settled(unit, beds, houseById)) continue;
            if (lodgers.contains(unit.key()) && retake(unit, previous, houseById, beds, taken)) continue;
            var house = choose(unit, houses, houseById, kept.get(unit.key()), anchors, previous, beds, taken, false);
            if (house == null) { unplaced.add(unit); continue; }
            moveInto(unit, house, beds, taken);
        }
        // Households that fit nowhere else move into a house a player built (those who asked on the notice board first).
        unplaced.sort(Comparator.comparing((Unit u) -> u.members().stream().noneMatch(t -> noticed.contains(t.id()))).thenComparing(u -> units.indexOf(u)));
        var stillUnplaced = new ArrayList<Unit>();
        for (var unit : unplaced) {
            var house = choose(unit, houses, houseById, kept.get(unit.key()), anchors, previous, beds, taken, true);
            if (house == null) { stillUnplaced.add(unit); continue; }
            moveInto(unit, house, beds, taken);
        }
        // Whoever is left takes any free bed: their own house first, then the inn and barracks, then anyone's spare bed.
        for (var unit : stillUnplaced) {
            String home = homeOf(unit, beds);
            for (var t : unit.members()) {
                if (beds.containsKey(t.id()) || newborn(t)) continue;
                // The bed they had, if it's still free; otherwise any.
                var before = previous.beds().get(t.id());
                var bed = before != null && usable(houseById, before, true) && !taken.containsKey(before) ? before : spare(t, home, houses, taken);
                if (bed != null) { beds.put(t.id(), bed); taken.put(bed, t.id()); if (home == null) home = bed.house(); }
            }
            // A baby takes a free bed only in the house where their family sleeps.
            for (var t : unit.members()) {
                if (beds.containsKey(t.id()) || !newborn(t) || home == null) continue;
                var h = houseById.get(home);
                var bed = h == null ? null : pick(h, t, unit, beds, taken);
                if (bed != null) { beds.put(t.id(), bed); taken.put(bed, t.id()); }
            }
        }

        // Who is short of room.
        var needs = new TreeMap<String, Need>();
        var homeless = new ArrayList<String>();
        for (var unit : units) {
            int housedCount = 0; var used = new HashSet<String>(); boolean lodging = false, waitingBaby = false, missing = false;
            for (var t : unit.members()) {
                var key = beds.get(t.id());
                if (key == null) {
                    homeless.add(t.id());
                    if (newborn(t)) waitingBaby = true; else missing = true;
                    continue;
                }
                housedCount++; used.add(key.house());
                var h = houseById.get(key.house());
                if (h != null && (h.use() == House.Use.INN || h.use() == House.Use.BARRACKS) && !h.jobs().contains(t.job())) lodging = true;
            }
            var members = unit.members().stream().map(Townsfolk::id).toList();
            String kind = housedCount == 0 ? HousingIndex.HOMELESS : missing || used.size() > 1 || lodging ? HousingIndex.CROWDED
                    : waitingBaby ? HousingIndex.NEWBORN : null;
            if (kind != null) needs.put(unit.key(), new Need(kind, members, housedCount));
        }
        homeless.sort(Comparator.naturalOrder());

        // When each resident moved into the house they sleep in now.
        var moved = new TreeMap<String, Long>();
        for (var e : beds.entrySet()) {
            var before = previous.beds().get(e.getKey());
            moved.put(e.getKey(), before != null && before.house().equals(e.getValue().house()) ? previous.moved().getOrDefault(e.getKey(), today) : today);
        }
        var sortedBeds = new TreeMap<>(beds);
        return new HousingIndex(previous.village(), previous.houses(), sortedBeds, homeless, needs, vacated, moved, cursed, previous.stamp(), previous.surveyed());
    }

    // -- households --------------------------------------------------------------------------------

    /** Residents at home grouped into households: partners, their minor children, and minors sharing a household. Largest first. */
    static List<Unit> units(Map<String, Townsfolk> byId) {
        var home = new TreeMap<String, Townsfolk>();
        for (var t : byId.values()) if (t.home()) home.put(t.id(), t);
        var parent = new HashMap<String, String>();
        for (String id : home.keySet()) parent.put(id, id);
        for (var t : home.values()) {
            if (!t.partner().isEmpty() && home.containsKey(t.partner())) union(parent, t.id(), t.partner());
            if (t.adult()) continue;
            for (var k : t.kin().entrySet()) if (k.getValue().equals("parent") && home.containsKey(k.getKey())) union(parent, t.id(), k.getKey());
            if (!t.household().isEmpty()) for (var o : home.values()) if (o != t && t.household().equals(o.household())) union(parent, t.id(), o.id());
        }
        var groups = new TreeMap<String, List<Townsfolk>>();
        for (var t : home.values()) groups.computeIfAbsent(find(parent, t.id()), k -> new ArrayList<>()).add(t);
        var units = new ArrayList<Unit>();
        for (var g : groups.values()) {
            g.sort(Comparator.comparing((Townsfolk t) -> !t.adult()).thenComparingLong(Townsfolk::joined).thenComparing(Townsfolk::id));
            units.add(new Unit(List.copyOf(g)));
        }
        units.sort(Comparator.comparingInt((Unit u) -> -u.size())
                .thenComparingLong(u -> u.members().stream().mapToLong(Townsfolk::joined).min().orElse(0))
                .thenComparing(u -> u.members().stream().map(Townsfolk::id).min(Comparator.naturalOrder()).orElse("")));
        return units;
    }
    private static String find(Map<String, String> parent, String id) {
        String root = id;
        while (!parent.get(root).equals(root)) root = parent.get(root);
        return root;
    }
    private static void union(Map<String, String> parent, String a, String b) {
        String x = find(parent, a), y = find(parent, b);
        if (x.equals(y)) return;
        if (x.compareTo(y) < 0) parent.put(y, x); else parent.put(x, y);
    }
    /** A baby born in the village who is still a child. */
    static boolean newborn(Townsfolk t) { return !t.adult() && t.born() >= 0; }

    // -- houses ------------------------------------------------------------------------------------

    /**
     * Whether a house's beds can be given out: it was checked, or it is one the village built and nobody has checked
     * yet (its beds are the catalog's, checked once its chunks load), so the first beds handed out cover the whole
     * village and not only the houses that happened to be loaded.
     */
    static boolean trusted(House h) { return h.verified() || h.kind() == House.Kind.GENERATED; }
    /** Whether a bed can be slept in: it is still there in a house that can be trusted (or not yet checked, for keeping it). */
    private static boolean usable(Map<String, House> houses, BedKey key, boolean placing) {
        var h = houses.get(key.house());
        if (h == null || h.privateHome()) return false;
        var bed = h.bed(key.head());
        if (bed == null) return false;
        return trusted(h) ? bed.present() : !placing;
    }
    /** A household lodging in a bigger family's home takes back the beds it had there, if they are all still free. */
    private static boolean retake(Unit unit, HousingIndex previous, Map<String, House> houses, Map<String, BedKey> beds, Map<BedKey, String> taken) {
        var keys = new LinkedHashMap<String, BedKey>(); String house = null;
        for (var t : unit.members()) {
            var key = previous.beds().get(t.id());
            if (key == null || house != null && !house.equals(key.house()) || !usable(houses, key, false) || taken.containsKey(key)) return false;
            house = key.house(); keys.put(t.id(), key);
        }
        keys.forEach((id, key) -> { beds.put(id, key); taken.put(key, id); });
        return true;
    }
    /** Everyone in the household has a bed, all in one house, and it is their own (not someone else's barracks or the inn's guest rooms). */
    private static boolean settled(Unit unit, Map<String, BedKey> beds, Map<String, House> houses) {
        String house = null;
        for (var t : unit.members()) {
            var key = beds.get(t.id());
            if (key == null || house != null && !house.equals(key.house())) return false;
            house = key.house();
        }
        return house != null && !lodging(unit, houses.get(house));
    }
    /** Sleeping in guest rooms or barracks that aren't for anyone in the household. */
    private static boolean lodging(Unit unit, House h) {
        if (h == null || h.use() != House.Use.INN && h.use() != House.Use.BARRACKS) return false;
        for (var t : unit.members()) if (!h.jobs().contains(t.job())) return true;
        return false;
    }
    private static List<House.Bed> free(House h, Map<BedKey, String> taken) {
        var out = new ArrayList<House.Bed>();
        if (!trusted(h) || h.privateHome()) return out;
        for (var b : h.beds()) if (b.present() && !taken.containsKey(new BedKey(h.id(), b.head()))) out.add(b);
        return out;
    }
    /** Room for the whole household in this house, counting the beds it already has there. */
    private static boolean fits(Unit unit, House h, Map<String, BedKey> beds, Map<BedKey, String> taken) {
        int have = 0;
        for (var t : unit.members()) { var key = beds.get(t.id()); if (key != null && key.house().equals(h.id())) have++; }
        return have + free(h, taken).size() >= unit.size();
    }
    /** The house a household moves into, or null when none has room for all of them. */
    private static House choose(Unit unit, List<House> houses, Map<String, House> houseById, String kept, Map<String, BlockPos> anchors,
            HousingIndex previous, Map<String, BedKey> beds, Map<BedKey, String> taken, boolean playerHouses) {
        var order = new ArrayList<House>();
        if (playerHouses) {
            houses.stream().filter(h -> h.kind() == House.Kind.PLAYER).sorted(Comparator.comparingInt((House h) -> h.beds().size()).thenComparing(House::id)).forEach(order::add);
        } else {
            if (kept != null && houseById.containsKey(kept)) order.add(houseById.get(kept));
            // The house of the bed they already sleep in.
            var anchored = new TreeMap<String, Integer>();
            for (var t : unit.members()) {
                var head = anchors.get(t.id()); if (head == null) continue;
                for (var h : houses) if (h.bed(head) != null) anchored.merge(h.id(), 1, Integer::sum);
            }
            anchored.entrySet().stream().sorted(Map.Entry.<String, Integer>comparingByValue().reversed().thenComparing(Map.Entry.comparingByKey()))
                    .forEach(e -> order.add(houseById.get(e.getKey())));
            // A grown child living alone stays near their parents, or the family they arrived with.
            for (var t : unit.members()) for (var k : t.kin().entrySet()) if (k.getValue().equals("parent")) {
                var key = beds.get(k.getKey()); if (key != null && houseById.containsKey(key.house())) order.add(houseById.get(key.house()));
            }
            // Someone on their own sleeps where they work: quarters, the barracks or the inn.
            if (unit.size() == 1) {
                String job = unit.members().getFirst().job();
                houses.stream().filter(h -> h.use() != House.Use.HOME && h.jobs().contains(job)).forEach(order::add);
            }
            houses.stream().filter(h -> h.use() == House.Use.HOME && h.kind() != House.Kind.PLAYER)
                    .sorted(Comparator.comparingInt((House h) -> h.presentBeds().size()).thenComparing(House::id)).forEach(order::add);
        }
        for (var h : order) {
            if (h == null || h.privateHome() || lodging(unit, h)) continue;
            if (!playerHouses && h.kind() == House.Kind.PLAYER && !h.id().equals(kept)) continue;
            if (fits(unit, h, beds, taken)) return h;
        }
        return null;
    }
    /** Moves a household into {@code h}: beds they had elsewhere are given up, partners share a room, children take another. */
    private static void moveInto(Unit unit, House h, Map<String, BedKey> beds, Map<BedKey, String> taken) {
        for (var t : unit.members()) {
            var key = beds.get(t.id());
            if (key != null && !key.house().equals(h.id())) { beds.remove(t.id()); taken.remove(key); }
        }
        // Partners first, then the other grown-ups, then the children.
        var order = new ArrayList<>(unit.members());
        order.sort(Comparator.comparing((Townsfolk t) -> !(t.adult() && !t.partner().isEmpty() && unit.has(t.partner()))).thenComparing(t -> !t.adult()));
        for (var t : order) {
            if (beds.containsKey(t.id())) continue;
            var bed = pick(h, t, unit, beds, taken);
            if (bed == null) continue;
            beds.put(t.id(), bed); taken.put(bed, t.id());
        }
    }
    /** The best free bed in {@code h} for one household member. */
    private static BedKey pick(House h, Townsfolk t, Unit unit, Map<String, BedKey> beds, Map<BedKey, String> taken) {
        var options = free(h, taken);
        if (options.isEmpty()) return null;
        House.Bed best = null; long bestCost = Long.MAX_VALUE;
        var partnerKey = t.partner().isEmpty() || !unit.has(t.partner()) ? null : beds.get(t.partner());
        var partnerBed = partnerKey != null && partnerKey.house().equals(h.id()) ? h.bed(partnerKey.head()) : null;
        boolean couple = t.adult() && !t.partner().isEmpty() && unit.has(t.partner());
        // The rooms the grown-ups of this household already sleep in, for children to keep apart from.
        var adultRooms = new HashSet<Integer>();
        for (var m : unit.members()) {
            var key = beds.get(m.id());
            if (m.adult() && key != null && key.house().equals(h.id()) && h.bed(key.head()) != null) adultRooms.add(h.bed(key.head()).room());
        }
        for (int i = 0; i < options.size(); i++) {
            var b = options.get(i); long cost;
            if (couple && partnerBed != null) cost = (b.room() == partnerBed.room() ? 0 : 1000) + (b.beside(partnerBed) ? 0 : 100) + b.head().distManhattan(partnerBed.head());
            else if (couple) cost = besideCost(b, options) * 10L + i;
            else if (!t.adult()) cost = (adultRooms.contains(b.room()) && options.stream().anyMatch(o -> !adultRooms.contains(o.room())) ? 1000 : 0) + i;
            else cost = i;
            if (cost < bestCost) { bestCost = cost; best = b; }
        }
        return new BedKey(h.id(), best.head());
    }
    /** For the first partner: how far this bed is from the best other free bed for the second (0 when one is right beside it in the same room). */
    private static long besideCost(House.Bed b, List<House.Bed> options) {
        long best = 10_000;
        for (var o : options) {
            if (o == b) continue;
            long cost = (o.room() == b.room() ? 0 : 1000) + (o.beside(b) ? 0 : 100) + o.head().distManhattan(b.head());
            best = Math.min(best, cost);
        }
        return best;
    }
    /** The house most of a household sleeps in, or null. */
    private static String homeOf(Unit unit, Map<String, BedKey> beds) {
        var count = new TreeMap<String, Integer>();
        for (var t : unit.members()) { var key = beds.get(t.id()); if (key != null) count.merge(key.house(), 1, Integer::sum); }
        String best = null;
        for (var e : count.entrySet()) if (best == null || e.getValue() > count.get(best)) best = e.getKey();
        return best;
    }
    /** Any free bed for someone the village couldn't house properly: their family's house, the inn, the barracks, then anyone's spare bed. */
    private static BedKey spare(Townsfolk t, String home, List<House> houses, Map<BedKey, String> taken) {
        var order = new ArrayList<House>();
        for (var h : houses) if (h.id().equals(home)) order.add(h);
        for (var use : List.of(House.Use.INN, House.Use.BARRACKS)) for (var h : houses) if (h.use() == use) order.add(h);
        for (var h : houses) if (h.kind() != House.Kind.PLAYER && h.use() != House.Use.INN && h.use() != House.Use.BARRACKS) order.add(h);
        for (var h : houses) if (h.kind() == House.Kind.PLAYER) order.add(h);
        for (var h : order) {
            if (h.privateHome()) continue;
            var options = free(h, taken);
            if (!options.isEmpty()) return new BedKey(h.id(), options.getFirst().head());
        }
        return null;
    }

    private Assignments() {}
}
