package dev.villagefriends;

import com.mojang.logging.LogUtils;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;
import net.minecraft.core.BlockPos;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.NonNullList;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.protocol.game.ClientboundBlockEntityDataPacket;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.ProblemReporter;
import net.minecraft.world.Containers;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.RecipeType;
import net.minecraft.world.item.crafting.SingleRecipeInput;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.storage.TagValueOutput;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;
import org.slf4j.Logger;

/**
 * What a workstation remembers: food cooking on the stove, drinks in the barrel or tap, herbs in the
 * press, offcuts at the sawmill, the cook's dish of the day and who has had some, and how far the
 * painter has got with the canvas.
 */
public final class WorkstationBlockEntity extends BlockEntity {
    private static final Logger LOGGER = LogUtils.getLogger();
    public static final int SLOTS = 4;
    final NonNullList<ItemStack> items = NonNullList.withSize(SLOTS, ItemStack.EMPTY);
    final int[] progress = new int[SLOTS], total = new int[SLOTS];
    /** Drinks, herbs or offcuts, depending on the station. */
    int stock;
    /** The day the cook last made the dish of the day, and who has been served it. */
    long mealDay = -1;
    final Set<String> served = new HashSet<>();
    /** The painter's progress on the current canvas, 0-100. */
    int paint;
    /** Game time until which the stove stays lit after its cook has been at work. */
    long warmUntil;
    /** Game time when the music stand can play again. */
    long quietUntil;

    public WorkstationBlockEntity(BlockPos pos, BlockState state) { super(VillageBlockEntities.WORKSTATION, pos, state); }

    public NonNullList<ItemStack> items() { return items; }
    public int stock() { return stock; }

    /** Puts raw food on the stove; false when every spot is taken or it isn't something to cook. */
    boolean cook(ServerLevel level, ItemStack food) {
        var recipe = level.recipeAccess().getRecipeFor(RecipeType.CAMPFIRE_COOKING, new SingleRecipeInput(food), level);
        if (recipe.isEmpty()) return false;
        for (int slot = 0; slot < SLOTS; slot++) {
            if (!items.get(slot).isEmpty()) continue;
            // A proper stove is twice as quick as a campfire.
            total[slot] = Math.max(100, recipe.get().value().cookingTime() / 2); progress[slot] = 0;
            items.set(slot, food.split(1));
            changed();
            return true;
        }
        return false;
    }
    boolean cooking() { return items.stream().anyMatch(s -> !s.isEmpty()); }

    static void stoveTick(ServerLevel level, BlockPos pos, BlockState state, WorkstationBlockEntity e) {
        boolean changed = false;
        for (int slot = 0; slot < SLOTS; slot++) {
            var stack = e.items.get(slot);
            if (stack.isEmpty()) continue;
            if (++e.progress[slot] < e.total[slot]) continue;
            var input = new SingleRecipeInput(stack);
            var result = level.recipeAccess().getRecipeFor(RecipeType.CAMPFIRE_COOKING, input, level).map(r -> r.value().assemble(input)).orElse(stack);
            Containers.dropItemStack(level, pos.getX(), pos.getY() + .75, pos.getZ(), result);
            e.items.set(slot, ItemStack.EMPTY); e.progress[slot] = 0;
            level.playSound(null, pos, SoundEvents.SMOKER_SMOKE, SoundSource.BLOCKS, .8F, 1.2F);
            changed = true;
        }
        if (changed) e.changed();
        // The fire burns while something cooks, and for a while after the cook has been at work.
        boolean lit = e.cooking() || level.getGameTime() < e.warmUntil;
        if (state.getValue(WorkstationBlock.LIT) != lit) level.setBlock(pos, state.setValue(WorkstationBlock.LIT, lit), 3);
        if (e.cooking() && level.getGameTime() % 40 == 0) level.playSound(null, pos, SoundEvents.CAMPFIRE_CRACKLE, SoundSource.BLOCKS, .5F, 1.3F);
    }

    void changed() {
        setChanged();
        if (level != null) level.sendBlockUpdated(worldPosition, getBlockState(), getBlockState(), 3);
    }

    @Override protected void loadAdditional(ValueInput input) {
        super.loadAdditional(input);
        items.clear();
        net.minecraft.world.ContainerHelper.loadAllItems(input, items);
        input.getIntArray("Progress").ifPresentOrElse(a -> System.arraycopy(a, 0, progress, 0, Math.min(SLOTS, a.length)), () -> Arrays.fill(progress, 0));
        input.getIntArray("Total").ifPresentOrElse(a -> System.arraycopy(a, 0, total, 0, Math.min(SLOTS, a.length)), () -> Arrays.fill(total, 0));
        stock = input.getIntOr("Stock", 0);
        mealDay = input.getLongOr("MealDay", -1);
        served.clear();
        for (String id : input.getStringOr("Served", "").split(",")) if (!id.isEmpty()) served.add(id);
        paint = input.getIntOr("Paint", 0);
        warmUntil = input.getLongOr("WarmUntil", 0);
        quietUntil = input.getLongOr("QuietUntil", 0);
    }
    @Override protected void saveAdditional(ValueOutput output) {
        super.saveAdditional(output);
        net.minecraft.world.ContainerHelper.saveAllItems(output, items, true);
        output.putIntArray("Progress", progress); output.putIntArray("Total", total);
        output.putInt("Stock", stock); output.putLong("MealDay", mealDay); output.putString("Served", String.join(",", served));
        output.putInt("Paint", paint); output.putLong("WarmUntil", warmUntil); output.putLong("QuietUntil", quietUntil);
    }
    @Override public ClientboundBlockEntityDataPacket getUpdatePacket() { return ClientboundBlockEntityDataPacket.create(this); }
    /** Clients only need what is on the stove, to draw it. */
    @Override public CompoundTag getUpdateTag(HolderLookup.Provider registries) {
        try (var reporter = new ProblemReporter.ScopedCollector(problemPath(), LOGGER)) {
            var output = TagValueOutput.createWithContext(reporter, registries);
            net.minecraft.world.ContainerHelper.saveAllItems(output, items, true);
            output.putInt("Stock", stock);
            return output.buildResult();
        }
    }
    @Override public void preRemoveSideEffects(BlockPos pos, BlockState state) {
        if (level != null) Containers.dropContents(level, pos, items);
    }
}
