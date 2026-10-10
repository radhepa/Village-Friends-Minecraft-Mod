package dev.villagefriends.stable.client.breed;

import dev.villagefriends.VillageBlocks;
import dev.villagefriends.stable.data.StableItems;
import java.util.Set;
import net.fabricmc.fabric.api.client.item.v1.ItemTooltipCallback;
import net.fabricmc.fabric.api.resource.v1.ResourceLoader;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.server.packs.PackType;
import net.minecraft.server.packs.resources.ResourceManager;
import net.minecraft.server.packs.resources.SimplePreparableReloadListener;
import net.minecraft.util.profiling.ProfilerFiller;

/** The breeds package's client side (coats, brush and whistle feedback). Called once from {@code StablehandClient}. */
public final class BreedClient {
    public static void register() {
        // Which painted coats exist, so a breed without art falls back to vanilla's coat instead of a missing texture.
        ResourceLoader.get(PackType.CLIENT_RESOURCES).registerReloadListener(VillageBlocks.id("horse_coats"),
                new SimplePreparableReloadListener<Set<Identifier>>() {
                    @Override protected Set<Identifier> prepare(ResourceManager resources, ProfilerFiller profiler) {
                        return Set.copyOf(resources.listResources(HorseCoats.FOLDER,
                                id -> id.getNamespace().equals("villagefriends") && id.getPath().endsWith(".png")).keySet());
                    }
                    @Override protected void apply(Set<Identifier> coats, ResourceManager resources, ProfilerFiller profiler) { HorseCoats.loaded(coats); }
                });
        // The brush and whistle say what they do (the rest of their feedback comes from the server).
        ItemTooltipCallback.EVENT.register((stack, context, flag, lines) -> {
            if (stack.is(StableItems.GROOMING_BRUSH)) lines.add(1, Component.literal("Use on your horse to groom it and grow your bond").withStyle(ChatFormatting.GRAY));
            else if (stack.is(StableItems.HORSE_WHISTLE)) lines.add(1, Component.literal("Calls your Loyal horse from up to 96 blocks").withStyle(ChatFormatting.GRAY));
        });
    }

    private BreedClient() {}
}
