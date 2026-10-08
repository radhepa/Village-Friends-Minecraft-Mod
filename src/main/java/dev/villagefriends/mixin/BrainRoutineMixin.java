package dev.villagefriends.mixin;

import dev.villagefriends.routine.RoutineBrain;
import net.minecraft.world.attribute.EnvironmentAttributeSystem;
import net.minecraft.world.entity.ai.Brain;
import net.minecraft.world.entity.schedule.Activity;
import net.minecraft.world.phys.Vec3;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Residents follow their own routine instead of vanilla's one-size schedule; panic, raids and the bell still come first (except for guards on duty). */
@Mixin(Brain.class)
public abstract class BrainRoutineMixin implements RoutineBrain {
    @Shadow private long lastScheduleUpdate;
    @Shadow public abstract boolean isActive(Activity activity);
    @Shadow public abstract void setActiveActivityIfPossible(Activity activity);
    @Unique private Activity villagefriends$activity;
    @Unique private boolean villagefriends$maySleep = true;
    @Unique private boolean villagefriends$duty;

    @Override public void villagefriends$routine(Activity activity, boolean maySleep) { villagefriends$activity = activity; villagefriends$maySleep = maySleep; }
    @Override public Activity villagefriends$routine() { return villagefriends$activity; }
    @Override public boolean villagefriends$maySleep() { return villagefriends$maySleep; }
    @Override public void villagefriends$duty(boolean duty) { villagefriends$duty = duty; }
    @Override public boolean villagefriends$duty() { return villagefriends$duty; }

    /** Guards on duty stand their ground: no panicking, hiding from the raid or running home at the bell. */
    @Inject(method = {"setActiveActivityIfPossible", "setDefaultActivity"}, at = @At("HEAD"), cancellable = true)
    private void villagefriends$standGround(Activity activity, CallbackInfo ci) {
        if (villagefriends$duty && (activity == Activity.PANIC || activity == Activity.RAID || activity == Activity.PRE_RAID || activity == Activity.HIDE)) ci.cancel();
    }

    @Inject(method = "updateActivityFromSchedule", at = @At("HEAD"), cancellable = true)
    private void villagefriends$followRoutine(EnvironmentAttributeSystem attributes, long gameTime, Vec3 pos, CallbackInfo ci) {
        var routine = villagefriends$activity;
        if (routine == null) return;
        ci.cancel();
        if (gameTime - lastScheduleUpdate > 20L) {
            lastScheduleUpdate = gameTime;
            if (!isActive(routine)) setActiveActivityIfPossible(routine);
        }
    }
}
