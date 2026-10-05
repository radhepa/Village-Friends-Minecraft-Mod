package dev.villagefriends;

import java.time.Duration;
import net.minecraft.world.item.Item;

/** Declares the future treatment contract without altering the existing companion rescue system. */
public final class MedicalSupplyItem extends Item {
    public enum Treatment {
        SMELLING_SALTS(0.20F, Duration.ZERO), REVIVAL_TONIC(1.0F, Duration.ZERO), BANDAGE_WRAP(0.0F, Duration.ofHours(12));
        private final float restoredHealthFraction;
        private final Duration extraTime;
        Treatment(float restoredHealthFraction, Duration extraTime) { this.restoredHealthFraction = restoredHealthFraction; this.extraTime = extraTime; }
        public float restoredHealthFraction() { return restoredHealthFraction; }
        public Duration extraTime() { return extraTime; }
    }
    private final Treatment treatment;
    public MedicalSupplyItem(Properties properties, Treatment treatment) { super(properties); this.treatment = treatment; }
    public Treatment treatment() { return treatment; }
}
