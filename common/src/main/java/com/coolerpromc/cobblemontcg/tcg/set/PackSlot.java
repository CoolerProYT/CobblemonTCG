package com.coolerpromc.cobblemontcg.tcg.set;

import com.coolerpromc.cobblemontcg.tcg.card.CardRarity;
import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.minecraft.util.ExtraCodecs;

import java.util.Map;

/**
 * A group of cards in a booster pack. Each of the {@code count} cards first rolls a rarity from the
 * {@code rarities} weight table, then a card of that rarity.
 * When {@code use_config_holo_chance} is set, the chance of rolling {@link CardRarity#RARE_HOLO}
 * comes from the config instead of the weight table.
 */
public record PackSlot(int count, Map<CardRarity, Integer> rarities, boolean useConfigHoloChance) {
    public static final Codec<PackSlot> CODEC = RecordCodecBuilder.create(instance -> instance.group(
            ExtraCodecs.POSITIVE_INT.fieldOf("count").forGetter(PackSlot::count),
            Codec.unboundedMap(CardRarity.CODEC, ExtraCodecs.POSITIVE_INT).fieldOf("rarities").forGetter(PackSlot::rarities),
            Codec.BOOL.optionalFieldOf("use_config_holo_chance", false).forGetter(PackSlot::useConfigHoloChance)
    ).apply(instance, PackSlot::new));
}
