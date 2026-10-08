package dev.villagefriends;

import dev.villagefriends.home.Homes;
import net.minecraft.core.BlockPos;
import net.minecraft.core.component.DataComponentGetter;
import net.minecraft.core.component.DataComponents;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;

/**
 * A House Plaque's memory: the house it names (its id in the village's housing index) and the name a player
 * gave it on an anvil. The house itself lives in the housing index ({@link Homes}).
 */
public final class HousePlaqueBlockEntity extends BlockEntity {
    private String house = "", name = "";

    public HousePlaqueBlockEntity(BlockPos pos, BlockState state) { super(VillageBlockEntities.HOUSE_PLAQUE, pos, state); }

    public String house() { return house; }
    public String name() { return name; }
    public void name(String next) { name = next == null ? "" : next; setChanged(); }

    /** Finds the house this plaque is in (a village house, or the rooms a player built around it) and its beds. Returns what to tell the player. */
    public String scanForBeds() {
        if (!(level instanceof ServerLevel server)) return "";
        String message = Homes.scanPlaque(server, worldPosition, name);
        var record = VillageSettlements.book(server).at(worldPosition);
        var index = record == null ? null : Homes.index(server, record.id());
        String found = "";
        if (index != null) for (var h : index.houses()) if (h.plaque().isPresent() && h.plaque().get().equals(worldPosition)) { found = h.id(); break; }
        if (!found.equals(house)) { house = found; setChanged(); }
        return message;
    }
    /** Looks the house's job sites over again (they are read with its beds). */
    public void scanForWorkstations() { scanForBeds(); }

    @Override protected void applyImplicitComponents(DataComponentGetter components) {
        super.applyImplicitComponents(components);
        var custom = components.get(DataComponents.CUSTOM_NAME);
        if (custom != null) name = custom.getString();
    }
    @Override protected void loadAdditional(ValueInput input) {
        super.loadAdditional(input);
        house = input.getStringOr("house", ""); name = input.getStringOr("name", "");
    }
    @Override protected void saveAdditional(ValueOutput output) {
        super.saveAdditional(output);
        if (!house.isEmpty()) output.putString("house", house);
        if (!name.isEmpty()) output.putString("name", name);
    }
}
