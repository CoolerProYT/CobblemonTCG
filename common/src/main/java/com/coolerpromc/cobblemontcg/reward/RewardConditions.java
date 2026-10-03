package com.coolerpromc.cobblemontcg.reward;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.minecraft.util.ExtraCodecs;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Optional;

/**
 * Conditions a {@link RewardRule} checks against a {@link RewardContext}.
 * <p>
 * {@code level}, {@code dex_every}, {@code dex_percent} and {@code first_catch_of_species: true} make the rule
 * a milestone: it pays out at most once per player for each milestone it reaches (see {@link #milestone}).
 *
 * @param level              milestone: a Pokémon reached at least this level
 * @param firstCatch         whether the capture must (or must not) be the player's first of the species
 * @param dexEvery           milestone: the player's Pokédex entry count is a multiple of this
 * @param dexPercent         milestone: the player has at least this percentage of the Pokédex
 */
public record RewardConditions(Optional<Integer> minLevel, List<String> species, Optional<Boolean> shiny,
                               Optional<Integer> level, Optional<Boolean> firstCatch, Optional<Integer> dexEvery, Optional<Integer> dexPercent) {
    public static final RewardConditions NONE = new RewardConditions(Optional.empty(), List.of(), Optional.empty(), Optional.empty(), Optional.empty(), Optional.empty(), Optional.empty());

    public static final Codec<RewardConditions> CODEC = RecordCodecBuilder.create(instance -> instance.group(
            Codec.INT.optionalFieldOf("min_level").forGetter(RewardConditions::minLevel),
            Codec.STRING.listOf().optionalFieldOf("species", List.of()).forGetter(RewardConditions::species),
            Codec.BOOL.optionalFieldOf("shiny").forGetter(RewardConditions::shiny),
            ExtraCodecs.POSITIVE_INT.optionalFieldOf("level").forGetter(RewardConditions::level),
            Codec.BOOL.optionalFieldOf("first_catch_of_species").forGetter(RewardConditions::firstCatch),
            ExtraCodecs.POSITIVE_INT.optionalFieldOf("dex_every").forGetter(RewardConditions::dexEvery),
            Codec.intRange(1, 100).optionalFieldOf("dex_percent").forGetter(RewardConditions::dexPercent)
    ).apply(instance, RewardConditions::new));

    public boolean test(RewardContext context) {
        if (minLevel.isPresent() && context.level().map(l -> l < minLevel.get()).orElse(true)) {
            return false;
        }
        if (!species.isEmpty() && context.species().map(s -> !species.contains(s.toLowerCase(Locale.ROOT))).orElse(true)) {
            return false;
        }
        if (shiny.isPresent() && !context.shiny().map(s -> s.equals(shiny.get())).orElse(false)) {
            return false;
        }
        if (level.isPresent() && context.level().map(l -> l < level.get()).orElse(true)) {
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
        return level.isPresent() || dexEvery.isPresent() || dexPercent.isPresent() || firstCatch.orElse(false);
    }

    /**
     * The id of the milestone this rule reaches for the context (only meaningful when {@link #test} passed),
     * or empty if the rule is not a milestone and may pay out every time.
     */
    public Optional<String> milestone(RewardContext context) {
        if (!isMilestone()) {
            return Optional.empty();
        }
        List<String> parts = new ArrayList<>();
        level.ifPresent(l -> parts.add("level/" + l));
        if (firstCatch.orElse(false)) {
            parts.add("first_catch/" + context.species().map(s -> s.toLowerCase(Locale.ROOT)).orElse("unknown"));
        }
        dexEvery.ifPresent(n -> parts.add("dex_every/" + n + "/" + context.dexEntries().orElse(0)));
        dexPercent.ifPresent(p -> parts.add("dex_percent/" + p));
        return Optional.of(String.join("+", parts));
    }
}
