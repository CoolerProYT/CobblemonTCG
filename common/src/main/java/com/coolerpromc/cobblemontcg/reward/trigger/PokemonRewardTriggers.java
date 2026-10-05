package com.coolerpromc.cobblemontcg.reward.trigger;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.config.TcgConfig;
import com.coolerpromc.cobblemontcg.reward.PackSource;
import com.coolerpromc.cobblemontcg.reward.RewardContext;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerPlayer;

import java.util.function.BooleanSupplier;

public class PokemonRewardTriggers {
    public static final SimpleTrigger CAPTURE = new SimpleTrigger(Constants.id("capture"), PackSource.CAPTURE, TcgConfig::captureRewardsEnabled);
    public static final SimpleTrigger LEVEL_UP = new SimpleTrigger(Constants.id("level_up"), PackSource.LEVEL_UP, TcgConfig::levelUpRewardsEnabled);
    public static final SimpleTrigger DEX_PROGRESS = new SimpleTrigger(Constants.id("dex_progress"), PackSource.DEX_PROGRESS, TcgConfig::dexRewardsEnabled);

    private static boolean registered;

    public static synchronized void register() {
        if (registered) {
            return;
        }
        registered = true;
        RewardTriggerRegistry.register(CAPTURE);
        RewardTriggerRegistry.register(LEVEL_UP);
        RewardTriggerRegistry.register(DEX_PROGRESS);
        Constants.LOG.info("Cobblemon found, registered Pokémon reward triggers");
    }

    public static void onCapture(ServerPlayer player, String species, int level, boolean shiny, boolean firstCatch) {
        CAPTURE.fire(RewardContext.capture(player, species, level, shiny, firstCatch));
    }

    public static void onLevelUp(ServerPlayer player, String species, int oldLevel, int newLevel, boolean shiny) {
        LEVEL_UP.fire(RewardContext.levelUp(player, species, oldLevel, newLevel, shiny));
    }

    public static void onDexProgress(ServerPlayer player, String species, int entries, int total) {
        DEX_PROGRESS.fire(RewardContext.dexProgress(player, species, entries, total));
    }

    public record SimpleTrigger(ResourceLocation id, PackSource source, BooleanSupplier toggle) implements RewardTrigger {
        @Override
        public boolean enabled() {
            return toggle.getAsBoolean();
        }
    }
}
