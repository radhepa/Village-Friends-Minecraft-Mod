package dev.villagefriends.mixin;

import com.llamalad7.mixinextras.injector.wrapoperation.Operation;
import com.llamalad7.mixinextras.injector.wrapoperation.WrapOperation;
import dev.villagefriends.fishing.Angling;
import dev.villagefriends.fishing.RodItem;
import it.unimi.dsi.fastutil.objects.ObjectArrayList;
import net.minecraft.core.BlockPos;
import net.minecraft.world.entity.projectile.FishingHook;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.storage.loot.LootParams;
import net.minecraft.world.level.storage.loot.LootTable;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * Tall Tales Fishing on vanilla's hook ({@link Angling}): a bite starts the catch-bar minigame and the bobber stays
 * under until it's decided; reeling in while it runs does nothing; what comes up is from the fish table; and the
 * Reinforced and Angler's Rods count as fishing rods for keeping the line out.
 */
@Mixin(FishingHook.class)
public abstract class FishingHookMixin {
    @Shadow private int nibble;
    @Unique private int villagefriends$lastNibble;

    @Inject(method = "catchingFish", at = @At("HEAD"), cancellable = true)
    private void villagefriends$holdTheFish(BlockPos pos, CallbackInfo ci) {
        if (!Angling.fighting((FishingHook) (Object) this)) return;
        if (nibble < 10) nibble = 20;
        ci.cancel();
    }
    @Inject(method = "catchingFish", at = @At("TAIL"))
    private void villagefriends$bite(BlockPos pos, CallbackInfo ci) {
        if (nibble > 0 && villagefriends$lastNibble <= 0) Angling.bite((FishingHook) (Object) this);
        villagefriends$lastNibble = nibble;
    }
    @Inject(method = "retrieve", at = @At("HEAD"), cancellable = true)
    private void villagefriends$waitForTheMinigame(ItemStack rod, CallbackInfoReturnable<Integer> cir) {
        if (Angling.holdsLine((FishingHook) (Object) this)) cir.setReturnValue(0);
    }
    @WrapOperation(method = "retrieve", at = @At(value = "INVOKE",
            target = "Lnet/minecraft/world/level/storage/loot/LootTable;getRandomItems(Lnet/minecraft/world/level/storage/loot/LootParams;)Lit/unimi/dsi/fastutil/objects/ObjectArrayList;"))
    private ObjectArrayList<ItemStack> villagefriends$catch(LootTable table, LootParams params, Operation<ObjectArrayList<ItemStack>> original) {
        return Angling.loot((FishingHook) (Object) this, params, () -> original.call(table, params));
    }
    // ItemStack.is(Item) compiles to the generic is(Object) in 26.3.
    @WrapOperation(method = "shouldStopFishing", at = @At(value = "INVOKE", target = "Lnet/minecraft/world/item/ItemStack;is(Ljava/lang/Object;)Z"))
    private boolean villagefriends$anyRod(ItemStack stack, Object item, Operation<Boolean> original) {
        return original.call(stack, item) || stack.getItem() instanceof RodItem;
    }
}
