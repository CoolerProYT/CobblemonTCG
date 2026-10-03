package com.coolerpromc.cobblemontcg.reward;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;

import java.util.List;
import java.util.Locale;
import java.util.Optional;

public record RewardConditions(Optional<Integer> minLevel, List<String> species, Optional<Boolean> shiny) {
    public static final RewardConditions NONE = new RewardConditions(Optional.empty(), List.of(), Optional.empty());

    public static final Codec<RewardConditions> CODEC = RecordCodecBuilder.create(instance -> instance.group(
            Codec.INT.optionalFieldOf("min_level").forGetter(RewardConditions::minLevel),
            Codec.STRING.listOf().optionalFieldOf("species", List.of()).forGetter(RewardConditions::species),
            Codec.BOOL.optionalFieldOf("shiny").forGetter(RewardConditions::shiny)
    ).apply(instance, RewardConditions::new));

    public boolean test(RewardContext context) {
        if (minLevel.isPresent() && context.level().map(level -> level < minLevel.get()).orElse(true)) {
            return false;
        }
        if (!species.isEmpty() && context.species().map(s -> !species.contains(s.toLowerCase(Locale.ROOT))).orElse(true)) {
            return false;
        }
        return shiny.isEmpty() || context.shiny().map(s -> s.equals(shiny.get())).orElse(false);
    }
}
