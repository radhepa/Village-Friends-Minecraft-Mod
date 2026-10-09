package dev.villagefriends.hearth;

import java.util.ArrayList;
import java.util.List;
import net.minecraft.core.BlockPos;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.TagKey;
import net.minecraft.world.Container;
import net.minecraft.world.SimpleContainer;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.ContainerData;
import net.minecraft.world.inventory.SimpleContainerData;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.item.ItemStack;

/**
 * A kitchen station's screen: the six-slot grid, the pot's vessel slot or the oven's fuel slot, the output
 * and the player's inventory, at the pixel positions of the {@code hearth_<station>.png} backgrounds. The
 * recipe book is sent when the screen opens ({@link Opening}); clicking a recipe in it presses menu button
 * {@code index} (or {@code index + MANY} with shift) to fill the grid from the player's inventory.
 */
public final class StationMenu extends AbstractContainerMenu {
    public static final int MANY = 1000;
    public static final int GRID_X = 30, GRID_Y = 17, EXTRA_X = 48, EXTRA_Y = 55, OUT_X = 124, OUT_Y = 35;

    /** One recipe in the book: what it makes, the options for each slot, the vessel, how long, and whether you know it. */
    public record BookEntry(String id, ItemStack result, List<List<ItemStack>> ingredients, ItemStack vessel, int time, boolean secret, boolean known) {
        static final StreamCodec<RegistryFriendlyByteBuf, BookEntry> STREAM_CODEC = StreamCodec.of((buf, e) -> {
            ByteBufCodecs.STRING_UTF8.encode(buf, e.id);
            ItemStack.OPTIONAL_STREAM_CODEC.encode(buf, e.result);
            buf.writeVarInt(e.ingredients.size());
            for (var options : e.ingredients) {
                buf.writeVarInt(options.size());
                for (var s : options) ItemStack.OPTIONAL_STREAM_CODEC.encode(buf, s);
            }
            ItemStack.OPTIONAL_STREAM_CODEC.encode(buf, e.vessel);
            buf.writeVarInt(e.time); buf.writeBoolean(e.secret); buf.writeBoolean(e.known);
        }, buf -> {
            String id = ByteBufCodecs.STRING_UTF8.decode(buf);
            var result = ItemStack.OPTIONAL_STREAM_CODEC.decode(buf);
            int n = buf.readVarInt();
            var ingredients = new ArrayList<List<ItemStack>>();
            for (int i = 0; i < n; i++) {
                int m = buf.readVarInt();
                var options = new ArrayList<ItemStack>();
                for (int j = 0; j < m; j++) options.add(ItemStack.OPTIONAL_STREAM_CODEC.decode(buf));
                ingredients.add(options);
            }
            var vessel = ItemStack.OPTIONAL_STREAM_CODEC.decode(buf);
            return new BookEntry(id, result, ingredients, vessel, buf.readVarInt(), buf.readBoolean(), buf.readBoolean());
        });
    }

    /** What the client needs to draw a station's screen: where it is, which station, and its recipe book. */
    public record Opening(BlockPos pos, Station station, List<BookEntry> book) {
        public static final StreamCodec<RegistryFriendlyByteBuf, Opening> STREAM_CODEC = StreamCodec.of((buf, o) -> {
            buf.writeBlockPos(o.pos); buf.writeVarInt(o.station.ordinal());
            buf.writeVarInt(o.book.size());
            for (var e : o.book) BookEntry.STREAM_CODEC.encode(buf, e);
        }, buf -> {
            var pos = buf.readBlockPos(); var station = Station.values()[buf.readVarInt()];
            int n = buf.readVarInt();
            var book = new ArrayList<BookEntry>();
            for (int i = 0; i < n; i++) book.add(BookEntry.STREAM_CODEC.decode(buf));
            return new Opening(pos, station, book);
        });

        static Opening of(StationBlockEntity be, ServerPlayer player) {
            var book = new ArrayList<BookEntry>();
            for (var r : Cookbook.forStation(be.station)) {
                var ingredients = new ArrayList<List<ItemStack>>();
                for (var ingredient : r.ingredients()) ingredients.add(options(ingredient));
                var vessel = r.vessel() == null ? ItemStack.EMPTY : HearthItems.stack(r.vessel(), 1);
                book.add(new BookEntry(r.id(), HearthItems.stack(r.result(), r.count()), ingredients, vessel, r.time(), r.secret(), be.knows(r)));
            }
            return new Opening(be.getBlockPos(), be.station, book);
        }
        /** The items an ingredient accepts, for the book to cycle through (a tag's members, or the one item). */
        static List<ItemStack> options(String ingredient) {
            if (!ingredient.startsWith("#")) return List.of(HearthItems.stack(ingredient, 1));
            var tag = TagKey.create(Registries.ITEM, Identifier.parse(ingredient.substring(1)));
            var out = new ArrayList<ItemStack>();
            for (var holder : BuiltInRegistries.ITEM.getTagOrEmpty(tag)) { out.add(new ItemStack(holder)); if (out.size() >= 8) break; }
            return out;
        }
    }

    public final Station station;
    public final Opening opening;
    private final Container container;
    private final ContainerData data;

