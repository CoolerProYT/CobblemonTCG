package com.coolerpromc.cobblemontcg.platform.services;

import net.minecraft.world.entity.npc.VillagerProfession;
import net.minecraft.world.entity.npc.VillagerTrades;

import java.util.function.Supplier;

/**
 * Trades are collected here and handed to each loader's trade hook ({@code TradeOfferHelper} on Fabric,
 * {@code VillagerTradesEvent} on NeoForge).
 */
public interface IVillagerTradeRegistrar {
    void registerVillagerTrade(Supplier<VillagerProfession> profession, int level, VillagerTrades.ItemListing listing);
    void applyVillagerTradeRegistrations(VillagerTradeRegistrar registrar);

    interface VillagerTradeRegistrar {
        void register(VillagerProfession profession, int level, VillagerTrades.ItemListing listing);
    }
}
