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

/**
 * Emerald trades for booster packs. Config is read when an offer is generated, so a change applies to
 * villagers that get new offers after it (existing offers keep their price and stock).
 */
public final class PackTrades {
    private static final int CARD_DEALER_XP = 2;
    private static final float PRICE_MULTIPLIER = 0.05F;

    private PackTrades() {
    }

    public static void init() {
        Services.VILLAGER_TRADES.registerVillagerTrade(ModVillagers.CARD_DEALER, 1, (trader, random) ->
                TcgConfig.cardDealerEnabled() ? packOffer(TcgConfig.cardDealerPrice(), TcgConfig.cardDealerMaxUses(), CARD_DEALER_XP, random) : null);
    }

    /**
     * @return an offer of one pack of the configured shop set for {@code price} emeralds, or {@code null}
     * (vanilla skips the offer) when that set is not loaded
     */
    @Nullable
    public static MerchantOffer packOffer(int price, int maxUses, int villagerXp, RandomSource random) {
        Optional<TcgSet> set = shopSet();
        if (set.isEmpty()) {
            return null;
        }
        // like reward packs, the wrapper is random
        List<String> wrappers = set.get().wrappers();
        String wrapper = wrappers.get(random.nextInt(wrappers.size()));
        return new MerchantOffer(new ItemCost(Items.EMERALD, price), TcgStacks.pack(set.get(), wrapper, 1), maxUses, villagerXp, PRICE_MULTIPLIER);
    }

    private static Optional<TcgSet> shopSet() {
        ResourceLocation id = ResourceLocation.tryParse(TcgConfig.shopSetId());
        Optional<TcgSet> set = id == null ? Optional.empty() : TcgDataManager.SERVER.set(id);
        if (set.isEmpty()) {
            Constants.LOG.warn("Shop set '{}' is not loaded, skipping the booster pack trade", TcgConfig.shopSetId());
        }
        return set;
    }
}
