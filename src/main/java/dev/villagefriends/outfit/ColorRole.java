package dev.villagefriends.outfit;

/** Textile coverage targets exclude hardware, whose area is additional. */
public enum ColorRole {
    ROLE_PRIMARY(60), ROLE_SECONDARY(30), ROLE_ACCENT(10), ROLE_HARDWARE(0);

    private final int textilePercent;
    ColorRole(int textilePercent) { this.textilePercent = textilePercent; }
    public int textilePercent() { return textilePercent; }
}
