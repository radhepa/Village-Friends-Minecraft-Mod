package dev.villagefriends;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;
import java.util.UUID;

/** Combat rules kept independent of Minecraft for focused policy checks. */
public final class GuardPolicy {
    public static final int SCAN_INTERVAL = 10;
    public static final int SCAN_RADIUS = 16;
    public static final int PURSUIT_RADIUS = 32;
    public static final int ANGER_TICKS = 1200;
    public static final int RECENT_ATTACK_TICKS = 600;

    public static boolean threat(boolean creeper, boolean predator, boolean targetingVillager, boolean recentAttack) {
        return !creeper && (predator || targetingVillager || recentAttack);
    }
    public static boolean forgives(BondState bond, FriendshipState friendship) {
        return bond.level(friendship) >= 2;
    }
    public static boolean angerActive(long now, long deadline) { return now < deadline; }

    /** Slot indexes are head, chest, legs, feet; exactly two are iron. */
    public static List<Integer> ironSlots(UUID id) {
        var slots = new ArrayList<>(List.of(0, 1, 2, 3));
        Collections.shuffle(slots, new Random(id.getMostSignificantBits() ^ id.getLeastSignificantBits()));
        return List.copyOf(slots.subList(0, 2));
    }
    private GuardPolicy() {}
}
