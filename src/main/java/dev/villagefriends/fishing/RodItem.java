package dev.villagefriends.fishing;

import java.util.function.Consumer;
import net.minecraft.ChatFormatting;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.stats.Stats;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.SlotAccess;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.projectile.FishingHook;
import net.minecraft.world.entity.projectile.Projectile;
import net.minecraft.world.inventory.ClickAction;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.item.FishingRodItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.component.TooltipDisplay;
import net.minecraft.world.item.enchantment.EnchantmentHelper;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.gameevent.GameEvent;

/**
 * The Reinforced Rod and the Angler's Rod: fishing rods that take bait and tackle. Click bait or tackle onto the
 * rod in your inventory to load it (the same kind tops up, another kind swaps); right-click the rod with an empty
 * hand to take the bait out (then the tackle). Bait makes bites come sooner, which this rod's cast accounts for;
 * what the gear does to the catch is in {@link Gear} and {@link Angling}.
 */
public class RodItem extends FishingRodItem {
    public final Gear.Rod rod;
    public RodItem(Properties properties, Gear.Rod rod) { super(properties); this.rod = rod; }

    /** What kind of rod a stack is: the vanilla Fishing Rod is plain. */
    public static Gear.Rod rod(ItemStack stack) { return stack.getItem() instanceof RodItem r ? r.rod : Gear.Rod.PLAIN; }
    public static Gear.Bait bait(ItemStack rod) {
        var loaded = rod.get(Fishing.BAIT);
        return loaded == null || loaded.count() <= 0 ? null : Gear.Bait.byId(path(loaded.item()));
    }
    public static Gear.Tackle tackle(ItemStack rod) {
        var loaded = rod.get(Fishing.TACKLE);
        return loaded == null || loaded.count() <= 0 ? null : Gear.Tackle.byId(path(loaded.item()));
    }
    private static String path(String id) { int c = id.indexOf(':'); return c < 0 ? id : id.substring(c + 1); }

    @Override public InteractionResult use(Level level, Player player, InteractionHand hand) {
        if (player.fishing != null) return super.use(level, player, hand);
        var stack = player.getItemInHand(hand);
        level.playSound(null, player.getX(), player.getY(), player.getZ(), SoundEvents.FISHING_BOBBER_THROW, SoundSource.NEUTRAL, .5F,
                .4F / (level.getRandom().nextFloat() * .4F + .8F));
        if (level instanceof ServerLevel serverLevel) {
            int lure = (int) (EnchantmentHelper.getFishingTimeReduction(serverLevel, stack, player) * 20) + Gear.quicker(bait(stack), tackle(stack), 350);
            int luck = EnchantmentHelper.getFishingLuckBonus(serverLevel, stack, player);
            Projectile.spawnProjectile(new FishingHook(player, level, luck, lure), serverLevel, stack);
        }
        player.awardStat(Stats.ITEM_USED.get(this));
        stack.causeUseVibration(player, GameEvent.ITEM_INTERACT_START);
        return InteractionResult.SUCCESS;
    }

    // -- loading bait and tackle ---------------------------------------------------------------------

    @Override public boolean overrideOtherStackedOnMe(ItemStack self, ItemStack other, Slot slot, ClickAction action, Player player, SlotAccess carried) {
        if (action == ClickAction.PRIMARY && !other.isEmpty()) return load(self, other, carried, player);
        if (action == ClickAction.SECONDARY && other.isEmpty()) {
            var out = unload(self);
            if (out.isEmpty()) return false;
            carried.set(out);
            player.playSound(SoundEvents.BUNDLE_REMOVE_ONE, .8F, 1);
            return true;
        }
        return false;
    }
    @Override public boolean overrideStackedOnOther(ItemStack self, Slot slot, ClickAction action, Player player) {
        if (action != ClickAction.SECONDARY || !slot.hasItem()) return false;
        var other = slot.getItem();
        if (FishingItems.bait(other) == null && FishingItems.tackle(other) == null) return false;
        var rest = other.copy();
        boolean done = load(self, rest, SlotAccess.of(() -> rest, s -> {}), player);
        if (done) slot.set(rest);
        return done;
    }

