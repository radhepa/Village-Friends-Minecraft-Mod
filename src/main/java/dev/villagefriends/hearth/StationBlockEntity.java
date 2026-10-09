package dev.villagefriends.hearth;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.UUID;
import net.fabricmc.fabric.api.menu.v1.ExtendedMenuProvider;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.NonNullList;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.TagKey;
import net.minecraft.world.ContainerHelper;
import net.minecraft.world.Containers;
import net.minecraft.world.WorldlyContainer;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.ContainerData;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.component.CookingFuel;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.entity.BaseContainerBlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;
import net.minecraft.world.level.storage.loot.providers.number.ints.ResolvableInt;

/**
 * A kitchen station's contents and cooking. Six grid slots, the pot's vessel or the oven's fuel, and the
 * output. Each tick it looks for the recipe the grid makes ({@link Cookbook#find}) and, while the pot sits on
 * a lit fire, the oven is burning or always at the prep table, works through it; a finished batch uses one of
 * every ingredient (buckets and bottles come back), a vessel for pot dishes, and lands in the output.
 *
 * <p>Family recipes only cook for someone who knows them: the station remembers the last player who opened it
 * (the cook) and which family recipes they knew. Hoppers fill the grid from above and the vessel or fuel from
 * the sides, and take dishes out from below.
 */
public final class StationBlockEntity extends BaseContainerBlockEntity implements WorldlyContainer, ExtendedMenuProvider<StationMenu.Opening> {
    public static final TagKey<Block> HEAT = TagKey.create(Registries.BLOCK, Hearth.id("hearth/heat_sources"));
    public static final int DATA_PROGRESS = 0, DATA_TOTAL = 1, DATA_BURN = 2, DATA_BURN_TOTAL = 3, DATA_HEAT = 4, DATA_RECIPE = 5, DATA_COUNT = 6;

    public final Station station;
    private NonNullList<ItemStack> items;
    private int progress, total, burn, burnTotal;
    private boolean heat;
    private String current;
    private UUID cook;
    private boolean cookCreative;
    private final Set<String> cookKnows = new HashSet<>();
    /** The recipe the grid makes, worked out again whenever the contents change. */
    private CookingRecipe matched;
    private boolean dirty = true, ticking;

    private final ContainerData data = new ContainerData() {
        @Override public int get(int i) {
            return switch (i) {
                case DATA_PROGRESS -> progress; case DATA_TOTAL -> total; case DATA_BURN -> burn; case DATA_BURN_TOTAL -> burnTotal;
                case DATA_HEAT -> heat ? 1 : 0;
                case DATA_RECIPE -> matched == null ? -1 : Cookbook.forStation(station).indexOf(matched);
                default -> 0;
            };
        }
        @Override public void set(int i, int value) {
            switch (i) { case DATA_PROGRESS -> progress = value; case DATA_TOTAL -> total = value; case DATA_BURN -> burn = value; case DATA_BURN_TOTAL -> burnTotal = value; default -> {} }
        }
        @Override public int getCount() { return DATA_COUNT; }
    };

    public StationBlockEntity(BlockPos pos, BlockState state) {
        super(HearthBlocks.STATION, pos, state);
        station = state.getBlock() instanceof StationBlock block ? block.station : Station.PREP;
        items = NonNullList.withSize(station.slots(), ItemStack.EMPTY);
    }

    // -- cooking -----------------------------------------------------------------------------------

