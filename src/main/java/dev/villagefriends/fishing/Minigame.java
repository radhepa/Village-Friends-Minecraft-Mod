package dev.villagefriends.fishing;

import java.util.Random;

/**
 * The catch-bar minigame, as a pure simulation. A vertical track of water holds the fish, which darts, glides,
 * sinks or floats by its {@link Fish.Behavior} and difficulty; the player's catch zone rises while they hold
 * the use button and falls when they let go, bouncing off the bottom. While the fish is inside the zone the
 * catch meter fills, otherwise it drains: full is a catch, empty is a fish that got away. Sometimes a treasure
 * chest shows up in the water too; keep it in the zone long enough and it's yours (and while you're holding it
 * the catch meter doesn't drain).
 *
 * <p>It runs at 20 ticks a second, three steps a tick, in "track pixels": the track is {@link #TRACK} tall, 0 at
 * the top. The client runs it while the fish is on and renders {@link #barPos()} and {@link #fishPos()} scaled
 * to the screen; the same seed always plays out the same way for the same input.
 */
public final class Minigame {
    public static final float TRACK = 568, FISH = 36, BASE_ZONE = 104, MAX_TICKS = 20 * 90;
    private static final int STEPS = 3;

    /** What the gear, the fish and the angler's skill set up: zone height (track pixels) and multipliers. */
    public record Tuning(float zone, float fishSpeed, float gain, float drain, boolean treasure) {
        public Tuning {
            zone = Math.clamp(zone, 48, TRACK * .6F);
            fishSpeed = Math.clamp(fishSpeed, .3F, 2);
            gain = Math.clamp(gain, .3F, 3);
            drain = Math.clamp(drain, .1F, 3);
        }
        public static Tuning of(Gear.Rod rod, Gear.Tackle tackle, boolean treasure) {
            float zone = BASE_ZONE + (float) rod.zone * TRACK + (tackle == Gear.Tackle.CORK_BOBBER ? 32 : 0);
            return new Tuning(zone, tackle == Gear.Tackle.LEAD_SINKER ? .75F : 1, 1 + (float) rod.reel, tackle == Gear.Tackle.BARBED_HOOK ? .6F : 1, treasure);
        }
        public Tuning widen(float px) { return new Tuning(zone + px, fishSpeed, gain, drain, treasure); }
        public Tuning reel(float more) { return new Tuning(zone, fishSpeed, gain * (1 + more), drain, treasure); }
    }

    private final Random random;
    private final Fish.Behavior behavior;
    private final float difficulty;
    private final Tuning tuning;

    private float barPos, barSpeed, prevBar;
    private float fishPos, fishSpeed, fishTarget = -1, sinkFloat, prevFish;
    private float progress = .3F, prevProgress = .3F;
    private boolean perfect = true, done, won;
    private int ticks;
    // Treasure: appears after a while at a random height and must be held in the zone to collect.
    private final boolean treasure;
    private int treasureAt;
    private float treasurePos, treasureProgress;
    private boolean treasureShown, treasureCaught;

    public Minigame(long seed, Fish.Behavior behavior, int difficulty, Tuning tuning) {
        this.random = new Random(seed);
        this.behavior = behavior;
        this.difficulty = Math.clamp(difficulty, 1, 110);
        this.tuning = tuning;
        this.barPos = (TRACK - tuning.zone()) / 2;
        this.fishPos = (TRACK - FISH) / 2;
        this.prevBar = barPos; this.prevFish = fishPos;
        this.treasure = tuning.treasure();
        this.treasureAt = 20 + random.nextInt(40);
        this.treasurePos = 40 + random.nextFloat() * (TRACK - 120);
    }

    /** One game tick: {@code holding} is whether the use button is down. */
    public void tick(boolean holding) {
        if (done) return;
        prevBar = barPos; prevFish = fishPos; prevProgress = progress;
        for (int i = 0; i < STEPS && !done; i++) step(holding);
        ticks++;
        if (!done && ticks >= MAX_TICKS) { done = true; won = false; }
    }

