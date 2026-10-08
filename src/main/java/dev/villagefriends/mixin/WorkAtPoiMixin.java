package dev.villagefriends.mixin;

import dev.villagefriends.Workstations;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.ai.behavior.WorkAtPoi;
import net.minecraft.world.entity.npc.villager.Villager;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Each time a resident works at their workstation, the station does its job. */
@Mixin(WorkAtPoi.class)
public abstract class WorkAtPoiMixin {
    @Inject(method = "start(Lnet/minecraft/server/level/ServerLevel;Lnet/minecraft/world/entity/npc/villager/Villager;J)V", at = @At("TAIL"))
    private void villagefriends$work(ServerLevel level, Villager body, long timestamp, CallbackInfo ci) {
        Workstations.worked(level, body);
    }
}
