package dev.villagefriends.mixin;

import dev.villagefriends.VillageGrounds;
import net.minecraft.world.level.StructureManager;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.chunk.ChunkAccess;
import net.minecraft.world.level.chunk.ChunkGenerator;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Shares the decorating region's structure manager with {@link VillageGrounds}. */
@Mixin(ChunkGenerator.class)
public abstract class ChunkGeneratorDecorationMixin {
    @Inject(method = "applyBiomeDecoration", at = @At("HEAD"))
    private void villagefriends$beginDecoration(WorldGenLevel level, ChunkAccess chunk, StructureManager structureManager, CallbackInfo ci) {
        VillageGrounds.begin(structureManager);
    }

    @Inject(method = "applyBiomeDecoration", at = @At("RETURN"))
    private void villagefriends$endDecoration(WorldGenLevel level, ChunkAccess chunk, StructureManager structureManager, CallbackInfo ci) {
        VillageGrounds.end();
    }
}
