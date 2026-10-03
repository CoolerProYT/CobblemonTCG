package com.coolerpromc.cobblemontcg.tcg.data;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.tcg.card.CardDefinition;
import com.coolerpromc.cobblemontcg.tcg.set.SetDefinition;
import com.google.gson.JsonElement;
import com.google.gson.JsonParser;
import com.mojang.serialization.Codec;
import com.mojang.serialization.JsonOps;
import net.minecraft.resources.FileToIdConverter;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.packs.resources.Resource;
import net.minecraft.server.packs.resources.ResourceManager;
import net.minecraft.server.packs.resources.SimplePreparableReloadListener;
import net.minecraft.util.profiling.ProfilerFiller;

import java.io.Reader;
import java.util.*;
import java.util.function.BiConsumer;

/**
 * Loads {@code tcg/sets/<set>.json} and {@code tcg/cards/<set>/<number>.json} from data packs.
 * A card in {@code data/foo/tcg/cards/bar/4.json} belongs to the set {@code foo:bar}.
 */
public class TcgDataReloadListener extends SimplePreparableReloadListener<TcgDataReloadListener.Loaded> {
    public static final ResourceLocation ID = Constants.id("tcg_data");

    private static final FileToIdConverter SETS = FileToIdConverter.json("tcg/sets");
    private static final FileToIdConverter CARDS = FileToIdConverter.json("tcg/cards");

    @Override
    protected Loaded prepare(ResourceManager resourceManager, ProfilerFiller profiler) {
        Map<ResourceLocation, SetDefinition> sets = new HashMap<>();
        readAll(resourceManager, SETS, SetDefinition.CODEC, sets::put);

        Map<ResourceLocation, Map<Integer, CardDefinition>> cards = new HashMap<>();
        readAll(resourceManager, CARDS, CardDefinition.CODEC, (id, card) -> {
            int slash = id.getPath().lastIndexOf('/');
            if (slash <= 0) {
                Constants.LOG.error("Card {} must be inside a set folder (tcg/cards/<set>/<number>.json)", id);
                return;
            }
            ResourceLocation setId = ResourceLocation.fromNamespaceAndPath(id.getNamespace(), id.getPath().substring(0, slash));
            CardDefinition previous = cards.computeIfAbsent(setId, k -> new TreeMap<>()).put(card.number(), card);
            if (previous != null) {
                Constants.LOG.warn("Duplicate card number {} in set {}, {} replaces {}", card.number(), setId, card.id(), previous.id());
            }
        });

        Map<ResourceLocation, List<CardDefinition>> cardLists = new HashMap<>();
        cards.forEach((setId, byNumber) -> cardLists.put(setId, List.copyOf(byNumber.values())));
        return new Loaded(sets, cardLists);
    }

    @Override
    protected void apply(Loaded loaded, ResourceManager resourceManager, ProfilerFiller profiler) {
        loaded.cards().keySet().stream()
                .filter(setId -> !loaded.sets().containsKey(setId))
                .forEach(setId -> Constants.LOG.warn("Found cards for unknown set {}, they will be ignored", setId));

        loaded.sets().forEach((setId, definition) -> {
            int count = loaded.cards().getOrDefault(setId, List.of()).size();
            if (count != definition.total()) {
                Constants.LOG.warn("Set {} declares {} cards but {} were loaded", setId, definition.total(), count);
            }
        });

        TcgDataManager.SERVER.replace(loaded.sets(), loaded.cards());
        Constants.LOG.info("Loaded {} TCG set(s)", loaded.sets().size());
    }

    private static <T> void readAll(ResourceManager resourceManager, FileToIdConverter converter, Codec<T> codec, BiConsumer<ResourceLocation, T> output) {
        for (Map.Entry<ResourceLocation, Resource> entry : converter.listMatchingResources(resourceManager).entrySet()) {
            ResourceLocation id = converter.fileToId(entry.getKey());
            try (Reader reader = entry.getValue().openAsReader()) {
                JsonElement json = JsonParser.parseReader(reader);
                codec.parse(JsonOps.INSTANCE, json)
                        .resultOrPartial(error -> Constants.LOG.error("Failed to parse {}: {}", entry.getKey(), error))
                        .ifPresent(value -> output.accept(id, value));
            } catch (Exception e) {
                Constants.LOG.error("Failed to read {}", entry.getKey(), e);
            }
        }
    }

    public record Loaded(Map<ResourceLocation, SetDefinition> sets, Map<ResourceLocation, List<CardDefinition>> cards) {
    }
}
