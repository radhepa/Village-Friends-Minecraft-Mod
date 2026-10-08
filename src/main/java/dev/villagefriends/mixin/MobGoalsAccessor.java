package dev.villagefriends.mixin;

import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.ai.goal.GoalSelector;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.gen.Accessor;

/** Lets residents' pets take on an extra goal for playing, napping by their resident and greeting players. */
@Mixin(Mob.class)
public interface MobGoalsAccessor {
    @Accessor("goalSelector") GoalSelector villagefriends$goals();
    @Accessor("targetSelector") GoalSelector villagefriends$targets();
}
