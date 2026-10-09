package dev.villagefriends.hearth;

import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;

/**
 * A recipe card: a family recipe written out by a friend. Use it to learn the recipe; family recipes only
 * cook at a station for someone who knows them, and show as a sealed card in the recipe book until then.
 */
public final class RecipeCardItem extends Item {
    public RecipeCardItem(Properties properties) { super(properties); }

    /** A card for this recipe. */
    public static ItemStack of(String recipe) {
        var stack = new ItemStack(HearthItems.RECIPE_CARD);
        stack.set(Hearth.RECIPE, recipe);
        return stack;
    }

    @Override public Component getName(ItemStack stack) {
        String recipe = stack.get(Hearth.RECIPE);
        var r = recipe == null ? null : Cookbook.get(recipe);
        var result = r == null ? null : HearthItems.stack(r.result(), 1);
        return result == null || result.isEmpty() ? super.getName(stack) : Component.translatable("item.villagefriends.recipe_card.named", result.getHoverName());
    }

    @Override public InteractionResult use(Level level, Player player, InteractionHand hand) {
        var stack = player.getItemInHand(hand);
        String recipe = stack.get(Hearth.RECIPE);
        if (recipe == null) return InteractionResult.PASS;
        if (!(player instanceof ServerPlayer p)) return InteractionResult.SUCCESS;
        var r = Cookbook.get(recipe);
        if (r == null) {
            p.sendSystemMessage(Component.literal("The ink has run; you can't make this recipe out.").withStyle(ChatFormatting.GRAY), true);
            return InteractionResult.FAIL;
        }
        var name = HearthItems.stack(r.result(), 1).getHoverName().getString();
        if (!Hearth.learn(p, recipe)) {
            p.sendSystemMessage(Component.literal("You already know how to make " + name + ".").withStyle(ChatFormatting.GRAY), true);
            return InteractionResult.FAIL;
        }
        if (!p.getAbilities().instabuild) stack.shrink(1);
        level.playSound(null, p.blockPosition(), SoundEvents.BOOK_PAGE_TURN, SoundSource.PLAYERS, 1F, 1F);
        p.sendSystemMessage(Component.literal("You learned the family recipe for " + name + ". It's in the recipe book at the "
                + Hearth.stationName(r.station()) + ".").withStyle(ChatFormatting.GOLD), false);
        return InteractionResult.SUCCESS_SERVER;
    }
}
