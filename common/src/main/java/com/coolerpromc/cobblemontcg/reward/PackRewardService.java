package com.coolerpromc.cobblemontcg.reward;

import com.coolerpromc.cobblemontcg.config.TcgConfig;
import com.coolerpromc.cobblemontcg.platform.Services;
import com.coolerpromc.cobblemontcg.tcg.data.TcgDataManager;
import com.coolerpromc.cobblemontcg.tcg.set.TcgSet;
import com.coolerpromc.cobblemontcg.util.TcgStacks;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.item.ItemStack;

import java.time.LocalDate;
import java.time.ZoneOffset;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
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

        // Like real packs, every pack gets a random wrapper; packs with the same wrapper stack.
        List<String> wrappers = set.get().wrappers();
        Map<String, Integer> perWrapper = new LinkedHashMap<>();
        for (int i = 0; i < granted; i++) {
            perWrapper.merge(wrappers.get(player.getRandom().nextInt(wrappers.size())), 1, Integer::sum);
        }
        perWrapper.forEach((wrapper, count) -> {
            int remaining = count;
            while (remaining > 0) {
                ItemStack stack = TcgStacks.pack(set.get(), wrapper, 1);
                int size = Math.min(remaining, stack.getMaxStackSize());
                stack.setCount(size);
                giveOrDrop(player, stack);
                remaining -= size;
            }
        });
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
