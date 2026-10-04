package com.coolerpromc.cobblemontcg.config;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.coolerconfig.config.ConfigBuilder;
import com.coolerpromc.coolerconfig.config.ConfigFormat;
import com.coolerpromc.coolerconfig.config.ConfigSpec;
import com.coolerpromc.coolerconfig.config.ConfigValue;
import net.minecraft.resources.ResourceLocation;

import java.util.List;

/**
 * The one place config values are read from. Getters return the defaults until {@link #init()} has run.
 */
public final class TcgConfig {
    public static final double DEFAULT_HOLO_CHANCE = 1.0 / 3.0;
    public static final int DEFAULT_PACK_SIZE = 11;
    public static final int DEFAULT_DAILY_PACK_CAP = 10;
    public static final List<String> DEFAULT_SHOP_SETS = List.of("cobblemontcg:base1", "cobblemontcg:base2");
    public static final int DEFAULT_CARD_DEALER_PRICE = 5;
    public static final int DEFAULT_CARD_DEALER_MAX_USES = 3;
    public static final int DEFAULT_WANDERING_TRADER_PRICE = 8;
    public static final int DEFAULT_WANDERING_TRADER_MAX_USES = 1;

    public static ConfigSpec CONFIG_SPEC;

    private static ConfigValue<Double> holoChance;
    private static ConfigValue<Integer> packSize;
    private static ConfigValue<Boolean> soundsEnabled;
    private static ConfigValue<Boolean> rewardsEnabled;
    private static ConfigValue<Integer> dailyPackCap;
    private static ConfigValue<Boolean> captureRewards;
    private static ConfigValue<Boolean> levelUpRewards;
    private static ConfigValue<Boolean> dexRewards;
    private static ConfigValue<List<String>> shopSets;
    private static ConfigValue<Boolean> cardDealerEnabled;
    private static ConfigValue<Integer> cardDealerPrice;
    private static ConfigValue<Integer> cardDealerMaxUses;
    private static ConfigValue<Boolean> wanderingTraderEnabled;
    private static ConfigValue<Integer> wanderingTraderPrice;
    private static ConfigValue<Integer> wanderingTraderMaxUses;

    private TcgConfig() {
    }

    public static void init() {
        if (CONFIG_SPEC != null) {
            return;
        }
        Constants.LOG.info("Registering common config.");
        ConfigBuilder builder = ConfigSpec.builder(Constants.MODID, ConfigFormat.TOML).watchForChanges();

        holoChance = builder.defineDouble("packs.holoChance", DEFAULT_HOLO_CHANCE, 0.0, 1.0, "Chance that the rare slot of a pack is a holo rare (0 to 1). Default is about 1 in 3, like the real Base Set");
        packSize = builder.defineInt("packs.packSize", DEFAULT_PACK_SIZE, 1, 64, "Cards per pack. Extra cards come from, and missing cards are taken from, the last slot of the set (commons)");
        soundsEnabled = builder.defineBoolean("effects.soundsEnabled", true, "Play a sound when a pack is opened");
        rewardsEnabled = builder.defineBoolean("rewards.enabled", true, "Allow reward triggers (capture, level up, Pokédex progress) to give packs. Commands always work");
        dailyPackCap = builder.defineInt("rewards.dailyPackCap", DEFAULT_DAILY_PACK_CAP, 0, 10000, "Maximum reward packs a player can receive per day (UTC). 0 means no limit. Commands are not limited");

        captureRewards = builder.defineBoolean("rewards.triggers.capture", true, "Give packs for catching Pokémon (needs Cobblemon)");
        levelUpRewards = builder.defineBoolean("rewards.triggers.levelUp", true, "Give packs for Pokémon level milestones (needs Cobblemon)");
        dexRewards = builder.defineBoolean("rewards.triggers.dexProgress", true, "Give packs for Pokédex progress milestones (needs Cobblemon)");

        shopSets = builder.defineList("shop.sets", DEFAULT_SHOP_SETS, "Sets of the booster packs sold by villagers, oldest first. The Card Dealer sells the first set as a Novice, "
                + "the second from Apprentice, the third from Journeyman and so on (up to 5 sets, one per villager level). Wandering traders offer one of them at random",
                v -> v instanceof String s && ResourceLocation.tryParse(s) != null);
        cardDealerEnabled = builder.defineBoolean("shop.cardDealer.enabled", true, "Card Dealer villagers sell booster packs. Only affects villagers that get their trades after the change");
        cardDealerPrice = builder.defineInt("shop.cardDealer.price", DEFAULT_CARD_DEALER_PRICE, 1, 64, "Emeralds per booster pack at the Card Dealer");
        cardDealerMaxUses = builder.defineInt("shop.cardDealer.maxUses", DEFAULT_CARD_DEALER_MAX_USES, 1, 64, "Booster packs a Card Dealer sells before it needs to restock");
        wanderingTraderEnabled = builder.defineBoolean("shop.wanderingTrader.enabled", true, "Wandering traders can offer a booster pack. Only affects traders that spawn after the change");
        wanderingTraderPrice = builder.defineInt("shop.wanderingTrader.price", DEFAULT_WANDERING_TRADER_PRICE, 1, 64, "Emeralds per booster pack at the wandering trader");
        wanderingTraderMaxUses = builder.defineInt("shop.wanderingTrader.maxUses", DEFAULT_WANDERING_TRADER_MAX_USES, 1, 64, "Booster packs a wandering trader sells (wandering traders never restock)");

        CONFIG_SPEC = builder.build();
    }

    public static double holoChance() {
        return holoChance == null ? DEFAULT_HOLO_CHANCE : holoChance.get();
    }

    public static int packSize() {
        return packSize == null ? DEFAULT_PACK_SIZE : packSize.get();
    }

    public static boolean soundsEnabled() {
        return soundsEnabled == null || soundsEnabled.get();
    }

    public static boolean rewardsEnabled() {
        return rewardsEnabled == null || rewardsEnabled.get();
    }

    public static int dailyPackCap() {
        return dailyPackCap == null ? DEFAULT_DAILY_PACK_CAP : dailyPackCap.get();
    }

    public static boolean captureRewardsEnabled() {
        return captureRewards == null || captureRewards.get();
    }

    public static boolean levelUpRewardsEnabled() {
        return levelUpRewards == null || levelUpRewards.get();
    }

    public static boolean dexRewardsEnabled() {
        return dexRewards == null || dexRewards.get();
    }

    /**
     * @return the shop sets in villager level order, as set ids like {@code cobblemontcg:base1}
     */
    public static List<String> shopSets() {
        return shopSets == null ? DEFAULT_SHOP_SETS : shopSets.get();
    }

    public static boolean cardDealerEnabled() {
        return cardDealerEnabled == null || cardDealerEnabled.get();
    }

    public static int cardDealerPrice() {
        return cardDealerPrice == null ? DEFAULT_CARD_DEALER_PRICE : cardDealerPrice.get();
    }

    public static int cardDealerMaxUses() {
        return cardDealerMaxUses == null ? DEFAULT_CARD_DEALER_MAX_USES : cardDealerMaxUses.get();
    }

    public static boolean wanderingTraderEnabled() {
        return wanderingTraderEnabled == null || wanderingTraderEnabled.get();
    }

    public static int wanderingTraderPrice() {
        return wanderingTraderPrice == null ? DEFAULT_WANDERING_TRADER_PRICE : wanderingTraderPrice.get();
    }

    public static int wanderingTraderMaxUses() {
        return wanderingTraderMaxUses == null ? DEFAULT_WANDERING_TRADER_MAX_USES : wanderingTraderMaxUses.get();
    }
}
