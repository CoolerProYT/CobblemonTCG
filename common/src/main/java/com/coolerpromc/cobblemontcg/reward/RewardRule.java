package com.coolerpromc.cobblemontcg.reward;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.ExtraCodecs;

/**
 * One entry from {@code data/<namespace>/tcg/rewards/*.json}: when {@code trigger} fires and the
 * conditions pass, give {@code amount} packs of {@code set} with probability {@code chance}.
 */
public record RewardRule(ResourceLocation trigger, ResourceLocation set, int amount, float chance, RewardConditions conditions) {
    public static final Codec<RewardRule> CODEC = RecordCodecBuilder.create(instance -> instance.group(
            ResourceLocation.CODEC.fieldOf("trigger").forGetter(RewardRule::trigger),
            ResourceLocation.CODEC.fieldOf("set").forGetter(RewardRule::set),
            ExtraCodecs.POSITIVE_INT.optionalFieldOf("amount", 1).forGetter(RewardRule::amount),
            Codec.floatRange(0.0F, 1.0F).optionalFieldOf("chance", 1.0F).forGetter(RewardRule::chance),
            RewardConditions.CODEC.optionalFieldOf("conditions", RewardConditions.NONE).forGetter(RewardRule::conditions)
    ).apply(instance, RewardRule::new));
}
