package com.coolerpromc.cobblemontcg.tcg.data;

import com.coolerpromc.cobblemontcg.tcg.card.CardDefinition;
import com.coolerpromc.cobblemontcg.tcg.set.SetDefinition;
import com.coolerpromc.cobblemontcg.tcg.set.TcgSet;
import net.minecraft.resources.ResourceLocation;

import java.util.*;

public class TcgDataManager {
    public static final TcgDataManager SERVER = new TcgDataManager();
    public static final TcgDataManager CLIENT = new TcgDataManager();

    private volatile Map<ResourceLocation, TcgSet> sets = Map.of();
    private volatile Map<ResourceLocation, SetDefinition> rawSets = Map.of();
    private volatile Map<ResourceLocation, List<CardDefinition>> rawCards = Map.of();
    private final List<Runnable> listeners = new ArrayList<>();

    public static TcgDataManager get(boolean clientSide) {
        return clientSide ? CLIENT : SERVER;
    }

    public static TcgDataManager forDisplay() {
        return CLIENT.sets.isEmpty() ? SERVER : CLIENT;
    }

    public synchronized void addListener(Runnable listener) {
        listeners.add(listener);
    }

    public void replace(Map<ResourceLocation, SetDefinition> setDefinitions, Map<ResourceLocation, List<CardDefinition>> cards) {
        Map<ResourceLocation, TcgSet> built = new TreeMap<>();
        setDefinitions.forEach((id, definition) -> built.put(id, new TcgSet(id, definition, cards.getOrDefault(id, List.of()))));

        this.rawSets = Map.copyOf(setDefinitions);
        this.rawCards = Map.copyOf(cards);
        this.sets = Collections.unmodifiableMap(built);

        List<Runnable> toRun;
        synchronized (this) {
            toRun = List.copyOf(listeners);
        }
        toRun.forEach(Runnable::run);
    }

    public Collection<TcgSet> sets() {
        return sets.values();
    }

    public Set<ResourceLocation> setIds() {
        return sets.keySet();
    }

    public Optional<TcgSet> set(ResourceLocation id) {
        return Optional.ofNullable(sets.get(id));
    }

    public Optional<CardDefinition> card(ResourceLocation setId, int number) {
        return set(setId).flatMap(set -> set.card(number));
    }

    public Map<ResourceLocation, SetDefinition> rawSets() {
        return rawSets;
    }

    public Map<ResourceLocation, List<CardDefinition>> rawCards() {
        return rawCards;
    }
}
