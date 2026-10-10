package dev.villagefriends.stable.yard;

import dev.villagefriends.stable.api.Horses;
import dev.villagefriends.stable.data.StableComponents;
import net.minecraft.core.Direction;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.entity.animal.equine.Horse;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.BlockHitResult;

/**
 * Horse Papers: the stablehand sells a horse as its papers. Used on the top of a block, they bring the animal they
 * name (a horse of a breed, a donkey or a mule) to stand there: grown, tame and yours, the papers handed over.
 * It is yours to stable anywhere; nothing about it belongs to a village.
 */
public final class Papers {
    /** Horse Papers were used on a block (the yard's UseBlockCallback; the game test calls it directly). */
    public static InteractionResult use(Player player, Level level, BlockHitResult hit, ItemStack stack) {
        if (hit.getDirection() != Direction.UP || player.isSpectator()) return InteractionResult.PASS;
        if (!(level instanceof ServerLevel server)) return InteractionResult.SUCCESS;
        var papers = stack.get(StableComponents.HORSE_PAPERS);
        String breed = papers == null ? "" : papers.breed();
        EntityType<? extends AbstractHorse> type = switch (breed) {
            case "donkey" -> EntityTypes.DONKEY;
            case "mule" -> EntityTypes.MULE;
            default -> Horses.breeds().contains(breed) ? EntityTypes.HORSE : null;
        };
        if (type == null) { player.sendOverlayMessage(Component.literal("These papers don't name any horse.")); return InteractionResult.FAIL; }
        var animal = type.create(server, EntitySpawnReason.SPAWN_ITEM_USE);
        if (animal == null) return InteractionResult.FAIL;
        var pos = hit.getBlockPos().above();
        animal.snapTo(pos.getX() + .5, pos.getY(), pos.getZ() + .5, player.getYRot() + 180, 0);
        if (!server.noCollision(animal)) { player.sendOverlayMessage(Component.literal("There's no room for a horse here.")); return InteractionResult.FAIL; }
        animal.finalizeSpawn(server, server.getCurrentDifficultyAt(pos), EntitySpawnReason.SPAWN_ITEM_USE, null);
        animal.setAge(0);
        if (animal instanceof Horse) Horses.assignBreed(animal, breed, server.getRandom());
        animal.tameWithName(player);
        server.addFreshEntity(animal);
        stack.consume(1, player);
        server.playSound(null, pos, SoundEvents.HORSE_AMBIENT, SoundSource.NEUTRAL, 1F, 1F);
        player.sendOverlayMessage(Component.literal("Your new " + Stalls.label(animal) + " is ready to ride."));
        return InteractionResult.SUCCESS_SERVER;
    }

    private Papers() {}
}
