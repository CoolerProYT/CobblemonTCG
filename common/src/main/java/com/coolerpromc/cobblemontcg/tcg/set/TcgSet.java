package com.coolerpromc.cobblemontcg.tcg.set;

import com.coolerpromc.cobblemontcg.tcg.card.CardDefinition;
import com.coolerpromc.cobblemontcg.tcg.card.CardRarity;
import net.minecraft.resources.ResourceLocation;

import java.util.*;

/**
 * A loaded set together with its cards, indexed for lookups and pack rolls.
 */
public final class TcgSet {
    private final ResourceLocation id;
    private final SetDefinition definition;
    private final List<CardDefinition> cards;
    private final Map<Integer, CardDefinition> byNumber;
    private final Map<CardRarity, List<CardDefinition>> byRarity;

    public TcgSet(ResourceLocation id, SetDefinition definition, Collection<CardDefinition> cards) {
        this.id = id;
        this.definition = definition;
        this.cards = cards.stream().sorted(Comparator.comparingInt(CardDefinition::number)).toList();

        Map<Integer, CardDefinition> numbers = new LinkedHashMap<>();
        Map<CardRarity, List<CardDefinition>> rarities = new EnumMap<>(CardRarity.class);
        for (CardDefinition card : this.cards) {
            numbers.put(card.number(), card);
            rarities.computeIfAbsent(card.rarity(), r -> new ArrayList<>()).add(card);
        }
        rarities.replaceAll((rarity, list) -> List.copyOf(list));

        this.byNumber = Collections.unmodifiableMap(numbers);
        this.byRarity = Collections.unmodifiableMap(rarities);
    }

    public ResourceLocation id() {
        return id;
    }

    public SetDefinition definition() {
        return definition;
    }

    public List<CardDefinition> cards() {
        return cards;
    }

    public Optional<CardDefinition> card(int number) {
        return Optional.ofNullable(byNumber.get(number));
    }

    public List<CardDefinition> cardsOfRarity(CardRarity rarity) {
        return byRarity.getOrDefault(rarity, List.of());
    }

    /**
     * The {@code custom_model_data} value for a booster pack wrapper: the set's base plus the
     * wrapper's position in {@code wrappers}. Packs are a different item from cards, so the ranges never clash.
     */
    public int packModelData(String wrapper) {
        return definition.modelDataBase() + Math.max(0, definition.wrappers().indexOf(wrapper));
    }

    public List<String> wrappers() {
        return definition.wrappers().isEmpty() ? List.of(SetDefinition.DEFAULT_WRAPPER) : definition.wrappers();
    }

    /**
     * The {@code custom_model_data} value for a card of this set. Every card number gets two values:
     * an even one for the regular print and the next odd one for the holo print.
     */
    public int modelData(int number, boolean holo) {
        return definition.modelDataBase() + number * 2 + (holo ? 1 : 0);
    }
}
