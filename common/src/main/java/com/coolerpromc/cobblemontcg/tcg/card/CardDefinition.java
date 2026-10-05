package com.coolerpromc.cobblemontcg.tcg.card;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.minecraft.util.ExtraCodecs;

import java.util.Optional;

public record CardDefinition(String id, int number, String name, CardSupertype supertype, Optional<String> type, Optional<Integer> hp, CardRarity rarity,
                             Optional<Integer> pokedex, Optional<Integer> evolvesFromPokedex) {
    public static final Codec<CardDefinition> CODEC = RecordCodecBuilder.create(instance -> instance.group(
            Codec.STRING.fieldOf("id").forGetter(CardDefinition::id),
            ExtraCodecs.POSITIVE_INT.fieldOf("number").forGetter(CardDefinition::number),
            Codec.STRING.fieldOf("name").forGetter(CardDefinition::name),
            CardSupertype.CODEC.fieldOf("supertype").forGetter(CardDefinition::supertype),
            Codec.STRING.optionalFieldOf("type").forGetter(CardDefinition::type),
            ExtraCodecs.POSITIVE_INT.optionalFieldOf("hp").forGetter(CardDefinition::hp),
            CardRarity.CODEC.fieldOf("rarity").forGetter(CardDefinition::rarity),
            ExtraCodecs.POSITIVE_INT.optionalFieldOf("pokedex").forGetter(CardDefinition::pokedex),
            ExtraCodecs.POSITIVE_INT.optionalFieldOf("evolves_from_pokedex").forGetter(CardDefinition::evolvesFromPokedex)
    ).apply(instance, CardDefinition::new));
}