    private void step(boolean holding) {
        moveFish();
        // The zone: holding lifts it, letting go drops it; it bounces off the bottom and stops at the top.
        barSpeed += holding ? -.25F : .25F;
        barPos += barSpeed;
        float bottom = TRACK - tuning.zone();
        if (barPos > bottom) { barPos = bottom; barSpeed = -barSpeed * 2 / 3F; if (Math.abs(barSpeed) < .5F) barSpeed = 0; }
        if (barPos < 0) { barPos = 0; barSpeed = 0; }

        boolean inZone = inZone(fishPos + FISH / 2);
        boolean holdingTreasure = false;
        if (treasure && !treasureCaught) {
            if (!treasureShown && ticks >= treasureAt) treasureShown = true;
            if (treasureShown) {
                holdingTreasure = inZone(treasurePos);
                treasureProgress = Math.max(0, treasureProgress + (holdingTreasure ? .0135F : -.01F));
                if (treasureProgress >= 1) { treasureCaught = true; treasureProgress = 1; }
            }
        }
        if (inZone) progress += .002F * tuning.gain();
        else if (!holdingTreasure) { progress -= .003F * tuning.drain(); perfect = false; }
        else perfect = false;
        if (progress >= 1) { progress = 1; done = true; won = true; }
        else if (progress <= 0) { progress = 0; done = true; won = false; }
    }

    /** Stardew-style fish motion: new targets at random, eased towards; darters dash, sinkers and floaters drift. */
    private void moveFish() {
        boolean smooth = behavior == Fish.Behavior.SMOOTH, dart = behavior == Fish.Behavior.DART;
        float range = TRACK - 20;
        if (random.nextFloat() < difficulty * (smooth ? 20 : 1) / 4000F && (!smooth || fishTarget == -1)) {
            float below = range - fishPos, above = fishPos;
            float percent = Math.min(99, difficulty + 10 + random.nextInt(35)) / 100F;
            fishTarget = fishPos + (-above + random.nextFloat() * (above + below)) * percent;
        }
        if (behavior == Fish.Behavior.FLOATER) sinkFloat = Math.max(sinkFloat - .01F, -1.5F);
        else if (behavior == Fish.Behavior.SINKER) sinkFloat = Math.min(sinkFloat + .01F, 1.5F);
        if (fishTarget != -1 && Math.abs(fishPos - fishTarget) > 3) {
            float accel = (fishTarget - fishPos) / (10 + random.nextInt(20) + (100 - Math.min(100, difficulty)));
            fishSpeed += (accel - fishSpeed) / 5;
        } else if (!smooth && random.nextFloat() < difficulty / 2000F) {
            fishTarget = fishPos + (random.nextBoolean() ? -(51 + random.nextInt(50)) : 50 + random.nextInt(51));
        } else fishTarget = -1;
        if (dart && random.nextFloat() < difficulty / 1000F)
            fishTarget = fishPos + (random.nextBoolean() ? -(51 + random.nextInt(50 + (int) difficulty * 2)) : 50 + random.nextInt(51 + (int) difficulty * 2));
        fishTarget = Math.clamp(fishTarget, -1, range);
        fishPos += (fishSpeed + sinkFloat) * tuning.fishSpeed();
        fishPos = Math.clamp(fishPos, 0, TRACK - FISH);
    }

    private boolean inZone(float y) { return y >= barPos && y <= barPos + tuning.zone(); }

    public float barPos() { return barPos; }
    /** How fast the zone is moving (track pixels a step, down is positive). */
    public float barSpeed() { return barSpeed; }
    public float fishPos() { return fishPos; }
    public float barPos(float partial) { return prevBar + (barPos - prevBar) * partial; }
    public float fishPos(float partial) { return prevFish + (fishPos - prevFish) * partial; }
    public float progress() { return progress; }
    public float progress(float partial) { return prevProgress + (progress - prevProgress) * partial; }
    public float zone() { return tuning.zone(); }
    public boolean fishInZone() { return inZone(fishPos + FISH / 2); }
    public boolean perfect() { return perfect; }
    public boolean done() { return done; }
    public boolean won() { return won; }
    public int ticks() { return ticks; }
    public boolean treasureShown() { return treasure && treasureShown && !treasureCaught; }
    public boolean treasureCaught() { return treasureCaught; }
    public float treasurePos() { return treasurePos; }
    public float treasureProgress() { return treasureProgress; }
    /** The quickest a fish could possibly be landed (the meter filling non-stop from the start), in ticks. */
    public static int quickest(Tuning tuning) { return (int) Math.floor(.7F / (.002F * tuning.gain() * STEPS)); }
}
