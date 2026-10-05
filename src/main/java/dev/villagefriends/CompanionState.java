package dev.villagefriends;
import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
public record CompanionState(String owner, String mode, double x, double y, double z,
        long until, boolean originalNoAi, long started) {
    public static final CompanionState NONE = new CompanionState("", "home", 0, 0, 0, 0, false, 0);
    public static final Codec<CompanionState> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.STRING.optionalFieldOf("owner", "").forGetter(CompanionState::owner),
            Codec.STRING.optionalFieldOf("mode", "home").forGetter(CompanionState::mode),
            Codec.DOUBLE.optionalFieldOf("home_x", 0D).forGetter(CompanionState::x),
            Codec.DOUBLE.optionalFieldOf("home_y", 0D).forGetter(CompanionState::y),
            Codec.DOUBLE.optionalFieldOf("home_z", 0D).forGetter(CompanionState::z),
            Codec.LONG.optionalFieldOf("until", 0L).forGetter(CompanionState::until),
            Codec.BOOL.optionalFieldOf("original_no_ai", false).forGetter(CompanionState::originalNoAi),
            Codec.LONG.optionalFieldOf("started", 0L).forGetter(CompanionState::started)
    ).apply(i, CompanionState::new));
    public boolean active() { return !owner.isEmpty(); }
    public boolean downed() { return mode.equals("downed"); }
    public CompanionState mode(String next) { return new CompanionState(owner, next, x, y, z, until, originalNoAi, started); }
    public CompanionState downed(long time) { return new CompanionState(owner, "downed", x, y, z, time, originalNoAi, started); }
}
