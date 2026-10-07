package dev.villagefriends;

import java.util.List;

/**
 * The tunes a music stand plays: a few old folk songs everyone knows and some village originals.
 * Notes use note-block steps (0 is F#3, 12 is F#4, 24 is F#5); each note is {step, ticks until the next}.
 */
public final class Songbook {
    public record Song(String title, int[][] notes) {}
    private static final int Q = 6, E = 3, H = 12, DQ = 9;

    public static final List<Song> SONGS = List.of(
            new Song("Ode to Joy", new int[][]{{12, Q}, {12, Q}, {13, Q}, {15, Q}, {15, Q}, {13, Q}, {12, Q}, {10, Q}, {8, Q}, {8, Q}, {10, Q}, {12, Q}, {12, DQ}, {10, E}, {10, H}}),
            new Song("Twinkle, Twinkle", new int[][]{{8, Q}, {8, Q}, {15, Q}, {15, Q}, {17, Q}, {17, Q}, {15, H}, {13, Q}, {13, Q}, {12, Q}, {12, Q}, {10, Q}, {10, Q}, {8, H}}),
            new Song("Frère Jacques", new int[][]{{8, Q}, {10, Q}, {12, Q}, {8, Q}, {8, Q}, {10, Q}, {12, Q}, {8, Q}, {12, Q}, {13, Q}, {15, H}, {12, Q}, {13, Q}, {15, H}}),
            new Song("Greensleeves", new int[][]{{15, Q}, {18, H}, {20, Q}, {22, DQ}, {23, E}, {22, Q}, {20, H}, {17, Q}, {13, DQ}, {15, E}, {17, Q}, {18, H}, {15, Q}, {15, DQ}, {14, E}, {15, Q}, {17, H}, {14, Q}, {10, H}}),
            new Song("The Bell Square Jig", new int[][]{{8, E}, {12, E}, {15, E}, {12, E}, {8, E}, {12, E}, {15, E}, {20, E}, {18, E}, {15, E}, {12, E}, {15, E}, {13, E}, {10, E}, {8, Q}, {15, E}, {20, E}, {15, E}, {12, E}, {8, Q}}),
            new Song("Harvest Home", new int[][]{{13, Q}, {17, Q}, {20, Q}, {17, Q}, {13, Q}, {15, Q}, {17, H}, {15, Q}, {13, Q}, {10, Q}, {8, Q}, {10, Q}, {13, H}}),
            new Song("Lantern Waltz", new int[][]{{15, Q}, {18, Q}, {22, Q}, {20, H}, {18, Q}, {15, H}, {13, Q}, {15, Q}, {18, Q}, {17, H}, {15, Q}, {13, Q}, {12, Q}, {13, Q}, {15, H}}),
            new Song("Shepherd's Evening", new int[][]{{10, H}, {13, Q}, {15, Q}, {17, H}, {15, Q}, {13, Q}, {10, H}, {8, Q}, {10, Q}, {13, Q}, {12, Q}, {10, H}, {8, H}}),
            new Song("The Cobbler's Reel", new int[][]{{17, E}, {15, E}, {13, E}, {15, E}, {17, E}, {20, E}, {22, Q}, {20, E}, {17, E}, {15, E}, {13, E}, {12, E}, {13, E}, {15, Q}, {17, E}, {15, E}, {13, Q}}),
            new Song("Golem's Lullaby", new int[][]{{12, H}, {10, Q}, {8, H}, {10, Q}, {12, Q}, {13, Q}, {15, H}, {13, Q}, {12, Q}, {10, Q}, {8, H}, {8, H}})
    );
    /** Note-block pitch for a step. */
    public static float pitch(int step) { return (float) Math.pow(2, (step - 12) / 12.0); }
    private Songbook() {}
}
