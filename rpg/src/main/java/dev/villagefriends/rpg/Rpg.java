package dev.villagefriends.rpg;

import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.attachment.v1.AttachmentRegistry;
import net.fabricmc.fabric.api.attachment.v1.AttachmentSyncPredicate;
import net.fabricmc.fabric.api.attachment.v1.AttachmentTarget;
import net.fabricmc.fabric.api.attachment.v1.AttachmentType;
import net.fabricmc.fabric.api.command.v2.CommandRegistrationCallback;
import net.fabricmc.fabric.api.entity.event.v1.ServerLivingEntityEvents;
import net.fabricmc.fabric.api.entity.event.v1.ServerPlayerEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.fabricmc.fabric.api.event.player.PlayerBlockBreakEvents;
import net.fabricmc.fabric.api.networking.v1.PayloadTypeRegistry;
import net.fabricmc.fabric.api.networking.v1.ServerPlayConnectionEvents;
import net.fabricmc.fabric.api.networking.v1.ServerPlayNetworking;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.player.Player;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/** Village Friends RPG: levels, attributes, skills, monster masteries and villager quests. */
public final class Rpg implements ModInitializer {
    public static final String ID = "villagefriends_rpg";
    public static final Logger LOGGER = LoggerFactory.getLogger("Village Friends RPG");
    public static Identifier id(String path) { return Identifier.fromNamespaceAndPath(ID, path); }

    /** The character sheet: saved with the player, kept through death, synced only to its owner. */
    public static final AttachmentType<Sheet> SHEET = AttachmentRegistry.create(id("sheet"), b -> b.persistent(Sheet.CODEC)
            .copyOnDeath().syncWith(ByteBufCodecs.fromCodec(Sheet.CODEC), AttachmentSyncPredicate.targetOnly()));

    public static Sheet sheet(Player p) { var s = ((AttachmentTarget) p).getAttached(SHEET); return s == null ? Sheet.NEW : s; }
    public static void set(ServerPlayer p, Sheet s) { ((AttachmentTarget) p).setAttached(SHEET, s); }

    @Override public void onInitialize() {
        RpgConfig.load();
        PayloadTypeRegistry.serverboundPlay().register(RpgActionPayload.TYPE, RpgActionPayload.CODEC);
        ServerPlayNetworking.registerGlobalReceiver(RpgActionPayload.TYPE, (payload, context) -> Life.action(context.player(), payload));
        ServerTickEvents.END_SERVER_TICK.register(Life::tick);
        ServerPlayConnectionEvents.JOIN.register((handler, sender, server) -> Life.joined(handler.getPlayer()));
        ServerPlayerEvents.AFTER_RESPAWN.register(Life::respawned);
        ServerLivingEntityEvents.ALLOW_DAMAGE.register(Hunt::allowDamage);
        ServerLivingEntityEvents.AFTER_DAMAGE.register(Hunt::afterDamage);
        ServerLivingEntityEvents.ALLOW_DEATH.register(Hunt::allowDeath);
        ServerLivingEntityEvents.AFTER_DEATH.register(Hunt::died);
        PlayerBlockBreakEvents.AFTER.register(Hunt::broke);
        CommandRegistrationCallback.EVENT.register((dispatcher, registry, env) -> RpgCommands.register(dispatcher));
        ServerLifecycleEvents.SERVER_STOPPED.register(server -> { Life.clear(); Hunt.clear(); Quests.clear(); });
        Cooking.register();
        // Development check (-Dvillagefriends_rpg.audit=true): apply every mixin once the server is up, then stop.
        if (Boolean.getBoolean("villagefriends_rpg.audit")) ServerLifecycleEvents.SERVER_STARTED.register(server -> {
            org.spongepowered.asm.mixin.MixinEnvironment.getCurrentEnvironment().audit();
            LOGGER.info("RPG audit finished");
            server.halt(false);
        });
        LOGGER.info("Village Friends RPG ready: {} attributes, {} skills, {} monster families.", Attr.values().length, Skill.values().length, Bestiary.FAMILIES.size());
    }
}
