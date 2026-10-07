package dev.villagefriends;

/**
 * The little speech bubbles residents pop above their heads, Tomodachi Life style. Shared by the
 * server, which decides when residents emote at each other or at a player, and the client, which
 * draws and animates them.
 */
public enum Emote {
    EXCLAIM, QUESTION, HEART, NOTE, ANGER, SWEAT, DOTS, SLEEP, SPARKLE, IDEA, GLOOM, BLUSH;

    public static Emote parse(String name) {
        if (name == null || name.isEmpty()) return null;
        try { return valueOf(name); } catch (IllegalArgumentException ignored) { return null; }
    }
}
