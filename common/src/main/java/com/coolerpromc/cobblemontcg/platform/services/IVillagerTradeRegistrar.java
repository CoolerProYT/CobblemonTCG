package com.coolerpromc.cobblemontcg.platform.services;

import net.minecraft.world.entity.npc.VillagerProfession;
import net.minecraft.world.entity.npc.VillagerTrades;

import java.util.function.Supplier;

/**
 * Trades are collected here and handed to each loader's trade hook ({@code TradeOfferHelper} on Fabric,
 * {@code VillagerTradesEvent} and {@code WandererTradesEvent} on NeoForge).
 */
public interface IVillagerTradeRegistrar {
    void registerVillagerTrade(Supplier<VillagerProfession> profession, int level, VillagerTrades.ItemListing listing);
    void applyVillagerTradeRegistrations(VillagerTradeRegistrar registrar);
    /**
     * @param rare whether the listing joins the rare pool (one offer per trader) instead of the generic pool
     */
    void registerWanderingTrade(boolean rare, VillagerTrades.ItemListing listing);
    void applyWanderingTradeRegistrations(WanderingTradeRegistrar registrar);

    interface VillagerTradeRegistrar {
        void register(VillagerProfession profession, int level, VillagerTrades.ItemListing listing);
    }

    interface WanderingTradeRegistrar {
        void register(boolean rare, VillagerTrades.ItemListing listing);
    }
}
