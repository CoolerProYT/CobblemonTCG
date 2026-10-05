package com.coolerpromc.cobblemontcg.reward;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.minecraft.util.ExtraCodecs;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Optional;

public record RewardConditions(Optional<Integer> minLevel, List<String> species, List<String> excludeSpecies, Optional<Boolean> shiny,
                               Optional<Integer> level, Optional<Boolean> firstCatch, Optional<Integer> dexEvery, Optional<Integer> dexPercent, boolean perPokemon) {
    public static final RewardConditions NONE = new RewardConditions(Optional.empty(), List.of(), List.of(), Optional.empty(), Optional.empty(), Optional.empty(), Optional.empty(), Optional.empty(), false);

    public static final Codec<RewardConditions> CODEC = RecordCodecBuilder.create(instance -> instance.group(
            Codec.INT.optionalFieldOf("min_level").forGetter(RewardConditions::minLevel),
            Codec.STRING.listOf().optionalFieldOf("species", List.of()).forGetter(RewardConditions::species),
            Codec.STRING.listOf().optionalFieldOf("exclude_species", List.of()).forGetter(RewardConditions::excludeSpecies),
            Codec.BOOL.optionalFieldOf("shiny").forGetter(RewardConditions::shiny),
            ExtraCodecs.POSITIVE_INT.optionalFieldOf("level").forGetter(RewardConditions::level),
            Codec.BOOL.optionalFieldOf("first_catch_of_species").forGetter(RewardConditions::firstCatch),
            ExtraCodecs.POSITIVE_INT.optionalFieldOf("dex_every").forGetter(RewardConditions::dexEvery),
            Codec.intRange(1, 100).optionalFieldOf("dex_percent").forGetter(RewardConditions::dexPercent),
            Codec.BOOL.optionalFieldOf("per_pokemon", false).forGetter(RewardConditions::perPokemon)
    ).apply(instance, RewardConditions::new));

    public boolean test(RewardContext context) {
        if (minLevel.isPresent() && context.level().map(l -> l < minLevel.get()).orElse(true)) {
            return false;
        }
        if (!species.isEmpty() && context.species().map(s -> !species.contains(s.toLowerCase(Locale.ROOT))).orElse(true)) {
            return false;
        }
        if (!excludeSpecies.isEmpty() && context.species().map(s -> excludeSpecies.contains(s.toLowerCase(Locale.ROOT))).orElse(false)) {
            return false;
        }
        if (shiny.isPresent() && !context.shiny().map(s -> s.equals(shiny.get())).orElse(false)) {
            return false;
        }
        if (level.isPresent() && context.level().map(l -> l < level.get()).orElse(true)) {
            return false;
        }
        if (level.isPresent() && context.previousLevel().map(previous -> previous >= level.get()).orElse(false)) {
            return false;
        }
        if (firstCatch.isPresent() && !context.firstCatch().map(f -> f.equals(firstCatch.get())).orElse(false)) {
            return false;
        }
        if (dexEvery.isPresent() && context.dexEntries().map(entries -> entries <= 0 || entries % dexEvery.get() != 0).orElse(true)) {
            return false;
        }
        return dexPercent.isEmpty() || reachedPercent(context, dexPercent.get());
    }

    private static boolean reachedPercent(RewardContext context, int percent) {
        if (context.dexEntries().isEmpty() || context.dexTotal().isEmpty() || context.dexTotal().get() <= 0) {
            return false;
        }
        return (long) context.dexEntries().get() * 100 >= (long) percent * context.dexTotal().get();
    }

    public boolean isMilestone() {
        return (level.isPresent() && !perPokemon) || dexEvery.isPresent() || dexPercent.isPresent() || firstCatch.orElse(false);
    }

    public Optional<String> milestone(RewardContext context) {
        if (!isMilestone()) {
            return Optional.empty();
        }
        List<String> parts = new ArrayList<>();
        if (!perPokemon) {
            level.ifPresent(l -> parts.add("level/" + l));
        }
        if (firstCatch.orElse(false)) {
            parts.add("first_catch/" + context.species().map(s -> s.toLowerCase(Locale.ROOT)).orElse("unknown"));
        }
        dexEvery.ifPresent(n -> parts.add("dex_every/" + n + "/" + context.dexEntries().orElse(0)));
        dexPercent.ifPresent(p -> parts.add("dex_percent/" + p));
        return Optional.of(String.join("+", parts));
    }
}
