package com.coolerpromc.cobblemontcg.tcg.pack;

import com.coolerpromc.cobblemontcg.tcg.card.CardDefinition;
import com.coolerpromc.cobblemontcg.tcg.card.CardRarity;
import com.coolerpromc.cobblemontcg.tcg.set.PackSlot;
import com.coolerpromc.cobblemontcg.tcg.set.TcgSet;
import net.minecraft.util.RandomSource;

import java.util.*;

public class PackRoller {
    public static List<RolledCard> roll(TcgSet set, RandomSource random, double holoChance, int packSize) {
        List<PackSlot> slots = set.definition().packSlots();
        int[] counts = resize(slots, packSize);

        Set<CardDefinition> used = new HashSet<>();
        List<RolledCard> result = new ArrayList<>(packSize);
        for (int i = 0; i < slots.size(); i++) {
            PackSlot slot = slots.get(i);
            for (int n = 0; n < counts[i]; n++) {
                CardDefinition card = rollCard(set, slot, random, holoChance, used);
                if (card == null) {
                    break;
                }
                used.add(card);
                result.add(new RolledCard(card, card.rarity().isHolo()));
            }
        }
        return result;
    }

    static int[] resize(List<PackSlot> slots, int packSize) {
        int[] counts = slots.stream().mapToInt(PackSlot::count).toArray();
        if (counts.length == 0) {
            return counts;
        }
        int diff = Math.max(packSize, 0) - Arrays.stream(counts).sum();
        if (diff > 0) {
            counts[counts.length - 1] += diff;
        }
        for (int i = counts.length - 1; i >= 0 && diff < 0; i--) {
            int removed = Math.min(counts[i], -diff);
            counts[i] -= removed;
            diff += removed;
        }
        return counts;
    }

    private static CardDefinition rollCard(TcgSet set, PackSlot slot, RandomSource random, double holoChance, Set<CardDefinition> used) {
        Map<CardRarity, Double> weights = new EnumMap<>(CardRarity.class);
        slot.rarities().forEach((rarity, weight) -> {
            if (hasUnused(set, rarity, used)) {
                weights.put(rarity, (double) weight);
            }
        });
        if (weights.isEmpty()) {
            return null;
        }
        if (slot.useConfigHoloChance()) {
            applyHoloChance(weights, holoChance);
        }

        CardRarity rarity = pickWeighted(weights, random);
        List<CardDefinition> pool = set.cardsOfRarity(rarity).stream().filter(card -> !used.contains(card)).toList();
        return pool.get(random.nextInt(pool.size()));
    }

    private static void applyHoloChance(Map<CardRarity, Double> weights, double holoChance) {
        if (!weights.containsKey(CardRarity.RARE_HOLO)) {
            return;
        }
        double chance = Math.clamp(holoChance, 0.0, 1.0);
        double others = weights.entrySet().stream().filter(e -> e.getKey() != CardRarity.RARE_HOLO).mapToDouble(Map.Entry::getValue).sum();
        if (others <= 0) {
            return;
        }
        weights.replaceAll((rarity, weight) -> rarity == CardRarity.RARE_HOLO ? chance : (1.0 - chance) * weight / others);
    }

    private static CardRarity pickWeighted(Map<CardRarity, Double> weights, RandomSource random) {
        double total = weights.values().stream().mapToDouble(Double::doubleValue).sum();
        double roll = random.nextDouble() * total;
        CardRarity last = null;
        for (Map.Entry<CardRarity, Double> entry : weights.entrySet()) {
            if (entry.getValue() <= 0) {
                continue;
            }
            last = entry.getKey();
            roll -= entry.getValue();
            if (roll < 0) {
                return last;
            }
        }
        return last != null ? last : weights.keySet().iterator().next();
    }

    private static boolean hasUnused(TcgSet set, CardRarity rarity, Set<CardDefinition> used) {
        for (CardDefinition card : set.cardsOfRarity(rarity)) {
            if (!used.contains(card)) {
                return true;
            }
        }
        return false;
    }
}