    public static void serverTick(Level level, BlockPos pos, BlockState state, StationBlockEntity be) {
        if (level instanceof ServerLevel server) be.tick(server, pos, state);
    }
    private void tick(ServerLevel level, BlockPos pos, BlockState state) {
        ticking = true;
        try { work(level, pos, state); } finally { ticking = false; }
    }
    private void work(ServerLevel level, BlockPos pos, BlockState state) {
        boolean changed = false;
        if (burn > 0) { burn--; changed = true; }
        if (dirty) { matched = Cookbook.find(station, view(0, Station.GRID), station == Station.POT ? new View(items.get(Station.GRID)) : null, this::allowed); dirty = false; }
        var recipe = matched;
        var result = recipe == null ? ItemStack.EMPTY : HearthItems.stack(recipe.result(), recipe.count());
        boolean room = recipe != null && !result.isEmpty() && fits(result);
        heat = switch (station) {
            case POT -> heated(level, pos);
            case OVEN -> burn > 0;
            case PREP -> true;
        };
        if (station == Station.OVEN && room && burn == 0 && refuel(level)) { heat = true; changed = true; }
        if (room && heat) {
            if (!recipe.id().equals(current)) { current = recipe.id(); progress = 0; }
            total = recipe.time();
            if (++progress >= total) { craft(level, pos, recipe); progress = 0; }
            changed = true;
        } else if (recipe == null || !room) {
            if (progress != 0 || current != null) changed = true;
            progress = 0; current = null; total = recipe == null ? 0 : recipe.time();
        } else if (station == Station.OVEN && progress > 0) {
            progress = Math.max(0, progress - 2); changed = true;
        }
        var next = state;
        if (station == Station.POT) next = next.setValue(StationBlock.LIT, heat && room).setValue(StationBlock.FILLED, !gridEmpty());
        if (station == Station.OVEN) next = next.setValue(StationBlock.LIT, burn > 0);
        if (next != state) level.setBlock(pos, next, Block.UPDATE_ALL);
        if (changed) setChanged();
    }
    /** A lit campfire, a fire, lava or magma right under the pot. */
    public static boolean heated(Level level, BlockPos pos) {
        var below = level.getBlockState(pos.below());
        return below.is(HEAT) && (!below.hasProperty(BlockStateProperties.LIT) || below.getValue(BlockStateProperties.LIT));
    }
    private boolean refuel(ServerLevel level) {
        var fuel = items.get(Station.GRID);
        if (fuel.isEmpty() || !fuel.has(DataComponents.COOKING_FUEL)) return false;
        int ticks = ResolvableInt.getFromItem(fuel, DataComponents.COOKING_FUEL, CookingFuel::burnTime, getLootContext(level), 0);
        if (ticks <= 0) return false;
        burn = burnTotal = ticks;
        var remainder = fuel.getItem().getCraftingRemainder();
        fuel.shrink(1);
        if (fuel.isEmpty() && remainder != null) items.set(Station.GRID, remainder.create());
        return true;
    }
    private boolean allowed(CookingRecipe r) { return !r.secret() || cookCreative || cookKnows.contains(r.id()); }
    private boolean fits(ItemStack result) {
        var out = items.get(station.output());
        return out.isEmpty() || ItemStack.isSameItemSameComponents(out, result) && out.getCount() + result.getCount() <= out.getMaxStackSize();
    }
    private void craft(ServerLevel level, BlockPos pos, CookingRecipe recipe) {
        int[] slots = Cookbook.assign(recipe, view(0, Station.GRID));
        if (slots == null) { dirty = true; return; }
        var spare = new ArrayList<ItemStack>();
        for (int slot : slots) {
            var stack = items.get(slot);
            var remainder = stack.getItem().getCraftingRemainder();
            stack.shrink(1);
            if (remainder != null) {
                if (stack.isEmpty()) items.set(slot, remainder.create()); else spare.add(remainder.create());
            }
        }
        if (recipe.vessel() != null && station == Station.POT) items.get(Station.GRID).shrink(1);
        var result = HearthItems.stack(recipe.result(), recipe.count());
        ServerPlayer player = cook == null ? null : level.getServer().getPlayerList().getPlayer(cook);
        HearthEvents.COOKED.invoker().cooked(level, pos, station, recipe, player, result);
        var out = items.get(station.output());
        if (out.isEmpty()) items.set(station.output(), result);
        else if (ItemStack.isSameItemSameComponents(out, result)) out.grow(result.getCount());
        else spare.add(result);
        for (var s : spare) Containers.dropItemStack(level, pos.getX() + .5, pos.getY() + 1.0, pos.getZ() + .5, s);
        dirty = true;
        double x = pos.getX() + .5, y = pos.getY() + .9, z = pos.getZ() + .5;
        switch (station) {
            case POT -> { level.playSound(null, pos, SoundEvents.BREWING_STAND_BREW, SoundSource.BLOCKS, .5F, 1.3F);
                level.sendParticles(ParticleTypes.WHITE_SMOKE, x, y, z, 6, .15, .1, .15, .02); }
            case OVEN -> { level.playSound(null, pos, SoundEvents.FURNACE_FIRE_CRACKLE, SoundSource.BLOCKS, .8F, 1.2F);
                level.sendParticles(ParticleTypes.SMOKE, x, pos.getY() + 1.05, z, 5, .1, .05, .1, .01); }
            case PREP -> level.playSound(null, pos, SoundEvents.WOOD_HIT, SoundSource.BLOCKS, .7F, 1.2F);
        }
    }

    /** The player who opens a station becomes its cook: their family recipes are what it may make. */
    public void cook(ServerPlayer p) {
        cook = p.getUUID();
        cookCreative = p.getAbilities().instabuild;
        cookKnows.clear(); cookKnows.addAll(Hearth.known(p));
        dirty = true; setChanged();
    }
    public boolean knows(CookingRecipe r) { return allowed(r); }

