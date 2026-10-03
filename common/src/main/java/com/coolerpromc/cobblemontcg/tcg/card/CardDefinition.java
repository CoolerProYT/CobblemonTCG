package com.coolerpromc.cobblemontcg.tcg.card;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.minecraft.util.ExtraCodecs;

import java.util.Optional;

/**
 * One card as defined in {@code data/<namespace>/tcg/cards/<set>/<number>.json}.
 * The set a card belongs to comes from the folder it is in, not from the JSON.
 */
public record CardDefinition(String id, int number, String name, CardSupertype supertype, Optional<String> type, Optional<Integer> hp, CardRarity rarity) {
    public static final Codec<CardDefinition> CODEC = RecordCodecBuilder.create(instance -> instance.group(
            Codec.STRING.fieldOf("id").forGetter(CardDefinition::id),
            ExtraCodecs.POSITIVE_INT.fieldOf("number").forGetter(CardDefinition::number),
            Codec.STRING.fieldOf("name").forGetter(CardDefinition::name),
            CardSupertype.CODEC.fieldOf("supertype").forGetter(CardDefinition::supertype),
            Codec.STRING.optionalFieldOf("type").forGetter(CardDefinition::type),
            ExtraCodecs.POSITIVE_INT.optionalFieldOf("hp").forGetter(CardDefinition::hp),
            CardRarity.CODEC.fieldOf("rarity").forGetter(CardDefinition::rarity)
    ).apply(instance, CardDefinition::new));
}
