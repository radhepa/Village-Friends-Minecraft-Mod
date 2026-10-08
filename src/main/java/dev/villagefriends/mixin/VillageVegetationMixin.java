package dev.villagefriends.mixin;

import dev.villagefriends.VillageGrounds;
import net.minecraft.core.BlockPos;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.chunk.ChunkGenerator;
import net.minecraft.world.level.levelgen.feature.BambooFeature;
import net.minecraft.world.level.levelgen.feature.BlockBlobFeature;
import net.minecraft.world.level.levelgen.feature.BlockColumnFeature;
import net.minecraft.world.level.levelgen.feature.FallenTreeFeature;
import net.minecraft.world.level.levelgen.feature.TreeFeature;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Trees, fallen logs, cacti/cane columns, bamboo and boulders skip village lots and streets. */
@Mixin({TreeFeature.class, FallenTreeFeature.class, BlockColumnFeature.class, BlockBlobFeature.class, BambooFeature.class})
public abstract class VillageVegetationMixin {
    @Inject(method = "place", at = @At("HEAD"), cancellable = true)
    private void villagefriends$keepOutOfVillages(WorldGenLevel level, ChunkGenerator generator, RandomSource random, BlockPos origin,
                                                 CallbackInfoReturnable<Boolean> cir) {
        if (VillageGrounds.occupied(origin)) cir.setReturnValue(false);
    }
}