    /**
     * The recipe book's "fill" button: puts one batch (or as many as the player can, up to sixteen) of the
     * recipe's ingredients from the player's inventory into the grid, clearing anything else out first.
     */
    public void fill(ServerPlayer p, int index, boolean many) {
        var book = Cookbook.forStation(station);
        if (index < 0 || index >= book.size()) return;
        var recipe = book.get(index);
        if (!allowed(recipe)) { p.sendSystemMessage(Component.literal("That's a family recipe you haven't learned yet.").withStyle(ChatFormatting.GRAY), true); return; }
        var inventory = p.getInventory();
        boolean laidOut = Cookbook.assign(recipe, view(0, Station.GRID)) != null;
        if (!laidOut) for (int i = 0; i < Station.GRID; i++) {
            var s = items.get(i);
            if (!s.isEmpty()) { items.set(i, ItemStack.EMPTY); if (!inventory.add(s)) dev.villagefriends.VillageFriends.drop(p, s); }
        }
        int[] slots = laidOut ? Cookbook.assign(recipe, view(0, Station.GRID)) : null;
        int want = many ? 16 : 1;
        var missing = new ArrayList<String>();
        var ingredients = recipe.ingredients();
        for (int n = 0; n < ingredients.size(); n++) {
            int slot = slots != null ? slots[n] : n;
            var have = items.get(slot);
            Item item = !have.isEmpty() ? have.getItem() : pick(inventory, ingredients.get(n));
            if (item == null) { missing.add(name(ingredients.get(n))); continue; }
            String ingredient = ingredients.get(n);
            long sharing = ingredients.stream().filter(ingredient::equals).count();
            int share = (int) Math.max(1, (count(inventory, item) + have.getCount() * sharing) / sharing);
            int target = Math.min(Math.min(want, share), item.getDefaultMaxStackSize());
            int moved = take(inventory, item, target - have.getCount());
            if (moved > 0) { if (have.isEmpty()) items.set(slot, new ItemStack(item, moved)); else have.grow(moved); }
            if (items.get(slot).isEmpty()) missing.add(name(ingredient));
        }
        if (recipe.vessel() != null && station == Station.POT) {
            var vessel = items.get(Station.GRID);
            var item = BuiltInRegistries.ITEM.getValue(Identifier.parse(recipe.vessel()));
            if (vessel.isEmpty() || vessel.is(item)) {
                int moved = take(inventory, item, Math.min(want, item.getDefaultMaxStackSize()) - vessel.getCount());
                if (moved > 0) { if (vessel.isEmpty()) items.set(Station.GRID, new ItemStack(item, moved)); else vessel.grow(moved); }
            }
            if (items.get(Station.GRID).isEmpty()) missing.add(name(recipe.vessel()));
        }
        if (!missing.isEmpty()) p.sendSystemMessage(Component.literal("Missing: " + String.join(", ", missing)).withStyle(ChatFormatting.YELLOW), true);
        dirty = true; setChanged();
    }
    private static Item pick(Inventory inventory, String ingredient) {
        for (int i = 0; i < inventory.getContainerSize(); i++) {
            var s = inventory.getItem(i);
            if (!s.isEmpty() && !s.isDamaged() && Cookbook.accepts(ingredient, new View(s))) return s.getItem();
        }
        return null;
    }
    private static int count(Inventory inventory, Item item) {
        int n = 0;
        for (int i = 0; i < inventory.getContainerSize(); i++) if (inventory.getItem(i).is(item)) n += inventory.getItem(i).getCount();
        return n;
    }
    private static int take(Inventory inventory, Item item, int wanted) {
        int moved = 0;
        for (int i = 0; i < inventory.getContainerSize() && moved < wanted; i++) {
            var s = inventory.getItem(i);
            if (!s.is(item) || s.has(DataComponents.CUSTOM_NAME)) continue;
            int n = Math.min(wanted - moved, s.getCount());
            s.shrink(n); moved += n;
        }
        return moved;
    }
    private static String name(String ingredient) {
        if (ingredient.startsWith("#")) return ingredient.endsWith("cooking/fish") ? "fish" : ingredient.substring(ingredient.indexOf(':') + 1);
        return HearthItems.stack(ingredient, 1).getHoverName().getString();
    }

    /** A redstone comparator reads how full the output is. */
    int signal() {
        var out = items.get(station.output());
        return out.isEmpty() ? 0 : Math.max(1, out.getCount() * 15 / out.getMaxStackSize());
    }
    private boolean gridEmpty() {
        for (int i = 0; i < Station.GRID; i++) if (!items.get(i).isEmpty()) return false;
        return true;
    }

