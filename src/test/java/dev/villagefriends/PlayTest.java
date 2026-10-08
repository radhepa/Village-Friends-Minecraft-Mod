package dev.villagefriends;

import static org.junit.jupiter.api.Assertions.*;

import dev.villagefriends.animation.AnimationLibrary;
import dev.villagefriends.play.Games;
import dev.villagefriends.play.Games.Game;
import dev.villagefriends.play.Games.Move;
import java.util.EnumMap;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;
import org.junit.jupiter.api.Test;

class PlayTest {
    private static final List<String> PERSONALITIES = List.of("warmhearted", "thoughtful", "playful", "adventurous", "meticulous", "steadfast",
            "reserved", "imaginative", "pragmatic", "curious", "protective", "gentle");
    private static final AnimationLibrary PACK = AnimationLibrary.builtin();

    @Test void groupsPickAGameThatSuitsHowManyTheyAre() {
        var random = new Random(3);
        for (int players = 2; players <= 6; players++) {
            var seen = new EnumMap<Game, Integer>(Game.class);
            for (int i = 0; i < 2000; i++) {
                var group = new java.util.ArrayList<String>();
                for (int k = 0; k < players; k++) group.add(PERSONALITIES.get(random.nextInt(PERSONALITIES.size())));
                var game = Games.choose(players, group, null, random);
                assertNotNull(game, players + " children find a game");
                assertTrue(players >= game.min, game + " needs " + game.min);
                if (game == Game.CATCH) assertTrue(players <= 3, "catch is for two or three");
                seen.merge(game, 1, Integer::sum);
            }
            if (players == 2) assertEquals(Set.of(Game.TAG, Game.HIDE_AND_SEEK, Game.CATCH), seen.keySet(), "two children: tag, hide-and-seek or catch");
            if (players >= 4) assertFalse(seen.containsKey(Game.CATCH), "four or more don't play catch");
            if (players >= 3) assertTrue(seen.keySet().containsAll(List.of(Game.TAG, Game.HIDE_AND_SEEK, Game.RING, Game.FOLLOW_THE_LEADER)), "every big game comes up: " + seen);
        }
        assertNull(Games.choose(1, List.of("playful"), null, random), "nobody plays a game alone");
    }

    @Test void theLastGameRarelyComesStraightBack() {
        var random = new Random(9);
        int again = 0, runs = 4000;
        for (int i = 0; i < runs; i++) if (Games.choose(4, List.of("playful", "playful", "adventurous", "playful"), Game.TAG, random) == Game.TAG) again++;
        assertTrue(again < runs / 8, "tag again straight after tag: " + again);
    }

    @Test void favoritesShowThroughPersonality() {
        var random = new Random(11);
        int tagForPlayful = 0, tagForReserved = 0;
        for (int i = 0; i < 4000; i++) {
            if (Games.choose(3, List.of("playful", "playful", "adventurous"), null, random) == Game.TAG) tagForPlayful++;
            if (Games.choose(3, List.of("reserved", "meticulous", "thoughtful"), null, random) == Game.TAG) tagForReserved++;
        }
        assertTrue(tagForPlayful > tagForReserved * 1.5, "lively children choose tag more: " + tagForPlayful + " vs " + tagForReserved);
    }

    @Test void boredomAndCuriosityFollowPersonality() {
        assertTrue(Games.boredAfter("playful") < Games.boredAfter("reserved"), "lively children get bored first");
        for (var p : PERSONALITIES) {
            int with = Games.curiosity(p, true), alone = Games.curiosity(p, false);
            assertTrue(with > 0 && with < 100 && alone > with, p + " is sometimes curious, more so with nobody to play with");
            assertTrue(Games.boredAfter(p) >= 10 && Games.boredAfter(p) <= 90, p + " plays alone a sensible while");
        }
        assertTrue(Games.curiosity("curious", true) > Games.curiosity("reserved", true), "curious children follow players the most");
        var random = new Random(1);
        for (int i = 0; i < 500; i++) {
            int follow = Games.curiousFor(random), rest = Games.restAfter(random);
            assertTrue(follow >= 800 && follow < 2400, "tags along for under two minutes");
            assertTrue(rest >= 500 && rest < 1400, "a breather between games");
        }
    }

    @Test void statesReadBack() {
        assertEquals("catch:throw:42:miss", Games.state(Game.CATCH, "throw:42:miss"));
        assertEquals("catch", Games.game("catch:throw:42:miss"));
        assertEquals("throw", Games.role("catch:throw:42:miss"));
        assertEquals("42:miss", Games.detail("catch:throw:42:miss"));
        assertEquals("curious:watch", Games.curious("watch"));
        assertEquals("Following you around", Games.doing("curious:watch"));
        assertEquals("Hiding", Games.doing("hide_and_seek:hidden"));
        assertEquals("Playing ring-around-the-rosie", Games.doing("ring:walk"));
        assertNull(Games.doing(null));
        assertNull(Games.role("tag"));
        for (var g : Game.values()) assertEquals(g, Game.byId(g.id()));
    }

    /** Every part a child can play in a game has animation, the way the client tags it. */
    @Test void everyPartOfEveryGameHasClips() {
        var random = new Random(2);
        var standing = List.of("tag:count", "tag:tagged", "tag:it", "tag:run", "hide_and_seek:count", "hide_and_seek:hidden", "hide_and_seek:seek",
                "hide_and_seek:point", "hide_and_seek:found", "hide_and_seek:home", "hide_and_seek:won", "ring:join", "ring:fall",
                "follow_the_leader:lead", "follow_the_leader:follow", "catch:ready", "catch:hold", "catch:throw:7", "catch:throw:7:miss", "catch:catch",
                "catch:fumble", "curious:watch", "curious:caught", "curious:bye");
        var moving = List.of("tag:it", "tag:run", "hide_and_seek:hide", "hide_and_seek:seek", "ring:walk", "ring:join", "follow_the_leader:lead",
                "follow_the_leader:follow", "curious:follow");
        for (var state : standing) assertNotNull(PACK.pick("play", tags(state, false), random), "a clip for " + state);
        for (var state : moving) assertNotNull(PACK.pick("play", tags(state, true), random), "a clip for " + state + " on the move");
        for (var move : Move.values()) {
            var clip = PACK.pick("play", tags("follow_the_leader:do:" + move.id, false), random);
            assertNotNull(clip, "the leader's " + move.id);
            // Everyone in the line copies the same move, and the line waits exactly as long as it lasts.
            assertEquals(move.ticks / 20F, clip.length(), .001, move.id + " lasts as long as Games.Move says");
            for (int i = 0; i < 20; i++) assertEquals(clip.id(), PACK.pick("play", tags("follow_the_leader:do:" + move.id, false), random).id(), "only one clip per move");
        }
        // Adults never play.
        assertNull(PACK.pick("play", Set.of("adult", "play:tag", "play:tag:run"), random), "grown-ups don't play tag");
    }
    private static Set<String> tags(String state, boolean moving) {
        var tags = new HashSet<String>(Set.of("child", "day", "personality:playful", "routine:play"));
        String game = Games.game(state), role = Games.role(state);
        tags.add("play:" + game);
        if (role != null) tags.add("play:" + game + ":" + role);
        if ("do".equals(role)) tags.add("play:" + state);
        if (moving) tags.add("moving");
        return tags;
    }
}
