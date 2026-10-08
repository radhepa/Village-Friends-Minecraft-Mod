package dev.villagefriends.home;

import java.util.List;
import java.util.Optional;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;

/**
 * Which resident house a block belongs to. Deeds asks this to tell theft from a resident's chest or a
 * broken bed, door or workstation apart from ordinary block breaking; Homes installs the real answer
 * from its housing index. Until then (and in tests) every block belongs to no house.
 */
public interface HouseBounds {
    /** A house: its village, its id within the village, its display name and the residents (UUIDs) living there. */
    record HouseRef(String village, String house, String name, List<String> residents) {}

    /** The house whose rooms contain {@code pos}, from loaded index data only; never loads chunks. */
    Optional<HouseRef> houseAt(ServerLevel level, BlockPos pos);

    /** The residents (UUIDs) who own the bed, door or workstation at {@code pos}, or an empty list. */
    List<String> owners(ServerLevel level, BlockPos pos);

    HouseBounds NONE = new HouseBounds() {
        @Override public Optional<HouseRef> houseAt(ServerLevel level, BlockPos pos) { return Optional.empty(); }
        @Override public List<String> owners(ServerLevel level, BlockPos pos) { return List.of(); }
    };

    static HouseBounds current() { return Holder.current; }

    static void install(HouseBounds bounds) { Holder.current = bounds == null ? NONE : bounds; }

    final class Holder {
        static volatile HouseBounds current = NONE;
        private Holder() {}
    }
}
