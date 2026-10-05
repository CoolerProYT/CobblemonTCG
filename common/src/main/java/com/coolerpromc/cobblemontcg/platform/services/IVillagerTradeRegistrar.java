package com.coolerpromc.cobblemontcg.platform.services;

import net.minecraft.world.entity.npc.VillagerProfession;
import net.minecraft.world.entity.npc.VillagerTrades;

import java.util.function.Supplier;

public interface IVillagerTradeRegistrar {
    void registerVillagerTrade(Supplier<VillagerProfession> profession, int level, VillagerTrades.ItemListing listing);
    void applyVillagerTradeRegistrations(VillagerTradeRegistrar registrar);
    void registerWanderingTrade(boolean rare, VillagerTrades.ItemListing listing);
    void applyWanderingTradeRegistrations(WanderingTradeRegistrar registrar);

    interface VillagerTradeRegistrar {
        void register(VillagerProfession profession, int level, VillagerTrades.ItemListing listing);
    }

    interface WanderingTradeRegistrar {
        void register(boolean rare, VillagerTrades.ItemListing listing);
    }
}
