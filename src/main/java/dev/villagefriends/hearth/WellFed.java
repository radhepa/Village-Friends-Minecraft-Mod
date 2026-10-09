package dev.villagefriends.hearth;

import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.minecraft.core.Holder;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectCategory;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.consume_effects.ConsumeEffect;
import net.minecraft.world.level.Level;

/**
 * Well Fed I-III, the buff a proper meal gives: hunger drains 15/25/35% slower, and at II and III you mend
 * half a heart every 12 or 8 seconds. It is short (two to four minutes) and never stacks: a better meal
 * replaces a lesser one and the same tier only tops the time up, as vanilla effects do.
 */
public final class WellFed extends MobEffect {
    public static Holder<MobEffect> EFFECT;
    public static ConsumeEffect.Type<OnEat> ON_EAT;

    WellFed() { super(MobEffectCategory.BENEFICIAL, 0xE8A33C); }

    static void register() {
        EFFECT = Registry.registerForHolder(BuiltInRegistries.MOB_EFFECT, Hearth.id("well_fed"), new WellFed());
        ON_EAT = Registry.register(BuiltInRegistries.CONSUME_EFFECT_TYPE, Hearth.id("well_fed"), new ConsumeEffect.Type<>(OnEat.CODEC, OnEat.STREAM_CODEC));
    }

    @Override public boolean shouldApplyEffectTickThisTick(int duration, int amplifier) {
        int every = Tastes.MEND_EVERY[Math.clamp(amplifier, 0, 2)];
        return every > 0 && duration % every == 0;
    }
    @Override public boolean applyEffectTick(ServerLevel level, LivingEntity entity, int amplifier) {
        if (entity.getHealth() < entity.getMaxHealth()) entity.heal(1.0F);
        return true;
    }

    /** How much exhaustion a player with Well Fed actually takes. */
    public static float exhaustion(Player player, float amount) {
        if (EFFECT == null) return amount;
        var effect = player.getEffect(EFFECT);
        return effect == null ? amount : (float) (amount * Tastes.hungerFactor(effect.getAmplifier()));
    }

    /** The consume effect every dish carries: Well Fed of its tier, for its time (longer for fine dishes and good cooks). */
    public record OnEat(int tier, int seconds) implements ConsumeEffect {
        public static final MapCodec<OnEat> CODEC = RecordCodecBuilder.mapCodec(i -> i.group(
                com.mojang.serialization.Codec.INT.fieldOf("tier").forGetter(OnEat::tier),
                com.mojang.serialization.Codec.INT.fieldOf("seconds").forGetter(OnEat::seconds)).apply(i, OnEat::new));
        public static final StreamCodec<RegistryFriendlyByteBuf, OnEat> STREAM_CODEC = StreamCodec.composite(
                ByteBufCodecs.VAR_INT, OnEat::tier, ByteBufCodecs.VAR_INT, OnEat::seconds, OnEat::new);

        @Override public Type<? extends ConsumeEffect> getType() { return ON_EAT; }
        @Override public boolean apply(Level level, ItemStack stack, LivingEntity entity) {
            if (level.isClientSide() || tier < 1) return false;
            var dish = Dishes.get(BuiltInRegistries.ITEM.getKey(stack.getItem()).toString());
            boolean fine = HearthApi.isFine(stack);
            double bonus = dish != null && entity instanceof ServerPlayer p ? HearthEvents.EATEN.invoker().wellFedFactor(p, dish, stack) : 1;
            int ticks = (int) Math.round(seconds * 20 * (fine ? Tastes.FINE_DURATION : 1) * Math.max(0, bonus));
            if (ticks <= 0) return false;
            return entity.addEffect(new MobEffectInstance(EFFECT, ticks, Math.clamp(tier - 1, 0, 2), false, true, true), entity);
        }
    }
}
