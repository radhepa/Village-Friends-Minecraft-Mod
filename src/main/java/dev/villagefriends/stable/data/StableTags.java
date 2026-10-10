package dev.villagefriends.stable.data;

import dev.villagefriends.VillageBlocks;
import net.minecraft.core.registries.Registries;
import net.minecraft.tags.TagKey;
import net.minecraft.world.entity.EntityType;

/** Stablehand's tags. */
public final class StableTags {
    /**
     * Not-So-Vanilla Mobs' challenger bosses, which spook every horse. Every entry is {@code "required": false},
     * so without that mod the tag is simply empty; it is only checked when {@code nsvmobs} is loaded.
     */
    public static final TagKey<EntityType<?>> CHALLENGERS = TagKey.create(Registries.ENTITY_TYPE, VillageBlocks.id("challengers"));
    /** The entity tag ({@code Tags} in NBT) that stable templates put on their horses; the yard settles them on first load. */
    public static final String STABLE_HORSE = "villagefriends.stable_horse";

    private StableTags() {}
}
