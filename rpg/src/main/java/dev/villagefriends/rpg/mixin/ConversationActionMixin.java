package dev.villagefriends.rpg.mixin;

import dev.villagefriends.ActionPayload;
import dev.villagefriends.VillageFriends;
import dev.villagefriends.rpg.Quests;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.npc.villager.Villager;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Routes the RPG's conversation choices (ids starting with "rpg_") to {@link Quests}. */
@Mixin(VillageFriends.class)
public abstract class ConversationActionMixin {
    @Inject(method = "handleAction", at = @At("HEAD"), cancellable = true)
    private static void villagefriendsRpg$action(ServerPlayer player, ActionPayload action, CallbackInfo ci) {
        if (!action.action().startsWith("rpg_")) return;
        ci.cancel();
        if (player.level().getEntity(action.entityId()) instanceof Villager v && v.getUUID().equals(action.villagerId())
                && VillageFriends.validTarget(player, v) && !v.isSleeping()) Quests.handle(player, v, action.action());
    }
}
