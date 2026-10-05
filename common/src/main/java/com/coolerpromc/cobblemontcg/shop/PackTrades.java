package com.coolerpromc.cobblemontcg.shop;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.config.TcgConfig;
import com.coolerpromc.cobblemontcg.platform.Services;
import com.coolerpromc.cobblemontcg.tcg.data.TcgDataManager;
import com.coolerpromc.cobblemontcg.tcg.set.TcgSet;
import com.coolerpromc.cobblemontcg.util.TcgStacks;
import com.coolerpromc.cobblemontcg.villager.ModVillagers;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.RandomSource;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.trading.ItemCost;
import net.minecraft.world.item.trading.MerchantOffer;
import org.jetbrains.annotations.Nullable;

import java.util.List;
import java.util.Optional;

public class PackTrades {
    public static final int MAX_LEVEL = 5;
    private static final int CARD_DEALER_XP = 2;
    private static final int WANDERING_TRADER_XP = 1;
    private static final float PRICE_MULTIPLIER = 0.05F;

    public static void init() {
        for (int level = 1; level <= MAX_LEVEL; level++) {
            int index = level - 1;
            Services.VILLAGER_TRADES.registerVillagerTrade(ModVillagers.CARD_DEALER, level, (trader, random) -> cardDealerOffer(index, random));
        }
        Services.VILLAGER_TRADES.registerWanderingTrade(false, (trader, random) -> wanderingTraderOffer(random));
    }

    @Nullable
    public static MerchantOffer cardDealerOffer(int index, RandomSource random) {
        List<String> sets = TcgConfig.shopSets();
        if (!TcgConfig.cardDealerEnabled() || index >= sets.size()) {
            return null;
        }
        return packOffer(sets.get(index), TcgConfig.cardDealerPrice(), TcgConfig.cardDealerMaxUses(), CARD_DEALER_XP, random);
    }

    @Nullable
    public static MerchantOffer wanderingTraderOffer(RandomSource random) {
        List<String> sets = TcgConfig.shopSets();
        if (!TcgConfig.wanderingTraderEnabled() || sets.isEmpty()) {
            return null;
        }
        String setId = sets.get(random.nextInt(sets.size()));
        return packOffer(setId, TcgConfig.wanderingTraderPrice(), TcgConfig.wanderingTraderMaxUses(), WANDERING_TRADER_XP, random);
    }

    @Nullable
    public static MerchantOffer packOffer(String setId, int price, int maxUses, int villagerXp, RandomSource random) {
        Optional<TcgSet> set = loadedSet(setId);
        if (set.isEmpty()) {
            return null;
        }
        List<String> wrappers = set.get().wrappers();
        String wrapper = wrappers.get(random.nextInt(wrappers.size()));
        return new MerchantOffer(new ItemCost(Items.EMERALD, price), TcgStacks.pack(set.get(), wrapper, 1), maxUses, villagerXp, PRICE_MULTIPLIER);
    }

    private static Optional<TcgSet> loadedSet(String setId) {
        ResourceLocation id = ResourceLocation.tryParse(setId);
        Optional<TcgSet> set = id == null ? Optional.empty() : TcgDataManager.SERVER.set(id);
        if (set.isEmpty()) {
            Constants.LOG.warn("Shop set '{}' is not loaded, skipping the booster pack trade", setId);
        }
        return set;
    }
}
