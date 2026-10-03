package com.coolerpromc.cobblemontcg.platform;

import com.coolerpromc.cobblemontcg.platform.services.IVillagerTradeRegistrar;
import net.minecraft.world.entity.npc.VillagerProfession;
import net.minecraft.world.entity.npc.VillagerTrades;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Supplier;

/**
 * Trades are collected once and handed to every {@code VillagerTradesEvent}, which fires on each server start.
 */
public class NeoForgeVillagerTradeRegistrar implements IVillagerTradeRegistrar {
    private final List<VillagerTradeEntry> villagerTrades = new ArrayList<>();

    @Override
    public void registerVillagerTrade(Supplier<VillagerProfession> profession, int level, VillagerTrades.ItemListing listing) {
        this.villagerTrades.add(new VillagerTradeEntry(profession, level, listing));
    }

    @Override
    public void applyVillagerTradeRegistrations(VillagerTradeRegistrar registrar) {
        for (VillagerTradeEntry entry : villagerTrades) {
            registrar.register(entry.profession().get(), entry.level(), entry.listing());
        }
    }

    private record VillagerTradeEntry(Supplier<VillagerProfession> profession, int level, VillagerTrades.ItemListing listing) {
    }
}
