package com.coolerpromc.cobblemontcg.reward;

import com.coolerpromc.cobblemontcg.config.TcgConfig;
import com.coolerpromc.cobblemontcg.platform.Services;
import com.coolerpromc.cobblemontcg.tcg.data.TcgDataManager;
import com.coolerpromc.cobblemontcg.tcg.set.SetDefinition;
import com.coolerpromc.cobblemontcg.tcg.set.TcgSet;
import com.coolerpromc.cobblemontcg.util.TcgStacks;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.item.ItemStack;

import java.time.LocalDate;
import java.time.ZoneOffset;
import java.util.Optional;

/**
 * Single entry point for handing booster packs to players, used by commands and future reward triggers.
 */
public final class PackRewardService {
    private PackRewardService() {
    }

    /**
     * @return how many packs the player actually received
     */
    public static int grantPack(ServerPlayer player, ResourceLocation setId, int amount, PackSource source) {
        Optional<TcgSet> set = TcgDataManager.SERVER.set(setId);
        if (set.isEmpty() || amount <= 0) {
            return 0;
        }

        int granted = amount;
        if (source.isReward()) {
            if (!TcgConfig.rewardsEnabled()) {
                return 0;
            }
            granted = applyDailyCap(player, amount);
            if (granted <= 0) {
                return 0;
            }
        }

        String variant = set.get().definition().wrappers().stream().findFirst().orElse(SetDefinition.DEFAULT_WRAPPER);
        int remaining = granted;
        while (remaining > 0) {
            ItemStack stack = TcgStacks.pack(setId, variant, 1);
            int count = Math.min(remaining, stack.getMaxStackSize());
            stack.setCount(count);
            giveOrDrop(player, stack);
            remaining -= count;
        }
        return granted;
    }

    public static void giveOrDrop(ServerPlayer player, ItemStack stack) {
        player.getInventory().add(stack);
        if (!stack.isEmpty()) {
            player.drop(stack, false);
        }
    }

    private static int applyDailyCap(ServerPlayer player, int amount) {
        int cap = TcgConfig.dailyPackCap();
        long today = today();
        DailyPackData data = Services.PLAYER_DATA.getDailyPackData(player);
        int allowed = cap <= 0 ? amount : Math.min(amount, cap - data.countOn(today));
        if (allowed > 0) {
            Services.PLAYER_DATA.setDailyPackData(player, data.add(today, allowed));
        }
        return allowed;
    }

    public static long today() {
        return LocalDate.now(ZoneOffset.UTC).toEpochDay();
    }
}
