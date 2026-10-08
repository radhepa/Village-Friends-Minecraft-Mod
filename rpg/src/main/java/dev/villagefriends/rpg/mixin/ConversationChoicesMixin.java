package dev.villagefriends.rpg.mixin;

import dev.villagefriends.FriendshipPayload;
import dev.villagefriends.NarrativeEngine;
import dev.villagefriends.rpg.Quests;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.npc.villager.Villager;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

import java.util.ArrayList;
import java.util.List;

/** Adds "Any work for me?" to a resident's talk tab and supplies the choices of the RPG's own "rpg" tab. */
@Mixin(NarrativeEngine.class)
public abstract class ConversationChoicesMixin {
    @Inject(method = "choices", at = @At("HEAD"), cancellable = true)
    private static void villagefriendsRpg$tab(Villager v, ServerPlayer p, String tab, CallbackInfoReturnable<List<FriendshipPayload.Choice>> cir) {
        if (tab.equals("rpg")) cir.setReturnValue(Quests.choices(v, p));
    }
    @Inject(method = "choices", at = @At("RETURN"), cancellable = true)
    private static void villagefriendsRpg$work(Villager v, ServerPlayer p, String tab, CallbackInfoReturnable<List<FriendshipPayload.Choice>> cir) {
        if (!tab.equals("talk") || cir.getReturnValue().size() >= FriendshipPayload.MAX_CHOICES) return;
        var choice = Quests.talkChoice(v, p);
        if (choice == null) return;
        var all = new ArrayList<>(cir.getReturnValue()); all.add(choice);
        cir.setReturnValue(List.copyOf(all));
    }
}
