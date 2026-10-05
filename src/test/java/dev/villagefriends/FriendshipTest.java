package dev.villagefriends;

import static org.junit.jupiter.api.Assertions.*;
import com.google.gson.JsonParser;
import com.mojang.serialization.JsonOps;
import java.util.UUID;
import org.junit.jupiter.api.Test;

class FriendshipTest {
    @Test void conversationsRewardOncePerDayAndResetTomorrow() {
        FriendshipState state = FriendshipState.NEW.talk(0);
        assertEquals(4, state.points());
        assertSame(state, state.talk(0));
        assertEquals(8, state.talk(1).points());
    }
    @Test void giftsHaveDailyLimitsAndVarietyBonus() {
        FriendshipState state = FriendshipState.NEW.gift(3, "minecraft:emerald", 12)
                .gift(3, "minecraft:poppy", 8).gift(3, "minecraft:poppy", 8);
        assertEquals(30, state.points());
        assertEquals(0, state.giftsLeft(3));
        assertSame(state, state.gift(3, "minecraft:emerald", 12));
        assertEquals(3, state.giftsLeft(4));
        assertEquals(44, state.gift(4, "minecraft:emerald", 12).points());
    }
    @Test void rejectedGiftsDoNotSpendTheDailyAllowance() {
        assertSame(FriendshipState.NEW, FriendshipState.NEW.gift(0, "minecraft:rotten_flesh", 0));
        assertEquals(3, FriendshipState.NEW.giftsLeft(0));
    }
    @Test void thresholdsAndMaximumPointsAreCorrect() {
        int[] boundaries = {0, 14, 15, 39, 40, 79, 80, 139, 140, 200};
        int[] levels = {0, 0, 1, 1, 2, 2, 3, 3, 4, 4};
        for (int i = 0; i < boundaries.length; i++)
            assertEquals(levels[i], new FriendshipState(boundaries[i], -1, -1, 0, "").level());
        assertEquals(200, new FriendshipState(199, -1, -1, 0, "").gift(0, "minecraft:emerald", 12).points());
        assertEquals(0, new FriendshipState(-200, -1, -1, 0, "").points());
    }
    @Test void professionAndBabyPreferencesWork() {
        assertEquals(10, GiftPreferences.value("farmer", false, "minecraft:carrot"));
        assertEquals(0, GiftPreferences.value("librarian", false, "minecraft:carrot"));
        assertEquals(12, GiftPreferences.value("none", true, "minecraft:cookie"));
        assertEquals(8, GiftPreferences.value("librarian", false, "minecraft:poppy"));
        assertEquals(0, GiftPreferences.value("farmer", false, "anothermod:emerald"));
    }
    @Test void savedFriendshipsRoundTripAndKeepPlayersIndependent() {
        UUID first = UUID.fromString("00000000-0000-0000-0000-000000000001");
        UUID second = UUID.fromString("00000000-0000-0000-0000-000000000002");
        FriendshipBook book = FriendshipBook.empty().with(first, FriendshipState.NEW.talk(1).gift(1, "minecraft:emerald", 12));
        var json = FriendshipBook.CODEC.encodeStart(JsonOps.INSTANCE, book).getOrThrow();
        FriendshipBook restored = FriendshipBook.CODEC.parse(JsonOps.INSTANCE, JsonParser.parseString(json.toString())).getOrThrow();
        assertEquals(book, restored);
        assertEquals(16, restored.get(first).points());
        assertEquals(0, restored.get(second).points());
        assertEquals(2, restored.get(first).giftsLeft(1));
        assertFalse(restored.get(first).canTalk(1));
    }
    @Test void namesAndPersonalitiesRemainStable() {
        UUID uuid = UUID.fromString("aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee");
        assertEquals(Dialogue.name(uuid), Dialogue.name(uuid));
        assertFalse(Dialogue.personality(uuid).isBlank());
        assertNotEquals(Dialogue.conversation(uuid, "work", "farmer", false, 0, 0),
                Dialogue.conversation(uuid, "work", "librarian", false, 0, 0));
    }

    @Test void appearanceIdentifiersAreStable() {
        UUID id=UUID.fromString("aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee");
        assertEquals(ResidentAppearance.generate(id), ResidentAppearance.generate(id));
        assertNotNull(dev.villagefriends.outfit.ResidentLook.parse(ResidentAppearance.generate(id)));
    }
}

