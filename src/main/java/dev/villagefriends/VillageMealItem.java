package dev.villagefriends;

import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;

public final class VillageMealItem extends Item {
    private final float healing;
    public VillageMealItem(Properties properties, float healing) { super(properties); this.healing = healing; }
    @Override public ItemStack finishUsingItem(ItemStack stack, Level level, LivingEntity entity) {
        ItemStack remainder = super.finishUsingItem(stack, level, entity);
        if (!level.isClientSide()) entity.heal(healing);
        return remainder;
    }
}