    /** A slot as the cookbook sees it. */
    record View(ItemStack stack) implements Cookbook.Slot {
        @Override public boolean isEmpty() { return stack.isEmpty(); }
        @Override public String item() { return BuiltInRegistries.ITEM.getKey(stack.getItem()).toString(); }
        @Override public boolean is(String tag) { return stack.is(TagKey.create(Registries.ITEM, Identifier.parse(tag))); }
    }
    private List<View> view(int from, int to) {
        var out = new ArrayList<View>();
        for (int i = from; i < to; i++) out.add(new View(items.get(i)));
        return out;
    }

    // -- container -----------------------------------------------------------------------------------

    public ContainerData data() { return data; }
    @Override protected Component getDefaultName() { return Component.translatable("container.villagefriends." + station.block); }
    @Override protected NonNullList<ItemStack> getItems() { return items; }
    @Override protected void setItems(NonNullList<ItemStack> items) { this.items = items; dirty = true; }
    @Override public int getContainerSize() { return items.size(); }
    @Override public void setItem(int slot, ItemStack stack) { super.setItem(slot, stack); dirty = true; }
    @Override public ItemStack removeItem(int slot, int count) { dirty = true; return super.removeItem(slot, count); }
    @Override public ItemStack removeItemNoUpdate(int slot) { dirty = true; return super.removeItemNoUpdate(slot); }
    /** Anything a menu or hopper changes means the grid may make something else; the station's own ticking doesn't. */
    @Override public void setChanged() { super.setChanged(); if (!ticking) dirty = true; }
    @Override public boolean canPlaceItem(int slot, ItemStack stack) {
        if (slot == station.output()) return false;
        if (slot == Station.GRID && station.extraSlot()) return station == Station.POT ? vessel(stack) : stack.has(DataComponents.COOKING_FUEL);
        return true;
    }
    public static boolean vessel(ItemStack stack) { return stack.is(Items.BOWL) || stack.is(Items.GLASS_BOTTLE); }
    @Override protected AbstractContainerMenu createMenu(int id, Inventory inventory) { return new StationMenu(id, inventory, this); }
    @Override public StationMenu.Opening getScreenOpeningData(ServerPlayer player) { return StationMenu.Opening.of(this, player); }

    private static final int[] NO_SLOTS = {};
    @Override public int[] getSlotsForFace(Direction side) {
        if (side == Direction.DOWN) return new int[]{station.output()};
        if (side == Direction.UP) return new int[]{0, 1, 2, 3, 4, 5};
        return station.extraSlot() ? new int[]{Station.GRID} : NO_SLOTS;
    }
    @Override public boolean canPlaceItemThroughFace(int slot, ItemStack stack, Direction side) {
        return side != Direction.DOWN && canPlaceItem(slot, stack);
    }
    @Override public boolean canTakeItemThroughFace(int slot, ItemStack stack, Direction side) { return side == Direction.DOWN && slot == station.output(); }

    @Override public void preRemoveSideEffects(BlockPos pos, BlockState state) {
        if (level != null) Containers.dropContents(level, pos, this);
    }

    @Override protected void loadAdditional(ValueInput input) {
        super.loadAdditional(input);
        items = NonNullList.withSize(station.slots(), ItemStack.EMPTY);
        ContainerHelper.loadAllItems(input, items);
        progress = input.getIntOr("progress", 0); total = input.getIntOr("total", 0);
        burn = input.getIntOr("burn", 0); burnTotal = input.getIntOr("burn_total", 0);
        current = input.getString("current").orElse(null);
        cook = input.getString("cook").map(UUID::fromString).orElse(null);
        cookCreative = input.getBooleanOr("cook_creative", false);
        cookKnows.clear();
        input.getString("cook_knows").ifPresent(s -> { for (var id : s.split(",")) if (!id.isBlank()) cookKnows.add(id); });
        dirty = true;
    }
    @Override protected void saveAdditional(ValueOutput output) {
        super.saveAdditional(output);
        ContainerHelper.saveAllItems(output, items);
        output.putInt("progress", progress); output.putInt("total", total);
        output.putInt("burn", burn); output.putInt("burn_total", burnTotal);
        if (current != null) output.putString("current", current);
        if (cook != null) output.putString("cook", cook.toString());
        output.putBoolean("cook_creative", cookCreative);
        output.putString("cook_knows", String.join(",", cookKnows));
    }

    @Override public boolean stillValid(Player player) { return net.minecraft.world.Container.stillValidBlockEntity(this, player); }
}
