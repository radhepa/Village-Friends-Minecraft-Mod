package dev.villagefriends;

/** An immutable relationship, scoped to one villager and one player. */
public record FriendshipState(int points, long talkDay, long giftDay, int giftsToday, String lastGift) {
    public static final int MAX_POINTS = 200;
    public static final int DAILY_GIFTS = 3;
    public static final FriendshipState NEW = new FriendshipState(0, -1, -1, 0, "");

    public FriendshipState {
        points = Math.clamp(points, 0, MAX_POINTS);
        giftsToday = Math.clamp(giftsToday, 0, DAILY_GIFTS);
        lastGift = lastGift == null ? "" : lastGift;
    }

    public int level() {
        if (points >= 140) return 4;
        if (points >= 80) return 3;
        if (points >= 40) return 2;
        if (points >= 15) return 1;
        return 0;
    }

    public String title() {
        return switch (level()) {
            case 1 -> "Acquaintance";
            case 2 -> "Friend";
            case 3 -> "Close Friend";
            case 4 -> "Best Friend";
            default -> "New Neighbor";
        };
    }

    public int nextThreshold() {
        return switch (level()) {
            case 0 -> 15;
            case 1 -> 40;
            case 2 -> 80;
            case 3 -> 140;
            default -> MAX_POINTS;
        };
    }

    public boolean canTalk(long day) { return talkDay != day; }
    public int giftsLeft(long day) { return DAILY_GIFTS - (giftDay == day ? giftsToday : 0); }

    public FriendshipState talk(long day) {
        return canTalk(day) ? new FriendshipState(points + 4, day, giftDay, giftsToday, lastGift) : this;
    }

    public FriendshipState gift(long day, String item, int value) {
        if (value <= 0 || giftsLeft(day) == 0) return this;
        int count = giftDay == day ? giftsToday : 0;
        int varietyBonus = !lastGift.isEmpty() && !lastGift.equals(item) ? 2 : 0;
        return new FriendshipState(points + value + varietyBonus, talkDay, day, count + 1, item);
    }
}
