package dev.villagefriends.home;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;
import java.util.Optional;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.level.levelgen.structure.BoundingBox;

/**
 * One house in a village: its rooms, beds, doors and workstations.
 *
 * <p>{@code id} is stable: {@code g:<template>@<x>,<y>,<z>} for a house a village generated (its structure
 * piece's corner), {@code p:<x>,<y>,<z>} for a house a player built and put a House Plaque in (the plaque),
 * and {@code f:<x>,<y>,<z>} for one found around a bed in a village with no structure (its first bed's head).
 * Beds are sorted by their head position, so a bed's place in the list never depends on scan order.
 * {@code privateHome} is a player house marked Private on its plaque: nobody moves in.
 */
public record House(String id, Kind kind, String template, Use use, BoundingBox box, List<Room> rooms, List<Bed> beds,
        List<BlockPos> doors, List<Workstation> workstations, Optional<BlockPos> plaque, String customName,
        boolean privateHome, boolean verified, long verifiedTick) {
    public enum Kind { GENERATED, PLAYER, FOUND;
        public static final Codec<Kind> CODEC = Codec.STRING.xmap(s -> valueOf(s.toUpperCase(Locale.ROOT)), k -> k.name().toLowerCase(Locale.ROOT));
    }
    /** What the house is for: a family home, a civic building's quarters, the tavern's guest rooms or the garrison's barracks. */
    public enum Use { HOME, QUARTERS, INN, BARRACKS;
        public static final Codec<Use> CODEC = Codec.STRING.xmap(Use::of, u -> u.name().toLowerCase(Locale.ROOT));
        public static Use of(String s) {
            return switch (s == null ? "" : s.toLowerCase(Locale.ROOT)) { case "quarters" -> QUARTERS; case "inn" -> INN; case "barracks" -> BARRACKS; default -> HOME; };
        }
    }
    /** A room: a catalog bedroom in a generated house, "Room 1".."Room n" in a flood-filled one. */
    public record Room(String name, BoundingBox box) {
        public static final Codec<Room> CODEC = RecordCodecBuilder.create(i -> i.group(
                Codec.STRING.fieldOf("name").forGetter(Room::name),
                BoundingBox.CODEC.fieldOf("box").forGetter(Room::box)
        ).apply(i, Room::new));
    }
    /** A bed: vanilla's HOME point of interest sits on its {@code head}. {@code present} is false once it was found missing. */
    public record Bed(BlockPos head, BlockPos foot, Direction facing, int room, boolean present) {
        public static final Codec<Bed> CODEC = RecordCodecBuilder.create(i -> i.group(
                BlockPos.CODEC.fieldOf("head").forGetter(Bed::head),
                BlockPos.CODEC.fieldOf("foot").forGetter(Bed::foot),
                Direction.CODEC.fieldOf("facing").forGetter(Bed::facing),
                Codec.INT.optionalFieldOf("room", 0).forGetter(Bed::room),
                Codec.BOOL.optionalFieldOf("present", true).forGetter(Bed::present)
        ).apply(i, Bed::new));
        public Bed present(boolean now) { return now == present ? this : new Bed(head, foot, facing, room, now); }
        /** Two beds side by side: the same height and facing, at most two blocks apart. */
        public boolean beside(Bed o) { return head.getY() == o.head.getY() && facing == o.facing && head.distManhattan(o.head) <= 2; }
    }
    /** A job site in the house: its point-of-interest type, which for every profession is also the job's id. */
    public record Workstation(BlockPos pos, String poi) {
        public static final Codec<Workstation> CODEC = RecordCodecBuilder.create(i -> i.group(
                BlockPos.CODEC.fieldOf("pos").forGetter(Workstation::pos),
                Codec.STRING.fieldOf("poi").forGetter(Workstation::poi)
        ).apply(i, Workstation::new));
        /** "farmer" for "minecraft:farmer", "apothecary" for "villagefriends:apothecary". */
        public String job() { return poi.substring(poi.indexOf(':') + 1); }
    }

    public static final Codec<House> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.STRING.fieldOf("id").forGetter(House::id),
            Kind.CODEC.fieldOf("kind").forGetter(House::kind),
            Codec.STRING.optionalFieldOf("template", "").forGetter(House::template),
            Use.CODEC.optionalFieldOf("use", Use.HOME).forGetter(House::use),
            BoundingBox.CODEC.fieldOf("box").forGetter(House::box),
            Room.CODEC.listOf().optionalFieldOf("rooms", List.of()).forGetter(House::rooms),
            Bed.CODEC.listOf().optionalFieldOf("beds", List.of()).forGetter(House::beds),
            BlockPos.CODEC.listOf().optionalFieldOf("doors", List.of()).forGetter(House::doors),
            Workstation.CODEC.listOf().optionalFieldOf("workstations", List.of()).forGetter(House::workstations),
            BlockPos.CODEC.optionalFieldOf("plaque").forGetter(House::plaque),
            Codec.STRING.optionalFieldOf("name", "").forGetter(House::customName),
            Codec.BOOL.optionalFieldOf("private", false).forGetter(House::privateHome),
            Codec.BOOL.optionalFieldOf("verified", false).forGetter(House::verified),
            Codec.LONG.optionalFieldOf("verified_tick", 0L).forGetter(House::verifiedTick)
    ).apply(i, House::new));

    public House {
        template = template == null ? "" : template;
        customName = customName == null ? "" : customName;
        rooms = List.copyOf(rooms);
        var sorted = new ArrayList<>(beds); sorted.sort(Comparator.comparing(Bed::head));
        beds = List.copyOf(sorted);
        doors = List.copyOf(doors);
        workstations = List.copyOf(workstations);
    }

    /** The bed whose head is at {@code head}, or null. */
    public Bed bed(BlockPos head) {
        for (var b : beds) if (b.head().equals(head)) return b;
        return null;
    }
    /** The bed with a head or foot at {@code pos}, or null. */
    public Bed bedAt(BlockPos pos) {
        for (var b : beds) if (b.head().equals(pos) || b.foot().equals(pos)) return b;
        return null;
    }
    public List<Bed> presentBeds() { return beds.stream().filter(Bed::present).toList(); }
    /** The room a position is in (walls included), or -1. */
    public int roomAt(BlockPos pos) {
        for (int r = 0; r < rooms.size(); r++) if (rooms.get(r).box().inflatedBy(1).isInside(pos)) return r;
        return -1;
    }
    /** The jobs whose workstations are in this house. */
    public List<String> jobs() { return workstations.stream().map(Workstation::job).distinct().sorted().toList(); }
    public boolean player() { return kind == Kind.PLAYER; }

    public House withBeds(List<Bed> next) { return new House(id, kind, template, use, box, rooms, next, doors, workstations, plaque, customName, privateHome, verified, verifiedTick); }
    public House verified(List<Bed> nextBeds, List<Workstation> nextStations, long tick) {
        return new House(id, kind, template, use, box, rooms, nextBeds, doors, nextStations, plaque, customName, privateHome, true, tick);
    }
    public House named(String name) { return new House(id, kind, template, use, box, rooms, beds, doors, workstations, plaque, name, privateHome, verified, verifiedTick); }
    public House withPlaque(BlockPos pos) { return new House(id, kind, template, use, box, rooms, beds, doors, workstations, Optional.ofNullable(pos), customName, privateHome, verified, verifiedTick); }
    public House privateHome(boolean closed) { return new House(id, kind, template, use, box, rooms, beds, doors, workstations, plaque, customName, closed, verified, verifiedTick); }
}