    /** Loads bait or tackle from {@code from} (shrinking it, or swapping what was loaded into {@code back}). */
    private boolean load(ItemStack rodStack, ItemStack from, SlotAccess back, Player player) {
        var bait = FishingItems.bait(from); var tackle = FishingItems.tackle(from);
        if (bait == null && tackle == null) return false;
        String id = BuiltInRegistries.ITEM.getKey(from.getItem()).toString();
        if (bait != null) {
            var loaded = rodStack.get(Fishing.BAIT);
            if (loaded != null && loaded.count() > 0 && !loaded.item().equals(id)) {
                // Another bait: swap them.
                var old = FishingItems.stack(loaded.item(), loaded.count());
                int take = Math.min(Gear.MAX_BAIT, from.getCount());
                rodStack.set(Fishing.BAIT, new Fishing.Loaded(id, take));
                from.shrink(take);
                if (from.isEmpty()) back.set(old); else if (!player.getInventory().add(old) && player.level() instanceof net.minecraft.server.level.ServerLevel sl) player.spawnAtLocation(sl, old);
            } else {
                int have = loaded == null ? 0 : loaded.count(), take = Math.min(Gear.MAX_BAIT - have, from.getCount());
                if (take <= 0) return true;
                rodStack.set(Fishing.BAIT, new Fishing.Loaded(id, have + take));
                from.shrink(take);
            }
        } else {
            var loaded = rodStack.get(Fishing.TACKLE);
            if (loaded != null && loaded.count() > 0) {
                if (loaded.item().equals(id)) return true;
                var old = FishingItems.stack(loaded.item(), 1);
                if (!player.getInventory().add(old) && player.level() instanceof net.minecraft.server.level.ServerLevel sl) player.spawnAtLocation(sl, old);
            }
            rodStack.set(Fishing.TACKLE, new Fishing.Loaded(id, Gear.TACKLE_USES));
            from.shrink(1);
        }
        player.playSound(SoundEvents.BUNDLE_INSERT, .8F, 1);
        return true;
    }
    /** Takes the bait out, or if there's none, the tackle (worn tackle can't be reused, so it comes out as new only when unused). */
    private static ItemStack unload(ItemStack rodStack) {
        var bait = rodStack.get(Fishing.BAIT);
        if (bait != null && bait.count() > 0) {
            rodStack.remove(Fishing.BAIT);
            return FishingItems.stack(bait.item(), bait.count());
        }
        var tackle = rodStack.get(Fishing.TACKLE);
        if (tackle != null && tackle.count() > 0) {
            rodStack.remove(Fishing.TACKLE);
            return tackle.count() >= Gear.TACKLE_USES ? FishingItems.stack(tackle.item(), 1) : ItemStack.EMPTY;
        }
        return ItemStack.EMPTY;
    }

    @Override public void appendHoverText(ItemStack stack, TooltipContext context, TooltipDisplay display, Consumer<Component> out, TooltipFlag flag) {
        var bait = stack.get(Fishing.BAIT); var tackle = stack.get(Fishing.TACKLE);
        out.accept(Component.literal("Bait: " + (bait == null || bait.count() <= 0 ? "none" : name(bait.item()) + " ×" + bait.count())).withStyle(ChatFormatting.GRAY));
        out.accept(Component.literal("Tackle: " + (tackle == null || tackle.count() <= 0 ? "none" : name(tackle.item()) + " (" + tackle.count() + " fish left)"))
                .withStyle(ChatFormatting.GRAY));
        if (bait == null && tackle == null) out.accept(Component.literal("Click bait or tackle onto this rod to load it.").withStyle(ChatFormatting.DARK_GRAY));
    }
    private static String name(String id) {
        return BuiltInRegistries.ITEM.getValue(Identifier.parse(id)).getDefaultInstance().getHoverName().getString();
    }
}
