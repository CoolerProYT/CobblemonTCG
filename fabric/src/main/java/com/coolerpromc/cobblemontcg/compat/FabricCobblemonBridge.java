package com.coolerpromc.cobblemontcg.compat;

import com.cobblemon.mod.common.Cobblemon;
import com.cobblemon.mod.common.api.Priority;
import com.cobblemon.mod.common.api.events.CobblemonEvents;
import com.cobblemon.mod.common.api.events.pokemon.LevelUpEvent;
import com.cobblemon.mod.common.api.events.pokemon.PokedexDataChangedEvent;
import com.cobblemon.mod.common.api.events.pokemon.PokemonCapturedEvent;
import com.cobblemon.mod.common.api.pokedex.AbstractPokedexManager;
import com.cobblemon.mod.common.api.pokedex.PokedexEntryProgress;
import com.cobblemon.mod.common.api.pokedex.SpeciesDexRecord;
import com.cobblemon.mod.common.api.pokedex.entry.DexEntries;
import com.cobblemon.mod.common.api.pokedex.entry.PokedexEntry;
import com.cobblemon.mod.common.pokemon.Pokemon;
import com.coolerpromc.cobblemontcg.reward.trigger.PokemonRewardTriggers;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import java.util.stream.Collectors;

/**
 * Turns Cobblemon's events into the Pokémon reward triggers, set up by {@code FabricCobblemonTCG};
 * written against Cobblemon 1.8.1.
 * <p>
 * Cobblemon adds a caught Pokémon to the party, which updates the Pokédex, before it posts
 * {@code POKEMON_CAPTURED}. So a new species is spotted on the Pokédex change (its knowledge goes to
 * {@code OWNED}) and remembered for that tick, and the capture that follows in the same tick is the first catch.
 */
public final class FabricCobblemonBridge {
    private static final Map<UUID, ResourceLocation> PENDING_NEW_SPECIES = new HashMap<>();
    private static final Map<UUID, NewSpecies> NEW_SPECIES = new HashMap<>();

    private FabricCobblemonBridge() {
    }

    public static void init() {
        PokemonRewardTriggers.register();
        CobblemonEvents.POKEDEX_DATA_CHANGED_PRE.subscribe(Priority.LOWEST, FabricCobblemonBridge::onPokedexChangePre);
        CobblemonEvents.POKEDEX_DATA_CHANGED_POST.subscribe(Priority.NORMAL, FabricCobblemonBridge::onPokedexChangePost);
        CobblemonEvents.POKEMON_CAPTURED.subscribe(Priority.NORMAL, FabricCobblemonBridge::onCapture);
        CobblemonEvents.LEVEL_UP_EVENT.subscribe(Priority.LOWEST, FabricCobblemonBridge::onLevelUp);
    }

    private static void onPokedexChangePre(PokedexDataChangedEvent.Pre event) {
        SpeciesDexRecord species = event.getRecord().getSpeciesDexRecord();
        if (event.getKnowledge() == PokedexEntryProgress.OWNED && species.getKnowledge() != PokedexEntryProgress.OWNED) {
            PENDING_NEW_SPECIES.put(event.getPlayerUUID(), species.getId());
        }
    }

    private static void onPokedexChangePost(PokedexDataChangedEvent.Post event) {
        SpeciesDexRecord species = event.getRecord().getSpeciesDexRecord();
        ResourceLocation pending = PENDING_NEW_SPECIES.remove(event.getPlayerUUID());
        if (!species.getId().equals(pending) || species.getKnowledge() != PokedexEntryProgress.OWNED) {
            return;
        }
        MinecraftServer server = Cobblemon.INSTANCE.getImplementation().server();
        ServerPlayer player = server == null ? null : server.getPlayerList().getPlayer(event.getPlayerUUID());
        if (player == null) {
            return;
        }
        NEW_SPECIES.put(player.getUUID(), new NewSpecies(species.getId(), server.getTickCount()));
        PokemonRewardTriggers.onDexProgress(player, species.getId().getPath(), caughtSpecies(event.getPokedexManager()), totalSpecies());
    }

    private static void onCapture(PokemonCapturedEvent event) {
        ServerPlayer player = event.getPlayer();
        Pokemon pokemon = event.getPokemon();
        ResourceLocation species = pokemon.getSpecies().getResourceIdentifier();
        NewSpecies added = NEW_SPECIES.remove(player.getUUID());
        boolean firstCatch = added != null && added.species().equals(species) && added.tick() == player.server.getTickCount();
        PokemonRewardTriggers.onCapture(player, species.getPath(), pokemon.getLevel(), pokemon.getShiny(), firstCatch);
    }

    private static void onLevelUp(LevelUpEvent event) {
        Pokemon pokemon = event.getPokemon();
        ServerPlayer owner = pokemon.getOwnerPlayer();
        if (owner == null || event.getNewLevel() <= event.getOldLevel()) {
            return;
        }
        PokemonRewardTriggers.onLevelUp(owner, pokemon.getSpecies().getResourceIdentifier().getPath(), event.getNewLevel(), pokemon.getShiny());
    }

    /** Same count as Cobblemon's {@code CaughtCount}: species the player owns. */
    private static int caughtSpecies(AbstractPokedexManager pokedex) {
        return (int) pokedex.getSpeciesRecords().values().stream()
                .filter(record -> record.getKnowledge() == PokedexEntryProgress.OWNED)
                .count();
    }

    /** Same total as Cobblemon's {@code CaughtPercent}: distinct species across all Pokédex entries. */
    private static int totalSpecies() {
        Set<ResourceLocation> species = DexEntries.INSTANCE.getEntries().values().stream()
                .map(PokedexEntry::getSpeciesId)
                .collect(Collectors.toSet());
        return species.size();
    }

    private record NewSpecies(ResourceLocation species, int tick) {
    }
}
