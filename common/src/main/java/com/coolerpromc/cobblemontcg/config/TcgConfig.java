package com.coolerpromc.cobblemontcg.config;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.coolerconfig.config.ConfigBuilder;
import com.coolerpromc.coolerconfig.config.ConfigFormat;
import com.coolerpromc.coolerconfig.config.ConfigSpec;
import com.coolerpromc.coolerconfig.config.ConfigValue;

/**
 * The one place config values are read from. Getters return the defaults until {@link #init()} has run.
 */
public final class TcgConfig {
    public static final double DEFAULT_HOLO_CHANCE = 1.0 / 3.0;
    public static final int DEFAULT_PACK_SIZE = 11;
    public static final int DEFAULT_DAILY_PACK_CAP = 10;

    public static ConfigSpec CONFIG_SPEC;

    private static ConfigValue<Double> holoChance;
    private static ConfigValue<Integer> packSize;
    private static ConfigValue<Boolean> soundsEnabled;
    private static ConfigValue<Boolean> rewardsEnabled;
    private static ConfigValue<Integer> dailyPackCap;
    private static ConfigValue<Boolean> captureRewards;
    private static ConfigValue<Boolean> levelUpRewards;
    private static ConfigValue<Boolean> dexRewards;

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
}