    /** The client's menu, built from the opening data. */
    public StationMenu(int id, Inventory inventory, Opening opening) {
        this(id, inventory, opening, new SimpleContainer(opening.station().slots()), new SimpleContainerData(StationBlockEntity.DATA_COUNT));
    }
    /** The server's menu, over the real station. */
    StationMenu(int id, Inventory inventory, StationBlockEntity be) {
        this(id, inventory, inventory.player instanceof ServerPlayer p ? Opening.of(be, p) : new Opening(be.getBlockPos(), be.station, List.of()), be, be.data());
    }
    private StationMenu(int id, Inventory inventory, Opening opening, Container container, ContainerData data) {
        super(HearthBlocks.MENU, id);
        this.station = opening.station(); this.opening = opening; this.container = container; this.data = data;
        checkContainerSize(container, station.slots());
        container.startOpen(inventory.player);
        for (int r = 0; r < 2; r++)
            for (int c = 0; c < 3; c++) addSlot(new Slot(container, r * 3 + c, GRID_X + c * 18, GRID_Y + r * 18));
        if (station.extraSlot()) addSlot(new Slot(container, Station.GRID, EXTRA_X, EXTRA_Y) {
            @Override public boolean mayPlace(ItemStack stack) { return extra(stack); }
        });
        addSlot(new Slot(container, station.output(), OUT_X, OUT_Y) {
            @Override public boolean mayPlace(ItemStack stack) { return false; }
            @Override public void onTake(Player player, ItemStack stack) {
                super.onTake(player, stack);
                if (player instanceof ServerPlayer p && !stack.isEmpty()) {
                    HearthEvents.TAKEN.invoker().taken(p, station, stack);
                    p.level().playSound(null, p.blockPosition(), SoundEvents.ITEM_PICKUP, SoundSource.PLAYERS, .3F, 1.4F);
                }
            }
        });
        addStandardInventorySlots(inventory, 8, 84);
        addDataSlots(data);
    }

    public int data(int i) { return data.get(i); }
    public int stationSlots() { return station.slots(); }

    @Override public boolean clickMenuButton(Player player, int id) {
        if (player instanceof ServerPlayer p && container instanceof StationBlockEntity be) {
            be.fill(p, id % MANY, id >= MANY);
            return true;
        }
        return false;
    }

    @Override public ItemStack quickMoveStack(Player player, int index) {
        var slot = slots.get(index);
        if (!slot.hasItem()) return ItemStack.EMPTY;
        var stack = slot.getItem(); var copy = stack.copy();
        int own = station.slots(), end = own + 36;
        int output = station.output();
        if (index == output) {
            if (!moveItemStackTo(stack, own, end, true)) return ItemStack.EMPTY;
            slot.onQuickCraft(stack, copy);
        } else if (index < own) {
            if (!moveItemStackTo(stack, own, end, false)) return ItemStack.EMPTY;
        } else {
            boolean extra = station.extraSlot() && extra(stack);
            if (extra && !moveItemStackTo(stack, Station.GRID, Station.GRID + 1, false) || !extra && !moveItemStackTo(stack, 0, Station.GRID, false)) {
                // Not an ingredient slot's business: shuffle between inventory and hotbar instead.
                if (index < end - 9 ? !moveItemStackTo(stack, end - 9, end, false) : !moveItemStackTo(stack, own, end - 9, false)) return ItemStack.EMPTY;
            }
        }
        if (stack.isEmpty()) slot.setByPlayer(ItemStack.EMPTY); else slot.setChanged();
        if (stack.getCount() == copy.getCount()) return ItemStack.EMPTY;
        slot.onTake(player, stack);
        return copy;
    }
    @Override public boolean stillValid(Player player) { return container.stillValid(player); }
    @Override public void removed(Player player) { super.removed(player); container.stopOpen(player); }

    /** Whether the player's inventory (plus what's already in the grid) holds everything this recipe needs. */
    public boolean canMake(Player player, BookEntry entry) {
        var pool = new ArrayList<ItemStack>();
        for (int i = 0; i < player.getInventory().getContainerSize(); i++) pool.add(player.getInventory().getItem(i).copy());
        for (int i = 0; i < Station.GRID; i++) pool.add(container.getItem(i).copy());
        for (var options : entry.ingredients()) {
            boolean found = false;
            for (var s : pool) {
                if (s.isEmpty()) continue;
                for (var o : options) if (ItemStack.isSameItem(s, o)) { s.shrink(1); found = true; break; }
                if (found) break;
            }
            if (!found) return false;
        }
        if (!entry.vessel().isEmpty()) {
            boolean vessel = container.getItem(Station.GRID).is(entry.vessel().getItem());
            for (var s : pool) if (s.is(entry.vessel().getItem())) vessel = true;
            return vessel;
        }
        return true;
    }
    /** What goes in the slot under the grid: a bowl or bottle in the pot, fuel in the oven. */
    boolean extra(ItemStack stack) { return station == Station.POT ? StationBlockEntity.vessel(stack) : station == Station.OVEN && stack.has(DataComponents.COOKING_FUEL); }
}
